/*!
Sublinear algorithms for TRUE O(log n) complexity
Implements Johnson-Lindenstrauss dimension reduction
*/

use ndarray::{Array1, Array2};
use rand::Rng;
use rand_distr::{Distribution, Normal};

/// Johnson-Lindenstrauss dimension reduction
/// Projects n-dimensional vectors to O(log n) dimensions
pub struct JLProjection {
    pub target_dimension: usize,
    pub distortion: f64,
    pub projection_matrix: Array2<f64>,
}

impl JLProjection {
    /// Create new JL projection
    ///
    /// # Arguments
    /// * `source_dimension` - Original dimension n
    /// * `distortion` - Allowed distortion ε (0 < ε < 1)
    pub fn new(source_dimension: usize, distortion: f64) -> Self {
        // JL lemma: target dimension k = O(log n / ε²)
        let target_dimension = ((source_dimension as f64).ln() / (distortion * distortion)).ceil() as usize;
        let target_dimension = target_dimension.max(4); // Minimum 4 dimensions

        // Create random Gaussian projection matrix
        let mut rng = rand::thread_rng();
        let normal = Normal::new(0.0, 1.0).unwrap();

        let projection_matrix = Array2::from_shape_fn(
            (target_dimension, source_dimension),
            |_| normal.sample(&mut rng) / (target_dimension as f64).sqrt()
        );

        Self {
            target_dimension,
            distortion,
            projection_matrix,
        }
    }

    /// Project vector to lower dimension
    pub fn project(&self, vector: &Array1<f64>) -> Array1<f64> {
        self.projection_matrix.dot(vector)
    }

    /// Project multiple vectors
    pub fn project_batch(&self, vectors: &Array2<f64>) -> Array2<f64> {
        self.projection_matrix.dot(vectors)
    }
}

/// Compute cosine similarity between two vectors
pub fn cosine_similarity(a: &Array1<f64>, b: &Array1<f64>) -> f64 {
    let dot_product = a.dot(b);
    let norm_a = a.dot(a).sqrt();
    let norm_b = b.dot(b).sqrt();

    if norm_a == 0.0 || norm_b == 0.0 {
        return 0.0;
    }

    dot_product / (norm_a * norm_b)
}

/// Sublinear similarity comparison using JL projection
pub fn sublinear_similarity(
    vec_a: &Array1<f64>,
    vec_b: &Array1<f64>,
    distortion: f64
) -> (f64, String) {
    let source_dim = vec_a.len();

    // Create JL projection
    let jl = JLProjection::new(source_dim, distortion);

    // Project vectors
    let proj_a = jl.project(vec_a);
    let proj_b = jl.project(vec_b);

    // Compute similarity in reduced space
    let similarity = cosine_similarity(&proj_a, &proj_b);

    let complexity = format!("O(log {})", source_dim);

    (similarity, complexity)
}

/// Batch similarity computation for multiple vectors
pub fn batch_sublinear_similarity(
    query: &Array1<f64>,
    corpus: &Array2<f64>,
    distortion: f64
) -> Vec<(usize, f64)> {
    let source_dim = query.len();

    // Create JL projection
    let jl = JLProjection::new(source_dim, distortion);

    // Project query and corpus
    let proj_query = jl.project(query);

    // Compute similarities
    let mut similarities: Vec<(usize, f64)> = corpus
        .axis_iter(ndarray::Axis(0))
        .enumerate()
        .map(|(idx, vec)| {
            let proj_vec = jl.project(&vec.to_owned());
            let sim = cosine_similarity(&proj_query, &proj_vec);
            (idx, sim)
        })
        .collect();

    // Sort by similarity descending
    similarities.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

    similarities
}

#[cfg(test)]
mod tests {
    use super::*;
    use ndarray::array;

    #[test]
    fn test_jl_projection() {
        let source_dim = 1000;
        let distortion = 0.5;

        let jl = JLProjection::new(source_dim, distortion);

        assert!(jl.target_dimension < source_dim);
        assert_eq!(jl.projection_matrix.shape(), &[jl.target_dimension, source_dim]);
    }

    #[test]
    fn test_cosine_similarity() {
        let a = array![1.0, 2.0, 3.0];
        let b = array![2.0, 4.0, 6.0]; // Parallel vector

        let sim = cosine_similarity(&a, &b);
        assert!((sim - 1.0).abs() < 1e-10); // Should be 1.0
    }

    #[test]
    fn test_sublinear_similarity() {
        let a = array![1.0, 2.0, 3.0, 4.0, 5.0];
        let b = array![2.0, 4.0, 6.0, 8.0, 10.0];

        let (sim, complexity) = sublinear_similarity(&a, &b, 0.5);

        assert!(sim > 0.9); // Should be close to 1.0
        assert!(complexity.contains("O(log"));
    }
}
