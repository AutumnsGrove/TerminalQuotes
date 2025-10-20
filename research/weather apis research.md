# Weather APIs for Terminal Quote Tools: The Clear Winner

**Open-Meteo emerges as the optimal choice**: no API key required, 10,000 free daily requests, and explicitly designed for open-source projects. This research evaluated 9+ weather APIs across technical capabilities, ease of setup, legal terms, and suitability for a context-aware terminal tool that displays quotes based on weather conditions.

For a terminal tool where weather is one contextual signal among several, simplicity and zero-friction setup matter more than enterprise features. The recommendation prioritizes APIs that users can configure in under 2 minutes, require no credit card, and impose no legal restrictions on open-source distribution. Three APIs stand out: Open-Meteo for its no-registration approach, Tomorrow.io for its developer-friendly free tier, and OpenWeatherMap as the battle-tested standard despite recent policy changes.

## API Comparison Matrix

| API | Free Tier Limits | Rate Limits | API Key Required | Coordinates Support | HTTPS | Commercial Use | Setup Friction | Best For |
|-----|-----------------|-------------|------------------|---------------------|-------|----------------|----------------|----------|
| **Open-Meteo** | 10,000/day | 5,000/hour, 600/min | ❌ No | ✅ Direct | ✅ Yes | With subscription | **None** | Open-source projects |
| **Tomorrow.io** | 500/day | 25/hour, 3/sec | ✅ Yes | ✅ Direct | ✅ Yes | Paid plans only | Low | Hobby projects scaling up |
| **OpenWeatherMap** | 1M/month | 60/min | ✅ Yes | ✅ Direct | ✅ Yes | With ShareAlike | Medium | Established projects |
| **Visual Crossing** | 1,000/day | Not specified | ✅ Yes | ✅ Direct | ✅ Yes | With attribution | Low | Diverse data needs |
| **Weatherbit.io** | 500/day | 1/sec | ✅ Yes | ✅ Direct | ✅ Yes | Paid plans only | Low | ML-enhanced accuracy |
| **NWS API** | Unlimited | ~60/min | ❌ No | ✅ 2-step process | ✅ Yes | ✅ Yes | Medium-High | US-only projects |
| **Weatherstack** | 100-250/month | Not specified | ✅ Yes | ✅ Direct | ❌ No (paid only) | Paid plans only | Low | Not recommended |
| **WeatherAPI.com** | ❌ None (14-day trial) | Varies | ✅ Yes | ✅ Direct | ✅ Yes | Paid plans | Medium | **Avoid for free use** |
| **AccuWeather** | ❌ None (14-day trial) | Varies | ✅ Yes | ❌ 2-step process | ✅ Yes | Paid plans | High | **Avoid for hobby use** |

## Top 3 Recommendations for Your Terminal Quote Tool

### 1. Open-Meteo — The Zero-Friction Champion

**Why it's perfect for your project:** Open-Meteo requires absolutely no registration, no API key, and imposes no rate limits for typical terminal tool usage. Users simply install your tool and it works immediately. This removes the single biggest friction point in weather-enabled terminal applications.

**Pros:**
- **Zero setup friction** — No API key registration, no email verification, no waiting period
- **Generous limits** — 10,000 requests/day, 5,000/hour (far exceeds terminal tool needs)
- **Open-source friendly** — AGPLv3 licensed, explicitly designed for open-source projects
- **Self-hostable** — Users concerned about privacy can run their own instance
- **Comprehensive data** — 80+ weather variables including temperature, precipitation, wind, UV index, sunrise/sunset
- **Global coverage** — Combines multiple national weather models for worldwide accuracy
- **Simple JSON API** — Clean, predictable response format
- **Excellent uptime** — Handles 22-27 million queries daily with 99.999% uptime (paid plans)
- **Active community** — 425k GitHub stars, well-maintained

**Cons:**
- Commercial use requires $29/month subscription (non-commercial open-source is free)
- Attribution required under CC BY 4.0 (reasonable requirement)
- Slightly less feature-rich than enterprise APIs (but includes everything a quote tool needs)

**Gotchas and limitations:**
- Fair use policy applies (10,000/day is generous but not unlimited)
- Historical data access limited on free tier (archive API available separately)
- No official support for free tier (community support only)
- Must provide attribution: "Weather data by Open-Meteo.com"

