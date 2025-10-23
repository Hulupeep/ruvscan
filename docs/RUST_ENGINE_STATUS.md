# Rust Engine Status Report

## What Does the Rust Engine Do?

The **Rust Sublinear Engine** is the performance-critical component of RuvScan that implements **TRUE O(log n) algorithms** for semantic similarity computation.

### Purpose

The Rust engine provides:

1. **Johnson-Lindenstrauss (JL) Dimension Reduction**
   - Reduces high-dimensional vectors (e.g., OpenAI embeddings at 1536 dims) down to O(log n) dimensions
   - Maintains distance properties with controlled distortion
   - Enables sublinear-time similarity computation

2. **Fast Semantic Similarity**
   - Compares query vectors against large corpus
   - Uses JL projection for O(log n) complexity instead of O(n)
   - Returns ranked similarity scores

3. **Matrix Analysis** (Not fully implemented)
   - Analyzes matrix properties (sparse, symmetric, diagonally dominant)
   - Recommends optimal solving algorithms
   - Estimates condition numbers

4. **gRPC Service**
   - Exposes algorithms via gRPC on port 50051
   - Python MCP server calls Rust engine for performance-critical operations
   - Asynchronous request handling with Tokio

### Architecture

```
Python MCP Server (FastAPI)
    ↓ gRPC call
Rust Engine (Tonic + Tokio)
    ↓ Linear Algebra
ndarray + OpenBLAS/LAPACK
```

### Key Algorithms

**File: `src/rust/src/sublinear.rs`**

```rust
pub struct JLProjection {
    pub target_dimension: usize,  // O(log n) dimensions
    pub distortion: f64,           // Allowed error ε
    pub projection_matrix: Array2<f64>,
}

// Target dimension k = O(log n / ε²)
// Projects 1536D → ~100D with 0.5 distortion
```

**gRPC Services** (`src/rust/src/grpc_service.rs`):
- `ComputeSimilarity` - Batch similarity search
- `CompareVectors` - Pairwise vector comparison
- `AnalyzeMatrix` - Matrix property analysis
- `SolveTrueSublinear` - O(log n) matrix solving (placeholder)

## What's Wrong With It?

### ❌ Current Problem: Silent Exit

**Symptom:**
The Rust engine container restarts continuously in Docker with exit code 0, producing **zero output**.

**Evidence:**
```bash
$ docker compose ps
ruvscan-rust  ruvscan-rust-engine  "./ruvscan-sublinear"  Restarting (0)

$ docker compose logs rust-engine
# No output at all

$ strace ./ruvscan-sublinear
execve("./ruvscan-sublinear", ...)
openat("/etc/ld.so.cache", ...)
openat("/lib/x86_64-linux-gnu/libgcc_s.so.1", ...)
openat("/lib/x86_64-linux-gnu/libc.so.6", ...)
openat("/proc/self/maps", ...)
+++ exited with 0 +++
```

The binary starts, loads dynamic libraries, and exits immediately **without executing main()**.

### 🔍 Root Cause Analysis

#### Not Reaching main()

The code in `src/rust/src/main.rs` has extensive debug output:
```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    // VERY FIRST THING - Debug output to stderr
    eprintln!("=== RUST ENGINE STARTING ===");  // ← NEVER PRINTS!
    eprintln!("DEBUG: Entered main function");
    // ...
}
```

**None of these print statements execute.** This means the binary is failing **before entering main()**, likely during:
1. Static initialization
2. Rust runtime initialization
3. Dynamic linker issues

#### Missing OpenBLAS Linkage

`ldd` output shows the binary is **not linked** against OpenBLAS/LAPACK:
```bash
$ ldd ./ruvscan-sublinear
linux-vdso.so.1
libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
# ← Missing libopenblas.so.0
# ← Missing liblapack.so.3
# ← Missing libgfortran.so.5
```

Even though:
- Dockerfile installs: `libopenblas-dev`, `liblapack-dev`, `gfortran`
- build.rs specifies: `println!("cargo:rustc-link-lib=dylib=openblas");`
- Cargo.toml has: `ndarray-linalg = { version = "0.16", features = ["openblas-system"] }`

**The libraries are not being dynamically linked.**

### 🤔 Possible Causes

1. **Static Linking**
   - Cargo may be statically linking OpenBLAS
   - If static lib is incomplete or corrupted, could cause silent failure
   - Check: Does `target/release/ruvscan-sublinear` file size indicate static linking?

2. **ndarray-linalg Initialization Panic**
   - `ndarray-linalg` might panic during static initialization if BLAS backend fails
   - Panic could be swallowed before main() if it happens in `lazy_static!` or similar
   - The library tries to detect/configure BLAS at initialization time

3. **gRPC Proto Code Generation Issue**
   - `grpc_service.rs` uses: `include!(concat!(env!("OUT_DIR"), "/ruvscan.sublinear.rs"));`
   - If proto compilation failed, this could cause a compile-time or runtime issue
   - But build succeeds, so proto generation works

4. **Tokio Runtime Pre-Initialization**
   - Unlikely since runtime is created in main()
   - But some dependency might try to initialize tokio globally

