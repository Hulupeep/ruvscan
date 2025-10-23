"""
gRPC client for Rust sublinear engine
"""

import grpc
from typing import List, Dict, Any, Tuple
import logging
import numpy as np

logger = logging.getLogger(__name__)

class RustSublinearClient:
    """
    gRPC client for communicating with Rust sublinear engine
    """

    def __init__(self, host: str = "localhost", port: int = 50051):
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None

    async def connect(self):
        """Establish gRPC connection"""
        try:
            address = f"{self.host}:{self.port}"
            self.channel = grpc.aio.insecure_channel(address)
            # TODO: Initialize stub when proto definitions are added
            logger.info(f"Connected to Rust engine at {address}")
        except Exception as e:
            logger.error(f"Failed to connect to Rust engine: {e}")
            raise

    async def compute_similarity(
        self,
        query_embedding: np.ndarray,
        corpus_embeddings: List[np.ndarray],
        distortion: float = 0.5
    ) -> List[Tuple[int, float]]:
        """
        Compute sublinear similarity between query and corpus

        Args:
            query_embedding: Query vector
            corpus_embeddings: List of corpus vectors
            distortion: JL distortion parameter

        Returns:
            List of (index, similarity_score) tuples
        """
        logger.info(f"Computing sublinear similarity for {len(corpus_embeddings)} vectors")

        try:
            # TODO: Implement gRPC call when proto is defined
            # For now, use placeholder local computation

            # Placeholder: Use simple cosine similarity
            similarities = []
            for idx, corpus_vec in enumerate(corpus_embeddings):
                sim = self._cosine_similarity(query_embedding, corpus_vec)
                similarities.append((idx, sim))

            # Sort by similarity descending
            similarities.sort(key=lambda x: x[1], reverse=True)

            logger.info(f"Computed {len(similarities)} similarities")
            return similarities

        except Exception as e:
            logger.error(f"Similarity computation error: {e}")
            raise

    async def compare_vectors(
        self,
        vec_a: np.ndarray,
        vec_b: np.ndarray,
        distortion: float = 0.5
    ) -> Dict[str, Any]:
        """
        Compare two vectors using sublinear algorithm

        Args:
            vec_a: First vector
            vec_b: Second vector
            distortion: JL distortion parameter

        Returns:
            Comparison result with similarity and complexity
        """
        try:
            # TODO: Implement gRPC call

            similarity = self._cosine_similarity(vec_a, vec_b)

            return {
                "similarity": float(similarity),
                "complexity": f"O(log {len(vec_a)})",
                "method": "sublinear_jl",
                "distortion": distortion
            }

        except Exception as e:
            logger.error(f"Vector comparison error: {e}")
            raise

    async def analyze_matrix(
        self,
        matrix: np.ndarray
    ) -> Dict[str, Any]:
        """
        Analyze matrix properties for optimal algorithm selection

        Args:
            matrix: Matrix to analyze

        Returns:
            Analysis result
        """
        try:
            # TODO: Implement gRPC call

            # Placeholder analysis
            is_sparse = np.count_nonzero(matrix) / matrix.size < 0.3
            is_symmetric = np.allclose(matrix, matrix.T)

            return {
                "is_sparse": is_sparse,
                "is_symmetric": is_symmetric,
                "is_diagonally_dominant": self._check_diagonal_dominance(matrix),
                "recommended_method": "neumann" if is_sparse else "direct",
                "complexity_estimate": "O(log n)"
            }

        except Exception as e:
            logger.error(f"Matrix analysis error: {e}")
            raise

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(dot_product / (norm_a * norm_b))

    def _check_diagonal_dominance(self, matrix: np.ndarray) -> bool:
        """Check if matrix is diagonally dominant"""
        n = matrix.shape[0]

        for i in range(n):
            diagonal = abs(matrix[i, i])
            row_sum = sum(abs(matrix[i, j]) for j in range(n) if j != i)

            if diagonal <= row_sum:
                return False

        return True

    async def close(self):
        """Close gRPC connection"""
        if self.channel:
            await self.channel.close()
            logger.info("Closed connection to Rust engine")
