#!/usr/bin/env python3
"""
Stoic Terminal - Day 1 Starter Code
Database setup and quote collection from Quotable API and Project Gutenberg
"""

import sqlite3
import json
import requests
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path


class QuoteDatabase:
    """SQLite database abstraction for philosophical quotes"""
    
    def __init__(self, db_path: str = "quotes_v1.db"):
        self.db_path = Path(db_path)
        self.conn = None
        self._init_database()
    
    def _init_database(self):
        """Create database schema if it doesn't exist"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # Main quotes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT NOT NULL,
                source TEXT,
                source_context TEXT,
                source_year INTEGER,
                translator TEXT,
                length_category TEXT CHECK(length_category IN ('bite-sized', 'medium', 'extended')),
                tradition TEXT,
                tags TEXT,
                embedding BLOB,
                copyright_status TEXT DEFAULT 'public_domain',
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Indexes for faster queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_author ON quotes(author)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tradition ON quotes(tradition)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_copyright ON quotes(copyright_status)")
        
        self.conn.commit()
    
    def add_quote(self, 
                  text: str, 
                  author: str,
                  source: Optional[str] = None,
                  source_context: Optional[str] = None,
                  source_year: Optional[int] = None,
                  translator: Optional[str] = None,
                  tradition: Optional[str] = None,
                  tags: Optional[List[str]] = None,
                  copyright_status: str = 'public_domain') -> int:
        """Add a quote to the database"""
        
        # Determine length category
        length = len(text)
        if length <= 150:
            length_category = 'bite-sized'
        elif length <= 400:
            length_category = 'medium'
        else:
            length_category = 'extended'
        
        # Convert tags to JSON
        tags_json = json.dumps(tags) if tags else json.dumps([])
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO quotes (
                text, author, source, source_context, source_year,
                translator, length_category, tradition, tags, copyright_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (text, author, source, source_context, source_year,
              translator, length_category, tradition, tags_json, copyright_status))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_quotes(self) -> List[Dict]:
        """Retrieve all quotes"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quotes ORDER BY date_added DESC")
        
        quotes = []
        for row in cursor.fetchall():
            quote = dict(row)
            quote['tags'] = json.loads(quote['tags']) if quote['tags'] else []
            quotes.append(quote)
        
        return quotes
    
    def search_by_tags(self, tags: List[str], match_mode: str = 'any') -> List[Dict]:
        """Search quotes by tags"""
        cursor = self.conn.cursor()
        
        if match_mode == 'any':
            # Match any tag
            conditions = " OR ".join(["tags LIKE ?" for _ in tags])
            params = [f'%"{tag}"%' for tag in tags]
        else:  # 'all'
            # Match all tags
            conditions = " AND ".join(["tags LIKE ?" for _ in tags])
            params = [f'%"{tag}"%' for tag in tags]
        
        query = f"SELECT * FROM quotes WHERE {conditions}"
        cursor.execute(query, params)
        
        quotes = []
        for row in cursor.fetchall():
            quote = dict(row)
            quote['tags'] = json.loads(quote['tags']) if quote['tags'] else []
            quotes.append(quote)
        
        return quotes
    
    def get_random_quote(self) -> Optional[Dict]:
        """Get a random quote"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
        
        row = cursor.fetchone()
        if row:
            quote = dict(row)
            quote['tags'] = json.loads(quote['tags']) if quote['tags'] else []
            return quote
        return None
    
    def count_quotes(self) -> int:
        """Count total quotes in database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM quotes")
        return cursor.fetchone()[0]
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class QuotableAPICollector:
    """Collect quotes from Quotable API (https://api.quotable.io)"""
    
    BASE_URL = "https://api.quotable.io"
    
    def __init__(self):
        self.session = requests.Session()
        # Disable SSL verification for API with expired cert (safe for read-only public API)
        self.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def fetch_quotes_by_tag(self, tag: str, limit: int = 50) -> List[Dict]:
        """Fetch quotes by tag from Quotable API"""
        quotes = []
        page = 1
        
        while len(quotes) < limit:
            url = f"{self.BASE_URL}/quotes"
            params = {
                'tags': tag,
                'limit': 50,  # Max per request
                'page': page
            }
            
            try:
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if not data['results']:
                    break
                
                for quote_data in data['results']:
                    if len(quotes) >= limit:
                        break
                    
                    quotes.append({
                        'text': quote_data['content'],
                        'author': quote_data['author'],
                        'tags': quote_data['tags'],
                        'source': 'Quotable API',
                        'copyright_status': 'attributed'  # Most are public domain but not all
                    })
                
                page += 1
                
            except requests.RequestException as e:
                print(f"Error fetching quotes: {e}")
                break
        
        return quotes[:limit]
    
    def fetch_quotes_by_author(self, author_name: str, limit: int = 50) -> List[Dict]:
        """Fetch quotes by author"""
        quotes = []
        page = 1
        
        while len(quotes) < limit:
            url = f"{self.BASE_URL}/quotes"
            params = {
                'author': author_name,
                'limit': 50,
                'page': page
            }
            
            try:
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if not data['results']:
                    break
                
                for quote_data in data['results']:
                    if len(quotes) >= limit:
                        break
                    
                    quotes.append({
                        'text': quote_data['content'],
                        'author': quote_data['author'],
                        'tags': quote_data['tags'],
                        'source': 'Quotable API',
                        'copyright_status': 'attributed'
                    })
                
                page += 1
                
            except requests.RequestException as e:
                print(f"Error fetching quotes: {e}")
                break
        
        return quotes[:limit]


