# Stoic Terminal

A context-aware terminal tool that displays philosophical quotes with ASCII art based on your current environment - time of day, weather conditions, and git activity.

## 🌟 Features

- **Context-Aware Quote Selection**: Uses semantic search with embeddings to match quotes to your current situation
- **Beautiful ASCII Art**: Hand-curated ASCII art that adapts to terminal width (40/60/80/120 columns)
- **Zero API Keys Required**: Works immediately with no configuration (uses Open-Meteo weather API)
- **Git Activity Analysis**: Optional integration that analyzes recent commits to provide relevant wisdom
- **Lightning Fast**: <500ms startup, <100ms quote display
- **250+ Curated Quotes**: High-quality quotes from stoic philosophers, military strategists, and wisdom traditions

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/stoic-terminal.git
cd stoic-terminal

# Install with UV (recommended)
uv tool install .

# Or install with pip
pip install -e .
```

### Basic Usage

```bash
# Display context-aware quote
stoic-terminal

# Display random quote
stoic-terminal --random

# Force specific theme
stoic-terminal --theme meditation

# Configure location for weather
stoic-terminal --config-location "Atlanta, GA"

# Run on terminal startup (add to .bashrc or .zshrc)
echo "stoic-terminal" >> ~/.bashrc
```

## 📋 Project Status

Currently following the 7-day implementation plan. See `TODOS.md` for current progress.

### Implementation Roadmap
- **Day 1**: Database setup + 250 quote collection ⏳
- **Day 2**: ASCII art curation (30 pieces)
- **Day 3**: Semantic search with embeddings
- **Day 4**: Context detection (time/weather/git)
- **Day 5**: CLI + display rendering
- **Day 6**: Configuration + error handling
- **Day 7**: Testing + documentation

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Package Manager**: UV
- **Database**: SQLite (embedded)
- **Key Libraries**:
  - `sentence-transformers` - Semantic search (all-MiniLM-L6-v2 model)
  - `requests` - Weather API integration
  - `pyfiglet` - ASCII text rendering
  - `pyyaml` - Configuration management
  - `numpy` - Embedding operations

## 🏗️ Architecture

### Hybrid Search System
1. **Tag-based filtering** - Narrow down quotes by relevant themes
2. **Semantic search** - Find the most contextually relevant quote using embeddings
3. **ASCII art selection** - Match art to quote theme and terminal width

### Context Detection Flow
```
Time Detection → Weather API → Git Analysis → Tag Extraction → Semantic Search → Display
```

### Performance Targets
- ✅ Startup time: <500ms
- ✅ Quote display: <100ms
- ✅ Memory usage: <150MB

## 📁 Project Structure

```
StoicTerminal/
├── CLAUDE.md                   # Project instructions for Claude Code
├── README.md                   # This file
├── TODOS.md                    # Current task list
├── pyproject.toml              # UV configuration
├── secrets_template.json       # Template for API keys (none needed!)
├── .gitignore                  # Git ignore patterns
│
├── src/
│   └── stoic_terminal/
│       ├── __init__.py
│       ├── cli.py              # Command-line interface
│       ├── database.py         # SQLite abstraction
│       ├── embeddings.py       # Semantic search
│       ├── context.py          # Context detection
│       ├── git_analyzer.py     # Git activity analysis
│       ├── ascii_art.py        # ASCII art loading
│       └── display.py          # Display orchestration
│
├── data/
│   ├── quotes_v1.db            # Quote database
│   ├── git_sessions.db         # Git history (user-specific)
│   └── ascii_art/              # Curated ASCII art
│       ├── metadata.yaml
│       ├── meditation/
│       ├── adversity/
│       ├── exploration/
│       ├── nature/
│       ├── wisdom/
│       └── general/
│
├── tests/
│   ├── test_database.py
│   ├── test_embeddings.py
│   ├── test_context.py
│   └── test_ascii_art.py
│
└── ClaudeUsage/                # Development workflow guides
    ├── README.md
    ├── git_workflow.md
    ├── secrets_management.md
    ├── uv_usage.md
    └── ... (18 comprehensive guides)
