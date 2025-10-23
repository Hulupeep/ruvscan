# RuvScan: Sublinear-Intelligence MCP Server

> **RuvScan: The sublinear intelligence layer that finds the world's hidden leverage.**

RuvScan is a **Model Context Protocol (MCP)** intelligence server that continuously scans GitHub repositories to uncover non-obvious leverage — tools, algorithms, and ideas that can 10× what developers are building. Instead of searching by keywords, it uses Ruvnet's computational brain — the sublinear-time-solver for O(log n) semantic comparison, FACT for deterministic reasoning replay, and SAFLA for analogical, "outside-the-box" inference.

## 🧠 What Makes RuvScan Different

- **TRUE O(log n) Semantic Comparison** - Johnson-Lindenstrauss dimension reduction for sublinear similarity
- **Deterministic Reasoning** - FACT cache ensures 100% reproducible insights
- **Analogical Inference** - SAFLA generates creative, cross-domain reuse ideas
- **Hybrid Architecture** - Python orchestration + Rust computation + Go scanning

## 🏗️ Architecture

```
                         ┌────────────────────────────┐
                         │        User / Agent        │
                         │ (CLI, IDE, TabStax, API)   │
                         └──────────────┬─────────────┘
                                        │
                                        ▼
                        ┌────────────────────────────────┐
                        │     🧠 Python MCP Orchestrator   │
                        │  (FastAPI + FACT + SAFLA/NOVA)  │
                        │---------------------------------│
                        │ - Handles /scan and /query       │
                        │ - Embeds Ruv reasoning layer     │
                        │ - Manages deterministic cache    │
                        │ - Calls Rust solver + Go workers │
                        └──────────────┬──────────────────┘
                                       │
               ┌───────────────────────┼────────────────────────┐
               │                                               │
               ▼                                               ▼
  ┌───────────────────────────┐                ┌─────────────────────────┐
  │ 🦀 Rust Sublinear Engine   │                │ 🐹 Go Scanning Workers   │
  │ (WASM + MidStream)        │                │ (Async GitHub Crawlers)  │
  │---------------------------│                │--------------------------│
  │ - TRUE O(log n) semantic  │                │ - Parallel repo fetching │
  │   comparison & clustering │                │ - Metadata diff checking │
  │ - WASM bindings for Python│                │ - Live webhook updates   │
  │ - MidStream inflight sync │                │ - Push updates to Python │
  └──────────────┬────────────┘                └────────────┬─────────────┘
                 │                                         │
                 ▼                                         ▼
           ┌────────────────────────────────────────────────┐
           │         🗂️ FACT Cache / SQLite Storage         │
           │  Deterministic prompt + reasoning persistence    │
           │  for reproducibility & versioned learning        │
           └────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Rust 1.75+
- Go 1.21+
- Docker & Docker Compose (optional)
- GitHub Personal Access Token

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ruvnet/ruvscan.git
cd ruvscan
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your tokens:
# - GITHUB_TOKEN
# - OPENAI_API_KEY (for embeddings)
```

3. **Install dependencies**

Python:
```bash
pip install -r requirements.txt
```

Rust:
```bash
cd src/rust
cargo build --release
```

Go:
```bash
cd src/go
go mod download
go build -o scanner ./scanner
```

### Running with Docker Compose (Recommended)

```bash
# Start all services
docker compose up -d

# Check logs
docker compose logs -f

# Stop services
docker compose down
```

### Running Manually

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
export RUVSCAN_SOURCE_TYPE=org
export RUVSCAN_SOURCE_NAME=ruvnet
cd src/go/scanner
go run main.go
```

## 📚 API Endpoints

### MCP Tools

#### `/scan` - Scan GitHub Repositories
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "org",
    "source_name": "ruvnet",
    "limit": 50
  }'
```

#### `/query` - Query for Leverage
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "How can I speed up context recall in my AI app?",
    "max_results": 10,
    "min_score": 0.7
  }'
```

#### `/compare` - Compare Two Repos
```bash
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{
    "repo_a": "ruvnet/sublinear-time-solver",
    "repo_b": "ruvnet/FACT"
  }'
```

#### `/analyze` - Analyze Reasoning Chain
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo": "ruvnet/sublinear-time-solver"
  }'
```

## 🧩 Key Components

### Python MCP Orchestrator
- FastAPI server handling MCP protocol
- FACT deterministic caching
- SAFLA analogical reasoning
- Embedding generation and storage

### Rust Sublinear Engine
- TRUE O(log n) algorithms
- Johnson-Lindenstrauss dimension reduction
- gRPC server for Python integration
- WASM bindings for portability

### Go Scanning Workers
- Concurrent GitHub API fetching
- README extraction and summarization
- Metadata change detection
- REST/gRPC integration with Python

## 🎯 Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Repos per scan | ≥ 50 | ✅ Planned |
| Query latency | ≤ 3 seconds | ✅ Planned |
| CPU usage | ≤ 1 core | ✅ Planned |
| Memory footprint | ≤ 500 MB | ✅ Planned |
| Deterministic replay | 100% | ✅ Planned |

## 🧠 Leverage Card Schema

```json
{
  "repo": "github.com/org/repo",
  "capabilities": ["solver", "context management"],
  "summary": "Short description of repo's value.",
  "outside_box_reasoning": "Creative reuse idea.",
  "integration_hint": "How to connect or adapt.",
  "relevance_score": 0.92,
  "runtime_complexity": "O(log n)",
  "cached": true
}
```

## 📈 Development Roadmap

| Week | Deliverable | Status |
|------|-------------|--------|
| 1 | Setup FastAPI MCP skeleton + endpoints | ✅ Done |
| 2 | Integrate GitHub API fetcher + README summarizer | 🔄 In Progress |
| 3 | Add Rust sublinear engine (via gRPC) | 📋 Planned |
| 4 | Implement FACT cache + Leverage Card schema | 📋 Planned |
| 5 | Test reasoning output + sample use cases | 📋 Planned |
| 6 | CLI + basic UX polish + documentation | 📋 Planned |

## 🔮 Post-MVP Extensions

| Phase | Feature | Description |
|-------|---------|-------------|
| v0.6 | Go scanner clustering | Asynchronous multi-threaded GitHub ingestion |
| v0.7 | MidStream integration | Real-time scanning + inflight updates |
| v0.8 | Supabase sync | Cloud cache & multi-agent collaboration |
| v1.0 | Self-optimizing agent | RuvScan learns which discoveries lead to real reuse |

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md).

## 📄 License

MIT OR Apache-2.0

## 🔗 Links

- [Ruvnet GitHub](https://github.com/ruvnet)
- [Sublinear Time Solver](https://github.com/ruvnet/sublinear-time-solver)
- [FACT Framework](https://github.com/ruvnet/FACT)
- [Issue Tracker](https://github.com/ruvnet/ruvscan/issues)

## ✨ Acknowledgments

Built with:
- [sublinear-time-solver](https://github.com/ruvnet/sublinear-time-solver) - TRUE O(log n) algorithms
- [FACT](https://github.com/ruvnet/FACT) - Deterministic caching
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Rust](https://www.rust-lang.org/) - Performance-critical computation
- [Go](https://go.dev/) - Concurrent scanning workers

---

*Created by Colm Byrne / Flout Labs - Transforming global code into actionable, deterministic insight.*
