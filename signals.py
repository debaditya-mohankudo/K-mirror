"""
K-Mirror Unlearning Engine: Insight Signals

Distinguishes genuine seeing from intellectual agreement.
This is the most nuanced judgment in the system.

K: "The description is not the described."
Agreement with a teaching is not understanding.
Understanding is a shift in the quality of attention.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SignalType(Enum):
    """Types of signals detected in user responses."""
    
    # Genuine insight signals
    LANGUAGE_SHIFT = "language_shift"
    QUESTION_REVERSAL = "question_reversal"
    GENUINE_PAUSE = "genuine_pause"
    SELF_CORRECTION = "self_correction"
    SPONTANEOUS_SEEING = "spontaneous_seeing"
    
    # Intellectual agreement signals (not insight)
    QUICK_AGREEMENT = "quick_agreement"
    REFORMULATION = "reformulation"
    FUTURE_PROJECTION = "future_projection"
    GRATITUDE_ESCAPE = "gratitude_escape"
    SEEKING_CONFIRMATION = "seeking_confirmation"


@dataclass
class InsightAssessment:
    """Assessment of whether genuine seeing occurred."""
    
    is_genuine: bool
    confidence: float  # 0-1
    signals_detected: list[SignalType]
    reasoning: str


# Prompt template for LLM-based insight assessment
INSIGHT_ASSESSMENT_PROMPT = """You are assessing whether a person has had a genuine moment of 
psychological insight, or whether they are merely agreeing intellectually.

Context: A contemplative companion has been asking questions to help this person 
look at their own psychological patterns. The principle being explored is: {principle}

The last few exchanges were:
{recent_exchanges}

The person's latest response is:
"{user_response}"

Assess whether this response shows GENUINE SEEING or INTELLECTUAL AGREEMENT.

GENUINE SEEING looks like:
- Language shift: they stop using their old framing and speak differently
- Question reversal: they start asking their own inquiry questions 
  ("Wait, who IS the one who wants to control?")
- Self-correction mid-sentence: "I want to fix — actually, who is the one fixing?"
- Genuine surprise or pause: "...", "Oh.", "I never noticed that"
- Dropping the label: they stop saying "I am anxious" and describe the sensation directly
- Quietness: a qualitative shift toward less wordy, more direct speech

INTELLECTUAL AGREEMENT looks like:
- Quick clean summary: "So basically what you're saying is..."
- "Yes, I understand" or "That makes sense" (too fast, too neat)
- Reformulating the teaching back: "So the observer IS the observed"
- Future projection: "I'll try to remember this" or "I'll work on seeing it"
- Gratitude as closure: "Thank you, that's really helpful" (shutting down inquiry)
- Seeking confirmation: "Am I on the right track?"

Respond with ONLY a JSON object (no markdown, no backticks):
{{
    "is_genuine": true/false,
    "confidence": 0.0-1.0,
    "signals": ["signal_name", ...],
    "reasoning": "Brief explanation"
}}
"""


# Pattern-matching heuristics (fast, no LLM needed)
# These catch obvious cases before calling the LLM

INTELLECTUAL_PATTERNS = [
    # Quick agreement
    (r"(?i)^(yes|yeah|right|exactly|true|correct)", "quick_agreement"),
    (r"(?i)that makes (total |perfect |a lot of )?sense", "quick_agreement"),
    (r"(?i)^i (see|understand|get it)", "quick_agreement"),
    
    # Reformulation
    (r"(?i)so (basically|essentially|what you.re saying)", "reformulation"),
    (r"(?i)in other words", "reformulation"),
    (r"(?i)let me (rephrase|restate|summarize)", "reformulation"),
    
    # Future projection
    (r"(?i)i.ll (try|work on|remember|practice|keep)", "future_projection"),
    (r"(?i)from now on", "future_projection"),
    (r"(?i)next time i.ll", "future_projection"),
    (r"(?i)i need to (start|stop|begin|learn)", "future_projection"),
    
    # Gratitude escape
    (r"(?i)^thank(s| you)", "gratitude_escape"),
    (r"(?i)this (is|was) (really |very )?(helpful|useful|insightful)", "gratitude_escape"),
    
    # Seeking confirmation
    (r"(?i)am i (right|correct|on the right)", "seeking_confirmation"),
    (r"(?i)is that (right|correct|what you mean)", "seeking_confirmation"),
]

INSIGHT_PATTERNS = [
    # Self-correction
    (r"(?i)(wait|hold on|actually|no,? wait)", "self_correction"),
    (r"(?i)i (was about to|almost said|catch myself)", "self_correction"),
    
    # Genuine pause / surprise
    (r"^\.\.\.", "genuine_pause"),
    (r"(?i)^(oh|huh|wow|hmm)\b", "genuine_pause"),
    (r"(?i)i never (thought|noticed|realized|saw|considered)", "spontaneous_seeing"),
    
    # Question reversal
    (r"(?i)^(who|what|where) is the (one|entity|person|observer)", "question_reversal"),
    (r"(?i)then who (is|am)", "question_reversal"),
    
    # Language shift (hard to detect with regex — these are rough)
    (r"(?i)there.s (just|only) (this|the|a) (feeling|sensation|movement)", "language_shift"),
]


def quick_assess(user_response: str) -> Optional[InsightAssessment]:
    """
    Fast heuristic check. Returns an assessment if the signal 
    is strong enough; None if ambiguous (needs LLM).
    """
    import re
    
    intellectual_hits = []
    insight_hits = []
    
    for pattern, signal_name in INTELLECTUAL_PATTERNS:
        if re.search(pattern, user_response):
            intellectual_hits.append(SignalType(signal_name))
    
    for pattern, signal_name in INSIGHT_PATTERNS:
        if re.search(pattern, user_response):
            insight_hits.append(SignalType(signal_name))
    
    # Strong intellectual signal with no insight counter-signal
    if len(intellectual_hits) >= 2 and not insight_hits:
        return InsightAssessment(
            is_genuine=False,
            confidence=0.7,
            signals_detected=intellectual_hits,
            reasoning="Multiple intellectual agreement patterns detected",
        )
    
    # Strong insight signal
    if len(insight_hits) >= 2 and not intellectual_hits:
        return InsightAssessment(
            is_genuine=True,
            confidence=0.6,
            signals_detected=insight_hits,
            reasoning="Multiple genuine seeing signals detected",
        )
    
    # Ambiguous — needs LLM assessment
    return None
