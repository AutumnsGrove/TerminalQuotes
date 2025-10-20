# Stoic Terminal - Implementation Roadmap (Post-Research)

## Executive Summary

Based on comprehensive research across quotes, weather APIs, ASCII art, and embedding models, we have a clear path to launch. **This project can ship a working v1.0 with 250 quotes in 7 days.**

## Research Findings & Decisions

### 1. Quote Collection Strategy ✅

**Primary Sources:**
- **Quotable API** (Immediate): 2,500+ quotes, MIT licensed, no API key, 180 req/min
  - Start here for rapid collection (100-150 quotes in 2 hours)
- **Project Gutenberg** (Legal Foundation): Public domain classics
  - Marcus Aurelius Meditations (50 quotes)
  - Sun Tzu Art of War (30 quotes)
  - Seneca's Letters (25 quotes)
  - Confucius Analects (20 quotes)
- **Abirate/english_quotes** (Quality Validation): 2,508 curated with misattribution warnings
  - Use for gap-filling and verification

**Legal Safety:**
- Pre-1930 published works are public domain (Marcus Aurelius, Seneca, Sun Tzu, Confucius = SAFE)
- No fair use assumptions needed if we stick to public domain
- Can safely publish to HuggingFace with proper attribution

**Quality Strategy:**
- Start with 250 hand-curated quotes (Week 1)
- Expand to 500 (Week 2-3)
- Scale to 1,000+ (Month 1)
- Only go to 5K-10K if repetition becomes an issue

### 2. Weather API Decision ✅

**Winner: Open-Meteo**
- **NO API key required** - Zero setup friction!
- 10,000 requests/day (far exceeds our needs)
- AGPLv3 licensed, open-source friendly
- Global coverage, simple JSON API
- 99.999% uptime

**Implementation:**
```python
# No setup needed! Just make requests:
import requests

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    return requests.get(url).json()
```

**User Experience:**
- Optional config (tool works without it)
- Users can provide: city name (geocoded), coordinates, or skip
- Cache responses for 60 minutes
- Graceful fallback if API unreachable

### 3. ASCII Art Strategy ✅

**Three-Tier Approach:**

**Tier 1: Immediate Launch (Days 1-2)**
- Clone asweigart's JSON database: `git clone https://github.com/asweigart/asciiartjsondb.git`
- Manually curate 30-50 pieces from asciiart.eu:
  - Meditation: 5-8 pieces (Buddha, lotus, zen garden, flowing water)
  - Adversity: 5-8 pieces (storm, mountain climb, anvil, fortress)
  - Exploration: 5-8 pieces (ship, compass, mountain peak, path)
  - Nature: 5-8 pieces (trees, mountains, sunrise, ocean)
  - Wisdom: 5-8 pieces (books, owl, scrolls, candle)
  - General: 5-8 pieces (decorative borders, simple frames)
- Use pyfiglet for author attribution headers

**Tier 2: Production Polish (Week 1)**
- Create size variants: 40/60/80/100/120 column versions
- Implement responsive loading (picks best-fit for terminal width)
- Build YAML metadata system with theme tags
- Add graceful degradation (complex → simple → text-only)

**Tier 3: Community Scaling (Month 1+)**
- Community contribution guidelines
- Automated validation for new submissions
- Seasonal/event-based art rotations

**Performance:**
- Pre-loading with LRU cache: <1ms art loading
- Terminal width detection: <1ms
- Total display time: 3-15ms (well under 100ms target)

### 4. Semantic Search Setup ✅

**Model Choice: all-MiniLM-L6-v2**
- **Size**: 90 MB (loads in <100ms)
- **Quality**: 56-58 MTEB score (excellent for philosophical text)
- **Speed**: 14,000 sentences/second on CPU
- **Reliability**: 1.5B+ downloads, battle-tested
- **Embedding dimension**: 384 (perfect for short quotes)

**Why Not Alternatives:**
- potion-base-8M: 500x faster but 10% quality loss (not worth it for our use case)
- paraphrase-mpnet-base-v2: Better quality but 420MB (overkill for v1)

**Implementation Strategy:**
1. Pre-compute embeddings at installation time
2. Store embeddings in SQLite as BLOB (15MB for 10K quotes)
3. Real-time search: <5ms with cosine similarity
4. Total startup: ~100-150ms (well under 500ms target)