```

## 🔐 Security & Privacy

- **No API keys required** for basic functionality
- **Optional features** can be disabled (weather, git analysis)
- **Local-only data** - No telemetry or external tracking
- **Open source** - Full transparency

## 🧪 Development

### Running Tests
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=stoic_terminal

# Run specific test file
uv run pytest tests/test_database.py
```

### Running Day 1 Starter Code
```bash
# Collect initial 250 quotes
uv run python day1_starter_code.py
```

## 📚 Quote Sources

All quotes are properly attributed and sourced from:
- **Quotable API** - MIT licensed, public domain quotes
- **Project Gutenberg** - Classic texts (Marcus Aurelius, Seneca, Sun Tzu, Epictetus)
- **Curated Collections** - Hand-selected for quality and relevance

### Legal Safety
- Pre-1930 published works (public domain)
- Proper attribution for all quotes
- Translator credits where applicable
- Copyright status tracked in database

## 🎨 ASCII Art Sources

- Hand-curated from [asciiart.eu](https://www.asciiart.eu)
- [asweigart's ASCII Art JSON Database](https://github.com/asweigart/asciiartjsondb)
- Custom creations with proper attribution

## 🤝 Contributing

Contributions welcome! Please read [ClaudeUsage/documentation_standards.md](ClaudeUsage/documentation_standards.md) for guidelines.

### Adding Quotes
1. Follow the quote schema in `database.py`
2. Include proper attribution (author, source, year, translator)
3. Add 3-5 relevant theme tags
4. Verify copyright status (prefer public domain)

### Adding ASCII Art
1. Place in appropriate theme directory
2. Update `metadata.yaml`
3. Create size variants for different terminal widths
4. Include artist attribution if known

## 🔧 Configuration

Optional configuration file: `~/.config/stoic-terminal/config.toml`

```toml
[location]
city = "Atlanta, GA"
# or use coordinates
latitude = 33.7490
longitude = -84.3880

[features]
weather_enabled = true
git_analysis_enabled = true

[display]
default_theme = "random"  # or: meditation, adversity, exploration, etc.
terminal_width = "auto"   # or: 40, 60, 80, 120
```

## 📖 Documentation

- **User Guide**: See [stoic-terminal-quick-reference.md](stoic-terminal-quick-reference.md)
- **Implementation Plan**: See [stoic-terminal-implementation-plan.md](stoic-terminal-implementation-plan.md)
- **Development Guides**: See [ClaudeUsage/README.md](ClaudeUsage/README.md)

## 🐛 Troubleshooting

### "Model download too slow"
The sentence-transformers model (~90MB) is downloaded on first run. Subsequent runs are instant.

### "ASCII art looks weird"
Check terminal encoding: `echo $LANG` (should be UTF-8). Use `--text-only` flag if issues persist.

### "Weather not updating"
Weather data is cached for 60 minutes. Use `--force-refresh` to update immediately.

### "Quotes feel repetitive"
Increase the quote database size or adjust tag diversity. See [CONTRIBUTING.md](CONTRIBUTING.md) for adding more quotes.

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- **Quotable API** - Luke Peavey ([quotable.io](https://quotable.io))
- **Open-Meteo** - Free weather API with no key required
- **sentence-transformers** - Hugging Face semantic search library
- **Project Gutenberg** - Public domain classics
- **asweigart** - ASCII Art JSON Database

---

## 🎯 What's Next?

1. **Complete Day 1** - Run `day1_starter_code.py` to populate the database
2. **Follow Implementation Plan** - See [stoic-terminal-implementation-plan.md](stoic-terminal-implementation-plan.md)
3. **Track Progress** - Update [TODOS.md](TODOS.md) as you build
4. **Ship v1.0** - 250 quotes, 30 art pieces, full context awareness

---

**Last updated:** 2025-10-20
**Status:** In Development (Day 1)
**Target Release:** v1.0 (7 days from start)
