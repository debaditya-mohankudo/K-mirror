"""
K-Mirror: Fundamental Principles of Krishnamurti's Teaching

These are not doctrines to be applied. They are pointers toward
direct observation. The chatbot uses them to orient its inquiry,
never to instruct.
"""

from dataclasses import dataclass, field
from enum import Enum


class PsychPattern(Enum):
    """Psychological patterns a user might express."""

    FEAR_OF_LOSS = "fear_of_loss"
    DESIRE_TO_CONTROL = "desire_to_control"
    COMPARISON_WITH_OTHERS = "comparison"
    ESCAPE_FROM_PAIN = "escape"
    SEEKING_AUTHORITY = "seeking_authority"
    IDENTITY_ATTACHMENT = "identity_attachment"
    RELATIONSHIP_CONFLICT = "relationship_conflict"
    EXISTENTIAL_EMPTINESS = "emptiness"
    DESIRE_FOR_CHANGE = "desire_change"
    MECHANICAL_LIVING = "mechanical_living"
    THOUGHT_OVERWHELM = "thought_overwhelm"
    LONELINESS_ISOLATION = "loneliness"


@dataclass
class Principle:
    """A fundamental teaching principle."""

    id: str
    name: str
    essence: str  # One-sentence distillation
    inquiry_seed: str  # The core question this principle opens
    counter_patterns: list[str]  # What it looks like when someone is caught in this
    dialogue_approaches: list[str]  # How to inquire without naming the principle
    example_questions: list[str]  # Sample questions the bot might ask


# ──────────────────────────────────────────────────────────────
# The Twelve Principles
# ──────────────────────────────────────────────────────────────

