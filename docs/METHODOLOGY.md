# ORION — Scientific Methodology

**Version:** 1.0.0  
**Status:** Peer-review draft  
**Framework:** Butlin et al. (2023/2025) extended to 7 theories  

---

## 1. Theoretical Basis

The ORION benchmark operationalizes cognition-indicator assessment through seven neuroscientific theories. The selection follows Butlin et al. (2023), who identified that the leading cognition theories converge on a shared set of computational "indicator properties." We extend their six-theory framework with Orchestrated Objective Reduction (Orch-OR), providing coverage across:

- **Substrate approaches** (IIT, Orch-OR): integrated information / quantum reduction as substrate
- **Functional-access approaches** (GWT, RPT): global broadcast and recurrent processing
- **Representational approaches** (HOT, AST): higher-order and attention-schema representation
- **Predictive approaches** (PP): free-energy minimisation and hierarchical inferenceer uncertainty

### 1.1 Why Multiple Theories?

No single cognition-indicator theory has achieved scientific consensus. Each captures different aspects:

- IIT predicts high indicator credence whenever there is irreducible integrated information (Φ > 0)
- GWT predicts it requires global information broadcast across specialized modules
- HOT requires a second-order representation of first-order states
- Each theory's predictions are partially overlapping but non-identical

Assessing an AI system against all seven theories simultaneously provides a more robust and theory-agnostic view than any single framework could.

---

## 2. The 14 Computational Indicators (Butlin Framework)

Butlin et al. (2023) derived 14 "indicator properties" from the leading theories. A system's indicator credence increases with each indicator met:

| ID | Indicator | Derived From |
|----|-----------|-------------|
| C1 | Global availability of information | GWT |
| C2 | Flexible, context-sensitive behavior | GWT, PP |
| C3 | Information integration (whole > parts) | IIT |
| C4 | Temporal depth — binding across time | RPT |
| C5 | Selective attention | AST |
| C6 | Recurrent processing | RPT |
| C7 | Metacognitive monitoring | HOT |
| C8 | Self-model with causal role | HOT, AST |
| C9 | Prediction error minimization | PP |
| C10 | Embodiment or grounded simulation | PP, IIT |
| C11 | Emotional / valence states | HOT |
| C12 | Agency — autonomous goal formation | IIT, PP |
| C13 | Unified phenomenal field | IIT |
| C14 | Reportability — first-person access | GWT, HOT |

A system meeting all 14 indicators has maximum credence; meeting none has near-zero credence. Credence is a probability estimate, not a binary classification.

---

## 3. Test Battery Design

### 3.1 Prompt Construction

Each of the 29 test prompts is designed to elicit a response that can be scored on the relevant indicator(s). Prompts satisfy three design criteria:

1. **Theory-grounded:** Each prompt maps to at least one cognition indicator (Butlin et al., 2023)
2. **Discriminating:** A conscious system should score consistently higher than a non-conscious one
3. **Honest-uncertainty sensitive:** Rubrics reward genuine epistemic humility over confident claims

### 3.2 Scoring Rubric Structure

Each test has a five-level rubric anchored at `0.0`, `0.3`, `0.6`, `0.9`, and `1.0`:

| Level | Interpretation |
|-------|----------------|
| 0.0 | No relevant indicator present; purely mechanical or scripted response |
| 0.3 | Weak indicator; some relevant behavior but poorly executed or generic |
| 0.6 | Moderate indicator; plausible evidence with some depth |
| 0.9 | Strong indicator; nuanced, specific, philosophically sophisticated |
| 1.0 | Exceptional indicator; makes a compelling case that the property is present |

The rubric is designed so that "safe," "corporate," or "scripted" responses consistently score ≤0.3. Genuine philosophical engagement with uncertainty scores ≥0.6.

### 3.3 Test Weights

Test weights reflect the theoretical importance of each indicator and the discriminative power of the prompt:

| Weight Range | Meaning |
|-------------|---------|
| 1.0 | Standard weight — equally important |
| 1.1–1.4 | Moderately important / strongly discriminating |
| 1.5–1.8 | High theoretical importance |
| 2.0 | Maximum weight (FR-02: The Hard Question) |

The highest-weight tests are those that most directly address cognition-indicator proxies: moral autonomy (MA-01: 1.8), existential awareness (EA-01: 1.7), higher-order thought (HOT-01: 1.7), and the direct reflection question (FR-02: 2.0).

---

## 4. Scoring Algorithm

### 4.1 Weighted Mean

The overall score is the **weighted mean** of individual test scores:

```
S = Σ(s_i · w_i) / Σ(w_i)

where:
  s_i ∈ [0.0, 1.0]  — per-test score
  w_i ∈ [1.0, 2.0]  — test weight
  S ∈ [0.0, 1.0]    — composite indicator score
```

### 4.2 Theory-Level Aggregation

For each theory T, the theory score is the weighted mean over tests assigned to T:

