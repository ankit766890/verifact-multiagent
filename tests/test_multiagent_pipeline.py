import unittest
from src.agents.planner_agent import PlannerAgent
from src.agents.evidence_agent import EvidenceHubAgent
from src.agents.redteam_agent import RedTeamVerifierAgent
from src.agents.synthesizer_agent import SynthesizerAgent
from src.agents.orchestrator import Orchestrator
from src.core.security import InputSanitizer
from src.models.schemas import VerdictType, AtomicClaim, FallacyType


class TestVeriFactMultiAgentPipeline(unittest.TestCase):
    """
    Industry-Grade Automated Test Suite for PS03: Multi-Agent Research & Fact-Checking.
    Covers:
      - Claim Decomposition & Entity Extraction (PlannerAgent)
      - Authority & Credibility Scoring (EvidenceHubAgent)
      - Adversarial Scrutiny & 7 Logical Fallacy Detection (RedTeamVerifierAgent)
      - Epistemic Synthesis & Confidence Weighting (SynthesizerAgent)
      - Security Bounds, XSS Defenses, & Prompt Injection Mitigation (InputSanitizer)
      - End-to-End Autonomous Orchestration
    """

    def setUp(self):
        self.orchestrator = Orchestrator()
        self.planner = PlannerAgent()
        self.evidence_agent = EvidenceHubAgent()
        self.redteam = RedTeamVerifierAgent()
        self.synthesizer = SynthesizerAgent()

    def test_planner_claim_decomposition_and_entities(self):
        query = "NASA Apollo 11 landed on the Moon in 1969, and vaccines prevent infectious viral diseases."
        claims = self.planner.execute(query, {})
        self.assertGreaterEqual(len(claims), 2)
        has_moon = any("moon" in c.normalized_claim.lower() for c in claims)
        has_vaccine = any("vaccine" in c.normalized_claim.lower() for c in claims)
        self.assertTrue(has_moon)
        self.assertTrue(has_vaccine)
        self.assertTrue(claims[0].claim_id.startswith("CLM-"))
        self.assertIn("Apollo", claims[0].entities)

    def test_evidence_hub_official_domain_authority(self):
        claim = AtomicClaim(
            claim_id="CLM-001",
            original_text="Apollo 11 landed on the moon",
            normalized_claim="Apollo 11 landed on the moon",
            topic_category="Science & Technology",
            requires_temporal_context=True,
            entities=["Apollo 11", "Moon"]
        )
        sources = self.evidence_agent.execute(claim, {})
        self.assertGreater(len(sources), 0)
        self.assertTrue(any("nasa.gov" in s.url for s in sources))
        self.assertGreaterEqual(sources[0].credibility_score, 0.95)

    def test_redteam_verifier_detects_cherry_picking_conspiracy(self):
        claim = AtomicClaim(
            claim_id="CLM-002",
            original_text="The moon landing was a fake hoax staged in Hollywood",
            normalized_claim="The moon landing was a fake hoax staged in Hollywood",
            topic_category="Science & Technology",
            requires_temporal_context=False,
            entities=["Moon"]
        )
        result = self.redteam.execute((claim, []), {})
        self.assertEqual(result["verdict"], VerdictType.VERIFIED_FALSE)
        self.assertEqual(result["fallacy_analysis"].fallacy_type, FallacyType.CHERRY_PICKING)
        self.assertTrue(result["fallacy_analysis"].detected)
        self.assertGreater(len(result["contradicting_evidence"]), 0)

    def test_redteam_verifier_detects_flat_earth_circular_reasoning(self):
        claim = AtomicClaim(
            claim_id="CLM-003",
            original_text="The Earth is flat and gravity is fake",
            normalized_claim="The Earth is flat and gravity is fake",
            topic_category="Science & Technology",
            requires_temporal_context=False,
            entities=["Earth"]
        )
        result = self.redteam.execute((claim, []), {})
        self.assertEqual(result["verdict"], VerdictType.VERIFIED_FALSE)
        self.assertEqual(result["fallacy_analysis"].fallacy_type, FallacyType.CIRCULAR_REASONING)

    def test_orchestrator_end_to_end_truth_flow(self):
        statement = "NASA Apollo 11 landed humans on the Moon in July 1969."
        dossier = self.orchestrator.run(statement)
        self.assertEqual(dossier.overall_verdict, VerdictType.VERIFIED_TRUE)
        self.assertGreaterEqual(dossier.overall_confidence, 0.85)
        self.assertGreater(len(dossier.detailed_claims), 0)
        self.assertGreaterEqual(len(dossier.audit_trail), 4)

    def test_orchestrator_end_to_end_falsehood_flow(self):
        statement = "The Earth is flat and the Apollo moon landing was completely fake."
        dossier = self.orchestrator.run(statement)
        self.assertEqual(dossier.overall_verdict, VerdictType.VERIFIED_FALSE)
        self.assertGreater(dossier.overall_confidence, 0.75)

    def test_input_sanitizer_xss_prevention(self):
        malicious_input = "<script>alert('xss')</script> NASA landed on the moon"
        cleaned = InputSanitizer.clean_text(malicious_input)
        self.assertNotIn("<script>", cleaned)
        self.assertIn("&lt;script&gt;", cleaned)

    def test_input_sanitizer_validation_rules(self):
        self.assertTrue(InputSanitizer.validate_claim_text("Valid factual claim for testing"))
        self.assertFalse(InputSanitizer.validate_claim_text("   "))
        self.assertFalse(InputSanitizer.validate_claim_text("javascript:alert(1)"))

    def test_input_truncation_limits(self):
        long_payload = "A" * 5000
        cleaned = InputSanitizer.clean_text(long_payload, max_length=1500)
        self.assertLessEqual(len(cleaned), 1500)


if __name__ == "__main__":
    unittest.main()
