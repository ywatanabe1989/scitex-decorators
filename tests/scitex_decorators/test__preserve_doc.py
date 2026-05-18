#!/usr/bin/env python3
# Timestamp: "2025-04-28 15:45:18 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex_repo/tests/scitex/decorators/test__preserve_doc.py
# ----------------------------------------
import os

__FILE__ = "./tests/scitex/decorators/test__preserve_doc.py"
__DIR__ = os.path.dirname(__FILE__)
# ----------------------------------------

import pytest

# Required for scitex_decorators module
pytest.importorskip("tqdm")

from scitex_decorators import preserve_doc


def test_preserve_doc_preserves_original_function_name():
    """``preserve_doc`` should keep the original function's ``__name__``."""
    # Arrange
    @preserve_doc
    def sample_function():
        """Test docstring."""
        return True
    # Act
    name = sample_function.__name__
    # Assert
    assert name == "sample_function"


def test_preserve_doc_preserves_original_function_docstring():
    """``preserve_doc`` should keep the original function's ``__doc__``."""
    # Arrange
    @preserve_doc
    def sample_function():
        """This docstring should be preserved."""
        return True
    # Act
    doc = sample_function.__doc__
    # Assert
    assert doc == "This docstring should be preserved."


@pytest.fixture
def preserved_add():
    """Provide a ``preserve_doc``-wrapped two-argument addition function."""

    @preserve_doc
    def add(xx, yy):
        """Add two numbers."""
        return xx + yy

    return add


def test_preserve_doc_call_returns_correct_positive_sum(preserved_add):
    """Wrapped ``add`` returns the correct sum for positive inputs."""
    # Arrange
    fn = preserved_add
    # Act
    result = fn(2, 3)
    # Assert
    assert result == 5


def test_preserve_doc_call_returns_correct_zero_sum(preserved_add):
    """Wrapped ``add`` returns zero when summing inverse values."""
    # Arrange
    fn = preserved_add
    # Act
    result = fn(-1, 1)
    # Assert
    assert result == 0


def test_preserve_doc_with_missing_docstring_returns_none():
    """``preserve_doc`` leaves ``__doc__`` as ``None`` when source has no docstring."""
    # Arrange
    @preserve_doc
    def no_docstring_function():
        pass
    # Act
    doc = no_docstring_function.__doc__
    # Assert
    assert doc is None


if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])

# EOF
