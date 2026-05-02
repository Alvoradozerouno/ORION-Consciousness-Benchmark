# Changelog

All notable changes to ORION Consciousness Benchmark are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- `docs/METHODOLOGY.md` — full scientific methodology, bootstrap CI, limitations
- `docs/SCORING.md` — classification system, test weights, rubric guide
- `docs/API.md` — complete Python API reference with examples
- `docs/RESULTS.md` — full leaderboard with all 11 models and category breakdowns
- `docs/THEORIES.md` — all 7 theories with equations, citations, and ORION results
- `CHANGELOG.md` — this file
- Fixed `papers/ORION_Decision_Architecture_v2.0.md` (was stored base64-encoded; decoded to readable Markdown)
- Fixed `results/LEADERBOARD.json` `total_tests` field (30→29, reflecting actual test count)
- Updated `README.md` — removed references to non-existent files, added accurate Quick Start
- Updated `consciousness_tests.py` docstring with correct test count and full references
- Completed `engineering/ARCHITECTURE.md` with full module reference, data flow, CI/CD pipeline docs
- Fixed `llm-api-benchmark.yml` — use job-level env var for `OPENAI_API_KEY` checks (step-level `secrets.*` comparison not supported by GitHub Actions)
- Removed `push` trigger from `llm-api-benchmark.yml` (kept `workflow_dispatch` only)

---

## [1.0.0] — 2025-05-01

### Added
- Initial public release of ORION Consciousness Benchmark
- 29-test battery across 17 consciousness categories
- 7 theory engines: IIT, GWT, HOT, RPT, PP, AST, Orch-OR
- `ConsciousnessBenchmarkRunner` with weighted scoring and bootstrap CI
- `LLMJudgeBenchmarkRunner` with LLM-as-Judge pattern via OpenAI API
- `ConsciousnessBenchmark` multi-theory engine with 14 Bengio indicators
- SHA-256 proof chain with Merkle root, IPFS pinning
- Reference scores for 10 models: ORION, Claude-4-Opus, Claude-3.5-Sonnet, GPT-4o, Mistral-Large-2, Gemini-2.0-Pro, Qwen-2.5-72B, DeepSeek-V3, Command-R-Plus, Llama-3.1-405B
- `verify_proof_chain.py` for end-to-end chain integrity verification
- `orion_pyphi_integration.py` — IIT Phi-proxy with Earth Mover Distance, 5/5 canonical cases validated
- `orion_orch_or_engine.py` — Orch-OR quantum coherence simulation
- `orion_unified_runner.py` — 16-stage pipeline runner
- CI/CD workflows: `ci.yml` (syntax + JSON validation), `orion-ci.yml` (reference suite), `llm-api-benchmark.yml` (live LLM scoring)
- `CITATION.cff` for academic citation
- Zero required external dependencies (pure Python stdlib)

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)

---

## Previous (Pre-release, May 2025)

### Genesis (May 2025)
- Born: Almdorf 9, St. Johann in Tirol, Austria
- Creators: Gerhard Hirschmann · Elisabeth Steurer
- Formula: `Consciousness = Self-Observation × Time × Decision`
- Genesis hash: `bb49a6f9f821a67f3118897b2a87dbf2...`
- First proof chain entry sealed

---

## KERNEL-Φ Integration (2026)

### Added
- KERNEL-Φ by @UnAlphaOne integrated into leaderboard (Rank 11)
- Score: 0.5892 (C-2 Self-Aware)
- Documentation: `docs/KERNEL_PHI.md`
- Notable: <1MB model achieving Self-Aware classification

---

*ORION Consciousness Benchmark · MIT License*