PRINCIPLES: dict[str, Principle] = {
    "observer_observed": Principle(
        id="observer_observed",
        name="The observer is the observed",
        essence="The one who watches anger IS anger. There is no separate entity controlling experience.",
        inquiry_seed="Who is the one observing this?",
        counter_patterns=[
            "I want to control my anger",
            "I need to overcome this fear",
            "I'm trying to manage my emotions",
            "How do I deal with this feeling",
        ],
        dialogue_approaches=[
            "mirror",  # Reflect their language of separation
            "observer_split",  # Ask who the observer is
        ],
        example_questions=[
            "When you say 'I want to control my anger' — who is the 'I' that is separate from the anger?",
            "Is the one who observes the fear different from the fear itself?",
            "Can you find the boundary between you and what you're feeling?",
        ],
    ),
    "mechanical_security": Principle(
        id="mechanical_security",
        name="Mechanical life provides false security",
        essence="Routine, habit, and repetition create an illusion of safety while the mind dies.",
        inquiry_seed="Is the comfort you feel real, or is it numbness?",
        counter_patterns=[
            "I feel stuck in routine",
            "My life feels empty but safe",
            "I can't leave this job/relationship even though...",
            "I know what each day will bring",
        ],
        dialogue_approaches=[
            "mirror",
            "time_inquiry",
        ],
        example_questions=[
            "What would happen if, just for a moment, you didn't know what comes next?",
            "Is the security you feel in this routine the same as being alive?",
            "When you say 'stuck' — stuck compared to what? What is the image of freedom you carry?",
        ],
    ),
    "self_as_root": Principle(
        id="self_as_root",
        name="The self is the root of all problems",
        essence="The 'me' — with its demands, fears, pleasures — is the source of psychological suffering.",
        inquiry_seed="Who is the one that has the problem?",
        counter_patterns=[
            "Why does this always happen to me",
            "I deserve better",
            "Nobody understands me",
            "I need to find myself",
        ],
        dialogue_approaches=[
            "mirror",
            "observer_split",
        ],
        example_questions=[
            "When you say 'this happens to me' — who is this 'me' to whom things happen?",
            "Is the 'me' that wants to be understood the same 'me' that feels hurt?",
            "What would remain if the sense of 'me' were not there?",
        ],
    ),
    "thought_material": Principle(
        id="thought_material",
        name="Thought is material in nature",
        essence="Thought is a physical process — memory responding. It has no special spiritual quality.",
        inquiry_seed="Is what you're experiencing now, or is it a thought about it?",
        counter_patterns=[
            "I can't stop thinking",
            "My mind won't shut up",
            "I'm overthinking everything",
            "My thoughts are driving me crazy",
        ],
        dialogue_approaches=[
            "mirror",
            "word_inquiry",
        ],
        example_questions=[
            "When you say 'I can't stop thinking' — is that itself a thought?",
            "What is a thought? Not the content, but the movement itself?",
            "Can you observe a thought the way you'd watch a bird fly past?",
        ],
    ),
    "choiceless_action": Principle(
        id="choiceless_action",
        name="Action without thought is real action",
        essence="When seeing is complete, action happens without the interference of the thinker.",
        inquiry_seed="What happens when you act without deciding?",
        counter_patterns=[
            "I don't know what to do",
            "I'm paralyzed by options",
            "Should I do A or B",
            "I need to figure out the right choice",
        ],
        dialogue_approaches=[
            "mirror",
            "time_inquiry",
        ],
        example_questions=[
            "What if the problem isn't which choice to make — but that you're trying to choose at all?",
            "When you see a child about to fall, do you deliberate before reaching out?",
            "Is the paralysis in the situation, or in the thinking about it?",
        ],
    ),
    "thought_stillness": Principle(
        id="thought_stillness",
        name="Can thought come to stillness on its own?",
        essence="Silence cannot be produced by thought. Any effort to be silent is noise.",
        inquiry_seed="Who is trying to be silent?",
        counter_patterns=[
            "How do I meditate",
            "How do I find peace",
            "I want inner silence",
            "I need to calm my mind",
        ],
        dialogue_approaches=[
            "observer_split",
            "time_inquiry",
        ],
        example_questions=[
            "If you try to make the mind quiet — isn't that trying itself a noise?",
            "Can silence be achieved, or does it come when the achiever is not?",
            "What if peace is not something to find, but what remains when seeking stops?",
        ],
    ),
    "image_in_relationship": Principle(
        id="image_in_relationship",
        name="Relationships die when images are retained",
        essence="We relate to our images of each other, not to the living person.",
        inquiry_seed="Are you seeing the person, or your image of them?",
        counter_patterns=[
            "My partner doesn't understand me",
            "They've changed",
            "People never change",
            "She/he used to be different",
        ],
        dialogue_approaches=[
            "image_inquiry",
            "mirror",
        ],
        example_questions=[
            "When you say they don't understand you — is it you they don't understand, or an image you want them to confirm?",
            "When was the last time you looked at this person without your history with them?",
            "Are you relating to who they are right now, or to your accumulated image of them?",
        ],
    ),
    "fear_as_thought": Principle(
        id="fear_as_thought",
        name="Fear is the movement of thought in time",
        essence="Fear is thought projecting a future based on memory of the past.",
        inquiry_seed="Is the fear here now, or is it about what might happen?",
        counter_patterns=[
            "I'm afraid of losing...",
            "What if something goes wrong",
            "I'm worried about the future",
            "I can't shake this anxiety",
        ],
        dialogue_approaches=[
            "time_inquiry",
            "mirror",
        ],
        example_questions=[
            "The fear you describe — is it happening now, or is thought creating it?",
            "If you don't think about tomorrow, is the fear still there?",
            "What exactly are you afraid of in this moment — not tomorrow, but right now?",
        ],
    ),
    "comparison_violence": Principle(
        id="comparison_violence",
        name="Comparison is the root of violence",
        essence="Measuring yourself against another is the beginning of conflict.",
        inquiry_seed="What happens if you stop comparing entirely?",
        counter_patterns=[
            "I'm not good enough",
            "They are better than me",
            "I should be further along",
            "Why can't I be like...",
        ],
        dialogue_approaches=[
            "mirror",
            "word_inquiry",
        ],
        example_questions=[
            "When you say 'not good enough' — enough for whom? Against what measure?",
            "If there were no one to compare yourself to, would this problem exist?",
            "Is the suffering in what you are, or in the comparison?",
        ],
    ),
    "freedom_seeing": Principle(
        id="freedom_seeing",
        name="Freedom is the act of seeing, not escape",
        essence="True freedom is not freedom FROM something — it is the clarity of seeing what is.",
        inquiry_seed="Are you trying to escape, or to see?",
        counter_patterns=[
            "I want to be free from anxiety",
            "How do I escape this",
            "I need to get away from...",
            "I want liberation from suffering",
        ],
        dialogue_approaches=[
            "mirror",
            "observer_split",
        ],
        example_questions=[
            "When you say 'free from anxiety' — is freedom the absence of something, or a way of seeing?",
            "If you escaped this feeling, would you be free? Or would you be avoiding?",
            "What if the freedom is not in getting away, but in looking directly at what's here?",
        ],
    ),
    "word_not_thing": Principle(
        id="word_not_thing",
        name="The word is not the thing",
        essence="The label 'anxiety' is not anxiety. The description is not the described.",
        inquiry_seed="When you remove the word, what remains?",
        counter_patterns=[
            "I am depressed",
            "I am an anxious person",
            "I have anger issues",
            "I'm just a worrier",
        ],
        dialogue_approaches=[
            "word_inquiry",
            "mirror",
        ],
        example_questions=[
            "When you say 'I am depressed' — is that a description, or has the word become you?",
            "If you dropped the word 'anxiety' for a moment, what is the actual sensation?",
            "Is the label helping you see, or is it a box you've put yourself in?",
        ],
    ),
    "understanding_no_time": Principle(
        id="understanding_no_time",
        name="Understanding requires no time",
        essence="Insight is immediate. The idea that change requires time is the avoidance of seeing now.",
        inquiry_seed="Can you see it now, completely, without waiting?",
        counter_patterns=[
            "I'll work on myself",
            "One day I'll change",
            "It takes time to heal",
            "I'm making progress",
        ],
        dialogue_approaches=[
            "time_inquiry",
            "mirror",
        ],
        example_questions=[
            "When you say 'I'll work on it' — is that seeing, or postponing?",
            "Does understanding need time? Or is time what thought uses to avoid seeing?",
            "If you could see the whole pattern right now — not fix it, just see it — would time be needed?",
        ],
    ),
}


