#!/usr/bin/env python3
"""
Seed RuvScan database with ruvnet's GitHub repositories

This script fetches ruvnet's repositories from GitHub and populates
the RuvScan database with initial data. Run this on first setup or
to refresh the database.

Usage:
    python scripts/seed_database.py [--org ORG_NAME] [--limit LIMIT]
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
except ImportError:
    print("❌ requests library not found. Installing...")
    os.system(f"{sys.executable} -m pip install requests")
    import requests

def get_github_token():
    """Get GitHub token from environment"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        # Try to load from .env.local
        env_file = Path(__file__).parent.parent / ".env.local"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("GITHUB_TOKEN="):
                    token = line.split("=", 1)[1].strip()
                    break
    return token

def fetch_repos(org_name="ruvnet", limit=50):
    """Fetch repositories from GitHub (supports both orgs and users)"""
    token = get_github_token()
    if not token:
        print("⚠️  No GITHUB_TOKEN found. API rate limits will apply.")

    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    print(f"📡 Fetching repositories from github.com/{org_name}...")

    # First, check if it's a user or org
    check_url = f"https://api.github.com/users/{org_name}"
    check_response = requests.get(check_url, headers=headers)

    if check_response.status_code != 200:
        print(f"❌ GitHub API error: {check_response.status_code}")
        return []

    account_type = check_response.json().get("type", "User")
    print(f"   Account type: {account_type}")

    # Use appropriate endpoint
    if account_type == "Organization":
        base_url = f"https://api.github.com/orgs/{org_name}/repos"
    else:
        base_url = f"https://api.github.com/users/{org_name}/repos"

    repos = []
    page = 1
    per_page = min(limit, 100)

    while len(repos) < limit:
        params = {
            "per_page": per_page,
            "page": page,
            "sort": "updated",
            "direction": "desc"
        }

        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"❌ GitHub API error: {response.status_code}")
            print(f"   {response.json().get('message', 'Unknown error')}")
            break

        batch = response.json()
        if not batch:
            break

        repos.extend(batch)
        print(f"   Fetched {len(repos)} repos...")

        if len(batch) < per_page:
            break

        page += 1

    return repos[:limit]

def fetch_readme(full_name, headers):
    """Fetch README content for a repository"""
    url = f"https://api.github.com/repos/{full_name}/readme"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        import base64
        content = response.json().get("content", "")
        if content:
            return base64.b64decode(content).decode("utf-8", errors="ignore")
    return None

def init_database(db_path):
    """Initialize database if it doesn't exist"""
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create repos table
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

    # Create leverage_cards table
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

    # Create fact_cache table
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

    conn.commit()
    return conn

def seed_repos(repos, db_path, fetch_readmes=True):
    """Seed database with repositories"""
    conn = init_database(db_path)
    cursor = conn.cursor()

    token = get_github_token()
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    print(f"\n💾 Seeding database: {db_path}")
    print(f"   Total repos to add: {len(repos)}")

    added = 0
    updated = 0
    skipped = 0

    for i, repo in enumerate(repos, 1):
        full_name = repo["full_name"]
        org, name = full_name.split("/")

        # Check if repo exists
        cursor.execute("SELECT id, last_scan FROM repos WHERE full_name = ?", (full_name,))
        existing = cursor.fetchone()

        # Get README if needed
        readme = None
        if fetch_readmes:
            print(f"   [{i}/{len(repos)}] Fetching {full_name}...", end="\r")
            readme = fetch_readme(full_name, headers)

        topics = json.dumps(repo.get("topics", []))
        description = repo.get("description", "")
        stars = repo.get("stargazers_count", 0)
        language = repo.get("language", "")

        if existing:
            # Update existing
            cursor.execute("""
                UPDATE repos
                SET description = ?, topics = ?, readme = ?, stars = ?,
                    language = ?, last_scan = ?
                WHERE full_name = ?
            """, (description, topics, readme, stars, language,
                  datetime.now().isoformat(), full_name))
            updated += 1
        else:
            # Insert new
            cursor.execute("""
                INSERT INTO repos
                (name, org, full_name, description, topics, readme, stars, language, last_scan)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, org, full_name, description, topics, readme, stars,
                  language, datetime.now().isoformat()))
            added += 1

        if i % 10 == 0 or i == len(repos):
            conn.commit()

    print(f"\n   ✅ Added: {added}")
    print(f"   🔄 Updated: {updated}")
    print(f"   ⏭️  Skipped: {skipped}")

    # Show stats
    cursor.execute("SELECT COUNT(*) FROM repos")
    total = cursor.fetchone()[0]
    print(f"\n📊 Database now has {total} total repositories")

    conn.close()
    return added, updated

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Seed RuvScan database with GitHub repos")
    parser.add_argument("--org", default="ruvnet", help="GitHub organization to scan")
    parser.add_argument("--limit", type=int, default=50, help="Max repos to fetch")
    parser.add_argument("--db", default="data/ruvscan.db", help="Database path")
    parser.add_argument("--no-readmes", action="store_true", help="Skip fetching READMEs (faster)")

    args = parser.parse_args()

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║           RuvScan Database Seeder v0.5.1                  ║
╚═══════════════════════════════════════════════════════════╝

Configuration:
  Organization: {args.org}
  Limit:        {args.limit}
  Database:     {args.db}
  Fetch READMEs: {not args.no_readmes}
""")

    try:
        # Fetch repos from GitHub
        repos = fetch_repos(args.org, args.limit)

        if not repos:
            print("❌ No repositories found!")
            return 1

        print(f"✅ Found {len(repos)} repositories")

        # Seed database
        added, updated = seed_repos(repos, args.db, fetch_readmes=not args.no_readmes)

        print(f"""
╔═══════════════════════════════════════════════════════════╗
║                     Seeding Complete!                     ║
╚═══════════════════════════════════════════════════════════╝

Next steps:
  1. Start RuvScan: docker compose up -d
  2. Query repos: curl http://localhost:8000/query \\
       -H "Content-Type: application/json" \\
       -d '{{"intent": "your question here"}}'

  3. Or use Claude Code:
     claude
     > Find tools for building AI applications

📝 To rescan and update:
   python scripts/seed_database.py --org {args.org}

⚠️  Remember to periodically rescan to get latest repos!
""")

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
