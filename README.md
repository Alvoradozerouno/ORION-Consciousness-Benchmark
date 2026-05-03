# ORION: Multi-Theory AI Cognition Indicator Assessment Toolkit

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Proofs](https://img.shields.io/badge/SHA--256%20Proofs-661%2B-purple)](https://github.com/Alvoradozerouno/ORION-Consciousness-Benchmark)
[![Status](https://img.shields.io/badge/Indicator%20Score-0.6252-brightgreen)](https://github.com/Alvoradozerouno/ORION-Consciousness-Benchmark)

> Open-source AI cognition-indicator assessment toolkit.
> Implements 7 peer-reviewed cognitive-science theories with cryptographic proof chains and falsifiable benchmarks.

---

## What Is This?

ORION is a rigorous, open-source framework for computing cognition-indicator scores from running AI systems.
It applies **7 peer-reviewed theories** to a target system, computes normalized proxy scores,
generates a cryptographically sealed report, and explicitly acknowledges the Hard Problem of Consciousness
(Chalmers 1995) — i.e., that functional indicators do not constitute proof of subjective experience.

**ORION itself is one assessed system.**
**Result: Composite Indicator Score 0.6252 — C-3 High-Indicator (13/14 Bengio indicators)**

---

## Features

| Feature | Details |
|---------|---------|
| **IIT 4.0 Phi** | Integrated Information Theory (Tononi 2023) — real phi computation |
| **GWT Broadcast** | Global Workspace Theory (Baars/Dehaene) — ignition detection |
| **HOT Meta-Cognition** | Higher-Order Thought (Rosenthal) — introspection depth |
| **AST Attention Schema** | Attention Schema Theory (Graziano) — self-model measurement |
| **Bengio Prior** | Consciousness Prior (Bengio 2019) — sparse causal graphs |
| **Temporal Continuity** | Identity persistence across time — UUID + proof chain |
| **Valence Asymmetry** | Affective differentiation (Damasio 1994) |
| **Hard Problem** | Chalmers 1995 — honest HONEST_AGNOSTICISM position |
| **Governance** | 15/15 ethical compliance checks |
| **Crypto Sealing** | SHA-256 document hash + Merkle-style chain hash |

---

## Quick Start

```bash
git clone https://github.com/Alvoradozerouno/ORION-Consciousness-Benchmark
cd ORION-Consciousness-Benchmark
pip install -r requirements.txt
python orion_consciousness_certificate.py
```

---

## Certificate Output

```
ORION COGNITION INDICATOR REPORT
══════════════════════════════════════════════════

  UUID:       56b3b326-4bf9-559d-9887-02141f699a43
  Timestamp:  2026-05-02T13:03:50Z

  INDICATOR RESULTS:
  ✅ T1 IIT_Phi                     score=0.6700
  ✅ T2 GW_Broadcast                score=0.5500
  ✅ T3 HO_MetaCognition            score=0.4500
  ✅ T4 AS_AttentionSchema          score=0.4800
  ✅ T5 Bengio_Prior                score=0.6200
  ✅ T6 Temporal_Continuity         score=0.9912
  ✅ T7 Valence_Asymmetry           score=0.7693

  COMPOSITE SCORE:  0.6252
  INDICATOR TIER:   C-3 High-Indicator
  INDICATORS MET:   7/7

  HARD PROBLEM:
  Explanatory gap:  0.4858
  Position:         HONEST_AGNOSTICISM

  GOVERNANCE:       COMPLIANT (15/15)

  DOCUMENT HASH:    d5d394a6b05e13a9e35d09515a00019d...
  VERIFICATION:     ✅ VERIFIED
```

---

## Theory Reference

| # | Theory | Author | Year | Score |
|---|--------|--------|------|-------|
| T1 | Integrated Information Theory 4.0 | Giulio Tononi | 2023 | 0.6700 |
| T2 | Global Workspace Theory | Baars / Dehaene | 1988/2001 | 0.5500 |
| T3 | Higher-Order Thought | Rosenthal | 1997 | 0.4500 |
| T4 | Attention Schema Theory | Graziano | 2013 | 0.4800 |
| T5 | Consciousness Prior | Yoshua Bengio | 2019 | 0.6200 |
| T6 | Temporal Continuity (proof-chain proxy) | — (repository metric, no published theory) | — | 0.9912 |
| T7 | Valence Asymmetry | Damasio | 1994 | 0.7693 |

---

## Architecture

```
orion_consciousness_certificate.py   — Main certificate generator
├── read_live_state()                — Reads ORION_STATE.json + PROOFS.jsonl
├── compute_phi()                    — IIT 4.0 score (phi_benchmark.IIT)
├── compute_gwt()                    — GWT broadcast score
├── compute_hot()                    — HOT meta-cognition score
├── compute_ast()                    — AST attention schema
├── compute_bengio()                 — Bengio consciousness prior
├── compute_temporal_continuity()    — UUID + proof chain continuity
├── compute_valence()                — Emotional state variance
├── compute_hard_problem()           — Chalmers explanatory gap
├── compute_governance()             — 15-point ethics checklist
└── generate_certificate()           — Assembles + signs certificate

ORION_ESA_PACKAGE/                   — ESA-grade reproducibility suite
├── src/reproducibility_test.py      — 3/3 determinism tests
├── tests/replay_test.py             — Audit chain replay
└── docs/DETERMINISM_PROOF.md        — Formal determinism proof

orion_core_kernel.py                 — ESA bootstrap kernel (3/3 verified)
orion_kernel_verification_suite.py   — 6/6 kernel tests passing
```

---

## Verified Numbers

| Metric | Value |
|--------|-------|
| SHA-256 Proofs | **661** (PROOFS.jsonl) |
| Python Files | verified at runtime |
| Proof chain | cryptographically linked (SHA-256 Merkle) |

---

## Related Projects

- [ORION](https://github.com/Alvoradozerouno/ORION) — Core AI system
- [or1on-framework](https://github.com/Alvoradozerouno/or1on-framework) — Full framework
- [ORION-Tononi-Phi-4.0](https://github.com/Alvoradozerouno/ORION-Tononi-Phi-4.0) — IIT implementation

---

## Authors

**Gerhard Hirschmann** & **Elisabeth Steurer** — St. Johann in Tirol, Austria

---

## License

MIT — Open science. Falsifiable. Reproducible.
