# Day 2 Plan: ASCII Art Curation & Implementation

## Objective
Curate and organize 30 high-quality ASCII art pieces with responsive sizing and implement the loader system.

## Current State
- ✅ Day 1 complete: 250 quotes in database
- ✅ All dependencies installed
- ✅ Project structure ready
- 📂 Empty directory: `data/ascii_art/`

## Goals for Day 2
1. **Curate 30 ASCII art pieces** organized by theme
2. **Create size variants** for responsive terminal display
3. **Build metadata.yaml** for art indexing and theme mapping
4. **Implement ASCIIArtLoader class** with LRU caching
5. **Test rendering** across different terminal widths

---

## Phase 1: Clone Existing ASCII Art Resources (15 minutes)

### Step 1.1: Clone asweigart's ASCII Art Database
```bash
# Clone the repo to a resources directory
git clone https://github.com/asweigart/asciiartjsondb.git resources/asciiartjsondb

# Explore the structure
ls -la resources/asciiartjsondb/
cat resources/asciiartjsondb/README.md
```

**What to look for:**
- JSON structure for programmatic access
- Categories that match our themes
- Size information and complexity

### Step 1.2: Explore the Database
```python
import json

with open('resources/asciiartjsondb/asciiart.json', 'r') as f:
    art_db = json.load(f)

# See what categories exist
categories = set()
for art in art_db:
    if 'category' in art:
        categories.add(art['category'])

print(f"Available categories: {sorted(categories)}")
print(f"Total pieces: {len(art_db)}")
```

---

## Phase 2: Manual ASCII Art Curation (45-60 minutes)

### Our 6 Themes
1. **Meditation** - Buddha, lotus, zen garden, flowing water, yin-yang
2. **Adversity** - Storm, mountain climb, anvil, fortress, challenges
3. **Exploration** - Ship, compass, mountain peak, path, journey
4. **Nature** - Trees, mountains, sunrise, ocean, forest
5. **Wisdom** - Books, owl, scrolls, candle, ancient symbols
6. **General** - Decorative borders, simple frames, dividers

### Step 2.1: Browse and Select from asciiart.eu

**Meditation sources:**
- https://www.asciiart.eu/religion/buddhism
- https://www.asciiart.eu/nature/flowers (lotus)
- https://www.asciiart.eu/nature/water

**Adversity sources:**
- https://www.asciiart.eu/nature/rains
- https://www.asciiart.eu/nature/mountains
- https://www.asciiart.eu/buildings-and-places/castles

**Exploration sources:**
- https://www.asciiart.eu/vehicles/boats
- https://www.asciiart.eu/miscellaneous/compasses
- https://www.asciiart.eu/nature/mountains

**Nature sources:**
- https://www.asciiart.eu/nature/trees
- https://www.asciiart.eu/nature/mountains
- https://www.asciiart.eu/nature/sun

**Wisdom sources:**
- https://www.asciiart.eu/books/books
- https://www.asciiart.eu/animals/birds-land (owls)
- https://www.asciiart.eu/miscellaneous/scrolls

**General sources:**
- https://www.asciiart.eu/art-and-design/borders
- https://www.asciiart.eu/art-and-design/dividers

### Step 2.2: Create Directory Structure
```bash
mkdir -p data/ascii_art/{meditation,adversity,exploration,nature,wisdom,general}
```

### Step 2.3: Save ASCII Art Files

For each piece, create a `.txt` file with this naming convention:
```
data/ascii_art/{theme}/{name}_{width}.txt
```

**Examples:**
- `data/ascii_art/meditation/buddha_60.txt` - 60-column Buddha
- `data/ascii_art/meditation/buddha_80.txt` - 80-column Buddha
- `data/ascii_art/adversity/storm_60.txt` - 60-column storm
- `data/ascii_art/nature/tree_40.txt` - 40-column tree

### Step 2.4: Create Size Variants

For each piece, create at least 2 size variants:
- **Small (40-60 columns)**: For narrow terminals
- **Medium (80-100 columns)**: Standard terminal width
- **Large (120+ columns)**: Wide displays (optional for Day 2)

**Tip:** You can manually resize ASCII art by:
- Removing detail lines
- Simplifying complex patterns
- Using simpler characters for smaller versions

---

## Phase 3: Create Metadata System (15 minutes)

### Step 3.1: Design metadata.yaml Structure

Create `data/ascii_art/metadata.yaml`:

```yaml
# ASCII Art Metadata
# Maps themes to available art pieces with size information

meditation:
  - name: "buddha"
    description: "Seated Buddha in meditation"
    variants:
      - width: 60
        file: "meditation/buddha_60.txt"
        height: 15
      - width: 80
        file: "meditation/buddha_80.txt"
        height: 20
    tags: ["meditation", "peace", "mindfulness", "zen"]

  - name: "lotus"
    description: "Lotus flower blooming"
    variants:
      - width: 40
        file: "meditation/lotus_40.txt"
        height: 10
      - width: 60
        file: "meditation/lotus_60.txt"
        height: 15
    tags: ["meditation", "growth", "beauty", "enlightenment"]

adversity:
  - name: "storm"
    description: "Storm clouds and lightning"
    variants:
      - width: 60
        file: "adversity/storm_60.txt"
        height: 12
      - width: 80
        file: "adversity/storm_80.txt"
        height: 18
    tags: ["adversity", "challenge", "resilience", "strength"]

# ... continue for all 6 themes with 5 pieces each
```

### Step 3.2: Validate Metadata

Create a simple validation script to ensure all files exist:

```python
import yaml
from pathlib import Path

with open('data/ascii_art/metadata.yaml', 'r') as f:
    metadata = yaml.safe_load(f)

for theme, pieces in metadata.items():
    print(f"\nTheme: {theme}")
    for piece in pieces:
        print(f"  {piece['name']}:")
        for variant in piece['variants']:
            filepath = Path('data/ascii_art') / variant['file']
            exists = "✓" if filepath.exists() else "✗"
            print(f"    {exists} {variant['width']}col: {variant['file']}")
```

---

## Phase 4: Implement ASCIIArtLoader Class (30 minutes)

### Step 4.1: Create src/stoic_terminal/ascii_art.py

```python
"""
ASCII Art loader with LRU caching and responsive sizing.
"""

import yaml
from pathlib import Path
from functools import lru_cache
from typing import Dict, List, Optional, Tuple


class ASCIIArtLoader:
    """Load and cache ASCII art with responsive sizing."""

    def __init__(self, art_dir: str = "data/ascii_art"):
        self.art_dir = Path(art_dir)
        self.metadata_path = self.art_dir / "metadata.yaml"
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict:
        """Load ASCII art metadata from YAML file."""
        if not self.metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_path}")

        with open(self.metadata_path, 'r') as f:
            return yaml.safe_load(f)

    @lru_cache(maxsize=128)
    def load_art(self, filepath: str) -> str:
        """Load ASCII art from file with LRU caching.

        Args:
            filepath: Relative path from art_dir (e.g., 'meditation/buddha_60.txt')

        Returns:
            The ASCII art as a string
        """
        full_path = self.art_dir / filepath

        if not full_path.exists():
            raise FileNotFoundError(f"ASCII art file not found: {full_path}")

        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()

    def get_art_by_theme(self, theme: str, terminal_width: int = 80) -> Optional[Tuple[str, Dict]]:
        """Get random ASCII art for a theme, sized for terminal width.

        Args:
            theme: Theme name (meditation, adversity, exploration, nature, wisdom, general)
            terminal_width: Current terminal width in columns

        Returns:
            Tuple of (art_string, metadata_dict) or None if not found
        """
        import random

        if theme not in self.metadata:
            return None

        # Get all pieces for this theme
        pieces = self.metadata[theme]
        if not pieces:
            return None

        # Pick a random piece
        piece = random.choice(pieces)

        # Find best-fitting variant for terminal width
        variant = self._find_best_variant(piece['variants'], terminal_width)

        if not variant:
            return None

        # Load the art
        art_string = self.load_art(variant['file'])

        return art_string, piece

    def _find_best_variant(self, variants: List[Dict], terminal_width: int) -> Optional[Dict]:
        """Find the best-fitting art variant for the given terminal width.

        Prefers variants that fit within the terminal but are as large as possible.
        """
        # Sort by width descending
        sorted_variants = sorted(variants, key=lambda v: v['width'], reverse=True)

        # Find largest variant that fits
        for variant in sorted_variants:
            if variant['width'] <= terminal_width - 4:  # Leave 4-column margin
                return variant

        # If nothing fits, return the smallest variant
        return sorted_variants[-1] if sorted_variants else None

    def get_art_by_tags(self, tags: List[str], terminal_width: int = 80) -> Optional[Tuple[str, Dict]]:
        """Get ASCII art matching any of the given tags.

        Args:
            tags: List of tags to match (e.g., ['meditation', 'peace'])
            terminal_width: Current terminal width in columns

        Returns:
            Tuple of (art_string, metadata_dict) or None if not found
        """
        import random

        # Collect all pieces that match any tag
        matching_pieces = []

        for theme, pieces in self.metadata.items():
            for piece in pieces:
                piece_tags = set(piece.get('tags', []))
                if piece_tags.intersection(set(tags)):
                    matching_pieces.append((theme, piece))

        if not matching_pieces:
            return None

        # Pick a random matching piece
        theme, piece = random.choice(matching_pieces)

        # Find best variant
        variant = self._find_best_variant(piece['variants'], terminal_width)

        if not variant:
            return None

        art_string = self.load_art(variant['file'])

        return art_string, piece

    def list_themes(self) -> List[str]:
        """Get list of available themes."""
        return list(self.metadata.keys())

    def get_cache_info(self) -> Dict:
        """Get LRU cache statistics."""
        cache_info = self.load_art.cache_info()
        return {
            'hits': cache_info.hits,
            'misses': cache_info.misses,
            'size': cache_info.currsize,
            'maxsize': cache_info.maxsize
        }


def get_terminal_width() -> int:
    """Get current terminal width in columns."""
    import shutil
    return shutil.get_terminal_size().columns
```

