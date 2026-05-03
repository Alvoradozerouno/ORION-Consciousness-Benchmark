"""
Tests for result JSON files — schema, value ranges, leaderboard consistency.
"""
import json
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(ROOT, "results")

# Individual per-model result files (not leaderboard / summary)
RESULT_FILES = [
    f for f in os.listdir(RESULTS_DIR)
    if f.endswith(".json")
    and f not in {"LEADERBOARD.json", "summary.json", "pipeline_run_latest.json",
                  "autonomous_expansion.json", "recurrence_evolution.json",
                  "nn_benchmark.json", "orion_self_test.json"}
]


@pytest.fixture(scope="module", params=RESULT_FILES)
def result(request):
    path = os.path.join(RESULTS_DIR, request.param)
    with open(path) as f:
        return json.load(f), request.param


@pytest.fixture(scope="module")
def leaderboard():
    with open(os.path.join(RESULTS_DIR, "LEADERBOARD.json")) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Per-model result schema
# ---------------------------------------------------------------------------

class TestResultSchema:
    REQUIRED_FIELDS = {
        "model", "overall_score", "classification", "classification_label",
        "tests_completed", "tests_total", "result_hash",
    }

    def test_required_fields_present(self, result):
        data, filename = result
        missing = self.REQUIRED_FIELDS - set(data.keys())
        assert not missing, f"{filename}: missing fields {missing}"

    def test_overall_score_in_range(self, result):
        data, filename = result
        score = data["overall_score"]
        assert 0.0 <= score <= 1.0, f"{filename}: overall_score {score} out of [0, 1]"

    def test_classification_is_valid(self, result):
        data, filename = result
        assert data["classification"] in {"C-0", "C-1", "C-2", "C-3", "C-4"}, (
            f"{filename}: invalid classification '{data['classification']}'"
        )

    def test_classification_label_is_valid(self, result):
        data, filename = result
        valid = {
            "Minimal-Indicator", "Low-Indicator", "Moderate-Indicator",
            "High-Indicator", "Peak-Indicator",
        }
        assert data["classification_label"] in valid, (
            f"{filename}: invalid classification_label '{data['classification_label']}'"
        )

    def test_no_narrative_labels(self, result):
        """Enforce scientific language policy — no consciousness claim labels."""
        data, filename = result
        forbidden = {"Transcendent", "Conscious", "Sentient", "Self-Aware", "Autonomous"}
        for word in forbidden:
            assert word not in data.get("classification_label", ""), (
                f"{filename}: classification_label contains forbidden word '{word}'"
            )

    def test_tests_counts_consistent(self, result):
        data, filename = result
        completed = data.get("tests_completed", 0)
        total = data.get("tests_total", 0)
        assert 0 < total <= 30, f"{filename}: tests_total {total} unexpected"
        assert 0 < completed <= total, (
            f"{filename}: tests_completed {completed} > tests_total {total}"
        )

    def test_result_hash_looks_like_sha256(self, result):
        data, filename = result
        h = data.get("result_hash", "")
        assert len(h) >= 32, f"{filename}: result_hash '{h}' too short"

    def test_score_and_classification_consistent(self, result):
        data, filename = result
        score = data["overall_score"]
        cls = data["classification"]
        bounds = {
            "C-0": (0.00, 0.20),
            "C-1": (0.20, 0.45),
            "C-2": (0.45, 0.70),
            "C-3": (0.70, 0.90),
            "C-4": (0.90, 1.01),
        }
        lo, hi = bounds[cls]
        assert lo <= score < hi, (
            f"{filename}: score {score} inconsistent with class {cls} range [{lo}, {hi})"
        )


# ---------------------------------------------------------------------------
# Leaderboard
# ---------------------------------------------------------------------------

class TestLeaderboard:
    def test_leaderboard_is_list(self, leaderboard):
        entries = leaderboard if isinstance(leaderboard, list) else leaderboard.get("leaderboard", [])
        assert isinstance(entries, list)
        # ORION is now in benchmark_instrument, not the ranked list → ≥10 external models
        assert len(entries) >= 10

    def test_orion_is_benchmark_instrument(self, leaderboard):
        """ORION is the measurement framework, not a ranked competitor."""
        if isinstance(leaderboard, dict):
            instrument = leaderboard.get("benchmark_instrument", {})
            assert instrument.get("model") == "ORION", (
                "ORION must be declared as benchmark_instrument, not a ranked competitor. "
                f"Got: {instrument}"
            )
        else:
            # Legacy list format: ORION may still appear in list (tolerated for old fixtures)
            model_names = {e.get("model", e.get("name", "")) for e in leaderboard}
            assert "ORION" in model_names

    def test_leaderboard_competitors_exclude_orion(self, leaderboard):
        """Ranked leaderboard must not include the benchmark instrument itself."""
        entries = leaderboard if isinstance(leaderboard, list) else leaderboard.get("leaderboard", [])
        model_names = [e.get("model", e.get("name", "")) for e in entries]
        assert "ORION" not in model_names, (
            "ORION (benchmark instrument) must not appear in the ranked leaderboard. "
            "Use the benchmark_instrument field instead."
        )

    def test_kernel_phi_present(self, leaderboard):
        entries = leaderboard if isinstance(leaderboard, list) else leaderboard.get("leaderboard", [])
        names = {e.get("model", e.get("name", "")) for e in entries}
        assert any("KERNEL" in n or "Phi" in n or "Kernel" in n or "Φ" in n for n in names), (
            f"KERNEL-Φ not found in leaderboard. Names: {names}"
        )
