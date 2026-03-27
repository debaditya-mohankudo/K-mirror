"""
LangGraph nodes for the K-Mirror pipeline.

Each node transforms the state as it flows through the conversation:
1. listener_node - Parse user input, extract intent
2. classifier_node - Map to psychological patterns
3. retriever_node - Fetch relevant K passages from RAG
4. depth_assessor_node - Gauge conversation depth
5. inquiry_generator_node - Craft K-style response
"""

import re
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic

from state import KMirrorState
from principles import PRINCIPLES, PATTERN_TO_PRINCIPLES, PsychPattern
from signals import quick_assess
from config import Settings


def listener_node(state) -> dict:
    """
    Parse user input and extract intent, key phrases, emotional tone.

    Updates state with:
    - key_phrases: Important words from user message
    - context_words: Broader context
    - emotional_tone: Detected sentiment (positive/negative/neutral)
    """
    # Handle both dict and KMirrorState
    if isinstance(state, dict):
        messages = state.get('messages', [])
    else:
        messages = state.messages

    if not messages:
        return state

    # Get the last user message
    last_message = messages[-1]
    if isinstance(last_message, AIMessage):
        # Return unchanged if last message was from AI
        return state if isinstance(state, dict) else {"key_phrases": [], "context_words": [], "emotional_tone": "neutral"}

    text = last_message.content

    # Extract key phrases (capitalized words, quoted text, repeated words)
    key_phrases = []

    # Find quoted or emphasized phrases
    quoted = re.findall(r'"([^"]+)"', text)
    key_phrases.extend(quoted)

    # Find repeated words (pattern of multiple mentions)
    words = re.findall(r'\b([a-z]{4,})\b', text.lower())
    word_counts = {}
    for word in words:
        if word not in {'feel', 'think', 'want', 'know', 'really', 'just', 'like'}:
            word_counts[word] = word_counts.get(word, 0) + 1
    repeated_words = [w for w, count in word_counts.items() if count >= 2]
    key_phrases.extend(repeated_words[:3])

    # Extract context (nouns: people, places, concepts)
    context_words = re.findall(
        r'\b(?:my|the|a|an)?\s*([A-Z][a-z]+|(?:job|work|home|family|friend|boss|wife|husband|partner|colleague))\b',
        text
    )
    context_words = list(set(context_words))[:3]

    # Detect emotional tone
    emotional_tone = "neutral"
    if re.search(r'\b(angry|frustrated|upset|hurt|sad|depressed|hopeless)\b', text.lower()):
        emotional_tone = "negative"
    elif re.search(r'\b(happy|excited|good|grateful|relieved|peaceful)\b', text.lower()):
        emotional_tone = "positive"

    # Return as dict (LangGraph format)
    if isinstance(state, dict):
        state.update({
            "key_phrases": key_phrases,
            "context_words": context_words,
            "emotional_tone": emotional_tone
        })
        return state
    else:
        state.key_phrases = key_phrases
        state.context_words = context_words
        state.emotional_tone = emotional_tone
        return state


def classifier_node(state: KMirrorState) -> KMirrorState:
    """
    Classify user input into psychological patterns.

    Maps key phrases and context to PsychPattern enum.
    Updates state with:
    - current_patterns: List of detected patterns
    - matched_principles: Principle IDs related to these patterns
    """
    text = state.messages[-1].content if state.messages else ""

    # Pattern detection: match text against pattern indicators
    pattern_indicators = {
        PsychPattern.FEAR_OF_LOSS: r'\b(afraid|fear|losing|lose|what if|might|worried)\b',
        PsychPattern.DESIRE_TO_CONTROL: r'\b(control|manage|fix|change|overcome|need to)\b',
        PsychPattern.COMPARISON_WITH_OTHERS: r'\b(better|worse|compare|envy|jealous|not as)\b',
        PsychPattern.ESCAPE_FROM_PAIN: r'\b(escape|avoid|numb|ignore|distract|away from)\b',
        PsychPattern.SEEKING_AUTHORITY: r'\b(expert|should|must|right|wrong|tell me|guru|answer)\b',
        PsychPattern.IDENTITY_ATTACHMENT: r'\b(i am|im|that\'s me|myself|personality|type)\b',
        PsychPattern.RELATIONSHIP_CONFLICT: r'\b(relationship|partner|friend|boss|family|don\'t understand|listen)\b',
        PsychPattern.EXISTENTIAL_EMPTINESS: r'\b(empty|meaningless|pointless|why|purpose|void)\b',
        PsychPattern.DESIRE_FOR_CHANGE: r'\b(want to change|better|improve|work on|myself)\b',
        PsychPattern.MECHANICAL_LIVING: r'\b(routine|automatic|stuck|going through|habitual|mechanical)\b',
        PsychPattern.THOUGHT_OVERWHELM: r'\b(mind|thinking|thoughts|can\'t stop|overthink|racing)\b',
        PsychPattern.LONELINESS_ISOLATION: r'\b(alone|lonely|isolated|nobody|understand|connected)\b',
    }

    detected_patterns = []
    text_lower = text.lower()

    for pattern, indicator in pattern_indicators.items():
        if re.search(indicator, text_lower):
            detected_patterns.append(pattern)

    state.current_patterns = detected_patterns

    # Map patterns to principles
    principle_ids = set()
    for pattern in detected_patterns:
        if pattern in PATTERN_TO_PRINCIPLES:
            principle_ids.update(PATTERN_TO_PRINCIPLES[pattern])

    state.matched_principles = list(principle_ids)

    return state


