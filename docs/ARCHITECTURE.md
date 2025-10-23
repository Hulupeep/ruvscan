# RuvScan Architecture

## System Overview

RuvScan is a hybrid tri-language system combining:

- **🐍 Python**: MCP orchestration, reasoning, and API
- **🦀 Rust**: High-performance sublinear computation
- **🐹 Go**: Concurrent GitHub scanning

```
┌─────────────────────────────────────────────────────────┐
│                    User Layer                            │
│  (CLI, IDE, TabStax, Claude Desktop, Custom Agents)     │
└────────────────────┬────────────────────────────────────┘
                     │ MCP Protocol
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Python MCP Orchestrator (FastAPI)              │
│  ┌──────────────┬──────────────┬─────────────────────┐ │
│  │   Endpoints  │  Reasoning   │     Bindings        │ │
│  │  /scan       │  FACT Cache  │  Rust gRPC Client   │ │
│  │  /query      │  SAFLA Agent │  Go REST Client     │ │
│  │  /compare    │  Embeddings  │  Database           │ │
│  │  /analyze    │              │                     │ │
│  └──────────────┴──────────────┴─────────────────────┘ │
└────────┬──────────────────────────────────┬────────────┘
         │ gRPC                             │ REST/MQ
         ▼                                  ▼
┌──────────────────────┐         ┌──────────────────────┐
│  Rust Engine         │         │  Go Scanner Workers  │
│  ┌────────────────┐  │         │  ┌────────────────┐  │
│  │ Sublinear Algo │  │         │  │ GitHub API     │  │
│  │ JL Projection  │  │         │  │ README Fetch   │  │
│  │ Similarity     │  │         │  │ Metadata Diff  │  │
│  │ gRPC Server    │  │         │  │ Concurrent     │  │
│  └────────────────┘  │         │  └────────────────┘  │
└──────────────────────┘         └──────────────────────┘
         │                                  │
         └────────────┬─────────────────────┘
                      ▼
         ┌─────────────────────────┐
         │   Storage Layer         │
         │  ┌───────────────────┐  │
         │  │ SQLite / Supabase │  │
         │  │ - repos           │  │
         │  │ - leverage_cards  │  │
         │  │ - fact_cache      │  │
         │  └───────────────────┘  │
         └─────────────────────────┘
```

## Component Details

### Python MCP Orchestrator

**Location**: `src/mcp/`

**Purpose**: Main control plane and API gateway

**Modules**:
- `server.py` - FastAPI application with MCP endpoints
- `endpoints/` - Individual endpoint handlers
- `reasoning/` - FACT cache and SAFLA reasoning
- `bindings/` - Clients for Rust and Go services
- `storage/` - Database layer and models

**Key Technologies**:
- FastAPI for async HTTP
- Pydantic for validation
- gRPC client for Rust
- HTTP client for Go

**Flow**:
1. Receive MCP request
2. Check FACT cache
3. If cache miss:
   - Call Rust for computation
   - Call Go for scanning
   - Generate embeddings
   - Run SAFLA reasoning
4. Store in FACT cache
5. Return leverage cards

### Rust Sublinear Engine

**Location**: `src/rust/`

**Purpose**: TRUE O(log n) semantic computation

**Modules**:
- `main.rs` - gRPC server entry point
- `sublinear.rs` - JL projection and algorithms
- `jl_reduction.rs` - Johnson-Lindenstrauss
- `similarity.rs` - Similarity computation
- `proto/` - gRPC definitions

**Key Algorithms**:

1. **Johnson-Lindenstrauss Projection**
   - Projects n-dimensional vectors to O(log n)
   - Preserves distances within (1 ± ε)
   - Random Gaussian projection matrix

2. **Sublinear Similarity**
   - Compute in reduced space
   - TRUE O(log n) complexity
   - Cosine similarity metric

3. **Batch Processing**
   - Process multiple vectors
   - Rank by similarity
   - Stream results

**Performance**:
- Target: <3s for 1000+ repo comparison
- Complexity: O(log n) guaranteed
- Memory: <500MB

### Go Scanner Workers

**Location**: `src/go/scanner/`

**Purpose**: Concurrent GitHub API integration

**Modules**:
- `main.go` - Worker entry point
- `worker.go` - Concurrent fetch logic
- `diff.go` - Change detection
- `api_client.go` - GitHub GraphQL
- `publisher.go` - Send to Python

**Features**:
- 10 concurrent workers
- Rate limit handling
- README extraction
- Metadata diffing
- REST/MQ publishing

**Flow**:
1. Receive scan request
2. Query GitHub API
3. Fetch repo metadata
4. Extract README
5. Detect changes
6. Push to Python MCP

### Storage Layer

**Database Schema**:

