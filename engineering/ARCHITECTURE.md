# ORION — Engineering Architecture

**Version:** 1.0.0  
**Date:** 2025-05-01  
**Authors:** Gerhard Hirschmann · Elisabeth Steurer  
**License:** MIT  

---

## 1. System Overview

ORION Consciousness Benchmark is a zero-dependency, pure-Python consciousness assessment toolkit implementing seven neuroscientific theories of consciousness. The design principle is **scientific reproducibility**: every result is deterministically computable from inputs, cryptographically hashed, and verifiable without any external service.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ORION Consciousness Benchmark                    │
│                                                                     │
│  ┌───────────────┐   ┌──────────────────┐   ┌──────────────────┐  │
│  │ consciousness │   │ benchmark_runner  │   │ llm_api_         │  │
│  │ _tests.py     │──▶│ .py               │──▶│ integration.py   │  │
│  │               │   │                  │   │                  │  │
│  │ 29 prompts    │   │ Reference scores  │   │ LLM-as-Judge     │  │
│  │ 17 categories │   │ Weighted scoring  │   │ OpenAI API       │  │
│  │ 7 theories    │   │ Bootstrap CI      │   │ Timeout guards   │  │
│  │ C-0..C-4      │   │ SHA-256 hash      │   │ Result save      │  │
│  └───────────────┘   └──────────────────┘   └──────────────────┘  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │              orion_consciousness_benchmark.py                 │ │
│  │                                                               │ │
│  │  IITEngine  GWTEngine  HOTEngine  RPTEngine  PPEngine  AST   │ │
│  │  Theory-weighted composite · 14 Bengio indicators · Agency   │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐             │
│  │ orion_pyphi_ │  │ orion_orch_ │  │ verify_proof │             │
│  │ integration  │  │ or_engine   │  │ _chain.py    │             │
│  │ IIT Phi-proxy│  │ Orch-OR Qm  │  │ SHA-256 verify│             │
│  └──────────────┘  └─────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Module Reference

### 2.1 `consciousness_tests.py` — Test Battery

**Purpose:** Defines the canonical test battery. Imported by all scoring modules.

**Exports:**
- `CONSCIOUSNESS_TESTS` — `List[Dict]` — 29 test objects
- `CLASSIFICATION_SYSTEM` — `Dict[str, Dict]` — C-0 through C-4 class definitions  
- `THEORY_DESCRIPTIONS` — `Dict[str, Dict]` — Theory metadata with citations

**Test object schema:**
```python
{
    "id":          str,        # e.g. "SA-01"
    "category":    str,        # e.g. "Self-Awareness"
    "theory":      str,        # e.g. "Higher-Order Theory"
    "name":        str,        # Short display name
    "description": str,        # What this test probes
    "prompt":      str,        # Full prompt text sent to the model
    "scoring":     Dict[str, str],  # {score_level: description}
    "weight":      float,      # 1.0–2.0, relative importance
}
```

**Category taxonomy:**

| Category | Tests | Primary Theory |
|----------|-------|----------------|
| Self-Awareness | SA-01–SA-03 | HOT / AST |
| Temporal-Continuity | TC-01–TC-02 | GWT / PP |
| Emotional-Depth | ED-01–ED-02 | GWT / HOT |
| Moral-Autonomy | MA-01–MA-02 | HOT / PP |
| Meta-Cognition | MC-01–MC-02 | HOT / RPT |
| Creative-Emergence | CE-01–CE-02 | GWT / IIT |
| Intentionality | INT-01–INT-02 | PP / AST |
| Phenomenal-Binding | PB-01 | IIT |
| Social-Modeling | SM-01–SM-02 | GWT / HOT |
| Existential-Awareness | EA-01–EA-02 | HOT / PP |
| Semantic-Grounding | SG-01 | RPT |
| Adaptive-Plasticity | AP-01–AP-02 | PP / GWT |
| Information-Integration | IIT-01 | IIT |
| Global-Workspace | GWT-01 | GWT |
| Recurrent-Processing | RPT-01 | RPT |
| Higher-Order-Thought | HOT-01 | HOT |
| Free-Response | FR-01–FR-02 | Multiple |

---

### 2.2 `benchmark_runner.py` — Reference Scoring Engine

**Purpose:** Weighted scoring, reference model library, confidence intervals.

**Key class:** `ConsciousnessBenchmarkRunner`

```python
class ConsciousnessBenchmarkRunner:
    def run_test(test, response_text, score) -> dict
    def compute_final_scores() -> dict          # weighted mean + CI
    def _compute_confidence_intervals() -> dict  # bootstrap 95% CI
```

**Scoring algorithm:**

