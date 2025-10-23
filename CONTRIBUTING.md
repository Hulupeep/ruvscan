# Contributing to RuvScan

🎉 **Thank you for considering contributing to RuvScan!**

RuvScan is building the future of code discovery — where developers find solutions from across domains they'd never think to search for. Every contribution helps make this vision real.

---

## 🚀 Quick Start

### 1. Fork & Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/ruvscan.git
cd ruvscan
```

### 2. Setup

```bash
# Run the setup script
bash scripts/setup.sh

# Or manually:
pip install -r requirements.txt
cd src/rust && cargo build --release
cd ../go && go mod download
```

### 3. Create a Branch

```bash
git checkout -b feature/your-amazing-feature
# or
git checkout -b fix/bug-description
```

### 4. Make Changes

Write awesome code! See our [style guides](#code-style) below.

### 5. Test

```bash
# Run all tests
./scripts/run_tests.sh

# Or specific suites
pytest tests/test_server.py
cd src/rust && cargo test
cd src/go && go test ./...
```

### 6. Commit

```bash
git add .
git commit -m "feat: add amazing feature

- Describe what you changed
- Why you changed it
- Any breaking changes"
```

**Commit message format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code restructuring
- `perf:` Performance improvement
- `chore:` Maintenance

### 7. Push & PR

```bash
git push origin feature/your-amazing-feature
```

Then open a Pull Request on GitHub!

---

## 🎯 What to Contribute

### 🐛 Bug Fixes

Found a bug? We want to fix it!

1. Check if it's [already reported](https://github.com/ruvnet/ruvscan/issues)
2. If not, [open an issue](https://github.com/ruvnet/ruvscan/issues/new?template=bug_report.md)
3. Submit a PR with the fix

### ✨ Features

Have an idea? Let's discuss!

1. [Open a feature request](https://github.com/ruvnet/ruvscan/issues/new?template=feature_request.md)
2. Discuss the design
3. Get approval from maintainers
4. Implement and submit PR

### 📚 Documentation

Docs are as important as code!

**What we need:**
- Tutorials and guides
- API examples
- Architecture explanations
- Troubleshooting tips
- Translation to other languages

**Where to contribute:**
- `README.md` - Main docs
- `docs/` - Detailed guides
- Code comments
- Docstrings

### 🧪 Testing

Help us test edge cases!

**Areas that need testing:**
- Large-scale scans (1000+ repos)
- Different GitHub org structures
- Edge cases in similarity computation
- Error handling
- Performance under load

### 🔌 Integrations

Build integrations with:
- IDEs (VS Code, Cursor, JetBrains)
- AI tools (Claude, ChatGPT, Copilot)
- CI/CD platforms
- Other developer tools

### 🎨 UI/Dashboard

Design and build:
- Web dashboard for RuvScan
- Visualization of repo relationships
- Interactive query builder
- Metrics and analytics

---

## 📏 Code Style

### Python

**Style:** [Black](https://black.readthedocs.io/) + [Ruff](https://docs.astral.sh/ruff/)

```bash
# Format code
black src/mcp

# Lint
ruff check src/mcp
```

**Guidelines:**
- Use type hints
- Write docstrings (Google style)
- Keep functions focused and small
- Prefer async/await for I/O

**Example:**
```python
async def query_leverage(
    intent: str,
    max_results: int = 10
) -> List[LeverageCard]:
    """
    Query for leverage cards based on user intent.

    Args:
        intent: User's problem or goal
        max_results: Maximum cards to return

    Returns:
        List of leverage cards ranked by relevance
    """
    # Implementation
```

### Rust

**Style:** [rustfmt](https://github.com/rust-lang/rustfmt)

```bash
cd src/rust
cargo fmt
cargo clippy
```

**Guidelines:**
- Follow Rust conventions
- Use `Result` for error handling
- Add doc comments (`///`)
- Write tests for public APIs

**Example:**
```rust
/// Compute sublinear similarity between two vectors.
///
/// # Arguments
/// * `vec_a` - First vector
/// * `vec_b` - Second vector
/// * `distortion` - JL distortion parameter
///
/// # Returns
/// Similarity score and complexity description
pub fn sublinear_similarity(
    vec_a: &Array1<f64>,
    vec_b: &Array1<f64>,
    distortion: f64
) -> (f64, String) {
    // Implementation
}
```

### Go

