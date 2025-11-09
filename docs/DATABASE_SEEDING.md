# 🌱 RuvScan Database Seeding Guide

## Overview

Each clone of RuvScan already ships with `data/ruvscan.db` filled with roughly 100 public projects from the **ruvnet** GitHub organization (think `ruvnet/sublinear-time-solver`, `ruvnet/FACT`, `ruvnet/MidStream`, etc.). You can run the MCP server immediately and start asking questions without touching any scripts.

The seeding workflow below is therefore **optional**—use it when you want to refresh that bundled catalog, add your own org/user, or rebuild the database from scratch.

## Quick Start

### Initial Setup (Automatic Seeding)

```bash
# 1. Clone the repository
git clone https://github.com/Hulupeep/ruvscan.git
cd ruvscan

# 2. Setup environment
cp .env.example .env.local
# Edit .env.local and add your GITHUB_TOKEN

# 3. (Optional) Refresh or extend the database
#    Skip if you're happy with the included ruvnet dataset.
python3 scripts/seed_database.py

# 4. Start RuvScan
docker compose up -d

# 5. Start using immediately!
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"intent": "Find tools for AI applications"}'
```

## Default Configuration

The default seeding settings are in `.env.local`:

```bash
# Default repository to scan/seed
RUVSCAN_SOURCE_TYPE=org        # or 'user'
RUVSCAN_SOURCE_NAME=ruvnet     # GitHub username/org

# Database location
DATABASE_TYPE=sqlite
SQLITE_PATH=data/ruvscan.db
```

## Seed Script Usage

### Basic Seeding

```bash
# Seed with default (ruvnet, 50 repos)
python3 scripts/seed_database.py

# Seed specific user/org
python3 scripts/seed_database.py --org openai --limit 30

# Seed without README content (faster)
python3 scripts/seed_database.py --org vercel --limit 20 --no-readmes
```

### Advanced Options

```bash
python3 scripts/seed_database.py \
  --org anthropics \      # GitHub user/org name
  --limit 100 \           # Max repos to fetch
  --db data/custom.db \   # Custom database path
  --no-readmes            # Skip README fetching (much faster)
```

### Prefer using the MCP tools?

- Inside Claude / Codex say: **“Use scan_github on org anthropics with limit 25.”**
- Or run the bundled CLI: `./scripts/ruvscan scan org anthropics --limit 25`

Both routes feed new repositories into the same SQLite database alongside the preloaded ruvnet entries.

## What Gets Seeded?

For each repository, the following data is stored:

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Repository name | `sublinear-time-solver` |
| `org` | Owner (user/org) | `ruvnet` |
| `full_name` | Full identifier | `ruvnet/sublinear-time-solver` |
| `description` | Repo description | "TRUE O(log n) algorithms" |
| `topics` | GitHub topics | `["algorithms", "optimization"]` |
| `readme` | README content | Full markdown text |
| `stars` | Star count | `157` |
| `language` | Primary language | `Python` |
| `last_scan` | Scan timestamp | `2025-10-23 14:10:32` |

## Database Tracking

### Last Scan Tracking

Every repository has a `last_scan` timestamp. Re-running the seed script will:

- ✅ **Update** existing repos with latest data
- ✅ **Add** new repos that don't exist
- ✅ **Refresh** the `last_scan` timestamp

```bash
# Check when repos were last scanned (requires sqlite3)
sqlite3 data/ruvscan.db "
  SELECT full_name, last_scan
  FROM repos
  ORDER BY last_scan DESC
  LIMIT 10;
"
```

### Rescan Strategy

**Recommended frequency:**
- **Active development**: Weekly
- **Production use**: Monthly
- **After major updates**: Immediately

```bash
# Quick rescan (no READMEs, faster)
python3 scripts/seed_database.py --org ruvnet --no-readmes

# Full rescan (includes READMEs)
python3 scripts/seed_database.py --org ruvnet
```

## Seeding Multiple Sources

You can seed from multiple organizations/users:

```bash
# Seed from multiple sources
python3 scripts/seed_database.py --org ruvnet --limit 50
python3 scripts/seed_database.py --org openai --limit 30
python3 scripts/seed_database.py --org anthropics --limit 20
python3 scripts/seed_database.py --org vercel --limit 25

# Check total repos
python3 scripts/seed_database.py --org facebook --limit 15
```

After seeding, your database will have repos from all sources!

## Performance Tips

### Fast Seeding (No READMEs)

```bash
# Fastest: Just metadata, no README content
python3 scripts/seed_database.py --org ruvnet --limit 100 --no-readmes

# Speed: ~2-3 seconds per 10 repos
# Use this for initial exploration
```

### Full Seeding (With READMEs)

```bash
# Slower: Includes full README content
python3 scripts/seed_database.py --org ruvnet --limit 50

# Speed: ~5-10 seconds per 10 repos
# Use this for production quality data
```

### Rate Limiting

**Without GitHub Token:**
- Limit: 60 requests/hour
- Seeding: ~10-15 repos max

**With GitHub Token:**
- Limit: 5,000 requests/hour
- Seeding: Hundreds of repos easily

**Always use a GitHub token for seeding!**

