# VeriFact Enterprise: Autonomous Multi-Agent Research & Fact Verification Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Clean & Modular](https://img.shields.io/badge/code%20style-clean%20%26%20modular-brightgreen.svg)]()
[![Automated Tests: 12/12 Passing](https://img.shields.io/badge/tests-12%2F12%20passing%20(100%25)-success.svg)]()
[![Compliance: Enterprise Grade](https://img.shields.io/badge/compliance-enterprise%20audit--ready-blue.svg)]()

> **VeriFact Enterprise** is a production-grade multi-agent autonomous cognitive research and fact-verification platform engineered for media forensics, risk compliance, regulatory auditing, and real-time claim scrutiny.

---

## 1. Architectural Overview & Value Proposition

Information ecosystems face unprecedented challenges from hallucinated synthetic media, cherry-picked datasets, and distorted assertions. Single-agent LLM systems exhibit systematic confirmation bias and lack formal epistemic rigor.

**VeriFact Enterprise** deploys an autonomous four-agent cognitive pipeline:
1. **Lead Planner Agent (`PlannerAgent`)**: Deconstructs compound discourse into atomic verifiable propositions, isolating named entities and temporal anchors.
2. **Evidence Hub Agent (`EvidenceHubAgent`)**: Cross-references certified domain authority registries (`.gov`, `.int`, `.org`, and peer-reviewed journals) with cryptographic trust calibration.
3. **Red-Team Verifier Agent (`RedTeamVerifierAgent`)**: Adversarially scrutinizes propositions against **7 classes of informal logical fallacies** (Cherry-Picking, Circular Reasoning, Post Hoc, False Dilemma, etc.) and disinformation tropes.
4. **Chief Synthesizer Agent (`SynthesizerAgent`)**: Weights Bayesian trust across all corroborations and counter-indications, generating an auditable, structured intelligence dossier.

---

## 2. Multi-Agent Pipeline & Execution Modes

```
                         Submitted Discourse / Claims
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │   1. Lead Planner Agent   │ ──► [Mode: PLANNER]
                        └─────────────┬─────────────┘
                                      │ (Atomic Propositions & Entities)
                                      ▼
                        ┌───────────────────────────┐
                        │   2. Evidence Hub Agent   │ ──► [Mode: EVIDENCE]
                        │ (Domain Trust Calibration)│
                        └─────────────┬─────────────┘
                                      │ (Primary Evidence & Registry Records)
                                      ▼
                        ┌───────────────────────────┐
                        │ 3. Red-Team Verifier Agent│ ──► [Mode: REDTEAM]
                        │ (Adversarial Fallacy Scan)│
                        └─────────────┬─────────────┘
                                      │ (Disconfirming Data & Fallacy Severity)
                                      ▼
                        ┌───────────────────────────┐
                        │ 4. Chief Synthesizer Agent│ ──► [Mode: PIPELINE (Full)]
                        │ (Bayesian Trust Synthesis)│
                        └─────────────┬─────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │    Research Dossier       │
                        │ (JSON, UI & Audit Report) │
                        └───────────────────────────┘
```

The system provides flexible execution isolation:
- **`PIPELINE`**: Full 4-agent cooperative swarm.
- **`PLANNER`**: Isolate decomposition and proposition analysis.
- **`EVIDENCE`**: Focus strictly on authority retrieval and trust scoring.
- **`REDTEAM`**: Adversarially stress-test propositions for formal/informal fallacies.

---

## 3. Enterprise Technical Pillars

- **Testing**: 12/12 comprehensive unit and integration tests passing deterministically.
- **Performance & Efficiency**: Integrated in-memory caching engine (`PerformanceMonitor`) enabling sub-millisecond return times on repeated queries (`cache_hit: true`). Repository footprint is ultra-lean (<0.2 MB).
- **Security & Hardening**: Defense-in-depth sanitization via `SecurityGuard` (XSS entity encoding, script injection mitigation, length boundaries).
- **Accessibility & Operations**: Clean institutional design system, keyboard accessible, Web Speech API audio briefing, and 1-click JSON/Print dossier export.

---

## 4. Quickstart Guide

### Prerequisites
- Python 3.10+
- Git

### Installation
```bash
git clone https://github.com/ankit766890/verifact-multiagent.git
cd verifact-multiagent
pip install -r requirements.txt
```

### Running Automated Tests
```bash
python -m unittest discover -s tests -v
```

### Running the CLI
```bash
python cli.py "NASA Apollo 11 landed humans on the Moon in July 1969."
```

### Running the Enterprise Server
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
Access the dashboard at [http://localhost:8000](http://localhost:8000).

---

## 5. API Specification

### `POST /api/v1/verify`
```json
{
  "statement": "NASA Apollo 11 landed humans on the Moon in July 1969.",
  "mode": "PIPELINE"
}
```

**Response Example:**
```json
{
  "query_id": "VF-A872BC10",
  "timestamp": "2026-11-18T05:40:12.000Z",
  "overall_verdict": "VERIFIED_TRUE",
  "overall_confidence": 0.92,
  "claims_analyzed": 1,
  "detailed_claims": [...],
  "audit_trail": [...]
}
```

---

## 6. License
Distributed under the open-source MIT License.
