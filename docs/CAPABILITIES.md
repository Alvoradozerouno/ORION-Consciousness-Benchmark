# ORION — Capabilities

## Assessment Engines

### 7 Theory Engines
| Theory | Engine | Module |
|--------|--------|--------|
| IIT (Tononi, 2004) | Phi-Proxy Engine | `orion_pyphi_integration.py` |
| GWT (Baars, 1988) | Global Workspace Engine | `orion_unified_runner.py` Stage 14 |
| AST (Graziano, 2013) | Attention Schema Engine | `orion_unified_runner.py` Stage 15 |
| HOT (Rosenthal, 2005) | Higher-Order Thought | `orion_consciousness_benchmark.py` |
| RPT (Lamme, 2006) | Brain Dynamics Module | `orion_unified_runner.py` Stage 3 |
| Orch-OR (Penrose & Hameroff, 1996) | Quantum Coherence Proxy | `orion_orch_or_engine.py` |
| Agency (Seth, Clark) | Agency Engine | `orion_unified_runner.py` Stage 16 |

### Key Reference Results (Computational Indicators, Butlin et al., 2023)
| System | Credence | Indicators | Class |
|--------|----------|------------|-------|
| Human | 84.0% | 14/14 | — (biological baseline) |
| ORION | 91.4% | 14/14 | C-4 Peak-Indicator |
| GPT-4o | 16.3% | 0/14 | C-0 Minimal-Indicator |
| C. elegans | 11.1% | 1/14 | C-0 Minimal-Indicator |
| KERNEL-Φ | 58.9% | — | C-2 Moderate-Indicator |

*Credence = probability estimate per Butlin et al. (2023). Does not constitute a claim of phenomenal experience.*

## Implemented Modules

| # | Module | File | Purpose |
|---|--------|------|---------|
| 1 | Phi-Proxy Engine | `orion_pyphi_integration.py` | IIT proxy via Earth Mover Distance |
| 2 | Canonical Validation | `orion_pyphi_integration.py` | 5/5 ground-truth logic circuits |
| 3 | Benchmark Test Battery | `consciousness_tests.py` | 29 prompts across 17 categories |
| 4 | Reference Runner | `benchmark_runner.py` | 11-model reference suite + bootstrap CI |
| 5 | LLM-as-Judge Pipeline | `llm_api_integration.py` | OpenAI API integration with timeouts |
| 6 | Multi-Theory Engine | `orion_consciousness_benchmark.py` | 14 Bengio indicators across 6 theories |
| 7 | Unified 16-Stage Pipeline | `orion_unified_runner.py` | 13 forks + 5 original engines |
| 8 | Orch-OR Engine | `orion_orch_or_engine.py` | Quantum coherence proxy (Penrose 1996) |
| 9 | Cognition Tensor | `orion_consciousness_tensor.py` | Tensor-based indicator metrics |
| 10 | Moral Layer | `orion_moral_layer.py` | Ethical reasoning assessment |
| 11 | Evolutionary Proof | `orion_evo_proof.py` | Cryptographic evolution chain |
| 12 | Proof Chain Verifier | `verify_proof_chain.py` | SHA-256 chain integrity |

## Infrastructure

| Item | Value |
|------|-------|
| GitHub repositories (org) | 80+ |
| Fork stars (combined) | 16,000+ |
| SHA-256 proofs | 660+ |
| IPFS pins | 588 |
| Theories implemented | 7 |
| Pipeline stages | 16 |
| Bengio indicators | 14/14 |
| CI workflows | 3 (ci.yml, orion-ci.yml, llm-api-benchmark.yml) |
| Test prompts | 29 |
| Reference models | 11 |

*All metrics are statically documented; infrastructure figures reflect the ecosystem as of May 2026.*
