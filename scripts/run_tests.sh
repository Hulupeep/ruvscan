#!/bin/bash
# Run RuvScan test suite

set -e

echo "🧪 RuvScan Test Suite"
echo "===================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "${RED}❌ pytest not found. Installing...${NC}"
    pip install pytest pytest-asyncio pytest-cov
fi

echo "📋 Running unit tests..."
pytest tests/test_server.py -v

echo ""
echo "🔬 Running FACT cache tests..."
pytest tests/test_fact_cache.py -v

echo ""
echo "🧠 Running embedding tests..."
pytest tests/test_embeddings.py -v

echo ""
echo "🔗 Running integration tests..."
pytest tests/test_integration.py -v

echo ""
echo "📊 Generating coverage report..."
pytest tests/ --cov=src/mcp --cov-report=html --cov-report=term

echo ""
echo "${GREEN}✅ All tests passed!${NC}"
echo ""
echo "📈 Coverage report generated in htmlcov/index.html"