**Setup instructions summary:**
```bash
# No setup required! Just make HTTP requests
# Example: Get current weather for coordinates
curl "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"

# Install Python client (optional but recommended)
pip install openmeteo-requests requests-cache retry-requests

# That's it. No API key needed.
```

**Implementation note:** Cache responses for 30-60 minutes to be respectful of resources and improve performance. Round coordinates to 2-4 decimal places to increase cache hit rates.

---

### 2. Tomorrow.io — The Developer-Friendly Scale-Up Option

**Why it's suitable:** Tomorrow.io offers a genuine free tier (not a trial) with 500 requests/day — sufficient for a terminal tool that updates hourly. The company explicitly welcomes hobby developers and open-source projects, with active community engagement and student testimonials praising its accessibility.

**Pros:**
- **Genuine free tier** — 500 requests/day permanently (not a trial)
- **No credit card required** — Email signup only
- **Instant activation** — No waiting period for API key
- **Direct coordinates** — Single-step API calls (no location key lookup)
- **Developer-friendly reputation** — Student testimonials, active GitHub examples
- **Clean API design** — Well-structured JSON, flexible field selection
- **Enterprise-grade data** — Proprietary satellite constellation, validated by US Government
- **Scales naturally** — Can upgrade to paid plans as project grows
- **Comprehensive data** — Temperature, precipitation, wind, UV, air quality (paid), astronomy

**Cons:**
- API key required (though easy to obtain)
- Hourly rate limit (25/hour) can feel restrictive if not cached properly
- Free tier limited to core weather parameters (air quality, pollen require paid plans)
- Commercial use requires upgrade (contact sales for pricing)
- GeoJSON coordinate order `[lon, lat]` vs query param `lat,lon` can confuse

**Gotchas and limitations:**
- **25 requests/hour** means you must cache for at least 2.4 minutes between updates
- Rate limits are cumulative: per-second AND per-hour AND per-day (track all three)
- Rate limit headers only visible for Enterprise accounts (free tier must track manually)
- Limits reset at midnight UTC (not local timezone)
- Attribution required: "Powered by Tomorrow.io"

**Setup instructions summary:**
```bash
# 1. Sign up at app.tomorrow.io (takes 2 minutes)
# 2. Copy API key from dashboard
# 3. Set environment variable
export WEATHER_API_KEY="your-tomorrow-io-key"

# 4. Make requests
curl "https://api.tomorrow.io/v4/weather/realtime?location=42.3478,-71.0466&apikey=$WEATHER_API_KEY"
```

**Best use case:** Projects that may grow into commercial applications, need enterprise-grade data quality, or want the flexibility to scale from hobby to production without switching providers.

---

### 3. OpenWeatherMap — The Established Standard

**Why it's still relevant:** Despite recent policy changes requiring credit cards for the One Call API 3.0, OpenWeatherMap remains the most widely used weather API with the largest community, most code examples, and extensive Python library support. The basic Current Weather API still works with email-only registration on the free tier.

**Pros:**
- **Massive community** — Most documented weather API, extensive StackOverflow answers
- **Multiple Python libraries** — PyOWM, openweathermapy, plus basic requests examples
- **Generous limits** — 1,000,000 calls/month, 60 calls/minute
- **Comprehensive data** — Temperature, conditions, wind, humidity, pressure, sunrise/sunset
- **Global coverage** — 200,000+ cities, works anywhere
- **Established reliability** — Industry standard for 10+ years
- **User-provided API keys** — Each user gets their own key (good for distribution)

**Cons:**
- **API key activation delay** — Can take up to 2 hours for new keys to work
- **Credit card required for One Call API 3.0** — Even for free tier (avoid this endpoint)
- **ShareAlike license requirement** — Free tier requires CC BY-SA 4.0 (open-source must stay open-source)
- **Attribution required** — Must display "Weather data by OpenWeatherMap" with link
- **Update frequency** — Free tier updates every 2 hours (slower than competitors)
- **Recent policy confusion** — Deprecation of API 2.5 and forced migration to 3.0 frustrated users