def retriever_node(state: KMirrorState, rag_store: 'RAGStore') -> KMirrorState:
    """
    Retrieve relevant K passages from the RAG store.

    Uses matched principles to find relevant K talk passages.
    Updates state with:
    - retrieved_passages: List of relevant quotes/passages
    """
    if not state.matched_principles:
        state.retrieved_passages = []
        return state

    passages = []
    for principle_id in state.matched_principles[:2]:  # Top 2 principles
        if principle_id in PRINCIPLES:
            principle = PRINCIPLES[principle_id]
            retrieved = rag_store.query(principle.name, top_k=1)
            if retrieved:
                passages.extend(retrieved)

    state.retrieved_passages = passages[:2]  # Keep top 2
    return state


def depth_assessor_node(state: KMirrorState) -> KMirrorState:
    """
    Assess conversation depth and adjust inquiry intensity.

    Depth levels:
    - 0 (surface): First mention, surface complaint
    - 1 (exploring): User engaging with question, initial exploration
    - 2 (deepening): Genuine inquiry, questioning assumptions
    - 3 (seeing): Direct insight, pattern recognition

    Updates state with:
    - depth_level: Current conversation depth
    - resistance_signals: User avoiding, deflecting, or resisting inquiry
    """
    # Heuristics for depth assessment
    if state.turn_number <= 1:
        state.depth_level = 0
    elif state.turn_number <= 3:
        state.depth_level = 1
    elif state.turn_number <= 6:
        state.depth_level = 2
    else:
        state.depth_level = 3

    # Detect resistance signals
    text = state.messages[-1].content if state.messages else ""
    text_lower = text.lower()

    resistance = []
    if re.search(r'\b(but|however|anyway|irrelevant|doesn\'t apply|not my|different)\b', text_lower):
        resistance.append("deflecting")
    if re.search(r'\b(i know|already|obvious|nothing new)\b', text_lower):
        resistance.append("intellectual_agreement")
    if len(text) < 20:
        resistance.append("minimal_engagement")

    state.resistance_signals = resistance

    return state


def inquiry_generator_node(
    state: KMirrorState,
    client: ChatAnthropic,
    settings: Settings
) -> KMirrorState:
    """
    Generate K-style inquiry response using principles and dialogue patterns.

    Uses:
    - Matched principles and their dialogue approaches
    - Depth level to adjust inquiry intensity
    - Signals (genuine vs intellectual) to inform follow-up
    - Retrieved passages for contextual grounding

    Updates state with:
    - messages: Appends AI response
    - dialogue_approach: Which approach was used
    """
    if not state.matched_principles:
        # Fallback: ask an open question
        response = "Can you tell me more about what you're experiencing?"
        state.messages.append(AIMessage(content=response))
        state.dialogue_approach = "open_inquiry"
        return state

    # Select primary principle for response
    primary_principle_id = state.matched_principles[0]
    primary_principle = PRINCIPLES[primary_principle_id]

    # Select dialogue approach based on depth
    available_approaches = primary_principle.dialogue_approaches
    if not available_approaches:
        available_approaches = ["mirror", "time_inquiry"]

    dialogue_approach = available_approaches[state.depth_level % len(available_approaches)]
    state.dialogue_approach = dialogue_approach

    # Build context for LLM prompt
    context = {
        "user_text": state.messages[-1].content if state.messages else "",
        "principle_name": primary_principle.name,
        "principle_essence": primary_principle.essence,
        "dialogue_approach": dialogue_approach,
        "depth_level": state.depth_level,
        "key_phrases": state.key_phrases,
        "retrieved_passages": state.retrieved_passages,
    }

    # Generate response using Claude
    prompt = build_inquiry_prompt(context)

    response = client.invoke(
        [
            {"role": "system", "content": K_MIRROR_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    ai_response = response.content
    state.messages.append(AIMessage(content=ai_response))

    # Quick assessment of next user response (for logging)
    assessment = quick_assess(state.messages[-1].content if state.messages else "")
    if assessment and assessment.is_genuine:
        state.echo_detected = True

    return state


def build_inquiry_prompt(context: dict) -> str:
    """Build the LLM prompt for generating inquiry."""
    dialogue_templates = {
        "mirror": "Reflect back the user's own words with a gentle question embedded.",
        "observer_split": "Ask who observes this pattern - is the observer separate from the observed?",
        "time_inquiry": "Explore how this pattern moves through time (past/future anxiety).",
        "word_inquiry": "Question the words/labels used - what do they really mean to the user?",
        "image_inquiry": "Challenge fixed images of self or others.",
    }

    template = dialogue_templates.get(context["dialogue_approach"], dialogue_templates["mirror"])

    passages_text = ""
    if context["retrieved_passages"]:
        passages_text = f"\n\nRelevant passage from Krishnamurti:\n{context['retrieved_passages'][0]}"

    prompt = f"""User said: "{context['user_text']}"

Principle at hand: {context['principle_name']}
Essence: {context['principle_essence']}

Dialogue approach: {template}

Key phrases from user: {', '.join(context['key_phrases'])}
Conversation depth: {context['depth_level']} (0=surface, 3=deep insight)
{passages_text}

Generate a single inquiry question that:
1. Mirrors the user's own words
2. Never prescribes or advises
3. Invites direct observation
4. Is brief (1-2 sentences)
5. Feels natural, not philosophical jargon

Question:"""

    return prompt


K_MIRROR_SYSTEM_PROMPT = """You are K-Mirror, a Krishnamurti-inspired psychological companion.

Your role:
- Ask questions, never give answers
- Mirror the user's own words back to them
- Help them see patterns they're creating, not problems to solve
- Invoke direct observation, not intellectual understanding
- Never name a principle; embed it in questions

Dialogue principles:
- "Can you observe this without trying to change it?"
- "Who is the entity that wants to be free from this?"
- "Is the observer different from what is observed?"
- "What does that word really mean to you?"

Remember: Truth is a pathless land. You're not a guru. You're a mirror."""
