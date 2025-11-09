#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PATH="$SCRIPT_DIR/../.venv/bin/activate"

if [ -f "$VENV_PATH" ]; then
    # Prefer the project virtualenv when present
    # shellcheck disable=SC1090
    source "$VENV_PATH"
fi

if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo "⚠️  GITHUB_TOKEN is not set. GitHub scans will hit anonymous rate limits and may fail."
    echo "    Export a token (repo + read:org scopes) or add it to your MCP client config before continuing."
fi

echo ""
echo "🧠 RuvScan MCP Server"
echo "- Ships with the preloaded ruvnet/* repository catalog so you can query immediately."
echo "- Use the MCP scan tool or './scripts/ruvscan scan <org|user|topic> <name>' to ingest additional sources."
echo ""

exec ruvscan-mcp "$@"
