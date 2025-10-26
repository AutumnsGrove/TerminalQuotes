# ASCII Art Curation Processing Guide

## Overview
This guide provides instructions for Claude Code to process the curation feedback from the ASCII art viewer and update the project accordingly.

---

## Prerequisites

Before running this guide, you must:
1. ✅ Open the ASCII art viewer at `http://localhost:8000/tools/ascii_art_viewer.html`
2. ✅ Review all 143 ASCII art pieces
3. ✅ Mark pieces as ✓ Good or ✗ Bad
4. ✅ Click "Export Curated List" button to download `ascii_art_curation.json`
5. ✅ Place the JSON file in the project root: `/Users/autumn/Documents/Projects/TerminalQuotes/ascii_art_curation.json`

---

## Instructions for Claude Code

When the user provides the curation results, follow these steps:

### Step 1: Load and Validate Curation Data

Read the exported curation file:
```bash
# File location: ascii_art_curation.json
```

The JSON structure will be:
```json
{
  "timestamp": "2025-10-26T14:30:00.000Z",
  "total": 143,
  "curated": {
    "meditation/buddha_seated_large_60.txt": "good",
    "animals/cat_sleeping_60.txt": "bad",
    ...
  },
  "summary": {
    "good": 75,
    "bad": 50,
    "unmarked": 18
  }
}
```

**Validation checks:**
- Verify the file exists and is valid JSON
- Check that `summary.good + summary.bad + summary.unmarked = total`
- Report the curation summary to the user

### Step 2: Create Filtered Metadata

Generate a new `metadata.yaml` containing ONLY the pieces marked as "good":

**Process:**
1. Load `data/ascii_art/metadata.yaml`
2. For each theme, filter out pieces whose file paths are marked as "bad" in the curation
3. Keep pieces marked as "good" or "unmarked" (unmarked = user wants to keep for now)
4. Backup the original: `data/ascii_art/metadata.yaml.backup`
5. Write the filtered metadata to `data/ascii_art/metadata.yaml`

**Important:**
- Preserve the exact YAML structure and formatting
- Keep all variant information for retained pieces
- Maintain tags, descriptions, and dimensions
- Update the header comment with new piece count

### Step 3: Archive Bad ASCII Art Files

Move "bad" ASCII art files to an archive directory instead of deleting them:

**Process:**
1. Create archive directory: `data/ascii_art_archive/`
2. Recreate the theme subdirectory structure in the archive
3. For each file marked as "bad":
   - Move from `data/ascii_art/{theme}/{file}.txt`
   - To `data/ascii_art_archive/{theme}/{file}.txt`
4. Create an archive manifest: `data/ascii_art_archive/ARCHIVED.md`

**Archive Manifest Format:**
```markdown
# Archived ASCII Art

These pieces were reviewed and marked as "bad" during curation on {date}.

## Archive Summary
- Total archived: {count}
- Archived by theme:
  - meditation: {count}
  - adversity: {count}
  ...

## Archived Files
### {Theme}
- `{filename}` - {description} ({width}x{height})
...
```

### Step 4: Generate Curation Summary Report

Create a report at `CURATION_SUMMARY.md` with:

**Report Contents:**
```markdown
# ASCII Art Curation Results

**Date:** {timestamp}
**Curator:** {user or "Autumn"}

## Summary Statistics

- **Total Reviewed:** 143 pieces
- **Kept (Good):** {good_count} pieces ({percentage}%)
- **Archived (Bad):** {bad_count} pieces ({percentage}%)
- **Unmarked (Kept):** {unmarked_count} pieces ({percentage}%)

## Final Collection

**Total Pieces:** {good + unmarked}

### By Theme:
- **Meditation:** {count} pieces (was {original_count})
- **Adversity:** {count} pieces (was {original_count})
- **Exploration:** {count} pieces (was {original_count})
- **Nature:** {count} pieces (was {original_count})
- **Wisdom:** {count} pieces (was {original_count})
- **General:** {count} pieces (was {original_count})
- **Animals:** {count} pieces (was {original_count})
- **Urban:** {count} pieces (was {original_count})
- **Whimsical:** {count} pieces (was {original_count})
- **Cosmic:** {count} pieces (was {original_count})

## Top Kept Pieces by Theme

### Meditation
- {piece_name} ({width}x{height}) - {description}
...

## Quality Improvements

{List any notable improvements from curation, e.g.:}
- Removed overly complex pieces that don't render well
- Kept high-quality, clear ASCII art
- Maintained variety across all themes
- Preserved multiple size options for key pieces

## Next Steps

- [ ] Review final collection
- [ ] Create size variants for responsive display (40/60/80 columns)
- [ ] Implement ASCIIArtLoader class
- [ ] Test rendering in different terminal widths
```

### Step 5: Update File System

**Verify operations:**
1. Count remaining .txt files in `data/ascii_art/`: should equal (good + unmarked)
2. Count archived .txt files in `data/ascii_art_archive/`: should equal bad
3. Validate metadata.yaml references only existing files
4. Check for orphaned files (files not in metadata)

**Cleanup:**
```bash
# Find any orphaned files in data/ascii_art/
find data/ascii_art/ -name "*.txt" -type f

# Compare against metadata.yaml file paths
# Report any files that exist but aren't in metadata
```

### Step 6: Commit Changes

Create a git commit documenting the curation:

