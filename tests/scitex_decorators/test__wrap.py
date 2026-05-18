#!/usr/bin/env python3
# Timestamp: "2025-04-28 15:45:52 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex_repo/tests/scitex/decorators/test__wrap.py
# ----------------------------------------
import os

__FILE__ = "./tests/scitex/decorators/test__wrap.py"
__DIR__ = os.path.dirname(__FILE__)
# ----------------------------------------

import inspect

import pytest

# Required for scitex_decorators module
pytest.importorskip("tqdm")

from scitex_decorators import wrap


@pytest.fixture
def wrapped_sample_function():
    """Provide a wrapped function with a known name, docstring, and signature."""

    @wrap
    def sample_function(xx: int) -> int:
        """Test docstring."""
        return xx + 1

    return sample_function


def test_wrap_preserves_original_function_name(wrapped_sample_function):
    """Wrap should preserve the original function's ``__name__``."""
    # Arrange
    fn = wrapped_sample_function
    # Act
    name = fn.__name__
    # Assert
    assert name == "sample_function"


def test_wrap_preserves_original_function_docstring(wrapped_sample_function):
    """Wrap should preserve the original function's ``__doc__``."""
    # Arrange
    fn = wrapped_sample_function
    # Act
    doc = fn.__doc__
    # Assert
    assert doc == "Test docstring."


def test_wrap_preserves_original_function_signature(wrapped_sample_function):
    """Wrap should preserve the original function's signature."""
    # Arrange
    fn = wrapped_sample_function
    # Act
    signature = inspect.signature(fn)
    # Assert
    assert str(signature) == "(xx: int) -> int"


def test_wrap_preserves_original_function_module(wrapped_sample_function):
    """Wrap should preserve the original function's ``__module__``."""
    # Arrange
    fn = wrapped_sample_function
    # Act
    module = fn.__module__
    # Assert
    assert module == __name__


@pytest.fixture
def wrapped_add_one():
    """Provide a wrapped single-argument function that increments its input."""

    @wrap
    def add_one(xx: int) -> int:
        return xx + 1

    return add_one


def test_wrap_call_returns_expected_positive_result(wrapped_add_one):
    """Wrapped function returns the correct value for a positive input."""
    # Arrange
    fn = wrapped_add_one
    # Act
    result = fn(1)
    # Assert
    assert result == 2


def test_wrap_call_returns_expected_zero_result(wrapped_add_one):
    """Wrapped function returns the correct value for a zero input."""
    # Arrange
    fn = wrapped_add_one
    # Act
    result = fn(0)
    # Assert
    assert result == 1


def test_wrap_call_returns_expected_negative_result(wrapped_add_one):
    """Wrapped function returns the correct value for a negative input."""
    # Arrange
    fn = wrapped_add_one
    # Act
    result = fn(-1)
    # Assert
    assert result == 0


@pytest.fixture
def wrapped_multiply():
    """Provide a wrapped two-argument multiplication function."""

    @wrap
    def multiply(aa: int, bb: int) -> int:
        return aa * bb

    return multiply


def test_wrap_supports_positional_arguments_correctly(wrapped_multiply):
    """Wrapped function works when both arguments are positional."""
    # Arrange
    fn = wrapped_multiply
    # Act
    result = fn(2, 3)
    # Assert
    assert result == 6


def test_wrap_supports_keyword_arguments_correctly(wrapped_multiply):
    """Wrapped function works when both arguments are passed by keyword."""
    # Arrange
    fn = wrapped_multiply
    # Act
    result = fn(aa=2, bb=3)
    # Assert
    assert result == 6


def test_wrap_supports_mixed_positional_keyword_arguments(wrapped_multiply):
    """Wrapped function works with a mix of positional and keyword arguments."""
    # Arrange
    fn = wrapped_multiply
    # Act
    result = fn(2, bb=3)
    # Assert
    assert result == 6


@pytest.fixture
def manually_wrapped_subtract():
    """Provide a function manually wrapped via ``wrap(func)`` (non-decorator)."""

    def subtract(xx: int, yy: int) -> int:
        return xx - yy

    return wrap(subtract)


def test_wrap_manual_usage_positional_call(manually_wrapped_subtract):
    """Manually wrapped function returns the correct value with positional args."""
    # Arrange
    fn = manually_wrapped_subtract
    # Act
    result = fn(5, 3)
    # Assert
    assert result == 2


def test_wrap_manual_usage_keyword_call(manually_wrapped_subtract):
    """Manually wrapped function returns the correct value with keyword args."""
    # Arrange
    fn = manually_wrapped_subtract
    # Act
    result = fn(xx=10, yy=5)
    # Assert
    assert result == 5


if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])

# EOF
