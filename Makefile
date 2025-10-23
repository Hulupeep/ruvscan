# RuvScan Makefile

.PHONY: help setup install build test clean docker-build docker-up docker-down run-python run-rust run-go

help: ## Show this help message
	@echo "RuvScan - Sublinear-intelligence MCP server"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

setup: ## Run setup script
	@bash scripts/setup.sh

install: ## Install all dependencies
	pip install -r requirements.txt
	cd src/rust && cargo build --release
	cd src/go && go mod download

build: ## Build all components
	@echo "Building Rust engine..."
	cd src/rust && cargo build --release
	@echo "Building Go scanner..."
	cd src/go && go build -o ../../bin/scanner ./scanner
	@echo "✅ Build complete"

test: ## Run tests
	@echo "Running Python tests..."
	pytest tests/
	@echo "Running Rust tests..."
	cd src/rust && cargo test
	@echo "✅ Tests complete"

clean: ## Clean build artifacts
	rm -rf data/*.db
	rm -rf logs/*.log
	rm -rf bin/*
	cd src/rust && cargo clean
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Clean complete"

docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start Docker containers
	docker-compose up -d
	@echo "✅ RuvScan started"
	@echo "   MCP Server: http://localhost:8000"
	@echo "   Rust Engine: localhost:50051"

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

run-python: ## Run Python MCP server
	python -m uvicorn src.mcp.server:app --reload --host 0.0.0.0 --port 8000

run-rust: ## Run Rust sublinear engine
	cd src/rust && cargo run --release

run-go: ## Run Go scanner
	cd src/go/scanner && go run main.go

scan: ## Quick scan example (org: ruvnet)
	./scripts/ruvscan scan org ruvnet --limit 20

query-example: ## Example query
	./scripts/ruvscan query "How can I speed up context recall in my AI system?"

init-db: ## Initialize database
	python -c "from src.mcp.storage.db import RuvScanDB; RuvScanDB('data/ruvscan.db')"

format: ## Format code
	black src/mcp
	cd src/rust && cargo fmt
	gofmt -w src/go/scanner/*.go

lint: ## Lint code
	ruff check src/mcp
	cd src/rust && cargo clippy
	cd src/go && go vet ./...

dev: docker-up ## Start development environment
	@echo "Development environment ready!"
