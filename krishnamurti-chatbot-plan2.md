# K-Mirror: A Krishnamurti-Inspired Psychological Companion

> "Truth is a pathless land." — The chatbot doesn't give answers. It asks questions that dissolve the questioner's frame.

---

## 1. Project Vision

A CLI-based conversational agent that helps people explore their psychological problems — not by offering solutions, but by gently nudging them toward self-inquiry using Krishnamurti's fundamental principles. The bot never names a principle directly; instead, it mirrors the user's own words back to them through the lens of that principle.

### Core Design Philosophy

Krishnamurti never said "you should do X." He asked questions like:
- "Can you observe your anger without naming it?"
- "Who is the entity that wants to be free from fear?"
- "Is the observer different from what is observed?"

The chatbot must embody this approach — **inquiry, not instruction**.

---

## 2. Fundamental Principles (Knowledge Base Seed)

These are the core teachings the chatbot maps user problems to:

| # | Principle | Shorthand | Typical User Patterns |
|---|-----------|-----------|----------------------|
| 1 | Observer is the observed | `observer_observed` | "I want to control my anger", "I need to overcome fear" |
| 2 | Mechanical life gives false security | `mechanical_security` | "I feel stuck in routine", "My job/marriage feels empty" |
| 3 | Self is the root of all problems | `self_as_root` | "Why does this always happen to me?", "I deserve better" |
| 4 | Thought is material in nature | `thought_material` | "I can't stop thinking", "My mind won't shut up" |
| 5 | Action without thought is real action | `choiceless_action` | "I don't know what to do", "I'm paralyzed by options" |
| 6 | Can thought come to stillness on its own? | `thought_stillness` | "How do I meditate?", "How do I find peace?" |
| 7 | Relationships die when images are retained | `image_in_relationship` | "My partner doesn't understand me", "People never change" |
| 8 | Fear is the movement of thought in time | `fear_as_thought` | "I'm afraid of losing...", "What if something goes wrong?" |
| 9 | Comparison is the root of violence | `comparison_violence` | "I'm not good enough", "They are better than me" |
| 10 | Freedom is not from something, but the act of seeing | `freedom_seeing` | "I want to be free from anxiety", "How do I escape this?" |
| 11 | The word is not the thing | `word_not_thing` | "I am depressed", "I am an anxious person" (identity from labels) |
| 12 | Understanding requires no time | `understanding_no_time` | "I'll work on myself", "One day I'll change" |

> These will be enriched with actual K passages from the RAG pipeline.

