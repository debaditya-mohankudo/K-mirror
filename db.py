"""
K-Mirror Unlearning Engine: Database Layer

The anti-memory store. Unlike traditional databases that grow,
this one is designed to shrink. Every record has a natural death.

Schema:
  asked_questions  — Questions asked by the bot, with TTL decay
  dissolved_patterns — Principles the user has seen through (sparse)
"""

import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


@dataclass
class AskedQuestion:
    id: str
    session_id: str
    question_text: str
    principle: str
    created_at: datetime
    expires_at: datetime
    decay_rate: float
    outcome: str  # explored | deflected | seen | surface | unknown
    context_hint: str  # minimal context, e.g. "work relationship"


@dataclass
class DissolvedPattern:
    id: str
    principle: str
    first_seen_at: datetime
    last_confirmed_at: Optional[datetime]
    confidence: float
    resurface_count: int


class UnlearnDB:
    """SQLite-backed anti-memory store."""

    def __init__(self, db_path: str = "./data/unlearn.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
        self._conn_obj = None

    def __enter__(self):
        """Context manager entry."""
        self._conn_obj = sqlite3.connect(
            str(self.db_path),
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        self._conn_obj.row_factory = sqlite3.Row
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self._conn_obj:
            if exc_type is None:
                self._conn_obj.commit()
            self._conn_obj.close()
        return False

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(
            str(self.db_path),
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self):
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS asked_questions (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    question_text TEXT NOT NULL,
                    principle TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    decay_rate REAL DEFAULT 1.0,
                    outcome TEXT CHECK(outcome IN (
                        'explored', 'deflected', 'seen', 
                        'surface', 'unknown'
                    )) DEFAULT 'unknown',
                    context_hint TEXT DEFAULT ''
                );

                CREATE TABLE IF NOT EXISTS dissolved_patterns (
                    id TEXT PRIMARY KEY,
                    principle TEXT NOT NULL UNIQUE,
                    first_seen_at TIMESTAMP NOT NULL,
                    last_confirmed_at TIMESTAMP,
                    confidence REAL DEFAULT 0.7,
                    resurface_count INTEGER DEFAULT 0
                );

                CREATE INDEX IF NOT EXISTS idx_questions_expires 
                    ON asked_questions(expires_at);
                CREATE INDEX IF NOT EXISTS idx_questions_principle 
                    ON asked_questions(principle);
                CREATE INDEX IF NOT EXISTS idx_dissolved_principle 
                    ON dissolved_patterns(principle);
            """)

    # ── Garbage Collection (the system gets lighter) ──────────

    def gc_expired_questions(self) -> int:
        """Remove expired questions. Returns count of removed."""
        with self._conn() as conn:
            cursor = conn.execute(
                "DELETE FROM asked_questions WHERE expires_at < ?",
                (datetime.now(),),
            )
            return cursor.rowcount

    def decay_dissolved_patterns(self, decay_rate_per_month: float = 0.05):
        """
        Monthly confidence decay on dissolved patterns.
        Even genuine insights fade if not alive.
        K: 'Understanding is always fresh. It is not a memory.'
        """
        with self._conn() as conn:
            patterns = conn.execute(
                "SELECT * FROM dissolved_patterns"
            ).fetchall()
            
            for row in patterns:
                last_confirmed = datetime.fromisoformat(
                    row["last_confirmed_at"]
                ) if row["last_confirmed_at"] else datetime.fromisoformat(
                    row["first_seen_at"]
                )
                months_since = (datetime.now() - last_confirmed).days / 30
                new_confidence = row["confidence"] * (
                    (1 - decay_rate_per_month) ** months_since
                )

                if new_confidence < 0.1:
                    # Pattern has faded from memory — as it should
                    conn.execute(
                        "DELETE FROM dissolved_patterns WHERE id = ?",
                        (row["id"],),
                    )
                else:
                    conn.execute(
                        "UPDATE dissolved_patterns SET confidence = ? WHERE id = ?",
                        (new_confidence, row["id"]),
                    )

    # ── Asked Questions ───────────────────────────────────────

    def record_question(
        self,
        session_id: str,
        question_text: str,
        principle: str,
        context_hint: str = "",
        ttl_days: int = 14,
    ) -> AskedQuestion:
        """Record a question the bot asked. It will auto-expire."""
        now = datetime.now()
        q = AskedQuestion(
            id=str(uuid.uuid4()),
            session_id=session_id,
            question_text=question_text,
            principle=principle,
            created_at=now,
            expires_at=now + timedelta(days=ttl_days),
            decay_rate=1.0,
            outcome="unknown",
            context_hint=context_hint,
        )
        with self._conn() as conn:
            conn.execute(
                """INSERT INTO asked_questions 
                   (id, session_id, question_text, principle, 
                    created_at, expires_at, decay_rate, outcome, context_hint)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    q.id, q.session_id, q.question_text, q.principle,
                    q.created_at, q.expires_at, q.decay_rate,
                    q.outcome, q.context_hint,
                ),
            )
        return q

    def update_question_outcome(
        self, question_id: str, outcome: str, ttl_override_days: Optional[int] = None
    ):
        """Update the outcome and optionally adjust TTL."""
        with self._conn() as conn:
            if ttl_override_days is not None:
                row = conn.execute(
                    "SELECT created_at FROM asked_questions WHERE id = ?",
                    (question_id,),
                ).fetchone()
                if row:
                    created = datetime.fromisoformat(row["created_at"])
                    new_expires = created + timedelta(days=ttl_override_days)
                    conn.execute(
                        """UPDATE asked_questions 
                           SET outcome = ?, expires_at = ? WHERE id = ?""",
                        (outcome, new_expires, question_id),
                    )
                    return
            conn.execute(
                "UPDATE asked_questions SET outcome = ? WHERE id = ?",
                (outcome, question_id),
            )

    def get_active_questions(
        self, principle: Optional[str] = None
    ) -> list[AskedQuestion]:
        """Get non-expired questions, optionally filtered by principle."""
        with self._conn() as conn:
            if principle:
                rows = conn.execute(
                    """SELECT * FROM asked_questions 
                       WHERE expires_at > ? AND principle = ?
                       ORDER BY created_at DESC""",
                    (datetime.now(), principle),
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT * FROM asked_questions 
                       WHERE expires_at > ?
                       ORDER BY created_at DESC""",
                    (datetime.now(),),
                ).fetchall()
            return [self._row_to_question(r) for r in rows]

    def get_open_inquiries(self) -> list[AskedQuestion]:
        """Get questions that were deflected and haven't expired.
        These are the unresolved inquiries worth gently revisiting."""
        with self._conn() as conn:
            rows = conn.execute(
                """SELECT * FROM asked_questions 
                   WHERE expires_at > ? AND outcome = 'deflected'
                   ORDER BY created_at ASC""",
                (datetime.now(),),
            ).fetchall()
            return [self._row_to_question(r) for r in rows]

    # ── Dissolved Patterns ────────────────────────────────────

    def record_dissolution(self, principle: str, confidence: float = 0.7):
        """Mark a principle as seen through."""
        with self._conn() as conn:
            existing = conn.execute(
                "SELECT * FROM dissolved_patterns WHERE principle = ?",
                (principle,),
            ).fetchone()

            if existing:
                new_confidence = min(1.0, existing["confidence"] + 0.1)
                conn.execute(
                    """UPDATE dissolved_patterns 
                       SET last_confirmed_at = ?, confidence = ?
                       WHERE principle = ?""",
                    (datetime.now(), new_confidence, principle),
                )
            else:
                conn.execute(
                    """INSERT INTO dissolved_patterns 
                       (id, principle, first_seen_at, last_confirmed_at, confidence)
                       VALUES (?, ?, ?, ?, ?)""",
                    (
                        str(uuid.uuid4()),
                        principle,
                        datetime.now(),
                        datetime.now(),
                        confidence,
                    ),
                )

    def record_resurface(self, principle: str):
        """
        A 'seen' pattern has resurfaced. The dissolution was
        intellectual, not real. Reduce confidence.
        """
        with self._conn() as conn:
            existing = conn.execute(
                "SELECT * FROM dissolved_patterns WHERE principle = ?",
                (principle,),
            ).fetchone()

            if existing:
                new_confidence = existing["confidence"] * 0.5
                new_count = existing["resurface_count"] + 1

                if new_confidence < 0.2:
                    # The seeing was partial — remove the marker
                    conn.execute(
                        "DELETE FROM dissolved_patterns WHERE principle = ?",
                        (principle,),
                    )
                else:
                    conn.execute(
                        """UPDATE dissolved_patterns 
                           SET confidence = ?, resurface_count = ?
                           WHERE principle = ?""",
                        (new_confidence, new_count, principle),
                    )

    def get_dissolved(self, principle: str) -> Optional[DissolvedPattern]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM dissolved_patterns WHERE principle = ?",
                (principle,),
            ).fetchone()
            return self._row_to_dissolved(row) if row else None

    def get_all_dissolved(self) -> list[DissolvedPattern]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM dissolved_patterns ORDER BY confidence DESC"
            ).fetchall()
            return [self._row_to_dissolved(r) for r in rows]

    # ── Stats (for developer insight, not user profiling) ─────

    def get_stats(self) -> dict:
        """How light is the system? This should trend toward emptiness."""
        with self._conn() as conn:
            active_q = conn.execute(
                "SELECT COUNT(*) as c FROM asked_questions WHERE expires_at > ?",
                (datetime.now(),),
            ).fetchone()["c"]
            total_q = conn.execute(
                "SELECT COUNT(*) as c FROM asked_questions"
            ).fetchone()["c"]
            dissolved = conn.execute(
                "SELECT COUNT(*) as c FROM dissolved_patterns"
            ).fetchone()["c"]
            return {
                "active_questions": active_q,
                "total_questions_ever": total_q,
                "expired_and_gone": total_q - active_q,
                "dissolved_patterns": dissolved,
                "lightness_ratio": 1 - (active_q / max(total_q, 1)),
            }

    # ── Helpers ────────────────────────────────────────────────

    def _row_to_question(self, row) -> AskedQuestion:
        return AskedQuestion(
            id=row["id"],
            session_id=row["session_id"],
            question_text=row["question_text"],
            principle=row["principle"],
            created_at=datetime.fromisoformat(row["created_at"]),
            expires_at=datetime.fromisoformat(row["expires_at"]),
            decay_rate=row["decay_rate"],
            outcome=row["outcome"],
            context_hint=row["context_hint"],
        )

    def _row_to_dissolved(self, row) -> DissolvedPattern:
        return DissolvedPattern(
            id=row["id"],
            principle=row["principle"],
            first_seen_at=datetime.fromisoformat(row["first_seen_at"]),
            last_confirmed_at=(
                datetime.fromisoformat(row["last_confirmed_at"])
                if row["last_confirmed_at"]
                else None
            ),
            confidence=row["confidence"],
            resurface_count=row["resurface_count"],
        )
