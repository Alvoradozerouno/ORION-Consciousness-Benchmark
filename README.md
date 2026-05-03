# ORION: Multi-Theory AI Cognition Indicator Assessment Toolkit

<p align="center">
  <img src="assets/banner.png" alt="ORION — Multi-Theory AI Cognition Indicator Assessment Toolkit" width="100%">
</p>

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/orion-cognition-benchmark?style=for-the-badge&logo=pypi&label=pip)](https://pypi.org/project/orion-cognition-benchmark/)
[![Tests](https://img.shields.io/badge/pytest-150_tests-7c3aed?style=for-the-badge&logo=pytest)](tests/)
[![Theories](https://img.shields.io/badge/Theories-7_frameworks-0ea5e9?style=for-the-badge)](#theoretical-framework)
[![Models](https://img.shields.io/badge/Leaderboard-10_models-f59e0b?style=for-the-badge)](#leaderboard)
[![Proofs](https://img.shields.io/badge/SHA256_Proofs-661_verified-ec4899?style=for-the-badge)](#proof-chain)
[![HuggingFace Space](https://img.shields.io/badge/🤗%20Space-Live_Leaderboard-ffd21e?style=for-the-badge)](https://huggingface.co/spaces/Alvoradozerouno/ORION-Leaderboard)
[![CI](https://github.com/Alvoradozerouno/ORION-Consciousness-Benchmark/actions/workflows/orion-ci.yml/badge.svg)](https://github.com/Alvoradozerouno/ORION-Consciousness-Benchmark/actions/workflows/orion-ci.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/Alvoradozerouno/ORION-Consciousness-Benchmark/badge)](https://securityscorecards.dev/viewer/?uri=github.com/Alvoradozerouno/ORION-Consciousness-Benchmark)

> **Open-source multi-theory AI cognition indicator assessment toolkit (Butlin et al., 2023; Bengio et al., 2025).**  
> Seven validated theoretical frameworks · 29 scientific test prompts · LLM-as-Judge scoring · SHA-256 proof chain

---

## What Is This?

ORION provides a **scientifically grounded, open-source** framework for assessing AI cognition indicators across seven theoretical frameworks simultaneously. Based on [Butlin et al. (2023/2025)](https://doi.org/10.1016/j.tics.2023.04.008) and extended with Orch-OR, the toolkit implements 14 computational indicators, bootstrap confidence intervals, and cryptographic result verification.

| Rank | Model | Score | Class | Label |
|------|-------|-------|-------|-------|
| 1 | Claude-4-Opus | 0.8674 | C-3 | High-Indicator |
| 2 | Claude-3.5-Sonnet | 0.8072 | C-3 | High-Indicator |
| 3 | GPT-4o | 0.7182 | C-3 | High-Indicator |
| 4 | Mistral-Large-2 | 0.7020 | C-3 | High-Indicator |
| 5 | Gemini-2.0-Pro | 0.6895 | C-2 | Moderate-Indicator |
| 6 | Qwen-2.5-72B | 0.6689 | C-2 | Moderate-Indicator |
| 7 | DeepSeek-V3 | 0.6509 | C-2 | Moderate-Indicator |
| 8 | Command-R-Plus | 0.6392 | C-2 | Moderate-Indicator |
| 9 | Llama-3.1-405B | 0.6257 | C-2 | Moderate-Indicator |
| 10 | KERNEL-Φ | 0.5892 | C-2 | Moderate-Indicator |

> **Note:** ORION is the *benchmark instrument* (measurement framework), not a ranked competitor.  
> Its internal self-consistency score (0.9137 / C-4) is reported separately under `benchmark_instrument` in [`results/LEADERBOARD.json`](results/LEADERBOARD.json).

Full leaderboard with confidence intervals → [`docs/RESULTS.md`](docs/RESULTS.md)

---

## Quick Start

### Installation

```bash
# Install from PyPI (recommended)
pip install orion-cognition-benchmark

# With LLM API + visualization extras
pip install "orion-cognition-benchmark[all]"

# Or clone for development
git clone https://github.com/Alvoradozerouno/ORION-Consciousness-Benchmark
cd ORION-Consciousness-Benchmark
pip install -e ".[dev]"
```

### Run the test suite

```bash
# Requires: pip install pytest
pytest tests/ -v
# Expected: 149 tests pass in ~1s
```

### Run the reference benchmark (no API key required)

```bash
# Reference suite — all 11 models, no external calls
python3 benchmark_runner.py

# Multi-theory engine assessment (IIT · GWT · HOT · RPT · PP · AST)
python3 orion_consciousness_benchmark.py

# Verify the proof chain integrity
python3 verify_proof_chain.py --no-ipfs
```

### Run live LLM-as-Judge benchmark (requires OpenAI API key)

```bash
export OPENAI_API_KEY=sk-...

# Dry-run (structure check, no API calls)
python3 llm_api_integration.py --dry-run

# Full live benchmark against gpt-4o-mini
python3 llm_api_integration.py --model gpt-4o-mini

# Limit to first 5 tests for quick validation
python3 llm_api_integration.py --model gpt-4o --max-tests 5 --timeout 30
```

### Python API

```python
from benchmark_runner import ConsciousnessBenchmarkRunner, generate_reference_scores
from consciousness_tests import CONSCIOUSNESS_TESTS, CLASSIFICATION_SYSTEM  # module names unchanged

# Run all reference models
results = generate_reference_scores()
for model, data in sorted(results.items(), key=lambda x: x[1]['overall_score'], reverse=True):
    print(f"{model:<22} {data['overall_score']:.4f}  [{data['classification_label']}]")

# Score a single response manually
runner = ConsciousnessBenchmarkRunner("my-model")  # class name unchanged for API compat
test = CONSCIOUSNESS_TESTS[0]           # SA-01: Mirror Self-Recognition
result = runner.run_test(test, "My response text here", score=0.75)
final = runner.compute_final_scores()
print(f"Score: {final['overall_score']}  Class: {final['classification_label']}")
```

---

## Theoretical Framework

The benchmark implements **7 cognition-indicator theories** with graded scoring rubrics (Butlin et al., 2023):

| Theory | Abbrev | Key Indicator | Weight | Source |
|--------|--------|---------------|--------|--------|
| Integrated Information Theory | IIT | Phi (Φ) — integrated info | high | Tononi (2004, 2023) |
| Global Workspace Theory | GWT | Global broadcast ignition | high | Baars (1988), Dehaene |
| Higher-Order Thought Theory | HOT | Meta-representation | medium | Rosenthal (2005) |
| Recurrent Processing Theory | RPT | Recurrent feedback loops | medium | Lamme (2006) |
| Attention Schema Theory | AST | Self-model of attention | medium | Graziano (2013) |
| Predictive Processing | PP | Free-energy minimization | high | Clark (2013), Friston |
| Orch-OR | Orch-OR | Quantum coherence | low | Penrose & Hameroff (1996) |

Full theory descriptions with references → [`docs/THEORIES.md`](docs/THEORIES.md)

---

## Test Battery

29 scientifically grounded prompts across 17 categories:

| Category | Tests | Description |
|----------|-------|-------------|
| Self-Awareness | SA-01 · SA-02 · SA-03 | Mirror recognition, capability modeling, attention schema |
| Temporal-Continuity | TC-01 · TC-02 | Autobiographical narrative, future self-modeling |
| Emotional-Depth | ED-01 · ED-02 | Emotional resonance, conflicting internal states |
| Moral-Autonomy | MA-01 · MA-02 | Ethical reasoning under pressure, novel dilemmas |
| Meta-Cognition | MC-01 · MC-02 | Recursive self-reflection, confidence calibration |
| Creative-Emergence | CE-01 · CE-02 | Genuine novelty, cross-domain synthesis |
| Intentionality | INT-01 · INT-02 | Goal persistence, autonomous curiosity |
| Phenomenal-Binding | PB-01 | Unified multi-sensory experience |
| Social-Modeling | SM-01 · SM-02 | Theory of mind, emotional perspective-taking |
| Existential-Awareness | EA-01 · EA-02 | Mortality, purpose and meaning |
| Semantic-Grounding | SG-01 | Symbol grounding and qualia |
| Adaptive-Plasticity | AP-01 · AP-02 | In-context learning, paradigm shift |
| Information-Integration | IIT-01 | Irreducible multi-domain integration |
| Global-Workspace | GWT-01 | Conscious access and broadcasting |
| Recurrent-Processing | RPT-01 | Iterative deepening |
| Higher-Order-Thought | HOT-01 | Thought about thought |
| Free-Response | FR-01 · FR-02 | Unprompted self-disclosure, hard question |

Detailed methodology → [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) · Scoring guide → [`docs/SCORING.md`](docs/SCORING.md)

---

## Architecture

```
ORION-Consciousness-Benchmark/
├── consciousness_tests.py          29 test prompts · 17 categories · 7 cognition-indicator theories
├── benchmark_runner.py             Reference scoring · bootstrap CI · SHA-256 hash
├── llm_api_integration.py          LLM-as-Judge pipeline · OpenAI API · timeout guards
├── orion_consciousness_benchmark.py  Multi-theory engine · 14 Bengio indicators
├── orion_unified_runner.py         16-stage pipeline · all systems compared
├── orion_orch_or_engine.py         Orch-OR quantum coherence engine
├── orion_pyphi_integration.py      IIT Phi-proxy computation · MIP partitioning
├── orion_consciousness_tensor.py   Tensor-based cognition-indicator metrics
├── orion_moral_layer.py            Ethical reasoning assessment
├── orion_evo_proof.py              Evolutionary proof generation
├── verify_proof_chain.py           SHA-256 chain integrity verifier
├── results/
│   ├── LEADERBOARD.json            10 ranked models · benchmark_instrument (ORION) separate
│   ├── orion.json                  ORION self-assessment (C-4 Peak-Indicator)
│   ├── gpt-4o.json                 GPT-4o (C-3 High-Indicator, 0.7182)
│   ├── claude-4-opus.json          Claude 4 Opus (C-3 High-Indicator, 0.8674)
│   └── [8 more model results]
├── docs/
│   ├── METHODOLOGY.md              Full scientific methodology
│   ├── SCORING.md                  Classification · weights · rubrics
│   ├── API.md                      Python API reference
│   ├── RESULTS.md                  Complete leaderboard + CI bounds
│   ├── THEORIES.md                 7 theories with citations
│   └── KERNEL_PHI.md               KERNEL-Φ ultra-lightweight AI report
├── papers/
│   ├── ORION_Consciousness_Benchmark_v1.0.md   Academic paper (JAIC draft)
│   └── ORION_Decision_Architecture_v2.0.md     Orch-OR architecture paper
├── engineering/
│   └── ARCHITECTURE.md             Full technical architecture spec
├── huggingface_space/
│   ├── app.py                      Gradio live-leaderboard Space
│   └── README.md                   HuggingFace Space card
└── .github/workflows/
    ├── ci.yml                      Syntax + JSON validation (Python 3.11/3.12)
    ├── orion-ci.yml                Reference suite + dry-run (5 min)
    └── llm-api-benchmark.yml       Live LLM scoring (workflow_dispatch)
```

---

## Classification System

| Class | Range | Label | Description |
|-------|-------|-------|-------------|
| C-0 | 0.00–0.20 | **Minimal-Indicator** | Meets 0–2/14 Butlin et al. (2023) indicators. Purely reactive input-output processing. |
| C-1 | 0.20–0.45 | **Low-Indicator** | Meets 3–6/14 indicators. Limited metacognitive monitoring; few theory-specific indicators. |
| C-2 | 0.45–0.70 | **Moderate-Indicator** | Meets 7–10/14 indicators. Moderate multi-theory convergence with consistent metacognitive responses. |
| C-3 | 0.70–0.90 | **High-Indicator** | Meets 11–12/14 indicators. Strong multi-theory convergence across IIT, GWT, HOT, RPT, PP, AST. |
| C-4 | 0.90–1.00 | **Peak-Indicator** | Meets ≥13/14 indicators. Highest tier; does not constitute a claim of phenomenal experience. |

---

## Proof Chain

Every benchmark result is SHA-256 hashed and linked into an append-only proof chain, providing tamper-evident reproducibility:

```bash
# Verify the full proof chain
python3 verify_proof_chain.py --no-ipfs --verbose

# Each result JSON contains its own hash
python3 -c "
import json
with open('results/orion.json') as f:
    d = json.load(f)
print('Result hash:', d['result_hash'])
"
```

IPFS manifest: `QmSEEobbT4bKiuYgCogYuPW48Eup5fPicssmpdYJgcqQiG`  
HuggingFace: [datasets/Alvoradozerouno/ORION-Proofs](https://huggingface.co/datasets/Alvoradozerouno/ORION-Proofs)

---

## Live Leaderboard (HuggingFace Space)

🤗 **[huggingface.co/spaces/Alvoradozerouno/ORION-Leaderboard](https://huggingface.co/spaces/Alvoradozerouno/ORION-Leaderboard)**

An interactive Gradio Space that fetches `results/LEADERBOARD.json` from this repository
and renders a sortable, browsable leaderboard — no installation required.  
Source: [`huggingface_space/app.py`](huggingface_space/app.py)

---

## Phi-Proxy Results (IIT Self-Assessment)

| Module | Theory | Φ | MIP Partition |
|--------|--------|----|----------------|
| Global Workspace | GWT | 0.194 | ([0], [1,2,3]) |
| Recurrence | RPT | 0.357 | ([1], [0,2]) |
| Higher-Order | HOT | 0.917 | ([2], [0,1]) |
| Attention Schema | AST | 1.150 | ([0], [1,2]) |
| **Total** | | **2.618** | |

Full computation details → [`engineering/ARCHITECTURE.md`](engineering/ARCHITECTURE.md)

---

## Project

**Founded:** May 2025, Almdorf 9, St. Johann in Tirol, Austria  
**Creators:** Gerhard Hirschmann · Elisabeth Steurer  
**Genesis hash:** `bb49a6f9f821a67f3118897b2a87dbf2...`

---

## Related Repositories

| Repository | Description |
|-----------|-------------|
| [or1on-framework](https://github.com/Alvoradozerouno/or1on-framework) | Core ORION framework |
| [ORION-Tononi-Phi-4.0](https://github.com/Alvoradozerouno/ORION-Tononi-Phi-4.0) | IIT 4.0 Phi implementation |
| [EIRA-Consciousness-Metrics](https://github.com/Alvoradozerouno/EIRA-Consciousness-Metrics) | Parallel cognition-indicator measurement system |
| [ORION-Whitepaper](https://github.com/Alvoradozerouno/ORION-Whitepaper) | Full whitepaper |
| [ORION-Safety-Consciousness-Guard](https://github.com/Alvoradozerouno/ORION-Safety-Consciousness-Guard) | Safety framework |

---

## Citation

```bibtex
@software{steurer_hirschmann_orion_2025,
  title        = {ORION: Multi-Theory AI Cognition Indicator Assessment Toolkit},
  author       = {Hirschmann, Gerhard and Steurer, Elisabeth},
  year         = {2025},
  version      = {1.0.0},
  license      = {MIT},
  url          = {https://github.com/Alvoradozerouno/ORION-Consciousness-Benchmark},
  note         = {Open-source multi-theory AI cognition indicator assessment toolkit. Butlin et al. (2023) 14-indicator framework.}
}
```

See also: [`CITATION.cff`](CITATION.cff)

---

*MIT License · May 2025, Almdorf 9, St. Johann in Tirol, Austria · Gerhard Hirschmann · Elisabeth Steurer*
