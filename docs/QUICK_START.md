# 🚀 Quick Start Guide

Get RuvScan running in 5 minutes.

## Prerequisites

You've already set up `.env.local` with:
- `GITHUB_TOKEN` - Your GitHub Personal Access Token
- `OPENAI_API_KEY` - Your OpenAI API key

✅ Environment verified!

## Option 1: Docker (Recommended)

### Start All Services

```bash
# Using docker compose (newer)
docker compose up -d

# OR using docker-compose (older)
docker-compose up -d
```

This starts:
- **MCP Server** (Python/FastAPI) on port 8000
- **Rust Engine** (gRPC) on port 50051  
- **Go Scanner** (Workers) in background

### Verify Services

```bash
# Check health
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","version":"0.5.0"}
```

### Your First Scan

```bash
# Scan an organization's repositories
curl -X POST http://localhost:8000/scan \
  -H 'Content-Type: application/json' \
  -d '{
    "source_type": "org",
    "name": "ruvnet",
    "limit": 10
  }'
```

### Your First Query

```bash
# Ask RuvScan for leverage
curl -X POST http://localhost:8000/query \
  -H 'Content-Type: application/json' \
  -d '{
    "intent": "How can I optimize my AI application performance?",
    "max_results": 5,
    "min_score": 0.7
  }'
```

## Option 2: Manual (Development)

### 1. Install Dependencies

**Python:**
```bash
cd src/mcp
pip install -r requirements.txt
```

**Rust:**
```bash
cd src/rust
cargo build --release
```

**Go:**
```bash
cd src/go/scanner
go mod download
```

### 2. Start Services

**Terminal 1 - Rust Engine:**
```bash
cd src/rust
cargo run --release
# Runs on localhost:50051
```

**Terminal 2 - Python MCP Server:**
```bash
cd src/mcp
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
# Runs on localhost:8000
```

**Terminal 3 - Go Scanner (optional):**
```bash
cd src/go/scanner
go run main.go
```

### 3. Test It

```bash
# Health check
curl http://localhost:8000/health

# Scan repos
curl -X POST http://localhost:8000/scan \
  -H 'Content-Type: application/json' \
  -d '{"source_type":"user","name":"ruvnet","limit":5}'

# Query leverage
curl -X POST http://localhost:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"intent":"Speed up vector database","max_results":3}'
```

## Option 3: Using Helper Scripts

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Scan a user's repositories
./scripts/ruvscan scan user ruvnet --limit 10

# Query for leverage
./scripts/ruvscan query "How to build real-time collaboration features?"

# Compare two solutions
./scripts/ruvscan compare "vector-db-v1" "vector-db-v2"
```

## Common Operations

### View Scanned Repositories

```bash
# List all scanned repos
curl http://localhost:8000/repos
```

### Get Specific Leverage Card

```bash
# Get leverage card by ID
curl http://localhost:8000/leverage/{card_id}
```

### Check FACT Cache

```bash
# View cached reasoning
curl http://localhost:8000/cache/stats
```

## Monitoring

### View Logs

**Docker:**
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f mcp-server
docker compose logs -f rust-engine
docker compose logs -f scanner
```

**Manual:**
Check terminal outputs for each service.

### Check Service Health

```bash
# MCP Server health
curl http://localhost:8000/health

# Rust Engine health (if exposed)
curl http://localhost:50051/health
```

## Troubleshooting

### Port Already in Use

```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml or .env
```

### Services Won't Start

```bash
# View detailed logs
docker compose logs

# Restart services
docker compose restart

# Rebuild if needed
docker compose build --no-cache
docker compose up -d
```

### API Key Issues

```bash
# Verify .env.local
cat .env.local

# Should contain:
# GITHUB_TOKEN=ghp_...
# OPENAI_API_KEY=sk-...
```

### Database Issues

```bash
# Reset database
rm -f data/ruvscan.db
docker compose restart mcp-server
```

## Next Steps

1. **Read the Full README** - [README.md](../README.md)
2. **Explore User Experience** - [USER_EXPERIENCE.md](USER_EXPERIENCE.md)
3. **Contribute** - [CONTRIBUTING.md](../CONTRIBUTING.md)
4. **Check Examples** - [examples/](../examples/)

## Getting Help

- **Issues**: https://github.com/Hulupeep/ruvscan/issues
- **Discussions**: https://github.com/Hulupeep/ruvscan/discussions
- **Documentation**: All docs in `docs/` folder

---

**Ready to discover leverage?** 🚀
