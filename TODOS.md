# Stoic Terminal - Development TODOs

## 🎯 Current Phase: Day 1 - Database & Quote Collection

### High Priority (Day 1)
- [x] Run day1_starter_code.py to initialize database
- [x] Verify quotes_v1.db created successfully
- [x] Collect 200+ quotes from Quotable API
- [x] Manually add 82 quotes from Project Gutenberg
  - [x] Marcus Aurelius Meditations (35 quotes)
  - [x] Sun Tzu Art of War (25 quotes)
  - [x] Seneca On Benefits (22 quotes)
- [x] Tag all quotes with 3-5 relevant theme tags
- [x] Verify 250 total quotes with proper attribution
- [x] Test database queries (random, by tag, by author)

### Medium Priority (Day 2)
- [ ] Clone asweigart ASCII art database
- [ ] Install pyfiglet: `uv add pyfiglet`
- [ ] Curate ASCII art from asciiart.eu:
  - [ ] Meditation: 5 pieces
  - [ ] Adversity: 5 pieces
  - [ ] Exploration: 5 pieces
  - [ ] Nature: 5 pieces
  - [ ] Wisdom: 5 pieces
  - [ ] General: 5 pieces (decorative borders)
- [ ] Create metadata.yaml for ASCII art indexing
- [ ] Implement ASCIIArtLoader class with LRU caching
- [ ] Test rendering in 80-column terminal

### Medium Priority (Day 3)
- [ ] Install sentence-transformers: `uv add sentence-transformers`
- [ ] Download all-MiniLM-L6-v2 model
- [ ] Write embedding generation script
- [ ] Generate embeddings for all 250 quotes
- [ ] Store embeddings in database as BLOB
- [ ] Implement search functions:
  - [ ] search_by_tags(tags) - Tag-based filtering
  - [ ] search_semantic(query_text) - Cosine similarity
  - [ ] get_contextual_quote(context_data) - Hybrid approach
- [ ] Benchmark search performance (<5ms target)

### Medium Priority (Day 4)
- [ ] Implement time of day detection
- [ ] Integrate Open-Meteo weather API
  - [ ] Add requests library (already in dependencies)
  - [ ] Implement geocoding (city → coordinates)
  - [ ] Add 60-minute response caching
- [ ] Build Git analyzer (optional feature):
  - [ ] Check for `gh` CLI availability
  - [ ] Parse last 10 commits
  - [ ] Extract commit metadata (count, sizes, time gaps)
  - [ ] Map activity to themes (debugging, progress, learning)
- [ ] Create context aggregator
- [ ] Test end-to-end: context → tags → quote selection

### Low Priority (Day 5)
- [ ] Build display orchestrator
  - [ ] Load quote based on context
  - [ ] Select matching ASCII art
  - [ ] Detect terminal width
  - [ ] Render art + quote + attribution
- [ ] Implement pyfiglet author headers
- [ ] Create responsive display for different terminal widths:
  - [ ] 120+ columns: Full experience
  - [ ] 80-119: Standard display
  - [ ] 40-79: Simplified
  - [ ] <40: Text-only
- [ ] Build CLI with argparse:
  - [ ] `stoic-terminal` (context-aware)
  - [ ] `stoic-terminal --random`
  - [ ] `stoic-terminal --theme meditation`
  - [ ] `stoic-terminal --config-location "City, State"`

### Low Priority (Day 6)
- [ ] Create config system
  - [ ] Create config.toml in user's config dir
  - [ ] Store location, weather enabled, git enabled
  - [ ] Implement `stoic-terminal --init` setup wizard
- [ ] Write shell integration snippets (.bashrc/.zshrc)
- [ ] Add comprehensive error handling:
  - [ ] Network failures for weather
  - [ ] Missing git CLI
  - [ ] Database corruption
  - [ ] Missing ASCII art files
- [ ] Implement logging system
- [ ] Add CLI commands: `--version`, `--help`, `--status`

### Low Priority (Day 7)
- [ ] Write unit tests:
  - [ ] test_database.py
  - [ ] test_embeddings.py
  - [ ] test_ascii_art.py
  - [ ] test_context.py
- [ ] Write integration tests:
  - [ ] Full flow: startup → context → quote → display
  - [ ] Test with network failures
  - [ ] Test with missing config
  - [ ] Test in different terminal sizes
- [ ] Performance validation:
  - [ ] Startup time <500ms
  - [ ] Display render <100ms
  - [ ] Memory usage <150MB
- [ ] Prepare for UV tool distribution:
  - [ ] Test `uv tool install .`
  - [ ] Verify clean system installation

## 🚀 Future Enhancements (Post v1.0)

### Week 2: Expand Quote Database
- [ ] Add 150 quotes from Quotable API
- [ ] Add 100 quotes from Project Gutenberg (Epictetus, Lao Tzu, Confucius)
- [ ] Accept 50 community submissions
- [ ] Reach 500 total quotes

### Week 3-4: Advanced Features
- [ ] Binary embeddings for storage reduction
- [ ] More ASCII art size variants (40/60/120 columns)
- [ ] Seasonal themes (winter wisdom, summer exploration)
- [ ] Quote of the day (deterministic based on date)

### Month 2: Community & Scale
- [ ] Publish dataset to HuggingFace
- [ ] Create GitHub PR workflow for contributions
- [ ] Automated validation pipeline
- [ ] Scale to 1,000 quotes
- [ ] Add `--upgrade` command for larger databases

### Month 3: Intelligence
- [ ] Learn user preferences (thumbs up/down tracking)
- [ ] Better git sentiment analysis
- [ ] Multi-language support (Spanish, French)
- [ ] Voice narration option (TTS integration)

## 📋 Blocked / Waiting

- None currently

## ✅ Completed

- [x] Clone BaseProject template
- [x] Customize CLAUDE.md with Stoic Terminal details
- [x] Customize README.md
- [x] Initialize UV project with dependencies
- [x] Create project directory structure (src/, tests/, data/)
- [x] Create secrets_template.json
- [x] Setup pyproject.toml with all dependencies
- [x] Day 1 Complete: Database with 250 verified quotes

---

**Last Updated:** 2025-10-20
**Current Sprint:** Day 1 - Database & Quote Collection
**Next Milestone:** 250 quotes collected and verified
