"""
Embedding generation service
Supports OpenAI, Anthropic, and local models
"""

from typing import List, Optional, Dict, Any
import numpy as np
import logging
import os
from enum import Enum

logger = logging.getLogger(__name__)

class EmbeddingProvider(Enum):
    """Supported embedding providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"

class EmbeddingService:
    """
    Service for generating embeddings from text
    """

    def __init__(
        self,
        provider: str = "openai",
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None
    ):
        self.provider = EmbeddingProvider(provider)
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.dimension = 1536  # Default for OpenAI

        self._init_client()

    def _init_client(self):
        """Initialize the embedding client"""
        if self.provider == EmbeddingProvider.OPENAI:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info(f"Initialized OpenAI client with model {self.model}")
            except ImportError:
                logger.error("OpenAI package not installed")
                raise
        elif self.provider == EmbeddingProvider.ANTHROPIC:
            logger.warning("Anthropic embeddings not yet implemented")
            self.client = None
        else:
            logger.warning("Local embeddings not yet implemented")
            self.client = None

    async def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text

        Args:
            text: Input text

        Returns:
            Numpy array of embedding vector
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return np.zeros(self.dimension)

        try:
            if self.provider == EmbeddingProvider.OPENAI:
                return await self._embed_openai(text)
            else:
                # Fallback to random embedding for development
                logger.warning(f"Using random embedding for provider {self.provider}")
                return np.random.randn(self.dimension)

        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return np.zeros(self.dimension)

    async def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of input texts

        Returns:
            List of numpy arrays
        """
        embeddings = []

        # Process in batches for efficiency
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            if self.provider == EmbeddingProvider.OPENAI:
                batch_embeddings = await self._embed_openai_batch(batch)
                embeddings.extend(batch_embeddings)
            else:
                # Fallback
                for text in batch:
                    embeddings.append(np.random.randn(self.dimension))

        return embeddings

    async def _embed_openai(self, text: str) -> np.ndarray:
        """Generate OpenAI embedding"""
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )

            embedding = response.data[0].embedding
            return np.array(embedding, dtype=np.float64)

        except Exception as e:
            logger.error(f"OpenAI embedding error: {e}")
            raise

    async def _embed_openai_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Generate OpenAI embeddings in batch"""
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )

            embeddings = [
                np.array(data.embedding, dtype=np.float64)
                for data in response.data
            ]

            return embeddings

        except Exception as e:
            logger.error(f"OpenAI batch embedding error: {e}")
            raise

    def embed_repo_summary(self, repo_data: Dict[str, Any]) -> np.ndarray:
        """
        Generate embedding for repository summary

        Args:
            repo_data: Repository data dictionary

        Returns:
            Embedding vector
        """
        # Combine relevant fields
        text_parts = []

        if repo_data.get('name'):
            text_parts.append(f"Repository: {repo_data['name']}")

        if repo_data.get('description'):
            text_parts.append(f"Description: {repo_data['description']}")

        if repo_data.get('topics'):
            topics = ', '.join(repo_data['topics'])
            text_parts.append(f"Topics: {topics}")

        if repo_data.get('readme'):
            # Use first 1000 chars of README
            readme_excerpt = repo_data['readme'][:1000]
            text_parts.append(f"README: {readme_excerpt}")

        combined_text = "\n".join(text_parts)

        # Generate embedding synchronously for now
        # In production, this should be async
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.embed_text(combined_text))

    def cosine_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """
        Compute cosine similarity between two vectors

        Args:
            vec_a: First vector
            vec_b: Second vector

        Returns:
            Similarity score [0, 1]
        """
        dot_product = np.dot(vec_a, vec_b)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        similarity = dot_product / (norm_a * norm_b)

        # Normalize to [0, 1]
        return (similarity + 1) / 2

    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.dimension
