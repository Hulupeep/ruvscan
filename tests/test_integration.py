"""
Integration tests for RuvScan
Tests full workflows end-to-end
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
import httpx

from src.mcp.server import app
from src.mcp.storage.db import RuvScanDB
from src.mcp.reasoning.embeddings import EmbeddingService
from src.mcp.reasoning.fact_cache import FACTCache

client = TestClient(app)

@pytest.fixture
def test_db():
    """Create test database"""
    db = RuvScanDB(":memory:")
    yield db
    db.close()

@pytest.fixture
def embedding_service():
    """Create embedding service"""
    return EmbeddingService(provider="local")

@pytest.fixture
def fact_cache():
    """Create FACT cache"""
    return FACTCache()

def test_full_scan_workflow():
    """Test complete scan workflow"""
    # Step 1: Initiate scan
    scan_response = client.post("/scan", json={
        "source_type": "org",
        "source_name": "test-org",
        "limit": 10
    })
    assert scan_response.status_code == 200
    scan_data = scan_response.json()
    assert scan_data["status"] == "initiated"
    job_id = scan_data.get("job_id")

    # Step 2: Check scan status
    if job_id:
        status_response = client.get(f"/scan/{job_id}/status")
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert "status" in status_data

def test_full_query_workflow():
    """Test complete query workflow"""
    # Query for leverage
    query_response = client.post("/query", json={
        "intent": "How can I build a high-performance system?",
        "max_results": 5,
        "min_score": 0.7
    })

    assert query_response.status_code == 200
    cards = query_response.json()
    assert isinstance(cards, list)

    # Validate leverage card structure
    if len(cards) > 0:
        card = cards[0]
        assert "repo" in card
        assert "capabilities" in card
        assert "outside_box_reasoning" in card
        assert "relevance_score" in card

def test_compare_workflow():
    """Test repository comparison workflow"""
    compare_response = client.post("/compare", json={
        "repo_a": "test/repo-a",
        "repo_b": "test/repo-b"
    })

    assert compare_response.status_code == 200
    data = compare_response.json()
    assert "similarity_score" in data
    assert "complexity" in data

def test_cards_retrieval():
    """Test leverage cards retrieval"""
    cards_response = client.get("/cards", params={
        "limit": 10,
        "min_score": 0.5
    })

    assert cards_response.status_code == 200
    data = cards_response.json()
    assert "cards" in data
    assert "total" in data

@pytest.mark.asyncio
async def test_embedding_generation_integration(embedding_service):
    """Test embedding generation in workflow"""
    text = "This is a test repository for machine learning"
    embedding = await embedding_service.embed_text(text)

    assert embedding.shape[0] > 0
    assert not all(v == 0 for v in embedding)

def test_fact_cache_integration(fact_cache):
    """Test FACT cache in workflow"""
    prompt = "test_query"
    response = "test_response"

    # Set cache
    cache_hash = fact_cache.set(prompt, response)
    assert len(cache_hash) == 64

    # Get cache (if database available)
    # cached = fact_cache.get(prompt)
    # assert cached is not None

def test_database_integration(test_db):
    """Test database operations"""
    # Add repository
    repo_data = {
        "name": "test-repo",
        "org": "test-org",
        "full_name": "test-org/test-repo",
        "description": "Test repository",
        "stars": 100
    }

    repo_id = test_db.add_repo(repo_data)
    assert repo_id > 0

    # Retrieve repository
    repo = test_db.get_repo("test-org/test-repo")
    assert repo is not None
    assert repo["name"] == "test-repo"

    # Add leverage card
    card_data = {
        "repo_id": repo_id,
        "capabilities": ["test"],
        "summary": "Test summary",
        "reasoning": "Test reasoning",
        "relevance_score": 0.9
    }

    card_id = test_db.add_leverage_card(card_data)
    assert card_id > 0

def test_mcp_tools_list():
    """Test MCP tools listing"""
    response = client.get("/mcp/tools")
    assert response.status_code == 200

    data = response.json()
    assert "tools" in data
    assert len(data["tools"]) >= 4

    # Verify tool structure
    for tool in data["tools"]:
        assert "name" in tool
        assert "description" in tool
        assert "inputSchema" in tool

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.5.0"

def test_error_handling():
    """Test error handling"""
    # Invalid source type
    response = client.post("/scan", json={
        "source_type": "invalid",
        "source_name": "test",
        "limit": 10
    })
    assert response.status_code == 422

    # Empty intent
    response = client.post("/query", json={
        "intent": "",
        "max_results": 5
    })
    assert response.status_code == 422

def test_concurrent_requests():
    """Test concurrent request handling"""
    async def make_request():
        async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
            return await ac.get("/health")

    async def run_concurrent():
        tasks = [make_request() for _ in range(10)]
        responses = await asyncio.gather(*tasks)
        return responses

    responses = asyncio.run(run_concurrent())
    assert len(responses) == 10
    assert all(r.status_code == 200 for r in responses)

@pytest.mark.asyncio
async def test_async_operations():
    """Test async operations"""
    embedding_service = EmbeddingService(provider="local")

    texts = [
        "Repository for machine learning",
        "Web framework for Python",
        "Database management system"
    ]

    embeddings = await embedding_service.embed_batch(texts)
    assert len(embeddings) == len(texts)
    assert all(len(e) > 0 for e in embeddings)
