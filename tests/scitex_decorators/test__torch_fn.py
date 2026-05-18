#!/usr/bin/env python3
# Timestamp: "2025-04-30 15:49:06 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex_repo/tests/scitex/decorators/test__torch_fn.py
# ----------------------------------------
import os

__FILE__ = "./tests/scitex/decorators/test__torch_fn.py"
__DIR__ = os.path.dirname(__FILE__)
# ----------------------------------------
from functools import wraps

import numpy as np
import pytest

# Required for scitex_decorators module
pytest.importorskip("tqdm")

# Optional dependencies
torch = pytest.importorskip("torch")
pd = pytest.importorskip("pandas")
xr = pytest.importorskip("xarray")

from scitex_decorators import torch_fn


@pytest.fixture
def list_input():
    # Arrange
    return [1.0, 2.0, 3.0]


@pytest.fixture
def numpy_input():
    # Arrange
    return np.array([1.0, 2.0, 3.0])


@pytest.fixture
def torch_input():
    # Arrange
    return torch.tensor([1.0, 2.0, 3.0])


@pytest.fixture
def list_doubled_result(list_input):
    # Arrange
    @torch_fn
    def doubler(arr):
        return arr * 2.0

    # Act
    return doubler(list_input)


def test_torch_fn_with_list_input_inner_receives_tensor(list_input):
    # Arrange
    seen = {}

    @torch_fn
    def capture_type(arr):
        seen["type"] = type(arr)
        return arr * 2.0

    # Act
    capture_type(list_input)
    # Assert
    assert seen["type"] is torch.Tensor


def test_torch_fn_with_list_input_returns_list(list_doubled_result):
    # Arrange
    expected_type = list
    # Act
    actual = list_doubled_result
    # Assert
    assert isinstance(actual, expected_type)


def test_torch_fn_with_list_input_returns_correct_values(list_doubled_result):
    # Arrange
    expected = [2.0, 4.0, 6.0]
    # Act
    actual = list_doubled_result
    # Assert
    assert actual == expected


@pytest.fixture
def torch_doubled_result(torch_input):
    # Arrange
    @torch_fn
    def doubler(arr):
        return arr * 2.0

    # Act
    return doubler(torch_input)


def test_torch_fn_with_torch_input_returns_tensor(torch_doubled_result):
    # Arrange
    expected_type = torch.Tensor
    # Act
    actual = torch_doubled_result
    # Assert
    assert isinstance(actual, expected_type)


def test_torch_fn_with_torch_input_returns_correct_values(torch_doubled_result):
    # Arrange
    expected = torch.tensor([2.0, 4.0, 6.0])
    # Act
    actual = torch_doubled_result
    # Assert
    assert torch.allclose(actual, expected)


@pytest.fixture
def numpy_doubled_result(numpy_input):
    # Arrange
    @torch_fn
    def doubler(arr):
        return arr * 2.0

    # Act
    return doubler(numpy_input)


def test_torch_fn_with_numpy_input_returns_ndarray(numpy_doubled_result):
    # Arrange
    expected_type = np.ndarray
    # Act
    actual = numpy_doubled_result
    # Assert
    assert isinstance(actual, expected_type)


def test_torch_fn_with_numpy_input_returns_correct_values(numpy_doubled_result):
    # Arrange
    expected = np.array([2.0, 4.0, 6.0])
    # Act
    actual = numpy_doubled_result
    # Assert
    assert np.allclose(actual, expected)


@pytest.fixture
def nested_decorator_result(numpy_input):
    # Arrange
    def dummy_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper._current_decorator = "dummy_decorator"
            return func(*args, **kwargs)

        wrapper._is_wrapper = True
        return wrapper

    import scitex_decorators._torch_fn as torch_fn_module

    _orig_is_nested = torch_fn_module.is_nested_decorator
    torch_fn_module.is_nested_decorator = lambda: True
    try:

        @torch_fn
        @dummy_decorator
        def nested_function(arr):
            return arr

        # Act
        return nested_function(numpy_input)
    finally:
        torch_fn_module.is_nested_decorator = _orig_is_nested


def test_torch_fn_nested_decorator_returns_ndarray(nested_decorator_result):
    # Arrange
    expected_type = np.ndarray
    # Act
    actual = nested_decorator_result
    # Assert
    assert isinstance(actual, expected_type)


def test_torch_fn_nested_decorator_preserves_values(
    nested_decorator_result, numpy_input
):
    # Arrange
    expected = numpy_input
    # Act
    actual = nested_decorator_result
    # Assert
    assert np.array_equal(actual, expected)


if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])

# EOF