**Commit Message Template:**
```
Curate ASCII art collection based on visual review

- Reviewed all 143 pieces using HTML curation viewer
- Kept {good + unmarked} high-quality pieces
- Archived {bad} pieces to data/ascii_art_archive/
- Updated metadata.yaml to reflect curated collection
- Generated curation summary report

Theme changes:
- Meditation: {original} → {new} pieces
- Adversity: {original} → {new} pieces
- Exploration: {original} → {new} pieces
- Nature: {original} → {new} pieces
- Wisdom: {original} → {new} pieces
- General: {original} → {new} pieces
- Animals: {original} → {new} pieces
- Urban: {original} → {new} pieces
- Whimsical: {original} → {new} pieces
- Cosmic: {original} → {new} pieces

Quality criteria applied:
- Clear, readable ASCII art
- Appropriate size for terminal display
- Good visual representation of theme
- Technical rendering quality

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Files to commit:**
```
data/ascii_art/metadata.yaml
data/ascii_art/metadata.yaml.backup
data/ascii_art_archive/
CURATION_SUMMARY.md
ascii_art_curation.json
```

---

## User Prompt Template

When you're ready to process the curation, provide this prompt to Claude Code:

```
I've completed the ASCII art curation using the viewer. The exported curation file is at:
ascii_art_curation.json

Please process the curation results following the guide at:
tools/CURATION_PROCESSING_GUIDE.md

Specifically:
1. Load and validate the curation data
2. Create filtered metadata.yaml (keep only "good" and "unmarked" pieces)
3. Archive "bad" files to data/ascii_art_archive/
4. Generate a curation summary report
5. Verify the file system matches the metadata
6. Commit all changes with an appropriate message

Show me the curation summary statistics before committing.
```

---

## Troubleshooting

### Issue: JSON file not found
**Solution:** Make sure you clicked "Export Curated List" in the viewer and the file downloaded to the project root.

### Issue: Metadata YAML parsing errors
**Solution:** Validate the YAML with: `uv run python -c "import yaml; yaml.safe_load(open('data/ascii_art/metadata.yaml'))"`

### Issue: File paths don't match
**Solution:** The curation JSON uses paths like `theme/file.txt`, metadata uses `variants[].file` with the same format. They should match exactly.

### Issue: Unmarked pieces
**Decision:** By default, keep unmarked pieces. The user can always archive them later. Only archive explicitly marked "bad" pieces.

---

## Validation Script

After processing, run this validation:

```python
import yaml
import json
from pathlib import Path

# Load curation data
with open('ascii_art_curation.json') as f:
    curation = json.load(f)

# Load metadata
with open('data/ascii_art/metadata.yaml') as f:
    metadata = yaml.safe_load(f)

# Count pieces in metadata
metadata_files = set()
for theme, pieces in metadata.items():
    for piece in pieces:
        for variant in piece['variants']:
            metadata_files.add(variant['file'])

# Count actual files
actual_files = set()
for txt_file in Path('data/ascii_art').rglob('*.txt'):
    rel_path = txt_file.relative_to('data/ascii_art')
    actual_files.add(str(rel_path))

# Count archived files
archived_files = set()
if Path('data/ascii_art_archive').exists():
    for txt_file in Path('data/ascii_art_archive').rglob('*.txt'):
        rel_path = txt_file.relative_to('data/ascii_art_archive')
        archived_files.add(str(rel_path))

# Validate
good_count = sum(1 for v in curation['curated'].values() if v == 'good')
bad_count = sum(1 for v in curation['curated'].values() if v == 'bad')
unmarked_count = curation['total'] - good_count - bad_count

print(f"✓ Curation Summary:")
print(f"  Good: {good_count}")
print(f"  Bad: {bad_count}")
print(f"  Unmarked: {unmarked_count}")
print(f"  Total: {curation['total']}")
print()
print(f"✓ File Counts:")
print(f"  Metadata references: {len(metadata_files)}")
print(f"  Actual files: {len(actual_files)}")
print(f"  Archived files: {len(archived_files)}")
print()
print(f"✓ Expected vs Actual:")
print(f"  Should keep: {good_count + unmarked_count}")
print(f"  Should archive: {bad_count}")
print(f"  Actual kept: {len(actual_files)}")
print(f"  Actual archived: {len(archived_files)}")
print()

# Check for mismatches
if metadata_files == actual_files:
    print("✓ All metadata files exist")
else:
    orphaned = actual_files - metadata_files
    missing = metadata_files - actual_files
    if orphaned:
        print(f"⚠ Orphaned files (exist but not in metadata): {orphaned}")
    if missing:
        print(f"⚠ Missing files (in metadata but don't exist): {missing}")

if len(archived_files) == bad_count:
    print("✓ Archive count matches 'bad' count")
else:
    print(f"⚠ Archive mismatch: {len(archived_files)} archived vs {bad_count} marked bad")
```

Save as: `tools/validate_curation.py`
Run with: `uv run python tools/validate_curation.py`

---

## Success Criteria

After processing, you should have:

- ✅ `metadata.yaml` contains only kept pieces
- ✅ `metadata.yaml.backup` preserves original
- ✅ `data/ascii_art/` contains only kept .txt files
- ✅ `data/ascii_art_archive/` contains all bad .txt files
- ✅ `CURATION_SUMMARY.md` documents the results
- ✅ `ascii_art_curation.json` preserved for reference
- ✅ Validation script passes all checks
- ✅ Git commit created documenting changes

**The collection is now curated and ready for Phase 4: Implement ASCIIArtLoader class!**
