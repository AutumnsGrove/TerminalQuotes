# Project Instructions - Claude Code

> **Note**: This is the main orchestrator file. For detailed guides, see `ClaudeUsage/README.md`

---

## Project Purpose
Stoic Terminal is a context-aware terminal tool that displays philosophical quotes with ASCII art based on time of day, weather conditions, and git activity analysis. It provides developers with relevant wisdom during their terminal sessions.

## Tech Stack
- **Language**: Python 3.10+
- **Framework**: CLI tool built with argparse
- **Key Libraries**:
  - sentence-transformers (semantic search with all-MiniLM-L6-v2)
  - requests (API calls)
  - pyfiglet (ASCII text rendering)
  - pyyaml (configuration management)
  - sqlite3 (database, built-in)
  - numpy (embedding operations)
- **Package Manager**: UV (modern Python package manager)
- **Database**: SQLite (embedded, no external dependencies)

## Architecture Notes
- **Hybrid search system**: Tag-based filtering + semantic search with embeddings
- **Context detection**: Combines time, weather (Open-Meteo API), and optional git analysis
- **Pre-computed embeddings**: All quote embeddings generated at setup time and stored as BLOBs
- **Responsive display**: ASCII art selection adapts to terminal width (40/60/80/120 column variants)
- **Zero API keys required**: Open-Meteo weather API requires no authentication
- **Performance targets**: <500ms startup, <100ms quote display

---

## Essential Instructions (Always Follow)

### Core Behavior
- Do what has been asked; nothing more, nothing less
- NEVER create files unless absolutely necessary for achieving your goal
- ALWAYS prefer editing existing files to creating new ones
- NEVER proactively create documentation files (*.md) or README files unless explicitly requested

### Naming Conventions
- **Directories**: Use CamelCase (e.g., `VideoProcessor`, `AudioTools`, `DataAnalysis`)
- **Date-based paths**: Use skewer-case with YYYY-MM-DD (e.g., `logs-2025-01-15`, `backup-2025-12-31`)
- **No spaces or underscores** in directory names (except date-based paths)

### TODO Management
- **Always check `TODOS.md` first** when starting a task or session
- **Update immediately** when tasks are completed, added, or changed
- Keep the list current and manageable

### Git Workflow Essentials
**After completing major changes, you MUST:**
1. Check git status: `git status`
2. Review recent commits for style: `git log --oneline -5`
3. Stage changes: `git add .`
4. Commit with proper message format (see below)

**Commit Message Format:**
```
[Action] [Brief description]

- [Specific change 1 with technical detail]
- [Specific change 2 with technical detail]
- [Additional implementation details]

🤖 Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>
```

**Action Verbs**: Add, Update, Fix, Refactor, Remove, Enhance

---

## When to Read Specific Guides

**Read the full guide in `ClaudeUsage/` when you encounter these situations:**

### Secrets & API Keys
- **When managing API keys or secrets** → Read `ClaudeUsage/secrets_management.md`
- **Before implementing secrets loading** → Read `ClaudeUsage/secrets_management.md`
- **Note**: This project requires NO API keys for basic functionality

### Package Management
- **When using UV package manager** → Read `ClaudeUsage/uv_usage.md`
- **Before creating pyproject.toml** → Read `ClaudeUsage/uv_usage.md`
- **When managing Python dependencies** → Read `ClaudeUsage/uv_usage.md`

### Version Control
- **Before making a git commit** → Read `ClaudeUsage/git_commit_guide.md`
- **When initializing a new repo** → Read `ClaudeUsage/git_commit_guide.md`
- **For git workflow details** → Read `ClaudeUsage/git_commit_guide.md`

### Search & Research
- **When searching across 20+ files** → Read `ClaudeUsage/house_agents.md`
- **When finding patterns in codebase** → Read `ClaudeUsage/house_agents.md`
- **When locating TODOs/FIXMEs** → Read `ClaudeUsage/house_agents.md`

### Testing
- **Before writing tests** → Read `ClaudeUsage/testing_strategies.md`
- **When implementing test coverage** → Read `ClaudeUsage/testing_strategies.md`
- **For test organization** → Read `ClaudeUsage/testing_strategies.md`


### Code Quality
- **When refactoring code** → Read `ClaudeUsage/code_style_guide.md`
- **Before major code changes** → Read `ClaudeUsage/code_style_guide.md`
- **For style guidelines** → Read `ClaudeUsage/code_style_guide.md`

### Project Setup
- **When starting a new project** → Read `ClaudeUsage/project_setup.md`
- **For directory structure** → Read `ClaudeUsage/project_setup.md`
- **Setting up CI/CD** → Read `ClaudeUsage/project_setup.md`

---

## Quick Reference

### Security Basics
- Store API keys in `secrets.json` (NEVER commit)
- Add `secrets.json` to `.gitignore` immediately
- Provide `secrets_template.json` for setup
- Use environment variables as fallbacks
- **This project**: No API keys needed for core functionality (Open-Meteo is keyless)


### House Agents Quick Trigger
**When searching 20+ files**, use house-research for:
- Finding patterns across codebase
- Searching TODO/FIXME comments
- Locating API endpoints or functions
- Documentation searches

---

## Code Style Guidelines

### Function & Variable Naming
- Use meaningful, descriptive names
- Keep functions small and focused on single responsibilities
- Add docstrings to functions and classes

### Error Handling
- Use try/except blocks gracefully
- Provide helpful error messages
- Never let errors fail silently
- Implement graceful degradation (work without weather/git if unavailable)

### File Organization
- Group related functionality into modules
- Use consistent import ordering:
  1. Standard library
  2. Third-party packages
  3. Local imports
- Keep configuration separate from logic

---

## Stoic Terminal Specific Guidelines

### Database Management
- All quotes stored in SQLite with pre-computed embeddings
- Use BLOB type for 384-dimensional embeddings
- Always include proper attribution (author, source, year, translator)
- Tag every quote with 3-5 relevant theme tags

### ASCII Art Standards
- Organize by theme: meditation, adversity, exploration, nature, wisdom, general
- Create size variants: 40/60/80/100/120 columns
- Store as plain text files with metadata.yaml for indexing
- Use LRU caching for performance (<1ms load time)

### Performance Requirements
- **Startup time**: <500ms (includes model loading, DB connection, context detection)
- **Quote display**: <100ms (search + art loading + rendering)
- **Memory usage**: <150MB (model: 90MB, art: 20MB, DB: 20MB)

### Context Detection Priority
1. **Git activity** (highest priority if available)
2. **Weather conditions** (medium priority, cached 60 minutes)
3. **Time of day** (lowest priority, always available)

---

## Communication Style
- Be concise but thorough
- Explain reasoning for significant decisions
- Ask for clarification when requirements are ambiguous
- Proactively suggest improvements when appropriate

---

## Complete Guide Index
For all detailed guides, workflows, and examples, see:
**`ClaudeUsage/README.md`** - Master index of all documentation

---

*Last updated: 2025-10-20*
*Model: Claude Sonnet 4.5*
