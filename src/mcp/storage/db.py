"""
Database layer for RuvScan
Handles SQLite storage for repos, leverage cards, and FACT cache
"""

import sqlite3
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import hashlib
import logging

logger = logging.getLogger(__name__)

class RuvScanDB:
    """SQLite database manager for RuvScan"""

    def __init__(self, db_path: str = "data/ruvscan.db"):
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _init_db(self):
        """Initialize database connection and create tables"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """Create database schema"""
        cursor = self.conn.cursor()

        # Repos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS repos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                org TEXT NOT NULL,
                full_name TEXT UNIQUE NOT NULL,
                description TEXT,
                topics TEXT,
                readme TEXT,
                embedding BLOB,
                sublinear_hash TEXT,
                stars INTEGER DEFAULT 0,
                language TEXT,
                last_scan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(org, name)
            )
        """)

        # Leverage cards table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leverage_cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                repo_id INTEGER NOT NULL,
                capabilities TEXT NOT NULL,
                summary TEXT NOT NULL,
                reasoning TEXT NOT NULL,
                integration_hint TEXT,
                relevance_score REAL NOT NULL,
                runtime_complexity TEXT,
                query_intent TEXT,
                cached BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (repo_id) REFERENCES repos(id)
            )
        """)

        # FACT cache table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT UNIQUE NOT NULL,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                version TEXT DEFAULT '0.5.0',
                metadata TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_repos_org ON repos(org)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_repos_full_name ON repos(full_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cards_repo ON leverage_cards(repo_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cards_score ON leverage_cards(relevance_score)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact_hash ON fact_cache(hash)")

        self.conn.commit()
        logger.info("Database tables created successfully")

    def add_repo(self, repo_data: Dict[str, Any]) -> int:
        """Add or update repository"""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO repos
            (name, org, full_name, description, topics, readme, stars, language, last_scan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            repo_data.get('name'),
            repo_data.get('org'),
            repo_data.get('full_name'),
            repo_data.get('description'),
            json.dumps(repo_data.get('topics', [])),
            repo_data.get('readme'),
            repo_data.get('stars', 0),
            repo_data.get('language'),
            datetime.utcnow()
        ))

        self.conn.commit()
        return cursor.lastrowid

    def get_repo(self, full_name: str) -> Optional[Dict[str, Any]]:
        """Get repository by full name"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM repos WHERE full_name = ?", (full_name,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        return None

    def add_leverage_card(self, card_data: Dict[str, Any]) -> int:
        """Add leverage card"""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO leverage_cards
            (repo_id, capabilities, summary, reasoning, integration_hint,
             relevance_score, runtime_complexity, query_intent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            card_data.get('repo_id'),
            json.dumps(card_data.get('capabilities', [])),
            card_data.get('summary'),
            card_data.get('reasoning'),
            card_data.get('integration_hint'),
            card_data.get('relevance_score'),
            card_data.get('runtime_complexity'),
            card_data.get('query_intent')
        ))

        self.conn.commit()
        return cursor.lastrowid

    def get_leverage_cards(
        self,
        limit: int = 50,
        min_score: float = 0.0,
        cached_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Get leverage cards with filters"""
        cursor = self.conn.cursor()

        query = """
            SELECT lc.*, r.full_name as repo
            FROM leverage_cards lc
            JOIN repos r ON lc.repo_id = r.id
            WHERE lc.relevance_score >= ?
        """
        params = [min_score]

        if cached_only:
            query += " AND lc.cached = 1"

        query += " ORDER BY lc.relevance_score DESC, lc.created_at DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    def add_fact_cache(self, prompt: str, response: str, metadata: Optional[Dict] = None) -> str:
        """Add entry to FACT cache"""
        # Generate deterministic hash
        cache_hash = hashlib.sha256(prompt.encode()).hexdigest()

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO fact_cache
            (hash, prompt, response, metadata)
            VALUES (?, ?, ?, ?)
        """, (
            cache_hash,
            prompt,
            response,
            json.dumps(metadata) if metadata else None
        ))

        self.conn.commit()
        return cache_hash

    def get_fact_cache(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Get cached response from FACT"""
        cache_hash = hashlib.sha256(prompt.encode()).hexdigest()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM fact_cache WHERE hash = ?", (cache_hash,))
        row = cursor.fetchone()

        if row:
            result = dict(row)
            if result.get('metadata'):
                result['metadata'] = json.loads(result['metadata'])
            return result
        return None

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
