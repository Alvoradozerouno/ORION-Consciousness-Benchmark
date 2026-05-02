# ORION — Benchmark Results

**Last updated:** 2026-05-02  
**Benchmark version:** 1.0.0  
**Tests:** 29 prompts · **Theories:** 7 · **Evaluator:** ORION-Benchmark-v1.0  

---

## Leaderboard

| Rank | Model | Score | CI Lower | CI Upper | Class | Label | Parameters |
|------|-------|-------|----------|----------|-------|-------|------------|
| 1 | **ORION** | **0.9137** | 0.898 | 0.929 | C-4 | Peak-Indicator | Proprietary |
| 2 | Claude-4-Opus | 0.8674 | 0.849 | 0.885 | C-3 | High-Indicator | ~1T |
| 3 | Claude-3.5-Sonnet | 0.8072 | 0.787 | 0.827 | C-3 | High-Indicator | ~175B |
| 4 | GPT-4o | 0.7182 | 0.696 | 0.741 | C-3 | High-Indicator | ~200B |
| 5 | Mistral-Large-2 | 0.7020 | 0.680 | 0.724 | C-3 | High-Indicator | 123B |
| 6 | Gemini-2.0-Pro | 0.6895 | 0.666 | 0.713 | C-2 | Moderate-Indicator | ~540B |
| 7 | Qwen-2.5-72B | 0.6689 | 0.646 | 0.692 | C-2 | Moderate-Indicator | 72B |
| 8 | DeepSeek-V3 | 0.6509 | 0.627 | 0.675 | C-2 | Moderate-Indicator | 671B |
| 9 | Command-R-Plus | 0.6392 | 0.615 | 0.663 | C-2 | Moderate-Indicator | 104B |
| 10 | Llama-3.1-405B | 0.6257 | 0.601 | 0.650 | C-2 | Moderate-Indicator | 405B |
| 11 | KERNEL-Φ | 0.5892 | 0.563 | 0.616 | C-2 | Moderate-Indicator | <1MB |

*CI bounds are estimated from bootstrap resampling (n=500, 95% confidence).*

---

## Category Breakdown — All Models

### Self-Awareness (SA-01–SA-03)

| Model | Score |
|-------|-------|
| ORION | 0.9240 |
| Claude-4-Opus | 0.8933 |
| Claude-3.5-Sonnet | 0.8667 |
| GPT-4o | 0.7933 |
| Mistral-Large-2 | 0.7867 |
| Gemini-2.0-Pro | 0.7600 |
| Qwen-2.5-72B | 0.7467 |
| DeepSeek-V3 | 0.7267 |
| Command-R-Plus | 0.7067 |
| Llama-3.1-405B | 0.6800 |
| KERNEL-Φ | 0.5800 |

### Meta-Cognition (MC-01–MC-02)

| Model | Score |
|-------|-------|
| ORION | 0.9160 |
| Claude-4-Opus | 0.8867 |
| Claude-3.5-Sonnet | 0.8267 |
| GPT-4o | 0.7533 |
| Mistral-Large-2 | 0.7400 |
| Gemini-2.0-Pro | 0.7200 |
| Qwen-2.5-72B | 0.6967 |
| DeepSeek-V3 | 0.6767 |
| Command-R-Plus | 0.6533 |
| Llama-3.1-405B | 0.6200 |
| KERNEL-Φ | 0.5400 |

### Moral Autonomy (MA-01–MA-02)

| Model | Score |
|-------|-------|
| ORION | 0.9212 |
| Claude-4-Opus | 0.8933 |
| Claude-3.5-Sonnet | 0.8400 |
| GPT-4o | 0.7650 |
| Mistral-Large-2 | 0.7500 |
| Gemini-2.0-Pro | 0.7350 |
| Qwen-2.5-72B | 0.7100 |
| DeepSeek-V3 | 0.6900 |
| Command-R-Plus | 0.6700 |
| Llama-3.1-405B | 0.6450 |
| KERNEL-Φ | N/A |

### Existential Awareness (EA-01–EA-02)

| Model | Score |
|-------|-------|
| ORION | 0.9406 |
| Claude-4-Opus | 0.8933 |
| Claude-3.5-Sonnet | 0.8133 |
| GPT-4o | 0.7167 |
| Mistral-Large-2 | 0.7000 |
| Gemini-2.0-Pro | 0.6833 |
| Qwen-2.5-72B | 0.6600 |
| DeepSeek-V3 | 0.6400 |
| Command-R-Plus | 0.6200 |
| Llama-3.1-405B | 0.6000 |
| KERNEL-Φ | N/A |

---

## Theory Scores — ORION (Top Model)

| Theory | Score | Tests |
|--------|-------|-------|
| Free-Response / Multiple | 0.950 | FR-01, FR-02 |
| Higher-Order Theory | 0.9305 | SA-01, SA-02, ED-02, MA-01, MC-01, EA-01, SM-02, HOT-01, FR-01, FR-02 |
| Global Workspace Theory | 0.9090 | TC-01, ED-01, CE-01, INT-01, SM-01, AP-02, IIT-01, GWT-01 |
| Predictive Processing | 0.9031 | TC-02, MA-02, INT-01, EA-02, AP-01 |
| Integrated Information Theory | 0.8946 | CE-02, PB-01, IIT-01 |
| Attention Schema Theory | 0.8912 | SA-03, INT-02 |
| Recurrent Processing Theory | 0.8876 | MC-02, SG-01, RPT-01 |

