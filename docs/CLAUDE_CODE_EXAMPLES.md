# 💬 RuvScan Examples for Claude Code CLI

Real conversation examples showing how to use RuvScan with Claude Code CLI.

## 🎯 Example 1: Finding Performance Solutions

```bash
$ claude

You: I'm building an AI chatbot and the context retrieval is way too slow.
     Every message takes 2-3 seconds because I'm searching through thousands
     of previous messages. What can I do?

Claude: I'll search for tools that could help optimize your context retrieval...

        [Using query_leverage tool with intent: "optimize context retrieval performance AI chatbot"]

        Found several highly relevant solutions:

        📦 ruvnet/sublinear-time-solver (Relevance: 0.94)

        Why this helps: You're doing O(n) linear search through messages.
        This library uses Johnson-Lindenstrauss projection to reduce your
        vector dimensions from 1536 → O(log n), making similarity search
        600× faster with minimal accuracy loss (<3%).

        How to integrate:
        ```python
        from sublinear_solver import JLProjection

        # One-time setup
        jl = JLProjection(input_dim=1536, distortion=0.5)

        # Reduce your message embeddings
        compressed = jl.project(message_embeddings)

        # Now search in compressed space - O(log n)!
        ```

        Complexity: TRUE O(log n)

        Would you like me to scan for more caching solutions?

You: Yes, what about caching the results?

Claude: [Using query_leverage tool again]

        📦 ruvnet/FACT (Relevance: 0.89)

        Why this helps: FACT provides deterministic caching for LLM
        interactions. Every context retrieval gets hashed (SHA256) and
        cached. If a user asks something similar, instant response.

        How to integrate:
        ```python
        from fact import FACTCache

        cache = FACTCache()

        # Check cache before expensive retrieval
        cached = cache.get(query_hash)
        if cached:
            return cached

        # Do retrieval and cache it
        result = expensive_retrieval(query)
        cache.set(query_hash, result)
        ```

        This gives you 100% reproducibility and massive speed boost
        for repeated queries.
```

---

## 🔍 Example 2: Exploring New Technologies

```bash
$ claude

You: I keep hearing about "sublinear algorithms" but I don't really understand
     what they are or when to use them. Can you scan repos that use them and
     explain?

Claude: I'll scan for repositories focused on sublinear algorithms...

        [Using scan_github tool with topic: "sublinear algorithms"]

        Scanning GitHub for topic: sublinear algorithms
        Found 23 repositories. Processing...

        Now let me find the most educational ones...

        [Using query_leverage tool]

        📚 Top Educational Repositories:

        1. ruvnet/sublinear-time-solver
           - Complete implementation of multiple sublinear algorithms
           - Includes Johnson-Lindenstrauss, Random Projection, HyperLogLog
           - Has detailed explanations and benchmarks

        2. mit-algorithms/6.046-sublinear
           - MIT course materials
           - Theory and proofs
           - Problem sets with solutions

        What are sublinear algorithms?

        Sublinear means the algorithm's running time is less than O(n) - it
        doesn't need to look at all the data. Examples:

        - O(log n) - Binary search
        - O(√n) - Some approximation algorithms
        - O(1) - Hash lookups

        When to use them:
        - Massive datasets where O(n) is too slow
        - Approximation is acceptable (usually >97% accuracy)
        - Real-time requirements
        - Streaming data

        Want me to compare some of these implementations?

You: Yes, compare the MIT course repo with the ruvnet implementation

Claude: [Using compare_repositories tool]

        Comparing: mit-algorithms/6.046-sublinear vs ruvnet/sublinear-time-solver

        Similarity Score: 0.72

        MIT Course Repo:
        - ✅ Theoretical foundation & proofs
        - ✅ Educational problem sets
        - ❌ No production-ready code
        - ❌ No WASM or MCP integration

        Ruvnet Implementation:
        - ✅ Production-ready implementation
        - ✅ WASM for browser use
        - ✅ MCP integration for AI tools
        - ✅ Comprehensive benchmarks
        - ❌ Less theoretical explanation

        Recommendation: Learn theory from MIT repo, use ruvnet for
        actual implementation in your projects.
```

---

