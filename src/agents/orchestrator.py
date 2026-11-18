from typing import List
from src.agents.planner_agent import PlannerAgent
from src.agents.evidence_agent import EvidenceHubAgent
from src.agents.redteam_agent import RedTeamVerifierAgent
from src.agents.synthesizer_agent import SynthesizerAgent
from src.models.schemas import (
    ResearchDossier,
    ClaimVerificationResult,
    PipelineExecutionMetric
)
from src.core.security import InputSanitizer


class Orchestrator:
    """
    Central Coordinator managing multi-agent pipelining, verification fan-out,
    adversarial checks, and end-to-end telemetry tracking.
    """

    def __init__(self):
        self.planner = PlannerAgent()
        self.evidence_hub = EvidenceHubAgent()
        self.red_team = RedTeamVerifierAgent()
        self.synthesizer = SynthesizerAgent()

    def run(self, query: str) -> ResearchDossier:
        audit_trail: List[PipelineExecutionMetric] = []
        cleaned_query = InputSanitizer.clean_text(query)

        if not InputSanitizer.validate_claim_text(cleaned_query):
            raise ValueError("Input statement failed security validation, contains forbidden syntax, or is empty.")

        # Stage 1: Deconstruct into Atomic Claims via Planner Agent
        claims, metric_planner = self.planner.run_with_telemetry(cleaned_query, {})
        audit_trail.append(metric_planner)

        # Stage 2 & 3: Evidence Discovery & Adversarial Cross-Examination
        detailed_claims: List[ClaimVerificationResult] = []
        for claim in claims:
            evidence, metric_ev = self.evidence_hub.run_with_telemetry(claim, {})
            red_team_out, metric_rt = self.red_team.run_with_telemetry((claim, evidence), {})

            res = ClaimVerificationResult(
                claim_id=claim.claim_id,
                claim_text=claim.normalized_claim,
                verdict=red_team_out["verdict"],
                confidence_score=red_team_out["confidence"],
                topic_category=claim.topic_category,
                corroborating_evidence=evidence,
                contradicting_evidence=red_team_out["contradicting_evidence"],
                fallacy_analysis=red_team_out["fallacy_analysis"],
                adversarial_critique=red_team_out["critique"],
                epistemic_certainty=red_team_out["epistemic_certainty"]
            )
            detailed_claims.append(res)
            audit_trail.extend([metric_ev, metric_rt])

        # Stage 4: Synthesize Complete Dossier
        dossier, metric_synth = self.synthesizer.run_with_telemetry({
            "query": cleaned_query,
            "claim_results": detailed_claims,
            "audit_trail": audit_trail
        }, {})
        audit_trail.append(metric_synth)
        dossier.audit_trail = audit_trail

        return dossier
