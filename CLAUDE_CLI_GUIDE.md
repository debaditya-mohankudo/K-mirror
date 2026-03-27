# K-Mirror: Claude CLI Developer Guide

This guide explains how to develop and work with K-Mirror using **Claude Code CLI** (`claude` command).

---

## Quick Start

### 1. Prerequisites
```bash
# Ensure you have Claude Code CLI installed
claude --version

# Check Python version (3.11+ required)
python3 --version

# Navigate to project directory
cd /Users/debaditya/workspace/K-mirror
```

### 2. One-Time Setup
```bash
# Create .env file with required secrets
echo "anthropic_api_key=sk-..." > .env
echo "embedding_model=all-MiniLM-L6-v2" >> .env
echo "chroma_persist_dir=data/chroma_db" >> .env
echo "sqlite_db_path=data/unlearn.db" >> .env

# Install dependencies
pip install -e .

# Initialize vector store directory
mkdir -p data
```

### 3. Start Claude Code Session
```bash
# Open project in Claude Code
claude

# In Claude, you can now:
# - Ask questions about the codebase
# - Request code changes
# - Run tests
# - Execute Python scripts
# - Create new files
```

---

## Working with Claude in This Project

### Common Workflows

#### 1. **Understanding the Codebase**
```
User: "What does the pattern_echo module do?"
Claude: [reads pattern_echo.py, explains echo detection logic]

User: "Show me how to use the anti-memory database"
Claude: [shows code examples from wiki_home.md]

User: "What's the relationship between principles.py and pattern_echo.py?"
Claude: [explains module interdependencies]
```

#### 2. **Implementing Missing Features**
```
User: "Implement the Classifier node for LangGraph"
Claude:
  - Reads principles.py to understand pattern mapping
  - Reads state.py to understand input/output
  - Creates new node that uses PATTERN_TO_PRINCIPLES
  - Writes tests

User: "Add input validation to db.py record_question()"
Claude:
  - Audits current code for validation gaps
  - Adds bounds checking (0 ≤ confidence ≤ 1)
  - Updates docstrings
  - Creates test cases
```

#### 3. **Debugging & Troubleshooting**
```
User: "Why is pattern echo not detecting repeats?"
Claude:
  - Reads pattern_echo.py detect_echo() logic
  - Checks for edge cases (empty turns, same context)
  - Writes test with step-by-step debugging
  - Identifies root cause

User: "Test if signals.quick_assess() handles empty strings"
Claude:
  - Writes unit test
  - Runs quick_assess("")
  - Identifies missing validation
  - Suggests fix
```

#### 4. **Documentation & Code Exploration**
```
User: "Document all regex patterns in signals.py with examples"
Claude:
  - Extracts INTELLECTUAL_PATTERNS and INSIGHT_PATTERNS
  - Creates markdown table with examples
  - Tests each pattern with sample text

User: "Generate a dependency diagram showing how config.py is used"
Claude:
  - Greps for `from config import`
  - Creates visual ASCII diagram
  - Documents each dependency relationship
```

---

## Claude Code Features for This Project

### 1. **File Search & Navigation**
```bash
# Find all files using a module
claude> grep "from principles import" --type=py

# List all Python files in project
claude> glob "**/*.py"

# Read a specific file with context
claude> read src/nodes/classifier.py
```

### 2. **Code Analysis & Refactoring**
```bash
# Ask Claude to review code quality
User: "Review signals.py for code quality issues"
Claude:
  - Checks for type hints ✅
  - Checks for error handling ❌ (suggests improvements)
  - Checks for docstrings ✅
  - Suggests refactoring opportunities

# Ask for simplification
User: "Simplify the pattern matching logic in db.py"
Claude:
  - Uses /simplify skill to review for reuse
  - Consolidates similar queries
  - Reduces duplication
```

### 3. **Testing & Validation**
```bash
# Run tests
User: "Run tests for principles.py module"
Claude:
  - Creates test file (if none exists)
  - Writes unit tests using pytest
  - Executes: pytest tests/test_principles.py -v
  - Shows coverage report

# Validate implementation
User: "Test if quick_assess() handles all edge cases"
Claude:
  - Writes comprehensive test cases
  - Tests: empty string, unicode, very long input, special chars
  - Identifies gaps in error handling
```