## 🏗️ Example 3: Building a New Project

```bash
$ claude

You: I want to build a collaborative code editor like Google Docs but for code.
     What libraries and tools should I look at?

Claude: Great project! Let me find relevant tools across different areas...

        [Using query_leverage tool multiple times for different aspects]

        🎨 Frontend/Editor Core:

        📦 microsoft/monaco-editor (Relevance: 0.91)
        - Powers VS Code
        - Syntax highlighting, IntelliSense
        - NPM: npm install monaco-editor

        📦 codemirror/dev (Relevance: 0.88)
        - Lightweight alternative
        - Excellent mobile support

        🔄 Real-time Synchronization:

        📦 yjs/yjs (Relevance: 0.95)
        - CRDT for conflict-free collaboration
        - Handles offline edits
        - Works with WebRTC, WebSocket

        📦 ruvnet/MidStream (Relevance: 0.87)
        - Real-time streaming architecture
        - Can handle thousands of concurrent editors
        - Built for low-latency

        🖥️ Backend:

        📦 liveblocks/liveblocks (Relevance: 0.89)
        - Complete collaboration infrastructure
        - Presence, cursors, comments
        - Hosted or self-hosted

        Want me to scan any of these organizations for more tools?

You: Scan the yjs organization

Claude: [Using scan_github tool]

        Scanning org: yjs
        Found 47 repositories...

        Notable discoveries:
        - y-websocket: WebSocket connector
        - y-webrtc: P2P WebRTC connector
        - y-indexeddb: Offline storage
        - y-monaco: Direct Monaco Editor binding

        You could use y-monaco + y-websocket for a quick MVP!

You: Perfect! Now compare yjs with liveblocks

Claude: [Using compare_repositories tool]

        yjs/yjs vs liveblocks/liveblocks

        Similarity: 0.81 (both solve real-time collab)

        Yjs:
        - ✅ Free, open-source
        - ✅ P2P option (no server needed)
        - ✅ Offline-first
        - ❌ You handle infrastructure
        - ❌ No built-in presence UI

        Liveblocks:
        - ✅ Hosted solution (easy setup)
        - ✅ Beautiful presence UI
        - ✅ Comments, notifications built-in
        - ❌ Paid after free tier
        - ❌ Vendor lock-in

        For MVP: Start with Yjs (free, learn CRDTs)
        For production: Consider Liveblocks if you want to focus on features
```

---

## 🔬 Example 4: Research and Learning

```bash
$ claude

You: I'm learning about different database architectures. Can you scan
     some database projects and explain the patterns?

Claude: I'll scan major database organizations...

        [Using scan_github tool multiple times]

        Scanning org: cockroachdb
        Scanning org: mongodb
        Scanning org: redis
        Scanning org: apache (focusing on database projects)

        Indexed 200+ repositories. Now analyzing patterns...

        [Using query_leverage tool to find educational content]

        🗄️ Database Architecture Patterns Found:

        1. Distributed SQL (CockroachDB)
           - Raft consensus for consistency
           - Automatic sharding
           - SQL compatibility
           Repository: cockroachdb/cockroach

        2. Document Store (MongoDB)
           - Flexible schema
           - Horizontal scaling via sharding
           - Aggregation pipeline
           Repository: mongodb/mongo

        3. In-Memory (Redis)
           - Extremely fast (microsecond latency)
           - Multiple data structures
           - Persistence options
           Repository: redis/redis

        4. Columnar (Apache Arrow)
           - Optimized for analytics
           - Zero-copy reads
           - Cross-language
           Repository: apache/arrow

You: Which pattern would work best for a real-time analytics dashboard?

Claude: [Using query_leverage tool with context]

        For real-time analytics, I'd recommend a hybrid:

        📦 apache/arrow (Relevance: 0.93)
        - Columnar format = fast aggregations
        - In-memory processing
        - Can query billions of rows in seconds

        📦 clickhouse/clickhouse (Relevance: 0.91)
        - Built specifically for real-time analytics
        - Handles time-series perfectly
        - Can ingest millions of events/second

        [Using compare_repositories tool]

        Comparing apache/arrow vs clickhouse/clickhouse...

        Arrow: Library for data representation
        ClickHouse: Complete database system

        Best solution: Use ClickHouse as your database,
        with Arrow for in-app data processing.

        Want me to find real-world examples using this combo?
```

