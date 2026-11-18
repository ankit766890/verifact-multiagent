import uuid
from typing import List, Dict, Any
from src.agents.base_agent import BaseAgent
from src.models.schemas import (
    ResearchDossier,
    ClaimVerificationResult,
    VerdictType,
    PipelineExecutionMetric
)


class SynthesizerAgent(BaseAgent):
    """
    Agent 4: Chief Synthesizer Agent.
    Aggregates atomic claim verifications, weights source credibility,
    and produces an authoritative, auditable Research Dossier.
    """

    def __init__(self):
        super().__init__(
            name="ChiefSynthesizerAgent",
            role_description="Synthesizes multi-agent verdicts into a cohesive, peer-reviewable intelligence dossier."
        )

    def execute(self, payload: Dict[str, Any], context: Dict[str, Any]) -> ResearchDossier:
        query_text: str = payload["query"]
        detailed_claims: List[ClaimVerificationResult] = payload["claim_results"]
        audit_trail: List[PipelineExecutionMetric] = payload.get("audit_trail", [])

        if not detailed_claims:
            return ResearchDossier(
                query_id=f"DOS-{uuid.uuid4().hex[:8].upper()}",
                raw_query=query_text,
                claims_analyzed=0,
                overall_verdict=VerdictType.UNVERIFIED,
                overall_confidence=0.0,
                executive_summary="No verifiable atomic claims were identified in the submitted statement.",
                detailed_claims=[],
                audit_trail=audit_trail,
                meta={"synthesizer_version": "1.0.0"}
            )

        false_count = sum(1 for c in detailed_claims if c.verdict == VerdictType.VERIFIED_FALSE)
        misleading_count = sum(1 for c in detailed_claims if c.verdict == VerdictType.MISLEADING)
        true_count = sum(1 for c in detailed_claims if c.verdict == VerdictType.VERIFIED_TRUE)

        avg_confidence = sum(c.confidence_score for c in detailed_claims) / len(detailed_claims)

        if false_count > 0:
            overall_verdict = VerdictType.VERIFIED_FALSE
            summary = (
                f"Analysis detected factual falsehoods across {false_count} claim(s). "
                "Adversarial verification and primary academic registries contradict the submitted premise."
            )
        elif misleading_count > 0:
            overall_verdict = VerdictType.MISLEADING
            summary = (
                f"Analysis determined the statement contains {misleading_count} misleading or uncontextualized assertion(s). "
                "While partial truths exist, key logical leaps or cherry-picked evidence distort the factual reality."
            )
        elif true_count == len(detailed_claims):
            overall_verdict = VerdictType.VERIFIED_TRUE
            summary = (
                f"All {len(detailed_claims)} atomic claims have been successfully verified against authoritative primary registries. "
                "Corroborating citations affirm factual accuracy with zero adversarial counter-indications."
            )
        else:
            overall_verdict = VerdictType.UNVERIFIED
            summary = "Insufficient primary documentation to conclusively establish truth value."

        return ResearchDossier(
            query_id=f"DOS-{uuid.uuid4().hex[:8].upper()}",
            raw_query=query_text,
            claims_analyzed=len(detailed_claims),
            overall_verdict=overall_verdict,
            overall_confidence=round(avg_confidence, 2),
            executive_summary=summary,
            detailed_claims=detailed_claims,
            audit_trail=audit_trail,
            meta={
                "synthesizer_version": "1.0.0",
                "total_sources_consulted": sum(len(c.corroborating_evidence) + len(c.contradicting_evidence) for c in detailed_claims)
            }
        )
