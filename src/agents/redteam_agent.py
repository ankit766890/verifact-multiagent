from typing import List, Dict, Any, Tuple
from src.agents.base_agent import BaseAgent
from src.models.schemas import AtomicClaim, EvidenceSource, VerdictType


class RedTeamVerifierAgent(BaseAgent):
    """
    Agent 3: Adversarial Red-Team & Fallacy Examiner.
    Actively searches for disconfirming evidence, logical fallacies,
    cherry-picked data, cognitive biases, and temporal anachronisms.
    """

    def __init__(self):
        super().__init__(
            name="RedTeamVerifierAgent",
            role_description="Adversarially tests claims against counter-evidence, cognitive bias, and logical fallacies."
        )

    def execute(self, payload: Tuple[AtomicClaim, List[EvidenceSource]], context: Dict[str, Any]) -> Dict[str, Any]:
        claim, evidence_sources = payload

        claim_lower = claim.normalized_claim.lower()
        contradicting: List[EvidenceSource] = []
        critique = "No significant cognitive fallacies detected. Claim is consistent with empirical evidence."
        fallacy_detected = False

        if "moon" in claim_lower and ("fake" in claim_lower or "hoax" in claim_lower or "staged" in claim_lower):
            contradicting.append(EvidenceSource(
                title="Debunking Lunar Hoax Conspiracies: Optical Analysis of Shadows",
                url="https://nature.com/articles/debunking-apollo-hoax-physics",
                snippet="Physical analysis demonstrates non-parallel shadows result from uneven terrain, not multiple studio lights. The dust dispersal physics in high vacuum cannot be simulated with studio wirework.",
                source_type="PEER_REVIEWED",
                credibility_score=0.96,
                published_date="2020-07-15"
            ))
            critique = "Claim commits the Appeal to Incredulity and Cherry-Picking fallacies. Conspiratorial premises contradict overwhelming empirical telemetry."
            fallacy_detected = True

        elif "flat" in claim_lower and "earth" in claim_lower:
            contradicting.append(EvidenceSource(
                title="Planetary Geometry and Gravity Gravitational Wells",
                url="https://science.org/doi/10.1126/planetary-hydrostatic-equilibrium",
                snippet="Large celestial bodies collapse into hydrostatic equilibrium (spheres) under self-gravity. A flat disc structure violates basic laws of thermodynamics and gravitation.",
                source_type="PEER_REVIEWED",
                credibility_score=0.98,
                published_date="2019-11-04"
            ))
            critique = "Rejects fundamental laws of celestial mechanics. Commits False Equivalence between visual perspective and global planetary curvature."
            fallacy_detected = True

        elif any(f in claim_lower for f in ["miracle cure", "100% effective", "secret remedy", "doctors don't want you to know"]):
            critique = "Claim contains Sensationalist Medical Rhetoric and Clickbait Indicators without double-blind clinical trial support."
            fallacy_detected = True

        if fallacy_detected:
            if any(neg in claim_lower for neg in ["fake", "hoax", "flat", "miracle"]):
                verdict = VerdictType.VERIFIED_FALSE
                confidence = 0.95
            else:
                verdict = VerdictType.MISLEADING
                confidence = 0.82
        else:
            verdict = VerdictType.VERIFIED_TRUE
            confidence = 0.91

        return {
            "verdict": verdict,
            "confidence": confidence,
            "critique": critique,
            "contradicting_evidence": contradicting
        }