### 4. **Interactive Development**
```bash
# Live REPL development
User: "Let me test the pattern_echo detector interactively"
Claude:
  - Opens Python REPL
  - Imports PatternEchoDetector
  - Creates sample data
  - Runs step-by-step detection
  - Shows results in real-time

# Jupyter notebook style
User: "Create a notebook to explore the principles database"
Claude:
  - Creates .ipynb file
  - Loads principles.py
  - Shows tables, statistics, query examples
  - Allows interactive exploration
```

---

## Project-Specific Claude Commands

### Recommended Aliases & Shortcuts

Create `~/.claude/aliases` for this project (if using custom settings):

```bash
# Useful commands for K-Mirror development

# Run all tests
alias test="pytest tests/ -v --cov=src"

# Check code quality
alias lint="flake8 src/ --max-line-length=100"

# Develop interactively
alias dev="python3 -i -c \"from config import Settings; from principles import *; from db import *\""

# Database cleanup
alias db-clean="rm -f data/unlearn.db; echo 'Database reset'"

# Run type checker
alias type-check="mypy src/ --ignore-missing-imports"
```

### Common Claude Prompts for This Project

```
# 1. Implement a node
"Implement the [Classifier|Retriever|Inquiry Generator] node for LangGraph
 that takes KMirrorState and updates [current_patterns|retrieved_passages|messages]"

# 2. Add tests
"Write pytest fixtures and test cases for [module].py covering:
 - Happy path
 - Edge cases
 - Error conditions"

# 3. Refactor
"Refactor [module].py to:
 - Add input validation
 - Improve error messages
 - Add type hints
 - Add docstrings"

# 4. Debug
"Debug why [component] isn't working. Trace through:
 - Input conditions
 - State transformations
 - Output validation"

# 5. Performance
"Profile [module] and optimize:
 - Database queries
 - Regex pattern matching
 - LLM prompt generation"

# 6. Documentation
"Create a markdown guide for using [module] with:
 - Code examples
 - Common patterns
 - Edge cases
 - Troubleshooting"
```

---

## Development Workflow

### Typical Session Flow

#### **Session 1: Understanding**
```
1. User: "Explain the K-Mirror architecture"
2. Claude reads: claude.md, wiki_home.md, principles.py
3. Claude draws ASCII diagram of data flow
4. User asks clarifying questions
5. Claude refines explanation
```

#### **Session 2: Implementation**
```
1. User: "Implement the Classifier node"
2. Claude:
   - Reads state.py (input/output structure)
   - Reads principles.py (pattern mapping logic)
   - Writes classifier node that:
     * Extracts patterns from user message
     * Maps to principles using PATTERN_TO_PRINCIPLES
     * Updates state.matched_principles
   - Writes unit tests
   - Shows code for review
3. User: "Looks good, make it detect patterns from context_words too"
4. Claude enhances with NLP pattern detection
5. Claude runs tests, all pass
```

#### **Session 3: Integration**
```
1. User: "Wire Classifier node into the LangGraph"
2. Claude:
   - Reads existing graph definition
   - Adds classifier node
   - Connects edges
   - Writes integration test
3. User: "Test with a sample conversation"
4. Claude:
   - Creates test conversation
   - Runs through pipeline
   - Shows state transformations at each node
   - Validates outputs
```

#### **Session 4: Testing & Polish**
```
1. User: "Write comprehensive tests for the full pipeline"
2. Claude:
   - Creates test fixtures (sample conversations)
   - Tests each node independently
   - Tests full pipeline integration
   - Tests edge cases
   - Reports coverage
3. User: "What's the coverage?"
4. Claude: "[coverage report]"
5. User: "Add tests for missing coverage"
6. Claude creates targeted tests
```

---

## Settings & Configuration for Claude Code

### Recommended `settings.json` for K-Mirror

