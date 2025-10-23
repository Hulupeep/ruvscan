"""
FACT (Framework for Autonomous Context Tracking) Cache Implementation
Deterministic reasoning trace and prompt replay
"""

import hashlib
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FACTCache:
    """
    Deterministic caching layer for reproducible reasoning
    Implements prompt replay and reasoning trace storage
    """

    def __init__(self, db_manager=None):
        self.db = db_manager
        self.version = "0.5.0"

    def generate_hash(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Generate deterministic hash for prompt + context

        Args:
            prompt: Input prompt text
            context: Optional context dictionary

        Returns:
            SHA256 hash string
        """
        content = prompt
        if context:
            # Sort keys for deterministic hashing
            content += json.dumps(context, sort_keys=True)

        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, prompt: str, context: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached response if exists

        Args:
            prompt: Input prompt
            context: Optional context

        Returns:
            Cached entry or None
        """
        if not self.db:
            return None

        try:
            cache_hash = self.generate_hash(prompt, context)
            entry = self.db.get_fact_cache(prompt)

            if entry:
                logger.info(f"FACT cache hit: {cache_hash[:16]}...")
                return entry

            logger.info(f"FACT cache miss: {cache_hash[:16]}...")
            return None

        except Exception as e:
            logger.error(f"FACT cache retrieval error: {e}")
            return None

    def set(
        self,
        prompt: str,
        response: str,
        context: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Store response in FACT cache

        Args:
            prompt: Input prompt
            response: Response to cache
            context: Optional context
            metadata: Additional metadata

        Returns:
            Cache hash
        """
        if not self.db:
            return ""

        try:
            cache_hash = self.generate_hash(prompt, context)

            # Prepare metadata
            cache_metadata = {
                "version": self.version,
                "timestamp": datetime.utcnow().isoformat(),
                "context": context,
                **(metadata or {})
            }

            # Store in database
            self.db.add_fact_cache(prompt, response, cache_metadata)

            logger.info(f"FACT cache stored: {cache_hash[:16]}...")
            return cache_hash

        except Exception as e:
            logger.error(f"FACT cache storage error: {e}")
            return ""

    def trace_reasoning(
        self,
        query: str,
        steps: List[Dict[str, Any]],
        final_result: str
    ) -> Dict[str, Any]:
        """
        Create reasoning trace for deterministic replay

        Args:
            query: Original query
            steps: List of reasoning steps
            final_result: Final reasoning output

        Returns:
            Reasoning trace dictionary
        """
        trace = {
            "query": query,
            "steps": steps,
            "final_result": final_result,
            "timestamp": datetime.utcnow().isoformat(),
            "version": self.version
        }

        # Store trace
        trace_json = json.dumps(trace, indent=2)
        self.set(
            prompt=f"reasoning_trace:{query}",
            response=trace_json,
            metadata={"type": "reasoning_trace", "steps_count": len(steps)}
        )

        return trace

    def replay_reasoning(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Replay cached reasoning trace

        Args:
            query: Original query

        Returns:
            Reasoning trace or None
        """
        entry = self.get(f"reasoning_trace:{query}")

        if not entry:
            return None

        try:
            trace = json.loads(entry['response'])
            logger.info(f"Replaying reasoning trace with {len(trace['steps'])} steps")
            return trace
        except Exception as e:
            logger.error(f"Error replaying reasoning trace: {e}")
            return None

    def validate_determinism(self, prompt: str, new_response: str) -> bool:
        """
        Validate that new response matches cached response (determinism check)

        Args:
            prompt: Input prompt
            new_response: New response to validate

        Returns:
            True if deterministic (matches cache)
        """
        cached = self.get(prompt)

        if not cached:
            # No cached version, store this one
            self.set(prompt, new_response)
            return True

        # Check if responses match
        cached_response = cached.get('response', '')
        is_deterministic = cached_response == new_response

        if not is_deterministic:
            logger.warning(f"Determinism violation detected for prompt: {prompt[:50]}...")

        return is_deterministic

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics

        Returns:
            Statistics dictionary
        """
        # TODO: Implement cache statistics from database
        return {
            "version": self.version,
            "total_entries": 0,
            "hit_rate": 0.0,
            "avg_response_size": 0
        }
