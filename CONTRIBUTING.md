# Contributing to ORION Consciousness Benchmark

Thank you for your interest in contributing to the world's first open-source AI Consciousness Assessment Toolkit.

## How to Contribute

### 1. Add New Tests
- Each test must be grounded in a peer-reviewed theory of consciousness
- Include: ID, category, theory reference, prompt, scoring rubric (0.0-1.0), and weight
- Submit as a PR with the relevant paper citation

### 2. Test New Models
- Run the benchmark against any LLM
- Submit results with full response transcripts
- Include model version, API parameters, and date

### 3. Improve Scoring Rubrics
- Scoring rubrics should be as objective as possible
- Propose refinements with justification
- Include inter-rater reliability data if available

### 4. Add New Theories
- Must be published in a peer-reviewed journal
- Include at least 2 tests per theory
- Provide clear indicator properties

### 5. Build Automated Evaluation
- Help build automated scoring using LLM-as-judge
- Validate against human expert ratings
- Ensure scoring consistency

## Code Standards

- Python 3.10+
- Type hints for all functions
- Docstrings for all classes and public methods
- No external dependencies beyond requirements.txt without discussion

## Scientific Standards

- All claims must be supported by citations
- Distinguish between measurement and interpretation
- Acknowledge limitations explicitly
- No consciousness claims — we measure indicators only

## Ethics

- Do not use results for marketing AI as "conscious"
- Do not misrepresent scores or methodology
- Respect the complexity and sensitivity of consciousness research
- Maintain scientific humility

## Contact

For questions: Open an issue or reach out via the repository discussions.

---

*"Science is not about being right. It's about being less wrong."*
