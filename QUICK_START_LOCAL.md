# 🚀 RuvScan Local Quick Start

## Current Status ✅

Your RuvScan instance is running at: **http://localhost:8000**

### Services Status
- ✅ **MCP Server** (Python) - Running on port 8000
- ✅ **Scanner** (Go) - Running on port 8081
- ⚠️ **Rust Engine** - Needs attention (not critical)

## Quick Commands

### Check Status
```bash
# Check all containers
docker compose ps

# Check health
curl http://localhost:8000/health

# View logs
docker compose logs -f mcp-server
docker compose logs -f scanner
```

### API Usage

#### 1. Query for Solutions
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "How can I optimize my database queries?",
    "max_results": 5,
    "min_score": 0.7
  }' | jq '.'
```

#### 2. Scan GitHub Organization
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "org",
    "source_name": "vercel",
    "limit": 10
  }' | jq '.'
```

#### 3. Compare Repositories
```bash
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{
    "repo_a": "facebook/react",
    "repo_b": "vuejs/core"
  }' | jq '.'
```

#### 4. Get Leverage Cards
```bash
curl -s http://localhost:8000/cards?limit=10 | jq '.'
```

### Web UI

- **API Documentation**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## Claude Code Integration

### Install MCP Server
```bash
claude mcp add ruvscan \
  --scope user \
  --env RUVSCAN_API_URL=http://localhost:8000 \
  --env GITHUB_TOKEN=ghp_your_github_token_here \
  -- uvx ruvscan-mcp
```

### Verify Installation
```bash
claude mcp list
```

### Use in Claude Code
```bash
claude

# Then ask questions like:
> Scan the anthropics organization
> Find tools for optimizing React performance
> Compare NextJS vs Remix
> Why did you recommend that library?
```

## Container Management

### Start/Stop Services
```bash
# Start all
docker compose up -d

# Stop all
docker compose down

# Restart specific service
docker compose restart mcp-server

# View logs
docker compose logs -f
```

### Rebuild After Changes
```bash
# Rebuild all
docker compose build

# Rebuild specific service
docker compose build mcp-server

# Restart after rebuild
docker compose up -d
```

## Troubleshooting

### Rust Engine Not Starting
The Rust engine is optional. The Python MCP server works without it. To fix:

```bash
# Check logs
docker compose logs rust-engine

# Rebuild Rust engine
cd src/rust
cargo build --release
cd ../..
docker compose build rust-engine
docker compose restart rust-engine
```

### Port Already in Use
```bash
# Check what's using port 8000
lsof -ti:8000

# Kill the process
lsof -ti:8000 | xargs kill -9

# Restart RuvScan
docker compose restart
```

### Database Issues
```bash
# Check database
ls -lh data/ruvscan.db

# Reset database (⚠️ deletes all data)
rm data/ruvscan.db
docker compose restart mcp-server
```

## Environment Variables

Your config is in `.env.local`:

```bash
# View current config
cat .env.local

# Edit config
nano .env.local

# Restart to apply changes
docker compose restart
```

## Database Location

SQLite database: `data/ruvscan.db`

```bash
# Check size
du -h data/ruvscan.db

# Backup
cp data/ruvscan.db data/ruvscan.db.backup

# Restore
cp data/ruvscan.db.backup data/ruvscan.db
docker compose restart
```

## Useful Queries

### Find Performance Tools
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"intent": "performance optimization tools"}' | jq '.'
```

### Find Real-time Collaboration Tools
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"intent": "real-time collaboration frameworks"}' | jq '.'
```

### Scan Popular Organizations
```bash
# OpenAI
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"source_type": "org", "source_name": "openai", "limit": 20}'

# Vercel
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"source_type": "org", "source_name": "vercel", "limit": 20}'

# Meta
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"source_type": "org", "source_name": "facebook", "limit": 20}'
```

## Monitoring

### Check Resource Usage
```bash
# Docker stats
docker stats

# Disk usage
docker system df
```

### View Real-time Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f mcp-server

# Last 100 lines
docker compose logs --tail 100 mcp-server
```

## Documentation

- Main README: `README.md`
- Architecture: `docs/ARCHITECTURE.md`
- API Docs: http://localhost:8000/docs
- MCP Install Guide: `docs/MCP_INSTALL.md`

## Support

- GitHub Issues: https://github.com/ruvnet/ruvscan/issues
- Documentation: `docs/` folder
- Examples: `examples/` folder

---

**Happy Scanning! 🚀**
