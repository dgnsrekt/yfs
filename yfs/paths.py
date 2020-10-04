"""Module for commonly used paths."""

from pathlib import Path

SOURCE_ROOT = Path(__file__).parent
"""* A path to the yfs source code directory."""

PROJECT_ROOT = SOURCE_ROOT.parent
"""* A path to the yfs project directory."""

TEST_DIRECTORY = PROJECT_ROOT / "tests"
"""* A path to the yfs test directory"""
