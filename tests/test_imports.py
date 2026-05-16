"""
Tests for module imports and basic functionality
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestImports:
    """Verify all core modules can be imported"""

    def test_import_verify_proof_chain(self):
        """verify_proof_chain module imports"""
        try:
            import verify_proof_chain
        except ImportError as e:
            pytest.fail(f"Failed to import verify_proof_chain: {e}")

    def test_import_consciousness_tests(self):
        """consciousness_tests module imports"""
        try:
            import consciousness_tests
        except ImportError as e:
            pytest.fail(f"Failed to import consciousness_tests: {e}")

    def test_import_orion_consciousness_benchmark(self):
        """orion_consciousness_benchmark module imports"""
        try:
            import orion_consciousness_benchmark
        except ImportError as e:
            pytest.fail(f"Failed to import orion_consciousness_benchmark: {e}")

    def test_verify_proof_chain_has_functions(self):
        """verify_proof_chain exports required functions"""
        from verify_proof_chain import compute_merkle_root, verify_hash, verify_chain
        assert callable(compute_merkle_root)
        assert callable(verify_hash)
        assert callable(verify_chain)

    def test_requirements_installable(self):
        """requirements.txt exists"""
        assert os.path.exists('requirements.txt')
        with open('requirements.txt') as f:
            lines = f.readlines()
        assert len(lines) > 0, "requirements.txt is empty"

    def test_python_version_correct(self):
        """Python version is 3.9+"""
        assert sys.version_info >= (3, 9), \
            f"Python version {sys.version_info.major}.{sys.version_info.minor} < 3.9"
