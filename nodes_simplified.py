"""
Simplified K-Mirror nodes for Claude Code integration (analysis only, no LLM).

Each node analyzes the state and returns updated context for Claude to use.
"""

import re
from principles import PATTERN_TO_PRINCIPLES, PsychPattern


def listener_node(state):
    """Extract intent, key phrases, emotional tone from user input."""
    messages = state.get('messages', []) if isinstance(state, dict) else state.messages
    
    if not messages:
        return state
    
    text = messages[-1].content
    
    # Extract key phrases
    quoted = re.findall(r'"([^"]+)"', text)
    words = re.findall(r'\b([a-z]{4,})\b', text.lower())
    word_counts = {}
    for word in words:
        if word not in {'feel', 'think', 'want', 'know', 'really', 'just', 'like'}:
            word_counts[word] = word_counts.get(word, 0) + 1
    repeated = [w for w, c in word_counts.items() if c >= 2]
    key_phrases = quoted + repeated[:3]
    
    # Extract context words
    context_words = re.findall(
        r'\b(?:my|the|a|an)?\s*([A-Z][a-z]+|(?:job|work|home|family|friend|boss|wife|husband|partner))\b',
        text
    )
    context_words = list(set(context_words))[:3]
    
    # Emotional tone
    emotional_tone = "neutral"
    if re.search(r'\b(angry|frustrated|upset|sad|depressed|hopeless)\b', text.lower()):
        emotional_tone = "negative"
    elif re.search(r'\b(happy|excited|good|grateful|peaceful)\b', text.lower()):
        emotional_tone = "positive"
    
    result = state if isinstance(state, dict) else state.__dict__
    result.update({
        'key_phrases': key_phrases,
        'context_words': context_words,
        'emotional_tone': emotional_tone
    })
    return result


def classifier_node(state):
    """Map to psychological patterns."""
    messages = state.get('messages', []) if isinstance(state, dict) else state.messages
    text = messages[-1].content if messages else ""
    
    pattern_indicators = {
        PsychPattern.FEAR_OF_LOSS: r'\b(afraid|fear|losing|worried)\b',
        PsychPattern.DESIRE_TO_CONTROL: r'\b(control|manage|fix|change|overcome)\b',
        PsychPattern.COMPARISON_WITH_OTHERS: r'\b(better|worse|compare|jealous)\b',
        PsychPattern.ESCAPE_FROM_PAIN: r'\b(escape|avoid|numb|distract)\b',
        PsychPattern.SEEKING_AUTHORITY: r'\b(expert|should|tell me|guru)\b',
        PsychPattern.IDENTITY_ATTACHMENT: r'\b(i am|im|myself|personality)\b',
        PsychPattern.RELATIONSHIP_CONFLICT: r'\b(relationship|partner|boss|family|listen)\b',
        PsychPattern.EXISTENTIAL_EMPTINESS: r'\b(empty|meaningless|pointless|why|purpose)\b',
        PsychPattern.DESIRE_FOR_CHANGE: r'\b(want to change|better|improve|work on)\b',
        PsychPattern.MECHANICAL_LIVING: r'\b(routine|automatic|stuck|habitual)\b',
        PsychPattern.THOUGHT_OVERWHELM: r'\b(mind|thinking|overthink|racing)\b',
        PsychPattern.LONELINESS_ISOLATION: r'\b(alone|lonely|isolated|nobody)\b',
    }
    
    detected = []
    for pattern, indicator in pattern_indicators.items():
        if re.search(indicator, text.lower()):
            detected.append(pattern)
    
    # Map to principles
    principle_ids = set()
    for pattern in detected:
        if pattern in PATTERN_TO_PRINCIPLES:
            principle_ids.update(PATTERN_TO_PRINCIPLES[pattern])
    
    result = state if isinstance(state, dict) else state.__dict__
    result.update({
        'current_patterns': detected,
        'matched_principles': list(principle_ids)
    })
    return result


def retriever_node(state, rag_store):
    """Retrieve relevant K passages."""
    matched_principles = state.get('matched_principles', []) if isinstance(state, dict) else state.matched_principles
    
    passages = []
    for principle_id in matched_principles[:2]:
        retrieved = rag_store.query(f"principle {principle_id}", top_k=1)
        if retrieved:
            passages.extend(retrieved)
    
    result = state if isinstance(state, dict) else state.__dict__
    result['retrieved_passages'] = passages[:2]
    return result


def depth_assessor_node(state):
    """Assess conversation depth."""
    messages = state.get('messages', []) if isinstance(state, dict) else state.messages
    turn = len(messages) if messages else 1
    
    if turn <= 1:
        depth = 0
    elif turn <= 3:
        depth = 1
    elif turn <= 6:
        depth = 2
    else:
        depth = 3
    
    # Detect resistance
    text = messages[-1].content if messages else ""
    resistance = []
    if re.search(r'\b(but|however|anyway|irrelevant)\b', text.lower()):
        resistance.append("deflecting")
    if re.search(r'\b(i know|already|obvious)\b', text.lower()):
        resistance.append("intellectual_agreement")
    
    result = state if isinstance(state, dict) else state.__dict__
    result.update({
        'depth_level': depth,
        'resistance_signals': resistance
    })
    return result