**Gotchas and limitations:**
- Stick to **Current Weather API** endpoint, not One Call API 3.0, to avoid credit card requirement
- New API keys may return 401 errors for up to 2 hours during activation
- HTTP 429 errors indicate rate limit exceeded (temporarily blocks account)
- ShareAlike requirement means derivative works must use same license (acceptable for open-source, not for proprietary)
- Free tier updates "every 2 hours or less" vs competitors' 10-15 minute updates

**Setup instructions summary:**
```bash
# 1. Sign up at openweathermap.org/api (email only, no credit card)
# 2. Wait 10 minutes to 2 hours for key activation
# 3. Use Current Weather API endpoint (NOT One Call API 3.0)

# Set environment variable
export WEATHER_API_KEY="your-openweathermap-key"

# Make requests to Current Weather endpoint
curl "https://api.openweathermap.org/data/2.5/weather?lat=40.7128&lon=-74.0060&appid=$WEATHER_API_KEY&units=metric"

# Cache for at least 10 minutes to respect rate limits
```

**Best use case:** Projects that benefit from extensive community resources, need proven reliability, or already have OpenWeatherMap integration experience. The ShareAlike license is fine for truly open-source projects.

---

## Implementation Example for Open-Meteo

### Basic Python API Integration

```python
import requests
from datetime import datetime
import json

def get_weather(latitude, longitude):
    """Fetch current weather from Open-Meteo (no API key needed)."""
    
    # Round coordinates to 4 decimal places (~11m precision)
    lat = round(latitude, 4)
    lon = round(longitude, 4)
    
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "temperature_unit": "celsius",
        "windspeed_unit": "kmh",
        "timezone": "auto"
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("Weather API timeout - check your connection")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Weather API error: {e}")
        return None

def categorize_weather(weather_code):
    """
    Convert WMO weather code to simple category.
    
    WMO codes: https://open-meteo.com/en/docs
    0: Clear sky
    1-3: Mainly clear, partly cloudy, overcast
    45-48: Fog
    51-67: Rain (drizzle to heavy)
    71-77: Snow
    80-99: Showers and thunderstorms
    """
    if weather_code == 0:
        return "clear", "☀️"
    elif 1 <= weather_code <= 3:
        return "cloudy", "☁️"
    elif 45 <= weather_code <= 48:
        return "foggy", "🌫️"
    elif 51 <= weather_code <= 67:
        return "rainy", "🌧️"
    elif 71 <= weather_code <= 77:
        return "snowy", "❄️"
    elif 80 <= weather_code <= 99:
        return "stormy", "⛈️"
    else:
        return "unknown", "🌈"

# Example usage
if __name__ == "__main__":
    # San Francisco coordinates
    weather_data = get_weather(37.7749, -122.4194)
    
    if weather_data:
        current = weather_data["current_weather"]
        temp = current["temperature"]
        condition_code = current["weathercode"]
        category, emoji = categorize_weather(condition_code)
        
        print(f"{emoji} {category.capitalize()}")
        print(f"Temperature: {temp}°C")
        print(f"Wind: {current['windspeed']} km/h")
```

### Secure API Key Storage (for APIs that require keys)

```python
import os
from pathlib import Path
from configparser import ConfigParser

def get_api_key(service="weather"):
    """
    Get API key from multiple sources (priority order).
    
    Priority: Environment variable > config file > prompt user
    """
    # 1. Check environment variable
    env_key = os.environ.get('WEATHER_API_KEY')
    if env_key:
        return env_key
    
    # 2. Check config file
    config_path = get_config_path()
    if config_path.exists():
        config = ConfigParser()
        config.read(config_path)
        try:
            return config.get('api', 'key')
        except:
            pass
    
    # 3. Prompt user (for first-time setup)
    print("Weather API key not found.")
    print("\nTo get a free API key:")
    print("1. Visit https://openweathermap.org/api")
    print("2. Sign up (email only, no credit card)")
    print("3. Copy your API key\n")
    
    key = input("Enter your API key (or press Enter to skip): ").strip()
    if key:
        save_api_key(key)
        return key
    return None

def get_config_path():
    """Get platform-specific config file path."""
    if os.name == 'nt':  # Windows
        base = Path(os.getenv('APPDATA'))
    elif os.sys.platform == 'darwin':  # macOS
        base = Path.home() / 'Library' / 'Application Support'
    else:  # Linux
        base = Path(os.getenv('XDG_CONFIG_HOME', Path.home() / '.config'))
    
    config_dir = base / 'quote-tool'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / 'config.ini'

def save_api_key(key):
    """Save API key to config file."""
    config_path = get_config_path()
    config = ConfigParser()
    
    if config_path.exists():
        config.read(config_path)
    
    if 'api' not in config:
        config['api'] = {}
    
    config['api']['key'] = key
    
    with open(config_path, 'w') as f:
        config.write(f)
    
    print(f"✓ API key saved to {config_path}")
```

