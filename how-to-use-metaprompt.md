# How to Use This Metaprompt with Claude

## Quick Start

1. **Start a new Claude conversation**

2. **Upload all these files:**
   - `claude-metaprompt-implementation.md` (the instruction file)
   - `stoic-terminal-spec.md` (original spec)
   - `stoic-terminal-implementation-plan.md` (detailed roadmap)
   - `stoic-terminal-quick-reference.md` (quick lookup)
   - `day1_starter_code.py` (example code)
   - `philosophical_quote_DB_research.md` (quote sources)
   - `weather_apis_research.md` (weather API info)
   - `ascii_art_research.md` (ASCII art strategies)
   - `lightweight_embedding_models_search_results.md` (embedding models)

3. **Send this exact message:**

```
I'm building a terminal tool called "Stoic Terminal" that displays philosophical quotes with ASCII art. I've uploaded comprehensive research and specifications.

Please read the metaprompt file (claude-metaprompt-implementation.md) and begin implementing the project. Start by creating the complete project structure and initial components.

Use the computer to create all files and folders.
```

## Expected Flow

Claude will:
1. ✅ Read all the research documents
2. ✅ Create the complete folder structure
3. ✅ Generate pyproject.toml and README.md
4. ✅ Implement database.py
5. ✅ Build the quote collection script
6. ✅ Continue systematically through all components

## If Claude Needs Guidance

If Claude asks questions or seems stuck, you can say:

**"Focus on getting database.py working first. Use the Day 1 starter code as reference."**

**"Prioritize the 7-day plan from the implementation guide. We want a working v1.0 fast."**

**"If unsure about a design choice, pick the simpler option that ships faster."**

## Files to Upload

### Required (Core Documentation)
1. `claude-metaprompt-implementation.md` ⭐ (THIS IS THE KEY FILE)
2. `stoic-terminal-implementation-plan.md` ⭐ (Detailed roadmap)
3. `stoic-terminal-quick-reference.md` ⭐ (Quick decisions)

### Recommended (Research Context)
4. `philosophical_quote_DB_research.md` (Quote sources)
5. `weather_apis_research.md` (Weather API details)
6. `ascii_art_research.md` (ASCII art strategies)
7. `lightweight_embedding_models_search_results.md` (Embedding info)

### Optional (Reference)
8. `stoic-terminal-spec.md` (Original specification)
9. `day1_starter_code.py` (Example database code)

## What You'll Get

After the conversation, you'll have:
- Complete project structure
- All Python modules implemented
- Working database layer
- Quote collection scripts
- ASCII art system
- Semantic search
- Context detection
- CLI interface
- Tests
- Documentation

## Tips for Success

1. **Let Claude work through the components systematically** - Don't rush ahead
2. **Test each component** as it's built before moving on
3. **Ask for clarifications** on design decisions you're unsure about
4. **Request additional features** once core is working
5. **Use follow-ups** like:
   - "Now implement the ASCII art loader"
   - "Add error handling for network failures"
   - "Write tests for the database layer"

## Alternative: Iterative Approach

If you prefer smaller chunks, you can ask Claude to implement one day at a time:

**Day 1 Only:**
```
Please implement Day 1 only: database.py and the quote collection script. 
Create the files, test them, and show me how to run them.
```

**Then Day 2:**
```
Good! Now let's do Day 2: ASCII art system. Create the loader, metadata 
structure, and add 5 example art pieces.
```

This gives you more control over the pace and lets you review each stage.

## Troubleshooting

**"Claude seems confused about the project structure"**
→ Re-upload the implementation plan and say: "Follow the exact folder structure from stoic-terminal-implementation-plan.md"

**"Claude is making different design decisions than the research"**
→ Say: "Please use the decisions already made in the research documents. For example, use Open-Meteo for weather (not OpenWeatherMap)."

**"Claude wants to use different libraries"**
→ Say: "Stick to the tech stack: sentence-transformers for embeddings, requests for HTTP, pyfiglet for text art, SQLite for database."

**"The code isn't working"**
→ Say: "Please test this code and fix any errors. Show me the complete, working version."

## Expected Timeline

With focused sessions:
- **Session 1** (1-2 hours): Project structure + database + quote collection
- **Session 2** (1-2 hours): ASCII art + semantic search
- **Session 3** (1-2 hours): Context detection + display + CLI
- **Session 4** (1 hour): Testing + polish + documentation

Total: 4-6 hours of Claude sessions to complete implementation

## Success Indicators

You'll know it's working when:
1. ✅ `uv tool install .` succeeds
2. ✅ Running `stoic-terminal` displays a quote with ASCII art
3. ✅ Database contains 250+ quotes
4. ✅ Weather integration works (if configured)
5. ✅ Different terminal sizes are handled gracefully
6. ✅ Startup is fast (<500ms)

## Ready to Start?

Upload the files and send the initial message. Claude will take it from there! 🚀

---

**Pro tip:** Keep the research documents handy in case you need to reference specific details during implementation.
