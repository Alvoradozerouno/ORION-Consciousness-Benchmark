"""
Pytest configuration for ORION test suite
"""
import sys
import os

# Add repo root to path for imports
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)

# Change to repo root for file access (JSON, PROOFS.jsonl, etc.)
os.chdir(repo_root)
