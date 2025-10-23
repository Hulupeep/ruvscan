"""
Tests for RuvScan MCP server
"""

import pytest
from fastapi.testclient import TestClient
from src.mcp.server import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.5.0"
    assert data["service"] == "RuvScan MCP Server"

def test_mcp_tools_list():
    """Test MCP tools listing"""
    response = client.get("/mcp/tools")
    assert response.status_code == 200
    data = response.json()
    assert "tools" in data
    assert len(data["tools"]) > 0

    # Check for required tools
    tool_names = [tool["name"] for tool in data["tools"]]
    assert "scan" in tool_names
    assert "query" in tool_names
    assert "compare" in tool_names
    assert "analyze" in tool_names

def test_scan_endpoint():
    """Test scan endpoint"""
    response = client.post("/scan", json={
        "source_type": "org",
        "source_name": "ruvnet",
        "limit": 10
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "initiated"
    assert data["source_type"] == "org"
    assert data["source_name"] == "ruvnet"

def test_query_endpoint():
    """Test query endpoint"""
    response = client.post("/query", json={
        "intent": "How can I speed up my context system?",
        "max_results": 5,
        "min_score": 0.7
    })
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_compare_endpoint():
    """Test compare endpoint"""
    response = client.post("/compare", json={
        "repo_a": "ruvnet/sublinear-time-solver",
        "repo_b": "ruvnet/FACT"
    })
    assert response.status_code == 200
    data = response.json()
    assert "repo_a" in data
    assert "repo_b" in data
    assert "similarity_score" in data

def test_cards_endpoint():
    """Test cards endpoint"""
    response = client.get("/cards", params={
        "limit": 10,
        "min_score": 0.5
    })
    assert response.status_code == 200
    data = response.json()
    assert "cards" in data
    assert "total" in data

def test_invalid_scan_type():
    """Test invalid scan type"""
    response = client.post("/scan", json={
        "source_type": "invalid",
        "source_name": "test",
        "limit": 10
    })
    assert response.status_code == 422  # Validation error
