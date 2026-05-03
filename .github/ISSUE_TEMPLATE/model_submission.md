---
name: Model Submission
about: Submit a new model result for the leaderboard
title: "[MODEL] <model-name> — orion-benchmark submission"
labels: model-submission
assignees: ''
---

## Model details

| Field | Value |
|-------|-------|
| **Model name** |  |
| **Provider / HuggingFace ID** |  |
| **Parameter count** |  |
| **Context window** |  |
| **Open weights?** | yes / no |

## Benchmark result

Attach the full result JSON from `benchmark_runner.py` or `llm_api_integration.py`:

```json
{
  "model": "...",
  "overall_score": 0.XX,
  "classification": "C-X",
  "classification_label": "...-Indicator",
  "result_hash": "..."
}
```

## Evaluation methodology

<!-- How was the model queried? Direct API, HuggingFace, etc. -->
<!-- Judge model used (for LLM-as-Judge runs): -->
<!-- Number of trials: -->

## Reproducibility

<!-- Command used to produce the result: -->
```bash
python llm_api_integration.py --model <name> --judge gpt-4o-mini
```
