"""
Tests for llm_api_integration — dry-run (via subprocess), structure, timeout handling.
No API calls are made in this suite.
"""
import subprocess
import sys
import pytest


class TestLLMJudgeDryRun:
    def test_dry_run_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "llm_api_integration.py", "--dry-run"],
            capture_output=True, text=True, timeout=30,
        )
        assert result.returncode == 0, f"Non-zero exit: {result.stderr}"

    def test_dry_run_reports_29_tests(self):
        result = subprocess.run(
            [sys.executable, "llm_api_integration.py", "--dry-run"],
            capture_output=True, text=True, timeout=30,
        )
        assert "29" in result.stdout, f"Expected '29' in output: {result.stdout}"

    def test_dry_run_smoke_test_passed(self):
        result = subprocess.run(
            [sys.executable, "llm_api_integration.py", "--dry-run"],
            capture_output=True, text=True, timeout=30,
        )
        assert "PASSED" in result.stdout, f"Smoke test not PASSED in: {result.stdout}"

    def test_dry_run_no_error_output(self):
        result = subprocess.run(
            [sys.executable, "llm_api_integration.py", "--dry-run"],
            capture_output=True, text=True, timeout=30,
        )
        # stderr may contain deprecation warnings but should not contain ERROR
        assert "Error" not in result.stderr and "Traceback" not in result.stderr, (
            f"Unexpected stderr: {result.stderr}"
        )
