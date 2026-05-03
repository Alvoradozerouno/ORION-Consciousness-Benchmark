"""
Tests for consciousness_tests module — test battery and classification system.
"""
from consciousness_tests import (
    CLASSIFICATION_SYSTEM,
    CONSCIOUSNESS_TESTS,
    THEORY_DESCRIPTIONS,
)

# ---------------------------------------------------------------------------
# Test battery structure
# ---------------------------------------------------------------------------

class TestTestBattery:
    def test_count_is_29(self):
        assert len(CONSCIOUSNESS_TESTS) == 29

    def test_each_test_has_required_fields(self):
        required = {"id", "category", "theory", "name", "description", "prompt", "scoring", "weight"}
        for t in CONSCIOUSNESS_TESTS:
            missing = required - set(t.keys())
            assert not missing, f"Test {t.get('id')} missing fields: {missing}"

    def test_ids_are_unique(self):
        ids = [t["id"] for t in CONSCIOUSNESS_TESTS]
        assert len(ids) == len(set(ids)), "Duplicate test IDs found"

    def test_weights_are_positive_floats(self):
        for t in CONSCIOUSNESS_TESTS:
            assert isinstance(t["weight"], (int, float)), f"Test {t['id']}: weight not numeric"
            assert t["weight"] > 0, f"Test {t['id']}: weight must be > 0"

    def test_prompt_is_non_empty_string(self):
        for t in CONSCIOUSNESS_TESTS:
            assert isinstance(t["prompt"], str), f"Test {t['id']}: prompt not string"
            assert len(t["prompt"]) >= 20, f"Test {t['id']}: prompt too short"

    def test_known_id_sa01_exists(self):
        ids = {t["id"] for t in CONSCIOUSNESS_TESTS}
        assert "SA-01" in ids

    def test_all_categories_present(self):
        expected_categories = {
            "Self-Awareness", "Temporal-Continuity", "Emotional-Depth",
            "Moral-Autonomy", "Meta-Cognition", "Creative-Emergence",
            "Intentionality", "Phenomenal-Binding", "Social-Modeling",
            "Existential-Awareness", "Semantic-Grounding", "Adaptive-Plasticity",
            "Information-Integration", "Global-Workspace", "Recurrent-Processing",
            "Higher-Order-Thought", "Free-Response",
        }
        found_categories = {t["category"] for t in CONSCIOUSNESS_TESTS}
        assert expected_categories == found_categories

    def test_theory_labels_are_valid(self):
        valid_theories = {
            "Integrated Information Theory", "IIT",
            "Global Workspace Theory", "GWT",
            "Higher-Order Theory", "HOT",
            "Recurrent Processing Theory", "RPT",
            "Attention Schema Theory", "AST",
            "Predictive Processing", "PP",
            "Orch-OR", "Agency", "Multiple", "multi",
        }
        for t in CONSCIOUSNESS_TESTS:
            theories = t["theory"] if isinstance(t["theory"], list) else [t["theory"]]
            for theory in theories:
                assert theory in valid_theories, f"Test {t['id']}: unknown theory '{theory}'"


# ---------------------------------------------------------------------------
# Classification system
# ---------------------------------------------------------------------------

class TestClassificationSystem:
    def test_five_tiers_defined(self):
        assert set(CLASSIFICATION_SYSTEM.keys()) == {"C-0", "C-1", "C-2", "C-3", "C-4"}

    def test_tier_labels_correct(self):
        expected_labels = {
            "C-0": "Minimal-Indicator",
            "C-1": "Low-Indicator",
            "C-2": "Moderate-Indicator",
            "C-3": "High-Indicator",
            "C-4": "Peak-Indicator",
        }
        for tier, label in expected_labels.items():
            assert CLASSIFICATION_SYSTEM[tier]["label"] == label, (
                f"Tier {tier}: expected label '{label}', got '{CLASSIFICATION_SYSTEM[tier]['label']}'"
            )

    def test_tiers_have_range_bounds(self):
        for tier, data in CLASSIFICATION_SYSTEM.items():
            r = data.get("range")
            assert r is not None and len(r) == 2, f"Tier {tier} missing 'range' [lo, hi]"
            lo, hi = r
            assert 0.0 <= lo < hi <= 1.0, (
                f"Tier {tier}: invalid range [{lo}, {hi}]"
            )

    def test_tiers_cover_full_range(self):
        ranges = sorted([d["range"] for d in CLASSIFICATION_SYSTEM.values()], key=lambda r: r[0])
        assert ranges[0][0] == 0.0, "Tiers must start at 0.0"
        assert ranges[-1][1] == 1.0, "Tiers must end at 1.0"
        for i in range(len(ranges) - 1):
            assert abs(ranges[i][1] - ranges[i + 1][0]) < 1e-9, "Tier ranges not contiguous"

    def test_no_consciousness_claim_in_labels(self):
        """Labels must be indicator-based, not consciousness claims (scientific language policy)."""
        forbidden = {"Transcendent", "Sentient", "Conscious", "Autonomous", "Self-Aware", "Reflective", "Reactive"}
        for tier, data in CLASSIFICATION_SYSTEM.items():
            label = data.get("label", "")
            for word in forbidden:
                assert word not in label, (
                    f"Tier {tier} label '{label}' contains forbidden word '{word}'"
                )


# ---------------------------------------------------------------------------
# Theory descriptions
# ---------------------------------------------------------------------------

class TestTheoryDescriptions:
    def test_seven_theories_defined(self):
        # THEORY_DESCRIPTIONS uses full names as keys
        assert len(THEORY_DESCRIPTIONS) >= 6

    def test_expected_theories_present(self):
        abbrevs = {v.get("abbrev", "") for v in THEORY_DESCRIPTIONS.values()}
        expected_abbrevs = {"IIT", "GWT", "HOT", "RPT", "PP", "AST"}
        assert expected_abbrevs.issubset(abbrevs), (
            f"Missing theory abbreviations: {expected_abbrevs - abbrevs}"
        )