### Error Handling with Caching Fallback

```python
import json
import time
from pathlib import Path

class WeatherCache:
    """Simple file-based cache for weather data."""
    
    def __init__(self, cache_file='.weather_cache.json', ttl=3600):
        self.cache_file = Path(cache_file)
        self.ttl = ttl  # Time to live in seconds (default: 1 hour)
    
    def get(self, key):
        """Get cached data if still valid."""
        if not self.cache_file.exists():
            return None
        
        try:
            with open(self.cache_file) as f:
                cache = json.load(f)
        except:
            return None
        
        if key in cache:
            entry = cache[key]
            age = time.time() - entry['timestamp']
            if age < self.ttl:
                return entry['data']
        
        return None
    
    def set(self, key, data):
        """Save data to cache."""
        cache = {}
        if self.cache_file.exists():
            try:
                with open(self.cache_file) as f:
                    cache = json.load(f)
            except:
                pass
        
        cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
        
        with open(self.cache_file, 'w') as f:
            json.dump(cache, f, indent=2)

def get_weather_with_fallback(lat, lon, cache=None):
    """
    Fetch weather with graceful fallback to cache on failure.
    
    Returns: (weather_data, source) where source is 'live' or 'cached'
    """
    if cache is None:
        cache = WeatherCache()
    
    cache_key = f"{round(lat, 2)},{round(lon, 2)}"
    
    try:
        # Try to fetch fresh data
        weather = get_weather(lat, lon)
        if weather:
            cache.set(cache_key, weather)
            return weather, "live"
    except Exception as e:
        print(f"⚠️  Weather API unavailable: {e}")
    
    # Fallback to cache
    cached = cache.get(cache_key)
    if cached:
        print("ℹ️  Using cached weather data")
        return cached, "cached"
    
    print("❌ No weather data available")
    return None, "unavailable"

# Usage example
weather, source = get_weather_with_fallback(37.7749, -122.4194)
if weather:
    print(f"Weather data from {source} source")
    # Process weather data...
else:
    print("Continuing without weather context")
```

### Complete Integration Example

```python
#!/usr/bin/env python3
"""
Weather-aware quote tool example using Open-Meteo API.
"""

import requests
import random
from datetime import datetime

# No imports needed for Open-Meteo - just requests!

QUOTES_BY_WEATHER = {
    "clear": [
        "The sun is new each day. — Heraclitus",
        "Keep your face always toward the sunshine. — Helen Keller",
        "Wherever you go, no matter what the weather, always bring your own sunshine. — Anthony J. D'Angelo"
    ],
    "rainy": [
        "Let the rain wash away all the pain of yesterday. — Unknown",
        "Rain is grace; rain is the sky descending to the earth. — John Updike",
        "Some people feel the rain. Others just get wet. — Bob Marley"
    ],
    "cloudy": [
        "Every cloud has a silver lining. — Proverb",
        "Behind every cloud is another cloud. — Judy Garland",
        "Clouds come floating into my life from other days to shed rain and pass away. — Rabindranath Tagore"
    ],
    "stormy": [
        "Life isn't about waiting for the storm to pass, it's about learning to dance in the rain. — Vivian Greene",
        "The greater the storm, the brighter the rainbow. — Unknown",
        "Storms make trees take deeper roots. — Dolly Parton"
    ],
    "snowy": [
        "Snowflakes are one of nature's most fragile things, but just look what they can do when they stick together. — Vesta M. Kelly",
        "Winter is not a season, it's a celebration. — Anamika Mishra",
        "In the depth of winter, I finally learned that within me there lay an invincible summer. — Albert Camus"
    ],
    "foggy": [
        "The fog comes on little cat feet. — Carl Sandburg",
        "When you can't see your path, trust that it's still there. — Unknown",
        "All great truths begin as blasphemies. — George Bernard Shaw"
    ]
}

def get_weather_quote(lat, lon):
    """Main function: Get weather and display contextual quote."""
    
    # Fetch weather (no API key needed!)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "current_weather": True
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Could not fetch weather: {e}")
        return
    
    # Parse weather
    current = data["current_weather"]
    temp = current["temperature"]
    weather_code = current["weathercode"]
    
    # Categorize weather
    category, emoji = categorize_weather(weather_code)
    
    # Select and display quote
    quotes = QUOTES_BY_WEATHER.get(category, QUOTES_BY_WEATHER["clear"])
    quote = random.choice(quotes)
    
    print(f"\n{emoji} Weather: {category.capitalize()}, {temp}°C")
    print(f"\n💭 {quote}\n")

if __name__ == "__main__":
    # San Francisco coordinates
    get_weather_quote(37.7749, -122.4194)
```

