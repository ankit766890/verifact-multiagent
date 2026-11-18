# VeriFact Multi-Agent: Autonomous Research & Fact-Checking System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Clean](https://img.shields.io/badge/code%20style-clean-brightgreen.svg)]()

> **Submission for Hacktoskill**  
> **Vertical:** `PS03: Multi-Agent Research & Fact-Checking`

---

## 1. Chosen Vertical & Problem Alignment
In information ecosystems saturated with unverified assertions and synthetic media, single-model prompt engineering often produces hallucinated citations or biased confirmations. 

**VeriFact** addresses **PS03 (Multi-Agent Research & Fact-Checking)** by deploying an autonomous, 4-agent verification pipeline that deconstructs composite statements into verifiable atomic units, retrieves corroborating and contradicting evidence from primary sources, subjects claims to adversarial cross-examination, and produces a scored intelligence dossier.

---

## 2. Multi-Agent Architecture

```
                      User Claim / Text
                              │
                              ▼
                   ┌─────────────────────┐
                   │  Lead Planner Agent │
                   └──────────┬──────────┘
                              │ (Atomic Claims)
                              ▼
            ┌──────────────────────────────────┐
            │   Evidence Hub Agent             │
            │   (Primary Registries & Scoring) │
            └─────────────────┬────────────────┘
                              │
                              ▼
            ┌──────────────────────────────────┐
            │   Red-Team Verifier Agent        │
            │   (Adversarial & Fallacy Checks) │
            └─────────────────┬────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Chief Synthesizer   │
                   └──────────┬──────────┘
                              │
                              ▼
                   Structured Dossier & UI
```

### Agent Roles:
1. **Lead Planner Agent (`PlannerAgent`)**: Deconstructs compound text into testable atomic claims, categorizes subject domains, and flags temporal/entity anchors.
2. **Evidence Hub Agent (`EvidenceHubAgent`)**: Queries domain registries, computes credibility metrics, and organizes primary citations.
3. **Red-Team Verifier Agent (`RedTeamVerifierAgent`)**: Adversarially stresses claims against disconfirming evidence, logical fallacies, and cognitive biases.
4. **Chief Synthesizer Agent (`SynthesizerAgent`)**: Weights evidence credibility, calculates aggregate confidence scores, and produces executive summaries with an audit trail.

---

## 3. Key Evaluation Criteria Addressed

- **Code Quality**: Strict separation of concerns, modular agent classes inheriting from `BaseAgent`, type hinting via Pydantic schemas, and structured logging.
- **Security**: Built-in input sanitization against prompt injection and XSS via `InputSanitizer`, strict payload length checks, and isolated environment configurations (`.env.example`).
- **Efficiency**: Lightweight runtime (<10 MB repository footprint), sub-millisecond local pipeline latency, and resource-bounded claim execution.
- **Testing**: Built-in automated test suite covering unit operations, security validation, and end-to-end multi-agent orchestration.
- **Accessibility**: Zero-dependency, responsive dashboard with high-contrast semantics, ARIA labels, and live screen-reader regions.

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

### Running the CLI
```bash
python cli.py "NASA Apollo 11 landed humans on the Moon in July 1969."
```

### Running the Web Dashboard
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 5. Running Automated Tests

Run the test suite using Python's built-in test runner:
```bash
python -m unittest discover -s tests -v
```

---

## 6. Assumptions & Scope
- **Domain Trust Calibration**: Primary government (`.gov`), medical (`who.int`, `nih.gov`), and peer-reviewed registries carry higher initial credibility weightings.
- **Autonomous Fallback**: Operates deterministically with offline knowledge baselines when external search APIs are not provisioned.