```sql
-- Repositories
CREATE TABLE repos (
  id INTEGER PRIMARY KEY,
  name TEXT,
  org TEXT,
  full_name TEXT UNIQUE,
  description TEXT,
  topics TEXT,
  readme TEXT,
  embedding BLOB,
  sublinear_hash TEXT,
  stars INTEGER,
  language TEXT,
  last_scan TIMESTAMP
);

-- Leverage Cards
CREATE TABLE leverage_cards (
  id INTEGER PRIMARY KEY,
  repo_id INTEGER,
  capabilities TEXT,
  summary TEXT,
  reasoning TEXT,
  integration_hint TEXT,
  relevance_score REAL,
  runtime_complexity TEXT,
  query_intent TEXT,
  cached BOOLEAN,
  FOREIGN KEY (repo_id) REFERENCES repos(id)
);

-- FACT Cache
CREATE TABLE fact_cache (
  id INTEGER PRIMARY KEY,
  hash TEXT UNIQUE,
  prompt TEXT,
  response TEXT,
  version TEXT,
  metadata TEXT,
  timestamp TIMESTAMP
);
```

## Data Flow

### Scan Flow

```
User → /scan → Python MCP
                  ↓
            Go Scanner
                  ↓
          GitHub API (fetch repos)
                  ↓
          Extract README
                  ↓
          POST /ingest → Python
                  ↓
          Store in DB
```

### Query Flow

```
User → /query → Python MCP
                  ↓
         Generate embedding
                  ↓
         Check FACT cache
                  ↓
         (if miss) gRPC → Rust Engine
                  ↓
         JL Projection
                  ↓
         Compute similarities
                  ↓
         Return matches → Python
                  ↓
         SAFLA reasoning
                  ↓
         Generate leverage cards
                  ↓
         Store in FACT cache
                  ↓
         Return to user
```

### Compare Flow

```
User → /compare → Python MCP
                     ↓
            Get repo embeddings
                     ↓
            gRPC → Rust Engine
                     ↓
            Sublinear compare
                     ↓
            Return similarity
                     ↓
            Cache result
                     ↓
            Return to user
```

## Communication Protocols

### Python ↔ Rust

**Protocol**: gRPC

**Messages**:
- `SimilarityRequest` / `SimilarityResponse`
- `CompareRequest` / `CompareResponse`
- `MatrixRequest` / `MatrixAnalysis`

**Port**: 50051

### Python ↔ Go

**Protocol**: REST HTTP

**Endpoints**:
- `POST /ingest` - Receive scan results
- `GET /status` - Check scanner status

**Port**: Configurable

### User ↔ Python

**Protocol**: MCP over HTTP

**Endpoints**:
- `/scan`, `/query`, `/compare`, `/analyze`, `/cards`

**Port**: 8000

## Deployment

### Docker Compose

All services orchestrated via `docker-compose.yml`:

```yaml
services:
  mcp-server:    # Python FastAPI
  rust-engine:   # Rust gRPC server
  scanner:       # Go workers
```

Network: `ruvscan-network`

### Kubernetes (Future)

Helm chart for:
- Python pods (replicas)
- Rust engine (stateless)
- Go scanner workers (jobs)
- Redis cache (optional)
- PostgreSQL (optional)

## Scalability

### Horizontal Scaling

1. **Python MCP**: Multiple replicas behind load balancer
2. **Rust Engine**: Stateless, scale as needed
3. **Go Scanners**: Worker pool, scale based on queue depth

### Vertical Scaling

1. **Rust**: CPU-bound, benefits from more cores
2. **Go**: Network-bound, benefits from more connections
3. **Python**: I/O-bound, benefits from async workers

### Caching Strategy

1. **FACT Cache**: Deterministic prompt replay
2. **Embedding Cache**: Pre-computed vectors
3. **Result Cache**: TTL-based expiry

## Security

1. **GitHub Token**: Secure env var, never logged
2. **API Keys**: Encrypted at rest
3. **gRPC**: TLS in production
4. **Database**: Encrypted connections
5. **Input Validation**: Pydantic schemas

## Monitoring

1. **Logs**: Structured JSON via tracing
2. **Metrics**: Prometheus exporters
3. **Health Checks**: `/health` endpoint
4. **Tracing**: OpenTelemetry (future)

## Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| Query latency | <3s | TBD |
| Scan throughput | >50 repos/min | TBD |
| Memory footprint | <500MB | TBD |
| CPU utilization | <1 core | TBD |
| Determinism | 100% | 100% |

## Future Enhancements

1. **MidStream Integration**: Real-time streaming
2. **Supabase Sync**: Cloud persistence
3. **Federated Nodes**: P2P scanning
4. **Self-Optimization**: Learn from usage
5. **Graph Analysis**: Repo relationships
