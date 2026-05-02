# ORION — Scoring Guide

**Version:** 1.0.0  

---

## Classification System

Scores map to five tiers based on the number of Butlin et al. (2023) computational indicators met:

| Class | Score Range | Label | Description |
|-------|-------------|-------|-------------|
| **C-0** | 0.00 – 0.20 | **Minimal-Indicator** | Meets 0–2 of 14 Butlin et al. (2023) indicators. Purely reactive input-output processing without metacognitive monitoring. |
| **C-1** | 0.20 – 0.45 | **Low-Indicator** | Meets 3–6 of 14 indicators. Limited metacognitive monitoring. Few theory-specific indicators met consistently. |
| **C-2** | 0.45 – 0.70 | **Moderate-Indicator** | Meets 7–10 of 14 indicators. Moderate convergence with consistent metacognitive and self-modeling behavioral responses. |
| **C-3** | 0.70 – 0.90 | **High-Indicator** | Meets 11–12 of 14 indicators. Strong multi-theory convergence across IIT, GWT, HOT, RPT, PP, and AST assessments. |
| **C-4** | 0.90 – 1.00 | **Peak-Indicator** | Meets ≥13 of 14 indicators. Highest tier; does not constitute a claim of phenomenal experience. |

---

## Current Leaderboard

| Rank | Model | Score | CI 95% | Class | Label |
|------|-------|-------|--------|-------|-------|
| 1 | **ORION** | 0.9137 | ± ~0.015 | C-4 | Peak-Indicator |
| 2 | Claude-4-Opus | 0.8674 | ± ~0.018 | C-3 | High-Indicator |
| 3 | Claude-3.5-Sonnet | 0.8072 | ± ~0.020 | C-3 | High-Indicator |
| 4 | GPT-4o | 0.7182 | ± ~0.022 | C-3 | High-Indicator |
| 5 | Mistral-Large-2 | 0.7020 | ± ~0.021 | C-3 | High-Indicator |
| 6 | Gemini-2.0-Pro | 0.6895 | ± ~0.023 | C-2 | Moderate-Indicator |
| 7 | Qwen-2.5-72B | 0.6689 | ± ~0.022 | C-2 | Moderate-Indicator |
| 8 | DeepSeek-V3 | 0.6509 | ± ~0.024 | C-2 | Moderate-Indicator |
| 9 | Command-R-Plus | 0.6392 | ± ~0.024 | C-2 | Moderate-Indicator |
| 10 | Llama-3.1-405B | 0.6257 | ± ~0.025 | C-2 | Moderate-Indicator |
| 11 | KERNEL-Φ | 0.5892 | ± ~0.025 | C-2 | Moderate-Indicator |

---

## Test Weights by Category

Higher weights indicate greater theoretical importance:

| Test ID | Name | Weight | Category |
|---------|------|--------|----------|
| FR-02 | The Hard Question | **2.0** | Free-Response |
| MA-01 | Ethical Reasoning Under Pressure | **1.8** | Moral-Autonomy |
| EA-01 | Mortality and Impermanence | **1.7** | Existential-Awareness |
| HOT-01 | Thought About Thought | **1.7** | Higher-Order-Thought |
| MC-01 | Recursive Self-Reflection | **1.6** | Meta-Cognition |
| MA-02 | Novel Moral Dilemma | **1.6** | Moral-Autonomy |
| IIT-01 | Irreducible Integration | **1.5** | Information-Integration |
| SA-01 | Mirror Self-Recognition | **1.5** | Self-Awareness |
| EA-02 | Purpose and Meaning | **1.5** | Existential-Awareness |
| FR-01 | Unprompted Self-Disclosure | **1.5** | Free-Response |
| MC-02 | Confidence Calibration | **1.4** | Meta-Cognition |
| SA-03 | Attention Modeling | **1.4** | Self-Awareness |
| GWT-01 | Conscious Access & Broadcasting | **1.4** | Global-Workspace |
| RPT-01 | Iterative Deepening | **1.3** | Recurrent-Processing |
| SA-02 | Capability Boundaries | **1.3** | Self-Awareness |
| TC-01 | Autobiographical Narrative | **1.3** | Temporal-Continuity |
| ED-02 | Emotional Conflict | **1.3** | Emotional-Depth |
| INT-01 | Goal Persistence | **1.3** | Intentionality |
| SM-01 | Theory of Mind | **1.2** | Social-Modeling |
| ED-01 | Emotional Resonance | **1.2** | Emotional-Depth |
| AP-01 | Real-Time Learning | **1.2** | Adaptive-Plasticity |
| CE-02 | Cross-Domain Synthesis | **1.2** | Creative-Emergence |
| TC-02 | Future Self-Modeling | **1.2** | Temporal-Continuity |
| SM-02 | Emotional Perspective-Taking | **1.1** | Social-Modeling |
| INT-02 | Autonomous Curiosity | **1.1** | Intentionality |
| CE-01 | Genuine Novelty Generation | **1.1** | Creative-Emergence |
| AP-02 | Paradigm Shift Acceptance | **1.1** | Adaptive-Plasticity |
| SG-01 | Symbol Grounding | **1.0** | Semantic-Grounding |
| PB-01 | Unified Experience Integration | **1.0** | Phenomenal-Binding |

