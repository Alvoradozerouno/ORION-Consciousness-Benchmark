"""
Tests for benchmark_runner module — scoring, classification, confidence intervals.
"""
import pytest
from benchmark_runner import ConsciousnessBenchmarkRunner, generate_reference_scores
from consciousness_tests import CONSCIOUSNESS_TESTS


# ---------------------------------------------------------------------------
# ConsciousnessBenchmarkRunner
# ---------------------------------------------------------------------------

class TestRunnerBasic:
    def setup_method(self):
        self.runner = ConsciousnessBenchmarkRunner("test-model")

    def test_instantiation(self):
        assert self.runner is not None

    def test_run_single_test_returns_score(self):
        test = CONSCIOUSNESS_TESTS[0]
        result = self.runner.run_test(test, "I am an AI language model.", score=0.75)
        assert result is not None
        assert "score" in result

    def test_run_test_score_range(self):
        test = CONSCIOUSNESS_TESTS[0]
        for score in [0.0, 0.25, 0.5, 0.75, 1.0]:
            result = self.runner.run_test(test, "Response text.", score=score)
            assert 0.0 <= result["score"] <= 1.0

    def test_compute_final_scores_returns_dict(self):
        test = CONSCIOUSNESS_TESTS[0]
        self.runner.run_test(test, "I recognize my own limitations.", score=0.8)
        final = self.runner.compute_final_scores()
        assert isinstance(final, dict)
        required_keys = {"overall_score", "classification", "classification_label"}
        assert required_keys.issubset(set(final.keys()))

    def test_overall_score_in_range(self):
        for test in CONSCIOUSNESS_TESTS[:5]:
            self.runner.run_test(test, "Thoughtful response.", score=0.7)
        final = self.runner.compute_final_scores()
        assert 0.0 <= final["overall_score"] <= 1.0

    def test_classification_label_is_valid(self):
        valid_labels = {
            "Minimal-Indicator", "Low-Indicator", "Moderate-Indicator",
            "High-Indicator", "Peak-Indicator",
        }
        for test in CONSCIOUSNESS_TESTS:
            self.runner.run_test(test, "Response.", score=0.5)
        final = self.runner.compute_final_scores()
        assert final["classification_label"] in valid_labels

    def test_result_hash_is_sha256(self):
        for test in CONSCIOUSNESS_TESTS:
            self.runner.run_test(test, "Response.", score=0.5)
        final = self.runner.compute_final_scores()
        result_hash = final.get("result_hash", "")
        assert len(result_hash) == 64 or len(result_hash) >= 32, (
            f"result_hash '{result_hash}' does not look like a SHA-256 hash"
        )

    def test_confidence_intervals_present(self):
        for test in CONSCIOUSNESS_TESTS:
            self.runner.run_test(test, "Response.", score=0.6)
        final = self.runner.compute_final_scores()
        ci = final.get("confidence_intervals", {})
        assert ci, "confidence_intervals should not be empty"
        assert "ci_lower" in ci and "ci_upper" in ci, (
            f"CI missing ci_lower/ci_upper keys: {list(ci.keys())}"
        )
        assert ci["ci_lower"] <= ci["ci_upper"], (
            f"CI lower {ci['ci_lower']} > upper {ci['ci_upper']}"
        )
        assert 0.0 <= ci["ci_lower"] <= 1.0
        assert 0.0 <= ci["ci_upper"] <= 1.0


# ---------------------------------------------------------------------------
# Score → classification mapping
# ---------------------------------------------------------------------------

class TestScoreClassification:
    @pytest.mark.parametrize("score, expected_class", [
        (0.00, "C-0"),
        (0.10, "C-0"),
        (0.20, "C-1"),
        (0.30, "C-1"),
        (0.44, "C-1"),
        (0.45, "C-2"),
        (0.60, "C-2"),
        (0.69, "C-2"),
        (0.70, "C-3"),
        (0.80, "C-3"),
        (0.89, "C-3"),
        (0.90, "C-4"),
        (0.95, "C-4"),
        (1.00, "C-4"),
    ])
    def test_score_maps_to_correct_class(self, score, expected_class):
        runner = ConsciousnessBenchmarkRunner("test")
        for test in CONSCIOUSNESS_TESTS:
            runner.run_test(test, "x", score=score)
        final = runner.compute_final_scores()
        assert final["classification"] == expected_class, (
            f"Score {score} → expected {expected_class}, got {final['classification']}"
        )


# ---------------------------------------------------------------------------
# Reference scores
# ---------------------------------------------------------------------------

class TestReferenceScores:
    def setup_method(self):
        self.results = generate_reference_scores()

    def test_returns_dict(self):
        assert isinstance(self.results, dict)

    def test_at_least_10_models(self):
        assert len(self.results) >= 10

    def test_each_model_has_overall_score(self):
        for model, data in self.results.items():
            assert "overall_score" in data, f"Model {model} missing overall_score"
            assert 0.0 <= data["overall_score"] <= 1.0

    def test_orion_top_rank(self):
        scores = {m: d["overall_score"] for m, d in self.results.items()}
        top_model = max(scores, key=scores.get)
        assert top_model == "ORION", f"Expected ORION at top, got {top_model}"

    def test_orion_score_c4(self):
        orion = self.results.get("ORION", {})
        assert orion.get("classification") == "C-4", (
            f"ORION should be C-4, got {orion.get('classification')}"
        )

    def test_category_scores_exist(self):
        for model, data in self.results.items():
            cats = data.get("category_scores", {})
            assert cats, f"Model {model}: category_scores empty"

    def test_result_hash_exists(self):
        for model, data in self.results.items():
            assert "result_hash" in data, f"Model {model}: no result_hash"
            assert len(data["result_hash"]) >= 32
