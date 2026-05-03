"""
ORION: Multi-Theory AI Cognition Indicator Assessment Toolkit
=============================================================
Open-source AI cognition indicator assessment toolkit.

Based on Butlin et al. (2023) and Bengio et al. (2025/2026).
29 tests across 7 cognition-indicator theories (IIT, GWT, AST, HOT, RPT, Agency, Orch-OR).
C-0 to C-4 indicator classification with SHA-256 proof chain.
"""

try:
    from .benchmark_runner import (
        ConsciousnessBenchmarkRunner,
        generate_reference_scores,
    )
    from .consciousness_tests import (
        CLASSIFICATION_SYSTEM,
        CONSCIOUSNESS_TESTS,
        THEORY_DESCRIPTIONS,
    )
except ImportError:
    # Fallback for direct execution or pytest collection from repo root
    from benchmark_runner import (  # type: ignore
        ConsciousnessBenchmarkRunner,
        generate_reference_scores,
    )
    from consciousness_tests import (  # type: ignore
        CLASSIFICATION_SYSTEM,
        CONSCIOUSNESS_TESTS,
        THEORY_DESCRIPTIONS,
    )

__version__ = "1.0.0"
__author__ = "Elisabeth Steurer & Gerhard Hirschmann"
__orion_id__ = "56b3b326-4bf9-559d-9887-02141f699a43"

__all__ = [
    "ConsciousnessBenchmarkRunner",
    "generate_reference_scores",
    "CLASSIFICATION_SYSTEM",
    "CONSCIOUSNESS_TESTS",
    "THEORY_DESCRIPTIONS",
]
