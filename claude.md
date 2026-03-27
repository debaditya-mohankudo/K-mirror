# K-Mirror: Claude Guide

**K-Mirror** is a Krishnamurti-inspired CLI psychological companion that facilitates self-inquiry through Socratic questioning—never prescribing answers, always mirroring the user's words through the lens of K's principles.

---

## Philosophy & Core Approach

- **Truth is a pathless land** — Don't give answers; ask questions that dissolve frames
- **Inquiry, not instruction** — Never name a principle directly; embed it in questions
- **Direct seeing matters** — Distinguish genuine insight from intellectual agreement
- **Anti-guru design** — Return agency to the user; always question, never preach

---

## Architecture

```
CLI Interface (Rich TUI)
    ↓
LangGraph Orchestrator (5 nodes)
├─ Listener (understand input)
├─ Classifier (map to psychological patterns)
├─ Retriever (RAG from ChromaDB)
├─ Depth Assessor (gauge conversation depth)
└─ Inquiry Generator (craft K-style questions)
    ↓
Conversation Memory + SQLite Anti-Memory DB
    ↓
Vector Store (ChromaDB) + Principles Engine
```

---

## Core Modules

| Module | Purpose |
|--------|---------|
| `principles.py` | 12 K principles, pattern taxonomy, pattern→principle mapping, dialogue templates |
| `state.py` | Ephemeral per-session state (turn analysis, depth tracking, pattern echoes) |
| `signals.py` | Distinguish genuine seeing vs. intellectual agreement (regex + LLM assessment) |
| `pattern_echo.py` | Detect recurring psychological patterns across conversation turns |
| `db.py` | SQLite anti-memory database with TTL-based decay (questions/patterns expire naturally) |
| `config.py` | Pydantic-based settings management from `.env` |

---

## 12 Fundamental Principles

Each maps to psychological patterns and has dialogue templates (mirror, observer_split, time_inquiry, word_inquiry, image_inquiry):

1. **Observer is the observed** → "I want to control my anger"
2. **Mechanical life gives false security** → "I feel stuck in routine"
3. **Self is the root of all problems** → "Why does this always happen to me?"
4. **Thought is material in nature** → "I can't stop thinking"
5. **Action without thought is real action** → "I'm paralyzed by options"
6. **Can thought come to stillness on its own?** → "How do I find peace?"
7. **Relationships die when images are retained** → "My partner doesn't understand me"
8. **Fear is the movement of thought in time** → "I'm afraid of losing..."
9. **Comparison is the root of violence** → "I'm not good enough"
10. **Freedom is not from something, but the act of seeing** → "How do I escape anxiety?"
11. **The word is not the thing** → Identity from labels ("I am depressed")
12. **Understanding requires no time** → Future-oriented self-work ("I'll work on myself")

---

## Key Features

| Feature | Implementation |
|---------|-----------------|
| **Pattern Matching** | Deterministic PsychPattern → Principle mapping |
| **RAG Retrieval** | ChromaDB (sentence-transformers embeddings) for K passages |
| **Depth Tracking** | 4-level system: surface (0) → direct seeing (3) |
| **Echo Detection** | PatternEchoDetector identifies recurring patterns across turns |
| **Insight Assessment** | Regex heuristics + LLM fallback to detect genuine vs. intellectual |
| **Anti-Memory** | Exponential decay on stored questions/insights (natural forgetting) |
| **Dialogue Patterns** | 5 templates: mirror, observer_split, time_inquiry, word_inquiry, image_inquiry |

---

## Technology Stack

- **LLM**: Claude (Anthropic) — nuanced dialogue for Socratic inquiry
- **Orchestration**: LangGraph — stateful agent with branching logic
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2) — local, semantic matching
- **Vector Store**: ChromaDB — lightweight Python-native
- **Database**: SQLite — anti-memory with TTL decay
- **CLI**: Rich — beautiful terminal output
- **Config**: pydantic-settings + python-dotenv

---

## Environment Configuration

`.env` settings (see `config.py`):
```
anthropic_api_key=<required>
embedding_model=all-MiniLM-L6-v2
chroma_persist_dir=data/chroma_db
sqlite_db_path=data/unlearn.db
default_question_ttl_days=14
deflected_question_ttl_days=30
explored_question_ttl_days=7
insight_decay_rate_per_month=0.05
insight_removal_threshold=0.1
```

---

## Current Status

**Implemented:**
- ✅ Domain models (Principles, PsychPattern, State)
- ✅ Insight detection (genuine vs. intellectual agreement)
- ✅ Pattern echo detection (within-session tracking)
- ✅ SQLite anti-memory with TTL decay
- ✅ Configuration management
- ✅ Detailed architectural planning

**Pending:**
- ⏳ Web scraper for jkrishnamurti.org talks
- ⏳ Vector store setup + retrieval integration
- ⏳ LangGraph workflow nodes
- ⏳ CLI interface (Rich TUI)
- ⏳ Test suite (pytest)
- ⏳ Conversation evaluation

---

## Development Guidelines

### Do
- Questions should mirror user's own words, never prescribe
- Detect pattern echoes and reflect recurring movements
- Distinguish genuine insight from intellectual agreement
- Let conversation depth guide inquiry intensity
- Let questions fade if not reinforced (anti-memory philosophy)

### Don't
- Offer solutions or advice
- Name principles explicitly
- Use generic chatbot patterns
- Build memory that accumulates without decay
- Create therapy replacement (it's educational inquiry only)

### Dialogue Principles
- **Mirror**: Reflect user's words back with embedded questioning
- **Observer split**: "Who observes this anger? Is it separate from anger?"
- **Time inquiry**: Explore how thought moves through time (past/future anxiety)
- **Word inquiry**: Examine labels ("What does 'depressed' mean to you?")
- **Image inquiry**: Challenge fixed images of self/others

---

## Key Files & Locations

- **Plans**: `krishnamurti-chatbot-plan*.md` (3 detailed planning docs)
- **Modules**: Root level (`principles.py`, `state.py`, `signals.py`, etc.)
- **Data**: `data/chroma_db/` (vector store), `data/unlearn.db` (SQLite)
- **Config**: `.env` (see `config.py` for schema)

---

## Philosophy Quote

> *"Truth is a pathless land. I cannot tell you how to get there; you must find it yourself."*
>
> The system embodies this: never a guru, always a mirror. The user finds their own seeing.