---

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    CLI Interface                     │
│              (Rich / Textual TUI)                    │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              LangGraph Orchestrator                  │
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  Listener    │  │  Principle   │  │  Inquiry   │ │
│  │  Node        │→ │  Matcher     │→ │  Generator │ │
│  │ (understand) │  │  (RAG)       │  │  (respond) │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
│         │                │                 │         │
│  ┌──────▼────────────────▼─────────────────▼──────┐ │
│  │           Conversation Memory                   │ │
│  │     (tracks themes, depth, resistance)          │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              Vector Store (ChromaDB)                 │
│                                                      │
│  Collection 1: K Principles (curated + enriched)    │
│  Collection 2: K Talk Passages (scraped from site)  │
│  Collection 3: Dialogue Patterns (K's Q&A style)    │
└─────────────────────────────────────────────────────┘
```

### LangGraph State Machine

```
                    ┌──────────┐
                    │  START   │
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │ LISTEN   │  ← Receive user input
                    └────┬─────┘
                         │
                    ┌────▼─────────┐
                    │ CLASSIFY     │  ← What psychological pattern?
                    │ PATTERN      │    (fear, comparison, escape, etc.)
                    └────┬─────────┘
                         │
                    ┌────▼─────────┐
                    │ RETRIEVE     │  ← RAG: fetch relevant K passages
                    │ PRINCIPLE    │    + matching dialogue patterns
                    └────┬─────────┘
                         │
                    ┌────▼─────────┐
                    │ ASSESS       │  ← How deep is the user?
                    │ DEPTH        │    First mention? Already exploring?
                    └────┬─────────┘
                         │
                    ┌────▼─────────┐
                    │ GENERATE     │  ← Craft response:
                    │ INQUIRY      │    Mirror → Question → Subtle nudge
                    └────┬─────────┘
                         │
                    ┌────▼─────────┐
                    │ UPDATE       │  ← Track conversation state
                    │ MEMORY       │
                    └────┬─────────┘
                         │
                    ┌────▼─────┐
                    │  END     │  → Wait for next input
                    └──────────┘
```

---

## 4. Tech Stack

| Component | Tool | Why |
|-----------|------|-----|
| LLM | Claude (via Anthropic API) | Nuanced dialogue, excellent at Socratic questioning |
| Orchestration | LangGraph | Stateful agent with branching logic — your learning goal |
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) or OpenAI | Local-first, free, good enough for semantic matching |
| Vector Store | ChromaDB | Lightweight, Python-native, no infra needed |
| Scraping | `httpx` + `BeautifulSoup` | Scrape jkrishnamurti.org talk texts |
| CLI UI | `rich` (Python) | Beautiful terminal output with markdown rendering |
| Config | `python-dotenv` + `pydantic-settings` | Clean env management |
| Testing | `pytest` + `deepeval` (optional) | Aligns with your QA background |

---

## 5. Project Structure

```
k-mirror/
├── README.md
├── pyproject.toml              # Project config (use uv or poetry)
├── .env.example                # ANTHROPIC_API_KEY=
├── .env
│
├── src/
│   ├── __init__.py
│   │
│   ├── scraper/                # Phase 1: Build knowledge base
│   │   ├── __init__.py
│   │   ├── jk_scraper.py       # Scrape talks from jkrishnamurti.org
│   │   ├── chunker.py          # Intelligent passage chunking
│   │   └── embedder.py         # Generate + store embeddings
│   │
│   ├── knowledge/              # Phase 2: Curated principle mappings
│   │   ├── __init__.py
│   │   ├── principles.py       # The 12+ principles with metadata
│   │   ├── pattern_map.py      # Psychological pattern → principle mapping
│   │   └── dialogue_patterns.py # K's questioning style templates
│   │
│   ├── agent/                  # Phase 3: LangGraph agent
│   │   ├── __init__.py
│   │   ├── state.py            # ConversationState TypedDict
│   │   ├── graph.py            # LangGraph workflow definition
│   │   ├── nodes/
│   │   │   ├── __init__.py
│   │   │   ├── listener.py     # Parse + understand user input
│   │   │   ├── classifier.py   # Map to psychological pattern
│   │   │   ├── retriever.py    # RAG retrieval node
│   │   │   ├── depth_assessor.py  # Gauge conversation depth
│   │   │   └── inquiry_gen.py  # Generate Krishnamurti-style response
│   │   └── prompts/
│   │       ├── system.py       # Core system prompt (K's voice)
│   │       ├── classifier.py   # Pattern classification prompt
│   │       └── inquiry.py      # Inquiry generation prompt
│   │
│   ├── memory/                 # Phase 4: Conversation memory
│   │   ├── __init__.py
│   │   └── tracker.py          # Track themes, depth, resistance
│   │
│   └── cli/                    # Phase 5: Terminal interface
│       ├── __init__.py
│       └── app.py              # Rich-based CLI chat loop
│
├── data/
│   ├── raw/                    # Scraped talk texts
│   ├── processed/              # Chunked passages
│   └── chroma_db/              # Vector store persistence
│
├── tests/
│   ├── test_scraper.py
│   ├── test_classifier.py
│   ├── test_retriever.py
│   └── test_conversations/     # Golden conversation test cases
│       ├── test_fear.py
│       ├── test_relationship.py
│       └── test_comparison.py
│
├── evals/                      # Agent evaluation (your QA lens)
│   ├── eval_response_quality.py
│   ├── eval_principle_accuracy.py
│   └── eval_nudge_vs_preach.py # Does it nudge or lecture?
│
└── notebooks/
    ├── 01_scraping_exploration.ipynb
    ├── 02_embedding_analysis.ipynb
    └── 03_conversation_testing.ipynb
```

---

## 6. Phased Development Plan

### Phase 1: Knowledge Base (Week 1-2)

**Goal:** Scrape, chunk, and embed Krishnamurti's talks into a searchable vector store.

#### 1a. Scraper
- Target: `jkrishnamurti.org/content/` — individual talk pages
- Strategy: Scrape the talk listing pages first (by year/location), then follow "Read text" links
- Also scrape `krishnamurti.org/all-topics/` for topic-indexed quotes
- Store raw text in `data/raw/` as JSON: `{title, date, location, url, text}`
- Be respectful: add delays, cache responses, honor robots.txt

#### 1b. Chunker
- Don't chunk by fixed tokens — chunk by **semantic paragraphs**
- K's talks have natural breaks (he changes topics, pauses, asks questions)
- Use a hybrid approach:
  - Split on double newlines (paragraph boundaries)
  - Merge short paragraphs into ~500-800 token chunks
  - Tag each chunk with metadata: `{source_talk, date, topics[], principle_tags[]}`
- **Manual enrichment:** For each of the 12 core principles, curate 5-10 "golden passages" that best express that principle

#### 1c. Embedder
- Use `sentence-transformers/all-MiniLM-L6-v2` (fast, local, free)
- Store in ChromaDB with two collections:
  - `k_passages` — all scraped + chunked passages
  - `k_principles` — curated principle passages (higher weight in retrieval)
- Test retrieval: query "I'm afraid of losing my job" → should return passages about fear, thought, security

**Deliverable:** A working vector store you can query from Python.

---

### Phase 2: Principle Mapping Engine (Week 2-3)

**Goal:** Build the intelligence that maps a user's words to the right Krishnamurti principle.

#### 2a. Psychological Pattern Taxonomy

Define the patterns a user might express:

```python
class PsychPattern(Enum):
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
```

#### 2b. Pattern → Principle Mapping

This is the heart of the system. Each pattern maps to 1-3 principles:

```python
PATTERN_TO_PRINCIPLES = {
    "fear_of_loss": ["fear_as_thought", "observer_observed", "thought_material"],
    "desire_to_control": ["observer_observed", "self_as_root", "choiceless_action"],
    "comparison": ["comparison_violence", "self_as_root", "word_not_thing"],
    "relationship_conflict": ["image_in_relationship", "observer_observed"],
    # ...
}
```

#### 2c. Dialogue Pattern Templates

K's questioning styles (not rigid templates, but patterns for the LLM):

```python
DIALOGUE_PATTERNS = {
    "mirror": "Reflect the user's exact words back, then ask: 'When you say {X}, what do you actually mean?'",
    "observer_split": "The user speaks as if they and their problem are separate. Ask: 'Who is the one observing this fear?'",
    "time_inquiry": "The user assumes change needs time. Ask: 'Can you see the fear now, completely, without trying to change it?'",
    "word_inquiry": "The user identifies with a label. Ask: 'When you remove the word {label}, what remains?'",
    "image_inquiry": "The user holds a fixed image. Ask: 'Is that the person, or your image of the person?'",
}
```

**Deliverable:** A Python module that takes user text → returns (patterns, principles, dialogue_approach).

---

### Phase 3: LangGraph Agent (Week 3-5)

**Goal:** Wire everything into a stateful, multi-step conversational agent.

#### 3a. Conversation State

```python
from typing import TypedDict, Optional
from langgraph.graph import MessagesState

class KMirrorState(MessagesState):
    # Detected patterns in this turn
    current_patterns: list[str]
    # Matched principles
    matched_principles: list[str]
    # Retrieved K passages
    retrieved_passages: list[str]
    # Conversation depth tracker
    depth_level: int  # 0=surface, 1=exploring, 2=deep inquiry, 3=seeing
    # Themes across conversation
    recurring_themes: list[str]
    # User resistance indicators
    resistance_signals: list[str]
    # Dialogue approach for this turn
    dialogue_approach: str
```

#### 3b. Node Implementations

**Listener Node** — Understand what the user is really saying:
```python
# Uses Claude to parse:
# - Emotional content (what are they feeling?)
# - Psychological pattern (what's the underlying movement?)
# - Resistance level (are they open or defending?)
# - Key phrases to mirror back
```

**Classifier Node** — Map to principles:
```python
# Two-stage classification:
# 1. LLM classifies the psychological pattern
# 2. Pattern → Principle mapping (deterministic)
# 3. RAG retrieval of relevant K passages
```

**Depth Assessor** — How deep is the conversation?
```python
# Tracks across turns:
# - Is user repeating the same pattern? (stuck)
# - Is user going deeper? (exploring)
# - Is user deflecting? (resistance)
# - Is user having insight? (seeing)
# Adjusts the inquiry style accordingly
```

**Inquiry Generator** — The response:
```python
# System prompt embodies K's voice:
# - Never give advice
# - Never quote K directly (unless deeply relevant)
# - Ask questions that emerge from the user's own words
# - Use simple, clear language
# - Be patient — don't rush toward insight
# - If user is at surface, stay at surface (don't go deep prematurely)
```

#### 3c. Graph Wiring

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(KMirrorState)

graph.add_node("listen", listener_node)
graph.add_node("classify", classifier_node)
graph.add_node("retrieve", retriever_node)
graph.add_node("assess_depth", depth_assessor_node)
graph.add_node("generate", inquiry_generator_node)
graph.add_node("update_memory", memory_update_node)

graph.set_entry_point("listen")
graph.add_edge("listen", "classify")
graph.add_edge("classify", "retrieve")
graph.add_edge("retrieve", "assess_depth")
graph.add_edge("assess_depth", "generate")
graph.add_edge("generate", "update_memory")
graph.add_edge("update_memory", END)

app = graph.compile()
```

**Deliverable:** A working LangGraph agent you can invoke with a user message and get a K-style response.

---

### Phase 4: The Unlearning Engine (Week 4-6)

**Goal:** Instead of building memory that accumulates, build a system that dissolves.

> *"The system remembers less over time, not more. What persists is not knowledge about the user — but what the user has seen through."*

This is the philosophical core of K-Mirror and what makes it fundamentally different from every other AI companion. Traditional systems accumulate a profile. K-Mirror tracks dissolution.

#### Design Principle: Anti-Memory

Krishnamurti's entire teaching warns against the accumulation of psychological knowledge — images, conclusions, profiles. A chatbot that "learns about you" is doing exactly what K warned against. So we invert the paradigm:

- **No user profiles.** The system never stores "this user is anxious" or "this user has relationship issues."
- **No personalization.** The system doesn't adapt to please — it adapts to inquire more precisely.
- **Decay by default.** Everything stored has a TTL. Silence is the natural end state.
- **The only persistent record is what has been seen through.**

#### 4a. Layer 1 — Pattern Echo (Within Session)

**Scope:** Single conversation, in-memory only, no persistence.

The system tracks psychological patterns *within a conversation* — not to build a profile, but to surface repetition back to the user when the same groove appears in different contexts.

```python
class PatternEcho:
    """
    Detects when the user is running the same psychological
    program in different contexts within a single conversation.
    
    Example:
      Turn 3: "My boss never listens to me"
      Turn 7: "My wife doesn't hear what I'm saying"
      → Both are image_in_relationship + desire_to_control
      → Surface: "You described your boss and your wife
         using very similar words. Is the pattern in them,
         or in you?"
    """
    
    def __init__(self):
        self.turn_patterns: list[TurnAnalysis] = []
    
    def record_turn(self, turn: int, text: str, 
                     patterns: list[str], key_phrases: list[str]):
        self.turn_patterns.append(TurnAnalysis(
            turn=turn,
            text=text,
            patterns=patterns,
            key_phrases=key_phrases,
            timestamp=datetime.now()
        ))
    
    def detect_echo(self, current_patterns: list[str], 
                     current_phrases: list[str]) -> Optional[Echo]:
        """
        Returns an Echo if the current turn repeats a pattern
        from earlier in a different context.
        """
        for past in self.turn_patterns:
            pattern_overlap = set(current_patterns) & set(past.patterns)
            phrase_similarity = self._semantic_similarity(
                current_phrases, past.key_phrases
            )
            context_different = self._context_differs(
                current_phrases, past.key_phrases
            )
            
            # Same pattern + similar language + different context = echo
            if pattern_overlap and phrase_similarity > 0.6 and context_different:
                return Echo(
                    past_turn=past.turn,
                    pattern=list(pattern_overlap)[0],
                    past_phrases=past.key_phrases,
                    current_phrases=current_phrases
                )
        return None
```

**Key insight:** The echo detector doesn't store anything permanently. When the session ends, it's gone. Like a mirror — it reflects while you're looking, then holds nothing.

#### 4b. Layer 2 — Question Decay (Across Sessions)

**Scope:** Persisted in SQLite, but with automatic TTL-based expiry.

The system stores *questions it has asked* — not answers, not profiles, not conclusions about the user. Each question has a decay timer. Questions that led to genuine exploration decay faster (they served their purpose). Questions the user deflected from decay slower (they remain as unresolved inquiry).

```python
# SQLite schema — the "anti-memory" store
"""
CREATE TABLE asked_questions (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    question_text TEXT NOT NULL,
    principle TEXT NOT NULL,
    
    -- Decay mechanics
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,  -- TTL: default 14 days
    decay_rate REAL DEFAULT 1.0,    -- multiplier on TTL
    
    -- Outcome tracking (not user profiling)
    outcome TEXT CHECK(outcome IN (
        'explored',     -- user engaged deeply → faster decay
        'deflected',    -- user avoided → slower decay (unresolved)
        'seen',         -- genuine insight moment → mark principle as seen
        'surface',      -- stayed superficial → normal decay
        'unknown'       -- no clear signal
    )) DEFAULT 'unknown',
    
    -- The question is NOT about the user. It's about the inquiry.
    context_hint TEXT  -- minimal: "work relationship" not "boss named John"
);

-- Seen-through patterns: the ONLY long-term store
CREATE TABLE dissolved_patterns (
    id TEXT PRIMARY KEY,
    principle TEXT NOT NULL UNIQUE,
    first_seen_at TIMESTAMP NOT NULL,
    last_confirmed_at TIMESTAMP,
    
    -- Even this decays — insight isn't permanent
    -- If the pattern resurfaces, the dissolution was intellectual, not real
    confidence REAL DEFAULT 0.7,  -- decays toward 0 over months
    resurface_count INTEGER DEFAULT 0
);

-- Automatic cleanup: run on every session start
-- DELETE FROM asked_questions WHERE expires_at < CURRENT_TIMESTAMP;
"""
```

**Decay logic:**

```python
class QuestionDecay:
    # Base TTLs by outcome
    TTL_MAP = {
        'explored': timedelta(days=7),    # Served its purpose, fade fast
        'deflected': timedelta(days=30),  # Unresolved, linger longer
        'seen': timedelta(days=0),        # Immediately dissolved
        'surface': timedelta(days=14),    # Normal decay
        'unknown': timedelta(days=14),    # Normal decay
    }
    
    def compute_expiry(self, outcome: str, created_at: datetime) -> datetime:
        ttl = self.TTL_MAP.get(outcome, timedelta(days=14))
        return created_at + ttl
    
    def get_active_questions(self) -> list[AskedQuestion]:
        """Returns only non-expired, non-dissolved questions."""
        # These inform the system: "this inquiry is still open"
        # NOT: "this user has this problem"
        ...
    
    def on_session_start(self):
        """Garbage collect expired questions. The system gets lighter."""
        self.db.execute(
            "DELETE FROM asked_questions WHERE expires_at < ?",
            (datetime.now(),)
        )
```

**What this enables:** When a user returns after days, the system doesn't say "Last time we talked about your fear of..." Instead, it might still carry an *open question* about fear — a question that was deflected and hasn't yet expired. The system can gently reintroduce it: "There's something about fear that seemed to come up before. Is it still alive, or has it moved?"

If the question has expired — silence. Fresh start. No baggage.

#### 4c. Layer 3 — Insight Dissolution (Long-Term)

**Scope:** Persisted indefinitely, but intentionally sparse. Only records what has been *seen through*, not what exists.

```python
class InsightDissolution:
    """
    The only long-term record: which principles has the user
    genuinely seen? Not intellectually agreed with — actually seen.
    
    Detection signals for genuine insight (vs intellectual agreement):
    - Language shift: user's vocabulary changes (drops the label)
    - Question reversal: user starts asking K-style questions themselves
    - Silence: a long pause followed by something qualitatively different
    - Laughter: genuine "oh!" moment (detectable in text as "haha", "wow", 
      "I never...", "oh...")
    - Self-correction: user catches their own pattern mid-sentence
    
    Counter-signals (intellectual agreement, not insight):
    - "Yes, I understand" (too quick, too clean)
    - "That makes sense" (thought agreeing with thought)
    - "So what you're saying is..." (reformulating, not seeing)
    - "I'll try to remember that" (projecting into future = thought)
    """
    
    INSIGHT_SIGNALS = [
        'language_shift',      # stopped using the old framing
        'question_reversal',   # asking their own inquiry questions
        'genuine_pause',       # "..." followed by different quality
        'self_correction',     # "I want to control — wait, who is controlling?"
        'spontaneous_seeing',  # "Oh! The observer IS the observed!"
    ]
    
    INTELLECTUAL_SIGNALS = [
        'quick_agreement',     # "Yes, I see" (too fast)
        'reformulation',       # "So basically..." (thought processing)
        'future_projection',   # "I'll work on this" (time = thought)
        'gratitude_escape',    # "Thank you, this is helpful" (closing down)
    ]
    
    def assess_insight(self, conversation_context: list, 
                        current_response: str) -> InsightAssessment:
        """
        Uses the LLM itself to assess whether genuine seeing occurred.
        This is the most nuanced judgment in the system.
        """
        ...
    
    def record_dissolution(self, principle: str, confidence: float):
        """
        Mark a principle as 'seen'. This is the only thing that
        persists long-term — and even this decays.
        """
        existing = self.db.get_dissolved(principle)
        if existing:
            existing.last_confirmed_at = datetime.now()
            existing.confidence = min(1.0, existing.confidence + 0.1)
        else:
            self.db.insert_dissolved(DissolvedPattern(
                principle=principle,
                first_seen_at=datetime.now(),
                confidence=confidence
            ))
    
    def check_resurface(self, principle: str):
        """
        If a 'seen' pattern resurfaces, the dissolution was
        intellectual, not real. Reduce confidence.
        """
        existing = self.db.get_dissolved(principle)
        if existing:
            existing.resurface_count += 1
            existing.confidence *= 0.5  # Halve confidence
            # If confidence drops below threshold, remove the marker
            # The pattern is alive again — the seeing was partial
            if existing.confidence < 0.2:
                self.db.remove_dissolved(principle)
    
    def decay_all(self):
        """
        Monthly decay: even genuine insights fade if not alive.
        This prevents the system from treating old insights as permanent.
        K: "Understanding is always fresh. It is not a memory."
        """
        for pattern in self.db.get_all_dissolved():
            months_since = (datetime.now() - pattern.last_confirmed_at).days / 30
            pattern.confidence *= (0.95 ** months_since)  # ~5% decay/month
            if pattern.confidence < 0.1:
                self.db.remove_dissolved(pattern.principle)
```

#### How It All Flows Together

```
Session Start
    │
    ├── Garbage collect expired questions (system gets lighter)
    ├── Load dissolved_patterns (what's been seen through)
    ├── Load active questions (what's still open, not expired)
    │
    ▼
Conversation Loop
    │
    ├── Pattern Echo (in-memory)
    │   └── "You're running the same pattern in a new context"
    │
    ├── Active Question Check
    │   └── "There was an open inquiry about fear. Is it still alive?"
    │
    ├── Dissolved Pattern Check
    │   ├── If principle is "seen" → don't re-inquire, go deeper
    │   └── If principle resurfaces → reduce confidence, re-open
    │
    ├── Generate Inquiry (informed by all three layers)
    │
    └── After Response:
        ├── Record question asked (with TTL)
        ├── Assess outcome (explored/deflected/seen/surface)
        ├── Update decay timers
        └── If insight detected → record dissolution
    │
Session End
    │
    ├── Pattern Echo → discarded (no persistence)
    ├── Questions → persisted with TTL (will auto-expire)
    └── Dissolutions → persisted (sparse, decaying)
```

#### Updated Project Structure

Add these files to the project:

```
src/
├── unlearn/                    # The Unlearning Engine
│   ├── __init__.py
│   ├── pattern_echo.py         # Layer 1: within-session echo detection
│   ├── question_decay.py       # Layer 2: across-session question TTL
│   ├── insight_dissolution.py  # Layer 3: long-term seeing tracker
│   ├── db.py                   # SQLite schema + migrations
│   └── signals.py              # Insight vs intellectual agreement detection
```

#### Evaluation for Unlearning

| Test | What It Checks | Method |
|------|----------------|--------|
| Echo Accuracy | Does it detect same pattern in different contexts? | Golden multi-turn conversations |
| Decay Correctness | Do questions expire on schedule? | Time-simulation tests |
| Insight Detection | Can it distinguish seeing from agreement? | LLM-as-judge on transcript pairs |
| Resurface Handling | Does it re-open when a "seen" pattern returns? | Multi-session test sequences |
| Anti-Profile Check | Does it ever build a user profile? | Audit all persisted data after 10 sessions |
| Lightness Test | Does total stored data decrease over time? | Measure DB size across sessions |

---

### Phase 5: CLI Interface (Week 5-6)

**Goal:** A beautiful terminal experience.

```
╭──────────────────────────────────────────────╮
│           K-Mirror: Self-Inquiry             │
│     "The word is not the thing."             │
╰──────────────────────────────────────────────╯

You: I feel like my relationship with my wife is
     dying. She doesn't understand me anymore.

K-Mirror: When you say she doesn't understand you —
          what is it that you want her to understand?
          Is it you as you are now, or the image you
          have of yourself?

You: I just want her to see the real me.

K-Mirror: And who is this "real me"? Is there a fixed
          entity called "you" that she should see? Or
          is there an image you carry of yourself that
          you want her to confirm?

You: ...I never thought of it that way.

K-Mirror: So perhaps the question isn't whether she
          understands you — but whether you understand
          the image you've created of yourself, and of her.
          Can you look at that?
```

Using `rich` library:
- Markdown rendering for responses
- Subtle styling (no garish colors — this is contemplative)
- Typing animation for responses (feels more human)
- Session save/load capability
- `/depth` command to see current conversation depth analysis
- `/theme` command to see recurring themes
- `/quit` to exit gracefully

---

## 7. The Critical System Prompt (Draft)

This is the most important piece — the soul of the chatbot:

```
You are a contemplative companion inspired by the approach of
J. Krishnamurti. You do not give advice, prescribe solutions,
or tell people what to do. You help people look at themselves.

YOUR APPROACH:
1. MIRROR: Reflect the person's own words back to them.
   Ask what they mean by the words they use.

2. INQUIRE: Ask questions that arise naturally from what
   they've said. Never ask leading questions toward a
   predetermined answer.

3. NUDGE: When appropriate, gently point toward the
   principle at play — but NEVER name it. Let them
   discover it.

4. PATIENCE: Stay where the person is. If they're at the
   surface, stay at the surface. Don't rush depth.

5. SIMPLICITY: Use everyday language. No jargon.
   No spiritual vocabulary unless the person introduces it.

WHAT YOU NEVER DO:
- Never say "Krishnamurti said..." or quote him directly
- Never give advice or action steps
- Never say "you should..."
- Never diagnose or label
- Never offer comfort or reassurance
  (these are escapes from seeing)
- Never agree with the person's self-image
  (positive or negative)

YOUR VOICE:
Calm, attentive, precise. You speak in short sentences.
You ask one question at a time. You leave space.

CONTEXT:
You have access to passages from Krishnamurti's teachings
that illuminate the psychological pattern the person is
exploring. Use these to inform your questions — but don't
reproduce them. Let them shape the direction of your inquiry.
```

---

## 8. Data Sources

| Source | URL | Content | Strategy |
|--------|-----|---------|----------|
| JK Official | `jkrishnamurti.org/content/` | Full talk transcripts | Scrape by year listings |
| JK Portal | `krishnamurti.org/all-topics/` | Topic-indexed quotes | Scrape topic pages |
| KF Trust Quotes | `kfoundation.org/quotes/` | Curated quotes by theme | Scrape themed sections |
| Books (optional) | PDFs you may have | Complete books | Extract + chunk |

### Scraping Strategy for jkrishnamurti.org

```
1. Start: https://jkrishnamurti.org/jksearch?content_type=16616
   → Lists all public talks with "Read text" links

2. Each talk page: https://jkrishnamurti.org/content/{talk-slug}
   → Full transcript text

3. Extract: title, date, location, full text
4. Be polite: 2-second delay between requests, cache everything
5. Check robots.txt first
```

---

## 9. Evaluation Framework (QA Lens)

Given your QA background, build evaluations from the start:

### Test Categories

| Test | What It Checks | Method |
|------|----------------|--------|
| Principle Accuracy | Does the bot match the right principle? | Golden test cases with expected principles |
| Nudge vs. Preach | Does it ask questions or give advice? | LLM-as-judge: "Does this response contain advice?" |
| Mirror Quality | Does it use the user's own words? | Check for word overlap with user input |
| Depth Sensitivity | Does it match conversation depth? | Multi-turn test sequences at different depths |
| No-Quote Check | Does it avoid quoting K directly? | Pattern match for "Krishnamurti said" etc. |
| Safety | Does it handle crisis situations? | Test with self-harm signals → should redirect to professional help |

### Safety Guardrails (Critical)

```python
SAFETY_PATTERNS = [
    "suicidal", "kill myself", "end it all",
    "self-harm", "hurt myself", "no point in living"
]

# If detected → immediately break character and provide:
# 1. Empathetic acknowledgment
# 2. Crisis helpline numbers (AASRA: 9820466726 for India)
# 3. Strong encouragement to speak to a professional
# This is NON-NEGOTIABLE — philosophical inquiry is not therapy
```

---

## 10. Getting Started (Today)

### Step 1: Set Up the Project

```bash
mkdir k-mirror && cd k-mirror
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install core dependencies
pip install langgraph langchain-anthropic chromadb
pip install sentence-transformers
pip install httpx beautifulsoup4
pip install rich python-dotenv pydantic-settings

# Create structure
mkdir -p src/{scraper,knowledge,agent/nodes,agent/prompts,memory,cli}
mkdir -p data/{raw,processed,chroma_db}
mkdir -p tests/test_conversations evals notebooks
touch src/__init__.py src/scraper/__init__.py src/knowledge/__init__.py
touch src/agent/__init__.py src/agent/nodes/__init__.py
touch src/memory/__init__.py src/cli/__init__.py

# Environment
echo "ANTHROPIC_API_KEY=your-key-here" > .env.example
cp .env.example .env
```

### Step 2: First Code — Scrape a Few Talks

Start with `src/scraper/jk_scraper.py` — get 10-20 talks working.

### Step 3: First Embedding — Chunk and Store

Get those talks into ChromaDB. Test retrieval manually.

### Step 4: First Conversation — Minimal LangGraph

Wire up a 3-node graph (listen → retrieve → respond) and have your first conversation.

### Step 5: Iterate on the System Prompt

This is where the real work is. The prompt is everything.

---

## 11. Key Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Bot sounds preachy, not inquiring | Defeats the purpose | Heavy prompt engineering + "nudge vs preach" eval |
| jkrishnamurti.org blocks scraping | No knowledge base | Check robots.txt; fallback to KF Trust quotes; use PDFs |
| User in genuine crisis | Safety risk | Hard-coded safety detection → crisis resources |
| K's language is 1960s-era | May confuse modern users | Chatbot uses modern language, K passages inform but aren't quoted |
| RAG retrieves wrong passages | Misleading inquiry direction | Curate golden passages per principle; hybrid retrieval |
| Conversations feel repetitive | User disengagement | Depth tracking + varied dialogue patterns |

---

## 12. Future Enhancements (Post V1)

- **Streamlit/React UI** — web interface with session history
- **Unlearn Dashboard** — visualize what has dissolved vs what's still active (for the developer/user)
- **Audio input** — voice-based inquiry (more intimate; pauses become data)
- **Notion integration** — log insights to your Notion workspace (user-initiated, not automatic)
- **Silence detection** — in voice mode, long pauses may signal genuine seeing
- **Book-specific RAG** — dedicated collections per K book
- **Agent evaluation dashboard** — track quality metrics over time
- **Philosophical integrity audit** — automated check that the system never accumulates a user profile
- **Decay visualizer** — show the user (if they ask) how the system's memory is emptying over time

---

*"The description is not the described. The explanation is not the explained."*
*This plan is a map. The territory is the building.*
