"""Smoke tests: every example script must run to completion."""

import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES = list(Path(__file__).parent.parent.joinpath("examples").glob("*.py"))


def test_examples_directory_has_at_least_one_script():
    # Arrange
    scripts = EXAMPLES
    # Act
    count = len(scripts)
    # Assert
    assert count > 0, "no example scripts found"


@pytest.mark.parametrize("example_path", EXAMPLES, ids=lambda p: p.name)
def test_example_script_runs_to_completion(example_path, tmp_path):
    # Arrange
    cmd = [sys.executable, str(example_path)]
    # Act
    r = subprocess.run(
        cmd,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    # Assert
    assert r.returncode == 0, f"{example_path.name} failed: {r.stderr}"
