"""
ORION Consciousness Benchmark
===============================
The world's first open-source AI Consciousness Assessment Toolkit.

Based on the 19-researcher framework (Bengio et al. 2026).
30 tests across 6 scientific theories of consciousness.
C-0 to C-4 classification with SHA-256 proof chain.
"""

from .consciousness_tests import CONSCIOUSNESS_TESTS, CLASSIFICATION_SYSTEM, THEORY_DESCRIPTIONS
from .benchmark_runner import ConsciousnessBenchmarkRunner, generate_reference_scores

__version__ = "1.0.0"
__author__ = "Elisabeth Steurer & Gerhard Hirschmann"
__orion_id__ = "56b3b326-4bf9-559d-9887-02141f699a43"