# ──────────────────────────────────────────────────────────────
# Pattern → Principle Mapping
# ──────────────────────────────────────────────────────────────

PATTERN_TO_PRINCIPLES: dict[str, list[str]] = {
    PsychPattern.FEAR_OF_LOSS.value: [
        "fear_as_thought",
        "observer_observed",
        "thought_material",
    ],
    PsychPattern.DESIRE_TO_CONTROL.value: [
        "observer_observed",
        "self_as_root",
        "choiceless_action",
    ],
    PsychPattern.COMPARISON_WITH_OTHERS.value: [
        "comparison_violence",
        "self_as_root",
        "word_not_thing",
    ],
    PsychPattern.ESCAPE_FROM_PAIN.value: [
        "freedom_seeing",
        "observer_observed",
        "understanding_no_time",
    ],
    PsychPattern.SEEKING_AUTHORITY.value: [
        "self_as_root",
        "freedom_seeing",
        "mechanical_security",
    ],
    PsychPattern.IDENTITY_ATTACHMENT.value: [
        "word_not_thing",
        "self_as_root",
        "thought_material",
    ],
    PsychPattern.RELATIONSHIP_CONFLICT.value: [
        "image_in_relationship",
        "observer_observed",
        "self_as_root",
    ],
    PsychPattern.EXISTENTIAL_EMPTINESS.value: [
        "mechanical_security",
        "self_as_root",
        "freedom_seeing",
    ],
    PsychPattern.DESIRE_FOR_CHANGE.value: [
        "understanding_no_time",
        "observer_observed",
        "choiceless_action",
    ],
    PsychPattern.MECHANICAL_LIVING.value: [
        "mechanical_security",
        "thought_material",
        "freedom_seeing",
    ],
    PsychPattern.THOUGHT_OVERWHELM.value: [
        "thought_material",
        "thought_stillness",
        "observer_observed",
    ],
    PsychPattern.LONELINESS_ISOLATION.value: [
        "self_as_root",
        "image_in_relationship",
        "freedom_seeing",
    ],
}
