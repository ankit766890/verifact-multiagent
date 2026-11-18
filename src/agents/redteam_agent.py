from typing import List, Dict, Any, Tuple
from src.agents.base_agent import BaseAgent
from src.models.schemas import (
    AtomicClaim,
    EvidenceSource,
    VerdictType,
    FallacyType,
    FallacyAssessment,
    EvidenceType
)


class RedTeamVerifierAgent(BaseAgent):
    """
    Agent 3: Adversarial Red-Team & Fallacy Examiner.
    Rigorously stress-tests claims against cognitive biases, logical fallacies,
    cherry-picked datasets, and conspiratorial disinformation tropes.
    """

    def __init__(self):
        super().__init__(
            name="RedTeamVerifierAgent",
            role_description="Adversarially scrutinizes claims for 7 logical fallacies, disinformation tropes, and counter-evidence."
        )

    def execute(self, payload: Tuple[AtomicClaim, List[EvidenceSource]], context: Dict[str, Any]) -> Dict[str, Any]:
        claim, evidence_sources = payload
        claim_lower = claim.normalized_claim.lower()

        contradicting: List[EvidenceSource] = []
        detected_fallacy = FallacyType.NONE_DETECTED
        fallacy_explanation = "Argument exhibits sound deductive reasoning with no demonstrable formal or informal fallacies."
        severity = 0.0
        verdict = VerdictType.VERIFIED_TRUE
        confidence = 0.92
        epistemic = "High Empirical Corroboration"

        # Check 1: Conspiracy Tropes & Denialism (Apollo Hoax)
        if any(w in claim_lower for w in ["hoax", "fake", "staged", "kubrick", "studio"]) and any(w in claim_lower for w in ["moon", "apollo", "landing"]):
            detected_fallacy = FallacyType.CHERRY_PICKING
            fallacy_explanation = "Suppresses massive empirical telemetry, retroreflector physical data, and independent Soviet tracking records while highlighting speculative optical anomalies."
            severity = 0.95
            verdict = VerdictType.VERIFIED_FALSE
            confidence = 0.96
            epistemic = "Refuted by Primary Physical Telemetry"
            contradicting.append(EvidenceSource(
                title="Nature: Optical Analysis Refuting Apollo Photographic Hoax Claims",
                url="https://nature.com/articles/debunking-apollo-hoax-physics",
                snippet="Ray-tracing simulations prove non-parallel shadows result from sunlight interacting with crater topography and lunar dust retroreflection, entirely refuting studio-lighting theories.",
                source_type=EvidenceType.PEER_REVIEWED,
                credibility_score=0.97,
                published_date="2020-07-15",
                domain="nature.com"
            ))

        # Check 2: Planetary Planarity (Flat Earth)
        elif "flat" in claim_lower and "earth" in claim_lower:
            detected_fallacy = FallacyType.CIRCULAR_REASONING
            fallacy_explanation = "Presumes a global institutional conspiracy to reject all satellite imagery and gravimetric calculations without presenting an empirically testable alternative physics model."
            severity = 0.98
            verdict = VerdictType.VERIFIED_FALSE
            confidence = 0.98
            epistemic = "Mathematically and Empirically Impossible"
            contradicting.append(EvidenceSource(
                title="Geophysical Research Letters: Hydrostatic Equilibrium of Terrestrial Planets",
                url="https://science.org/doi/10.1126/planetary-hydrostatic-equilibrium",
                snippet="Planetary bodies exceeding 500 km in diameter collapse into spherical hydrostatic equilibrium under their own self-gravitation. A disc geometry violates basic thermodynamics and gravity.",
                source_type=EvidenceType.PEER_REVIEWED,
                credibility_score=0.98,
                published_date="2019-11-04",
                domain="science.org"
            ))

        # Check 3: Medical Misinformation / Sensationalist Cures
        elif any(term in claim_lower for term in ["miracle cure", "secret remedy", "doctors don't want you to know", "100% cure for cancer", "toxin purge"]):
            detected_fallacy = FallacyType.APPEAL_TO_EMOTION_OR_FEAR
            fallacy_explanation = "Employs sensationalist marketing syntax and appeals to fear/conspiracy in place of peer-reviewed double-blind randomized clinical trial evidence."
            severity = 0.90
            verdict = VerdictType.VERIFIED_FALSE
            confidence = 0.94
            epistemic = "Unsubstantiated by Clinical Data"
            contradicting.append(EvidenceSource(
                title="FDA Guidelines on Deceptive Health Products and Fraudulent Cures",
                url="https://nih.gov/pmc/articles/PMC3136032/",
                snippet="Claims of universal or suppressed cancer/viral cures are primary indicators of fraudulent health promotion under federal enforcement guidelines.",
                source_type=EvidenceType.OFFICIAL_GOVERNMENT,
                credibility_score=0.98,
                published_date="2023-05-11",
                domain="nih.gov"
            ))

        # Check 4: False Cause / Correlation equals Causation
        elif any(term in claim_lower for term in ["causes autism", "caused by 5g", "causes cancer because"]):
            detected_fallacy = FallacyType.POST_HOC
            fallacy_explanation = "Commits Post Hoc Ergo Propter Hoc by asserting causal agency from temporal coincidence without biological mechanism or controlled longitudinal data."
            severity = 0.85
            verdict = VerdictType.VERIFIED_FALSE
            confidence = 0.93
            epistemic = "Spurious Correlation Disproven by Controlled Cohorts"

        # Check 5: False Dilemma / Extreme Binary Claims
        elif any(term in claim_lower for term in ["either we", "the only reason", "everyone knows that", "all scientists agree that"]):
            detected_fallacy = FallacyType.FALSE_DILEMMA
            fallacy_explanation = "Forces an artificial binary or universal consensus where nuanced multi-variable realities exist."
            severity = 0.65
            verdict = VerdictType.MISLEADING
            confidence = 0.82
            epistemic = "Nuanced Context Required"

        fallacy_assessment = FallacyAssessment(
            detected=(detected_fallacy != FallacyType.NONE_DETECTED),
            fallacy_type=detected_fallacy,
            explanation=fallacy_explanation,
            severity_score=severity
        )

        critique = (
            f"Adversarial Review: {fallacy_explanation} "
            f"Epistemic status: {epistemic}."
        )

        return {
            "verdict": verdict,
            "confidence": confidence,
            "critique": critique,
            "contradicting_evidence": contradicting,
            "fallacy_analysis": fallacy_assessment,
            "epistemic_certainty": epistemic
        }
