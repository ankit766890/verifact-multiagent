from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class VerdictType(str, Enum):
    VERIFIED_TRUE = "VERIFIED_TRUE"
    VERIFIED_FALSE = "VERIFIED_FALSE"
    MISLEADING = "MISLEADING"
    UNVERIFIED = "UNVERIFIED"
    CONFLICTING_EVIDENCE = "CONFLICTING_EVIDENCE"


class EvidenceType(str, Enum):
    PEER_REVIEWED = "PEER_REVIEWED"
    OFFICIAL_GOVERNMENT = "OFFICIAL_GOVERNMENT"
    NEWS_ORGANIZATION = "NEWS_ORGANIZATION"
    ACADEMIC_INSTITUTION = "ACADEMIC_INSTITUTION"
    ENCYCLOPEDIC = "ENCYCLOPEDIC"
    SOCIAL_OR_UNVERIFIED = "SOCIAL_OR_UNVERIFIED"


class EvidenceSource(BaseModel):
    title: str = Field(..., min_length=2, max_length=250)
    url: str = Field(..., pattern=r"^https?://")
    snippet: str = Field(..., min_length=5, max_length=1500)
    source_type: EvidenceType = Field(default=EvidenceType.NEWS_ORGANIZATION)
    credibility_score: float = Field(..., ge=0.0, le=1.0)
    published_date: Optional[str] = None


class AtomicClaim(BaseModel):
    claim_id: str
    original_text: str
    normalized_claim: str
    topic_category: str
    requires_temporal_context: bool = False
    entities: List[str] = Field(default_factory=list)


class ClaimVerificationResult(BaseModel):
    claim_id: str
    claim_text: str
    verdict: VerdictType
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    corroborating_evidence: List[EvidenceSource] = Field(default_factory=list)
    contradicting_evidence: List[EvidenceSource] = Field(default_factory=list)
    red_team_critique: str
    mitigation_notes: Optional[str] = None


class PipelineExecutionMetric(BaseModel):
    agent_name: str
    duration_ms: float
    status: str
    items_processed: int


class ResearchDossier(BaseModel):
    query_id: str
    raw_query: str
    claims_analyzed: int
    overall_verdict: VerdictType
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    executive_summary: str
    detailed_claims: List[ClaimVerificationResult]
    audit_trail: List[PipelineExecutionMetric] = Field(default_factory=list)
    meta: Dict[str, Any] = Field(default_factory=dict)
