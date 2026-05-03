"""
pytest configuration for ORION test suite.
Ensures the project root is on sys.path so tests can import modules directly.
"""
import os
import sys

# Add the repository root to sys.path so tests import directly without
# triggering the relative-import __init__.py package machinery.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