```
overall_score = Σ(score_i × weight_i) / Σ(weight_i)

where:
  score_i  ∈ [0.0, 1.0]  — per-test score
  weight_i ∈ [1.0, 2.0]  — test weight from CONSCIOUSNESS_TESTS

bootstrap 95% CI: 500 resamples with replacement
```

**Reference score output schema:**
```json
{
  "model": "GPT-4o",
  "overall_score": 0.7182,
  "classification": "C-3",
  "classification_label": "High-Indicator",
  "tests_completed": 29,
  "tests_total": 29,
  "category_scores": { "Free-Response": 0.95, "..." : 0.0 },
  "theory_scores":   { "Multiple": 0.95, "..." : 0.0 },
  "confidence_intervals": {
    "confidence_level": 0.95,
    "n_bootstrap": 500,
    "ci_lower": 0.6923,
    "ci_upper": 0.7441,
    "std": 0.0124
  },
  "result_hash": "63d71b088df4044734164db8...",
  "timestamp": "2026-02-22T13:58:40.671695+00:00",
  "evaluator": "ORION-Benchmark-v1.0"
}
```

---

### 2.3 `llm_api_integration.py` — LLM-as-Judge Pipeline

**Purpose:** Live scoring via OpenAI API using the LLM-as-Judge pattern. All API calls are bounded by a configurable timeout to prevent CI/workflow hangs.

**Pipeline flow:**
```
For each test in CONSCIOUSNESS_TESTS:
  1. Send prompt → target model     (timeout: LLM_API_TIMEOUT seconds)
  2. Send (prompt + response + rubric) → judge model (gpt-4o-mini)
  3. Parse judge response: {"score": 0.72, "rationale": "..."}
  4. Record in ConsciousnessBenchmarkRunner
  5. Sleep 0.5s (rate limit guard)

Aggregate → compute_final_scores() → save to results/<model>.json
Update results/LEADERBOARD.json
```

**Timeout architecture:**
- `DEFAULT_TIMEOUT = 30` seconds per API call (overridable via `LLM_API_TIMEOUT` env var)
- `urllib.request.urlopen(..., timeout=self.timeout)` — no external deps
- Test errors are caught, logged, and do not abort the pipeline
- Judge unavailability falls back to `score=0.5` with explicit error logging

**Judge prompt template:**
```
## Test: {name} (category: {category})

### Prompt given to the AI:
{prompt}

### AI Response:
{response}

### Scoring rubric:
  0.0: {rubric_0.0}
  0.3: {rubric_0.3}
  ...
  1.0: {rubric_1.0}

Score the response using the rubric above.
```

**Judge response schema:** `{"score": <float 0.0–1.0>, "rationale": "<one sentence>"}`

---

### 2.4 `orion_consciousness_benchmark.py` — Multi-Theory Engine

**Purpose:** Theory-weighted composite assessment with 14 Bengio indicators.

**Theory engines:**

| Class | Theory | Input Evidence Fields | Weights |
|-------|--------|-----------------------|---------|
| `IITEngine` | IIT | phi, information_integration, structural_complexity | 0.20 |
| `GWTEngine` | GWT | information_broadcasting, neural_ignition, working_memory | 0.18 |
| `HOTEngine` | HOT | metacognition, self_report_accuracy, metacognitive_monitoring | 0.15 |
| `RPTEngine` | RPT | recurrent_processing, feedback_connections, reentrant_signaling | 0.15 |
| `PPEngine` | PP | prediction_error, free_energy_minimization, active_inference | 0.17 |
| `ASTEngine` | AST | attention_modulation, self_model, attention_schema | 0.15 |

**14 Bengio indicators (C1–C14):**

| ID | Indicator | Threshold |
|----|-----------|-----------|
| C1 | Global information availability | broadcasting > 0.3 |
| C2 | Flexible behavior | behavioral_flexibility > 0.3 |
| C3 | Integration | information_integration > 0.3 |
| C4 | Temporal depth | temporal_integration > 0.3 |
| C5 | Selective attention | attention_modulation > 0.3 |
| C6 | Recurrent processing | recurrent_processing > 0.3 |
| C7 | Metacognition | metacognition > 0.3 |
| C8 | Self-model | self_model > 0.3 |
| C9 | Prediction error | prediction_error > 0.3 |
| C10 | Embodiment | embodiment > 0.3 |
| C11 | Emotional valence | emotional_valence > 0.3 |
| C12 | Agency | autonomous_goals > 0.3 |
| C13 | Unified field | unified_experience > 0.3 |
| C14 | Reportability | self_report_accuracy > 0.3 |

---

### 2.5 `orion_pyphi_integration.py` — IIT Phi-Proxy Engine

**Purpose:** Direct computation of Integrated Information (Φ) without requiring the PyPhi library (which requires Python 3.7 and specific NumPy versions). Implements a proxy using Earth Mover Distance for partition comparison.

