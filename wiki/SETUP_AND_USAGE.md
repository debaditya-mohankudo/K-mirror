# K-Mirror: Setup & Usage Guide

Complete guide for installing and using K-Mirror with `uv` package manager.

---

## Prerequisites

### Required
- **Python 3.11+**
- **uv** (modern Python package manager in Rust)
- **Anthropic API Key** (for Claude integration)

### Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# OR use Homebrew
brew install uv

# Verify
uv --version
```

---

## Installation & Setup

### 1. Clone/Navigate to Project

```bash
cd /Users/debaditya/workspace/K-mirror
```

### 2. Create Virtual Environment with uv

```bash
# Create venv (uv handles this automatically)
uv venv

# Activate it
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

### 3. Install Dependencies with uv

```bash
# Install all dependencies
uv pip install -e .

# OR install with development dependencies
uv pip install -e ".[dev]"

# Verify installation
uv pip list | grep -E "langgraph|chromadb|langchain|rich"
```

### 4. Configure Environment Variables

Create `.env` file in project root:

```bash
cat > .env << 'EOF'
anthropic_api_key=sk-YOUR-API-KEY-HERE
embedding_model=all-MiniLM-L6-v2
chroma_persist_dir=data/chroma_db
sqlite_db_path=data/unlearn.db
default_question_ttl_days=14
deflected_question_ttl_days=30
explored_question_ttl_days=7
insight_decay_rate_per_month=0.05
insight_removal_threshold=0.1
EOF
```

**Get your API key:**
1. Go to https://console.anthropic.com
2. Create account or sign in
3. Navigate to API keys
4. Create new key
5. Paste into `.env`

### 5. Initialize Data Directories

```bash
mkdir -p data
mkdir -p data/sessions

# These will be auto-created by the app, but good to have them ready
```

### 6. Test Installation

```bash
# Quick test of imports
uv run python3 -c "from app import create_app; print('✓ K-Mirror imports successfully')"

# Or with venv activated:
python3 -c "from app import create_app; print('✓ K-Mirror imports successfully')"
```

---

## Running K-Mirror

### Method 1: Direct Python Execution

```bash
# Activate venv first
source .venv/bin/activate

# Run with python
python3 main.py
```

### Method 2: Using uv (Recommended)

```bash
# No need to activate venv
uv run main.py

# Or with python3
uv run python3 main.py

# Or run the CLI command directly
uv run k-mirror
```

### Method 3: After Installing as Package

```bash
# Install in development mode
uv pip install -e .

# Then run from anywhere
k-mirror
```

---

## Using K-Mirror: Interactive Session

### Starting a Conversation

```
Welcome to K-Mirror!

You
> I feel stuck in my job. I just go through the motions every day.

K-Mirror is thinking...

┌─────────────────────────────────────────────────────────┐
│ K-Mirror                                                │
│                                                         │
│ Can you describe what "going through the motions"      │
│ actually means? What are the motions? What would it    │
│ look like to be *present* during them?                 │
└─────────────────────────────────────────────────────────┘

You
> I guess I'm not really there. My mind is elsewhere.

K-Mirror is thinking...

┌─────────────────────────────────────────────────────────┐
│ K-Mirror                                                │
│                                                         │
│ Where is your mind? And is the one who notices the     │
│ mind is elsewhere separate from the mind?              │
└─────────────────────────────────────────────────────────┘
```

### Commands During Conversation

Type these while chatting:

| Command | Purpose |
|---------|---------|
| `/new` | Start a new conversation |
| `/sessions` | List previous sessions |
| `/load <id>` | Continue a previous session |
| `/stats` | Show conversation statistics |
| `/rag` | Show knowledge base stats |
| `/end` | End session and save |
| `/help` | Show help |
| `/quit` | Exit (with save) |

### Example Session Flow

```bash
$ uv run main.py

# Welcome screen appears
# Session ID: a1b2c3d4-e5f6...

You
> My boss never listens to me

[K-Mirror processes and responds with inquiry]

You
> I've tried telling him multiple times but he dismisses me

You
> /stats

[Shows statistics about the conversation]

You
> /end

[Session saved, summary shown]
```

---

## How It Works: Data Flow

