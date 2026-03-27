"""
Session management for K-Mirror conversations.

Handles session lifecycle, state persistence, and context loading.
"""

import uuid
from datetime import datetime
from typing import Optional
from pathlib import Path

from state import KMirrorState
from db import UnlearnDB
from pattern_echo import PatternEchoDetector
from langchain_core.messages import HumanMessage, AIMessage


class Session:
    """Represents a single conversation session."""

    def __init__(
        self,
        session_id: Optional[str] = None,
        db_path: str = "data/unlearn.db"
    ):
        """
        Initialize a session.

        Args:
            session_id: Unique session identifier (generated if not provided)
            db_path: Path to SQLite database
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.db_path = db_path

        # Initialize state
        self.state = KMirrorState(
            messages=[],
            session_id=self.session_id,
            turn_number=0,
            depth_level=0
        )

        # Pattern echo detector (per-session)
        self.echo_detector = PatternEchoDetector()

        # Load context from previous sessions
        self._load_context()

    def _load_context(self):
        """Load open inquiries and dissolved principles from previous sessions."""
        try:
            with UnlearnDB(self.db_path) as db:
                # Load open (deflected) inquiries as context
                open_inquiries = db.get_open_inquiries()
                if open_inquiries:
                    self.state.open_inquiries = [q.question_text for q in open_inquiries]

                # Load dissolved (seen-through) principles
                dissolved = db.get_all_dissolved()
                if dissolved:
                    self.state.dissolved_principles = [(p.principle, p.confidence) for p in dissolved]
        except Exception as e:
            print(f"Warning: Could not load context: {e}")

    def add_message(self, content: str, role: str = "user") -> None:
        """
        Add a message to the conversation.

        Args:
            content: Message content
            role: "user" or "assistant"
        """
        if role == "user":
            message = HumanMessage(content=content)
        else:
            message = AIMessage(content=content)

        self.state.messages.append(message)
        self.state.turn_number += 1
        self.updated_at = datetime.now()

    def save_question(self, question_text: str, principle_id: int, outcome: str = "unknown") -> None:
        """
        Save a question to the anti-memory database.

        Args:
            question_text: The question asked
            principle_id: ID of the principle used
            outcome: "explored", "deflected", "seen", "surface", or "unknown"
        """
        try:
            with UnlearnDB(self.db_path) as db:
                db.record_question(
                    session_id=self.session_id,
                    question_text=question_text,
                    principle=principle_id,
                    context_hint="; ".join(self.state.context_words)
                )
                if outcome != "unknown":
                    db.update_question_outcome(question_text, outcome)
        except Exception as e:
            print(f"Warning: Could not save question: {e}")

    def save_dissolution(self, principle_id: int, confidence: float) -> None:
        """
        Save that a principle was seen through.

        Args:
            principle_id: ID of principle seen
            confidence: 0-1 confidence that it was genuinely seen
        """
        try:
            with UnlearnDB(self.db_path) as db:
                db.record_dissolution(principle_id, confidence)
        except Exception as e:
            print(f"Warning: Could not save dissolution: {e}")

    def end_session(self) -> dict:
        """
        End the session and return summary.

        Returns:
            Session summary with stats
        """
        self.echo_detector.reset()

        summary = {
            "session_id": self.session_id,
            "duration": (self.updated_at - self.created_at).total_seconds(),
            "turns": self.state.turn_number,
            "patterns_explored": self.state.current_patterns,
            "depth_reached": self.state.depth_level,
            "message_count": len(self.state.messages),
        }

        return summary

    def get_context_string(self) -> str:
        """Get context string for LLM (open inquiries, dissolved principles)."""
        context_parts = []

        if self.state.open_inquiries:
            context_parts.append(f"Open inquiries from before: {'; '.join(self.state.open_inquiries)}")

        if self.state.dissolved_principles:
            dissolved_str = ", ".join([
                f"Principle {p[0]} (confidence {p[1]:.0%})"
                for p in self.state.dissolved_principles[:3]
            ])
            context_parts.append(f"Principles you've seen through: {dissolved_str}")

        return " ".join(context_parts) if context_parts else ""

    def to_dict(self) -> dict:
        """Convert session to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "turn_number": self.state.turn_number,
            "depth_level": self.state.depth_level,
            "messages": [
                {
                    "role": msg.__class__.__name__.replace("Message", "").lower(),
                    "content": msg.content
                }
                for msg in self.state.messages
            ],
            "patterns": [p.value for p in self.state.current_patterns],
            "principles": self.state.matched_principles,
        }


class SessionManager:
    """Manage multiple sessions and session history."""

    def __init__(self, db_path: str = "data/unlearn.db", sessions_dir: str = "data/sessions"):
        """Initialize session manager."""
        self.db_path = db_path
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.current_session: Optional[Session] = None

    def create_session(self, session_id: Optional[str] = None) -> Session:
        """Create a new session."""
        session = Session(session_id=session_id, db_path=self.db_path)
        self.current_session = session
        return session

    def load_session(self, session_id: str) -> Optional[Session]:
        """Load an existing session by ID."""
        session_file = self.sessions_dir / f"{session_id}.json"
        if session_file.exists():
            import json
            with open(session_file) as f:
                data = json.load(f)
            session = Session(session_id=session_id, db_path=self.db_path)
            # Reconstruct messages
            for msg in data.get("messages", []):
                role = msg["role"]
                content = msg["content"]
                session.add_message(content, role=role)
            self.current_session = session
            return session
        return None

    def save_session(self, session: Optional[Session] = None) -> None:
        """Save a session to disk."""
        if session is None:
            session = self.current_session
        if session is None:
            return

        session_file = self.sessions_dir / f"{session.session_id}.json"
        import json
        with open(session_file, "w") as f:
            json.dump(session.to_dict(), f, indent=2)

    def list_sessions(self) -> list:
        """List all saved sessions."""
        import json
        sessions = []
        for session_file in self.sessions_dir.glob("*.json"):
            with open(session_file) as f:
                data = json.load(f)
            sessions.append({
                "session_id": data["session_id"],
                "created_at": data["created_at"],
                "turns": data["turn_number"],
            })
        return sorted(sessions, key=lambda x: x["created_at"], reverse=True)
