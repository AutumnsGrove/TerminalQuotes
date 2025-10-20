# Stoic Terminal - Quick Reference

## TL;DR - Ready to Build!

All research is complete. Clear path to ship v1.0 with 250 quotes in 7 days.

## Key Decisions Matrix

| Component | Winner | Why | Link |
|-----------|--------|-----|------|
| **Quotes** | Quotable API + Project Gutenberg | Legal safety (public domain), high quality, 2,500+ available | [Research](../uploads/philosophical_quote_DB_research.md) |
| **Weather** | Open-Meteo | NO API key, 10K/day free, zero friction | [Research](../uploads/weather_apis_research.md) |
| **ASCII Art** | Pre-curated (asciiart.eu + asweigart) | Highest quality, <1ms load, 30-50 pieces for v1 | [Research](../uploads/ascii_art_research.md) |
| **Embeddings** | all-MiniLM-L6-v2 | 90MB, <100ms load, 56-58 MTEB, 1.5B+ downloads | [Research](../uploads/lightweight_embedding_models_search_results.md) |

## Installation Commands (Day 0)

```bash
# Python dependencies
pip install sentence-transformers requests pyyaml pyfiglet

# ASCII art resources
git clone https://github.com/asweigart/asciiartjsondb.git resources/

# Optional: GitHub CLI for git analysis
# macOS: brew install gh
# Linux: snap install gh
```

## Quote Collection (Day 1)

### Quotable API
```python
import requests

def fetch_quotes(tag, limit=100):
    url = f"https://api.quotable.io/quotes?tags={tag}&limit={limit}"
    return requests.get(url).json()['results']

# Get 100 stoicism quotes
stoic_quotes = fetch_quotes('wisdom', 100)
```

### Project Gutenberg Sources
- Marcus Aurelius: https://www.gutenberg.org/ebooks/2680
- Seneca Letters: https://www.gutenberg.org/ebooks/3794
- Sun Tzu: https://www.gutenberg.org/ebooks/132
- Epictetus: https://www.gutenberg.org/ebooks/45109

## Weather Setup (Day 4)

```python
import requests

def get_weather(lat, lon):
    """No API key needed!"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    
    weather_code = data['current_weather']['weathercode']
    return map_weather_code(weather_code)  # clear, cloudy, rainy, stormy, snowy

def map_weather_code(code):
    if code == 0: return 'clear'
    elif code in [1, 2, 3]: return 'cloudy'
    elif code in [51, 53, 55, 61, 63, 65]: return 'rainy'
    elif code in [95, 96, 99]: return 'stormy'
    elif code in [71, 73, 75, 77, 85, 86]: return 'snowy'
    return 'clear'
```

## ASCII Art Curation (Day 2)

### Sources to Browse
1. **Meditation**: https://www.asciiart.eu/religion/buddhism
2. **Nature**: https://www.asciiart.eu/nature/mountains
3. **Adversity**: https://www.asciiart.eu/nature/rains
4. **Wisdom**: https://www.asciiart.eu/books/books
5. **Exploration**: https://www.asciiart.eu/vehicles/boats

### File Structure
```
ascii_art/
├── metadata.yaml
├── meditation/
│   ├── buddha_80.txt
│   ├── lotus_80.txt
│   └── zen_garden_80.txt
├── adversity/
│   ├── storm_80.txt
│   └── mountain_climb_80.txt
└── ...
```

## Semantic Search (Day 3)

```python
from sentence_transformers import SentenceTransformer, util
import torch

# Load model (one-time, ~100ms)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for all quotes (one-time)
quotes = ["Quote 1...", "Quote 2...", ...]
quote_embeddings = model.encode(quotes, convert_to_tensor=True)

# Runtime search (<5ms)
def search_quotes(context_description):
    query_embedding = model.encode(context_description, convert_to_tensor=True)
    similarities = util.cos_sim(query_embedding, quote_embeddings)[0]
    best_idx = similarities.argmax().item()
    return quotes[best_idx]

# Example
quote = search_quotes("dealing with adversity during difficult debugging")
```

## Database Schema

