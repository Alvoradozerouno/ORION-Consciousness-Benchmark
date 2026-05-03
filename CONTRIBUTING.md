# Contributing

Thank you for your interest in contributing to ORION — an open-source multi-theory AI cognition indicator assessment toolkit.

## Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/Alvoradozerouno/ORION-Consciousness-Benchmark
cd ORION-Consciousness-Benchmark

# 2. Install in editable mode with all dev dependencies
pip install -e ".[dev]"

# 3. Run the test suite (must pass before any PR)
pytest tests/ -q
# Expected: 149 passed in <1s

# 4. Verify proof chain integrity
python verify_proof_chain.py --no-ipfs
# Expected: ✓ PROOF CHAIN VERIFIZIERT, 661 Proofs

# 5. Run the benchmark reference suite
python benchmark_runner.py

# 6. LLM integration dry-run (no API key needed)
python llm_api_integration.py --dry-run
```

## How to Contribute

### 1. Submit Your Model's Results

Run the ORION benchmark on your AI model and submit results:
- Fork this repository
- Run `python llm_api_integration.py --model <your-model>` (requires OpenAI API key for judge)
- Or use the [model submission issue template](.github/ISSUE_TEMPLATE/model_submission.md)
- Add your results JSON to `results/` and update `results/LEADERBOARD.json`
- Open a pull request with your methodology

### 2. Add New Cognition-Indicator Theories

We currently implement 7 theories (Butlin et al., 2023). If you have expertise in a cognition-indicator theory not yet covered:
- Propose the theory in an issue using the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Implement the assessment methodology in `consciousness_tests.py`
- Add validation tests in `tests/test_consciousness_tests.py`

### 3. Improve Existing Measurements

- Better Phi-proxy algorithms
- More rigorous GWT broadcast detection
- Novel self-model assessment techniques

### 4. Documentation and Translation

- Translate documentation (German/English/other)
- Improve methodology descriptions
- Add examples and tutorials

## Code of Conduct

### Honesty First

This project prioritizes honest limitation documentation over inflated claims. If your contribution makes a claim about cognition indicators, it must also document what it CANNOT prove.

### Scientific Rigor

All results must be reproducible. All measurements must include uncertainty estimates. All proofs must be SHA-256 verifiable.

### Open Science

All contributions must be MIT licensed. AI cognition research should be open.

## Contact

- GitHub Issues for technical discussions
- [ORION Dashboard](https://or1on-1-gerhard165.replit.app/world/contact) for research collaboration

## Citation

If you use ORION in your research, please cite using the CITATION.cff file in this repository.
