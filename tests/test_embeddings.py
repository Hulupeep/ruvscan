"""
Tests for embedding generation service
"""

import pytest
import numpy as np
from src.mcp.reasoning.embeddings import EmbeddingService

@pytest.fixture
def embedding_service():
    """Create embedding service instance"""
    # Use mock provider for testing
    return EmbeddingService(provider="local")

@pytest.mark.asyncio
async def test_embed_text(embedding_service):
    """Test single text embedding"""
    text = "This is a test repository for machine learning"
    embedding = await embedding_service.embed_text(text)

    assert isinstance(embedding, np.ndarray)
    assert embedding.shape[0] == embedding_service.dimension
    assert not np.all(embedding == 0)

@pytest.mark.asyncio
async def test_embed_empty_text(embedding_service):
    """Test embedding of empty text"""
    embedding = await embedding_service.embed_text("")

    assert isinstance(embedding, np.ndarray)
    assert embedding.shape[0] == embedding_service.dimension
    assert np.all(embedding == 0)

@pytest.mark.asyncio
async def test_embed_batch(embedding_service):
    """Test batch embedding"""
    texts = [
        "Machine learning framework",
        "Web development toolkit",
        "Data visualization library"
    ]

    embeddings = await embedding_service.embed_batch(texts)

    assert len(embeddings) == len(texts)
    for embedding in embeddings:
        assert isinstance(embedding, np.ndarray)
        assert embedding.shape[0] == embedding_service.dimension

def test_embed_repo_summary(embedding_service):
    """Test repository summary embedding"""
    repo_data = {
        "name": "test-repo",
        "description": "A test repository for machine learning",
        "topics": ["ml", "python", "tensorflow"],
        "readme": "This repository contains tools for building ML models..."
    }

    embedding = embedding_service.embed_repo_summary(repo_data)

    assert isinstance(embedding, np.ndarray)
    assert embedding.shape[0] == embedding_service.dimension

def test_cosine_similarity(embedding_service):
    """Test cosine similarity computation"""
    vec_a = np.array([1.0, 2.0, 3.0])
    vec_b = np.array([2.0, 4.0, 6.0])  # Parallel to vec_a

    similarity = embedding_service.cosine_similarity(vec_a, vec_b)

    assert 0.0 <= similarity <= 1.0
    assert similarity > 0.9  # Should be very similar

def test_cosine_similarity_orthogonal(embedding_service):
    """Test cosine similarity of orthogonal vectors"""
    vec_a = np.array([1.0, 0.0, 0.0])
    vec_b = np.array([0.0, 1.0, 0.0])

    similarity = embedding_service.cosine_similarity(vec_a, vec_b)

    assert abs(similarity - 0.5) < 0.1  # Should be ~0.5 after normalization

def test_get_dimension(embedding_service):
    """Test dimension getter"""
    dimension = embedding_service.get_dimension()
    assert dimension == 1536
