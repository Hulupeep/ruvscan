# 🖥️ RuvScan Examples for Claude Desktop

Visual guide showing how to use RuvScan with Claude Desktop application.

## 🚀 Setup Overview

### What You'll See

When RuvScan is properly configured in Claude Desktop, you'll see:

1. **🔌 MCP Server Indicator** - A small icon showing "ruvscan" is connected
2. **🛠️ Available Tools** - 4 new tools Claude can use:
   - `scan_github` - Scan organizations/users/topics
   - `query_leverage` - Find relevant tools by intent
   - `compare_repositories` - Compare repos with sublinear similarity
   - `analyze_reasoning` - View FACT cache reasoning chains

---

## 📸 Example 1: Finding Performance Solutions

### User Message:
```
I'm building a real-time AI chatbot and the vector database
queries are taking 2-3 seconds per message. What can I do?
```

### What Claude Does:

1. **Understands the problem**: Slow O(n) vector search
2. **Uses `query_leverage` tool** with intent: "optimize vector database query performance"
3. **Returns relevant repositories** with high relevance scores

### Claude's Response:

```
I found several solutions for your vector database performance issue:

📦 ruvnet/sublinear-time-solver
Relevance Score: 0.94
Complexity: O(log n)

Why This Helps:
You're doing O(n) linear search through all vectors. This library
uses Johnson-Lindenstrauss projection to reduce your vector
dimensions from 1536 → O(log n), making similarity search
600× faster with minimal accuracy loss (<3%).

Installation:
pip install sublinear-solver

Quick Integration:
```python
from sublinear_solver import JLProjection

# One-time setup
jl = JLProjection(input_dim=1536, distortion=0.5)

# Compress your embeddings
compressed_vectors = jl.project_batch(your_vectors)

# Now search is O(log n) instead of O(n)!
similarities = jl.similarity_search(query_vector, compressed_vectors)
```

Speedup: 600× for 10,000 vectors
Accuracy: >97% preserved
```

### User Follow-up:
```
Can I also cache the results?
```

### Claude Uses Tools Again:

**Tool:** `query_leverage` with intent: "cache vector database queries"

### Response:

```
📦 ruvnet/FACT
Relevance Score: 0.89

FACT provides deterministic caching with SHA256 hashing.
Every query gets cached, so repeated similar questions
return instantly.

Combined approach for maximum speed:
1. O(n) → O(log n) with sublinear-time-solver (600× faster)
2. O(log n) → O(1) with FACT cache (instant for repeats)

Total speedup: 10,000× for cached queries!
```

---

## 📸 Example 2: Discovering New Technologies

### User Message:
```
I keep hearing about "collaborative text editing with CRDTs"
but I don't know where to start. Can you find some repos?
```

### What Claude Does:

1. **Uses `scan_github` tool** with topic: "crdt"
2. **Scans GitHub** finding 50+ repositories
3. **Uses `query_leverage` tool** to filter for educational/practical repos

### Claude's Response:

```
I scanned GitHub for CRDT repositories and found several excellent ones:

📚 Educational:
1. yjs/yjs
   - Most popular CRDT library (12k+ stars)
   - Powers collaborative editors like Notion
   - Excellent documentation
   - Live demos available

2. automerge/automerge
   - Pure CRDT implementation
   - Great for understanding the theory
   - JSON-like data structures

🏗️ Production-Ready:
3. ruvnet/MidStream
   - Real-time collaborative infrastructure
   - Built-in CRDT support
   - Handles 1000+ concurrent editors

Would you like me to compare any of these?
```

### User Follow-up:
```
Yes, compare yjs with automerge
```

### Claude Uses Compare Tool:

**Tool:** `compare_repositories` - "yjs/yjs" vs "automerge/automerge"

### Response:

```
Comparing: yjs/yjs vs automerge/automerge
Similarity Score: 0.78 (both are CRDT libraries)

yjs/yjs:
✅ Faster (more optimized)
✅ Better for real-time apps
✅ WebSocket + WebRTC support
✅ Monaco/CodeMirror bindings
❌ Less portable (JavaScript focused)

automerge/automerge:
✅ More portable (Rust + WASM)
✅ Better for understanding CRDTs
✅ Simpler API
✅ Strong consistency guarantees
❌ Slower for real-time (more overhead)

Recommendation:
- Learning CRDTs? Start with Automerge
- Building real-time app? Use Yjs
```

---

## 📸 Example 3: Building a New Feature

### User Message:
```
I need to add real-time presence (like Google Docs) to my
React app. What libraries should I use?
```

### What Claude Does:

**Tool 1:** `query_leverage` - "real-time presence library react"
**Tool 2:** `scan_github` - org: "liveblocks"
**Tool 3:** `query_leverage` - "websocket real-time collaboration"

### Claude's Response:

```
I found several options for real-time presence:

🎨 Complete Solution:
📦 liveblocks/liveblocks
Relevance: 0.92

Includes:
- Live cursors
- User presence indicators
- Comments system
- Notifications
- Beautiful UI components

```tsx
import { useOthers } from "@liveblocks/react";

function Presence() {
  const others = useOthers();

  return (
    <div>
      {others.map(user => (
        <Cursor key={user.id} position={user.cursor} />
      ))}
    </div>
  );
}
```

🔧 DIY Solution:
📦 yjs/yjs + y-webrtc
Relevance: 0.85

More control, free, open-source:
```tsx
import * as Y from 'yjs'
import { WebrtcProvider } from 'y-webrtc'

const doc = new Y.Doc()
const provider = new WebrtcProvider('room-name', doc)

// Share presence
const awareness = provider.awareness
awareness.setLocalState({ cursor: { x, y } })
```

Want me to scan the Liveblocks org for more tools?
```

### User Says:
```
Yes, scan liveblocks
```

### Claude Uses Scan Tool:

**Tool:** `scan_github` - org: "liveblocks"

### Response:

```
Scanned liveblocks organization (12 repositories found)

Notable Projects:
1. liveblocks/liveblocks - Main library
2. liveblocks/liveblocks-examples - 20+ example apps
3. liveblocks/liveblocks-starter-kit - Quick start templates

Example Apps Found:
✅ Next.js + Liveblocks
✅ React + Liveblocks
✅ Vue + Liveblocks
✅ Collaborative Figma clone
✅ Collaborative code editor
✅ Collaborative whiteboard

You can clone any of these as a starting point!
```

---

## 📸 Example 4: Optimizing Existing Code

### User Message:
```
Here's my function - it's too slow:

def search_similar_docs(query, docs):
    results = []
    for doc in docs:
        score = calculate_similarity(query, doc)
        if score > 0.7:
            results.append((doc, score))
    return sorted(results, key=lambda x: x[1], reverse=True)
```

### What Claude Does:

**Tool:** `query_leverage` - "optimize similarity search O(n) performance"

### Claude's Response:

```
Your function is O(n) - it checks every document. Here's how to fix it:

📦 ruvnet/sublinear-time-solver
Relevance: 0.96

Transform to O(log n):

```python
from sublinear_solver import JLProjection, sublinear_similarity

# Setup (once at startup)
jl = JLProjection(input_dim=len(query), distortion=0.5)
compressed_docs = jl.project_batch(docs)

# Optimized search - O(log n)
def search_similar_docs_fast(query, docs):
    compressed_query = jl.project(query)
    similarities = sublinear_similarity(
        compressed_query,
        compressed_docs,
        threshold=0.7
    )
    return similarities  # Already sorted!
```

Performance Improvement:
- 1,000 docs: 300× faster
- 10,000 docs: 600× faster
- 100,000 docs: 1,200× faster

Accuracy: >97% (adjustable via distortion parameter)

Want me to find caching solutions too?
```

---

## 📸 Example 5: Learning Architecture Patterns

### User Message:
```
I'm learning about database architectures. Can you scan some
major database projects and explain the patterns?
```

### What Claude Does:

**Tool 1:** `scan_github` - org: "cockroachdb"
**Tool 2:** `scan_github` - org: "mongodb"
**Tool 3:** `scan_github` - org: "redis"
**Tool 4:** `query_leverage` - "database architecture patterns"

### Claude's Response:

```
I scanned 3 major database organizations (200+ repos indexed).
Here are the key architecture patterns:

1. Distributed SQL (CockroachDB)
   Architecture: Raft consensus + SQL layer
   Use Case: Need ACID + horizontal scaling
   Repository: cockroachdb/cockroach

2. Document Store (MongoDB)
   Architecture: Sharding + replica sets
   Use Case: Flexible schemas, JSON documents
   Repository: mongodb/mongo

3. In-Memory Key-Value (Redis)
   Architecture: Single-threaded event loop
   Use Case: Caching, real-time data
   Repository: redis/redis

Would you like me to compare any two of these?
```

### User Follow-up:
```
Compare MongoDB vs Redis for a real-time leaderboard
```

### Claude Uses Compare Tool:

**Tool:** `compare_repositories` - "mongodb/mongo" vs "redis/redis"

### Response:

```
For a real-time leaderboard:

redis/redis wins for this use case:

Redis:
✅ Sub-millisecond latency
✅ Built-in sorted sets (perfect for leaderboards)
✅ Atomic increment operations
✅ Pub/sub for live updates
Performance: Handle 100k+ updates/sec

MongoDB:
❌ Slower (disk-based, 10-50ms latency)
❌ Need custom indexes
❌ No built-in leaderboard structures
Performance: ~5k updates/sec

Code Example with Redis:
```python
# Add score
redis.zadd('leaderboard', {user_id: score})

# Get top 10
top_10 = redis.zrevrange('leaderboard', 0, 9, withscores=True)

# Get user rank
rank = redis.zrevrank('leaderboard', user_id)
```

Recommendation: Use Redis for leaderboards, MongoDB for user profiles.
```