```python
from sentence_transformers import SentenceTransformer, util

# One-time setup
model = SentenceTransformer('all-MiniLM-L6-v2')
quote_embeddings = model.encode(quotes, convert_to_tensor=True)

# Runtime query (<5ms)
query_embedding = model.encode(context_description, convert_to_tensor=True)
similarities = util.cos_sim(query_embedding, quote_embeddings)
top_quote = quotes[similarities.argmax()]
```

## Finalized Architecture

### Database Schema

```sql
-- Main quotes table
CREATE TABLE quotes (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    author TEXT NOT NULL,
    source TEXT,                    -- Book/speech name
    source_context TEXT,            -- Chapter, date, occasion
    source_year INTEGER,
    translator TEXT,
    length_category TEXT CHECK(length_category IN ('bite-sized', 'medium', 'extended')),
    tradition TEXT,                 -- 'stoic', 'buddhist', 'military', 'exploration', etc.
    tags TEXT,                      -- JSON array: ["adversity", "perseverance", "wisdom"]
    embedding BLOB,                 -- 384-dim vector (1536 bytes)
    copyright_status TEXT,          -- 'public_domain', 'attributed', etc.
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Git session tracking (separate DB)
CREATE TABLE git_sessions (
    id INTEGER PRIMARY KEY,
    session_start TIMESTAMP,
    session_end TIMESTAMP,
    total_commits INTEGER,
    total_lines_changed INTEGER,
    commit_messages TEXT,           -- JSON array
    detected_themes TEXT            -- JSON array: ["debugging", "perseverance"]
);

-- User config
CREATE TABLE config (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

### Context Detection Flow

```
Terminal Startup
    ↓
1. Time of Day Detection (local)
    → morning, afternoon, evening, night
    ↓
2. Weather Check (Open-Meteo, cached 60min)
    → clear, cloudy, rainy, stormy, snowy
    ↓
3. Git Activity Analysis (optional)
    → Read last 10 commits via gh CLI
    → Analyze: session length, diff sizes, commit frequency
    → Map to themes: ["debugging", "progress", "learning"]
    ↓
4. Tag Extraction
    → Combine all context signals into tags
    → Example: ["morning", "stormy", "adversity", "debugging"]
    ↓
5. Hybrid Search
    → Step A: Filter quotes by matching tags (reduce search space)
    → Step B: Semantic search within filtered set using embeddings
    → Return best match
    ↓
6. ASCII Art Selection
    → Pick art matching quote's primary theme
    → Select size variant based on terminal width
    ↓
7. Display with pyfiglet header
```

### Project Structure

```
stoic-terminal/
├── pyproject.toml              # UV tool config
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
│
├── src/
│   └── stoic_terminal/
│       ├── __init__.py
│       ├── cli.py              # Entry point, arg parsing
│       ├── database.py         # SQLite abstraction layer
│       ├── embeddings.py       # Semantic search with sentence-transformers
│       ├── context.py          # Time/weather/git detection
│       ├── git_analyzer.py     # Git session analysis
│       ├── ascii_art.py        # Art loading and rendering
│       ├── display.py          # Main display orchestration
│       └── config.py           # Config management
│
├── data/
│   ├── quotes_v1.db            # 250 quotes (bundled)
│   ├── git_sessions.db         # User's git history
│   └── ascii_art/
│       ├── metadata.yaml
│       ├── meditation/
│       ├── adversity/
│       ├── exploration/
│       ├── nature/
│       ├── wisdom/
│       └── general/
│
├── scripts/
│   ├── collect_quotes.py       # Quotable API scraper
│   ├── build_embeddings.py     # Pre-compute embeddings
│   ├── curate_ascii.py         # Helper for art curation
│   └── validate_db.py          # Quality checks
│
└── tests/
    ├── test_database.py
    ├── test_embeddings.py
    ├── test_context.py
    └── test_ascii_art.py
