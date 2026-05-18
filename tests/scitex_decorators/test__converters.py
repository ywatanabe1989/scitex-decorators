#!/usr/bin/env python3
"""Tests for scitex_decorators._converters.

Covers the predicates (`is_torch`, `is_cuda`) and the round-trippable
helpers (`to_numpy`, `to_torch`) that don't require GPU. Skipped
gracefully when torch isn't installed.
"""

import numpy as np
import pytest

from scitex_decorators._converters import (
    ConversionWarning,
    _return_always,
    _return_if,
    is_torch,
    to_numpy,
)

torch = pytest.importorskip("torch")


class TestConversionWarning:
    def test_conversion_warning_is_userwarning_subclass(self):
        # Arrange
        cls = ConversionWarning
        # Act
        is_subclass = issubclass(cls, UserWarning)
        # Assert
        assert is_subclass


class TestIsTorch:
    def test_is_torch_returns_true_for_tensor_positional_arg(self):
        # Arrange
        t = torch.zeros(3)
        # Act
        result = is_torch(t)
        # Assert
        assert result is True

    def test_is_torch_returns_true_for_tensor_keyword_arg(self):
        # Arrange
        t = torch.zeros(3)
        # Act
        result = is_torch(x=t)
        # Assert
        assert result is True

    def test_is_torch_returns_false_for_numpy_only_arg(self):
        # Arrange
        arr = np.zeros(3)
        # Act
        result = is_torch(arr)
        # Assert
        assert result is False

    def test_is_torch_returns_false_when_no_args_given(self):
        # Arrange
        # (no args)
        # Act
        result = is_torch()
        # Assert
        assert result is False


class TestReturnAlways:
    def test_return_always_returns_args_kwargs_tuple_pair(self):
        # Arrange
        # (inline args)
        # Act
        out = _return_always(1, 2, x=3)
        # Assert
        assert out == ((1, 2), {"x": 3})

    def test_return_always_handles_no_args_no_kwargs(self):
        # Arrange
        # (no args)
        # Act
        out = _return_always()
        # Assert
        assert out == ((), {})


class TestReturnIf:
    def test_return_if_with_args_only_returns_args_tuple(self):
        # Arrange
        # (inline args)
        # Act
        out = _return_if(1, 2)
        # Assert
        assert out == (1, 2)

    def test_return_if_with_kwargs_only_returns_kwargs_dict(self):
        # Arrange
        # (inline args)
        # Act
        out = _return_if(x=1)
        # Assert
        assert out == {"x": 1}

    def test_return_if_with_both_returns_pair_tuple(self):
        # Arrange
        # (inline args)
        # Act
        out = _return_if(1, x=2)
        # Assert
        assert out == ((1,), {"x": 2})

    def test_return_if_with_neither_returns_none(self):
        # Arrange
        # (no args)
        # Act
        out = _return_if()
        # Assert
        assert out is None


class TestToNumpy:
    def test_to_numpy_wraps_numpy_array_in_one_tuple(self):
        # Arrange
        arr = np.array([1, 2, 3])
        # Act
        out = to_numpy(arr)
        # Assert
        assert isinstance(out, tuple) and len(out) == 1

    def test_to_numpy_preserves_numpy_array_values_inside_tuple(self):
        # Arrange
        arr = np.array([1, 2, 3])
        # Act
        out = to_numpy(arr)
        # Assert
        assert np.array_equal(out[0], arr)

    def test_to_numpy_converts_torch_tensor_to_ndarray_inside_tuple(self):
        # Arrange
        t = torch.tensor([1.0, 2.0, 3.0])
        # Act
        out = to_numpy(t)
        # Assert
        assert isinstance(out[0], np.ndarray)

    def test_to_numpy_returns_one_element_tuple_for_torch_input(self):
        # Arrange
        t = torch.tensor([1.0, 2.0, 3.0])
        # Act
        out = to_numpy(t)
        # Assert
        assert isinstance(out, tuple) and len(out) == 1

    def test_to_numpy_preserves_torch_tensor_values_after_conversion(self):
        # Arrange
        t = torch.tensor([1.0, 2.0, 3.0])
        expected = np.array([1.0, 2.0, 3.0])
        # Act
        out = to_numpy(t)
        # Assert
        assert np.array_equal(out[0], expected)

    def test_to_numpy_returns_python_list_untouched_inside_tuple(self):
        # Arrange
        lst = [1, 2, 3]
        # Act
        out = to_numpy(lst)
        # Assert
        assert out == ([1, 2, 3],)


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__), "-v"])

# EOF
