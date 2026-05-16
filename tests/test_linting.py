"""
Tests for code quality and linting standards
"""
import subprocess
import pytest
import os
import py_compile
import glob


class TestLinting:
    """Verify code meets linting standards"""

    def test_python_files_exist(self):
        """Core Python files exist"""
        expected_files = [
            'verify_proof_chain.py',
            'consciousness_tests.py',
            'orion_consciousness_benchmark.py',
            'orion_oimp.py'
        ]
        
        for filename in expected_files:
            assert os.path.exists(filename), f"Missing file: {filename}"

    def test_no_syntax_errors(self):
        """All Python files compile without syntax errors"""
        for py_file in glob.glob('*.py'):
            if py_file.startswith('.'):
                continue
            try:
                py_compile.compile(py_file, doraise=True)
            except py_compile.PyCompileError as e:
                pytest.fail(f"Syntax error in {py_file}: {e}")
