# K-Mirror: Detailed Usage Examples

Complete examples of how to use K-Mirror, from basic CLI to programmatic usage.

---

## Table of Contents

1. [CLI Usage](#cli-usage)
2. [Programmatic Usage](#programmatic-usage)
3. [Working with Sessions](#working-with-sessions)
4. [Advanced Features](#advanced-features)
5. [Real Conversation Examples](#real-conversation-examples)

---

## CLI Usage

### Starting K-Mirror

```bash
# Option 1: With uv (recommended)
uv run main.py

# Option 2: With activated venv
source .venv/bin/activate
python3 main.py

# Option 3: Direct command (after installation)
k-mirror
```

### Basic Conversation

```
Welcome to K-Mirror!

Session ID: abc12345-6789-abcd-ef01-234567890abc

You
> I feel like I'm not making progress in my life

K-Mirror is thinking...

┌──────────────────────────────────────────────────────────────┐
│ K-Mirror                                                     │
│                                                              │
│ What does "progress" mean to you? And what makes you feel   │
│ like you're not making it?                                  │
└──────────────────────────────────────────────────────────────┘

You
> Well, I'm doing the same things every day. Nothing changes.

K-Mirror is thinking...

┌──────────────────────────────────────────────────────────────┐
│ K-Mirror                                                     │
│                                                              │
│ When you observe what happens day by day, can you see the   │
│ change? Or does the sameness have a quality of stillness?   │
└──────────────────────────────────────────────────────────────┘
```

### Using Commands

```
You
> /stats

Conversation Statistics:
┌────────────────────────┬──────────────┐
│ Metric                 │ Value        │
├────────────────────────┼──────────────┤
│ Turn                   │ 4            │
│ Depth Level            │ 1/3          │
│ Patterns               │ mechanical_l… │
│ Principles             │ 1, 2, 12     │
└────────────────────────┴──────────────┘

You
> /rag

RAG Store Statistics:
┌─────────────────────┬───────┐
│ Collection          │ Count │
├─────────────────────┼───────┤
│ Principles          │ 12    │
│ Passages            │ 12    │
│ Dialogue Patterns   │ 0     │
└─────────────────────┴───────┘

You
> /sessions

Previous Sessions:
┌──────────────┬────────────┬───────┐
│ Session ID   │ Created    │ Turns │
├──────────────┼────────────┼───────┤
│ abc12345-... │ 2026-03-25 │ 12    │
│ def67890-... │ 2026-03-24 │ 8     │
│ ghi13579-... │ 2026-03-22 │ 15    │
└──────────────┴────────────┴───────┘

You
> /load abc12345

Session loaded: abc12345-6789-abcd-ef01-234567890abc

You
> /end

Session ended.

Summary:
- Duration: 420 seconds
- Turns: 12
- Depth reached: 2/3
- Patterns explored: 3

Session saved for future reference.
```

---

## Programmatic Usage

### Simple Conversation

```python
from app import create_app

# Create app instance
app = create_app()

# Start conversation
session = app.new_session()

# Process a user input
response = app.process_input("I feel anxious about the future")
print(f"K-Mirror: {response}")

# Continue conversation
response = app.process_input("I keep thinking about things that could go wrong")
print(f"K-Mirror: {response}")

# Get statistics
print(f"Turn: {session.state.turn_number}")
print(f"Depth: {session.state.depth_level}")
print(f"Patterns: {session.state.current_patterns}")
print(f"Principles: {session.state.matched_principles}")

# End and save
summary = app.end_conversation()
print(summary)
```

### Working with Sessions

```python
from app import create_app

app = create_app()

# List previous sessions
sessions = app.get_sessions()
for session in sessions[:5]:
    print(f"{session['session_id']}: {session['turns']} turns on {session['created_at']}")

# Load a session and continue
previous_session = app.load_session(sessions[0]['session_id'])
if previous_session:
    response = app.process_input("Following up on what we discussed...")
    print(f"K-Mirror: {response}")
```

### Deep Programmatic Access

```python
from app import create_app
from session import Session

app = create_app()
session = app.new_session()

# Process input through the full pipeline
session.add_message("I feel like I'm trapped in my job", role="user")

# The compiled graph processes it through all nodes
output_state = app.compiled_graph.invoke(session.state)

# Inspect each node's output
print("=== Analysis ===")
print(f"Key Phrases: {output_state.key_phrases}")
print(f"Context Words: {output_state.context_words}")
print(f"Emotional Tone: {output_state.emotional_tone}")
print(f"Current Patterns: {output_state.current_patterns}")
print(f"Matched Principles: {output_state.matched_principles}")
print(f"Retrieved Passages: {output_state.retrieved_passages}")
print(f"Depth Level: {output_state.depth_level}")
print(f"Dialogue Approach: {output_state.dialogue_approach}")

# Save the session
app.session_manager.save_session(session)
```

---

## Working with Sessions

### Creating and Managing Sessions

```python
from session import SessionManager, Session

manager = SessionManager(db_path="data/unlearn.db")

# Create new session
session = manager.create_session()
print(f"New session: {session.session_id}")

# Add messages
session.add_message("I've been comparing myself to others a lot", role="user")
session.add_message("Can you observe this comparison without judging it?", role="assistant")

# Save to disk
manager.save_session(session)

# Load session later
loaded = manager.load_session(session.session_id)
print(f"Loaded session with {loaded.state.turn_number} turns")

# List all sessions
all_sessions = manager.list_sessions()
for s in all_sessions:
    print(f"Session {s['session_id'][:8]}... on {s['created_at']}")
```

### Session Lifecycle

```python
from session import Session
from db import UnlearnDB

session = Session(db_path="data/unlearn.db")

# The session automatically loads open inquiries
if session.state.open_inquiries:
    print("Previous unanswered questions:")
    for q in session.state.open_inquiries:
        print(f"  - {q}")

# Add conversation
session.add_message("I was thinking about that question you asked...", role="user")
session.add_message("What did you see?", role="assistant")

# Save a question to the anti-memory DB
session.save_question(
    question_text="What did you see?",
    principle_id=10,  # Freedom principle
    outcome="explored"  # or "deflected", "seen", etc.
)

# Mark a principle as seen through
session.save_dissolution(
    principle_id=10,
    confidence=0.8  # 80% confident user genuinely saw it
)

# End session
summary = session.end_session()
print(f"Session lasted {summary['duration']} seconds")
```

---

## Advanced Features

### Using the Anti-Memory Database

```python
from db import UnlearnDB
from config import Settings

settings = Settings()

with UnlearnDB(settings.sqlite_db_path) as db:

    # Record a question asked
    db.record_question(
        session_id="session_123",
        question_text="Who is the entity that wants to be free from this fear?",
        principle=1,  # Observer is the Observed
        context_hint="User mentioned fear of job loss"
    )

    # Check what's active (not expired)
    active_questions = db.get_active_questions()
    for q in active_questions:
        print(f"Q: {q.question_text}")
        print(f"  Principle: {q.principle}")
        print(f"  Expires: {q.expires_at}")

    # Questions user deflected (avoided answering)
    open_inquiries = db.get_open_inquiries()
    print(f"\n{len(open_inquiries)} questions still open")

    # Update a question's outcome
    db.update_question_outcome(
        question_text="Who is the entity...",
        outcome="explored"  # User engaged with it
    )

    # Mark a principle as seen through
    db.record_dissolution(
        principle=1,
        confidence=0.9  # Very confident
    )

    # Check dissolved principles
    dissolved = db.get_all_dissolved()
    for p in dissolved:
        print(f"Principle {p.principle}: {p.confidence:.0%} confidence (last seen: {p.last_confirmed_at})")

    # TTL decay: how much has been forgotten?
    db.decay_dissolved_patterns()

    # Get "lightness ratio" (metric of forgetting)
    stats = db.get_stats()
    print(f"Lightness ratio: {stats['lightness_ratio']:.0%}")  # % of insights forgotten

    # Run garbage collection
    db.gc_expired_questions()
```

### Working with the RAG Store

```python
from rag import RAGStore
from config import Settings

settings = Settings()
store = RAGStore(settings)

# Query for relevant passages
passages = store.query("freedom and observation", top_k=3)
for passage in passages:
    print(f"'{passage}'")

# Add custom passages
store.add_passage(
    text="The observer is not different from the observed. This is the central fact.",
    principle_id=1,
    source="Krishnamurti Talk - Observer and the Observed"
)

# Get statistics
stats = store.get_stats()
print(f"Total passages: {stats['passages_count']}")
print(f"Principles: {stats['principles_count']}")
```

### Pattern Echo Detection

```python
from pattern_echo import PatternEchoDetector, TurnAnalysis, PsychPattern
from datetime import datetime

detector = PatternEchoDetector()

# Simulate conversation
detector.record_turn(TurnAnalysis(
    turn=1,
    text="My boss doesn't listen to my ideas",
    patterns=[PsychPattern.RELATIONSHIP_CONFLICT],
    key_phrases=["boss", "listen", "ideas"],
    context_words=["work"],
    timestamp=datetime.now()
))

detector.record_turn(TurnAnalysis(
    turn=2,
    text="I find myself trying to explain but he just dismisses me",
    patterns=[PsychPattern.RELATIONSHIP_CONFLICT],
    key_phrases=["explain", "dismisses"],
    context_words=["work"],
    timestamp=datetime.now()
))

detector.record_turn(TurnAnalysis(
    turn=4,
    text="At home, my wife does the same thing. She doesn't hear me.",
    patterns=[PsychPattern.RELATIONSHIP_CONFLICT],
    key_phrases=["wife", "hear"],
    context_words=["home"],
    timestamp=datetime.now()
))

# Detect echo
echo = detector.detect_echo()
if echo:
    print(echo.describe())
    # Output: "You mentioned RELATIONSHIP_CONFLICT with your boss (turn 1)...
    #          and now the same pattern appears at home with your wife (turn 4)..."

# Get recurring patterns
patterns = detector.get_recurring_patterns()
print(f"Recurring patterns: {patterns}")
# {"RELATIONSHIP_CONFLICT": 3, "SEEKING_AUTHORITY": 1}

# Reset at session end
detector.reset()
```

### Insight Assessment

```python
from signals import quick_assess

# Test if user's response is genuine insight or intellectual agreement
responses = [
    "Oh wow, I never thought of it that way!",  # Likely intellectual
    "Wait, I see... so the fear comes from thought itself?",  # Likely genuine
    "Yes, that makes sense.",  # Likely intellectual
    "I'm noticing that I was looking for a solution when there's nothing to solve.",  # Genuine
]

for response in responses:
    assessment = quick_assess(response)
    if assessment:
        print(f"Response: '{response}'")
        print(f"  Genuine: {assessment.is_genuine}")
        print(f"  Confidence: {assessment.confidence:.0%}")
        print(f"  Signals: {assessment.signals_detected}")
        print()
```

---

## Real Conversation Examples

### Example 1: Fear Pattern

```
User:
> I'm really worried about my job. I keep thinking about what could go wrong.

K-Mirror:
> When you say "what could go wrong" — are you worried about something that is
> happening now, or about something you're imagining in the future?

User:
> Mostly imagining. The future worry.

K-Mirror:
> Is the worry there now? Or is it only when thought moves to future possibilities?

User:
> Oh... it's only when I think about it. When I'm not thinking, there's no worry.

K-Mirror:
> So fear is the movement of thought in time — from now to imagined future. Can you
> observe this movement without identifying with it?
```

**Analysis:**
- **Pattern Detected**: FEAR_OF_LOSS
- **Principles Used**: Fear as Thought (8), Understanding Requires No Time (12)
- **Dialogue Approach**: time_inquiry
- **Depth Progression**: 0 (surface) → 2 (deepening) → 3 (seeing)

---

### Example 2: Comparison Pattern

```
User:
> Everyone at work seems to have it figured out except me. I feel like I'm behind.

K-Mirror:
> Can you observe this comparison happening? Who is comparing?

User:
> I am... I guess I'm comparing myself to others.

K-Mirror:
> The part of you that compares — is that different from the part of you that
> feels "behind"? Or are they the same movement?

User:
> [Long pause]... They're the same thing. I'm doing both at once.

K-Mirror:
> When comparison stops, what remains?
```

**Analysis:**
- **Pattern**: COMPARISON_WITH_OTHERS
- **Principles**: Observer is the Observed (1), Comparison as Violence (9)
- **Dialogue Approach**: observer_split
- **Insight Quality**: Genuine (user noticed self-created division)

---

### Example 3: Identity Pattern

```
User:
> I am an anxious person. That's just how I am.

K-Mirror:
> When you say "I am anxious" — have you ever observed a moment when you're not
> anxious? Or does the label "anxious person" cover everything?

User:
> Well... sometimes I'm fine. But when I'm anxious, it feels like that's all I am.

K-Mirror:
> Is "being anxious" different from "a moment of anxiety"? When you label yourself
> with a word, does that word become the reality?

User:
> Hmm, so I'm adding another layer by calling myself an anxious person...

K-Mirror:
> What happens if you drop the word for a moment and just observe the actual feeling?
```

**Analysis:**
- **Pattern**: IDENTITY_ATTACHMENT
- **Principles**: The Word is Not the Thing (11), Observer is Observed (1)
- **Dialogue Approach**: word_inquiry
- **Outcome**: Genuine shift from identity attachment to observation

---

## Performance Tips

### Speed Up Responses
- LLM calls take 2-3s by default
- First run initializes RAG store (~10s)
- Subsequent calls are cached

### Reduce Database Size
```python
from db import UnlearnDB
from config import Settings

settings = Settings()
with UnlearnDB(settings.sqlite_db_path) as db:
    # Clean up expired questions weekly
    db.gc_expired_questions()

    # Decay insights monthly
    db.decay_dissolved_patterns()
```

### Optimize Memory Usage
- Clear sessions regularly: `rm -f data/sessions/*.json`
- ChromaDB persists automatically to disk
- Each session takes < 1MB

---

## Troubleshooting

### "No modules named langgraph"
See [SETUP_AND_USAGE.md](/SETUP_AND_USAGE.md#troubleshooting)

### Session not saving
```python
from app import create_app

app = create_app()
session = app.new_session()
# ... conversation ...
session = app.current_session  # Get reference
app.session_manager.save_session(session)  # Explicit save
```

### Pattern echo not detecting
```python
# Echoes require:
# 1. Same pattern detected in both turns
# 2. Different context_words
# 3. At least 1 turn gap

# Check:
detector.get_recurring_patterns()  # Shows pattern counts
```

### LLM API errors
- Check `.env` for valid `anthropic_api_key`
- Check account balance in Anthropic console
- Retry after 30 seconds (rate limits)

---

## Next Steps

1. **Run a session**: `uv run main.py`
2. **Explore documentation**: Read `wiki_home.md` and `CLAUDE_CLI_GUIDE.md`
3. **Extend**: Add custom K passages to RAG store
4. **Develop**: Modify dialogue approaches in `principles.py`
5. **Test**: Write tests in `tests/` directory

---

**Happy exploring! Remember: Truth is a pathless land.** 🎋
