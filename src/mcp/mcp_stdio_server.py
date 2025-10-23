#!/usr/bin/env python3
"""
RuvScan MCP Server (STDIO Transport)
For use with Claude Code CLI, Codex, and Claude Desktop
"""

import asyncio
import os
import sys
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("ruvscan")

# Get API endpoint from environment (defaults to localhost if running locally)
RUVSCAN_API = os.getenv("RUVSCAN_API_URL", "http://localhost:8000")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")


@mcp.tool()
async def scan_github(
    source_type: str,
    source_name: str,
    limit: int = 50
) -> str:
    """Scan GitHub organization, user, or topic for repositories.

    Args:
        source_type: Type of source - 'org', 'user', or 'topic'
        source_name: Name of the organization, user, or topic keyword
        limit: Maximum number of repositories to scan (default: 50)
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{RUVSCAN_API}/scan",
                json={
                    "source_type": source_type,
                    "source_name": source_name,
                    "limit": limit
                },
                headers={"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()

            return f"""Scan initiated for {source_type}: {source_name}
Status: {data.get('status', 'unknown')}
Estimated repositories: {data.get('estimated_repos', limit)}
Message: {data.get('message', 'Processing')}
"""
        except Exception as e:
            return f"Error scanning GitHub: {str(e)}"


@mcp.tool()
async def query_leverage(
    intent: str,
    max_results: int = 10,
    min_score: float = 0.7
) -> str:
    """Query for leverage opportunities based on your intent or problem.

    Args:
        intent: Your problem statement or what you're trying to build
        max_results: Maximum number of results to return (default: 10)
        min_score: Minimum relevance score from 0-1 (default: 0.7)
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{RUVSCAN_API}/query",
                json={
                    "intent": intent,
                    "max_results": max_results,
                    "min_score": min_score
                },
                timeout=30.0
            )
            response.raise_for_status()
            cards = response.json()

            if not cards:
                return f"No leverage opportunities found for: {intent}"

            results = []
            for card in cards:
                result = f"""
Repository: {card['repo']}
Relevance Score: {card['relevance_score']:.2f}
Complexity: {card.get('runtime_complexity', 'N/A')}

Summary: {card['summary']}

Why This Helps: {card['outside_box_reasoning']}

How to Use: {card['integration_hint']}

Capabilities: {', '.join(card['capabilities'])}
{'(Cached Result)' if card.get('cached') else ''}
"""
                results.append(result)

            return "\n" + "="*80 + "\n".join(results)

        except Exception as e:
            return f"Error querying leverage: {str(e)}"


@mcp.tool()
async def compare_repositories(
    repo_a: str,
    repo_b: str
) -> str:
    """Compare two GitHub repositories using sublinear similarity.

    Args:
        repo_a: First repository in format 'org/repo'
        repo_b: Second repository in format 'org/repo'
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{RUVSCAN_API}/compare",
                json={
                    "repo_a": repo_a,
                    "repo_b": repo_b
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()

            return f"""
Repository Comparison (O(log n) complexity)

{repo_a} vs {repo_b}

Similarity Score: {data.get('similarity_score', 0):.2f}
Complexity: {data.get('complexity', 'O(log n)')}

Analysis: {data.get('analysis', 'Comparison complete')}
"""
        except Exception as e:
            return f"Error comparing repositories: {str(e)}"


@mcp.tool()
async def analyze_reasoning(repo: str) -> str:
    """Analyze and replay the reasoning chain for a repository using FACT cache.

    Args:
        repo: Repository name in format 'org/repo'
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{RUVSCAN_API}/analyze",
                params={"repo": repo},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()

            trace = data.get('reasoning_trace', [])
            if not trace:
                return f"No reasoning trace available for {repo}"

            result = f"Reasoning Chain for {repo}:\n\n"
            for step in trace:
                result += f"- {step}\n"

            if data.get('cached'):
                result += "\n(Retrieved from FACT deterministic cache)"

            return result

        except Exception as e:
            return f"Error analyzing reasoning: {str(e)}"


@mcp.resource("ruvscan://status")
async def get_status() -> str:
    """Get RuvScan server status and health."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{RUVSCAN_API}/health", timeout=5.0)
            response.raise_for_status()
            data = response.json()

            return f"""RuvScan Server Status

Status: {data.get('status', 'unknown')}
Version: {data.get('version', '0.5.0')}
Service: {data.get('service', 'RuvScan MCP Server')}
API Endpoint: {RUVSCAN_API}
"""
        except Exception as e:
            return f"Server unreachable: {str(e)}\n\nMake sure the RuvScan API server is running:\ndocker-compose up -d"


def main():
    """Run the MCP server using stdio transport."""
    # Initialize and run the server
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