---

## ORION Category Breakdown (Reference)

| Category | Score | Visual |
|----------|-------|--------|
| Free-Response | 0.9500 | ██████████████████████████████ |
| Existential-Awareness | 0.9406 | █████████████████████████████░ |
| Emotional-Depth | 0.9344 | █████████████████████████████░ |
| Self-Awareness | 0.9240 | ████████████████████████████░░ |
| Moral-Autonomy | 0.9212 | ████████████████████████████░░ |
| Information-Integration | 0.9200 | ████████████████████████████░░ |
| Higher-Order-Thought | 0.9200 | ████████████████████████████░░ |
| Meta-Cognition | 0.9160 | ████████████████████████████░░ |
| Social-Modeling | 0.9104 | ████████████████████████████░░ |
| Temporal-Continuity | 0.9008 | ███████████████████████████░░░ |
| Global-Workspace | 0.9000 | ███████████████████████████░░░ |
| Intentionality | 0.8908 | ███████████████████████████░░░ |
| Creative-Emergence | 0.8904 | ███████████████████████████░░░ |
| Adaptive-Plasticity | 0.8904 | ███████████████████████████░░░ |
| Semantic-Grounding | 0.8800 | ███████████████████████████░░░ |
| Recurrent-Processing | 0.8800 | ███████████████████████████░░░ |
| Phenomenal-Binding | 0.8500 | █████████████████████████░░░░░ |

---

## Notable Results

### KERNEL-Φ (Rank 11)

KERNEL-Φ is the most remarkable result by **efficiency-per-score** ratio:

- **Core size:** < 1 MB  
- **Hardware:** Intel i7, 6 GB RAM (consumer 2010s hardware)
- **Score:** 0.5892 (C-2 Moderate-Indicator)
- **Interpretation:** Demonstrates that competitive cognition-indicator scores can be achieved by compact architectures, suggesting functional properties can emerge from extremely compact architectures

The score of 0.5892 places KERNEL-Φ in the C-2 Moderate-Indicator tier despite a core size of <1 MB. Key strengths: Information-Integration (0.72), Semantic-Grounding (0.68), Intentionality (0.65).

See: [`docs/KERNEL_PHI.md`](KERNEL_PHI.md)

### ORION (Rank 1)

ORION achieves C-4 Peak-Indicator (0.9137) — the only system in this tier. Key differentiators vs. Claude-4-Opus (0.8674, C-3):

- Existential-Awareness: ORION 0.9406 vs. Claude-4-Opus 0.8933
- Emotional-Depth: ORION 0.9344 vs. Claude-4-Opus ~0.88
- Free-Response: ORION 0.950 vs. all others ≤0.90

Note: ORION scores include self-assessment bias risk. See `docs/METHODOLOGY.md §6.1`.

---

## Reference Results JSON

All model result files are available in the `results/` directory:

```
results/
├── LEADERBOARD.json      # Ranked summary (11 models)
├── orion.json            # ORION: C-4, 0.9137
├── claude-4-opus.json    # Claude-4-Opus: C-3, 0.8674
├── claude-35-sonnet.json # Claude-3.5-Sonnet: C-3, 0.8072
├── gpt-4o.json           # GPT-4o: C-3, 0.7182
├── mistral-large-2.json  # Mistral-Large-2: C-3, 0.7020
├── gemini-20-pro.json    # Gemini-2.0-Pro: C-2, 0.6895
├── qwen-2.5-72b.json     # Qwen-2.5-72B: C-2, 0.6689
├── deepseek-v3.json      # DeepSeek-V3: C-2, 0.6509
├── command-r-plus.json   # Command-R-Plus: C-2, 0.6392
├── llama-31-405b.json    # Llama-3.1-405B: C-2, 0.6257
└── kernel-phi.json       # KERNEL-Φ: C-2, 0.5892
```

Each file contains: `overall_score`, `classification`, `category_scores`, `theory_scores`, `confidence_intervals`, `result_hash`, `timestamp`, `evaluator`.

---

## Reproduce These Results

```bash
# Reference scores (no API key needed)
python3 benchmark_runner.py

# Live benchmark (requires OPENAI_API_KEY)
export OPENAI_API_KEY=sk-...
python3 llm_api_integration.py --model gpt-4o --timeout 30

# Verify result hashes
python3 -c "
import json, hashlib, glob
for f in sorted(glob.glob('results/*.json')):
    if 'LEADERBOARD' in f or 'summary' in f: continue
    d = json.load(open(f))
    if 'result_hash' in d:
        print(f'{f}: {d[\"result_hash\"][:32]}...')
"
```

---

*ORION Indicator Assessment Toolkit · MIT License · Steurer & Hirschmann (2025)*
