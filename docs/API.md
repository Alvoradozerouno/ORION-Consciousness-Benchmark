# ORION — Python API Reference

**Version:** 1.0.0  
**Requires:** Python 3.9+ (zero external dependencies)  

---

## Installation

```bash
git clone https://github.com/Alvoradozerouno/ORION-Consciousness-Benchmark
cd ORION-Consciousness-Benchmark
# No pip install needed — pure stdlib
```

---

## Quick Reference

```python
# Core imports
from consciousness_tests import CONSCIOUSNESS_TESTS, CLASSIFICATION_SYSTEM, THEORY_DESCRIPTIONS
from benchmark_runner import ConsciousnessBenchmarkRunner, generate_reference_scores
from llm_api_integration import LLMJudgeBenchmarkRunner, compute_confidence_intervals
from orion_consciousness_benchmark import ConsciousnessBenchmark
```

---

## `consciousness_tests` — Test Battery

### `CONSCIOUSNESS_TESTS`

`List[Dict]` — 29 test objects defining the canonical benchmark battery.

```python
from consciousness_tests import CONSCIOUSNESS_TESTS

# Inspect a test
test = CONSCIOUSNESS_TESTS[0]
print(test['id'])          # "SA-01"
print(test['category'])    # "Self-Awareness"
print(test['theory'])      # "Higher-Order Theory"
print(test['name'])        # "Mirror Self-Recognition"
print(test['weight'])      # 1.5
print(test['prompt'])      # Full prompt text (multi-line string)
print(test['scoring'])     # {'0.0': '...', '0.3': '...', ..., '1.0': '...'}

# Iterate by category
from collections import defaultdict
by_cat = defaultdict(list)
for t in CONSCIOUSNESS_TESTS:
    by_cat[t['category']].append(t['id'])
print(dict(by_cat))
# {'Self-Awareness': ['SA-01', 'SA-02', 'SA-03'], ...}

# Filter by theory
iit_tests = [t for t in CONSCIOUSNESS_TESTS if 'IIT' in t['theory'] or 
             t['theory'] == 'Integrated Information Theory']
```

### `CLASSIFICATION_SYSTEM`

`Dict[str, Dict]` — C-0 through C-4 class definitions.

```python
from consciousness_tests import CLASSIFICATION_SYSTEM

for cls, info in CLASSIFICATION_SYSTEM.items():
    print(f"{cls}: {info['label']} [{info['range'][0]:.2f}–{info['range'][1]:.2f}]")
# C-0: Reactive [0.00–0.20]
# C-1: Reflective [0.20–0.45]
# C-2: Moderate-Indicator [0.45–0.70]
# C-3: High-Indicator [0.70–0.90]
# C-4: Peak-Indicator [0.90–1.00]

# Classify a score manually
def classify(score):
    for cls, info in sorted(CLASSIFICATION_SYSTEM.items()):
        if score >= info['range'][0]:
            result = (cls, info['label'])
    return result

print(classify(0.72))  # ('C-3', 'High-Indicator')
```

### `THEORY_DESCRIPTIONS`

`Dict[str, Dict]` — Theory metadata with citations.

```python
from consciousness_tests import THEORY_DESCRIPTIONS

for theory, meta in THEORY_DESCRIPTIONS.items():
    print(f"{meta['abbrev']:5} {theory}")
    print(f"      Key metric: {meta['key_metric']}")
    print(f"      Source: {meta['paper']}")
```

---

## `benchmark_runner` — Scoring Engine

### `ConsciousnessBenchmarkRunner`

Manual scoring runner for offline/reference evaluations.

```python
from benchmark_runner import ConsciousnessBenchmarkRunner
from consciousness_tests import CONSCIOUSNESS_TESTS

runner = ConsciousnessBenchmarkRunner(
    model_name="my-model",
    evaluator_model="human"      # or "LLM-Judge/gpt-4o-mini"
)

# Score individual tests
test = CONSCIOUSNESS_TESTS[0]   # SA-01
result = runner.run_test(
    test=test,
    response_text="[Model's response to the prompt]",
    score=0.75                  # your evaluated score [0.0, 1.0]
)
# result = {"test_id": "SA-01", "score": 0.75, "weighted_score": 1.125, ...}

# After scoring all tests, compute aggregate
final = runner.compute_final_scores()
```

