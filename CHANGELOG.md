# Changelog

All notable changes to RuvScan will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-10-23

### Added
- Initial MVP release
- Python MCP orchestrator with FastAPI
- Rust sublinear engine with gRPC
- Go concurrent GitHub scanner
- FACT deterministic caching
- SAFLA analogical reasoning
- Johnson-Lindenstrauss O(log n) similarity
- SQLite database storage
- Docker Compose orchestration
- CLI tool with 6 commands
- Comprehensive documentation
- Example usage scripts
- Unit and integration tests

### MCP Endpoints
- `/scan` - Scan GitHub org/user/topic
- `/query` - Query for leverage cards
- `/compare` - Compare repositories
- `/analyze` - Analyze reasoning chain
- `/cards` - List saved leverage cards
- `/mcp/tools` - List available MCP tools

### Components
- **Python MCP Server**
  - FastAPI with async support
  - FACT cache implementation
  - SAFLA reasoning engine
  - Embedding generation (OpenAI)
  - Database layer with SQLite
  - gRPC client for Rust

- **Rust Sublinear Engine**
  - TRUE O(log n) algorithms
  - JL dimension reduction
  - gRPC server
  - Cosine similarity
  - Batch processing

- **Go Scanner Workers**
  - Concurrent GitHub API
  - README extraction
  - Rate limit handling
  - REST integration

### Infrastructure
- Docker multi-container setup
- Kubernetes manifests
- Production configurations
- Monitoring and metrics
- Health checks
- Backup scripts

### Documentation
- README with architecture
- Quick start guide
- API reference
- Deployment guide
- Architecture details
- Build summary

## [Unreleased]

### Planned for v0.6
- [ ] Complete Rust-Python gRPC integration
- [ ] Real Go scanner → Python data flow
- [ ] LLM integration for SAFLA reasoning
- [ ] Enhanced error handling
- [ ] Performance optimizations
- [ ] Supabase cloud storage option

### Planned for v0.7
- [ ] MidStream real-time updates
- [ ] Advanced caching strategies
- [ ] Prometheus metrics export
- [ ] Grafana dashboards
- [ ] API authentication
- [ ] Rate limiting

### Planned for v1.0
- [ ] Self-optimizing agent
- [ ] Federated scanning nodes
- [ ] Graph analysis
- [ ] WebSocket support
- [ ] Advanced query DSL
- [ ] ML-powered ranking

## Security

### Known Issues
- No authentication implemented (v0.5)
- No rate limiting (v0.5)
- Secrets in environment variables (consider Vault)

### Addressed in Future Versions
- API key authentication (v0.6)
- OAuth 2.0 support (v0.7)
- Rate limiting (v0.6)
- Audit logging (v0.7)

## Performance

### Current Metrics (v0.5)
- Query latency: Not yet benchmarked
- Scan throughput: Not yet benchmarked
- Memory footprint: <500MB target
- CPU usage: <1 core target

### Improvements Planned
- Database query optimization
- Caching improvements
- Batch processing enhancements
- Connection pooling

## Breaking Changes

### v0.5.0
- Initial release - no breaking changes

## Migration Guide

### From Development to Production
1. Update environment variables
2. Enable SSL/TLS
3. Configure external database
4. Set up monitoring
5. Configure backups
6. Review security checklist

## Contributors

- Colm Byrne (Flout Labs) - Initial implementation

## Acknowledgments

Built with:
- [sublinear-time-solver](https://github.com/ruvnet/sublinear-time-solver)
- [FACT](https://github.com/ruvnet/FACT)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Rust](https://www.rust-lang.org/)
- [Go](https://go.dev/)