```sql
CREATE TABLE quotes (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    author TEXT NOT NULL,
    source TEXT,
    source_year INTEGER,
    tradition TEXT,
    tags TEXT,                  -- JSON: ["stoic", "adversity", "wisdom"]
    embedding BLOB,             -- 1536 bytes (384 floats × 4 bytes)
    copyright_status TEXT
);

CREATE INDEX idx_tradition ON quotes(tradition);
CREATE INDEX idx_tags ON quotes(tags);
```

## Context → Quote Flow

```
1. Detect Context
   - Time: morning/afternoon/evening/night
   - Weather: clear/cloudy/rainy/stormy/snowy
   - Git: debugging/progress/learning (optional)

2. Extract Tags
   - morning + stormy + debugging → ["adversity", "perseverance", "morning"]

3. Filter by Tags
   - SELECT * FROM quotes WHERE tags LIKE '%adversity%'

4. Semantic Search
   - Generate embedding for "dealing with adversity in morning during storm"
   - Find most similar quote in filtered set

5. Display
   - Load ASCII art matching quote's theme
   - Render with pyfiglet header
```

## 7-Day Checklist

- [ ] **Day 1**: Database + 250 quotes collected
- [ ] **Day 2**: 30 ASCII art pieces curated
- [ ] **Day 3**: Embeddings generated, search working
- [ ] **Day 4**: Context detection (time/weather/git)
- [ ] **Day 5**: CLI + display working
- [ ] **Day 6**: Config system + error handling
- [ ] **Day 7**: Tests + documentation + release

## Performance Targets

- Startup time: <500ms ✓ (Model load: 100ms, DB: 50ms, Art: <1ms)
- Quote display: <100ms ✓ (Search: 5ms, Art load: 1ms, Render: 10ms)
- Memory usage: <150MB ✓ (Model: 90MB, Art: 20MB, DB: 20MB)

## Testing Commands

```bash
# Test model loading speed
python -c "from sentence_transformers import SentenceTransformer; import time; start = time.time(); model = SentenceTransformer('all-MiniLM-L6-v2'); print(f'Load time: {time.time()-start:.3f}s')"

# Test weather API
curl "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"

# Test terminal width detection
python -c "import shutil; print(shutil.get_terminal_size())"

# Test pyfiglet
python -c "from pyfiglet import Figlet; f = Figlet(font='slant'); print(f.renderText('Marcus Aurelius'))"
```

## Common Issues & Solutions

### "Model download too slow"
```python
# Pre-download in setup script
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
# Saves to ~/.cache/torch/sentence_transformers/
```

### "ASCII art looks weird"
- Check terminal encoding: `echo $LANG` (should be UTF-8)
- Test with simple ASCII first: `cat ascii_art/simple_border.txt`
- Fallback to text-only mode if issues persist

### "Weather not updating"
- Check cache timestamp (should be <60 minutes old)
- Test API directly: `curl "https://api.open-meteo.com/v1/forecast?latitude=40.7&longitude=-74.0&current_weather=true"`
- Verify internet connection

### "Quotes feel repetitive"
- Increase tag diversity (5-10 tags per quote)
- Add more quotes to database (500+ reduces repetition)
- Implement "recently shown" tracking to avoid repeats

## Next Steps

1. **Read the full implementation plan**: `/tmp/stoic-terminal-implementation-plan.md`
2. **Start Day 1 tomorrow**: Database setup + quote collection
3. **Follow the 7-day schedule**: One component per day
4. **Ship v1.0 next week**: 250 quotes, 30 art pieces, full context awareness

## Resources

- **Full Spec**: `/tmp/stoic-terminal-spec.md`
- **Implementation Plan**: `/tmp/stoic-terminal-implementation-plan.md`
- **Quote Research**: `/mnt/user-data/uploads/philosophical_quote_DB_research.md`
- **Weather Research**: `/mnt/user-data/uploads/weather_apis_research.md`
- **ASCII Art Research**: `/mnt/user-data/uploads/ascii_art_research.md`
- **Embedding Models**: `/mnt/user-data/uploads/lightweight_embedding_models_search_results.md`

---

**You're ready to build! Start coding tomorrow. 🚀**