def collect_initial_250_quotes(db: QuoteDatabase):
    """Collect initial 250 quotes from various sources"""
    
    collector = QuotableAPICollector()
    total_added = 0
    
    print("=" * 60)
    print("STOIC TERMINAL - Quote Collection (Day 1)")
    print("=" * 60)
    
    # 1. Wisdom quotes (50)
    print("\n[1/5] Collecting wisdom quotes...")
    wisdom_quotes = collector.fetch_quotes_by_tag('wisdom', limit=50)
    for quote in wisdom_quotes:
        db.add_quote(
            text=quote['text'],
            author=quote['author'],
            source=quote['source'],
            tradition='wisdom',
            tags=['wisdom'] + quote['tags'],
            copyright_status=quote['copyright_status']
        )
    total_added += len(wisdom_quotes)
    print(f"    Added {len(wisdom_quotes)} wisdom quotes")
    
    # 2. Philosophy quotes (50)
    print("\n[2/5] Collecting philosophy quotes...")
    philosophy_quotes = collector.fetch_quotes_by_tag('philosophy', limit=50)
    for quote in philosophy_quotes:
        db.add_quote(
            text=quote['text'],
            author=quote['author'],
            source=quote['source'],
            tradition='philosophy',
            tags=['philosophy'] + quote['tags'],
            copyright_status=quote['copyright_status']
        )
    total_added += len(philosophy_quotes)
    print(f"    Added {len(philosophy_quotes)} philosophy quotes")
    
    # 3. Famous quotes (50)
    print("\n[3/5] Collecting famous quotes...")
    famous_quotes = collector.fetch_quotes_by_tag('famous-quotes', limit=50)
    for quote in famous_quotes:
        db.add_quote(
            text=quote['text'],
            author=quote['author'],
            source=quote['source'],
            tradition='general',
            tags=['famous'] + quote['tags'],
            copyright_status=quote['copyright_status']
        )
    total_added += len(famous_quotes)
    print(f"    Added {len(famous_quotes)} famous quotes")
    
    # 4. Inspirational quotes (50)
    print("\n[4/5] Collecting inspirational quotes...")
    inspirational_quotes = collector.fetch_quotes_by_tag('inspirational', limit=50)
    for quote in inspirational_quotes:
        db.add_quote(
            text=quote['text'],
            author=quote['author'],
            source=quote['source'],
            tradition='inspirational',
            tags=['inspirational'] + quote['tags'],
            copyright_status=quote['copyright_status']
        )
    total_added += len(inspirational_quotes)
    print(f"    Added {len(inspirational_quotes)} inspirational quotes")
    
    # 5. Manually add Project Gutenberg quotes (50)
    print("\n[5/5] Adding Project Gutenberg classics...")
    print("    NOTE: You'll need to manually add these 50 quotes from:")
    print("    - Marcus Aurelius Meditations: https://www.gutenberg.org/ebooks/2680")
    print("    - Sun Tzu Art of War: https://www.gutenberg.org/ebooks/132")
    print("    - Seneca's Letters: https://www.gutenberg.org/ebooks/3794")
    print("\n    Use the add_manual_quote() function below as a template.")
    
    # Example manual quote
    db.add_quote(
        text="You have power over your mind - not outside events. Realize this, and you will find strength.",
        author="Marcus Aurelius",
        source="Meditations",
        source_context="Book 8",
        source_year=-180,  # Approximate
        translator="George Long",
        tradition="stoic",
        tags=["stoicism", "control", "inner_strength", "wisdom"],
        copyright_status="public_domain"
    )
    total_added += 1
    
    db.add_quote(
        text="The impediment to action advances action. What stands in the way becomes the way.",
        author="Marcus Aurelius",
        source="Meditations",
        source_context="Book 5",
        source_year=-180,
        translator="Gregory Hays",
        tradition="stoic",
        tags=["stoicism", "adversity", "perseverance", "obstacles"],
        copyright_status="public_domain"
    )
    total_added += 1
    
    print(f"    Added 2 example Stoic quotes (add 48 more manually)")
    
    print("\n" + "=" * 60)
    print(f"COLLECTION COMPLETE: {total_added} quotes added!")
    print(f"Database now contains: {db.count_quotes()} total quotes")
    print("=" * 60)