## Changing Default Repository

### Method 1: Edit .env.local

```bash
# Edit the file
nano .env.local

# Change these lines:
RUVSCAN_SOURCE_NAME=your-github-username
RUVSCAN_SOURCE_TYPE=user

# Reseed
python3 scripts/seed_database.py
```

### Method 2: CLI Override

```bash
# One-time seed of different repo
python3 scripts/seed_database.py --org microsoft --limit 50

# Your .env.local default stays unchanged
```

## Database Management

### Check Database Stats

```bash
# Run seed script with any org to see stats at the end
python3 scripts/seed_database.py --org ruvnet --limit 1

# Shows:
# - Total repos in database
# - Added/Updated counts
```

### Backup Database

```bash
# Backup before major changes
cp data/ruvscan.db data/ruvscan.db.backup.$(date +%Y%m%d)

# Restore if needed
cp data/ruvscan.db.backup.20251023 data/ruvscan.db
docker compose restart
```

### Reset Database

```bash
# Complete reset (deletes all data)
docker compose down
rm -f data/ruvscan.db
python3 scripts/seed_database.py
docker compose up -d
```

## Troubleshooting

### Permission Denied

```bash
# If data directory owned by root
docker compose down
rm -rf data
mkdir -p data
python3 scripts/seed_database.py
docker compose up -d
```

### GitHub API 404 Error

```bash
# Check if user/org exists
curl -s https://api.github.com/users/username | jq .

# If "Not Found", the username is wrong
```

### No GitHub Token

```bash
# Add to .env.local
echo "GITHUB_TOKEN=ghp_your_token_here" >> .env.local

# Generate token at: https://github.com/settings/tokens
# Needs scopes: public_repo, read:org
```

### Database Locked

```bash
# Stop Docker to release lock
docker compose down

# Then seed
python3 scripts/seed_database.py

# Restart
docker compose up -d
```

## Seeding in Production

### Docker-based Seeding

Create a seed script in your Dockerfile or docker-compose:

```dockerfile
# Dockerfile.python
RUN python3 scripts/seed_database.py --org ruvnet --limit 100 --no-readmes
```

### Automated Reseeding

Create a cron job:

```bash
# crontab -e
# Reseed every week on Sunday at 2am
0 2 * * 0 cd /path/to/ruvscan && python3 scripts/seed_database.py
```

### CI/CD Integration

```yaml
# .github/workflows/seed.yml
name: Seed Database
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:      # Manual trigger

jobs:
  seed:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Seed Database
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python3 scripts/seed_database.py --org ruvnet
```

## Best Practices

### ✅ DO

- ✅ **Seed on first setup** - Provides immediate functionality
- ✅ **Use GitHub token** - Avoids rate limiting
- ✅ **Rescan periodically** - Keeps data fresh
- ✅ **Start with `--no-readmes`** - Faster initial seed
- ✅ **Add multiple sources** - Broader coverage
- ✅ **Backup before reseeding** - Safety first

### ❌ DON'T

- ❌ **Commit .env.local** - Contains your token
- ❌ **Seed without token** - Very slow, limited
- ❌ **Never rescan** - Data gets stale
- ❌ **Seed while Docker running** - May cause locks
- ❌ **Use massive limits initially** - Start small

## FAQ

### Q: Does seeding replace scanning?

A: **No.** Seeding pre-populates the database for immediate use. The scanning feature (when fully implemented) will continuously update repos in the background.

### Q: How often should I reseed?

A: **Weekly for development, monthly for production.** Or after major GitHub updates to repos you track.

### Q: Can I seed multiple users/orgs?

A: **Yes!** Just run the script multiple times with different `--org` parameters. All repos accumulate in the database.

### Q: Does it overwrite existing data?

A: **No.** It uses `INSERT OR REPLACE`, which updates existing repos and adds new ones. No data loss.

### Q: What if I want different default repos?

A: Edit `.env.local` and change `RUVSCAN_SOURCE_NAME` to your preferred GitHub user/org.

### Q: Can I seed private repos?

A: **Yes**, if your GitHub token has `repo` scope (not just `public_repo`). Add `--org your-private-org`.

### Q: Does seeding cost money?

A: **No.** It only uses the free GitHub API. Just stay within rate limits (5,000/hour with token).

### Q: Can I automate reseeding?

A: **Yes!** Use cron jobs, GitHub Actions, or systemd timers to periodically reseed.

## Summary

**Key Points:**
1. 🌱 **Seed on first setup** for immediate functionality
2. 🔄 **Rescan periodically** to keep data fresh
3. 🎯 **Configure default in `.env.local`**
4. 📊 **Database tracks `last_scan`** timestamps
5. 🚀 **Use `--no-readmes` for speed**
6. 💾 **Backup before major changes**
7. 🔑 **Always use a GitHub token**

**Quick Commands:**
```bash
# First-time setup
python3 scripts/seed_database.py

# Regular rescan
python3 scripts/seed_database.py --no-readmes

# Add more repos
python3 scripts/seed_database.py --org openai --limit 30
```

---

**Need help?** See [QUICK_START_LOCAL.md](../QUICK_START_LOCAL.md) or open an issue!
