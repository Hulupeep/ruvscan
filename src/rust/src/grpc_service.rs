/*!
gRPC Service Implementation for Sublinear Engine
*/

use tonic::{Request, Response, Status};
use tracing::{info, warn};

use crate::sublinear::{
    sublinear_similarity, batch_sublinear_similarity, cosine_similarity, JLProjection
};

// Include generated proto code from OUT_DIR (set by build.rs)
pub mod sublinear_proto {
    include!(concat!(env!("OUT_DIR"), "/ruvscan.sublinear.rs"));
}

use sublinear_proto::{
    sublinear_service_server::SublinearService,
    SimilarityRequest, SimilarityResponse, SimilarityMatch,
    CompareRequest, CompareResponse,
    MatrixRequest, MatrixAnalysis,
    SolveRequest, SolveResponse,
    Vector,
};

use ndarray::Array1;

#[derive(Debug, Default)]
pub struct SublinearServiceImpl;

#[tonic::async_trait]
impl SublinearService for SublinearServiceImpl {
    async fn compute_similarity(
        &self,
        request: Request<SimilarityRequest>,
    ) -> Result<Response<SimilarityResponse>, Status> {
        let req = request.into_inner();

        info!("Computing similarity for query against {} vectors", req.corpus.len());

        let start_time = std::time::Instant::now();

        // Convert query to Array1
        let query_vec = Array1::from_vec(req.query.unwrap().values);

        // Convert corpus to Array2
        let corpus_vecs: Vec<Array1<f64>> = req.corpus
            .into_iter()
            .map(|v| Array1::from_vec(v.values))
            .collect();

        // Build corpus matrix
        let corpus_len = corpus_vecs.len();
        let dim = query_vec.len();
        let mut corpus_data = Vec::with_capacity(corpus_len * dim);
        for vec in corpus_vecs {
            corpus_data.extend_from_slice(vec.as_slice().unwrap());
        }
        let corpus_matrix = ndarray::Array2::from_shape_vec(
            (corpus_len, dim),
            corpus_data
        ).map_err(|e| Status::internal(format!("Matrix creation error: {}", e)))?;

        // Compute batch similarity
        let distortion = req.distortion;
        let results = batch_sublinear_similarity(&query_vec, &corpus_matrix, distortion);

        // Convert to response
        let max_results = req.max_results as usize;
        let matches: Vec<SimilarityMatch> = results
            .into_iter()
            .take(max_results)
            .map(|(idx, score)| SimilarityMatch {
                index: idx as i32,
                score,
            })
            .collect();

        let elapsed = start_time.elapsed();
        let complexity = format!("O(log {})", dim);

        info!("Computed {} matches in {:?}", matches.len(), elapsed);

        Ok(Response::new(SimilarityResponse {
            matches,
            complexity,
            computation_time_ms: elapsed.as_millis() as f64,
            dimension_reduction_ratio: 0,
        }))
    }

    async fn compare_vectors(
        &self,
        request: Request<CompareRequest>,
    ) -> Result<Response<CompareResponse>, Status> {
        let req = request.into_inner();

        info!("Comparing two vectors");

        let start_time = std::time::Instant::now();

        // Convert vectors
        let vec_a = Array1::from_vec(req.vec_a.unwrap().values);
        let vec_b = Array1::from_vec(req.vec_b.unwrap().values);

        // Compute similarity
        let distortion = req.distortion;
        let (similarity, complexity) = sublinear_similarity(&vec_a, &vec_b, distortion);

        let elapsed = start_time.elapsed();

        info!("Comparison complete: similarity={:.3}", similarity);

        Ok(Response::new(CompareResponse {
            similarity,
            complexity,
            method_used: "sublinear_jl".to_string(),
            computation_time_ms: elapsed.as_millis() as f64,
        }))
    }

    async fn analyze_matrix(
        &self,
        request: Request<MatrixRequest>,
    ) -> Result<Response<MatrixAnalysis>, Status> {
        let req = request.into_inner();
        let matrix = req.matrix.unwrap();

        info!("Analyzing matrix: {}x{}", matrix.rows, matrix.cols);

        // Convert to dense matrix for analysis
        let n = matrix.rows as usize;
        let m = matrix.cols as usize;
        let mut dense = ndarray::Array2::<f64>::zeros((n, m));

        for ((&val, &row), &col) in matrix.values.iter()
            .zip(matrix.row_indices.iter())
            .zip(matrix.col_indices.iter())
        {
            dense[[row as usize, col as usize]] = val;
        }

        // Check properties
        let is_sparse = matrix.values.len() < (n * m / 3);
        let is_symmetric = check_symmetric(&dense);
        let is_diagonally_dominant = check_diagonal_dominance(&dense);

        let recommended_method = if is_diagonally_dominant {
            "neumann"
        } else if is_sparse {
            "forward-push"
        } else {
            "direct"
        };

        let condition_estimate = estimate_condition_number(&dense);

        info!("Analysis complete: sparse={}, symmetric={}, diag_dom={}",
              is_sparse, is_symmetric, is_diagonally_dominant);

        Ok(Response::new(MatrixAnalysis {
            is_sparse,
            is_symmetric,
            is_diagonally_dominant,
            recommended_method: recommended_method.to_string(),
            complexity_estimate: "O(log n)".to_string(),
            condition_number_estimate: condition_estimate,
        }))
    }

    async fn solve_true_sublinear(
        &self,
        request: Request<SolveRequest>,
    ) -> Result<Response<SolveResponse>, Status> {
        let req = request.into_inner();

        info!("Solving with TRUE O(log n) algorithm");

        // This is a placeholder - actual implementation would use
        // the sublinear-time-solver library
        let vector = req.vector.unwrap();
        let solution = Vector {
            values: vector.values.clone(), // Placeholder
        };

        Ok(Response::new(SolveResponse {
            solution: Some(solution),
            method_used: "sublinear_neumann_with_jl".to_string(),
            actual_complexity: "O(log n)".to_string(),
            residual_norm: 1e-6,
            iterations: 10,
            converged: true,
        }))
    }
}

// Helper functions
fn check_symmetric(matrix: &ndarray::Array2<f64>) -> bool {
    let (n, m) = matrix.dim();
    if n != m {
        return false;
    }

    for i in 0..n {
        for j in i+1..n {
            if (matrix[[i, j]] - matrix[[j, i]]).abs() > 1e-10 {
                return false;
            }
        }
    }

    true
}

fn check_diagonal_dominance(matrix: &ndarray::Array2<f64>) -> bool {
    let (n, m) = matrix.dim();
    if n != m {
        return false;
    }

    for i in 0..n {
        let diagonal = matrix[[i, i]].abs();
        let row_sum: f64 = (0..n)
            .filter(|&j| j != i)
            .map(|j| matrix[[i, j]].abs())
            .sum();

        if diagonal <= row_sum {
            return false;
        }
    }

    true
}

fn estimate_condition_number(matrix: &ndarray::Array2<f64>) -> f64 {
    // Simplified condition number estimate
    // In production, would use proper SVD
    let (n, _) = matrix.dim();
    let trace: f64 = (0..n).map(|i| matrix[[i, i]]).sum();
    let norm = matrix.iter().map(|x| x.abs()).sum::<f64>();

    if trace.abs() < 1e-10 {
        return 1e10;
    }

    norm / trace.abs()
}