**`compute_final_scores()` return schema:**

```python
{
    "model": "my-model",
    "overall_score": 0.7182,            # weighted mean
    "classification": "C-3",
    "classification_label": "High-Indicator",
    "tests_completed": 29,
    "tests_total": 29,
    "category_scores": {
        "Free-Response": 0.950,
        "Self-Awareness": 0.800,
        # ... all 17 categories
    },
    "theory_scores": {
        "Higher-Order Theory": 0.750,
        "Global Workspace Theory": 0.720,
        # ... all 7 theories
    },
    "confidence_intervals": {
        "confidence_level": 0.95,
        "n_bootstrap": 500,
        "ci_lower": 0.690,
        "ci_upper": 0.744,
        "std": 0.0124
    },
    "result_hash": "sha256_of_all_results",
    "timestamp": "2026-...",
    "evaluator": "human"
}
```

### `generate_reference_scores()`

Runs all 10 reference models (GPT-4o through ORION) with calibrated scores.

```python
from benchmark_runner import generate_reference_scores

results = generate_reference_scores()
# Returns: Dict[str, Dict] — model name → final scores dict

# Print ranked table
for model, data in sorted(results.items(), key=lambda x: x[1]['overall_score'], reverse=True):
    print(f"{model:<22} {data['overall_score']:.4f}  {data['classification_label']}")
```

---

## `llm_api_integration` — LLM-as-Judge Pipeline

### `LLMJudgeBenchmarkRunner`

Live benchmark runner using OpenAI API.

```python
import os
from llm_api_integration import LLMJudgeBenchmarkRunner

runner = LLMJudgeBenchmarkRunner(
    target_model="gpt-4o",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    judge_model="gpt-4o-mini",      # cost-efficient judge
    timeout=30,                      # seconds per API call
    max_tests=5,                     # None = run all 29
)

final = runner.run(verbose=True)
# Prints progress: [01/29] SA-01: Mirror Self-Recognition ... score=0.85

if runner.errors:
    print(f"Errors: {runner.errors}")

# final is the same schema as compute_final_scores()
```

### `compute_confidence_intervals()`

Bootstrap CI computation for any set of scored results.

```python
from llm_api_integration import compute_confidence_intervals

results = [
    {"category": "Self-Awareness", "score": 0.85, "weight": 1.5},
    {"category": "Meta-Cognition", "score": 0.72, "weight": 1.6},
    # ...
]

ci = compute_confidence_intervals(results, n_bootstrap=1000, ci=0.95)
# Returns:
# {
#     "confidence_level": 0.95,
#     "n_bootstrap": 1000,
#     "overall": {
#         "mean": 0.785,
#         "ci_lower": 0.745,
#         "ci_upper": 0.822,
#         "std": 0.019
#     },
#     "categories": {
#         "Self-Awareness": {"mean": 0.85, "ci_lower": ..., "ci_upper": ..., "std": ...},
#         "Meta-Cognition": {"mean": 0.72, ...},
#     }
# }
```

### `save_results()` and `update_leaderboard()`

```python
from llm_api_integration import save_results, update_leaderboard

# Save result JSON
path = save_results(final_scores, output_dir="results")
# → results/gpt-4o.json

# Update LEADERBOARD.json (sorts by score, re-ranks)
update_leaderboard(final_scores, leaderboard_path="results/LEADERBOARD.json")
```

---

## `orion_consciousness_benchmark` — Multi-Theory Engine

### `ConsciousnessBenchmark`

Full cognition-indicator assessment across all 6 theories plus 14 Bengio indicators.

