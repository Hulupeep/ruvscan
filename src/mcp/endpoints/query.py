"""
Query endpoint implementation
Handles leverage discovery queries
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import logging
import numpy as np

from ..reasoning.embeddings import EmbeddingService
from ..reasoning.fact_cache import FACTCache
from ..reasoning.safla_agent import SAFLAAgent
from ..bindings.rust_client import RustSublinearClient
from ..storage.db import RuvScanDB
from ..storage.models import LeverageCard

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
embedding_service = EmbeddingService()
fact_cache = FACTCache()
safla_agent = SAFLAAgent(fact_cache)
rust_client = RustSublinearClient()

class QueryRequest(BaseModel):
    """Request to query for leverage"""
    intent: str = Field(..., min_length=10)
    max_results: int = Field(10, gt=0, le=100)
    min_score: float = Field(0.7, ge=0.0, le=1.0)

@router.post("/query", response_model=List[LeverageCard])
async def query_leverage(request: QueryRequest):
    """
    Query for leverage cards based on user intent

    Uses sublinear similarity and SAFLA reasoning to find relevant repos
    """
    logger.info(f"Querying intent: {request.intent[:100]}...")

    try:
        # Check FACT cache first
        cached = fact_cache.get(f"query:{request.intent}")
        if cached:
            logger.info("Returning cached query results")
            import json
            return json.loads(cached['response'])

        # Generate embedding for intent
        logger.info("Generating embedding for query intent")
        intent_embedding = await embedding_service.embed_text(request.intent)

        # Get all repo embeddings from database
        # TODO: Implement database retrieval
        # For now, create mock data
        mock_repos = create_mock_repos()

        # Compute similarities using Rust engine
        logger.info(f"Computing sublinear similarity against {len(mock_repos)} repos")
        corpus_embeddings = [repo['embedding'] for repo in mock_repos]

        similarities = await rust_client.compute_similarity(
            intent_embedding,
            corpus_embeddings,
            distortion=0.5
        )

        # Filter by minimum score
        filtered = [
            (idx, score) for idx, score in similarities
            if score >= request.min_score
        ][:request.max_results]

        logger.info(f"Found {len(filtered)} repos above threshold {request.min_score}")

        # Generate leverage cards with SAFLA reasoning
        leverage_cards = []
        for idx, score in filtered:
            repo_data = mock_repos[idx]

            # Generate SAFLA reasoning
            card = safla_agent.generate_leverage_card(
                repo_data=repo_data,
                query_intent=request.intent,
                similarity_score=score
            )

            leverage_cards.append(LeverageCard(**card))

        # Cache results
        import json
        fact_cache.set(
            f"query:{request.intent}",
            json.dumps([card.dict() for card in leverage_cards]),
            metadata={"query_length": len(request.intent)}
        )

        logger.info(f"Returning {len(leverage_cards)} leverage cards")
        return leverage_cards

    except Exception as e:
        logger.error(f"Query error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

def create_mock_repos() -> List[dict]:
    """Create mock repository data for testing"""
    return [
        {
            "id": 1,
            "full_name": "ruvnet/sublinear-time-solver",
            "name": "sublinear-time-solver",
            "org": "ruvnet",
            "description": "TRUE O(log n) matrix solver with consciousness exploration",
            "capabilities": ["O(log n) solving", "WASM acceleration", "MCP integration"],
            "embedding": np.random.randn(1536),
            "stars": 150,
            "language": "Rust"
        },
        {
            "id": 2,
            "full_name": "ruvnet/FACT",
            "name": "FACT",
            "org": "ruvnet",
            "description": "Framework for Autonomous Context Tracking - deterministic caching",
            "capabilities": ["Deterministic caching", "Prompt replay", "Context management"],
            "embedding": np.random.randn(1536),
            "stars": 85,
            "language": "Python"
        },
        {
            "id": 3,
            "full_name": "ruvnet/MidStream",
            "name": "MidStream",
            "org": "ruvnet",
            "description": "Real-time streaming and inflight data processing",
            "capabilities": ["Streaming", "Real-time processing", "Async channels"],
            "embedding": np.random.randn(1536),
            "stars": 120,
            "language": "Rust"
        }
    ]