### 📊 Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Build | ✅ Success | Compiles without errors |
| Binary | ✅ Exists | 364KB at `/app/ruvscan-sublinear` |
| Dynamic Links | ⚠️ Incomplete | Missing OpenBLAS/LAPACK/gfortran |
| Execution | ❌ Fails | Exits immediately with code 0 |
| Output | ❌ None | Not even first eprintln! |
| Container | ❌ Restart Loop | Keeps restarting |

### 💡 Why It's Not Critical

**The MCP server works without the Rust engine.**

Currently, all MCP endpoints return placeholder/hardcoded data (see `src/mcp/server.py` lines with `# TODO`). The system is designed as an MVP skeleton where:

1. ✅ **Python MCP Server** - Works, serves API
2. ✅ **Go Scanner** - Works, can scan GitHub
3. ❌ **Rust Engine** - Broken, but not called yet
4. ❌ **Integration** - No data flow between components

So the Rust engine failing doesn't prevent:
- Querying the API (returns placeholder data)
- Scanning GitHub repos (Go scanner works)
- Using the MCP server with Claude

## Recent Fixes Attempted (2025-10-23)

### ✅ Fixed Static Linking
- Changed from `openblas-system` (dynamic) to `openblas-static`
- Updated build.rs to properly link static OpenBLAS library
- Resolved "undefined reference to cblas_*" errors
- Binary now compiles successfully with all BLAS functions statically linked

### ❌ Still Failing: Binary Exits Immediately
Even with static linking fixed, the binary:
- Exits with code 0 immediately
- Produces ZERO output (not even first `stderr().write_all()`)
- Never reaches main() function
- Works when built but fails when run

### 🔬 Investigation Status
The issue appears to be:
- NOT OpenBLAS initialization (we fixed static linking)
- NOT missing dynamic libraries (ldd shows only libc)
- NOT gRPC or Tokio (never reaches runtime creation code)
- Possibly a Rust runtime initialization issue or Docker output buffering

**Current Status:** Disabled in docker-compose with restart: "no" and profiles.

### 🔧 How to Fix

#### Option 1: Debug Static Initialization

```bash
# Run with debug env vars
RUST_BACKTRACE=full RUST_LOG=trace ./ruvscan-sublinear

# Use GDB to catch early crashes
docker compose run --rm --entrypoint gdb rust-engine -- \
  --batch -ex run -ex bt ./ruvscan-sublinear
```

#### Option 2: Simplify Dependencies

Remove ndarray-linalg temporarily to isolate the issue:

```toml
# Cargo.toml - comment out:
# ndarray-linalg = { version = "0.16", features = ["openblas-system"] }
```

See if binary runs without BLAS dependencies.

#### Option 3: Dynamic → Static Linking

Force static linking of OpenBLAS:

```dockerfile
# Dockerfile.rust
RUN apt-get install -y libopenblas-dev liblapack-dev gfortran

# Add static linking flags
ENV RUSTFLAGS="-C target-feature=+crt-static"
```

#### Option 4: Use Different BLAS Backend

Try Intel MKL or pure Rust implementation:

```toml
ndarray-linalg = { version = "0.16", features = ["intel-mkl-static"] }
# or
ndarray = "0.15"  # without linalg
```

#### Option 5: Disable Rust Engine Temporarily

Since it's not critical right now:

```yaml
# docker-compose.yml
services:
  rust-engine:
    # Comment out or set restart: "no"
    restart: "no"
```

### 📝 Recommended Next Steps

1. **Short-term**: Disable Rust engine container (not critical for MVP)
2. **Mid-term**: Debug with GDB/strace to find exact failure point
3. **Long-term**: Implement proper integration with Python MCP server

### 🎯 What Needs to Happen for Full Integration

For the Rust engine to be useful, these need to be completed:

1. **Fix the silent exit issue** (current blocker)
2. **Python gRPC client** - MCP server needs to call Rust engine
3. **Real embeddings** - Replace placeholder data with actual OpenAI embeddings
4. **JL projection** - Use Rust's O(log n) algorithm for similarity
5. **Performance testing** - Verify speed improvements

## Testing (When Fixed)

```bash
# Test if Rust engine is healthy
docker compose ps rust-engine

# Check logs for startup message
docker compose logs rust-engine
# Should see: "🦀 RuvScan Sublinear Engine v0.5.0"

# Test gRPC endpoint
grpcurl -plaintext -d '{
  "vec_a": {"values": [1.0, 2.0, 3.0]},
  "vec_b": {"values": [2.0, 4.0, 6.0]},
  "distortion": 0.5
}' localhost:50051 ruvscan.sublinear.SublinearService/CompareVectors
```

## References

- Johnson-Lindenstrauss Lemma: https://en.wikipedia.org/wiki/Johnson%E2%80%93Lindenstrauss_lemma
- ndarray-linalg docs: https://docs.rs/ndarray-linalg/
- OpenBLAS: https://www.openblas.net/
- Original sublinear-time-solver: https://github.com/ruvnet/sublinear-time-solver

---

**Last Updated:** 2025-10-23
**Status:** Non-functional, under investigation
**Priority:** Low (not blocking MVP functionality)