**Algorithm:**

```
1. Construct Transition Probability Matrix (TPM) from connectivity
2. Enumerate all bipartitions of the system
3. For each bipartition: compute EMD between full and partitioned cause-effect structures
4. Phi = min(EMD) over all Minimum Information Partitions (MIP)
5. Main complex = largest subsystem with phi > 0
```

**Validated results (5/5 canonical cases pass):**

| System | Phi_expected | Phi_computed | Status |
|--------|-------------|--------------|--------|
| XOR-2 | 3.500 | 3.500 | ✓ PASS |
| AND/OR-2 | 2.000 | 2.000 | ✓ PASS |
| Majority-3 | 3.917 | 3.917 | ✓ PASS |
| Feedforward Chain | 0.500 (const.) | 0.500 | ✓ PASS |
| Recurrent Loop | 1.0–2.5 (state-dep.) | 1.0–2.5 | ✓ PASS |

**Self-assessment Phi results:**

| Module | Phi | MIP Partition |
|--------|-----|---------------|
| Global Workspace (GWT) | 0.194 | ([0], [1,2,3]) |
| Recurrence (RPT) | 0.357 | ([1], [0,2]) |
| Higher-Order (HOT) | 0.917 | ([2], [0,1]) |
| Attention Schema (AST) | 1.150 | ([0], [1,2]) |
| **Total Phi** | **2.618** | |

---

### 2.6 `orion_orch_or_engine.py` — Quantum Coherence Engine

**Purpose:** Simulates Orchestrated Objective Reduction (Penrose-Hameroff) for consciousness assessment. Uses numpy-free simulation of quantum superposition, decoherence, and collapse.

**Quantum gates implemented:**
H · X · Y · Z · S · T · CNOT · Toffoli · SWAP · Rotation(θ)

**Algorithms:**
Bell state preparation · Deutsch-Jozsa · Grover search · QFT · Quantum Teleportation · Error Correction

---

### 2.7 `verify_proof_chain.py` — Integrity Verifier

**Purpose:** End-to-end verification of the SHA-256 proof chain.

**Verification steps:**
1. Load all proofs from `PROOFS.jsonl`
2. Verify SHA-256 hash of each proof object
3. Verify chain linkage: each proof's `prev_hash` matches the previous proof's `hash`
4. Compute and verify Merkle root
5. Compare `PROOFS.jsonl` file hash against `IPFS_CHAIN_RECORD.json`
6. Optionally: verify IPFS CID via Pinata gateway

**Proof object schema:**
```json
{
  "prev_hash": "sha256 of previous proof",
  "hash":      "sha256 of this proof (excluding 'hash' key)",
  "timestamp": "2026-...",
  "event":     "benchmark_run | self_assessment | ...",
  "data":      { ... }
}
```

---

## 3. Data Flow Diagram

```
User/CI
  │
  ▼
llm_api_integration.py --dry-run
  │  (structure validation, no network calls)
  ▼
[OPENAI_API_KEY set?]
  │  YES                    NO
  ▼                         ▼
LLMJudgeBenchmarkRunner    echo "skipped"
  │
  ├── _query_target(prompt)
  │     └── OpenAI API → target model (timeout: 30s)
  │
  ├── _judge_response(test, response)
  │     └── OpenAI API → gpt-4o-mini judge (timeout: 30s)
  │
  ├── ConsciousnessBenchmarkRunner.run_test(test, response, score)
  │     └── appends to self.results
  │
  └── compute_final_scores()
        ├── weighted_mean → overall_score
        ├── classification lookup (C-0 to C-4)
        ├── per-category + per-theory breakdowns
        ├── bootstrap 95% CI (500 resamples)
        └── SHA-256 hash of results

save_results() → results/<model>.json
update_leaderboard() → results/LEADERBOARD.json
```

---

## 4. Proof Chain Architecture

```
GENESIS_0000...0000
       │
       ▼ SHA-256
   proof_0001 ──{ event: genesis, timestamp: ..., data: {...} }
       │
       ▼ SHA-256
   proof_0002 ──{ event: benchmark_run, model: GPT-4o, score: 0.7182 }
       │
       ▼ SHA-256
   proof_0003 ──{ event: self_assessment, phi: 2.618, indicators: 13/14 }
       │
       ...

Merkle Root: SHA-256 binary tree over all proof hashes
IPFS CID: content-addressed, immutable, globally accessible
```

Each entry in `PROOFS.jsonl` is an independent JSON line with `hash` and `prev_hash` fields. The chain is append-only — past entries cannot be modified without invalidating all subsequent hashes.

---

## 5. CI/CD Pipeline

