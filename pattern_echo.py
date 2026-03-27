"""
K-Mirror Unlearning Engine: Pattern Echo

Detects when the user is running the same psychological program
in different contexts within a single conversation.

This is ephemeral — nothing persists beyond the session.
Like a mirror: it reflects while you're looking, then holds nothing.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class TurnAnalysis:
    """Analysis of a single conversation turn."""

    turn: int
    text: str
    patterns: list[str]
    key_phrases: list[str]
    context_words: list[str]  # who/what is being discussed
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Echo:
    """A detected echo — same pattern, different context."""

    past_turn: int
    current_turn: int
    pattern: str
    past_context: list[str]  # e.g. ["boss", "work"]
    current_context: list[str]  # e.g. ["wife", "home"]
    past_phrases: list[str]
    current_phrases: list[str]

    def describe(self) -> str:
        """Generate a natural-language echo observation."""
        past_ctx = " and ".join(self.past_context[:2]) if self.past_context else "earlier"
        curr_ctx = " and ".join(self.current_context[:2]) if self.current_context else "now"
        return (
            f"Earlier, when talking about {past_ctx}, "
            f"and now, about {curr_ctx} — "
            f"there seems to be a similar movement."
        )


class PatternEchoDetector:
    """
    Tracks patterns within a single conversation session.
    Detects when the same psychological groove appears
    in different contexts.
    
    Example:
        Turn 3: "My boss never listens to me"
            → pattern: image_in_relationship, desire_to_control
            → context: [boss, work]
        Turn 7: "My wife doesn't hear what I'm saying"  
            → pattern: image_in_relationship, desire_to_control
            → context: [wife, home]
        → Echo detected! Same pattern, different context.
    """

    def __init__(self):
        self.turns: list[TurnAnalysis] = []
        self.echoes_surfaced: list[Echo] = []

    def record_turn(
        self,
        turn: int,
        text: str,
        patterns: list[str],
        key_phrases: list[str],
        context_words: list[str],
    ):
        """Record a turn's analysis. Called after the classifier node."""
        self.turns.append(
            TurnAnalysis(
                turn=turn,
                text=text,
                patterns=patterns,
                key_phrases=key_phrases,
                context_words=context_words,
            )
        )

    def detect_echo(
        self,
        current_turn: int,
        current_patterns: list[str],
        current_phrases: list[str],
        current_context: list[str],
        min_turn_gap: int = 2,
    ) -> Optional[Echo]:
        """
        Check if the current turn echoes a past turn.
        
        An echo requires:
        1. Overlapping psychological patterns
        2. Different context (talking about different people/situations)
        3. At least min_turn_gap turns apart (not just continuation)
        4. Not already surfaced as an echo
        
        Returns an Echo if detected, None otherwise.
        """
        for past in self.turns:
            # Must be sufficiently apart
            if current_turn - past.turn < min_turn_gap:
                continue

            # Must share at least one pattern
            pattern_overlap = set(current_patterns) & set(past.patterns)
            if not pattern_overlap:
                continue

            # Must be in a different context
            context_overlap = set(current_context) & set(past.context_words)
            if context_overlap:
                # Same context = continuation, not echo
                continue

            # Check we haven't already surfaced this exact echo
            already_surfaced = any(
                e.past_turn == past.turn and e.pattern in pattern_overlap
                for e in self.echoes_surfaced
            )
            if already_surfaced:
                continue

            # Echo detected
            echo = Echo(
                past_turn=past.turn,
                current_turn=current_turn,
                pattern=list(pattern_overlap)[0],
                past_context=past.context_words,
                current_context=current_context,
                past_phrases=past.key_phrases,
                current_phrases=current_phrases,
            )
            self.echoes_surfaced.append(echo)
            return echo

        return None

    def get_recurring_patterns(self) -> dict[str, int]:
        """
        Which patterns have appeared most often in this session?
        Not for profiling — for understanding what's alive right now.
        """
        counts: dict[str, int] = {}
        for turn in self.turns:
            for p in turn.patterns:
                counts[p] = counts.get(p, 0) + 1
        return dict(sorted(counts.items(), key=lambda x: -x[1]))

    def get_session_summary(self) -> dict:
        """Summary for the developer/debugger, not stored anywhere."""
        return {
            "total_turns": len(self.turns),
            "echoes_detected": len(self.echoes_surfaced),
            "recurring_patterns": self.get_recurring_patterns(),
            "unique_contexts": list(
                {w for t in self.turns for w in t.context_words}
            ),
        }

    def reset(self):
        """Called at session end. Everything is released."""
        self.turns.clear()
        self.echoes_surfaced.clear()
