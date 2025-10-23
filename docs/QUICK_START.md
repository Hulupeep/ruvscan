# RuvScan Quick Start Guide

Get RuvScan up and running in 5 minutes!

## Prerequisites

- **Docker & Docker Compose** (recommended) OR
- **Python 3.11+**, **Rust 1.75+**, **Go 1.21+** (for manual setup)
- **GitHub Personal Access Token** ([Create one here](https://github.com/settings/tokens))
- **OpenAI API Key** (optional, for embeddings)

## Option 1: Docker (Recommended)

### 1. Clone and Setup

```bash
git clone https://github.com/ruvnet/ruvscan.git
cd ruvscan

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` and add your tokens:

```bash
GITHUB_TOKEN=ghp_your_github_token_here
OPENAI_API_KEY=sk-your_openai_key_here
```

### 3. Start All Services

```bash
# Build and start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

That's it! RuvScan is now running at `http://localhost:8000`

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# List MCP tools
curl http://localhost:8000/mcp/tools

# Scan a GitHub org
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"source_type":"org","source_name":"ruvnet","limit":10}'

# Query for leverage
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"intent":"How can I speed up my AI context system?"}'
```

## Option 2: Manual Setup

### 1. Clone and Setup

```bash
git clone https://github.com/ruvnet/ruvscan.git
cd ruvscan

# Run setup script
bash scripts/setup.sh
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your tokens
```

### 3. Start Services Manually

**Terminal 1 - Rust Engine:**
```bash
cd src/rust
cargo run --release
```

**Terminal 2 - Python MCP Server:**
```bash
python -m uvicorn src.mcp.server:app --reload
```

**Terminal 3 - Go Scanner (optional):**
```bash
cd src/go/scanner
export RUVSCAN_SOURCE_TYPE=org
export RUVSCAN_SOURCE_NAME=ruvnet
go run main.go
```

## Using the CLI

### Scan a GitHub Organization

```bash
./scripts/ruvscan scan org ruvnet --limit 20
```

### Query for Leverage

```bash
./scripts/ruvscan query "How can I optimize my AI context retrieval?"
```

### Compare Repositories

```bash
./scripts/ruvscan compare ruvnet/sublinear-time-solver ruvnet/FACT
```

### List Saved Leverage Cards

```bash
./scripts/ruvscan cards --limit 10 --min-score 0.7
```

## Integration with Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ruvscan": {
      "command": "docker",
      "args": ["run", "-p", "8000:8000", "ruvscan/mcp-server"]
    }
  }
}
```

Or for local installation:

```json
{
  "mcpServers": {
    "ruvscan": {
      "command": "python",
      "args": ["-m", "uvicorn", "src.mcp.server:app", "--host", "0.0.0.0", "--port", "8000"],
      "cwd": "/path/to/ruvscan"
    }
  }
}
```

## Example Queries

### Find Performance Tools
```bash
./scripts/ruvscan query "Find tools for optimizing real-time performance"
```

### Discover Context Management Solutions
```bash
./scripts/ruvscan query "How can I improve context memory in my LLM application?"
```

### Search for Sublinear Algorithms
```bash
./scripts/ruvscan query "What are the best sublinear algorithms for similarity search?"
```

## Troubleshooting

### Docker Issues

```bash
# Reset everything
docker-compose down
docker-compose up --build -d

# Check logs
docker-compose logs -f mcp-server
docker-compose logs -f rust-engine
docker-compose logs -f scanner
```

### Python Issues

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.11+
```

### Rust Build Issues

```bash
cd src/rust
cargo clean
cargo build --release
```

### Database Issues

```bash
# Reinitialize database
rm data/ruvscan.db
make init-db
```

## Next Steps

1. **Scan Your Organization**
   ```bash
   ./scripts/ruvscan scan org YOUR_ORG_NAME --limit 50
   ```

2. **Explore the API**
   - Visit `http://localhost:8000/docs` for interactive API docs
   - Check out `docs/api/MCP_PROTOCOL.md` for MCP integration

3. **Customize Configuration**
   - Edit `config/config.yaml` for advanced settings
   - Adjust Rust engine parameters
   - Configure SAFLA reasoning domains

4. **Integrate with Your Workflow**
   - Add to Claude Desktop
   - Use with TabStax
   - Call from your custom agents

## Support

- **Documentation**: `/docs` folder
- **Issues**: [GitHub Issues](https://github.com/ruvnet/ruvscan/issues)
- **Discord**: Join the Ruvnet community

## Performance Tips

1. **Use Docker** - Optimized for production
2. **Enable Caching** - FACT cache speeds up repeated queries
3. **Batch Scans** - Scan multiple orgs in parallel
4. **Tune Distortion** - Lower = more accurate, higher = faster (default: 0.5)

Happy scanning! 🧠🚀