---

## 📸 Example 6: Multi-Step Discovery

### User Message:
```
I want to build a Figma-like collaborative design tool.
What do I need?
```

### What Claude Does (Multiple Tools):

1. **`query_leverage`** - "collaborative canvas library"
2. **`query_leverage`** - "CRDT real-time sync"
3. **`query_leverage`** - "vector graphics rendering web"
4. **`scan_github`** - topic: "collaborative-editing"

### Claude's Response:

```
Building a collaborative design tool requires 3 main components:

🎨 1. Canvas/Graphics Layer:
📦 tldraw/tldraw (Relevance: 0.93)
- Infinite canvas
- Vector graphics
- Built-in collaboration support
- React components

📦 fabricjs/fabric.js (Relevance: 0.89)
- HTML5 canvas library
- Rich graphics primitives
- Good performance

🔄 2. Real-Time Sync:
📦 yjs/yjs (Relevance: 0.95)
- CRDT for conflict-free collaboration
- WebRTC or WebSocket transport
- Works offline

📦 ruvnet/MidStream (Relevance: 0.88)
- Built for collaborative apps
- Handles 1000+ concurrent users
- Low latency

👥 3. Presence & Cursors:
📦 liveblocks/liveblocks (Relevance: 0.90)
- Live cursors
- User avatars
- Comments system

Recommended Stack:
- Frontend: tldraw (has collaboration built-in)
- Sync: Yjs (free, proven)
- Backend: Your own Node.js server

Quick Start:
```bash
npm install @tldraw/tldraw yjs y-websocket
```

Want me to find example implementations?
```

---

## 🎯 UI Indicators in Claude Desktop

### When RuvScan is Working:

You'll see Claude's responses include:

**1. Tool Usage Indicators:**
```
🔧 Using scan_github...
🔍 Using query_leverage...
⚖️ Using compare_repositories...
🧠 Using analyze_reasoning...
```

**2. Structured Results:**
```
📦 Repository Name
Relevance Score: 0.XX
Complexity: O(...)

[Detailed explanation]
```

**3. Code Examples:**
Claude will often provide ready-to-use code snippets based on the repositories found.

---

## 💡 Pro Tips for Claude Desktop

### 1. Chain Discoveries
```
User: Scan the vercel organization, then find tools related to edge computing
```
Claude will execute both operations in sequence.

### 2. Ask for Reasoning
```
User: Why did you recommend that specific library?
```
Claude will use the `analyze_reasoning` tool to show the FACT cache decision chain.

### 3. Compare Multiple Options
```
User: Compare React, Vue, and Svelte
```
Claude will use `compare_repositories` multiple times.

### 4. Iterate on Solutions
```
User: That's good, but I need Python instead of JavaScript
```
Claude will use `query_leverage` again with updated context.

---

## 🎨 Visual Flow

Here's how a typical session looks:

```
┌─────────────────────────────────────┐
│  You: "Find tools for X"            │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  🔧 Claude uses query_leverage      │
│  🔍 Searches RuvScan index          │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  📦 Results with relevance scores   │
│  💡 Explanations                    │
│  💻 Code examples                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  You: "Compare A vs B"              │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  ⚖️ Claude uses compare_repos       │
│  📊 Shows similarity scores         │
│  ✅❌ Lists pros/cons               │
└─────────────────────────────────────┘
```

---

## 🚀 Getting Started

### First Conversation:

Start simple to test the setup:

```
You: Scan the anthropics organization
```

Claude should respond with a list of Anthropic's repositories.

### Then Try a Real Problem:

```
You: I'm building [describe your project]. What tools
could help with [specific challenge]?
```

Claude will use RuvScan's tools to find relevant solutions.

---

## 📚 More Examples

See also:
- **[Claude Code CLI Examples](CLAUDE_CODE_EXAMPLES.md)** - Terminal-based examples
- **[MCP Install Guide](MCP_INSTALL.md)** - Full installation instructions
- **[Quick Reference](MCP_QUICK_REFERENCE.md)** - Command quick reference

---

## 🔧 Troubleshooting

### "RuvScan tools not showing up"

1. Check config file syntax (must be valid JSON)
2. Restart Claude Desktop completely (Cmd+Q on Mac)
3. Check logs: `~/Library/Logs/Claude/mcp*.log`

### "Connection errors"

1. Verify backend is running: `curl http://localhost:8000/health`
2. Check docker-compose: `docker compose ps`
3. Restart backend: `docker compose restart`

### "No results found"

1. Scan some repos first: "Scan the openai organization"
2. Check GitHub token is valid
3. Try broader queries

---

**Ready to use RuvScan in Claude Desktop?**

1. ✅ Backend running: `docker compose up -d`
2. ✅ Config file updated with your GitHub token
3. ✅ Claude Desktop restarted
4. 🚀 Start discovering!

```
First message: "Scan the microsoft organization"
```
