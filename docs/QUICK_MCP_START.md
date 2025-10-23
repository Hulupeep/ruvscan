# ⚡ Quick MCP Setup (30 Seconds)

Get RuvScan working in Claude Code CLI or Claude Desktop in under a minute.

## For Claude Code CLI

```bash
# 1. Start backend (one-time setup)
git clone https://github.com/ruvnet/ruvscan.git
cd ruvscan
docker compose up -d

# 2. Install MCP server
claude mcp add ruvscan \
  --scope user \
  --env GITHUB_TOKEN=ghp_your_token_here \
  -- uvx ruvscan-mcp

# 3. Start using it!
claude
> Scan the anthropics organization
> Find tools that could help me build real-time AI applications
```

## For Claude Desktop

### 1. Start Backend (One-Time)
```bash
git clone https://github.com/ruvnet/ruvscan.git
cd ruvscan
docker compose up -d
```

### 2. Add to Claude Desktop

**macOS:**
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```powershell
code %APPDATA%\Claude\claude_desktop_config.json
```

**Add this:**
```json
{
  "mcpServers": {
    "ruvscan": {
      "command": "uvx",
      "args": ["ruvscan-mcp"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

### 3. Restart Claude Desktop

Quit completely (Cmd+Q on Mac) and reopen.

## Test It

In Claude, try:
- "Scan the openai GitHub organization"
- "Find me tools for building real-time collaborative editors"
- "Compare facebook/react vs vuejs/core"

## What You Get

RuvScan gives Claude 4 powerful tools:

1. **`scan_github`** - Scan any GitHub org/user/topic
2. **`query_leverage`** - Find relevant tools & libraries
3. **`compare_repositories`** - Compare repos with O(log n) similarity
4. **`analyze_reasoning`** - See the reasoning chain (FACT cache)

## Need More Help?

📖 **Full Guide:** [MCP_INSTALL.md](MCP_INSTALL.md)
🐛 **Troubleshooting:** [MCP_INSTALL.md#troubleshooting](MCP_INSTALL.md#troubleshooting)
📚 **Main README:** [../README.md](../README.md)

---

**That's it!** You now have an AI that can discover GitHub tools with sublinear intelligence. 🚀
