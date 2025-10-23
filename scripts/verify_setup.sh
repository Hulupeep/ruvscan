#!/bin/bash
# Simple setup verification

echo "🔍 RuvScan Setup Verification"
echo "=============================="
echo ""

# Check .env.local exists
if [ -f .env.local ]; then
    echo "✅ .env.local file exists"
    
    # Check for required variables (without loading)
    if grep -q "GITHUB_TOKEN=" .env.local && grep -q "OPENAI_API_KEY=" .env.local; then
        echo "✅ Required environment variables found"
    else
        echo "❌ Missing GITHUB_TOKEN or OPENAI_API_KEY in .env.local"
        exit 1
    fi
else
    echo "❌ .env.local not found"
    exit 1
fi

# Check Docker is available
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
else
    echo "❌ Docker not found"
    exit 1
fi

# Check Docker Compose
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1; then
    echo "✅ Docker Compose is installed"
else
    echo "❌ Docker Compose not found"
    exit 1
fi

# Check gh CLI
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI is installed"
else
    echo "⚠️  GitHub CLI not found (optional)"
fi

echo ""
echo "🎉 Setup verified! You're ready to:"
echo ""
echo "  1. Start RuvScan:"
echo "     docker-compose up -d"
echo ""
echo "  2. Check health:"
echo "     curl http://localhost:8000/health"
echo ""
echo "  3. Scan repositories:"
echo "     curl -X POST http://localhost:8000/scan \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"source_type\":\"org\",\"name\":\"ruvnet\",\"limit\":5}'"
echo ""
echo "  4. Query for leverage:"
echo "     curl -X POST http://localhost:8000/query \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"intent\":\"How to optimize AI performance?\",\"max_results\":5}'"
echo ""