```json
{
  "model": "claude-opus-4-6",
  "permissions": {
    "global": ["read", "bash"],
    "user": ["edit", "write", "bash"]
  },
  "hooks": {
    "when_tool_fails": {
      "timeout": true,
      "shell_error": true
    }
  },
  "project": {
    "name": "K-Mirror",
    "root": "/Users/debaditya/workspace/K-mirror",
    "language": "python",
    "python_version": "3.11+"
  },
  "environment": {
    "PYTHONPATH": "/Users/debaditya/workspace/K-mirror",
    "DEBUG": false
  }
}
```

### Using Fast Mode
```bash
# Enable fast mode for quick iterations
/fast

# This uses Claude Opus 4.6 with faster output
# Great for: code generation, file edits, testing
# Not ideal for: complex reasoning, architecture decisions

# Disable to return to full reasoning
/fast
```

---

## Advanced Workflows

### 1. **Multi-File Refactoring**
```
User: "Refactor signals.py and db.py to use a shared validation module"

Claude:
  - Analyzes both files
  - Identifies common validation patterns
  - Creates new validation module
  - Updates imports in both files
  - Runs tests
  - Shows before/after comparison
```

### 2. **Feature Development**
```
User: "Add support for multi-turn dialogue patterns. Requirements:
  - Track dialogue turn number
  - Different prompts for different turn levels
  - Adapt based on pattern_echo results"

Claude:
  - Breaks down into sub-tasks
  - Updates state.py (add dialogue_turn_number)
  - Updates principles.py (add turn-specific dialogue templates)
  - Updates inquiry_generator node
  - Writes integration test
  - Documents new feature
```

### 3. **Performance Optimization**
```
User: "Profile and optimize database queries"

Claude:
  - Runs cProfile on db.py methods
  - Identifies slow queries
  - Suggests indices
  - Benchmarks before/after
  - Documents performance gains
```

### 4. **Investigation & Debugging**
```
User: "Why is the confidence decay formula producing unexpected results?"

Claude:
  - Extracts decay logic from db.py
  - Creates test cases with known inputs
  - Traces through calculation
  - Compares expected vs. actual
  - Identifies root cause (floating point precision? formula error?)
  - Suggests fix
  - Validates with test
```

---

## Collaboration with Claude

### Code Review Workflow
```
1. You write some code
2. User: "Review this code: [paste code]"
3. Claude:
   - Checks type hints ✅
   - Checks error handling ✅
   - Checks for bugs ❌ (suggests fix)
   - Checks readability ✅
   - Suggests improvements
4. User: "Make those improvements"
5. Claude updates code, shows diff
6. You approve and commit
```

### Pair Programming
```
1. User: "Let's build the Retriever node together"
2. Claude:
   - Explains what it needs to do
   - Asks clarifying questions
   - Writes skeleton
   - User suggests changes
   - Claude implements suggestions
   - Claude writes tests
   - You both review
```

### Learning Mode
```
1. User: "Explain how TTL decay works in db.py"
2. Claude:
   - Shows the decay formula
   - Explains each component
   - Gives examples with numbers
   - Shows code implementation
   - Explains why this aligns with K philosophy
3. User: "How would we implement periodic decay?"
4. Claude: [explains implementation options]
```

---

## Tips & Best Practices

### 1. **Be Specific in Requests**
```
❌ Bad: "Fix the database"
✅ Good: "Add input validation to record_question() to ensure principle_id
         is between 1-12 and confidence is 0-1. Add docstring explaining
         valid ranges."
```

### 2. **Use Iterative Refinement**
```
1. User: "Implement the Classifier node"
2. Claude writes basic version
3. User: "Add logging for debugging"
4. Claude adds logging
5. User: "Make pattern detection case-insensitive"
6. Claude updates logic
7. User: "Add caching to improve performance"
8. Claude adds caching layer
```

### 3. **Leverage Code Examples**
```
User: "Here's how I want pattern detection to work: [show example]
       Can you implement this?"

Claude: [understands intent from example, implements + tests]
```