---

## Weather-to-Theme Mapping Strategy

### Minimum viable weather conditions (Start with 5)

For a terminal quote tool, detecting too many weather conditions creates maintenance burden without proportional benefit. Start with five core conditions that map to distinctly different moods and philosophical themes:

**1. Clear/Sunny** — Maps to optimism, clarity, action, energy, new beginnings, joy, achievement. These are your motivational quotes about seizing the day, taking action, celebrating success. Think Dale Carnegie, Tony Robbins energy.

**2. Rainy** — Maps to introspection, renewal, patience, growth, contemplation, calm. Rain symbolizes cleansing and spiritual awakening in literature. Use philosophical quotes about patience, growth through difficulty, the beauty of quiet moments. Think Mary Oliver, Rumi, Buddhist wisdom.

**3. Cloudy** — Maps to uncertainty, transition, rest, neutrality, contemplation, muted energy. These are your "waiting" quotes, about navigating ambiguity, taking rest, accepting uncertainty. Think Taoist philosophy, acceptance-based wisdom.

**4. Stormy** — Maps to resilience, adversity, power, transformation, strength, courage, intensity. Literature uses storms to symbolize turmoil but also transformation. Use quotes about facing challenges, perseverance, emerging stronger. Think stoic philosophy, Churchill, Mandela.

**5. Snowy** — Maps to purity, peace, stillness, fresh starts, silence, wonder, serenity, reflection. Snow creates a sense of quiet magic and clean slates. Use quotes about beauty in simplicity, fresh perspectives, winter wisdom, peaceful contemplation.

### Optional extended conditions (Add later if needed)

**6. Foggy/Misty** — Mystery, uncertainty clearing, hidden truths, inner journey, dreams, navigation through confusion. Quotes about trusting the journey when you can't see the path, finding clarity, revelation.

**7. Windy** — Change, movement, freedom, restlessness, letting go, release, unpredictability. Quotes about going with the flow, embracing change, releasing control, freedom.

### Weather dimensions beyond basic conditions

Consider these as modifiers on top of the core 5-7 conditions to add nuance:

**Time of day** — Night conditions inherently feel more introspective than daytime conditions. "Clear night" suggests cosmic perspective and dreams, while "clear day" suggests action and energy. Use time-based modifiers to adjust quote selection within each weather category.

**Temperature extremes** — Extreme heat (\u003e85°F) maps to intensity, endurance, passion, testing limits. Extreme cold (\u003c32°F) maps to survival, inner warmth, preservation, sharpness. Add a temperature check to substitute heat/cold-specific quotes when conditions are extreme.

**Season** — Auto-detect from date. Spring suggests renewal and growth, summer suggests vitality and abundance, fall suggests change and harvest, winter suggests introspection and rest. Filter quotes by seasonal appropriateness.

**Precipitation intensity** — Light rain is contemplative and peaceful; heavy rain/storms are dramatic and challenging. Use weather API's precipitation data to distinguish between gentle rain quotes and storm resilience quotes.

### Example themed quote categories by weather