---

## 🎓 Example 5: Code Review and Optimization

```bash
$ claude

You: I have this Python function that's really slow. Can you help me optimize it?

     def find_similar(query, documents):
         results = []
         for doc in documents:
             score = cosine_similarity(query, doc)
             if score > 0.7:
                 results.append((doc, score))
         return sorted(results, key=lambda x: x[1], reverse=True)

Claude: This is O(n) for the search. Let me find faster alternatives...

        [Using query_leverage tool]

        📦 ruvnet/sublinear-time-solver (Relevance: 0.96)

        Perfect match! This library can make your search O(log n):

        ```python
        from sublinear_solver import JLProjection, sublinear_similarity

        # One-time setup (do once at startup)
        jl = JLProjection(input_dim=len(query), distortion=0.5)
        compressed_docs = jl.project_batch(documents)
        compressed_query = jl.project(query)

        # Now search - O(log n) instead of O(n)!
        def find_similar_fast(query, documents):
            similarities = sublinear_similarity(
                compressed_query,
                compressed_docs
            )
            # This returns top-k automatically, already sorted
            return [(doc, score) for doc, score in similarities if score > 0.7]
        ```

        Speedup: 600× for 10,000 documents
        Accuracy: >97% (controlled by distortion parameter)

        Want me to find more optimization techniques?

You: Yes, what about caching frequently queried documents?

Claude: [Using query_leverage tool]

        📦 ruvnet/FACT (Relevance: 0.89)

        Add deterministic caching:

        ```python
        from fact import FACTCache
        import hashlib

        cache = FACTCache()

        def find_similar_cached(query, documents):
            # Hash the query for cache lookup
            query_hash = hashlib.sha256(str(query).encode()).hexdigest()

            # Check cache first
            cached = cache.get(query_hash)
            if cached:
                return cached

            # Do the search
            results = find_similar_fast(query, documents)

            # Cache for next time
            cache.set(query_hash, results)
            return results
        ```

        Now repeated queries are instant (O(1))!
        Combined with sublinear search, you've gone from:
        - O(n) → O(log n) → O(1) for cached queries

        That's a 10,000× speedup for 10K documents with cache hits!
```

---

## 💡 Pro Tips for Claude Code CLI

### 1. Chain Multiple Tool Calls

```bash
You: Scan the openai organization, then find tools related to function calling

Claude: [First uses scan_github, then uses query_leverage on the results]
```

### 2. Ask for Reasoning

```bash
You: Why did you recommend that specific library?

Claude: [Uses analyze_reasoning tool to show the decision chain]
```

### 3. Compare Multiple Options

```bash
You: Compare React, Vue, and Svelte

Claude: [Uses compare_repositories multiple times and synthesizes]
```

### 4. Iterate on Solutions

```bash
You: That's good, but what if I need it to work in Python instead of JavaScript?

Claude: [Uses query_leverage with updated context]
```

---

## 🎯 Common Patterns

### Pattern 1: Discovery → Deep Dive
```
1. scan_github (broad discovery)
2. query_leverage (find relevant subset)
3. compare_repositories (evaluate options)
4. analyze_reasoning (understand why)
```

### Pattern 2: Problem → Solution
```
1. Describe problem
2. query_leverage (find solutions)
3. compare_repositories (pick best)
4. Get integration code
```

### Pattern 3: Learning
```
1. scan_github (explore topic)
2. query_leverage (find educational resources)
3. compare_repositories (understand differences)
```

---

## 📚 More Examples

See also:
- **[Claude Desktop Examples](CLAUDE_DESKTOP_EXAMPLES.md)** - Visual examples with screenshots
- **[MCP Install Guide](MCP_INSTALL.md)** - Full installation instructions
- **[Quick Reference](MCP_QUICK_REFERENCE.md)** - Command quick reference

---

**Ready to try it?**

```bash
docker compose up -d
claude mcp add ruvscan --scope user --env GITHUB_TOKEN=ghp_token -- uvx ruvscan-mcp
claude
```
