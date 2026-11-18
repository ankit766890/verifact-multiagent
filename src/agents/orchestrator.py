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
    FallacyType,
    AgentStreamStep
)
from src.core.security import SecurityGuard
from src.core.performance import PerformanceMonitor


class Orchestrator:
    """
    Central Coordinator managing multi-agent pipelining, verification fan-out,
    agent timeline logging, LRU caching, and end-to-end telemetry tracking.
    """

    def __init__(self):
        self.planner = PlannerAgent()
        self.evidence_hub = EvidenceHubAgent()
        self.red_team = RedTeamVerifierAgent()
        self.synthesizer = SynthesizerAgent()

    def run(self, query: str, mode: ExecutionMode = ExecutionMode.PIPELINE) -> ResearchDossier:
        audit_sec = SecurityGuard.audit_security(query)
        if not audit_sec["safe"]:
            raise ValueError(audit_sec["reason"])

        cleaned_query = SecurityGuard.sanitize(query)
        now_iso = datetime.now(timezone.utc).isoformat()

        # Performance Optimization: High-Efficiency Caching Layer
        cache_key = f"{mode.value}::{cleaned_query.lower()}"
        cached_dossier = PerformanceMonitor.get_cached(cache_key)
        if cached_dossier is not None:
            dossier_copy = cached_dossier.model_copy(deep=True)
            dossier_copy.timestamp = now_iso
            dossier_copy.meta["cache_hit"] = True
            return dossier_copy

        audit_trail: List[PipelineExecutionMetric] = []
        timeline: List[AgentStreamStep] = []

        # Stage 1: Lead Planner Agent
        timeline.append(AgentStreamStep(
            agent_id="agent_1",
            agent_name="Lead Planner",
            timestamp=datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3],
            action="Deconstruct Discourse",
            thought_summary="Tokenizing sentence clauses, isolating named entities, identifying temporal anchors.",
            detail=f"Analyzing input: '{cleaned_query[:60]}...'"
        ))
        claims, metric_planner = self.planner.run_with_telemetry(cleaned_query, {})
        audit_trail.append(metric_planner)

        # MODE: PLANNER ONLY
        if mode == ExecutionMode.PLANNER:
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
                    adversarial_critique="Planner Mode Active: Downstream verification bypassed.",
                    epistemic_certainty="Deconstructed Propositions Ready for Downstream Agents"
                )
                for c in claims
            ]
            dossier = ResearchDossier(
                query_id=f"DOS-PLAN-{uuid.uuid4().hex[:6].upper()}",
                timestamp=now_iso,
                raw_query=cleaned_query,
                execution_mode=ExecutionMode.PLANNER,
                claims_analyzed=len(claims),
                overall_verdict=VerdictType.CONTEXT_REQUIRED,
                overall_confidence=0.95,
                verdict_badge_color="#06b6d4",
                executive_summary=f"Lead Planner extracted {len(claims)} atomic proposition(s) across categories: {', '.join(set(c.topic_category for c in claims))}.",
                detailed_claims=detailed,
                audit_trail=audit_trail,
                agent_timeline=timeline,
                meta={"mode": "PLANNER", "isolated_entities": [e for c in claims for e in c.entities], "cache_hit": False}
            )
            PerformanceMonitor.set_cache(cache_key, dossier)
            return dossier

        # Stage 2: Evidence Gathering
        timeline.append(AgentStreamStep(
            agent_id="agent_2",
            agent_name="Evidence Hub",
            timestamp=datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3],
            action="Query Authority Registries",
            thought_summary="Searching certified repositories (.gov, .int, peer-reviewed indices) with trust scoring.",
            detail=f"Querying sources across {len(claims)} extracted propositions."
        ))

        detailed_claims: List[ClaimVerificationResult] = []
        for claim in claims:
            evidence, metric_ev = self.evidence_hub.run_with_telemetry(claim, {})
            audit_trail.append(metric_ev)

            if mode == ExecutionMode.EVIDENCE:
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
                    corroborating_evidence=[] if mode == ExecutionMode.REDTEAM else evidence,
                    contradicting_evidence=red_team_out["contradicting_evidence"],
                    fallacy_analysis=red_team_out["fallacy_analysis"],
                    adversarial_critique=red_team_out["critique"],
                    epistemic_certainty=red_team_out["epistemic_certainty"]
                )
                detailed_claims.append(res)

        if mode == ExecutionMode.EVIDENCE:
            total_sources = sum(len(c.corroborating_evidence) for c in detailed_claims)
            dossier = ResearchDossier(
                query_id=f"DOS-EVID-{uuid.uuid4().hex[:6].upper()}",
                timestamp=now_iso,
                raw_query=cleaned_query,
                execution_mode=ExecutionMode.EVIDENCE,
                claims_analyzed=len(claims),
                overall_verdict=VerdictType.VERIFIED_TRUE,
                overall_confidence=0.91,
                verdict_badge_color="#10b981",
                executive_summary=f"Evidence Hub retrieved {total_sources} primary source citations with authority trust scoring.",
                detailed_claims=detailed_claims,
                audit_trail=audit_trail,
                agent_timeline=timeline,
                meta={"mode": "EVIDENCE", "sources_retrieved": total_sources, "cache_hit": False}
            )
            PerformanceMonitor.set_cache(cache_key, dossier)
            return dossier

        if mode == ExecutionMode.REDTEAM:
            timeline.append(AgentStreamStep(
                agent_id="agent_3",
                agent_name="Red-Team Verifier",
                timestamp=datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3],
                action="Adversarial Audit",
                thought_summary="Scrutinizing assertions for 7 informal cognitive fallacies and disinformation tropes.",
                detail=f"Completed fallacy scan across {len(claims)} claim(s)."
            ))
            fallacies_found = sum(1 for c in detailed_claims if c.fallacy_analysis.detected)
            dossier = ResearchDossier(
                query_id=f"DOS-REDT-{uuid.uuid4().hex[:6].upper()}",
                timestamp=now_iso,
                raw_query=cleaned_query,
                execution_mode=ExecutionMode.REDTEAM,
                claims_analyzed=len(claims),
                overall_verdict=VerdictType.VERIFIED_FALSE if fallacies_found > 0 else VerdictType.VERIFIED_TRUE,
                overall_confidence=0.94,
                verdict_badge_color="#ef4444" if fallacies_found > 0 else "#10b981",
                executive_summary=f"Red-Team Examiner completed adversarial stress-testing. Identified {fallacies_found} informal cognitive/logical fallacy indicator(s).",
                detailed_claims=detailed_claims,
                audit_trail=audit_trail,
                agent_timeline=timeline,
                meta={"mode": "REDTEAM", "fallacies_count": fallacies_found, "cache_hit": False}
            )
            PerformanceMonitor.set_cache(cache_key, dossier)
            return dossier

        # MODE: FULL PIPELINE
        timeline.append(AgentStreamStep(
            agent_id="agent_3",
            agent_name="Red-Team Verifier",
            timestamp=datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3],
            action="Adversarial Scrutiny",
            thought_summary="Screening claims against cognitive biases, cherry-picking, and false causality.",
            detail="Completed fallacy analysis with counter-evidence checks."
        ))

        timeline.append(AgentStreamStep(
            agent_id="agent_4",
            agent_name="Chief Synthesizer",
            timestamp=datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3],
            action="Bayesian Synthesis",
            thought_summary="Calibrating source weights, aggregating truth values, and compiling formal dossier.",
            detail="Generated intelligence verdict and confidence calibration."
        ))

        dossier, metric_synth = self.synthesizer.run_with_telemetry({
            "query": cleaned_query,
            "claim_results": detailed_claims,
            "audit_trail": audit_trail
        }, {})
        audit_trail.append(metric_synth)
        dossier.execution_mode = ExecutionMode.PIPELINE
        dossier.audit_trail = audit_trail
        dossier.agent_timeline = timeline
        dossier.meta["cache_hit"] = False

        PerformanceMonitor.set_cache(cache_key, dossier)
        return dossier
