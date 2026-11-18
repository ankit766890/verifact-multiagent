import uuid
from datetime import datetime, timezone
from typing import List
from src.agents.planner_agent import PlannerAgent
from src.agents.evidence_agent import EvidenceHubAgent
from src.agents.redteam_agent import RedTeamVerifierAgent
from src.agents.synthesizer_agent import SynthesizerAgent
from src.models.schemas import (
    ResearchDossier,
    ClaimVerificationResult,
    PipelineExecutionMetric,
    ExecutionMode,
    VerdictType,
    FallacyAssessment,
    FallacyType
)
from src.core.security import InputSanitizer
from src.core.performance import PerformanceMonitor


class Orchestrator:
    """
    Central Coordinator managing multi-agent pipelining, verification fan-out,
    agent execution mode switching, LRU caching, and end-to-end telemetry tracking.
    """

    def __init__(self):
        self.planner = PlannerAgent()
        self.evidence_hub = EvidenceHubAgent()
        self.red_team = RedTeamVerifierAgent()
        self.synthesizer = SynthesizerAgent()

    def run(self, query: str, mode: ExecutionMode = ExecutionMode.PIPELINE) -> ResearchDossier:
        cleaned_query = InputSanitizer.clean_text(query)
        now_iso = datetime.now(timezone.utc).isoformat()

        if not InputSanitizer.validate_claim_text(cleaned_query):
            raise ValueError("Input statement failed security validation, contains forbidden syntax, or is empty.")

        # Performance Optimization: High-Efficiency Caching Layer
        cache_key = f"{mode.value}::{cleaned_query.lower()}"
        cached_dossier = PerformanceMonitor.get_cached(cache_key)
        if cached_dossier is not None:
            # Return cached dossier with fresh timestamp and cache hit indicator
            dossier_copy = cached_dossier.model_copy(deep=True)
            dossier_copy.timestamp = now_iso
            dossier_copy.meta["cache_hit"] = True
            return dossier_copy

        audit_trail: List[PipelineExecutionMetric] = []

        # Stage 1: Lead Planner Agent (Deconstructs propositions)
        claims, metric_planner = self.planner.run_with_telemetry(cleaned_query, {})
        audit_trail.append(metric_planner)

        # MODE: PLANNER ONLY
        if mode == ExecutionMode.PLANNER_ONLY:
            detailed = [
                ClaimVerificationResult(
                    claim_id=c.claim_id,
                    claim_text=c.normalized_claim,
                    verdict=VerdictType.CONTEXT_REQUIRED,
                    confidence_score=0.95,
                    topic_category=c.topic_category,
                    corroborating_evidence=[],
                    contradicting_evidence=[],
                    fallacy_analysis=FallacyAssessment(
                        detected=False,
                        fallacy_type=FallacyType.NONE_DETECTED,
                        explanation=f"Planner isolated entities: {c.entities}. Temporal anchor: {c.temporal_anchor or 'None'}"
                    ),
                    adversarial_critique="Planner Mode Active: Synthesizer bypassed.",
                    epistemic_certainty="Deconstructed Propositions Ready for Downstream Agents"
                )
                for c in claims
            ]
            dossier = ResearchDossier(
                query_id=f"DOS-PLAN-{uuid.uuid4().hex[:6].upper()}",
                timestamp=now_iso,
                raw_query=cleaned_query,
                execution_mode=ExecutionMode.PLANNER_ONLY,
                claims_analyzed=len(claims),
                overall_verdict=VerdictType.CONTEXT_REQUIRED,
                overall_confidence=0.95,
                verdict_badge_color="#38bdf8",
                executive_summary=f"Lead Planner isolated {len(claims)} atomic proposition(s) across categories: {', '.join(set(c.topic_category for c in claims))}.",
                detailed_claims=detailed,
                audit_trail=audit_trail,
                meta={"mode": "PLANNER_ONLY", "isolated_entities": [e for c in claims for e in c.entities], "cache_hit": False}
            )
            PerformanceMonitor.set_cache(cache_key, dossier)
            return dossier

        # Stage 2: Evidence Gathering
        detailed_claims: List[ClaimVerificationResult] = []
        for claim in claims:
            evidence, metric_ev = self.evidence_hub.run_with_telemetry(claim, {})
            audit_trail.append(metric_ev)

            # MODE: EVIDENCE HUB ONLY
            if mode == ExecutionMode.EVIDENCE_ONLY:
                detailed_claims.append(ClaimVerificationResult(
                    claim_id=claim.claim_id,
                    claim_text=claim.normalized_claim,
                    verdict=VerdictType.VERIFIED_TRUE if evidence else VerdictType.UNVERIFIED,
                    confidence_score=0.90,
                    topic_category=claim.topic_category,
                    corroborating_evidence=evidence,
                    contradicting_evidence=[],
                    fallacy_analysis=FallacyAssessment(detected=False, explanation="Adversarial check bypassed in Evidence Mode."),
                    adversarial_critique="Evidence Mode Active: Discovered primary sources without adversarial audit.",
                    epistemic_certainty=f"Corroborated by {len(evidence)} certified registry sources."
                ))
            else:
                # Stage 3: Red Team Adversarial Verification
                red_team_out, metric_rt = self.red_team.run_with_telemetry((claim, evidence), {})
                audit_trail.append(metric_rt)

                res = ClaimVerificationResult(
                    claim_id=claim.claim_id,
                    claim_text=claim.normalized_claim,
                    verdict=red_team_out["verdict"],
                    confidence_score=red_team_out["confidence"],
                    topic_category=claim.topic_category,
                    corroborating_evidence=[] if mode == ExecutionMode.REDTEAM_ONLY else evidence,
                    contradicting_evidence=red_team_out["contradicting_evidence"],
                    fallacy_analysis=red_team_out["fallacy_analysis"],
                    adversarial_critique=red_team_out["critique"],
                    epistemic_certainty=red_team_out["epistemic_certainty"]
                )
                detailed_claims.append(res)

        # MODE: EVIDENCE ONLY RETURN
        if mode == ExecutionMode.EVIDENCE_ONLY:
            total_sources = sum(len(c.corroborating_evidence) for c in detailed_claims)
            dossier = ResearchDossier(
                query_id=f"DOS-EVID-{uuid.uuid4().hex[:6].upper()}",
                timestamp=now_iso,
                raw_query=cleaned_query,
                execution_mode=ExecutionMode.EVIDENCE_ONLY,
                claims_analyzed=len(claims),
                overall_verdict=VerdictType.VERIFIED_TRUE,
                overall_confidence=0.91,
                verdict_badge_color="#10b981",
                executive_summary=f"Evidence Hub retrieved {total_sources} primary source citations with authority trust scoring.",
                detailed_claims=detailed_claims,
                audit_trail=audit_trail,
                meta={"mode": "EVIDENCE_ONLY", "sources_retrieved": total_sources, "cache_hit": False}
            )
            PerformanceMonitor.set_cache(cache_key, dossier)
            return dossier

        # MODE: RED TEAM ONLY RETURN
        if mode == ExecutionMode.REDTEAM_ONLY:
            fallacies_found = sum(1 for c in detailed_claims if c.fallacy_analysis.detected)
            dossier = ResearchDossier(
                query_id=f"DOS-REDT-{uuid.uuid4().hex[:6].upper()}",
                timestamp=now_iso,
                raw_query=cleaned_query,
                execution_mode=ExecutionMode.REDTEAM_ONLY,
                claims_analyzed=len(claims),
                overall_verdict=VerdictType.VERIFIED_FALSE if fallacies_found > 0 else VerdictType.VERIFIED_TRUE,
                overall_confidence=0.94,
                verdict_badge_color="#ef4444" if fallacies_found > 0 else "#10b981",
                executive_summary=f"Red-Team Examiner completed adversarial stress-testing. Identified {fallacies_found} informal cognitive/logical fallacy indicator(s).",
                detailed_claims=detailed_claims,
                audit_trail=audit_trail,
                meta={"mode": "REDTEAM_ONLY", "fallacies_count": fallacies_found, "cache_hit": False}
            )
            PerformanceMonitor.set_cache(cache_key, dossier)
            return dossier

        # MODE: FULL COOPERATIVE PIPELINE (Default)
        dossier, metric_synth = self.synthesizer.run_with_telemetry({
            "query": cleaned_query,
            "claim_results": detailed_claims,
            "audit_trail": audit_trail
        }, {})
        audit_trail.append(metric_synth)
        dossier.execution_mode = ExecutionMode.PIPELINE
        dossier.audit_trail = audit_trail
        dossier.meta["cache_hit"] = False

        PerformanceMonitor.set_cache(cache_key, dossier)
        return dossier
