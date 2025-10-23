"""
SAFLA (Symbolic Analogical Framework for Lateral Analysis) Agent
Generates outside-the-box reasoning and creative leverage insights
"""

from typing import Dict, List, Any, Optional
import logging
import json

logger = logging.getLogger(__name__)

class SAFLAAgent:
    """
    Analogical reasoning agent for generating creative reuse insights
    """

    def __init__(self, fact_cache=None):
        self.fact_cache = fact_cache
        self.reasoning_domains = [
            "algorithmic",
            "architectural",
            "performance",
            "scalability",
            "integration",
            "domain_transfer"
        ]

    async def generate_outside_box_reasoning(
        self,
        repo_summary: str,
        query_intent: str,
        repo_capabilities: List[str]
    ) -> Dict[str, Any]:
        """
        Generate outside-the-box reasoning for how a repo could be reused

        Args:
            repo_summary: Repository summary
            query_intent: User's intent/problem statement
            repo_capabilities: List of repo capabilities

        Returns:
            Reasoning result with insights
        """
        logger.info(f"Generating SAFLA reasoning for query: {query_intent[:50]}...")

        # Check FACT cache first
        cache_key = f"safla:{query_intent}:{repo_summary[:100]}"
        if self.fact_cache:
            cached = self.fact_cache.get(cache_key)
            if cached:
                logger.info("SAFLA reasoning retrieved from FACT cache")
                return json.loads(cached['response'])

        # Generate reasoning (placeholder - would use LLM in production)
        reasoning = await self._analogical_inference(
            repo_summary,
            query_intent,
            repo_capabilities
        )

        result = {
            "outside_box_reasoning": reasoning['primary_insight'],
            "integration_hint": reasoning['integration_strategy'],
            "analogical_domains": reasoning['domains'],
            "confidence": reasoning['confidence'],
            "reasoning_chain": reasoning['chain']
        }

        # Store in FACT cache
        if self.fact_cache:
            self.fact_cache.set(
                cache_key,
                json.dumps(result),
                metadata={"type": "safla_reasoning"}
            )

        return result

    async def _analogical_inference(
        self,
        repo_summary: str,
        query_intent: str,
        capabilities: List[str]
    ) -> Dict[str, Any]:
        """
        Perform analogical inference using cross-domain mapping

        Args:
            repo_summary: Repository summary
            query_intent: User intent
            capabilities: Repository capabilities

        Returns:
            Inference result
        """
        # TODO: Integrate with LLM for actual analogical reasoning
        # This is a placeholder implementation

        # Extract key concepts from intent
        intent_concepts = self._extract_concepts(query_intent)

        # Map capabilities to domains
        domain_mappings = self._map_to_domains(capabilities)

        # Generate creative transfer insights
        insights = self._generate_transfer_insights(
            intent_concepts,
            domain_mappings,
            repo_summary
        )

        return {
            "primary_insight": insights['primary'],
            "integration_strategy": insights['strategy'],
            "domains": domain_mappings,
            "confidence": insights['confidence'],
            "chain": insights['reasoning_steps']
        }

    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        # Simplified concept extraction
        keywords = [
            "speed", "performance", "optimize", "scale",
            "context", "memory", "recall", "search",
            "api", "latency", "throughput", "real-time"
        ]

        concepts = []
        text_lower = text.lower()

        for keyword in keywords:
            if keyword in text_lower:
                concepts.append(keyword)

        return concepts

    def _map_to_domains(self, capabilities: List[str]) -> List[str]:
        """Map capabilities to reasoning domains"""
        domain_map = {
            "solver": ["algorithmic", "performance"],
            "O(log n)": ["algorithmic", "scalability"],
            "context": ["architectural", "integration"],
            "caching": ["performance", "scalability"],
            "MCP": ["integration", "architectural"]
        }

        domains = set()
        for cap in capabilities:
            cap_lower = cap.lower()
            for key, mapped_domains in domain_map.items():
                if key in cap_lower:
                    domains.update(mapped_domains)

        return list(domains)

    def _generate_transfer_insights(
        self,
        intent_concepts: List[str],
        domains: List[str],
        repo_summary: str
    ) -> Dict[str, Any]:
        """Generate creative transfer insights"""

        # Placeholder implementation
        # In production, this would use LLM with carefully crafted prompts

        primary_insight = (
            "This technology could be repurposed by applying its core algorithmic "
            "approach to your use case, even though the original implementation "
            "was designed for a different domain."
        )

        if "performance" in intent_concepts and "algorithmic" in domains:
            primary_insight = (
                "The sublinear algorithmic approach could replace linear operations "
                "in your system, achieving exponential speedup through dimensional "
                "reduction and probabilistic guarantees."
            )

        strategy = "Integrate as MCP tool or standalone service with API bridge"

        if "MCP" in repo_summary or "integration" in domains:
            strategy = "Direct MCP integration - install via npx and call from agent workflow"

        return {
            "primary": primary_insight,
            "strategy": strategy,
            "confidence": 0.85,
            "reasoning_steps": [
                "Identified domain overlap",
                "Mapped algorithmic primitives",
                "Generated creative transfer",
                "Validated integration path"
            ]
        }

    def generate_leverage_card(
        self,
        repo_data: Dict[str, Any],
        query_intent: str,
        similarity_score: float
    ) -> Dict[str, Any]:
        """
        Generate complete leverage card with SAFLA reasoning

        Args:
            repo_data: Repository data
            query_intent: User intent
            similarity_score: Sublinear similarity score

        Returns:
            Leverage card dictionary
        """
        # Extract capabilities
        capabilities = repo_data.get('capabilities', [])
        if not capabilities:
            capabilities = self._infer_capabilities(repo_data)

        # Generate outside-box reasoning
        # This would be async in production with LLM calls
        reasoning_result = {
            "outside_box_reasoning": "Creative reuse insight",
            "integration_hint": "Integration strategy",
            "analogical_domains": ["algorithmic"],
            "confidence": 0.85,
            "reasoning_chain": []
        }

        card = {
            "repo": repo_data['full_name'],
            "capabilities": capabilities,
            "summary": repo_data.get('description', 'No description'),
            "outside_box_reasoning": reasoning_result['outside_box_reasoning'],
            "integration_hint": reasoning_result['integration_hint'],
            "relevance_score": similarity_score,
            "runtime_complexity": self._infer_complexity(repo_data),
            "cached": True
        }

        return card

    def _infer_capabilities(self, repo_data: Dict[str, Any]) -> List[str]:
        """Infer capabilities from repo data"""
        capabilities = []

        description = (repo_data.get('description', '') + ' ' +
                      repo_data.get('readme', '')[:500]).lower()

        capability_keywords = {
            "solver": ["solve", "solver", "solution"],
            "O(log n)": ["sublinear", "logarithmic", "o(log"],
            "caching": ["cache", "caching", "memoiz"],
            "MCP": ["mcp", "model context protocol"],
            "API": ["api", "rest", "graphql"],
            "ML": ["machine learning", "neural", "model"]
        }

        for cap, keywords in capability_keywords.items():
            if any(kw in description for kw in keywords):
                capabilities.append(cap)

        return capabilities or ["general purpose"]

    def _infer_complexity(self, repo_data: Dict[str, Any]) -> Optional[str]:
        """Infer runtime complexity from repo data"""
        text = (repo_data.get('description', '') + ' ' +
               repo_data.get('readme', '')[:500]).lower()

        complexity_patterns = [
            ("O(log n)", ["o(log", "sublinear", "logarithmic"]),
            ("O(n)", ["linear time", "o(n)"]),
            ("O(n²)", ["quadratic", "o(n^2)", "o(n2)"]),
            ("O(1)", ["constant time", "o(1)"])
        ]

        for complexity, patterns in complexity_patterns:
            if any(p in text for p in patterns):
                return complexity

        return None