**Style:** [gofmt](https://go.dev/blog/gofmt) + [golint](https://github.com/golang/lint)

```bash
cd src/go
gofmt -w .
go vet ./...
```

**Guidelines:**
- Follow Go conventions
- Use context for cancellation
- Handle errors explicitly
- Add package-level comments

**Example:**
```go
// Scanner manages concurrent GitHub scanning.
// It handles rate limiting and parallel processing.
type Scanner struct {
    client *github.Client
    config ScanConfig
}

// ScanOrg scans all repos in a GitHub organization.
func (s *Scanner) ScanOrg(ctx context.Context) error {
    // Implementation
}
```

---

## 🧪 Testing Guidelines

### Unit Tests

**Python:**
```python
import pytest

def test_fact_cache_determinism():
    """Test that FACT cache returns identical results"""
    cache = FACTCache()
    prompt = "test"
    response = "result"

    hash1 = cache.set(prompt, response)
    hash2 = cache.set(prompt, response)

    assert hash1 == hash2
```

**Rust:**
```rust
#[test]
fn test_jl_projection() {
    let source_dim = 1000;
    let jl = JLProjection::new(source_dim, 0.5);

    assert!(jl.target_dimension < source_dim);
}
```

### Integration Tests

Test full workflows:

```python
def test_scan_query_workflow():
    # Scan
    scan_response = client.post("/scan", json={
        "source_type": "org",
        "source_name": "test"
    })
    assert scan_response.status_code == 200

    # Query
    query_response = client.post("/query", json={
        "intent": "test query"
    })
    assert query_response.status_code == 200
```

### Coverage

Aim for:
- **Python**: 80%+ coverage
- **Rust**: 70%+ coverage
- **Critical paths**: 100% coverage

---

## 📝 Documentation Guidelines

### Code Comments

**When to comment:**
- Complex algorithms
- Non-obvious decisions
- Performance optimizations
- Security considerations

**When NOT to comment:**
- Obvious code
- What the code does (use clear names instead)

**Good:**
```python
# Use Johnson-Lindenstrauss projection to reduce from
# n dimensions to O(log n) while preserving distances
# within (1 ± ε) with probability > 99%
jl = JLProjection(dim, distortion=0.5)
```

**Bad:**
```python
# Create JL projection
jl = JLProjection(dim, distortion=0.5)
```

### API Documentation

Document all public APIs:

```python
class RuvScanClient:
    """
    Client for RuvScan MCP server.

    Provides methods for scanning repos, querying for leverage,
    and comparing repositories.

    Example:
        >>> client = RuvScanClient("http://localhost:8000")
        >>> results = await client.query("optimize my code")
    """

    async def query(
        self,
        intent: str,
        max_results: int = 10
    ) -> List[LeverageCard]:
        """
        Query for leverage based on intent.

        Args:
            intent: Your problem or goal
            max_results: Max cards to return (default: 10)

        Returns:
            List of leverage cards sorted by relevance

        Raises:
            httpx.HTTPError: If request fails
        """
```

---

## 🔍 Code Review Process

### Submitting PRs

**PR checklist:**
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code formatted
- [ ] All tests passing
- [ ] No merge conflicts
- [ ] Description explains changes

**PR description template:**
```markdown
## What

Brief description of changes

## Why

Problem this solves or feature it adds

## How

Technical approach

## Testing

How you tested this

## Screenshots

If UI changes
```

### Review Guidelines

**For reviewers:**
- Be kind and constructive
- Ask questions, don't demand changes
- Approve when it's good enough
- Focus on logic, not style (we have linters)

**For authors:**
- Respond to all comments
- Ask for clarification if needed
- Make requested changes or discuss
- Mark conversations as resolved

---

## 🎯 Areas That Need Help

### High Priority

1. **Performance Testing**
   - Benchmark O(log n) claims
   - Load testing with 10k+ repos
   - Memory profiling

2. **LLM Integration**
   - Improve SAFLA reasoning prompts
   - Test different models
   - Optimize token usage

3. **Error Handling**
   - Better error messages
   - Retry logic
   - Graceful degradation

### Medium Priority

4. **IDE Integrations**
   - VS Code extension
   - Cursor plugin
   - JetBrains support

5. **Dashboard**
   - Web UI for queries
   - Visualization of results
   - Admin panel

6. **Documentation**
   - Video tutorials
   - More examples
   - Troubleshooting guide

### Good First Issues

Look for issues labeled [`good first issue`](https://github.com/ruvnet/ruvscan/labels/good%20first%20issue):

- Documentation improvements
- Adding tests
- Bug fixes with clear reproduction
- Small feature additions

---

## 🤔 Questions?

**Before asking:**
1. Check [existing issues](https://github.com/ruvnet/ruvscan/issues)
2. Read the [docs](docs/)
3. Search [discussions](https://github.com/ruvnet/ruvscan/discussions)

**Still need help?**
- Open a [Discussion](https://github.com/ruvnet/ruvscan/discussions)
- Ask in the issue you're working on
- Reach out to maintainers

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT OR Apache-2.0).

---

## 🙏 Thank You!

Every contribution makes RuvScan better for developers worldwide. Whether you fix a typo or add a major feature, we appreciate you!

**Happy coding!** 🚀

---

<p align="center">
  <strong>Built with 💙 by the RuvScan community</strong>
</p>
