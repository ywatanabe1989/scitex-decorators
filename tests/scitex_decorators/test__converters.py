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
    def test_is_userwarning_subclass(self):
        assert issubclass(ConversionWarning, UserWarning)


class TestIsTorch:
    def test_true_for_tensor_arg(self):
        assert is_torch(torch.zeros(3)) is True

    def test_true_for_tensor_kwarg(self):
        assert is_torch(x=torch.zeros(3)) is True

    def test_false_for_numpy_only(self):
        assert is_torch(np.zeros(3)) is False

    def test_false_for_no_args(self):
        assert is_torch() is False


class TestReturnAlways:
    def test_always_returns_args_kwargs_tuple(self):
        out = _return_always(1, 2, x=3)
        assert out == ((1, 2), {"x": 3})

    def test_no_args_no_kwargs(self):
        assert _return_always() == ((), {})


class TestReturnIf:
    def test_args_only(self):
        assert _return_if(1, 2) == (1, 2)

    def test_kwargs_only(self):
        assert _return_if(x=1) == {"x": 1}

    def test_both_returns_tuple(self):
        out = _return_if(1, x=2)
        assert out == ((1,), {"x": 2})

    def test_neither_returns_none(self):
        assert _return_if() is None


class TestToNumpy:
    def test_numpy_array_passes_through_in_tuple(self):
        arr = np.array([1, 2, 3])
        out = to_numpy(arr)
        # to_numpy returns a 1-tuple of converted positional args.
        assert isinstance(out, tuple) and len(out) == 1
        np.testing.assert_array_equal(out[0], arr)

    def test_torch_tensor_converts(self):
        t = torch.tensor([1.0, 2.0, 3.0])
        out = to_numpy(t)
        assert isinstance(out, tuple) and len(out) == 1
        assert isinstance(out[0], np.ndarray)
        np.testing.assert_array_equal(out[0], [1.0, 2.0, 3.0])

    def test_list_kept_as_is_inside_tuple(self):
        # Python lists are returned untouched inside the tuple wrapper —
        # the converter only transforms torch tensors / numpy arrays.
        out = to_numpy([1, 2, 3])
        assert out == ([1, 2, 3],)


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__), "-v"])

# EOF