### 4. **Ask Claude to Trace Through**
```
User: "Trace through what happens when user says 'My boss never listens'"

Claude:
  1. Input: "My boss never listens"
  2. Listener node: extracts key_phrases = ["boss", "never listens"]
  3. Classifier node: matches RELATIONSHIP_CONFLICT pattern
  4. Pattern echo: checks against previous turns
  5. Retrieved passages: fetches K talks about relationships
  6. Depth assessor: surface level (first mention)
  7. Inquiry generator: selects mirror dialogue approach
  8. Signal assessment: user response → genuine vs intellectual
  [shows full state at each step]
```

### 5. **Use `/simplify` Skill**
```
After implementing a feature:
User: "/simplify"

Claude uses simplify skill to:
  - Review for code reuse opportunities
  - Check for similar functions
  - Suggest consolidation
  - Check for dead code
  - Report on code quality
```

---

## Testing in Claude Code

### Running Tests

```bash
# Run all tests
claude> bash -c "pytest tests/ -v"

# Run specific test file
claude> bash -c "pytest tests/test_principles.py -v"

# Run with coverage
claude> bash -c "pytest tests/ --cov=src --cov-report=html"

# Run interactively (step through failures)
claude> bash -c "pytest tests/ -x -vv"  # Stop on first failure
```

### Creating Tests with Claude

```
User: "Write comprehensive tests for the quick_assess() function
       in signals.py. Cover all regex patterns and edge cases."

Claude:
  - Reads signals.py (INTELLECTUAL_PATTERNS, INSIGHT_PATTERNS)
  - Creates test_signals.py with:
    * Test for each INTELLECTUAL pattern
    * Test for each INSIGHT pattern
    * Tests for ambiguous cases
    * Tests for empty/special input
    * Tests for confidence values
  - Runs tests: all pass
  - Shows coverage: 100%
```

---

## Documentation in Claude Code

### Generate Documentation
```
User: "Generate API documentation for all modules"

Claude creates:
  - Module docstrings (if missing)
  - Function signatures with type hints
  - Usage examples
  - README for each module
  - Architecture diagrams
```

### Update Wiki
```
User: "Add a section to wiki_home.md showing how to debug pattern echoes"

Claude:
  - Reads wiki_home.md
  - Adds new section with:
    * Common issues
    * Step-by-step debugging
    * Example code
    * Expected outputs
```

---

## Keyboard Shortcuts & Commands

### Essential Claude Code Commands

```
/help              - Show all available commands
/clear             - Clear conversation history
/fast              - Toggle fast mode (faster output)
/code              - Show recent code changes
/files             - List files you've read/edited
/memory            - Show session memory
/settings          - Show Claude Code settings

# File operations
/read <path>       - Read file with syntax highlighting
/edit <path>       - Edit file interactively
/write <path>      - Create or overwrite file
/glob <pattern>    - Find files matching pattern
/grep <pattern>    - Search file contents

# Execution
/run <command>     - Run bash command
/test              - Run test suite
/debug             - Enter debugging mode
```

### Custom Shortcuts

Add to `~/.claude/keybindings.json`:

```json
{
  "bindings": [
    {
      "keys": ["ctrl+shift+t"],
      "command": "run",
      "args": "pytest tests/ -v"
    },
    {
      "keys": ["ctrl+shift+d"],
      "command": "run",
      "args": "python3 -m pytest tests/ -x -vv"
    },
    {
      "keys": ["ctrl+shift+l"],
      "command": "run",
      "args": "flake8 src/"
    }
  ]
}
```

---

## Troubleshooting Common Issues

### Issue: Claude can't find imported modules
```
Solution: Set PYTHONPATH
  bash> export PYTHONPATH=/Users/debaditya/workspace/K-mirror:$PYTHONPATH
  bash> python3 -c "from principles import PRINCIPLES"
```

### Issue: Tests fail with missing dependencies
```
Solution: Install in editable mode
  bash> pip install -e .
```

### Issue: `.env` file not being read
```
Solution: Ensure file location and format
  bash> cat .env  # Verify content
  bash> python3 -c "from config import Settings; print(Settings())"
```

### Issue: Database file locked (concurrent access)
```
Solution: Check for stale processes
  bash> lsof | grep unlearn.db
  bash> kill -9 <PID>  # Kill stale process
```

