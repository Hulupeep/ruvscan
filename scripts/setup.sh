#!/bin/bash
# RuvScan Setup Script

set -e

echo "🧠 RuvScan Setup"
echo "================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi
echo "✅ Python $(python3 --version | cut -d' ' -f2)"

# Rust (optional)
if command -v cargo &> /dev/null; then
    echo "✅ Rust $(rustc --version | cut -d' ' -f2)"
else
    echo "⚠️  Rust not found (optional for development)"
fi

# Go (optional)
if command -v go &> /dev/null; then
    echo "✅ Go $(go version | cut -d' ' -f3)"
else
    echo "⚠️  Go not found (optional for development)"
fi

# Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker $(docker --version | cut -d' ' -f3 | tr -d ',')"
else
    echo "⚠️  Docker not found (optional for containerized deployment)"
fi

echo ""

# Create directories
echo "Creating directories..."
mkdir -p data logs config
echo "✅ Directories created"

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env created - please edit with your tokens"
else
    echo "✅ .env already exists"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Build Rust (if available)
if command -v cargo &> /dev/null; then
    echo ""
    echo "Building Rust sublinear engine..."
    cd src/rust
    cargo build --release
    cd ../..
    echo "✅ Rust engine built"
fi

# Build Go scanner (if available)
if command -v go &> /dev/null; then
    echo ""
    echo "Building Go scanner..."
    cd src/go
    go mod download
    go build -o ../../bin/scanner ./scanner
    cd ../..
    echo "✅ Go scanner built"
fi

# Initialize database
echo ""
echo "Initializing database..."
python -c "
from src.mcp.storage.db import RuvScanDB
db = RuvScanDB('data/ruvscan.db')
print('✅ Database initialized')
"

# Make CLI executable
chmod +x scripts/ruvscan

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GitHub token and API keys"
echo "2. Start the server:"
echo "   docker-compose up -d    (Docker)"
echo "   OR"
echo "   python -m uvicorn src.mcp.server:app --reload    (Manual)"
echo ""
echo "3. Test with CLI:"
echo "   ./scripts/ruvscan scan org ruvnet"
echo "   ./scripts/ruvscan query 'How can I speed up my AI context?'"
echo ""
