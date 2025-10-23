"""
Tests for FACT cache
"""

import pytest
from src.mcp.reasoning.fact_cache import FACTCache

@pytest.fixture
def fact_cache():
    """Create FACT cache instance"""
    return FACTCache()

def test_generate_hash(fact_cache):
    """Test hash generation"""
    prompt = "Test prompt"
    hash1 = fact_cache.generate_hash(prompt)
    hash2 = fact_cache.generate_hash(prompt)

    # Same input should produce same hash
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA256 hex length

def test_generate_hash_with_context(fact_cache):
    """Test hash generation with context"""
    prompt = "Test prompt"
    context = {"key": "value"}

    hash1 = fact_cache.generate_hash(prompt, context)
    hash2 = fact_cache.generate_hash(prompt, context)

    assert hash1 == hash2

    # Different context should produce different hash
    hash3 = fact_cache.generate_hash(prompt, {"key": "different"})
    assert hash1 != hash3

def test_cache_miss(fact_cache):
    """Test cache miss"""
    result = fact_cache.get("non_existent_prompt")
    assert result is None

def test_trace_reasoning(fact_cache):
    """Test reasoning trace creation"""
    query = "How can I optimize my AI?"
    steps = [
        {"step": "analysis", "description": "Analyzed query"},
        {"step": "search", "description": "Searched for solutions"}
    ]
    final_result = "Use sublinear algorithms"

    trace = fact_cache.trace_reasoning(query, steps, final_result)

    assert trace["query"] == query
    assert trace["steps"] == steps
    assert trace["final_result"] == final_result
    assert "timestamp" in trace
    assert trace["version"] == "0.5.0"

def test_validate_determinism(fact_cache):
    """Test determinism validation"""
    prompt = "test_prompt"
    response = "test_response"

    # First call should store and return True
    is_deterministic = fact_cache.validate_determinism(prompt, response)
    assert is_deterministic is True

def test_get_cache_stats(fact_cache):
    """Test cache statistics"""
    stats = fact_cache.get_cache_stats()

    assert "version" in stats
    assert "total_entries" in stats
    assert stats["version"] == "0.5.0"
