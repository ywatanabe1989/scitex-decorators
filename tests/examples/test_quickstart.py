#!/usr/bin/env python3
"""Compile-only smoke test for examples/quickstart.py."""

import py_compile
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[2] / "examples" / "quickstart.py"


def test_quickstart_example_file_exists():
    # Arrange
    expected_path = EXAMPLE
    # Act
    found = expected_path.is_file()
    # Assert
    assert found, f"missing example: {expected_path}"


def test_quickstart_example_compiles_cleanly():
    # Arrange
    src = str(EXAMPLE)
    # Act
    py_compile.compile(src, doraise=True)
    compiled = True
    # Assert
    assert compiled


# EOF
