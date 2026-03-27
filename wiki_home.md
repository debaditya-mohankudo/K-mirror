# K-Mirror Wiki Home

**Quick Links**: [Module Catalog](#module-catalog) | [Implementation Status](#implementation-status) | [How to Use](#how-to-use) | [Architecture](#architecture) | [Roadmap](#roadmap)

---

## Project Status at a Glance

**K-Mirror** is a Krishnamurti-inspired psychological companion CLI. The **domain logic is 100% implemented** (6/6 core modules complete). The **orchestration layer and CLI are 0% implemented**.

| Category | Status | Coverage |
|----------|--------|----------|
| Configuration | ✅ Complete | 100% |
| Domain Models | ✅ Complete | 100% |
| Anti-Memory DB | ✅ Complete | 100% |
| Insight Detection | ✅ Complete | 80% (heuristics done; LLM call missing) |
| LangGraph Pipeline | ❌ Not Started | 0% |
| ChromaDB Integration | ❌ Not Started | 0% |
| CLI Interface | ❌ Not Started | 0% |
| Tests | ❌ Not Started | 0% |

---

## Module Catalog

### 1. **config.py** ✅ Complete
**Purpose**: Environment-based configuration management.

**Use Case**: Load settings at application startup.

```python
from config import Settings

# Automatic via Pydantic (reads .env)
settings = Settings()

# Access configuration
api_key = settings.anthropic_api_key
db_path = settings.sqlite_db_path
ttl_days = settings.default_question_ttl_days
```

**What It Provides**:
- `Settings` class with Pydantic validation
- API keys, database paths, TTL decay rates
- Scraping defaults (jkrishnamurti.org URL, request delays)
- Logging configuration

**Status**: Production-ready. No changes needed.

---

### 2. **state.py** ✅ Complete
**Purpose**: Per-session ephemeral state for the LangGraph pipeline.

**Use Case**: Track conversation state as it flows through nodes.

```python
from state import KMirrorState
from langchain_core.messages import HumanMessage

# Create initial state for a session
state = KMirrorState(
    messages=[HumanMessage(content="I feel stuck in my job")],
    session_id="session_123",
    turn_number=1,
    depth_level=0  # surface level
)

# State updates as conversation progresses
state.turn_number += 1
state.depth_level = 1
state.current_patterns = ["MECHANICAL_LIVING", "ESCAPE_FROM_PAIN"]
state.matched_principles = [1, 2]  # Principle IDs
```

**What It Provides**:
- `KMirrorState` - Extends LangGraph's MessagesState
- Fields for: turn analysis, principle matching, depth tracking, echo detection, safety
- Integration with LangGraph message history

**Status**: Production-ready. Used by LangGraph nodes (not yet implemented).

---

### 3. **principles.py** ✅ Complete
**Purpose**: 12 Krishnamurti principles, pattern taxonomy, and dialogue templates.

**Use Case**: Map psychological patterns to principles and access inquiry seeds.

```python
from principles import PRINCIPLES, PATTERN_TO_PRINCIPLES, PsychPattern

# Get all principles
all_principles = PRINCIPLES  # Dict[int, Principle]

# Access a specific principle
principle_1 = PRINCIPLES[1]
print(principle_1.name)  # "Observer is the Observed"
print(principle_1.inquiry_seed)  # "Can you observe this pattern without immediately trying to change it?"

# Map a pattern to principles
pattern = PsychPattern.FEAR_OF_LOSS
related_principles = PATTERN_TO_PRINCIPLES[pattern]
# Returns: [1, 8, 10] (Observer/Observed, Fear as Thought, Freedom as Seeing)

# Get dialogue approaches for this principle
dialogue_templates = principle_1.dialogue_approaches
# ["mirror", "observer_split", "time_inquiry", "word_inquiry", "image_inquiry"]

# Get example questions
questions = principle_1.example_questions
```

**What It Provides**:
- 12 fully-defined Krishnamurti principles
- 12 psychological pattern types (enum)
- Deterministic pattern → principle mapping (3 principles per pattern)
- Dialogue templates for each principle
- Example questions (Socratic, non-prescriptive)

**12 Principles**:
1. Observer is the observed
2. Mechanical life gives false security
3. Self is the root of all problems
4. Thought is material in nature
5. Action without thought is real action
6. Can thought come to stillness on its own?
7. Relationships die when images are retained
8. Fear is the movement of thought in time
9. Comparison is the root of violence
10. Freedom is the act of seeing, not escape
11. The word is not the thing
12. Understanding requires no time

**Status**: Production-ready. Extend with more principles or dialogue patterns as needed.

---

### 4. **pattern_echo.py** ✅ Complete
**Purpose**: Detect recurring psychological patterns within a conversation.

**Use Case**: Identify when the same pattern appears in different contexts.

```python
from pattern_echo import PatternEchoDetector, TurnAnalysis, PsychPattern

# Create detector (per session)
detector = PatternEchoDetector()

# Record each turn as conversation progresses
detector.record_turn(TurnAnalysis(
    turn=1,
    text="My boss doesn't listen to me.",
    patterns=[PsychPattern.RELATIONSHIP_CONFLICT],
    key_phrases=["doesn't listen"],
    context_words=["boss", "work"],
    timestamp=datetime.now()
))

# Later turn: same pattern, different context
detector.record_turn(TurnAnalysis(
    turn=5,
    text="My wife doesn't hear what I'm saying.",
    patterns=[PsychPattern.RELATIONSHIP_CONFLICT],
    key_phrases=["doesn't hear"],
    context_words=["wife", "home"],
    timestamp=datetime.now()
))

# Detect the echo
echo = detector.detect_echo()
if echo:
    print(echo.describe())
    # Output: "You mentioned 'relationship conflict' with your boss (turn 1),
    #          and now the same pattern appears with your wife (turn 5).
    #          Different people, same movement."

# Get recurring patterns
patterns = detector.get_recurring_patterns()
# {"RELATIONSHIP_CONFLICT": 2, "ESCAPE_FROM_PAIN": 1}

# Reset at session end
detector.reset()
```

**What It Provides**:
- `PatternEchoDetector` - Session-scoped echo detection
- `TurnAnalysis` - Single turn snapshot (patterns, phrases, context)
- `Echo` - Echo result with `describe()` for natural language output
- Echo prevention (doesn't surface same echo twice)

**Key Design**:
- **Ephemeral** - Per-session only, reset at end
- **Semantic** - Detects pattern + context shift (same pattern ≠ echo if same context continues)
- **Dialogue-ready** - Echo has `describe()` method for natural surfacing

**Status**: Production-ready. Reset at session end to prevent memory leaks.

---

### 5. **db.py** ✅ Complete
**Purpose**: SQLite anti-memory database with TTL-based decay.

**Use Case**: Remember questions asked and principles seen, but forget them naturally.

```python
from db import UnlearnDB
from config import Settings

settings = Settings()

# Open database (context manager)
with UnlearnDB(settings.sqlite_db_path) as db:

    # Record a question asked
    db.record_question(
        session_id="session_123",
        question_text="Can you observe your anger without naming it?",
        principle=1,  # "Observer is the Observed"
        context_hint="User mentioned frustration with boss"
    )

    # Update question outcome when user responds
    db.update_question_outcome(
        question_text="Can you observe...",
        outcome="explored"  # or: "deflected", "seen", "surface", "unknown"
    )

    # Check what questions are still active (not TTL-expired)
    active = db.get_active_questions()

    # Get questions that were deflected (user avoided answering)
    open_inquiries = db.get_open_inquiries()

    # Mark a principle as "seen through"
    db.record_dissolution(
        principle=1,
        confidence=0.8  # 0-1: how certain the user saw it
    )

    # If principle resurfaces later, lower confidence (penalty for not reinforcing)
    db.record_resurface(
        principle=1
        # Confidence halved: 0.8 → 0.4
    )

    # Check what's been dissolved (seen through)
    dissolved = db.get_dissolved(principle=1)

    # Garbage collection: remove expired questions
    db.gc_expired_questions()

    # Monthly decay: confidence drops on insights not reinforced
    db.decay_dissolved_patterns()

    # Get "lightness ratio" (trend toward emptiness)
    stats = db.get_stats()
    # Returns: {"total_questions_asked": 15, "active_questions": 3,
    #           "lightness_ratio": 0.8}  # 80% forgotten
```

**What It Provides**:
- `UnlearnDB` - SQLite database interface
- `AskedQuestion` - Question record with TTL and outcome tracking
- `DissolvedPattern` - Principle seen-through with confidence decay
- **Context manager** - Proper connection handling

**Key Design** (Anti-Memory Philosophy):
- **Questions expire** - Default 14 days (configurable per outcome)
  - explored: 7 days (seen through, forget quickly)
  - deflected: 30 days (user avoided it, revisit later)
  - others: 14 days (default)
- **Confidence decays** - 5% per month by default
- **Resurface penalty** - Confidence halved if pattern returns
- **Removal threshold** - Delete from DB if confidence drops below 10%
- **Lightness ratio** - Metric of how much is forgotten (trend toward emptiness)

**Status**: Production-ready. TTL and decay rates are configurable via `.env`.

---

### 6. **signals.py** ✅ Complete (80% - LLM call missing)
**Purpose**: Distinguish genuine psychological insight from intellectual agreement.

**Use Case**: Assess whether user's response reflects real seeing or just nodding along.

```python
from signals import quick_assess, InsightAssessment

# Quick heuristic assessment (regex-based, instant)
user_response = "Oh wow, I never thought of it that way! That's really interesting."
assessment = quick_assess(user_response)

if assessment:
    print(f"Genuine: {assessment.is_genuine}")
    # False (matches INTELLECTUAL_PATTERNS)
    print(f"Confidence: {assessment.confidence}")
    # 0.95 (very confident it's intellectual agreement)
    print(f"Signals: {assessment.signals_detected}")
    # ["QUICK_AGREEMENT", "SEEKING_CONFIRMATION"]
    print(f"Reasoning: {assessment.reasoning}")
    # "Strong intellectual agreement without behavioral commitment"
else:
    print("Ambiguous - would need LLM assessment")
```

**What It Provides**:
- `quick_assess()` - Fast regex-based heuristic (no LLM cost)
- `InsightAssessment` - Result with confidence, signals, reasoning
- **Genuine signals**: LANGUAGE_SHIFT, QUESTION_REVERSAL, SELF_CORRECTION, SPONTANEOUS_SEEING, GENUINE_PAUSE
- **Intellectual signals**: QUICK_AGREEMENT, REFORMULATION, FUTURE_PROJECTION, GRATITUDE_ESCAPE, SEEKING_CONFIRMATION

**Two-Tier Strategy**:
1. **Heuristic (fast)** - Regex patterns for common intellectual agreement/insight
2. **LLM fallback** - For ambiguous cases (prompt template defined, but LLM call not implemented)

**Typical Genuine Response**:
- "I see... so it's my own fear creating this."
- "Wait, you mean I'm doing this to myself?"
- *[pause, visible reflection]*

**Typical Intellectual Response**:
- "That's a great point!"
- "So I'll just work on this over time..."
- "That explains a lot."

**Status**: 80% complete. Heuristics work. LLM call needs implementation in orchestration layer.

---

## Implementation Status

### ✅ Fully Implemented & Ready
1. **config.py** - Configuration management via `.env`
2. **state.py** - LangGraph state structure
3. **principles.py** - 12 K principles + pattern taxonomy
4. **pattern_echo.py** - Session-scoped echo detection
5. **db.py** - SQLite anti-memory with TTL decay
6. **signals.py** - Insight/intellectual assessment (heuristics complete)

### ⏳ Not Yet Implemented (Critical Path)
1. **LangGraph Nodes** (5 nodes needed):
   - **Listener** - Parse user input, extract intent
   - **Classifier** - Map input to PsychPatterns
   - **Retriever** - Fetch K passages from ChromaDB (requires RAG)
   - **Depth Assessor** - Gauge conversation depth, adjust inquiry intensity
   - **Inquiry Generator** - Craft K-style questions using principles + signals

2. **ChromaDB Integration**:
   - Vector store setup
   - Web scraper for jkrishnamurti.org talks
   - Embedding pipeline (sentence-transformers)

3. **LLM Integration**:
   - Claude API calls in signals.py assessment
   - Response generation with principle-aware prompting

4. **CLI Interface** (Rich TUI):
   - Session management
   - Message display
   - User interaction loop

5. **Tests**:
   - Unit tests per module
   - Integration tests for full pipeline

---

## How to Use

### 1. Setup

```bash
# Install dependencies
pip install -e .

# Create .env file
cat > .env << EOF
anthropic_api_key=sk-...
embedding_model=all-MiniLM-L6-v2
chroma_persist_dir=data/chroma_db
sqlite_db_path=data/unlearn.db
default_question_ttl_days=14
EOF
```

### 2. Use Existing Modules (Standalone)

```python
from config import Settings
from principles import PRINCIPLES, PATTERN_TO_PRINCIPLES, PsychPattern
from pattern_echo import PatternEchoDetector, TurnAnalysis
from db import UnlearnDB
from signals import quick_assess

# All modules work independently
settings = Settings()
principles = PRINCIPLES  # Knowledge base
detector = PatternEchoDetector()  # Per-session
with UnlearnDB(settings.sqlite_db_path) as db:
    # Track what's been asked
    db.record_question(session_id="s1", question_text="...", principle=1)
    db.gc_expired_questions()  # Garbage collection
```

### 3. Build LangGraph Pipeline (Next Step)

```python
from langgraph.graph import StateGraph
from state import KMirrorState

# Create graph
graph = StateGraph(KMirrorState)

# Add nodes (to be implemented)
def classifier_node(state):
    # Use principles.py + pattern_echo.py
    pass

def inquiry_generator_node(state):
    # Use signals.py + principles.py dialogue_approaches
    pass

graph.add_node("classifier", classifier_node)
graph.add_node("inquiry_gen", inquiry_generator_node)
graph.add_edge("classifier", "inquiry_gen")
```

### 4. Session Lifecycle

```python
# Start session
session_id = "user_123_20250327"
state = KMirrorState(
    messages=[],
    session_id=session_id,
    turn_number=0,
    depth_level=0
)

# Load open inquiries from previous sessions
with UnlearnDB(settings.sqlite_db_path) as db:
    open_inquiries = db.get_open_inquiries()
    # Use these as context for current session

# Run conversation loop (not yet implemented)
# ... process turns ...

# At session end: save dissolved patterns, reset echo detector
with UnlearnDB(settings.sqlite_db_path) as db:
    db.record_dissolution(principle=1, confidence=0.7)
    db.gc_expired_questions()
```

---

## Architecture

### Data Flow

```
User Input
    ↓
[Listener Node] - Extract intent (NOT YET IMPLEMENTED)
    ↓
[Classifier Node] - Map to PsychPattern using principles.py
    ↓
[Pattern Echo Detector] - Check pattern_echo.py for echoes
    ↓
[Depth Assessor] - Gauge conversation depth from state.py
    ↓
[Retriever Node] - Fetch K passages from ChromaDB (NOT YET IMPLEMENTED)
    ↓
[Signals Assessment] - quick_assess() from signals.py
    ↓
[Inquiry Generator] - Use principle's dialogue_approaches + LLM
    ↓
[State Update] - Update state.py + db.py + pattern_echo.py
    ↓
Response to User (Rich CLI)
```

### Module Relationships

```
principles.py
    ↑
    └─ Used by: classifier_node, inquiry_generator_node

pattern_echo.py (per-session)
    ↑
    └─ Populated by: state updates
    └─ Read by: inquiry_generator_node (surface echoes)

db.py (persistent)
    ↑
    └─ Written by: end-of-turn state updates
    └─ Read by: session start (load open_inquiries), depth_assessor_node

signals.py
    ↑
    └─ Called by: inquiry_generator_node (after each user response)

state.py (ephemeral per-session)
    ↑
    └─ Used by: all nodes (passes state through pipeline)

config.py (startup)
    ↑
    └─ Loaded once at app start
```

---

## Code Quality Notes

### Strengths
- ✅ Clean separation of concerns (each module: one responsibility)
- ✅ Type hints throughout (dataclasses + Enum)
- ✅ Anti-memory design (TTL decay aligns with K philosophy)
- ✅ Two-tier assessment (heuristic + LLM fallback)
- ✅ Proper database context management

### Gaps to Address
1. **Input validation** - No bounds checking on confidence values, no TTL validation
2. **Error handling** - Missing try/except in decay_dissolved_patterns
3. **Docstrings** - Principle fields lack documentation
4. **Edge cases** - pattern_echo edge case when turns list is empty
5. **Testing** - Zero test coverage

### Recommended Improvements
- Add pytest fixtures for test data
- Add input validation (e.g., 0 ≤ confidence ≤ 1)
- Document regex patterns in signals.py with examples
- Add logging throughout (DEBUG level for state transitions)
- Handle potential datetime parsing errors in db.py

---

## Roadmap

### Phase 1: LangGraph Orchestration (Blocking)
- [ ] Implement Listener node (intent extraction)
- [ ] Implement Classifier node (pattern mapping)
- [ ] Implement Depth Assessor node
- [ ] Wire nodes together
- **Deliverable**: Can classify user input → psychological pattern

### Phase 2: RAG Integration
- [ ] Build web scraper for jkrishnamurti.org
- [ ] Index K passages into ChromaDB
- [ ] Implement Retriever node
- **Deliverable**: Can retrieve relevant K passages for context

### Phase 3: LLM Integration
- [ ] Implement LLM call in signals.py assessment
- [ ] Implement Inquiry Generator node (response synthesis)
- [ ] Add prompt engineering for K-style questions
- **Deliverable**: End-to-end working dialogue (no UI yet)

### Phase 4: CLI Interface
- [ ] Build Rich-based TUI
- [ ] Implement session management (save/load)
- [ ] Add message history display
- **Deliverable**: Functional CLI for user interaction

### Phase 5: Testing & Polish
- [ ] Write unit tests (80%+ coverage)
- [ ] Add integration tests
- [ ] Performance tuning (LLM latency, DB queries)
- [ ] Documentation updates
- **Deliverable**: Production-ready beta

---

## Debugging & Development Tips

### Running Individual Modules
```python
# Test principles engine
python3 -c "from principles import PRINCIPLES; print(PRINCIPLES[1].name)"

# Test anti-memory DB
python3 << 'EOF'
from db import UnlearnDB
with UnlearnDB("test.db") as db:
    db.record_question("s1", "Test?", 1)
    print(db.get_active_questions())
EOF

# Test pattern echo
python3 << 'EOF'
from pattern_echo import PatternEchoDetector, TurnAnalysis, PsychPattern
from datetime import datetime
d = PatternEchoDetector()
d.record_turn(TurnAnalysis(1, "My boss...", [PsychPattern.RELATIONSHIP_CONFLICT], [], [], datetime.now()))
d.record_turn(TurnAnalysis(2, "My wife...", [PsychPattern.RELATIONSHIP_CONFLICT], [], [], datetime.now()))
echo = d.detect_echo()
print(echo.describe() if echo else "No echo")
EOF
```

### Key Configuration Options
```python
# In .env
anthropic_api_key=sk-...              # Required for LLM
default_question_ttl_days=14          # How long before question expires
deflected_question_ttl_days=30        # Longer TTL for unanswered questions
explored_question_ttl_days=7          # Short TTL for "seen" questions
insight_decay_rate_per_month=0.05     # 5% monthly decay on confidence
insight_removal_threshold=0.1         # Remove insights below 10% confidence
```

### Common Issues

**Issue**: `ImportError: No module named 'langgraph'`
**Solution**: `pip install langgraph langchain-anthropic`

**Issue**: `FileNotFoundError: unlearn.db`
**Solution**: db.py creates the DB automatically on first use. Check `sqlite_db_path` in .env.

**Issue**: Pattern echo not detecting repeats
**Solution**: Echo requires min 2 turns between pattern mentions AND different context. Check `turn_gap >= 1` and `context_words` differ.

---

## References

- **Krishnamurti Teachings**: jkrishnamurti.org
- **LangGraph Docs**: langchain.com/langgraph
- **ChromaDB Docs**: docs.trychroma.com
- **Anthropic Claude API**: console.anthropic.com

---

**Last Updated**: 2026-03-27
**Maintainer**: K-Mirror Development Team