### Issue: Claude suggests code that doesn't match existing style
```
Solution: Show Claude the style guide
  User: "Follow the coding style in [module].py"
  Claude will analyze and match style
```

---

## Example: Full Development Session

### Goal: Implement the Classifier Node

```
SESSION START
=============

User: "I want to implement the Classifier node. What do I need to know?"

Claude: [reads state.py, principles.py, wiki_home.md]
"The Classifier node needs to:
1. Extract features from user message
2. Match against PsychPatterns using pattern_to_principles mapping
3. Update state.matched_principles
Here's the plan..."

User: "OK, let's do it. Start with the skeleton"

Claude: [writes classifier_node() function]
"Here's the skeleton. It:
- Takes KMirrorState as input
- Extracts key phrases and context
- Looks up patterns
- Returns updated state"

User: "How do we actually detect patterns? What NLP approach?"

Claude: "Good question. Three options:
1. Keyword matching (fast, deterministic)
2. Regex patterns (moderate complexity)
3. LLM-based (most accurate, slowest)
For now, let's do keyword + pattern matching since we have regex in signals.py"

User: "OK, implement that"

Claude: [implements pattern detection logic]
"Here's the implementation with:
- Keyword extraction from message
- Pattern matching using principles.py
- Confidence scoring
- Edge case handling"

User: "Write tests"

Claude: [creates test_classifier.py]
"Tests cover:
- Single pattern detection
- Multiple patterns
- No pattern match
- Case insensitivity
- Special characters
- All 12 patterns"

User: "Run the tests"

Claude: [runs pytest]
"All tests pass! ✅ Coverage: 95%"

User: "Integrate it into the graph"

Claude: [adds node to LangGraph]
"Graph now has:
graph.add_node("classifier", classifier_node)
graph.add_edge("listener", "classifier")
graph.add_edge("classifier", "depth_assessor")

Ready to test end-to-end?"

User: "Test with a sample conversation"

Claude: [creates test conversation, traces through]
"Sample input: 'My boss never listens to my ideas'
State evolution:
Turn 1:
  input → key_phrases: ["boss", "ideas"]
       → patterns: [RELATIONSHIP_CONFLICT, SEEKING_AUTHORITY]
       → principles: [7, 5, 10]
Output: Updated state with matched_principles = [7, 5, 10]

Ready for next node?"

User: "Yes, implement Depth Assessor next"

SESSION CONTINUES...
```

---

## Recommended Claude Code Settings for K-Mirror

```json
{
  "model": "claude-opus-4-6",
  "fast_mode": false,
  "permissions": {
    "global": {
      "read": true,
      "glob": true,
      "grep": true
    },
    "user": {
      "bash": true,
      "edit": true,
      "write": true
    }
  },
  "project": {
    "name": "K-Mirror",
    "root": "/Users/debaditya/workspace/K-mirror",
    "language": "python",
    "version": "3.11+",
    "main_files": [
      "claude.md",
      "wiki_home.md",
      "CLAUDE_CLI_GUIDE.md",
      "principles.py",
      "state.py",
      "db.py"
    ]
  },
  "testing": {
    "framework": "pytest",
    "test_dir": "tests/",
    "coverage_target": 80
  },
  "editor": {
    "tabs": 4,
    "line_length": 100
  }
}
```

---

## Summary

**K-Mirror is optimized for Claude Code development:**

✅ Clean, modular architecture (easy to read/modify)
✅ Comprehensive documentation (context for Claude)
✅ Type hints throughout (Claude understands structure)
✅ Test framework ready (Claude can write tests immediately)
✅ Anti-memory design (aligns with K philosophy for learning-focused development)

**Best Claude Code workflows for this project:**
- **Understanding**: Ask Claude to explain modules and architecture
- **Implementation**: Use iterative refinement with /fast mode for speed
- **Testing**: Let Claude write comprehensive test suites
- **Integration**: Have Claude wire components together and trace through
- **Documentation**: Generate docs automatically as you build

**Your superpower:** You think strategically about *what* to build; Claude handles *how* to build it, tests it, and documents it.

---

**Happy developing with Claude! 🚀**
