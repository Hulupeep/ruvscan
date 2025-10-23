"""
Pydantic models for RuvScan data structures
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Repository(BaseModel):
    """Repository model"""
    id: Optional[int] = None
    name: str
    org: str
    full_name: str
    description: Optional[str] = None
    topics: List[str] = []
    readme: Optional[str] = None
    embedding: Optional[bytes] = None
    sublinear_hash: Optional[str] = None
    stars: int = 0
    language: Optional[str] = None
    last_scan: Optional[datetime] = None
    created_at: Optional[datetime] = None

class LeverageCard(BaseModel):
    """Leverage card model"""
    id: Optional[int] = None
    repo_id: int
    repo: Optional[str] = None
    capabilities: List[str]
    summary: str
    reasoning: str = Field(..., alias='outside_box_reasoning')
    integration_hint: Optional[str] = None
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    runtime_complexity: Optional[str] = None
    query_intent: Optional[str] = None
    cached: bool = True
    created_at: Optional[datetime] = None

    class Config:
        populate_by_name = True

class FACTCacheEntry(BaseModel):
    """FACT cache entry model"""
    id: Optional[int] = None
    hash: str
    prompt: str
    response: str
    version: str = "0.5.0"
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

class ScanJob(BaseModel):
    """Scan job configuration"""
    source_type: str = Field(..., pattern="^(org|user|topic)$")
    source_name: str
    limit: int = Field(50, gt=0, le=1000)
    status: str = "pending"
    repos_found: int = 0
    repos_processed: int = 0

class SublinearComparison(BaseModel):
    """Result of sublinear comparison"""
    repo_a: str
    repo_b: str
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    complexity: str = "O(log n)"
    method_used: str = "sublinear_neumann"
    computation_time_ms: Optional[float] = None

class ReasoningTrace(BaseModel):
    """Reasoning trace for FACT replay"""
    repo: str
    steps: List[Dict[str, Any]] = []
    final_reasoning: str
    cached: bool = False
    confidence_score: float = Field(..., ge=0.0, le=1.0)
