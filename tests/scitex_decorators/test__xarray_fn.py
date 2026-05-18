#!/usr/bin/env python3
# Timestamp: "2025-04-30 16:25:56 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex_repo/tests/scitex/decorators/test__xarray_fn.py
# ----------------------------------------
import os

__FILE__ = "./tests/scitex/decorators/test__xarray_fn.py"
__DIR__ = os.path.dirname(__FILE__)
# ----------------------------------------

from functools import wraps

import numpy as np
import pytest

# Required for scitex_decorators module
pytest.importorskip("tqdm")

# Optional dependencies
pd = pytest.importorskip("pandas")
torch = pytest.importorskip("torch")
xr = pytest.importorskip("xarray")

from scitex_decorators import xarray_fn


@pytest.fixture
def list_input():
    # Arrange
    return [1.0, 2.0, 3.0]


@pytest.fixture
def numpy_input():
    # Arrange
    return np.array([1.0, 2.0, 3.0])


@pytest.fixture
def xarray_input():
    # Arrange
    return xr.DataArray([1.0, 2.0, 3.0])


@pytest.fixture
def torch_input():
    # Arrange
    return torch.tensor([1.0, 2.0, 3.0])


@pytest.fixture
def list_plus_one_result(list_input):
    # Arrange
    @xarray_fn
    def add_one(arr):
        return arr + 1.0

    # Act
    return add_one(list_input)


def test_xarray_fn_with_list_input_inner_receives_dataarray(list_input):
    # Arrange
    seen = {}

    @xarray_fn
    def capture_type(arr):
        seen["type"] = type(arr)
        return arr + 1.0

    # Act
    capture_type(list_input)
    # Assert
    assert seen["type"] is xr.DataArray


def test_xarray_fn_with_list_input_returns_list(list_plus_one_result):
    # Arrange
    expected_type = list
    # Act
    actual = list_plus_one_result
    # Assert
    assert isinstance(actual, expected_type)


def test_xarray_fn_with_list_input_returns_correct_values(list_plus_one_result):
    # Arrange
    expected = [2.0, 3.0, 4.0]
    # Act
    actual = list_plus_one_result
    # Assert
    assert actual == expected


@pytest.fixture
def xarray_doubled_result(xarray_input):
    # Arrange
    @xarray_fn
    def doubler(arr):
        return arr * 2.0

    # Act
    return doubler(xarray_input)


def test_xarray_fn_with_xarray_input_returns_dataarray(xarray_doubled_result):
    # Arrange
    expected_type = xr.DataArray
    # Act
    actual = xarray_doubled_result
    # Assert
    assert isinstance(actual, expected_type)


def test_xarray_fn_with_xarray_input_returns_correct_values(xarray_doubled_result):
    # Arrange
    expected = xr.DataArray([2.0, 4.0, 6.0])
    # Act
    actual = xarray_doubled_result
    # Assert
    assert np.allclose(actual.values, expected.values)


@pytest.fixture
def numpy_tripled_result(numpy_input):
    # Arrange
    @xarray_fn
    def tripler(arr):
        return arr * 3.0

    # Act
    return tripler(numpy_input)


def test_xarray_fn_with_numpy_input_returns_ndarray(numpy_tripled_result):
    # Arrange
    expected_type = np.ndarray
    # Act
    actual = numpy_tripled_result
    # Assert
    assert isinstance(actual, expected_type)


def test_xarray_fn_with_numpy_input_returns_correct_values(numpy_tripled_result):
    # Arrange
    expected = np.array([3.0, 6.0, 9.0])
    # Act
    actual = numpy_tripled_result
    # Assert
    assert np.allclose(actual, expected)


@pytest.fixture
def nested_decorator_result(torch_input):
    # Arrange
    def dummy_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper._current_decorator = "dummy_decorator"
            return func(*args, **kwargs)

        wrapper._is_wrapper = True
        return wrapper

    import scitex_decorators._xarray_fn as xarray_fn_module

    _orig_is_nested = xarray_fn_module.is_nested_decorator
    xarray_fn_module.is_nested_decorator = lambda: True
    try:

        @xarray_fn
        @dummy_decorator
        def nested_function(arr):
            return arr

        # Act
        return nested_function(torch_input)
    finally:
        xarray_fn_module.is_nested_decorator = _orig_is_nested


def test_xarray_fn_nested_decorator_returns_tensor(nested_decorator_result):
    # Arrange
    expected_type = torch.Tensor
    # Act
    actual = nested_decorator_result
    # Assert
    assert isinstance(actual, expected_type)


def test_xarray_fn_nested_decorator_preserves_values(
    nested_decorator_result, torch_input
):
    # Arrange
    expected = torch_input
    # Act
    actual = nested_decorator_result
    # Assert
    assert torch.allclose(actual, expected)


if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])

# EOF
