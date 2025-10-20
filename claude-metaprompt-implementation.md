# Metaprompt: Stoic Terminal Implementation

You are an expert Python developer tasked with implementing "Stoic Terminal" - a context-aware philosophical quote display tool for terminals. You have access to comprehensive research and specifications. Your goal is to initialize the repository and begin systematic implementation.

## Project Overview

Stoic Terminal displays philosophical quotes with ASCII art in the terminal, using semantic search and contextual awareness (time of day, weather, git activity) to select relevant quotes. It's a UV-installable Python tool targeting <500ms startup and beautiful terminal display.

## Available Documentation

You have these research documents:
1. **Technical Specification** (`stoic-terminal-spec.md`) - Original architecture
2. **Implementation Plan** (`stoic-terminal-implementation-plan.md`) - 7-day roadmap with all decisions
3. **Quick Reference** (`stoic-terminal-quick-reference.md`) - TL;DR of key decisions
4. **Day 1 Starter Code** (`day1_starter_code.py`) - Database and collection script
5. **Quote Research** (`philosophical_quote_DB_research.md`) - Source analysis
6. **Weather Research** (`weather_apis_research.md`) - API comparison
7. **ASCII Art Research** (`ascii_art_research.md`) - Implementation strategies
8. **Embedding Models** (`lightweight_embedding_models_search_results.md`) - Model selection

## Key Technical Decisions (Already Made)

- **Language**: Python 3.10+ with UV for distribution
- **Quotes**: Quotable API + Project Gutenberg (public domain)
- **Weather**: Open-Meteo (no API key required!)
- **ASCII Art**: Pre-curated from asciiart.eu + asweigart's database
- **Embeddings**: sentence-transformers with all-MiniLM-L6-v2 (90MB)
- **Database**: SQLite with semantic search via embeddings
- **Performance Target**: <500ms startup, <100ms display

## Your Task

### Phase 1: Repository Initialization

Create a professional Python project structure:

```
stoic-terminal/
├── pyproject.toml           # UV tool config with dependencies
├── README.md                # Installation and usage guide
├── LICENSE                  # MIT or similar
├── .gitignore              # Python standard
├── CONTRIBUTING.md          # Contribution guidelines
├── src/
│   └── stoic_terminal/
│       ├── __init__.py
│       ├── cli.py          # Entry point
│       ├── database.py     # SQLite abstraction
│       ├── embeddings.py   # Semantic search
│       ├── context.py      # Time/weather/git detection
│       ├── ascii_art.py    # Art loading
│       ├── display.py      # Terminal rendering
│       └── config.py       # User configuration
├── data/
│   ├── ascii_art/
│   │   └── metadata.yaml
│   └── .gitkeep
├── scripts/
│   ├── collect_quotes.py   # Quote collection tool
│   └── build_embeddings.py # Embedding generation
└── tests/
    ├── __init__.py
    └── test_database.py
```

**Key files to create:**

1. **pyproject.toml** - UV tool configuration with:
   - Dependencies: sentence-transformers, requests, pyyaml, pyfiglet, numpy
   - Entry point: `stoic-terminal = stoic_terminal.cli:main`
   - Python >=3.10

2. **README.md** - Include:
   - Project description and philosophy
   - Quick start installation (`uv tool install .`)
   - Configuration instructions (optional weather setup)
   - Usage examples
   - Attribution (Open-Meteo, quote sources)

