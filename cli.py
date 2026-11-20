import sys
from src.core.security import InputSanitizer
from src.agents.orchestrator import Orchestrator


def print_banner():
    print("=" * 70)
    print("   VeriFact Multi-Agent CLI Fact-Checker (PS03)")
    print("=" * 70)


def main():
    print_banner()
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "NASA Apollo 11 landed humans on the Moon in July 1969."

    if not query:
        print("Error: statement cannot be blank.")
        sys.exit(1)

    orchestrator = Orchestrator()
    print(f"\n[+] Initiating multi-agent pipeline for query: '{query}'")
    print("[*] Running Planner -> Evidence Hub -> Red Team -> Synthesizer...")

    try:
        dossier = orchestrator.run(query)
        print("\n" + "=" * 70)
        print(f"VERDICT: {dossier.overall_verdict.value} (Confidence: {int(dossier.overall_confidence * 100)}%)")
        print("=" * 70)
        print(f"\nExecutive Summary:\n{dossier.executive_summary}\n")
        print(f"Deconstructed Claims Analyzed: {dossier.claims_analyzed}\n")

        for idx, claim in enumerate(dossier.detailed_claims, 1):
            print(f"[{idx}] Claim: {claim.claim_text}")
            print(f"    Verdict: {claim.verdict.value} | Confidence: {int(claim.confidence_score * 100)}%")
            print(f"    Adversarial Critique: {claim.adversarial_critique}")
            if claim.fallacy_analysis and claim.fallacy_analysis.detected:
                print(f"    Fallacy Flagged: {claim.fallacy_analysis.fallacy_type.value}")
            print(f"    Evidence Sources: {len(claim.corroborating_evidence)} corroborating, {len(claim.contradicting_evidence)} contradicting")
            for ev in claim.corroborating_evidence:
                print(f"      - [{ev.source_type.value}] {ev.title} (Trust: {int(ev.credibility_score * 100)}%)")
                print(f"        URL: {ev.url}")
            for ev in claim.contradicting_evidence:
                print(f"      - [CONTRADICTION] {ev.title} (Trust: {int(ev.credibility_score * 100)}%)")
                print(f"        URL: {ev.url}")
            print()

        print("--- Execution Telemetry ---")
        for m in dossier.audit_trail:
            print(f"  * {m.agent_name:<22} | {m.duration_ms:6.2f} ms | Status: {m.status}")

    except Exception as e:
        print(f"\n[!] Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
