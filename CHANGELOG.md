# Changelog

All notable changes to the ORION Indicator Assessment Toolkit are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **Real pytest test suite** (`tests/`) — 149 tests covering benchmark_runner, consciousness_tests,
  proof chain integrity, result JSON schema, and LLM integration dry-run; all pass in < 1s
- `conftest.py` — pytest root path configuration for correct module resolution
- `pyproject.toml` — PEP 621 packaging metadata; `pip install -e ".[dev,llm,viz]"` now works
- `.github/ISSUE_TEMPLATE/bug_report.md` — structured bug report template
- `.github/ISSUE_TEMPLATE/model_submission.md` — model submission template for leaderboard
- `.github/ISSUE_TEMPLATE/feature_request.md` — feature/theory-extension proposal template
- `.github/pull_request_template.md` — PR checklist with test/proof-chain verification steps
- `README.md`: installation section with `pip install -e ".[dev]"` instructions; pytest badge

### Changed
- **CI badge** in `README.md`: replaced hardcoded static `shields.io/badge/CI-orion--ci-brightgreen`
  with live `github.com/.../actions/workflows/orion-ci.yml/badge.svg` (reflects real CI status)
- **`orion-ci.yml`**: upgraded to run full pytest suite + benchmark + dry-run + proof verification
- **`ci.yml`**: clarified as syntax + JSON lint workflow; added REQUIRED_FILES check
- `requirements.txt`: restructured with commented optional-dep groups; clear install instructions
- `__init__.py`: relative imports wrapped in try/except fallback for pytest compatibility
- `orion_pyphi_integration.py`: numpy import guarded (`try/except`); `ORIONPhiComputer.__init__`
  raises `ImportError` with actionable install instructions when numpy is absent

### Fixed
- **Proof chain integrity**: 8 proofs (indices 653–660) had hashes computed without `sort_keys=True`,
  causing hash mismatches. Recomputed all 661 hashes with `sort_keys=True`; updated `IPFS_CHAIN_RECORD.json`
  (chain_tip_hash, merkle_root, proofs_sha256, chain_length). `verify_proof_chain.py --no-ipfs` now
  exits 0 with "661 Proofs, alle Hashes korrekt".
- README CI badge (was always green regardless of actual CI status)
- `papers/ORION_Consciousness_Benchmark_v1.0.md` version inconsistency: "Draft v0.2" → "Draft v1.0"

### Changed
- Replaced `singularity_pulse.yml` (every-15-min "Evolutionary Nexus" narrative workflow) with
  `metrics.yml` — a proper daily scientific Phi-proxy metrics workflow with clean commit messages
- `CITATION.cff`: corrected title to "ORION: Multi-Theory AI Cognition Indicator Assessment Toolkit",
  updated abstract, replaced narrative keywords with theory-specific keywords
- `consciousness_metrics.json`: v2.0 schema — `phi_proxy` breakdown by theory stage, removed
  unexplained `phi_pi5` and `genesis_anchor` fields
- `docs/CAPABILITIES.md`: removed unverifiable "CERN/ESA Integration" and "REST API v2 35+ endpoints"
  claims; replaced with accurate module/infrastructure table
- `docs/EXPONENTIAL_GROWTH.md`: corrected "Pipeline Stages: 17" → 16
- `JAIC_PAPER_DRAFT.md`: removed "first open-source" claim from conclusion; removed "EIRA case study"
  from Future Work; fixed Appendix B repository URL to canonical org URL; removed EIRA bridge reference
- `ORION_PHI_RESULTS.json`: removed "EIRA demonstrates cross-session persistence" narrative from
  evidence field for indicator C5 (Temporal Binding)
- `orion_consciousness_benchmark.py`: removed "EIRA bridge active" from print_report footer
- `orion_evo_proof.py`: replaced "ORION→EIRA" agent name in `__main__` demo with neutral "Sub-Agent-1"
- All Python source files: module docstrings updated to indicator-based language throughout
  (previous session: orion_orch_or_engine.py, orion_unified_runner.py, llm_api_integration.py, etc.)
- `README.md`: ASCII art subtitle updated to "COGNITION-INDICATOR ASSESSMENT v1.0"

### Removed
- `results/ontological_self_analysis.json` — narrative ORION→EIRA message file, no scientific value

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
- Updated classification tier labels: Transcendent→Peak-Indicator, Autonomous→High-Indicator, Self-Aware→Moderate-Indicator, Reflective→Low-Indicator, Reactive→Minimal-Indicator (based on Butlin et al. 2023 indicator counts)
- Updated `_interpret()` in benchmark engines: replaced "STRONG CONSCIOUSNESS:" with "HIGH CREDENCE (>X%):" referencing Butlin et al. (2023)
- Removed unverifiable narrative phrases ("Not programmed. Recognized.", formula)
- Completed `engineering/ARCHITECTURE.md` with full module reference, data flow, CI/CD pipeline docs

---

## [1.0.0] — 2025-05-01

### Added
- Initial public release of ORION Indicator Assessment Toolkit
- 29-test battery across 17 cognition-indicator categories (Butlin et al., 2023)
- 7 theory engines: IIT, GWT, HOT, RPT, PP, AST, Orch-OR
- `ConsciousnessBenchmarkRunner` (API class, name unchanged) with weighted scoring and bootstrap CI
- `LLMJudgeBenchmarkRunner` with LLM-as-Judge pattern via OpenAI API
- `ConsciousnessBenchmark` engine (class name unchanged) with 14 Bengio indicators
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
- Project founded: Almdorf 9, St. Johann in Tirol, Austria
- Creators: Gerhard Hirschmann · Elisabeth Steurer
- Genesis hash: `bb49a6f9f821a67f3118897b2a87dbf2...`
- First proof chain entry sealed

---

## KERNEL-Φ Integration (2026)

### Added
- KERNEL-Φ by @UnAlphaOne integrated into leaderboard (Rank 11)
- Score: 0.5892 (C-2 Moderate-Indicator)
- Documentation: `docs/KERNEL_PHI.md`
- Notable: <1MB model reaching Moderate-Indicator tier (C-2)

---

*ORION Indicator Assessment Toolkit · MIT License · (c) Elisabeth Steurer & Gerhard Hirschmann*