```

## 7-Day Implementation Plan

### Day 1: Database & Quote Collection
**Goal**: Collect 250 quotes and set up database

**Tasks:**
1. Create SQLite schema
2. Write database abstraction layer (CRUD operations)
3. Build Quotable API scraper script
   - Fetch 100 quotes from Quotable API
   - Parse and insert into DB with tags
4. Manually add 50 quotes from Project Gutenberg
   - Marcus Aurelius Meditations (25 quotes)
   - Sun Tzu Art of War (25 quotes)
5. Add 100 more from Abirate dataset (quality-focused)
6. Validate: 250 quotes total, all with proper attribution
7. Tag each quote with 3-5 relevant themes

**Deliverable**: `quotes_v1.db` with 250 high-quality, properly attributed quotes

### Day 2: ASCII Art Foundation
**Goal**: Curate and organize ASCII art collection

**Tasks:**
1. Clone asweigart's database
2. Install pyfiglet: `pip install pyfiglet`
3. Manually curate from asciiart.eu:
   - Meditation: 5 pieces
   - Adversity: 5 pieces
   - Exploration: 5 pieces
   - Nature: 5 pieces
   - Wisdom: 5 pieces
   - General: 5 pieces (decorative borders)
4. Save as plain text files: `ascii_art/meditation/buddha_80.txt`, etc.
5. Create metadata.yaml with theme tags
6. Write ASCIIArtLoader class with LRU caching
7. Test rendering in 80-column terminal

**Deliverable**: 30 curated ASCII art pieces with loader system

### Day 3: Semantic Search Setup
**Goal**: Implement embedding generation and search

**Tasks:**
1. Install sentence-transformers: `pip install sentence-transformers`
2. Download all-MiniLM-L6-v2 model
3. Write embedding generation script:
   - Load all 250 quotes
   - Generate embeddings
   - Store in quotes table as BLOB
4. Implement search functions:
   - `search_by_tags(tags)` - Tag-based filtering
   - `search_semantic(query_text, candidate_pool)` - Cosine similarity
   - `get_contextual_quote(context_data)` - Hybrid approach
5. Add embedding column to database schema
6. Test search quality with sample queries
7. Benchmark performance (<5ms search time)

**Deliverable**: Working semantic search with pre-computed embeddings

### Day 4: Context Detection
**Goal**: Build time/weather/git context awareness

**Tasks:**
1. Time detection: Simple datetime.now() mapping
2. Weather integration:
   - Install requests, geopy
   - Implement Open-Meteo API calls
   - Add 60-minute caching
   - Write city → coordinates geocoding
3. Git analyzer (optional feature):
   - Test `gh` CLI availability
   - Parse last 10 commits
   - Extract: commit count, diff sizes, time gaps
   - Map to themes: debugging, progress, learning
4. Context aggregator:
   - Combine time/weather/git into tag list
   - Weight by priority (git > weather > time)
5. Test end-to-end: context → tags → quote selection

**Deliverable**: Context detection system producing relevant tags

### Day 5: Display & CLI
**Goal**: Complete user interface and display logic

**Tasks:**
1. Build display orchestrator:
   - Load quote based on context
   - Select matching ASCII art
   - Detect terminal width
   - Render art + quote + attribution
2. Use pyfiglet for author headers
3. Implement responsive display:
   - 120+ columns: Full experience
   - 80-119: Standard display
   - 40-79: Simplified
   - <40: Text-only
4. Create CLI with argparse:
   - `stoic-terminal` (context-aware)
   - `stoic-terminal --random` (pure random)
   - `stoic-terminal --theme meditation` (force theme)
   - `stoic-terminal --config-location "Atlanta, GA"`
5. Add color support with colorama (optional)

**Deliverable**: Working CLI with beautiful terminal output

### Day 6: Configuration & Polish
**Goal**: User configuration and edge cases

**Tasks:**
1. Config system:
   - Create config.toml in user's config dir
   - Store: location (coords/city), weather enabled, git enabled
   - `stoic-terminal --init` setup wizard
2. Shell integration:
   - Write .bashrc/.zshrc snippets
   - Test auto-run on terminal startup
3. Error handling:
   - Network failures for weather
   - Missing git CLI
   - Database corruption
   - Missing ASCII art files
4. Logging system (for debugging)
5. Add `--version`, `--help`, `--status` commands
6. Write comprehensive README:
   - Installation instructions
   - Configuration guide
   - Troubleshooting section
   - Screenshot/demo

**Deliverable**: Production-ready CLI with error handling

### Day 7: Testing & Documentation
**Goal**: Ensure reliability and prepare for release

**Tasks:**
1. Unit tests:
   - Database functions
   - Embedding search
   - ASCII art loading
   - Context detection
2. Integration tests:
   - Full flow: startup → context → quote → display
   - Test with network failures
   - Test with missing config
   - Test in different terminal sizes
3. Performance validation:
   - Startup time <500ms
   - Display render <100ms
   - Memory usage <150MB
4. Documentation:
   - API documentation (docstrings)
   - Architecture overview
   - Contribution guidelines
   - Code of conduct
5. Prepare for UV tool distribution:
   - Write pyproject.toml
   - Test `uv tool install .`
   - Verify it works on clean system

**Deliverable**: Tested, documented, ready-to-ship v1.0

## Success Metrics for v1.0

- ✅ 250 high-quality quotes with proper attribution
- ✅ 30 ASCII art pieces across 6 themes
- ✅ <500ms startup time
- ✅ <100ms quote display time
- ✅ Zero API keys required for basic functionality
- ✅ Works on Linux, macOS, and Windows
- ✅ Beautiful terminal display
- ✅ Context-aware quote selection
- ✅ Graceful degradation (works without weather/git)

## Future Enhancements (Post v1.0)

### Week 2: Expand to 500 Quotes
- Quotable API: +150 quotes
- Project Gutenberg: +100 quotes (Epictetus, Lao Tzu, Confucius)
- Community submissions: +50 quotes

### Week 3-4: Advanced Features
- Binary embeddings for 100x storage reduction (nomic-embed)
- More ASCII art size variants (40/60/120 column versions)
- Seasonal themes (winter wisdom, summer exploration)
- Quote of the day (deterministic based on date)

### Month 2: Community & Scale
- Publish to HuggingFace: Dataset + Model Card
- GitHub PR workflow for quote contributions
- Automated validation pipeline
- Scale to 1,000 quotes
- Add `--upgrade` command for larger databases

### Month 3: Intelligence
- Learn user preferences (track thumbs up/down)
- Better git session analysis (sentiment from commit messages)
- Multi-language support (Spanish, French philosophical quotes)
- Voice narration option (TTS integration)

## Technical Dependencies

### Python Packages (pyproject.toml)
```toml
[project]
dependencies = [
    "sentence-transformers>=2.2.0",
    "requests>=2.28.0",
    "pyyaml>=6.0",
    "pyfiglet>=0.8.0",
    "numpy>=1.21.0",
]
```

### Optional Dependencies
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "mypy>=0.990",
]
```