```
User Input
    ↓
[Listener Node]
  - Extract key phrases, context, emotional tone
    ↓
[Classifier Node]
  - Map to psychological patterns (12 types)
  - Find related principles
    ↓
[Retriever Node]
  - Fetch relevant K passages from vector store
    ↓
[Depth Assessor Node]
  - Gauge conversation depth (0-3)
  - Detect resistance signals
    ↓
[Inquiry Generator Node]
  - Select dialogue approach
  - Generate K-style response using Claude
    ↓
Response to User
  ↓
[Save to Anti-Memory DB]
  - Store question asked
  - Track when principles are "seen through"
  - TTL decay: questions naturally expire
```

---

## Understanding the Components

### 1. **Principles Engine** (`principles.py`)
12 Krishnamurti principles mapped to psychological patterns.

```python
# See which principles relate to a pattern
from principles import PATTERN_TO_PRINCIPLES, PsychPattern

patterns = PATTERN_TO_PRINCIPLES[PsychPattern.FEAR_OF_LOSS]
# Returns: [1, 8, 10] (Observer/Observed, Fear as Thought, Freedom as Seeing)
```

### 2. **Anti-Memory Database** (`db.py`)
Questions asked and principles seen are naturally forgotten.

```python
from db import UnlearnDB
from config import Settings

settings = Settings()
with UnlearnDB(settings.sqlite_db_path) as db:
    # Active questions (not expired)
    active = db.get_active_questions()

    # Questions user avoided
    deflected = db.get_open_inquiries()

    # Run garbage collection (remove expired)
    db.gc_expired_questions()

    # Monthly decay: confidence drops on insights
    db.decay_dissolved_patterns()
```

### 3. **Pattern Echo Detection** (`pattern_echo.py`)
Detects recurring patterns across conversation turns.

```python
from pattern_echo import PatternEchoDetector

detector = PatternEchoDetector()

# As conversation progresses, recorder turns
detector.record_turn(turn_analysis)

# Detect if same pattern appears in different context
echo = detector.detect_echo()
if echo:
    print(echo.describe())
    # "You mentioned this with your boss, now with your partner..."
```

### 4. **RAG Store** (`rag.py`)
Vector store of Krishnamurti passages for context.

```python
from rag import RAGStore
from config import Settings

settings = Settings()
store = RAGStore(settings)

# Query for passages
passages = store.query("fear and time", top_k=2)
# Returns relevant quotes

# Add custom passages
store.add_passage(
    "Your quote here",
    principle_id=8,  # Fear principle
    source="Custom"
)
```

### 5. **Session Management** (`session.py`)
Handle conversation state and persistence.

```python
from session import SessionManager

manager = SessionManager()

# Start new session
session = manager.create_session()

# Or load previous
session = manager.load_session("session-id")

# Add messages
session.add_message("I feel stuck", role="user")
session.add_message("Can you tell me more?", role="assistant")

# Save to disk
manager.save_session(session)

# List all sessions
sessions = manager.list_sessions()
```

### 6. **LangGraph Pipeline** (`app.py`)
Orchestrates all nodes together.

```python
from app import create_app

app = create_app()

# Start conversation
session = app.new_session()

# Process user input
response = app.process_input("I feel anxious about the future")
print(response)

# Get stats
stats = app.get_rag_stats()

# End and save
summary = app.end_conversation()
```

---

## Development Workflow with uv

### Running Tests

```bash
# With uv (no venv activation needed)
uv run pytest tests/ -v

# With venv activated
pytest tests/ -v --cov=src
```

### Adding New Dependencies

```bash
# Add a new package
uv pip install new-package

# Update pyproject.toml manually OR:
# Add to [project] dependencies section, then:
uv sync
```

### Quick REPL Exploration

```bash
# Start Python REPL with all imports available
uv run python3

# Then in the REPL:
>>> from principles import PRINCIPLES
>>> print(PRINCIPLES[1].name)
"Observer is the Observed"
```

### Debugging

```bash
# Run with debugging output
uv run python3 -u main.py  # unbuffered output

# Or with ipdb
uv run python3 -m ipdb main.py
```

---

## Configuration Options

Edit `.env` to customize:

```bash
# LLM
anthropic_api_key=sk-...

# Storage
chroma_persist_dir=data/chroma_db      # Vector store location
sqlite_db_path=data/unlearn.db         # Anti-memory DB

# TTL settings (question expiration)
default_question_ttl_days=14           # Days before question expires
deflected_question_ttl_days=30         # Longer for unanswered
explored_question_ttl_days=7           # Shorter for "seen"

# Insight decay
insight_decay_rate_per_month=0.05      # 5% monthly confidence loss
insight_removal_threshold=0.1          # Remove if below 10% confidence

# Embeddings
embedding_model=all-MiniLM-L6-v2       # Sentence transformer model
```

---

## Troubleshooting

### "ImportError: No module named 'langgraph'"
```bash
# Reinstall dependencies
uv pip install --force-reinstall -e .
```

### "anthropic_api_key not found"
```bash
# Check .env file exists and has key
cat .env | grep anthropic_api_key

# If missing:
echo "anthropic_api_key=sk-..." >> .env
```

### "ChromaDB connection error"
```bash
# Check data directory exists
mkdir -p data/chroma_db

# Or reset the store
rm -rf data/chroma_db
# It will be recreated on next run
```

### "Database is locked"
```bash
# Kill any stale Python processes
pkill -f "python.*k-mirror"

# Or check specific port
lsof -i :8000
```

### "LLM API rate limit"
```bash
# The app will retry. If persistent:
# 1. Check your API key is valid
# 2. Check billing in Anthropic console
# 3. Wait a bit and try again
```

---

## Project Structure

```
K-mirror/
├── main.py                      # Entry point
├── cli.py                       # Rich CLI interface
├── app.py                       # LangGraph orchestrator
├── nodes.py                     # All 5 pipeline nodes
├── principles.py                # 12 K principles (100% complete)
├── state.py                     # LangGraph state (100% complete)
├── signals.py                   # Insight detection (100% complete)
├── pattern_echo.py              # Echo detection (100% complete)
├── db.py                        # Anti-memory DB (100% complete)
├── session.py                   # Session management
├── rag.py                       # ChromaDB integration
├── config.py                    # Settings (100% complete)
├── pyproject.toml               # Project config (for uv)
├── .env                         # Configuration (GITIGNORED)
├── data/
│   ├── chroma_db/              # Vector store (auto-created)
│   ├── unlearn.db              # SQLite DB (auto-created)
│   └── sessions/               # Saved sessions (auto-created)
├── tests/                       # Test suite (to be expanded)
├── claude.md                    # Quick reference
├── wiki_home.md                 # Full documentation
└── CLAUDE_CLI_GUIDE.md          # Claude Code integration
```

---

## Next Steps After Setup

### First Run
1. Run `uv run main.py`
2. Share a psychological concern
3. Observe how K-Mirror mirrors back your words
4. Notice patterns being reflected
5. Type `/end` to save session

### Explore Features
- Use `/load <session_id>` to continue previous conversations
- Try different types of concerns (fear, comparison, identity)
- Watch how depth_level increases across turns
- Check `/stats` to see patterns detected

### Development
- Add custom K passages via `rag.py`
- Extend dialogue approaches in `principles.py`
- Build custom nodes for your workflow
- Write tests in `tests/` directory

---

## Performance Notes

- **First run**: Takes ~10-15s (initializes RAG store)
- **Subsequent runs**: ~2-3s per LLM call
- **Database queries**: < 100ms (SQLite + ChromaDB)
- **Memory usage**: ~300MB with ChromaDB loaded

---

## Quick Reference: Common Commands

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e .

# Run
uv run main.py

# Test
uv run pytest tests/ -v

# Interactive debugging
uv run python3
>>> from app import create_app
>>> app = create_app()
>>> app.process_input("I feel stuck")

# Check installation
uv run python3 -c "from app import KMirrorApp; print('✓')"
```

---

## Support & Resources

- **Krishnamurti teachings**: https://jkrishnamurti.org
- **LangGraph docs**: https://langchain.com/langgraph
- **ChromaDB docs**: https://docs.trychroma.com
- **Anthropic Claude API**: https://console.anthropic.com

---

**Ready to explore? Start with: `uv run main.py`** 🚀
