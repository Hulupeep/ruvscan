# 🔌 RuvScan MCP Server Installation

RuvScan integrates seamlessly with Claude Code CLI, Codex, and Claude Desktop as an MCP (Model Context Protocol) server.

## 📋 Prerequisites

Before installing RuvScan as an MCP server, you need the backend API running:

```bash
# Clone and start RuvScan API
git clone https://github.com/ruvnet/ruvscan.git
cd ruvscan
cp .env.example .env
# Add your GITHUB_TOKEN to .env

# Start with Docker
docker compose up -d

# Verify it's running
curl http://localhost:8000/health
```

## 🚀 Installation Methods

### Method 1: Claude Code CLI (Recommended)

The easiest way to add RuvScan to Claude Code:

```bash
# Install from PyPI
claude mcp add ruvscan \
  --scope user \
  --env RUVSCAN_API_URL=http://localhost:8000 \
  --env GITHUB_TOKEN=ghp_your_token_here \
  -- uvx ruvscan-mcp
```

**Options:**
- `--scope user` - Available across all your projects
- `--scope project` - Only for current project (creates `.mcp.json`)
- `--scope local` - Local to this directory only

Verify installation:
```bash
claude mcp list
```

### Method 2: Claude Desktop (macOS/Windows)

#### Step 1: Install uv (if not already installed)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Step 2: Configure Claude Desktop

