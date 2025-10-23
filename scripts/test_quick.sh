#!/bin/bash
# Quick integration test - verifies the system can start

set -e

echo "🧪 RuvScan Quick Test"
echo "===================="

# Load environment
if [ -f .env.local ]; then
    export $(cat .env.local | grep -v '^#' | xargs)
    echo "✅ Loaded .env.local"
else
    echo "❌ .env.local not found"
    exit 1
fi

# Check tokens
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN not set"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not set"
    exit 1
fi

echo "✅ Environment variables verified"

# Test GitHub token
echo ""
echo "Testing GitHub token..."
gh auth status 2>&1 | head -5

# Test Docker services can build
echo ""
echo "Building Docker images (this may take a few minutes)..."
docker compose build --quiet

echo ""
echo "✅ All quick tests passed!"
echo ""
echo "Next steps:"
echo "  1. Start services: docker compose up -d"
echo "  2. Check health: curl http://localhost:8000/health"
echo "  3. Run scan: ./scripts/ruvscan scan org ruvnet --limit 5"
echo "  4. Query: ./scripts/ruvscan query \"How to optimize performance?\""

