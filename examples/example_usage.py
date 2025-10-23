#!/usr/bin/env python3
"""
RuvScan Example Usage
Demonstrates how to use the RuvScan API programmatically
"""

import httpx
import json
import asyncio
from typing import List, Dict, Any

# Server configuration
RUVSCAN_SERVER = "http://localhost:8000"

class RuvScanClient:
    """Simple client for RuvScan API"""

    def __init__(self, base_url: str = RUVSCAN_SERVER):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=30.0)

    async def scan(self, source_type: str, source_name: str, limit: int = 50) -> Dict:
        """Trigger a scan"""
        response = await self.client.post("/scan", json={
            "source_type": source_type,
            "source_name": source_name,
            "limit": limit
        })
        response.raise_for_status()
        return response.json()

    async def query(
        self,
        intent: str,
        max_results: int = 10,
        min_score: float = 0.7
    ) -> List[Dict]:
        """Query for leverage"""
        response = await self.client.post("/query", json={
            "intent": intent,
            "max_results": max_results,
            "min_score": min_score
        })
        response.raise_for_status()
        return response.json()

    async def compare(self, repo_a: str, repo_b: str) -> Dict:
        """Compare two repositories"""
        response = await self.client.post("/compare", json={
            "repo_a": repo_a,
            "repo_b": repo_b
        })
        response.raise_for_status()
        return response.json()

    async def get_cards(self, limit: int = 50, min_score: float = 0.0) -> Dict:
        """Get saved leverage cards"""
        response = await self.client.get("/cards", params={
            "limit": limit,
            "min_score": min_score
        })
        response.raise_for_status()
        return response.json()

    async def close(self):
        """Close the client"""
        await self.client.aclose()

async def example_1_scan_organization():
    """Example 1: Scan a GitHub organization"""
    print("=" * 60)
    print("Example 1: Scanning GitHub Organization")
    print("=" * 60)

    client = RuvScanClient()

    try:
        # Scan ruvnet organization
        result = await client.scan(
            source_type="org",
            source_name="ruvnet",
            limit=20
        )

        print(f"\n✅ Scan initiated!")
        print(f"   Status: {result['status']}")
        print(f"   Source: {result['source_type']}/{result['source_name']}")
        print(f"   Repos: {result['estimated_repos']}")
        print(f"   Job ID: {result.get('job_id', 'N/A')}")

    finally:
        await client.close()

async def example_2_query_leverage():
    """Example 2: Query for leverage based on intent"""
    print("\n" + "=" * 60)
    print("Example 2: Querying for Leverage")
    print("=" * 60)

    client = RuvScanClient()

    try:
        # Query with specific intent
        intent = "How can I optimize context recall in my AI application?"
        print(f"\n🔍 Query: {intent}")

        cards = await client.query(
            intent=intent,
            max_results=5,
            min_score=0.7
        )

        print(f"\n📊 Found {len(cards)} leverage opportunities:\n")

        for i, card in enumerate(cards, 1):
            print(f"{i}. {card['repo']} (score: {card['relevance_score']:.2f})")
            print(f"   Capabilities: {', '.join(card['capabilities'])}")
            print(f"   💡 Insight: {card['outside_box_reasoning']}")
            print(f"   🔧 How to integrate: {card['integration_hint']}")
            if card.get('runtime_complexity'):
                print(f"   ⚡ Complexity: {card['runtime_complexity']}")
            print()

    finally:
        await client.close()

async def example_3_compare_repos():
    """Example 3: Compare two repositories"""
    print("=" * 60)
    print("Example 3: Comparing Repositories")
    print("=" * 60)

    client = RuvScanClient()

    try:
        # Compare two repos
        result = await client.compare(
            repo_a="ruvnet/sublinear-time-solver",
            repo_b="ruvnet/FACT"
        )

        print(f"\n🔀 Comparison Results:")
        print(f"   Repo A: {result['repo_a']}")
        print(f"   Repo B: {result['repo_b']}")
        print(f"   Similarity: {result['similarity_score']:.2f}")
        print(f"   Complexity: {result['complexity']}")
        print(f"   Analysis: {result['analysis']}")

    finally:
        await client.close()

async def example_4_workflow():
    """Example 4: Complete workflow"""
    print("\n" + "=" * 60)
    print("Example 4: Complete Workflow")
    print("=" * 60)

    client = RuvScanClient()

    try:
        # Step 1: Scan
        print("\n📡 Step 1: Scanning repositories...")
        scan_result = await client.scan("org", "ruvnet", 30)
        print(f"   ✅ Scan {scan_result['status']}")

        # Step 2: Wait a bit for processing (in real app, poll status)
        print("\n⏳ Step 2: Waiting for processing...")
        await asyncio.sleep(2)

        # Step 3: Query for insights
        print("\n🔍 Step 3: Querying for insights...")
        cards = await client.query(
            "Find tools for building high-performance AI systems",
            max_results=3
        )
        print(f"   ✅ Found {len(cards)} relevant tools")

        # Step 4: Compare top results
        if len(cards) >= 2:
            print("\n🔀 Step 4: Comparing top 2 results...")
            comparison = await client.compare(
                cards[0]['repo'],
                cards[1]['repo']
            )
            print(f"   ✅ Similarity: {comparison['similarity_score']:.2f}")

        print("\n✅ Workflow complete!")

    finally:
        await client.close()

async def main():
    """Run all examples"""
    print("\n🧠 RuvScan API Examples")
    print("=" * 60)

    try:
        # Check if server is running
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{RUVSCAN_SERVER}/health")
            if response.status_code != 200:
                print("❌ Server not responding. Please start the server:")
                print("   docker-compose up -d")
                print("   OR")
                print("   python -m uvicorn src.mcp.server:app --reload")
                return

        # Run examples
        await example_1_scan_organization()
        await example_2_query_leverage()
        await example_3_compare_repos()
        await example_4_workflow()

        print("\n" + "=" * 60)
        print("✨ All examples completed successfully!")
        print("=" * 60)

    except httpx.ConnectError:
        print("\n❌ Error: Could not connect to RuvScan server")
        print("Please ensure the server is running:")
        print("  docker-compose up -d")
        print("  OR")
        print("  python -m uvicorn src.mcp.server:app --reload")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