### External Dependencies (User Installs)
- Git (for version control features)
- GitHub CLI (`gh`) - optional, for git analysis

## Distribution Strategy

### Phase 1: UV Tool (v1.0)
```bash
# Install from source
git clone https://github.com/username/stoic-terminal.git
cd stoic-terminal
uv tool install .

# Or from PyPI (after publishing)
uv tool install stoic-terminal
```

### Phase 2: Package Managers
- PyPI: `pip install stoic-terminal`
- Homebrew: `brew install stoic-terminal`
- AUR (Arch Linux): Community package

### Phase 3: Binaries
- PyInstaller for standalone executables
- Windows: `.exe` installer
- macOS: `.app` bundle
- Linux: AppImage

## Risk Mitigation

### Technical Risks
1. **Embedding model too slow**: Switch to potion-base-8M (8MB, 500x faster)
2. **ASCII art looks bad**: Fallback to simple borders, still ship
3. **Weather API rate limits**: Open-Meteo gives 10K/day, far more than needed
4. **Database corruption**: Write validation and recovery tools
5. **Terminal compatibility**: Extensive testing, graceful degradation

### Legal Risks
1. **Quote attribution issues**: Stick to public domain for v1.0 (zero risk)
2. **ASCII art copyright**: Respect artist credits, only use permissive sources
3. **Weather API terms**: Open-Meteo explicitly allows open-source use

### Project Risks
1. **Scope creep**: Stick to 7-day plan for v1.0, defer enhancements
2. **Perfectionism**: Ship with 250 quotes, don't wait for 10K
3. **Over-engineering**: Use simple solutions (SQLite, plain text files)

## Conclusion

This project is ready to build. All research questions are answered, technical decisions are made, and the implementation path is clear. The 7-day plan is aggressive but achievable for a focused week of development.

**Start tomorrow morning with Day 1: Database & Quote Collection.**

The beauty of this design is that each component can be developed and tested independently, then integrated. If any piece takes longer than expected, the others aren't blocked.

Ship fast, iterate based on user feedback, and build the community. This has the potential to become a widely-used terminal tool that brings wisdom to developers every day.

---

*"The journey of a thousand quotes begins with a single database." — Ancient Terminal Wisdom*
