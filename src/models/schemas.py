from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ExecutionMode(str, Enum):
    PIPELINE = "PIPELINE"       # All 4 agents work cooperatively
    PLANNER_ONLY = "PLANNER"    # Only Agent 1 (Decomposition & Entity Extraction)
    EVIDENCE_ONLY = "EVIDENCE"  # Only Agent 2 (Primary Domain Search & Trust Scoring)
    REDTEAM_ONLY = "REDTEAM"    # Only Agent 3 (Adversarial Fallacy & Bias Audit)


class VerdictType(str, Enum):
    VERIFIED_TRUE = "VERIFIED_TRUE"
    VERIFIED_FALSE = "VERIFIED_FALSE"
    MISLEADING = "MISLEADING"
    UNVERIFIED = "UNVERIFIED"
    CONTEXT_REQUIRED = "CONTEXT_REQUIRED"


class FallacyType(str, Enum):
    CHERRY_PICKING = "Cherry-Picking (Suppressed Evidence)"
    APPEAL_TO_FALSE_AUTHORITY = "Appeal to False Authority"
    FALSE_DILEMMA = "False Dilemma / Bifurcation"
    HASTY_GENERALIZATION = "Hasty Generalization"
    POST_HOC = "Post Hoc Ergo Propter Hoc (False Cause)"
    CIRCULAR_REASONING = "Circular Reasoning (Begging the Question)"
    APPEAL_TO_EMOTION_OR_FEAR = "Sensationalism / Appeal to Emotion"
    NONE_DETECTED = "None Detected"


class EvidenceType(str, Enum):
    PEER_REVIEWED = "PEER_REVIEWED"
    OFFICIAL_GOVERNMENT = "OFFICIAL_GOVERNMENT"
    ACADEMIC_INSTITUTION = "ACADEMIC_INSTITUTION"
    TIER1_JOURNALISM = "TIER1_JOURNALISM"
    FACT_CHECK_REGISTRY = "FACT_CHECK_REGISTRY"
    GENERAL_WEB = "GENERAL_WEB"


class EvidenceSource(BaseModel):
    title: str = Field(..., min_length=2, max_length=300)
    url: str = Field(..., pattern=r"^https?://")
    snippet: str = Field(..., min_length=5, max_length=2000)
    source_type: EvidenceType = Field(default=EvidenceType.TIER1_JOURNALISM)
    credibility_score: float = Field(..., ge=0.0, le=1.0)
    published_date: Optional[str] = None
    domain: str = ""


class AtomicClaim(BaseModel):
    claim_id: str
    original_text: str
    normalized_claim: str
    topic_category: str
    requires_temporal_context: bool = False
    temporal_anchor: Optional[str] = None
    entities: List[str] = Field(default_factory=list)
    confidence_weight: float = Field(default=1.0, ge=0.1, le=2.0)


class FallacyAssessment(BaseModel):
    detected: bool
    fallacy_type: FallacyType = FallacyType.NONE_DETECTED
    explanation: str
    severity_score: float = Field(default=0.0, ge=0.0, le=1.0)


class ClaimVerificationResult(BaseModel):
    claim_id: str
    claim_text: str
    verdict: VerdictType
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    topic_category: str
    corroborating_evidence: List[EvidenceSource] = Field(default_factory=list)
    contradicting_evidence: List[EvidenceSource] = Field(default_factory=list)
    fallacy_analysis: FallacyAssessment
    adversarial_critique: str
    epistemic_certainty: str


class PipelineExecutionMetric(BaseModel):
    agent_name: str
    duration_ms: float
    status: str
    items_processed: int
    memory_footprint_kb: float = 0.0


class ResearchDossier(BaseModel):
    query_id: str
    timestamp: str
    raw_query: str
    execution_mode: ExecutionMode = ExecutionMode.PIPELINE
    claims_analyzed: int
    overall_verdict: VerdictType
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    verdict_badge_color: str
    executive_summary: str
    detailed_claims: List[ClaimVerificationResult]
    audit_trail: List[PipelineExecutionMetric]
    meta: Dict[str, Any] = Field(default_factory=dict)
