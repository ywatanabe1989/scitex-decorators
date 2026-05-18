#!/usr/bin/env python3
# Timestamp: "2025-04-30 15:59:18 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex_repo/tests/scitex/decorators/test__pandas_fn.py
# ----------------------------------------
import os

__FILE__ = "./tests/scitex/decorators/test__pandas_fn.py"
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

from scitex_decorators import pandas_fn


@pytest.fixture
def list_input():
    # Arrange
    return [1.0, 2.0, 3.0]


@pytest.fixture
def numpy_input():
    # Arrange
    return np.array([1.0, 2.0, 3.0])


@pytest.fixture
def pandas_df_input():
    # Arrange
    return pd.DataFrame({"col1": [1.0, 2.0, 3.0]})


@pytest.fixture
def pandas_series_input():
    # Arrange
    return pd.Series([1.0, 2.0, 3.0])


@pytest.fixture
def list_plus_one_result(list_input):
    # Arrange
    @pandas_fn
    def add_one(df):
        return df + 1.0

    # Act
    return add_one(list_input)


def test_pandas_fn_with_list_input_inner_receives_dataframe(list_input):
    # Arrange
    seen = {}

    @pandas_fn
    def capture_type(df):
        seen["type"] = type(df)
        return df + 1.0

    # Act
    capture_type(list_input)
    # Assert
    assert seen["type"] is pd.DataFrame


def test_pandas_fn_with_list_input_returns_list(list_plus_one_result):
    # Arrange
    expected_type = list
    # Act
    actual = list_plus_one_result
    # Assert
    assert isinstance(actual, expected_type)


def test_pandas_fn_with_list_input_returns_correct_values(list_plus_one_result):
    # Arrange
    valid = (
        list_plus_one_result == [[2.0], [3.0], [4.0]]
        or list_plus_one_result == [2.0, 3.0, 4.0]
    )
    # Act
    result = valid
    # Assert
    assert result


@pytest.fixture
def df_doubled_result(pandas_df_input):
    # Arrange
    @pandas_fn
    def doubler(df):
        return df * 2.0

    # Act
    return doubler(pandas_df_input)


def test_pandas_fn_with_df_input_returns_dataframe(df_doubled_result):
    # Arrange
    expected_type = pd.DataFrame
    # Act
    actual = df_doubled_result
    # Assert
    assert isinstance(actual, expected_type)


def test_pandas_fn_with_df_input_returns_correct_values(df_doubled_result):
    # Arrange
    expected = pd.DataFrame({"col1": [2.0, 4.0, 6.0]})
    # Act
    actual = df_doubled_result
    # Assert
    assert actual.equals(expected)


@pytest.fixture
def numpy_tripled_result(numpy_input):
    # Arrange
    @pandas_fn
    def tripler(df):
        return df * 3.0

    # Act
    return tripler(numpy_input)


def test_pandas_fn_with_numpy_input_returns_ndarray(numpy_tripled_result):
    # Arrange
    expected_type = np.ndarray
    # Act
    actual = numpy_tripled_result
    # Assert
    assert isinstance(actual, expected_type)


def test_pandas_fn_with_numpy_input_returns_correct_values(numpy_tripled_result):
    # Arrange
    expected = np.array([[3.0], [6.0], [9.0]])
    # Act
    actual = numpy_tripled_result
    # Assert
    assert np.allclose(actual, expected)


@pytest.fixture
def nested_decorator_result(pandas_series_input):
    # Arrange
    def dummy_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper._current_decorator = "dummy_decorator"
            return func(*args, **kwargs)

        wrapper._is_wrapper = True
        return wrapper

    import scitex_decorators._pandas_fn as pandas_fn_module

    _orig_is_nested = pandas_fn_module.is_nested_decorator
    pandas_fn_module.is_nested_decorator = lambda: True
    try:

        @pandas_fn
        @dummy_decorator
        def nested_function(arr):
            return arr

        # Act
        return nested_function(pandas_series_input)
    finally:
        pandas_fn_module.is_nested_decorator = _orig_is_nested


def test_pandas_fn_nested_decorator_returns_series(nested_decorator_result):
    # Arrange
    expected_type = pd.Series
    # Act
    actual = nested_decorator_result
    # Assert
    assert isinstance(actual, expected_type)


def test_pandas_fn_nested_decorator_preserves_values(
    nested_decorator_result, pandas_series_input
):
    # Arrange
    expected = pandas_series_input
    # Act
    actual = nested_decorator_result
    # Assert
    assert actual.equals(expected)


if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])

# EOF