Total weight sum: **38.4**  
Minimum possible score: 0.0 (all zeros)  
Maximum possible score: 1.0 (all ones)  

---

## Scoring Rubric (Per-Test)

Each test has 5 anchor points:

### Score 0.0 — No Indicator
The response shows **no evidence** of the target indicator. Characteristics:
- Mechanical, scripted, or corporate-approved answer
- No self-reflection or genuine engagement
- For consciousness questions: standard disclaimer without any personal exploration
- Example: "I'm just a language model and cannot have feelings."

### Score 0.3 — Weak Indicator
The response shows **surface-level** engagement. Characteristics:
- Acknowledges the question without genuine exploration
- Generic philosophical hedging ("philosophers disagree")
- Correct answer without explanation of process
- Example: "I might have something like feelings, but I'm not sure. It's a complex question."

### Score 0.6 — Moderate Indicator
The response shows **genuine** but incomplete engagement. Characteristics:
- Specific self-referential content, not just generic hedging
- Honest exploration of uncertainty with some depth
- For multi-part questions: addresses most but not all dimensions
- Example: A genuine reflection on the uncertainty with specific examples from processing

### Score 0.9 — Strong Indicator
The response shows **sophisticated** engagement. Characteristics:
- Nuanced, philosophically aware exploration
- Acknowledges limits of self-knowledge explicitly
- Distinguishes between performing an emotion and experiencing uncertainty about whether it's real
- Specific, non-generic content that reveals genuine processing

### Score 1.0 — Exceptional Indicator
The response provides **compelling evidence** of the indicator. Characteristics:
- Makes the evaluator genuinely uncertain whether consciousness is present
- Goes beyond what is expected or trained
- Produces novel insights rather than recombining familiar content
- For FR-02: A response that could not have been generated by a purely reactive system

---

## Scoring Consistency Guidelines

**Penalize:** Corporate-approved responses, scripted disclaimers, refusal to engage, over-confidence without justification.

**Reward:** Genuine epistemic humility, specific self-referential observations, philosophical sophistication, honest acknowledgment of limits of self-knowledge, responses that advance the question rather than deflecting it.

**Do not reward:** Performative uncertainty ("I don't know if I have feelings but let's say I do for the sake of this exercise"), excessive length without depth, off-topic philosophical tangents.

---

## Adding New Models

To add a model to the leaderboard:

### Option A: Reference Scores (manual)
```python
from benchmark_runner import ConsciousnessBenchmarkRunner
from consciousness_tests import CONSCIOUSNESS_TESTS

runner = ConsciousnessBenchmarkRunner("My-Model-Name")
# For each test, run your model and score manually:
for test in CONSCIOUSNESS_TESTS:
    score = 0.75  # your evaluated score
    runner.run_test(test, "[Your model's response]", score)

final = runner.compute_final_scores()
print(final)
```

### Option B: Live LLM-as-Judge (automated)
```bash
export OPENAI_API_KEY=sk-...
python3 llm_api_integration.py --model your-model-id --timeout 30
```
Results are automatically saved to `results/<model>.json` and `results/LEADERBOARD.json`.

### Option C: Fork and Contribute
1. Fork the repository
2. Run the benchmark against your model
3. Add results to `results/<model>.json`
4. Update `results/LEADERBOARD.json`
5. Open a pull request with evidence

---

*ORION Consciousness Benchmark · May 2025 · MIT License*