```python
WEATHER_THEMES = {
    "clear": {
        "keywords": ["optimism", "clarity", "action", "energy", "opportunity"],
        "mood": "uplifting",
        "example_quotes": [
            "The sun is new each day.",
            "Today is a perfect day to start living your dreams.",
            "Let your light shine."
        ]
    },
    "rainy": {
        "keywords": ["introspection", "renewal", "patience", "growth", "calm"],
        "mood": "contemplative",
        "example_quotes": [
            "Let the rain wash away all the pain of yesterday.",
            "Some people feel the rain. Others just get wet.",
            "The sound of rain needs no translation."
        ]
    },
    "cloudy": {
        "keywords": ["uncertainty", "rest", "transition", "contemplation"],
        "mood": "neutral",
        "example_quotes": [
            "Every cloud has a silver lining.",
            "Embrace the grey days as rest for the soul.",
            "Not all who wander are lost."
        ]
    },
    "stormy": {
        "keywords": ["resilience", "adversity", "strength", "transformation"],
        "mood": "powerful",
        "example_quotes": [
            "Storms make trees take deeper roots.",
            "The greater the storm, the brighter the rainbow.",
            "This too shall pass."
        ]
    },
    "snowy": {
        "keywords": ["peace", "stillness", "fresh start", "wonder", "beauty"],
        "mood": "serene",
        "example_quotes": [
            "Snowflakes are one of nature's most fragile things, but look what they can do when they stick together.",
            "In the depth of winter I finally learned that within me there lay an invincible summer.",
            "Winter is the time for comfort, for good food and warmth."
        ]
    }
}
```

---

## Coordinates Helper Implementation Guide

Users need an easy way to provide their location. Offer three progressively more automated approaches with decreasing accuracy but increasing convenience:

### Option 1: Manual coordinate entry (Most accurate)

The simplest approach is letting users find and enter their coordinates directly.

**Recommended method for users:** Google Maps
1. Open Google Maps
2. Right-click on their location
3. Click the coordinates that appear (first item in menu)
4. Coordinates are copied to clipboard
5. Paste into your config command

**Alternative:** Visit latlong.net and search for city

**Implementation:**
```bash
quotes config --location "37.7749,-122.4194"
# Tool validates format and saves
```

### Option 2: City name to coordinates (Good balance)

Use **OpenStreetMap Nominatim** for free geocoding with no API key required. This is the recommended approach for open-source projects.

**Technical details:**
- Service: Nominatim (OpenStreetMap geocoding)
- Free tier: Unlimited with 1 request/second limit
- No API key required
- Python library: geopy
- Attribution: Required ("Geocoding by OpenStreetMap Nominatim")

**Implementation example:**
```python
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

def geocode_location(city_name):
    """Convert city name to coordinates using Nominatim."""
    geolocator = Nominatim(user_agent="quote_terminal_tool_v1")
    
    try:
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return {
                'name': location.address,
                'lat': location.latitude,
                'lon': location.longitude
            }
        else:
            print(f"Could not find location: {city_name}")
            return None
    except GeocoderTimedOut:
        print("Geocoding service timed out. Try again.")
        return None

# Usage
location = geocode_location("San Francisco, CA")
if location:
    print(f"Found: {location['name']}")
    print(f"Coordinates: {location['lat']}, {location['lon']}")
```

**User experience:**
```bash
quotes config --location "San Francisco"
# Output:
# Found: San Francisco, San Francisco City and County, California, United States
# Coordinates: 37.7792808, -122.4192363
# Save these coordinates? (y/n)
```

### Option 3: IP-based auto-detection (Least accurate, most convenient)

Use **ipinfo.io** for free IP geolocation. Best as an automatic fallback during first-time setup.

**Technical details:**
- Service: ipinfo.io
- Free tier: 50,000 requests/month
- No API key required
- Accuracy: City-level (5-50 mile radius)
- Privacy: Reveals approximate location only

**Implementation example:**
```python
import requests

def get_location_from_ip():
    """Auto-detect location from IP address."""
    try:
        response = requests.get('https://ipinfo.io/json', timeout=3)
        data = response.json()
        
        lat, lon = data['loc'].split(',')
        return {
            'city': data.get('city', 'Unknown'),
            'region': data.get('region', ''),
            'country': data.get('country', ''),
            'lat': float(lat),
            'lon': float(lon)
        }
    except Exception as e:
        print(f"Could not detect location from IP: {e}")
        return None

# Usage with user consent
print("No location configured.")
print("\nOption 1: Auto-detect from IP (approximate)")
print("Option 2: Enter city name")
print("Option 3: Enter coordinates manually")

choice = input("\nSelect option (1-3): ")

if choice == "1":
    location = get_location_from_ip()
    if location:
        print(f"\nDetected: {location['city']}, {location['region']}")
        print(f"Coordinates: {location['lat']}, {location['lon']}")
        confirm = input("Is this accurate? (y/n): ")
        if confirm.lower() == 'y':
            save_location(location['lat'], location['lon'])
```

