//! RuvScan Sublinear Engine Library
//! 
//! This library provides sublinear-time algorithms for semantic similarity
//! computation using Johnson-Lindenstrauss projection.

pub mod sublinear;
pub mod grpc_service;

// Re-export main types for convenience
pub use sublinear::{JLProjection, compute_similarity, batch_sublinear_similarity};
pub use grpc_service::{SublinearServiceImpl, start_grpc_server};

/// Library version
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version() {
        assert!(!VERSION.is_empty());
    }
}