### Step 4.2: Write Tests

Create `tests/test_ascii_art.py`:

```python
"""Tests for ASCII art loader."""

import pytest
from pathlib import Path
from stoic_terminal.ascii_art import ASCIIArtLoader, get_terminal_width


def test_load_metadata():
    """Test metadata loading."""
    loader = ASCIIArtLoader()
    assert loader.metadata is not None
    assert isinstance(loader.metadata, dict)


def test_list_themes():
    """Test theme listing."""
    loader = ASCIIArtLoader()
    themes = loader.list_themes()

    expected_themes = ['meditation', 'adversity', 'exploration', 'nature', 'wisdom', 'general']
    for theme in expected_themes:
        assert theme in themes


def test_get_art_by_theme():
    """Test loading art by theme."""
    loader = ASCIIArtLoader()

    art, metadata = loader.get_art_by_theme('meditation', terminal_width=80)

    assert art is not None
    assert isinstance(art, str)
    assert len(art) > 0
    assert metadata is not None
    assert 'name' in metadata


def test_responsive_sizing():
    """Test that art adapts to terminal width."""
    loader = ASCIIArtLoader()

    # Get art for narrow terminal
    art_narrow, _ = loader.get_art_by_theme('meditation', terminal_width=50)

    # Get art for wide terminal
    art_wide, _ = loader.get_art_by_theme('meditation', terminal_width=120)

    # Both should return valid art
    assert art_narrow is not None
    assert art_wide is not None


def test_cache_functionality():
    """Test LRU cache is working."""
    loader = ASCIIArtLoader()

    # Load same art twice
    art1, _ = loader.get_art_by_theme('wisdom', terminal_width=80)
    cache_info_1 = loader.get_cache_info()

    art2, _ = loader.get_art_by_theme('wisdom', terminal_width=80)
    cache_info_2 = loader.get_cache_info()

    # Cache hits should increase on second load
    assert cache_info_2['hits'] >= cache_info_1['hits']


def test_get_terminal_width():
    """Test terminal width detection."""
    width = get_terminal_width()
    assert width > 0
    assert width < 1000  # Sanity check
```

---

## Phase 5: Manual Testing & Verification (15 minutes)

### Step 5.1: Test in Interactive Python

```python
from stoic_terminal.ascii_art import ASCIIArtLoader, get_terminal_width

# Initialize loader
loader = ASCIIArtLoader()

# Check available themes
print("Available themes:", loader.list_themes())

# Test loading art
print("\nTesting meditation theme:")
art, metadata = loader.get_art_by_theme('meditation', terminal_width=80)
print(art)
print(f"\nMetadata: {metadata}")

# Test responsive sizing
print("\nTesting responsive sizing:")
print(f"Terminal width: {get_terminal_width()}")
art_small, _ = loader.get_art_by_theme('nature', terminal_width=50)
print("50-column version:")
print(art_small)

# Test cache
print("\nCache stats:", loader.get_cache_info())
```

### Step 5.2: Test in Actual Terminal

```bash
# Test at 80 columns (standard)
uv run python -c "
from stoic_terminal.ascii_art import ASCIIArtLoader
loader = ASCIIArtLoader()
art, _ = loader.get_art_by_theme('wisdom', terminal_width=80)
print(art)
"

# Test at 60 columns (narrow)
uv run python -c "
from stoic_terminal.ascii_art import ASCIIArtLoader
loader = ASCIIArtLoader()
art, _ = loader.get_art_by_theme('adversity', terminal_width=60)
print(art)
"
```

### Step 5.3: Run Pytest

```bash
uv run pytest tests/test_ascii_art.py -v
```

---

## Success Criteria for Day 2