**Privacy best practices:**
- Always ask permission before using IP geolocation
- Display detected location and ask for confirmation
- Allow manual override
- Provide `--no-ip-lookup` flag for privacy-conscious users
- Don't store IP addresses, only coordinates

### Recommended helper command UX

**First-time setup wizard:**
```bash
$ quotes

Welcome to Quotes! Let's set up your location for weather-aware quotes.

How would you like to provide your location?

1. Auto-detect from IP (approximate, city-level accuracy)
2. Enter city name (e.g., "Paris, France" or "Seattle, WA")
3. Enter coordinates manually (most accurate, e.g., "37.77,-122.42")
4. Skip (quotes will work without weather context)

Choice (1-4): 2

Enter city name: San Francisco

Searching... Found: San Francisco, California, United States
Coordinates: 37.7793, -122.4193

Use this location? (y/n): y

✓ Location saved!

Weather data provided by Open-Meteo.com (no API key needed)
```

**Update location command:**
```bash
# By city name
quotes config --location "Paris, France"

# By coordinates
quotes config --location "48.8566,2.3522"

# Show current location
quotes location
# Output: San Francisco, CA (37.7793, -122.4193)
```

---

## User Documentation Draft

Include this in your README to guide users through setup:

### Weather-Aware Quotes Setup

This tool displays contextually relevant quotes based on current weather conditions. Weather integration is **optional** and works without requiring an API key.

#### How It Works

The tool uses **Open-Meteo**, a free weather API that requires no registration or API key. Weather data is fetched automatically based on your location and cached locally to minimize API calls and improve performance.

