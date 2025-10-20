# Quote Extraction Task - Project Gutenberg Sources

## Objective
Extract 82 high-quality philosophical quotes from downloaded Project Gutenberg texts and add them to the existing quotes database (`quotes_v1.db`).

## Current State
- **Existing quotes**: 168 (from Quotable API)
- **Target**: 250 total quotes
- **Needed**: 82 additional quotes
- **Database location**: `quotes_v1.db` (already exists with schema)

## Source Files Available
All files are in `data/gutenberg_sources/`:
1. **meditations.txt** - Marcus Aurelius "Meditations" (415KB, George Long translation, 1862)
2. **art_of_war.txt** - Sun Tzu "The Art of War" (334KB, Lionel Giles translation, 1910)
3. **seneca_letters.txt** - Seneca "Letters from a Stoic" (466KB, Richard Mott Gummere translation)

## Quote Extraction Guidelines

### Quality Criteria
A good quote must be:
1. **Self-contained** - Makes sense without surrounding context
2. **Actionable or insightful** - Provides wisdom, perspective, or guidance
3. **Terminal-appropriate** - Not too long (prefer <400 characters)
4. **Verified** - Exact text from the source file, no paraphrasing

### What to Extract
- Standalone aphorisms and maxims
- Complete sentences that convey a single idea
- Powerful metaphors or comparisons
- Practical wisdom about life, adversity, virtue, strategy

### What to Avoid
- Long paragraphs (>400 chars)
- Quotes requiring heavy context to understand
- Transitional sentences ("As I mentioned before...")
- Questions without answers (unless rhetorically powerful)
- Religious or outdated medical advice

## Extraction Process

### Step 1: Read Source Files Systematically
For each text file, read sections looking for standalone quotes. Use the Read tool to examine the content methodically.

**Marcus Aurelius Meditations:**
- Focus on Books 1-12 (skip Introduction and Appendix)
- Look for short, powerful statements about stoic philosophy
- Target: ~35 quotes

**Sun Tzu Art of War:**
- Focus on the 13 chapters of strategic wisdom
- Look for timeless principles applicable beyond warfare
- Target: ~25 quotes

**Seneca Letters:**
- Focus on the letter content (skip translator notes)
- Look for practical stoic advice
- Target: ~22 quotes

### Step 2: Use Exact Text from Source
**CRITICAL**: Copy the exact text as it appears in the file. Do NOT:
- Paraphrase or modernize language
- Combine multiple sentences unless they appear together
- Add your own interpretations
- Use quotes from your training data

### Step 3: Record Context Metadata
For each quote, capture:
- **Exact text** (as it appears in the source file)
- **Book/Chapter/Letter number** (e.g., "Book 4", "Chapter III: Attack by Stratagem", "Letter LXVII")
- **Line number range** from the source file (for verification)
- **Suggested tags** (3-5 relevant themes)

### Step 4: Add to Database Using Existing Code

Use the `QuoteDatabase` class from `day1_starter_code.py`:

```python
from day1_starter_code import QuoteDatabase

db = QuoteDatabase("quotes_v1.db")

# Example for Marcus Aurelius
db.add_quote(
    text="<exact text from file>",
    author="Marcus Aurelius",
    source="Meditations",
    source_context="Book 4, Section 12",  # Based on where you found it
    source_year=-180,  # Approximate composition date
    translator="George Long",
    tradition="stoic",
    tags=["stoicism", "control", "wisdom", "inner_strength"],
    copyright_status="public_domain"
)

# Example for Sun Tzu
db.add_quote(
    text="<exact text from file>",
    author="Sun Tzu",
    source="The Art of War",
    source_context="Chapter III: Attack by Stratagem",
    source_year=-500,  # Approximate composition date
    translator="Lionel Giles",
    tradition="military_strategy",
    tags=["strategy", "victory", "wisdom", "planning"],
    copyright_status="public_domain"
)

# Example for Seneca
db.add_quote(
    text="<exact text from file>",
    author="Seneca",
    source="Letters from a Stoic",
    source_context="Letter LXVII",
    source_year=65,  # Approximate composition date
    translator="Richard Mott Gummere",
    tradition="stoic",
    tags=["stoicism", "adversity", "strength", "wisdom"],
    copyright_status="public_domain"
)

db.close()
```

## Recommended Tag Vocabulary

Use consistent tags across quotes:

**Stoic Themes:**
- stoicism, virtue, wisdom, control, acceptance, inner_strength, mindfulness, tranquility, duty, excellence

**Emotional/Mental:**
- courage, fear, anger, gratitude, contentment, resilience, patience, humility, self_discipline

**Life Concepts:**
- mortality, time, change, adversity, growth, simplicity, purpose, character, integrity

**Strategic (Sun Tzu):**
- strategy, tactics, warfare, planning, deception, timing, victory, preparation, leadership

**Relational:**
- friendship, relationships, community, solitude, teaching, learning

## Output Format

Create a Python script called `add_gutenberg_quotes.py` that:
1. Imports the QuoteDatabase class
2. Opens the existing quotes_v1.db
3. Adds all 82 quotes with proper attribution
4. Prints progress (e.g., "Added quote 1/82: '<first 50 chars>...'")
5. Prints final count verification
6. Shows 5 random samples from the new additions

## Verification Steps

After adding all quotes:
1. Verify database has exactly 250 quotes: `db.count_quotes()`
2. Test random quote retrieval: `db.get_random_quote()`
3. Test tag-based search: `db.search_by_tags(['stoicism'])`
4. Manually spot-check 5 quotes by opening the source file and finding the exact text

## Example Quote Extraction Workflow

1. Read `data/gutenberg_sources/meditations.txt` starting from "FIRST BOOK"
2. Scan for standalone wisdom (e.g., short paragraphs that are complete thoughts)
3. For each candidate quote:
   - Copy exact text
   - Note the Book number and section
   - Record line numbers for later verification
   - Draft 3-5 tags
4. Create `add_gutenberg_quotes.py` with all quotes as structured data
5. Run the script to populate database
6. Verify final count

## Success Criteria

- ✅ Database contains exactly 250 quotes
- ✅ All 82 new quotes are verbatim from source files
- ✅ Every quote has proper attribution (author, source, source_context, translator, year)
- ✅ Every quote has 3-5 relevant tags
- ✅ All quotes are marked as copyright_status="public_domain"
- ✅ Script runs without errors
- ✅ Manual verification of 5 random quotes against source files confirms accuracy

## Time Estimate
- Reading and extracting quotes: 45-60 minutes
- Creating Python script: 15 minutes
- Running and verifying: 5 minutes
- **Total**: ~75 minutes

## Important Reminders

1. **NEVER hallucinate quotes** - Only use text that exists in the source files
2. **EXACT TEXT ONLY** - Copy-paste from the files, don't paraphrase
3. **RECORD LINE NUMBERS** - So quotes can be verified later
4. **USE CONSISTENT TAGS** - Refer to the tag vocabulary above
5. **PUBLIC DOMAIN ONLY** - All three sources are confirmed public domain

## After Completion

Once the script successfully adds 82 quotes and verification passes:
1. Update `TODOS.md` to mark Day 1 complete
2. Update `add_manual_quotes.py` → `add_gutenberg_quotes.py`
3. Commit to git with message: "Add 82 verified Project Gutenberg quotes to database"
4. Report back to the main session with quote count and sample quotes

---

**Start by reading the first 200 lines of each source file to understand structure, then systematically extract quotes following the guidelines above.**
