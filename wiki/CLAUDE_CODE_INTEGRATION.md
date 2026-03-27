# K-Mirror + Claude Code Integration Guide

K-Mirror now works as a **backend analysis engine** - Claude Code handles all dialogue generation.

## Architecture

```
User Input (in Claude Code)
    ↓
K-Mirror Analysis Backend
├─ Pattern Detection
├─ Principle Mapping
├─ Echo Detection
├─ RAG Retrieval
└─ Context Preparation
    ↓
Return Structured Context
    ↓
Claude (Agent) Generates Response
    ↓
Save to K-Mirror Database
```

## How It Works

K-Mirror no longer calls the LLM. Instead, it:
1. Analyzes user input
2. Detects psychological patterns
3. Finds related principles
4. Retrieves relevant K passages
5. Returns all context to Claude Code
6. Claude Code generates the response
7. Response gets saved back to K-Mirror

## Using K-Mirror in Claude Code

### 1. Analyze User Input

```python
from app import create_app

app = create_app()
session = app.new_session()

# Analyze input
analysis = app.analyze_input(
    user_input="I feel stuck in my routine"
)

print(analysis)
# Returns:
# {
#     'patterns': [PsychPattern.MECHANICAL_LIVING, ...],
#     'principles': [1, 2, 12],
#     'passages': ['Mechanical life...', ...],
#     'dialogue_approaches': ['mirror', 'time_inquiry'],
#     'depth_level': 0,
#     'key_phrases': ['stuck', 'routine'],
#     'emotional_tone': 'negative'
# }
```

### 2. Claude Generates Response

Claude uses the analysis to craft a Socratic inquiry:

```
Based on K-Mirror analysis:
- Patterns: mechanical_living, existential_emptiness
- Principle: "Mechanical life gives false security" 
- Approach: mirror + time_inquiry

Generate a brief Socratic question...
```

Claude might respond:
> "You mention being stuck in routine. Can you observe what 'stuck' actually means? When you're doing these routines, are you present in them, or is your mind elsewhere?"

### 3. Save to K-Mirror

```python
# After Claude generates response
session.save_question(
    question_text="Can you observe what 'stuck' actually means?...",
    principle_id=2,
    outcome="unknown"
)

# Track if user's response shows insight
if user_shows_genuine_insight:
    session.save_dissolution(principle_id=2, confidence=0.85)
```

## API Reference

### Create App & Session

```python
from app import create_app

app = create_app()
session = app.new_session()
```

### Analyze Input

```python
analysis = app.analyze_input(user_input)
# Returns dict with:
# - patterns: List[PsychPattern]
# - principles: List[int]
# - passages: List[str]
# - dialogue_approaches: List[str]
# - depth_level: int (0-3)
# - key_phrases: List[str]
# - emotional_tone: str
# - resistance_signals: List[str]
```

### Track Questions

```python
session.save_question(
    question_text="Your question here",
    principle_id=1,
    outcome="explored"  # or deflected, seen, surface, unknown
)
```

### Track Insights

```python
session.save_dissolution(
    principle_id=1,
    confidence=0.8  # 0-1
)
```

### Session Management

```python
# List previous sessions
sessions = app.get_sessions()

# Load previous session
session = app.load_session(session_id)

# Get session context (open inquiries, dissolved principles)
context = session.get_context_string()

# End session
summary = session.end_session()
```

### Pattern Echo

```python
# Within conversation, track turns
detector = session.echo_detector

# Get recurring patterns
patterns = detector.get_recurring_patterns()
# {'MECHANICAL_LIVING': 3, 'EXISTENTIAL_EMPTINESS': 1}

# Detect if same pattern appeared
echo = detector.detect_echo()
if echo:
    print(echo.describe())
    # "You mentioned MECHANICAL_LIVING in context of work,
    #  and now in context of relationships..."
```

## Example: Full Conversation Loop

```python
from app import create_app

app = create_app()
session = app.new_session()

# Turn 1: User input
user_msg = "I keep comparing myself to others and feeling bad"

# K-Mirror analyzes
analysis = app.analyze_input(user_msg)
print(f"Patterns detected: {analysis['patterns']}")
print(f"Dialogue approach: {analysis['dialogue_approaches']}")
print(f"Related principles: {analysis['principles']}")
print(f"Relevant passages: {analysis['passages']}")

# Claude reads the analysis and generates response
claude_prompt = f"""
User said: "{user_msg}"

K-Mirror Analysis:
- Patterns: {analysis['patterns']}
- Principles: {analysis['principles']}
- Suggested approach: {analysis['dialogue_approaches'][0]}
- Key passage: {analysis['passages'][0]}
- Emotional tone: {analysis['emotional_tone']}

Generate a brief Socratic question that:
1. Mirrors the user's own words
2. Doesn't prescribe
3. Invites observation
4. Uses the suggested approach
"""

# Claude generates (via your prompt)
claude_response = "When you compare yourself to others, who is doing the comparing?"

# Save to K-Mirror
session.save_question(
    question_text=claude_response,
    principle_id=analysis['principles'][0],
    outcome="unknown"
)

# Turn 2: User response
user_response = "I guess... I'm the one doing it."

# Check for insight
from signals import quick_assess
insight = quick_assess(user_response)
if insight and insight.is_genuine:
    print(f"✓ Genuine insight detected (confidence: {insight.confidence:.0%})")
    session.save_dissolution(
        principle_id=analysis['principles'][0],
        confidence=insight.confidence
    )
else:
    print(f"Intellectual engagement (confidence: {insight.confidence:.0%})")
    session.save_question(analysis['question_text'], analysis['principles'][0], outcome="deflected")

# Continue...
```

## Example: Using in Claude Code with /run

```bash
# In Claude Code:
/run python3 analyze_input.py "I feel anxious about the future"

# analyze_input.py
import sys
from app import create_app

app = create_app()
analysis = app.analyze_input(sys.argv[1])

import json
print(json.dumps({
    'patterns': [p.value for p in analysis['patterns']],
    'principles': analysis['principles'],
    'approaches': analysis['dialogue_approaches'],
    'passages': analysis['passages'],
}, indent=2))
```

## Key Differences from Original Design

| Before | Now |
|--------|-----|
| K-Mirror calls Claude API | Claude Code calls K-Mirror |
| Dialogue hardcoded in nodes | Claude generates dialogue |
| LLM decisions in Python | LLM decisions in Claude |
| API key required | No API key needed |
| Single LLM | Your Claude session |

## What K-Mirror Still Does

✅ Pattern recognition (12 psychological patterns)
✅ Principle mapping (12 K principles)
✅ RAG retrieval (K passages from ChromaDB)
✅ Echo detection (recurring patterns)
✅ Insight assessment (genuine vs intellectual)
✅ Session management (save/load conversations)
✅ Anti-memory system (TTL decay, confidence tracking)
✅ Depth assessment (conversation progression)

## What Claude Now Does

✅ Dialogue generation (Socratic inquiry)
✅ Response crafting (using K-Mirror analysis)
✅ Decision making (which approach to use)
✅ Context understanding (full picture)

## No API Keys, No Direct LLM Calls

K-Mirror is now a pure Python library. All LLM interaction happens through Claude Code.

This gives you:
- ✅ Full control over responses
- ✅ No API key management
- ✅ Direct integration with Claude
- ✅ Ability to customize dialogue
- ✅ Transparency in all decisions