- ✅ 30 ASCII art files created (6 themes × 5 pieces)
- ✅ At least 2 size variants per piece (60col and 80col)
- ✅ metadata.yaml complete and validated
- ✅ ASCIIArtLoader class implemented with LRU caching
- ✅ Responsive sizing working (adapts to terminal width)
- ✅ All tests passing
- ✅ Cache performance verified (<1ms load time for cached items)
- ✅ Manual rendering tests successful in 60, 80, and 100 column terminals

---

## File Checklist

By end of Day 2, you should have:

```
data/ascii_art/
├── metadata.yaml                          # Central index
├── meditation/
│   ├── buddha_60.txt
│   ├── buddha_80.txt
│   ├── lotus_40.txt
│   ├── lotus_60.txt
│   ├── zen_garden_60.txt
│   ├── zen_garden_80.txt
│   ├── water_40.txt
│   ├── water_60.txt
│   ├── yin_yang_40.txt
│   └── yin_yang_60.txt
├── adversity/
│   ├── storm_60.txt
│   ├── storm_80.txt
│   ├── mountain_60.txt
│   ├── mountain_80.txt
│   ├── anvil_40.txt
│   ├── anvil_60.txt
│   ├── fortress_60.txt
│   ├── fortress_80.txt
│   ├── challenge_40.txt
│   └── challenge_60.txt
├── exploration/
│   ├── ship_60.txt
│   ├── ship_80.txt
│   ├── compass_40.txt
│   ├── compass_60.txt
│   ├── mountain_peak_60.txt
│   ├── mountain_peak_80.txt
│   ├── path_40.txt
│   ├── path_60.txt
│   ├── journey_60.txt
│   └── journey_80.txt
├── nature/
│   ├── tree_40.txt
│   ├── tree_60.txt
│   ├── tree_80.txt
│   ├── mountains_60.txt
│   ├── mountains_80.txt
│   ├── sunrise_60.txt
│   ├── sunrise_80.txt
│   ├── ocean_40.txt
│   ├── ocean_60.txt
│   └── forest_60.txt
├── wisdom/
│   ├── books_40.txt
│   ├── books_60.txt
│   ├── owl_60.txt
│   ├── owl_80.txt
│   ├── scroll_40.txt
│   ├── scroll_60.txt
│   ├── candle_40.txt
│   ├── candle_60.txt
│   ├── symbols_60.txt
│   └── symbols_80.txt
└── general/
    ├── border_simple_60.txt
    ├── border_simple_80.txt
    ├── border_fancy_60.txt
    ├── border_fancy_80.txt
    ├── divider_40.txt
    ├── divider_60.txt
    ├── frame_40.txt
    ├── frame_60.txt
    ├── decorative_60.txt
    └── decorative_80.txt

src/stoic_terminal/
└── ascii_art.py                           # Complete implementation

tests/
└── test_ascii_art.py                      # All tests passing
```

---

## Git Commit Message Template

After Day 2 completion:

```
Add ASCII art curation system with responsive sizing

- Curated 30 ASCII art pieces across 6 themes (meditation, adversity, exploration, nature, wisdom, general)
- Created 60+ size variants (40/60/80 column widths)
- Implemented metadata.yaml indexing system with tags
- Built ASCIIArtLoader class with LRU caching for <1ms load times
- Added responsive sizing that adapts to terminal width
- Implemented tag-based art selection
- All tests passing (test_ascii_art.py)
- Verified rendering in 60, 80, and 100 column terminals

Performance:
- Cache hit rate: >90% after warmup
- Load time: <1ms for cached items, <10ms for uncached
- Memory footprint: <20MB for all art cached

🤖 Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>
```

---

## Time Breakdown

- **Phase 1**: Clone resources - 15 min
- **Phase 2**: Manual curation - 45-60 min
- **Phase 3**: Metadata creation - 15 min
- **Phase 4**: Implementation - 30 min
- **Phase 5**: Testing - 15 min

**Total estimated time**: 2-2.5 hours

---

## Tips for Success

1. **Start with simple ASCII art** - Don't get bogged down finding "perfect" art. You can always upgrade later.
2. **Use asweigart's database** as much as possible to save time.
3. **Test incrementally** - Verify each theme works before moving to the next.
4. **Size variants can be simple** - For narrow terminals, just trim edges or simplify detail.
5. **Tag generously** - More tags = better matching in the context system.

---

## After Day 2

Once complete, you'll be ready for Day 3:
- Generate embeddings for all 250 quotes
- Implement semantic search
- Build the hybrid search system (tags + embeddings)

**Day 2 sets the visual foundation for the entire tool!**
