#!/usr/bin/env python3
# Timestamp: "2025-05-18 06:07:01 (ywatanabe)"
# File: /ssh:sp:/home/ywatanabe/proj/scitex_repo/tests/scitex/decorators/test__numpy_fn.py
# ----------------------------------------
import os

__FILE__ = "./tests/scitex/decorators/test__numpy_fn.py"
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

from scitex_decorators import numpy_fn


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
def list_plus_one_result(list_input):
    # Arrange
    @numpy_fn
    def add_one(arr):
        return arr + 1.0

    # Act
    return add_one(list_input)


def test_numpy_fn_with_list_input_inner_receives_ndarray(list_input):
    # Arrange
    seen = {}

    @numpy_fn
    def capture_type(arr):
        seen["type"] = type(arr)
        return arr + 1.0

    # Act
    capture_type(list_input)
    # Assert
    assert seen["type"] is np.ndarray


def test_numpy_fn_with_list_input_returns_list(list_plus_one_result):
    # Arrange
    expected_type = list
    # Act
    actual_type = type(list_plus_one_result)
    # Assert
    assert actual_type is expected_type


def test_numpy_fn_with_list_input_returns_correct_values(list_plus_one_result):
    # Arrange
    expected = [2.0, 3.0, 4.0]
    # Act
    actual = list_plus_one_result
    # Assert
    assert actual == expected


@pytest.fixture
def numpy_doubled_result(numpy_input):
    # Arrange
    @numpy_fn
    def doubler(arr):
        return arr * 2.0

    # Act
    return doubler(numpy_input)


def test_numpy_fn_with_numpy_input_returns_ndarray(numpy_doubled_result):
    # Arrange
    expected_type = np.ndarray
    # Act
    actual = numpy_doubled_result
    # Assert
    assert isinstance(actual, expected_type)


def test_numpy_fn_with_numpy_input_returns_correct_values(numpy_doubled_result):
    # Arrange
    expected = np.array([2.0, 4.0, 6.0])
    # Act
    actual = numpy_doubled_result
    # Assert
    assert np.allclose(actual, expected)


def test_numpy_fn_with_numpy_input_inner_receives_ndarray(numpy_input):
    # Arrange
    seen = {}

    @numpy_fn
    def capture_type(arr):
        seen["type"] = type(arr)
        return arr * 2.0

    # Act
    capture_type(numpy_input)
    # Assert
    assert seen["type"] is np.ndarray


@pytest.fixture
def torch_tripled_result(torch_input):
    # Arrange
    @numpy_fn
    def tripler(arr):
        return arr * 3.0

    # Act
    return tripler(torch_input)


def test_numpy_fn_with_torch_input_returns_tensor(torch_tripled_result):
    # Arrange
    expected_type = torch.Tensor
    # Act
    actual = torch_tripled_result
    # Assert
    assert isinstance(actual, expected_type)


def test_numpy_fn_with_torch_input_returns_correct_values(torch_tripled_result):
    # Arrange
    expected = torch.tensor([3.0, 6.0, 9.0])
    # Act
    actual = torch_tripled_result
    # Assert
    assert torch.allclose(actual, expected)


def test_numpy_fn_with_torch_input_inner_receives_ndarray(torch_input):
    # Arrange
    seen = {}

    @numpy_fn
    def capture_type(arr):
        seen["type"] = type(arr)
        return arr * 3.0

    # Act
    capture_type(torch_input)
    # Assert
    assert seen["type"] is np.ndarray


@pytest.fixture
def nested_decorator_result(list_input):
    # Arrange
    def dummy_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper._current_decorator = "dummy_decorator"
            return func(*args, **kwargs)

        wrapper._is_wrapper = True
        return wrapper

    import scitex_decorators._numpy_fn as numpy_fn_module

    _orig_is_nested = numpy_fn_module.is_nested_decorator
    numpy_fn_module.is_nested_decorator = lambda: True
    try:

        @numpy_fn
        @dummy_decorator
        def nested_function(arr):
            return arr

        # Act
        return nested_function(list_input)
    finally:
        numpy_fn_module.is_nested_decorator = _orig_is_nested


def test_numpy_fn_nested_decorator_returns_list(nested_decorator_result):
    # Arrange
    expected_type = list
    # Act
    actual = nested_decorator_result
    # Assert
    assert isinstance(actual, expected_type)


def test_numpy_fn_nested_decorator_preserves_values(nested_decorator_result, list_input):
    # Arrange
    expected = list_input
    # Act
    actual = nested_decorator_result
    # Assert
    assert actual == expected


if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])

# EOF