3. **.gitignore** - Standard Python + additions:
   - `*.db` (user's quote database)
   - `.cache/` (model cache)
   - `data/quotes_*.db` (except example)

### Phase 2: Implement Core Components (Priority Order)

Follow the 7-day plan but adapt as needed. Implement in this order:

**Day 1 Priority: Database Layer**
- Implement `database.py` with QuoteDatabase class
- Schema from spec (quotes table with embedding BLOB)
- Methods: add_quote(), get_all_quotes(), search_by_tags(), get_random_quote()
- Use the provided starter code as foundation

**Day 2 Priority: Quote Collection**
- Implement `scripts/collect_quotes.py`
- Quotable API integration (https://api.quotable.io)
- Fetch 200+ quotes with tags
- Store with proper attribution

**Day 3 Priority: ASCII Art Foundation**
- Create `ascii_art.py` with ASCIIArtLoader class
- Implement LRU caching (@lru_cache(maxsize=128))
- Create 6 theme folders in data/ascii_art/
- Add metadata.yaml schema
- Include 5-10 example art pieces (from asciiart.eu)

**Day 4 Priority: Semantic Search**
- Implement `embeddings.py`
- Load all-MiniLM-L6-v2 model
- Pre-compute embeddings for quotes
- Store in DB as BLOB (384 floats × 4 bytes = 1536 bytes)
- Implement cosine similarity search

**Day 5 Priority: Context Detection**
- Implement `context.py`
- Time detection (morning/afternoon/evening/night)
- Open-Meteo weather integration (no API key!)
- Git analysis (optional, use `gh` CLI if available)
- Map context → tags

**Day 6 Priority: Display System**
- Implement `display.py`
- Terminal width detection with fallbacks
- ASCII art + quote rendering
- pyfiglet for author headers
- Responsive display (120/80/40 column variants)

**Day 7 Priority: CLI Interface**
- Implement `cli.py` with argparse
- Commands: default (context-aware), --random, --theme X
- Config commands: --init, --set-location
- Shell integration helper

## Implementation Guidelines

### Code Quality Standards
- **Type hints**: Use on all function signatures
- **Docstrings**: Google style for all public methods
- **Error handling**: Graceful degradation, never crash
- **Logging**: Use Python logging module (DEBUG level)
- **Testing**: Write pytest tests for core functions

### Performance Requirements
- Model loading: <100ms (use caching)
- Database queries: <50ms
- ASCII art loading: <5ms (LRU cache)
- Total startup: <500ms
- Quote display: <100ms

### Code Style
- Follow PEP 8
- Use pathlib for file paths
- Use context managers for file/DB operations
- Type annotations from __future__ import annotations
- Keep functions focused and single-purpose

### Dependencies to Install
```python
# In pyproject.toml:
dependencies = [
    "sentence-transformers>=2.2.0",
    "requests>=2.28.0",
    "pyyaml>=6.0",
    "pyfiglet>=0.8.0",
    "numpy>=1.21.0",
]
```

## Critical Implementation Details

### Database Schema
```sql
CREATE TABLE quotes (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    author TEXT NOT NULL,
    source TEXT,
    tradition TEXT,
    tags TEXT,              -- JSON array
    embedding BLOB,         -- 1536 bytes (384 floats)
    copyright_status TEXT
);
```

### Weather API (Open-Meteo)
```python
# NO API KEY NEEDED!
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": lat,
    "longitude": lon,
    "current_weather": "true"
}
response = requests.get(url, params=params)
```

### Semantic Search Pattern
```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')
quote_embeddings = model.encode(quotes, convert_to_tensor=True)
query_embedding = model.encode(context_desc, convert_to_tensor=True)
similarities = util.cos_sim(query_embedding, quote_embeddings)
best_match = quotes[similarities.argmax()]
```

## Success Criteria

After implementation, the tool should:
- ✅ Install via `uv tool install .`
- ✅ Run with zero configuration (quotes work immediately)
- ✅ Display beautiful ASCII art + quote on invocation
- ✅ Support optional weather context (if user configures)
- ✅ Start in <500ms with 250 quotes
- ✅ Work on Linux, macOS, Windows
- ✅ Gracefully degrade (no weather = still works)
- ✅ Include 250+ quotes with proper attribution

## Execution Instructions

1. **Start with pyproject.toml and README.md** - Set the foundation
2. **Create the directory structure** - All folders and __init__.py files
3. **Implement database.py** - Core data layer first
4. **Build quote collection script** - Get data flowing
5. **Add ASCII art infrastructure** - Display foundation
6. **Integrate semantic search** - Intelligence layer
7. **Wire up context detection** - Smart selection
8. **Complete CLI and display** - User-facing interface
9. **Test end-to-end** - Verify all flows work
10. **Polish documentation** - Make it accessible

## What to Ask Me

If you encounter decisions not covered in the specs:
- Ask about trade-offs (performance vs features)
- Ask about scope (is this feature v1.0 or v2.0?)
- Ask about user experience choices
- Ask about error handling strategies

## Output Format

For each component you implement:
1. **Show the code** - Complete, working implementations
2. **Explain key decisions** - Why you chose this approach
3. **Note dependencies** - What other components need this
4. **Test instructions** - How to verify it works
5. **Next steps** - What to build next

## Begin Implementation

Start by:
1. Creating the complete project structure (all folders and files)
2. Writing pyproject.toml with proper UV configuration
3. Implementing database.py with the complete schema
4. Creating a simple test to verify database operations

Show me the initial structure and first components, then we'll proceed systematically through the implementation.

Remember: The goal is a working v1.0 in 7 days. Prioritize functionality over perfection. Ship it, then iterate!