**macOS:**
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
code %APPDATA%\Claude\claude_desktop_config.json
```

Add this configuration:

```json
{
  "mcpServers": {
    "ruvscan": {
      "command": "uvx",
      "args": ["ruvscan-mcp"],
      "env": {
        "RUVSCAN_API_URL": "http://localhost:8000",
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

#### Step 3: Restart Claude Desktop

**macOS:** Quit completely with `Cmd+Q`
**Windows:** Exit from system tray

### Method 3: Local Development Setup

For local development or if you want to run from source:

**macOS/Linux:**
```json
{
  "mcpServers": {
    "ruvscan": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/ruvscan",
        "run",
        "src/mcp/mcp_stdio_server.py"
      ],
      "env": {
        "RUVSCAN_API_URL": "http://localhost:8000",
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "ruvscan": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\ABSOLUTE\\PATH\\TO\\ruvscan",
        "run",
        "src\\mcp\\mcp_stdio_server.py"
      ],
      "env": {
        "RUVSCAN_API_URL": "http://localhost:8000",
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

### Method 4: Project-Specific (.mcp.json)

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "ruvscan": {
      "command": "uvx",
      "args": ["ruvscan-mcp"],
      "env": {
        "RUVSCAN_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

**Note:** GITHUB_TOKEN can be in your `.env` file instead of `.mcp.json` for security.

## 🧪 Testing Your Installation

### In Claude Desktop

1. Open Claude Desktop
2. Look for the tools icon (🔧) in the chat interface
3. You should see 4 RuvScan tools listed:
   - `scan_github` - Scan GitHub org/user/topic
   - `query_leverage` - Find leverage opportunities
   - `compare_repositories` - Compare two repos
   - `analyze_reasoning` - Analyze reasoning chains

### In Claude Code CLI

```bash
# Start a chat
claude

# Test the tools
> Can you scan the openai organization for me?
> What leverage can I find for "building real-time AI apps"?
> Compare facebook/react vs vuejs/core
```

### Test Commands

Try these in Claude:

```
1. "Scan the anthropics GitHub organization"
   → Uses: scan_github tool

2. "Find tools that could help me build a real-time collaborative editor"
   → Uses: query_leverage tool

3. "Compare facebook/react and vuejs/core"
   → Uses: compare_repositories tool

4. "Show me the reasoning for why you recommended that repo"
   → Uses: analyze_reasoning tool
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `RUVSCAN_API_URL` | RuvScan API endpoint | `http://localhost:8000` | No |
| `GITHUB_TOKEN` | GitHub Personal Access Token | None | Recommended |

### Scopes

- **`user`** - Available in all projects for your user
- **`project`** - Shared via `.mcp.json` in git
- **`local`** - Only in current directory, not in git

## 🐛 Troubleshooting

### Server Not Showing Up

**Check Claude's logs:**

**macOS:**
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

**Windows:**
```powershell
Get-Content $env:LOCALAPPDATA\Claude\logs\mcp*.log -Wait
```

**Common fixes:**
1. Verify absolute paths (not relative)
2. Restart Claude Desktop completely (Cmd+Q/Exit)
3. Check JSON syntax in config file
4. Ensure RuvScan API is running: `curl http://localhost:8000/health`

### Tools Failing

**Check API connectivity:**
```bash
# Verify RuvScan API is accessible
curl http://localhost:8000/health

# Check Docker containers
docker compose ps

# View API logs
docker compose logs mcp-server
```

### GitHub Token Issues

**Error: `401 Unauthorized` or rate limiting**

1. Verify your GitHub token has correct permissions:
   - Go to https://github.com/settings/tokens
   - Token needs: `public_repo`, `read:org`, `read:user`

2. Update your configuration:
```bash
# For Claude Code CLI
claude mcp remove ruvscan
claude mcp add ruvscan --scope user --env GITHUB_TOKEN=ghp_new_token -- uvx ruvscan-mcp

# For Claude Desktop - edit config file and restart
```

### Connection Refused

**Error: `Connection refused to localhost:8000`**

Make sure the RuvScan API backend is running:

```bash
# Start the backend
cd ruvscan
docker compose up -d

# Verify it's running
curl http://localhost:8000/health
# Should return: {"status":"healthy","version":"0.5.0",...}
```

### No Results from Queries

**If `query_leverage` returns nothing:**

1. The database might be empty - scan some repos first:
```bash
# Via API
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "org",
    "source_name": "openai",
    "limit": 10
  }'

# Or via Claude
> Scan the openai GitHub organization
```

2. Wait for the scan to complete (check logs)
3. Try your query again

## 📚 Usage Examples

### Example 1: Find Performance Tools

**In Claude:**
```
I'm building an AI application and my context retrieval from the vector
database is too slow. Can you help me find tools that could speed this up?
```

**RuvScan will:**
1. Query for relevant repos
2. Find sublinear algorithms
3. Suggest creative solutions from other domains
4. Explain how to integrate them

### Example 2: Scan and Discover

**In Claude:**
```
Scan the anthropics organization and then show me what AI tools they have
that could help with prompt engineering
```

**RuvScan will:**
1. Scan all Anthropics repos
2. Filter for prompt engineering tools
3. Show leverage opportunities
4. Explain integration

### Example 3: Compare Frameworks

**In Claude:**
```
I'm trying to choose between FastAPI and Flask for my new API.
Can you compare them for me?
```

**RuvScan will:**
1. Compare the repositories
2. Show similarity scores
3. Highlight key differences
4. Suggest which fits your use case

## 🔗 Integration with Your Workflow

### With VS Code + Claude Code

1. Install Claude Code extension
2. Configure RuvScan MCP server
3. As you code, ask Claude about tools:
   ```
   > What libraries could help me optimize this database query?
   ```

### With Cursor

Same configuration as Claude Desktop - add to Cursor's MCP settings.

### With Codex

Add RuvScan to your Codex MCP configuration.

## 📖 Learn More

- **[Main README](../README.md)** - Full project documentation
- **[API Reference](../docs/API.md)** - HTTP API documentation
- **[Architecture](../docs/ARCHITECTURE.md)** - How RuvScan works
- **[MCP Protocol](https://modelcontextprotocol.io)** - Model Context Protocol docs

## 🆘 Getting Help

- **Issues**: https://github.com/ruvnet/ruvscan/issues
- **Discussions**: https://github.com/ruvnet/ruvscan/discussions
- **MCP Docs**: https://docs.claude.com/mcp

---

**Quick Start Summary:**

```bash
# 1. Start RuvScan backend
docker compose up -d

# 2. Install MCP server
claude mcp add ruvscan --scope user --env GITHUB_TOKEN=ghp_token -- uvx ruvscan-mcp

# 3. Use in Claude
claude
> Scan the openai organization and find tools for real-time AI
```

🎉 **You're ready to discover sublinear leverage!**
