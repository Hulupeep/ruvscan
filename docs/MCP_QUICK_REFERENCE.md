# 📋 RuvScan MCP Quick Reference

One-page reference for using RuvScan as an MCP server.

## Installation Commands

### Claude Code CLI
```bash
claude mcp add ruvscan --scope user --env GITHUB_TOKEN=ghp_token -- uvx ruvscan-mcp
```

### Claude Desktop Config

**File Location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration:**
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

### Project-Specific (.mcp.json)
```json
{
  "mcpServers": {
    "ruvscan": {
      "command": "uvx",
      "args": ["ruvscan-mcp"]
    }
  }
}
```

## Available Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `scan_github` | Scan GitHub org/user/topic | "Scan the openai organization" |
| `query_leverage` | Find leverage opportunities | "Find tools for real-time AI" |
| `compare_repositories` | Compare two repos | "Compare react vs vue" |
| `analyze_reasoning` | Show reasoning chain | "Analyze reasoning for that repo" |

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `RUVSCAN_API_URL` | Backend API endpoint | `http://localhost:8000` | No |
| `GITHUB_TOKEN` | GitHub PAT | None | Recommended |

## Common Commands

### Start Backend
```bash
docker compose up -d
```

### Check Health
```bash
curl http://localhost:8000/health
```

### View Logs
```bash
# API logs
docker compose logs mcp-server

# Claude Desktop logs (macOS)
tail -f ~/Library/Logs/Claude/mcp*.log
```

### Restart Claude Desktop
- **macOS:** Cmd+Q and reopen
- **Windows:** Exit from system tray

## Quick Test

```
> Scan the anthropics organization and find tools for prompt engineering
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Server not showing up | Check JSON syntax, restart Claude |
| Tools failing | Verify backend is running: `curl localhost:8000/health` |
| No results | Scan repos first, check logs |
| 401 errors | Update `GITHUB_TOKEN` |

## Links

- **Full Install Guide:** [MCP_INSTALL.md](MCP_INSTALL.md)
- **Quick Start:** [QUICK_MCP_START.md](QUICK_MCP_START.md)
- **Main README:** [../README.md](../README.md)
- **MCP Protocol:** https://modelcontextprotocol.io

---

**Quick Copy-Paste:**

```bash
# 1. Backend
docker compose up -d

# 2. MCP Server
claude mcp add ruvscan --scope user --env GITHUB_TOKEN=ghp_token -- uvx ruvscan-mcp

# 3. Test
claude
> Scan the openai organization
```