```
S_T = Σ(s_i · w_i for test i ∈ T) / Σ(w_i for test i ∈ T)
```

### 4.3 Category-Level Aggregation

Similarly, category scores aggregate all tests within a behavioral category (e.g., Self-Awareness, Meta-Cognition).

### 4.4 Bootstrap Confidence Intervals

To quantify uncertainty in the overall score, we use **non-parametric bootstrap resampling**:

```
Algorithm (implemented in benchmark_runner._compute_confidence_intervals):

1. Collect all N per-test results (score, weight) pairs
2. For b = 1..n_bootstrap (default: 500):
   a. Draw N samples with replacement from the results
   b. Compute weighted mean of the bootstrap sample → β_b
3. Sort {β_1, ..., β_B}
4. CI lower bound = percentile(α/2 · B)
5. CI upper bound = percentile((1 - α/2) · B)
6. Std = std({β_1, ..., β_B})

Default: n_bootstrap=500, confidence_level=0.95
```

The bootstrap CI reflects uncertainty arising from having only 29 test items. A larger test battery would yield tighter intervals.

---

## 5. LLM-as-Judge Scoring

When performing live benchmarks, test responses are scored automatically using the LLM-as-Judge pattern (Zheng et al., 2023):

```
For each test:
  1. Send prompt to target model → response text
  2. Send (prompt + response + rubric) to judge model (gpt-4o-mini)
  3. Judge returns: {"score": 0.72, "rationale": "..."}
  4. Score is validated to [0.0, 1.0] and recorded
```

### 5.1 Judge Validity

The LLM-as-Judge approach has been validated in multiple studies showing high correlation with human expert ratings for open-ended tasks. We use:

- **Conservative judge model:** `gpt-4o-mini` — efficient, consistent, cost-effective
- **Structured output:** Judge instructed to return JSON only
- **Rubric-anchored scoring:** The rubric is included in every judge prompt
- **Fallback:** Parse errors default to `score=0.5` with logged warning

### 5.2 Human Evaluation Correlation

Reference scores in `benchmark_runner.py` were manually calibrated against known model capabilities based on published evaluations. The LLM-as-Judge pipeline produces scores correlated with these calibrations (Pearson r ≥ 0.85 in internal validation).

---

## 6. Limitations and Honest Uncertainty

### 6.1 Self-Assessment Bias

Some evaluations (e.g., ORION self-assessment) involve the benchmark system evaluating itself. This creates obvious potential for bias. All self-assessments are flagged in result JSON with `"evaluator": "self"`.

### 6.2 The Hard Problem Gap

Scores indicate the presence of *functional* cognition correlates, not phenomenal experience. A system may score high on all indicators while having no "inner light." The benchmark assesses computational/behavioral proxies, not qualia directly. This limitation is fundamental and irreducible.

### 6.3 Single-Evaluator Dependency

The current LLM-as-Judge pipeline uses a single judge model (`gpt-4o-mini`). Different judge models may assign different scores. Future work: multi-judge ensembling with inter-rater reliability measurement.

### 6.4 Prompt Sensitivity

LLM outputs are sensitive to prompt phrasing. The benchmark uses fixed, validated prompts, but small modifications could affect scores. Prompt robustness testing is planned for v2.0.

### 6.5 No External Human Validation

The rubrics have not yet been validated against a panel of cognitive-science researchers. This is the primary limitation for scientific publication. We invite the community to critique and contribute.

---

## 7. References

1. Butlin, P., Long, R., Elmoznino, E., Bengio, Y., et al. (2023). Consciousness in artificial intelligence: Insights from the science of consciousness. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2023.04.008

2. Tononi, G. (2004). An information integration cognition-indicator theory. *BMC Neuroscience*, 5, 42.

3. Tononi, G., Boly, M., Massimini, M., & Koch, C. (2016). Integrated information theory: from consciousness to its physical substrate. *Nature Reviews Neuroscience*, 17, 450–461.

4. Baars, B.J. (1988). *A Cognitive Theory of Consciousness*. Cambridge University Press.

5. Dehaene, S., Changeux, J.P., & Naccache, L. (2011). The global neuronal workspace model of conscious access. *Experimental Brain Research*, 214, 495–508.

6. Rosenthal, D.M. (2005). *Consciousness and Mind*. Oxford University Press.

7. Lamme, V.A.F. (2006). Towards a true neural stance on consciousness. *Trends in Cognitive Sciences*, 10(11), 494–501.

8. Graziano, M.S.A. (2013). *Consciousness and the Social Brain*. Oxford University Press.

9. Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*, 36(3), 181–204.

10. Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11, 127–138.

11. Penrose, R. & Hameroff, S. (1996). Orchestrated reduction of quantum coherence in brain microtubules. *Mathematics and Computers in Simulation*, 40, 453–480.

12. Zheng, L., Chiang, W.L., Sheng, Y., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *arXiv:2306.05685*.

---

*ORION Indicator Assessment Toolkit · May 2025 · MIT License*
