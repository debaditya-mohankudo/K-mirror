"""
K-Mirror: Conversation State

The state that flows through the LangGraph pipeline.
Note: this state is ephemeral per-session. The unlearning
engine handles cross-session persistence separately.
"""

from dataclasses import dataclass, field
from typing import Optional

from langgraph.graph import MessagesState


class KMirrorState(MessagesState):
    """State passed between LangGraph nodes."""

    # Current turn analysis
    turn_number: int = 0
    current_patterns: list[str] = field(default_factory=list)
    key_phrases: list[str] = field(default_factory=list)
    context_words: list[str] = field(default_factory=list)
    emotional_tone: str = ""

    # Principle matching
    matched_principles: list[str] = field(default_factory=list)
    retrieved_passages: list[str] = field(default_factory=list)
    dialogue_approach: str = "mirror"

    # Depth tracking (within session)
    depth_level: int = 0  # 0=surface, 1=exploring, 2=deep, 3=seeing
    resistance_signals: list[str] = field(default_factory=list)

    # Echo detection
    echo_detected: Optional[str] = None  # Natural-language echo observation

    # Cross-session context (loaded from unlearn engine at session start)
    open_inquiries: list[str] = field(default_factory=list)  # Deflected questions still alive
    dissolved_principles: list[str] = field(default_factory=list)  # What's been seen through

    # Safety
    safety_triggered: bool = False

    # Session metadata
    session_id: str = ""