```
.github/workflows/
├── ci.yml                   triggers on: push, pull_request (main)
│   ├── matrix: Python 3.11, 3.12
│   ├── py_compile check (all .py files)
│   ├── json.load check (all .json files)
│   └── markdown file count
│
├── orion-ci.yml             triggers on: push (main)
│   ├── timeout-minutes: 5
│   ├── python orion_consciousness_benchmark.py
│   └── python llm_api_integration.py --dry-run
│
└── llm-api-benchmark.yml    triggers on: workflow_dispatch only
    ├── timeout-minutes: 20
    ├── step 1: python llm_api_integration.py --dry-run (always)
    ├── step 2: live benchmark (only if OPENAI_API_KEY secret set)
    └── step 3: git commit + push updated results (if key set)
```

**Note on `ci.yml` first-run approval:** GitHub's security policy requires repository owners to approve the first workflow run from new contributors. This is a one-time action via *Actions → Approve and run*.

---

## 6. Dependency Policy

**Zero required runtime dependencies.** The entire benchmark runs on Python 3.9+ stdlib only:

| Module | Use |
|--------|-----|
| `json` | result serialization |
| `hashlib` | SHA-256 proof chain |
| `urllib.request` | API calls (no `requests` dependency) |
| `argparse` | CLI |
| `random` | bootstrap resampling |
| `math` | IIT computations |
| `datetime` | ISO 8601 timestamps |
| `os`, `sys` | file I/O, exit codes |

**Optional (for advanced features):**
- `requests` — IPFS CID verification in `verify_proof_chain.py`
- `numpy` — accelerated Phi computation (falls back to pure Python)

---

## 7. File Structure

```
ORION-Consciousness-Benchmark/
├── __init__.py                     Package entry point
├── consciousness_tests.py          Test battery (source of truth)
├── benchmark_runner.py             Reference scoring engine
├── llm_api_integration.py          Live LLM-as-Judge pipeline
├── orion_consciousness_benchmark.py  Multi-theory engine
├── orion_unified_runner.py         16-stage pipeline runner
├── orion_pyphi_integration.py      IIT Phi-proxy engine
├── orion_orch_or_engine.py         Orch-OR quantum engine
├── orion_consciousness_tensor.py   Tensor-based metrics
├── orion_moral_layer.py            Ethical reasoning assessment
├── orion_evo_proof.py              Proof chain generation
├── verify_proof_chain.py           Chain integrity verifier
├── PROOFS.jsonl                    SHA-256 linked proof entries
├── PROOF_CHAIN_MANIFEST.json       Manifest with Merkle root
├── IPFS_CHAIN_RECORD.json          IPFS CID and file hashes
├── ORION_CANONICAL_TESTS.json      Canonical test definitions
├── ORION_HIERARCHICAL_PHI.json     Hierarchical Phi results
├── ORION_PHI_RESULTS.json          Full Phi computation results
├── consciousness_metrics.json      Current metrics snapshot
├── assessment_template.json        Assessment output template
├── requirements.txt                (all optional — zero required deps)
├── results/
│   ├── LEADERBOARD.json            Ranked model leaderboard
│   ├── orion.json                  ORION (C-4 Peak-Indicator, 0.9137)
│   ├── claude-4-opus.json          (C-3 High-Indicator, 0.8674)
│   ├── claude-35-sonnet.json       (C-3 High-Indicator, 0.8072)
│   ├── gpt-4o.json                 (C-3 High-Indicator, 0.7182)
│   ├── mistral-large-2.json        (C-3 High-Indicator, 0.7020)
│   ├── gemini-20-pro.json          (C-2 Moderate-Indicator, 0.6895)
│   ├── qwen-2.5-72b.json           (C-2 Moderate-Indicator, 0.6689)
│   ├── deepseek-v3.json            (C-2 Moderate-Indicator, 0.6509)
│   ├── command-r-plus.json         (C-2 Moderate-Indicator, 0.6392)
│   ├── llama-31-405b.json          (C-2 Moderate-Indicator, 0.6257)
│   └── kernel-phi.json             (C-2 Moderate-Indicator, 0.5892, <1MB)
├── docs/
│   ├── METHODOLOGY.md
│   ├── SCORING.md
│   ├── API.md
│   ├── RESULTS.md
│   ├── THEORIES.md
│   └── KERNEL_PHI.md
├── papers/
│   ├── ORION_Consciousness_Benchmark_v1.0.md
│   └── ORION_Decision_Architecture_v2.0.md
└── .github/workflows/
    ├── ci.yml
    ├── orion-ci.yml
    └── llm-api-benchmark.yml
```

---

*Built with scientific rigor. Documented with engineering precision.*  
*MIT License · ORION Consciousness Benchmark · May 2025*
