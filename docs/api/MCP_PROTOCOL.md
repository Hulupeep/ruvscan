# RuvScan MCP Protocol Documentation

## Overview

RuvScan implements the Model Context Protocol (MCP) to provide sublinear-intelligence scanning as a service that can be integrated with AI agents, IDEs, and other tools.

## MCP Endpoints

### `/mcp/tools` - List Available Tools

Returns the list of available MCP tools.

**Request:**
```http
GET /mcp/tools
```

**Response:**
```json
{
  "tools": [
    {
      "name": "scan",
      "description": "Scan GitHub org/user/topic for repos",
      "inputSchema": {
        "type": "object",
        "properties": {
          "source_type": {"type": "string", "enum": ["org", "user", "topic"]},
          "source_name": {"type": "string"},
          "limit": {"type": "integer", "default": 50}
        },
        "required": ["source_type", "source_name"]
      }
    }
  ]
}
```

## Tool Endpoints

### `/scan` - Scan GitHub Repositories

Initiates a scan of GitHub repositories for a given org, user, or topic.

**Request:**
```http
POST /scan
Content-Type: application/json

{
  "source_type": "org",
  "source_name": "ruvnet",
  "limit": 50
}
```

**Response:**
```json
{
  "status": "initiated",
  "source_type": "org",
  "source_name": "ruvnet",
  "estimated_repos": 50,
  "message": "Scan initiated - workers processing in background"
}
```

### `/query` - Query for Leverage

Queries for leverage cards based on user intent using sublinear similarity.

**Request:**
```http
POST /query
Content-Type: application/json

{
  "intent": "How can I speed up context recall in my AI system?",
  "max_results": 10,
  "min_score": 0.7
}
```

**Response:**
```json
[
  {
    "repo": "ruvnet/sublinear-time-solver",
    "capabilities": ["O(log n) solving", "WASM acceleration"],
    "summary": "TRUE O(log n) matrix solver",
    "outside_box_reasoning": "Could accelerate context similarity by...",
    "integration_hint": "Use as MCP tool via npx",
    "relevance_score": 0.92,
    "runtime_complexity": "O(log n)",
    "cached": true
  }
]
```

### `/compare` - Compare Repositories

Compares two repositories using sublinear algorithm.

**Request:**
```http
POST /compare
Content-Type: application/json

{
  "repo_a": "ruvnet/sublinear-time-solver",
  "repo_b": "ruvnet/FACT"
}
```

**Response:**
```json
{
  "repo_a": "ruvnet/sublinear-time-solver",
  "repo_b": "ruvnet/FACT",
  "similarity_score": 0.85,
  "complexity": "O(log n)",
  "analysis": "Both focus on deterministic computation..."
}
```

### `/analyze` - Analyze Reasoning Chain

Analyzes and replays the reasoning chain using FACT cache.

**Request:**
```http
POST /analyze
Content-Type: application/json

{
  "repo": "ruvnet/sublinear-time-solver"
}
```

**Response:**
```json
{
  "repo": "ruvnet/sublinear-time-solver",
  "reasoning_trace": [
    {
      "step": "extraction",
      "description": "Extracted capabilities from README"
    },
    {
      "step": "similarity",
      "description": "Computed O(log n) semantic similarity"
    }
  ],
  "cached": true
}
```

### `/cards` - List Leverage Cards

Lists saved leverage cards with optional filtering.

**Request:**
```http
GET /cards?limit=50&min_score=0.7&cached_only=false
```

**Response:**
```json
{
  "cards": [...],
  "total": 42,
  "limit": 50
}
```

## Integration Examples

### Claude Desktop

Add to `claude_desktop_config.json`:

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

### TabStax

```javascript
const ruvscan = await mcp.connect("http://localhost:8000");

const results = await ruvscan.call("query", {
  intent: "Find tools for optimizing AI context",
  max_results: 5
});
```

### CLI

```bash
./scripts/ruvscan query "Find performance optimization tools"
```

## Error Handling

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `400 Bad Request` - Invalid input
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message"
}
```

## Rate Limiting

Currently no rate limiting implemented. Future versions will include:
- Per-client rate limits
- Token bucket algorithm
- Configurable limits

## Authentication

Currently no authentication required. Future versions will support:
- API keys
- JWT tokens
- OAuth 2.0
