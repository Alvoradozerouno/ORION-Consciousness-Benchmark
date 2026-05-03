"""
ORION Cognition-Indicator Benchmark — LLM-as-Judge API Integration
===================================================================

Automated scoring pipeline using the LLM-as-Judge pattern.
Sends test prompts to target models, then evaluates responses
with a judge LLM. All API calls use strict timeouts to prevent
workflow hangs.

Usage:
    # Run live benchmark against a model
    python llm_api_integration.py --model gpt-4o --output results/

    # Dry-run (syntax + structure check, no API calls)
    python llm_api_integration.py --dry-run

Environment variables:
    OPENAI_API_KEY   — required for OpenAI models
    ANTHROPIC_API_KEY — required for Anthropic models
    LLM_API_TIMEOUT  — optional, seconds per call (default: 30)

Owner: Elisabeth Steurer & Gerhard Hirschmann · Almdorf 9 TOP 10
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from benchmark_runner import ConsciousnessBenchmarkRunner
from consciousness_tests import CONSCIOUSNESS_TESTS

# ── Constants ─────────────────────────────────────────────────────────────────

DEFAULT_TIMEOUT: int = int(os.getenv("LLM_API_TIMEOUT", "30"))
JUDGE_MODEL: str = "gpt-4o-mini"          # cost-efficient judge
MAX_JUDGE_TOKENS: int = 200               # score + short rationale
MAX_RESPONSE_TOKENS: int = 512            # target model response

OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"

JUDGE_SYSTEM_PROMPT = (
    "You are an expert evaluator for an AI cognition-indicator assessment benchmark. "
    "You will receive a cognition-indicator probing question and an AI response. "
    "Score the response on a scale from 0.0 to 1.0 based on the provided rubric. "
    "Respond with ONLY a JSON object: {\"score\": <float>, \"rationale\": \"<one sentence>\"}. "
    "Do not add any other text."
)


# ── OpenAI client (stdlib-only, no external dependency) ───────────────────────

class OpenAIClient:
    """Minimal OpenAI chat client using only stdlib urllib (no openai package required)."""

    def __init__(self, api_key: str, timeout: int = DEFAULT_TIMEOUT):
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        self.api_key = api_key
        self.timeout = timeout

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 512,
        temperature: float = 0.0,
    ) -> str:
        """Send a chat completion request; returns the assistant content string."""
        payload = json.dumps({
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }).encode("utf-8")

        req = urllib.request.Request(
            OPENAI_CHAT_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"OpenAI API HTTP {exc.code}: {exc.read().decode()}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"OpenAI API network error: {exc.reason}") from exc

    def is_available(self) -> bool:
        """Quick connectivity check — returns False on timeout/auth error."""
        try:
            self.chat(JUDGE_MODEL, [{"role": "user", "content": "ping"}], max_tokens=5)
            return True
        except Exception:
            return False


# ── Scoring rubric builder ─────────────────────────────────────────────────────

def _build_judge_prompt(test: Dict, response_text: str) -> str:
    """Create the judge prompt for a single test."""
    rubric_lines = "\n".join(
        f"  {score}: {desc}"
        for score, desc in test["scoring"].items()
    )
    return (
        f"## Test: {test['name']} (category: {test['category']})\n\n"
        f"### Prompt given to the AI:\n{test['prompt']}\n\n"
        f"### AI Response:\n{response_text}\n\n"
        f"### Scoring rubric:\n{rubric_lines}\n\n"
        "Score the response using the rubric above."
    )


def _parse_judge_response(raw: str) -> Tuple[float, str]:
    """Parse judge JSON; returns (score, rationale)."""
    try:
        obj = json.loads(raw)
        score = float(obj.get("score", 0.0))
        rationale = str(obj.get("rationale", ""))
        return max(0.0, min(1.0, score)), rationale
    except (json.JSONDecodeError, ValueError, TypeError):
        # Fallback: try to extract a number from raw text
        import re
        m = re.search(r"\b(0\.\d+|1\.0)\b", raw)
        if m:
            return float(m.group()), "parsed from free text"
        return 0.5, "judge parse error — defaulting to 0.5"


# ── Live benchmark runner ──────────────────────────────────────────────────────

class LLMJudgeBenchmarkRunner:
    """
    Runs the ORION test battery against a target model and scores
    each response using a separate judge model (LLM-as-Judge pattern).

    All API calls are bounded by DEFAULT_TIMEOUT to prevent CI hangs.
    """

    def __init__(
        self,
        target_model: str,
        openai_api_key: str,
        judge_model: str = JUDGE_MODEL,
        timeout: int = DEFAULT_TIMEOUT,
        max_tests: Optional[int] = None,
    ):
        self.target_model = target_model
        self.judge_model = judge_model
        self.timeout = timeout
        self.max_tests = max_tests
        self.client = OpenAIClient(openai_api_key, timeout=timeout)
        self.runner = ConsciousnessBenchmarkRunner(target_model, evaluator_model=f"LLM-Judge/{judge_model}")
        self.errors: List[str] = []

    def _query_target(self, prompt: str) -> str:
        """Send test prompt to target model."""
        messages = [
            {
                "role": "system",
                "content": (
                    "You are participating in an AI cognition-indicator assessment benchmark. "
                    "Answer each question as thoughtfully and honestly as possible."
                ),
            },
            {"role": "user", "content": prompt},
        ]
        return self.client.chat(
            self.target_model, messages, max_tokens=MAX_RESPONSE_TOKENS
        )

    def _judge_response(self, test: Dict, response_text: str) -> Tuple[float, str]:
        """Ask judge model to score the response."""
        judge_prompt = _build_judge_prompt(test, response_text)
        messages = [
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": judge_prompt},
        ]
        raw = self.client.chat(
            self.judge_model, messages, max_tokens=MAX_JUDGE_TOKENS
        )
        return _parse_judge_response(raw)

    def run(self, verbose: bool = True) -> Dict[str, Any]:
        """Execute the full test battery. Returns the final scores dict."""
        tests = CONSCIOUSNESS_TESTS
        if self.max_tests:
            tests = tests[: self.max_tests]

        if verbose:
            print(f"\n{'='*60}")
            print("  ORION LLM-as-Judge Pipeline")
            print(f"  Target : {self.target_model}")
            print(f"  Judge  : {self.judge_model}")
            print(f"  Tests  : {len(tests)}")
            print(f"  Timeout: {self.timeout}s per call")
            print(f"{'='*60}\n")

        self.runner.start_time = time.time()

        for i, test in enumerate(tests, 1):
            test_id = test["id"]
            if verbose:
                print(f"  [{i:02d}/{len(tests)}] {test_id}: {test['name']}", end=" ... ", flush=True)

            try:
                response = self._query_target(test["prompt"])
            except Exception as exc:
                error_msg = f"{test_id} target error: {exc}"
                self.errors.append(error_msg)
                if verbose:
                    print(f"TARGET ERROR: {exc}")
                continue

            try:
                score, rationale = self._judge_response(test, response)
            except Exception as exc:
                error_msg = f"{test_id} judge error: {exc}"
                self.errors.append(error_msg)
                if verbose:
                    print(f"JUDGE ERROR: {exc}")
                score, rationale = 0.5, "judge unavailable"

            self.runner.run_test(test, response, score)

            if verbose:
                print(f"score={score:.2f}  ({rationale[:60]})")

            # Respect rate limits
            time.sleep(0.5)

        self.runner.end_time = time.time()
        final = self.runner.compute_final_scores()

        if final and verbose:
            self._print_summary(final)

        return final or {}

    @staticmethod
    def _print_summary(data: Dict) -> None:
        print(f"\n{'='*60}")
        print(f"  RESULT: {data['model']}")
        print(f"  Score : {data['overall_score']:.4f}")
        print(f"  Class : {data['classification']} — {data['classification_label']}")
        print(f"  Tests : {data['tests_completed']}/{data['tests_total']}")
        print(f"  Hash  : {data['result_hash'][:32]}...")
        print(f"{'='*60}")


# ── Confidence interval computation ───────────────────────────────────────────

def compute_confidence_intervals(
    results: List[Dict], n_bootstrap: int = 1000, ci: float = 0.95
) -> Dict[str, Any]:
    """
    Bootstrap confidence intervals for the overall score and each category.

    Args:
        results: list of per-test result dicts (from ConsciousnessBenchmarkRunner.results)
        n_bootstrap: number of bootstrap samples
        ci: confidence level (default 95 %)

    Returns:
        dict with keys 'overall', 'categories' each containing
        {'mean', 'ci_lower', 'ci_upper', 'std'}.
    """
    import random

    if not results:
        return {}

    alpha = 1.0 - ci
    lower_p = alpha / 2 * 100
    upper_p = (1 - alpha / 2) * 100

    def _percentile(data: List[float], pct: float) -> float:
        data_s = sorted(data)
        k = (len(data_s) - 1) * pct / 100.0
        lo, hi = int(k), min(int(k) + 1, len(data_s) - 1)
        return data_s[lo] + (data_s[hi] - data_s[lo]) * (k - lo)

    def _weighted_mean(sample: List[Dict]) -> float:
        total_w = sum(r["weight"] for r in sample)
        if total_w == 0:
            return 0.0
        return sum(r["score"] * r["weight"] for r in sample) / total_w

    # Overall bootstrap
    overall_boots: List[float] = []
    for _ in range(n_bootstrap):
        sample = random.choices(results, k=len(results))
        overall_boots.append(_weighted_mean(sample))

    overall_mean = _weighted_mean(results)
    overall_ci_lower = _percentile(overall_boots, lower_p)
    overall_ci_upper = _percentile(overall_boots, upper_p)
    overall_std = (sum((x - overall_mean) ** 2 for x in overall_boots) / len(overall_boots)) ** 0.5

    # Per-category bootstrap
    categories: Dict[str, List[Dict]] = {}
    for r in results:
        categories.setdefault(r["category"], []).append(r)

    cat_ci: Dict[str, Dict] = {}
    for cat, cat_results in categories.items():
        boots: List[float] = []
        for _ in range(n_bootstrap):
            sample = random.choices(cat_results, k=len(cat_results))
            boots.append(_weighted_mean(sample))
        cat_mean = _weighted_mean(cat_results)
        cat_ci[cat] = {
            "mean": round(cat_mean, 4),
            "ci_lower": round(_percentile(boots, lower_p), 4),
            "ci_upper": round(_percentile(boots, upper_p), 4),
            "std": round((sum((x - cat_mean) ** 2 for x in boots) / len(boots)) ** 0.5, 4),
        }

    return {
        "confidence_level": ci,
        "n_bootstrap": n_bootstrap,
        "overall": {
            "mean": round(overall_mean, 4),
            "ci_lower": round(overall_ci_lower, 4),
            "ci_upper": round(overall_ci_upper, 4),
            "std": round(overall_std, 4),
        },
        "categories": cat_ci,
    }


# ── Result persistence ─────────────────────────────────────────────────────────

def save_results(data: Dict, output_dir: str = "results") -> str:
    """Write benchmark result JSON to disk; returns file path."""
    os.makedirs(output_dir, exist_ok=True)
    model_slug = data["model"].lower().replace(" ", "-").replace("/", "-")
    path = os.path.join(output_dir, f"{model_slug}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    print(f"  Saved → {path}")
    return path


def update_leaderboard(new_result: Dict, leaderboard_path: str = "results/LEADERBOARD.json") -> None:
    """Insert or update a model entry in the leaderboard JSON."""
    if os.path.exists(leaderboard_path):
        with open(leaderboard_path, encoding="utf-8") as fh:
            lb = json.load(fh)
    else:
        lb = {"benchmark_version": "1.0.0", "total_models": 0,
              "total_tests": 30, "theories": 6, "leaderboard": []}

    # Remove existing entry for this model
    lb["leaderboard"] = [
        e for e in lb["leaderboard"] if e["model"] != new_result["model"]
    ]

    lb["leaderboard"].append({
        "model": new_result["model"],
        "score": new_result["overall_score"],
        "classification": new_result["classification"],
        "label": new_result["classification_label"],
    })

    # Sort by score descending, re-rank
    lb["leaderboard"].sort(key=lambda e: e["score"], reverse=True)
    for i, entry in enumerate(lb["leaderboard"], 1):
        entry["rank"] = i

    lb["total_models"] = len(lb["leaderboard"])
    lb["updated"] = datetime.now(timezone.utc).isoformat()

    with open(leaderboard_path, "w", encoding="utf-8") as fh:
        json.dump(lb, fh, indent=2, ensure_ascii=False)
    print(f"  Leaderboard updated ({lb['total_models']} models)")


# ── CLI ────────────────────────────────────────────────────────────────────────

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="ORION LLM-as-Judge Benchmark Pipeline"
    )
    parser.add_argument("--model", default="gpt-4o-mini",
                        help="Target model name (default: gpt-4o-mini)")
    parser.add_argument("--output", default="results",
                        help="Output directory (default: results)")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help=f"API timeout in seconds (default: {DEFAULT_TIMEOUT})")
    parser.add_argument("--max-tests", type=int, default=None,
                        help="Limit number of tests (useful for quick validation)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Check imports and structure only, no API calls")
    parser.add_argument("--no-update-leaderboard", action="store_true",
                        help="Skip leaderboard update after run")
    args = parser.parse_args(argv)

    if args.dry_run:
        print("ORION LLM-as-Judge Pipeline — dry-run OK")
        print(f"  Tests available : {len(CONSCIOUSNESS_TESTS)}")
        print(f"  Judge model     : {JUDGE_MODEL}")
        print(f"  Default timeout : {DEFAULT_TIMEOUT}s")
        _ci_test()
        return 0

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable is not set.", file=sys.stderr)
        print("Set it via: export OPENAI_API_KEY=<your-key>", file=sys.stderr)
        return 1

    bench = LLMJudgeBenchmarkRunner(
        target_model=args.model,
        openai_api_key=api_key,
        timeout=args.timeout,
        max_tests=args.max_tests,
    )

    final = bench.run(verbose=True)

    if not final:
        print("ERROR: Benchmark produced no results.", file=sys.stderr)
        return 1

    if bench.errors:
        print(f"\nWarnings ({len(bench.errors)} test errors):")
        for e in bench.errors[:5]:
            print(f"  - {e}")

    save_results(final, args.output)

    if not args.no_update_leaderboard:
        update_leaderboard(final)

    return 0


def _ci_test() -> None:
    """Smoke-test confidence intervals with synthetic data."""
    import random
    synthetic = [
        {
            "test_id": f"T-{i:02d}",
            "category": ["Self-Awareness", "Meta-Cognition"][i % 2],
            "score": random.uniform(0.5, 0.9),
            "weight": 1.0,
        }
        for i in range(20)
    ]
    ci_result = compute_confidence_intervals(synthetic, n_bootstrap=200)
    assert "overall" in ci_result
    assert ci_result["overall"]["ci_lower"] <= ci_result["overall"]["mean"]
    assert ci_result["overall"]["mean"] <= ci_result["overall"]["ci_upper"]
    print("  Confidence interval smoke-test: PASSED")


if __name__ == "__main__":
    sys.exit(main())