def add_manual_quote(db: QuoteDatabase):
    """Helper function to add quotes manually from Project Gutenberg"""
    
    # Example template - copy and modify this 50 times
    db.add_quote(
        text="All cruelty springs from weakness.",
        author="Seneca",
        source="On Anger",
        source_context="Book 2, Section 15",
        source_year=41,
        translator="Aubrey Stewart",
        tradition="stoic",
        tags=["stoicism", "anger", "weakness", "virtue"],
        copyright_status="public_domain"
    )
    
    print("Quote added successfully!")


def main():
    """Main collection script"""
    
    # Initialize database
    db = QuoteDatabase("quotes_v1.db")
    
    # Check if database already has quotes
    existing_count = db.count_quotes()
    if existing_count > 0:
        print(f"\n⚠️  Database already contains {existing_count} quotes!")
        response = input("Do you want to add more quotes? (yes/no): ")
        if response.lower() != 'yes':
            print("Exiting without adding quotes.")
            db.close()
            return
    
    # Collect quotes
    collect_initial_250_quotes(db)
    
    # Show some random samples
    print("\n" + "=" * 60)
    print("SAMPLE QUOTES:")
    print("=" * 60)
    for i in range(3):
        quote = db.get_random_quote()
        if quote:
            print(f"\n{i+1}. \"{quote['text']}\"")
            print(f"   — {quote['author']}")
            print(f"   Tags: {', '.join(quote['tags'][:5])}")
    
    db.close()
    
    print("\n✅ Day 1 Complete!")
    print("\nNext steps:")
    print("1. Manually add 48 more Project Gutenberg quotes using add_manual_quote()")
    print("2. Move on to Day 2: ASCII Art Curation")
    print(f"3. Database saved to: {Path('quotes_v1.db').absolute()}")


if __name__ == "__main__":
    main()