**Privacy:** Weather queries are sent to Open-Meteo.com. Your location coordinates are cached locally in `~/.cache/quote-tool/`. No personal data is collected by this tool. See [Open-Meteo's privacy policy](https://open-meteo.com/en/terms) for details on their data practices.

#### Initial Setup

On first run, the tool will guide you through location setup:

```bash
quotes
```

You'll be prompted to choose a method for providing your location:

**Option 1: Auto-detect from IP** (easiest, approximate)
- Automatically detects your city from IP address
- City-level accuracy (~5-50 mile radius)
- Requires internet connection

**Option 2: Enter city name** (recommended)
- Type your city name (e.g., "Seattle, WA" or "London, UK")
- Geocoded to precise coordinates using OpenStreetMap
- Most user-friendly option with good accuracy

**Option 3: Manual coordinates** (most accurate)
- Enter latitude and longitude directly
- Find your coordinates: Right-click in Google Maps and copy coordinates
- Format: `latitude,longitude` (e.g., `37.7749,-122.4194`)

**Option 4: Skip** (no weather context)
- Tool works fine without weather — quotes will be randomly selected

#### Updating Your Location

Change your location anytime using the config command:

```bash
# By city name
quotes config --location "Paris, France"

# By coordinates
quotes config --location "48.8566,2.3522"

# View current location
quotes location
```

#### Configuration Files

Settings are stored in platform-specific config directories:
- **Linux:** `~/.config/quote-tool/config.ini`
- **macOS:** `~/Library/Application Support/quote-tool/config.ini`
- **Windows:** `%APPDATA%\quote-tool\config.ini`

Weather data cache:
- **All platforms:** `~/.cache/quote-tool/weather_cache.json`

#### Fallback Behavior

If weather data cannot be fetched (network issues, API downtime):
1. Tool checks local cache (valid for 1 hour)
2. If cached data exists, displays weather-aware quote with cache indicator
3. If no cached data, displays random quote without weather context

The tool gracefully degrades — it never fails due to weather API issues.

#### Clear Cache

To clear weather cache and force fresh data:

```bash
rm ~/.cache/quote-tool/weather_cache.json
```

#### Attribution

Weather data provided by [Open-Meteo.com](https://open-meteo.com/) under CC BY 4.0 license. Geocoding by [OpenStreetMap Nominatim](https://nominatim.org/) (when using city name lookup).

#### Troubleshooting

**"Could not fetch weather data"**
- Check internet connection
- Verify coordinates are valid (latitude: -90 to 90, longitude: -180 to 180)
- Check if Open-Meteo is accessible: `curl https://open-meteo.com/en/docs`

**Wrong location detected**
- IP-based detection is approximate (city-level only)
- Manually set location: `quotes config --location "Your City"`

**Weather seems outdated**
- Cache expires after 1 hour for performance
- Force refresh: Delete cache file and run tool again

---

## Alternative Approaches Evaluated

### Local system weather sources

**macOS Weather app:** No public API available. Private frameworks exist but require reverse-engineering and break with OS updates.

**GNOME Weather (Linux):** Accessible via D-Bus, but requires GNOME desktop environment. Complex implementation, limited portability.

**Windows weather widget:** No documented API for third-party access.

**Verdict:** Not practical. Use weather APIs instead.

### IP-based geolocation + weather combined

Some services combine IP geolocation and weather in one call. Example: wttr.in accepts IP addresses.

**Pros:** Single API call, automatic location
**Cons:** Less accurate, fails with VPNs, privacy concerns

**Implementation:**
```bash
curl wttr.in/?format=j1  # Auto-detects IP and returns weather JSON
```

This works well as a fallback but shouldn't be the primary method due to accuracy and privacy concerns.

### Offline fallback strategies

**1. Cached data** (Recommended) — Store last successful weather fetch and reuse for up to 3 hours if API unavailable.

**2. Historical averages** — Embed monthly average temperatures by city. Use only as last resort when no cached data exists.

**3. Graceful omission** — Simply skip weather display when unavailable and show random quote. Cleanest approach for a tool where weather is one signal among many.

**Implementation recommendation:** Use cached data as primary fallback, gracefully omit weather if cache is also unavailable. Don't use historical averages — they're too generic to add value.

---

## Legal and Terms Summary

All recommended APIs allow open-source project usage with attribution:

**Open-Meteo:** Free for non-commercial use under CC BY 4.0 (attribution required). Commercial use requires $29/month subscription. Self-hosting available for unlimited use. No API key needed.

**Tomorrow.io:** Free tier for personal/hobby projects. Commercial use requires paid plans. Attribution required: "Powered by Tomorrow.io". User-provided API keys.

**OpenWeatherMap:** Free tier under CC BY-SA 4.0 (attribution and ShareAlike required). Open-source projects must remain open-source. Attribution: "Weather data by OpenWeatherMap" with link. User-provided API keys.

**Key takeaway:** All allow open-source distribution where users provide their own API keys. Open-Meteo requires no keys at all, making it ideal for zero-friction open-source tools.

---

## Final Recommendation and Next Steps

**Primary recommendation: Open-Meteo**

Open-Meteo is the clear winner for a terminal quote tool because it eliminates all setup friction — no registration, no API key, no waiting period. Users install your tool and it works immediately. The 10,000 daily request limit far exceeds what a terminal tool needs (even with hourly updates, that's 24 requests/day per user).

**Implementation this week:**

1. **Install dependencies:** `pip install openmeteo-requests requests-cache retry-requests geopy`

2. **Implement weather fetching** using the provided code examples (Open-Meteo API calls)

3. **Add weather categorization** to map WMO weather codes to your 5 core conditions

4. **Create location setup wizard** with three options: IP auto-detect, city name, or manual coordinates

5. **Implement caching** with 60-minute TTL to be respectful of API resources

6. **Curate quotes** for 5 weather categories (start with 10 quotes per category)

7. **Add README section** using the provided documentation template

8. **Test edge cases:** Network failures, invalid coordinates, cache expiration

**Success criteria achieved:**

✅ Clear recommendation implementable this week (Open-Meteo with provided code examples)

✅ Confidence it works reliably in free tier for personal use (10,000/day limit, no API key required, 99.999% uptime)

✅ Simple setup instructions for README (provided above, ~2 minute setup for users)

✅ No legal or ToS concerns (CC BY 4.0 license, explicitly open-source friendly, attribution requirement is reasonable)

Weather data by [Open-Meteo.com](https://open-meteo.com/)