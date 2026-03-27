# K-Mirror: Claude Code Integration Mode

**K-Mirror is now a Python backend service for Claude Code agents.** No direct LLM API calls - all dialogue generation happens through Claude Code.

## Quick Start

```bash
# 1. Get dependencies (already done via uv sync)
uv sync

# 2. Use in Python
from app import create_app

app = create_app()
session = app.new_session()

# Analyze user input
analysis = app.analyze_input("I feel stuck in my routine")
```

## Architecture

```
Claude Code Agent
    ↓
K-Mirror Backend (analyze_input)
├─ Pattern Detection
├─ Principle Mapping
├─ RAG Retrieval
└─ Context Preparation
    ↓
Return Analysis Dict
    ↓
Claude Generates Response
    ↓
Save to K-Mirror (save_response)
```

## API Reference

### Initialize

```python
from app import create_app

app = create_app()
session = app.new_session()
```

### Analyze Input

```python
analysis = app.analyze_input(user_input)

# Returns dict with:
# - patterns: detected patterns
# - principles: related principle IDs
# - passages: K passages
# - dialogue_approaches: suggested approaches
# - depth_level: conversation depth (0-3)
# - key_phrases, context_words, emotional_tone, etc.
```

### Save Response

```python
app.save_response(
    response_text="Your response",
    principle_id=1,
    outcome="explored"  # or "deflected", "seen"
)
```

### Session Management

```python
sessions = app.get_sessions()
session = app.load_session(session_id)
context = session.get_context_string()
summary = session.end_session()
```

## What K-Mirror Does (Backend)

✅ Pattern Recognition (12 psychological patterns)
✅ Principle Mapping (12 K principles)
✅ RAG Retrieval (K passages from ChromaDB)
✅ Echo Detection (recurring patterns)
✅ Insight Assessment (genuine vs intellectual)
✅ Session Tracking (save/load conversations)
✅ Anti-Memory System (TTL decay)

## What Claude Does (Agent)

✅ Dialogue Generation
✅ Response Crafting
✅ Decision Making
✅ Context Understanding

## Key Features

- No API keys needed
- No direct LLM calls
- Pure Python backend
- Full control over responses
- Transparent decision-making
- Persistent conversation memory

## Example

```python
from app import create_app

app = create_app()
session = app.new_session()

# Analyze
analysis = app.analyze_input("I feel stuck")

# Claude generates response using analysis
response = "Can you observe what 'stuck' means?"

# Save
app.save_response(response, analysis['principles'][0])
```

## Status

✅ Backend fully functional
✅ No API key required
✅ Ready for Claude Code integration
✅ All analysis features working
✅ Session management operational