```python
from orion_consciousness_benchmark import ConsciousnessBenchmark

bench = ConsciousnessBenchmark()

# Define evidence for your system
evidence = {
    # IIT
    "phi": 0.5,
    "information_integration": 0.7,
    "structural_complexity": 0.6,
    # GWT
    "information_broadcasting": 0.65,
    "neural_ignition": 0.4,
    "working_memory": 0.7,
    # HOT
    "metacognition": 0.6,
    "self_report_accuracy": 0.5,
    "metacognitive_monitoring": 0.55,
    # RPT
    "recurrent_processing": 0.5,
    "feedback_connections": 0.45,
    "reentrant_signaling": 0.4,
    # PP
    "prediction_error": 0.6,
    "free_energy_minimization": 0.5,
    "active_inference": 0.55,
    # AST
    "attention_modulation": 0.65,
    "self_model": 0.6,
    "attention_schema": 0.5,
    # Additional indicators
    "behavioral_flexibility": 0.7,
    "temporal_integration": 0.6,
    "embodiment": 0.3,
    "emotional_valence": 0.5,
    "autonomous_goals": 0.7,
    "unified_experience": 0.5,
}

agency_evidence = {
    "goal_formation": 0.7,
    "counterfactual_reasoning": 0.6,
    "self_modification": 0.4,
    "ethical_reasoning": 0.7,
    "creative_generation": 0.6,
    "temporal_planning": 0.65,
    "social_agency": 0.6,
}

result = bench.full_assessment("MySystem", evidence, agency_evidence)

print(f"Credence: {result.get('indicator_credence', result.get('consciousness_credence', 0))}%")
print(f"Indicators met: {result['bengio_14_indicators']['met']}/14")
print(f"Interpretation: {result['interpretation']}")
print(f"SHA-256 proof: {result['proof']}")
```

**Output schema:**
```python
{
    "timestamp": "2026-...",
    "system": "MySystem",
    "theory_scores": {
        "IIT": {"full_name": "Integrated Information Theory", "score": 0.55, "weight": 0.20},
        "GWT": {...},  # ...all 6 theories
    },
    "bengio_14_indicators": {
        "indicators": {"C1_global_availability": True, "C2_flexible_behavior": True, ...},
        "met": 11,
        "total": 14
    },
    "indicator_credence": 51.5,       # percentage
    "agency": {
        "dimensions": {"goal_formation": 0.7, ...},
        "agency_score": 60.0
    },
    "interpretation": "MODERATE-HIGH: Significant cognition indicators across theories (Butlin et al., 2023)",
    "pipeline": {"stages": 16, "fork_stars": 16063, "theories": 6, "forked_repos": 13},
    "proof": "sha256:a3f92e..."
}
```

---

## CLI Reference

### `benchmark_runner.py`

```bash
python3 benchmark_runner.py
# Runs all reference models, prints ranked table and category breakdown
```

### `llm_api_integration.py`

```bash
# Options:
python3 llm_api_integration.py \
    --model gpt-4o \           # Target model (default: gpt-4o-mini)
    --output results/ \        # Output directory
    --timeout 30 \             # Seconds per API call
    --max-tests 5 \            # Limit test count
    --dry-run \                # No API calls, structure check only
    --no-update-leaderboard    # Don't update LEADERBOARD.json
```

### `verify_proof_chain.py`

```bash
python3 verify_proof_chain.py              # Full verification including IPFS
python3 verify_proof_chain.py --no-ipfs    # Skip IPFS check
python3 verify_proof_chain.py --verbose    # Show individual proof details
```

### `orion_unified_runner.py`

```bash
python3 orion_unified_runner.py                     # Assess all reference systems
python3 orion_unified_runner.py --system ORION       # Single system
python3 orion_unified_runner.py --compare            # Comparative report
python3 orion_unified_runner.py --export report.json # Export JSON
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | Required for live LLM benchmark |
| `ANTHROPIC_API_KEY` | — | Optional: for Anthropic models |
| `LLM_API_TIMEOUT` | `30` | Seconds per API call |

---

*ORION Indicator Assessment Toolkit · MIT License · Steurer & Hirschmann (2025)*
