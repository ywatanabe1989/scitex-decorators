#!/usr/bin/env python3
# Timestamp: "2025-06-03 07:47:00 (ywatanabe)"
# File: ./tests/scitex/decorators/test__signal_fn.py

import numpy as np
import pytest

# Required for scitex_decorators module
pytest.importorskip("tqdm")

# Optional dependencies
pd = pytest.importorskip("pandas")
torch = pytest.importorskip("torch")
xr = pytest.importorskip("xarray")

from scitex_decorators import signal_fn


@pytest.fixture
def basic_signal_result():
    # Arrange
    @signal_fn
    def dummy_signal_function(signal, param=1.0):
        return signal + param

    input_signal = np.array([1.0, 2.0, 3.0])
    # Act
    return dummy_signal_function(input_signal, param=0.5)


def test_signal_fn_basic_functionality_returns_ndarray(basic_signal_result):
    # Arrange
    expected_type = np.ndarray
    # Act
    actual = basic_signal_result
    # Assert
    assert isinstance(actual, expected_type)


def test_signal_fn_basic_functionality_returns_correct_values(basic_signal_result):
    # Arrange
    expected = np.array([1.5, 2.5, 3.5])
    # Act
    actual = basic_signal_result
    # Assert
    assert np.allclose(actual, expected)


@pytest.fixture
def identity_decorated():
    # Arrange
    @signal_fn
    def identity_function(signal):
        return signal

    # Act
    return identity_function


def test_signal_fn_with_list_input_returns_list(identity_decorated):
    # Arrange
    input_list = [1.0, 2.0, 3.0]
    # Act
    result = identity_decorated(input_list)
    # Assert
    assert isinstance(result, list)


def test_signal_fn_with_list_input_preserves_values(identity_decorated):
    # Arrange
    input_list = [1.0, 2.0, 3.0]
    # Act
    result = identity_decorated(input_list)
    # Assert
    assert result == input_list


def test_signal_fn_with_numpy_input_returns_ndarray(identity_decorated):
    # Arrange
    input_array = np.array([1.0, 2.0, 3.0])
    # Act
    result = identity_decorated(input_array)
    # Assert
    assert isinstance(result, np.ndarray)


def test_signal_fn_with_numpy_input_preserves_values(identity_decorated):
    # Arrange
    input_array = np.array([1.0, 2.0, 3.0])
    # Act
    result = identity_decorated(input_array)
    # Assert
    assert np.array_equal(result, input_array)


def test_signal_fn_with_dataframe_input_returns_dataframe(identity_decorated):
    # Arrange
    input_df = pd.DataFrame({"col1": [1.0, 2.0], "col2": [3.0, 4.0]})
    # Act
    result = identity_decorated(input_df)
    # Assert
    assert isinstance(result, pd.DataFrame)


def test_signal_fn_with_dataframe_input_preserves_values(identity_decorated):
    # Arrange
    input_df = pd.DataFrame({"col1": [1.0, 2.0], "col2": [3.0, 4.0]})
    # Act
    result = identity_decorated(input_df)
    # Assert
    assert np.array_equal(result.values, input_df.values)


def test_signal_fn_with_series_input_returns_series(identity_decorated):
    # Arrange
    input_series = pd.Series([1.0, 2.0, 3.0])
    # Act
    result = identity_decorated(input_series)
    # Assert
    assert isinstance(result, pd.Series)


def test_signal_fn_with_series_input_preserves_values(identity_decorated):
    # Arrange
    input_series = pd.Series([1.0, 2.0, 3.0])
    # Act
    result = identity_decorated(input_series)
    # Assert
    assert np.array_equal(result.values, input_series.values)


def test_signal_fn_with_xarray_input_returns_dataarray(identity_decorated):
    # Arrange
    input_xr = xr.DataArray([1.0, 2.0, 3.0], dims=["x"])
    # Act
    result = identity_decorated(input_xr)
    # Assert
    assert isinstance(result, xr.DataArray)


def test_signal_fn_with_xarray_input_preserves_values(identity_decorated):
    # Arrange
    input_xr = xr.DataArray([1.0, 2.0, 3.0], dims=["x"])
    # Act
    result = identity_decorated(input_xr)
    # Assert
    assert np.array_equal(result.values, input_xr.values)


@pytest.fixture
def params_signal_result():
    # Arrange
    captured = {}

    @signal_fn
    def signal_with_params(signal, fs, window_size):
        captured["fs_type"] = type(fs)
        captured["window_size_type"] = type(window_size)
        return signal * fs / window_size

    input_signal = np.array([1.0, 2.0, 3.0])
    # Act
    result = signal_with_params(input_signal, 256.0, 128)
    return {"result": result, "captured": captured, "input": input_signal}


def test_signal_fn_preserves_fs_argument_type(params_signal_result):
    # Arrange
    captured = params_signal_result["captured"]
    # Act
    fs_type = captured["fs_type"]
    # Assert
    assert fs_type is float


def test_signal_fn_preserves_window_size_argument_type(params_signal_result):
    # Arrange
    captured = params_signal_result["captured"]
    # Act
    ws_type = captured["window_size_type"]
    # Assert
    assert ws_type is int


def test_signal_fn_with_extra_args_returns_ndarray(params_signal_result):
    # Arrange
    expected_type = np.ndarray
    # Act
    actual = params_signal_result["result"]
    # Assert
    assert isinstance(actual, expected_type)


def test_signal_fn_with_extra_args_returns_correct_values(params_signal_result):
    # Arrange
    input_signal = params_signal_result["input"]
    expected = input_signal * 256.0 / 128
    # Act
    actual = params_signal_result["result"]
    # Assert
    assert np.allclose(actual, expected)


@pytest.fixture
def tuple_return_result():
    # Arrange
    @signal_fn
    def function_returning_tuple(signal):
        processed_signal = signal * 2
        metadata = {"factor": 2.0}
        return processed_signal, metadata

    input_signal = np.array([1.0, 2.0, 3.0])
    # Act
    return function_returning_tuple(input_signal)


def test_signal_fn_tuple_return_signal_is_ndarray(tuple_return_result):
    # Arrange
    result_signal, _ = tuple_return_result
    # Act
    actual = result_signal
    # Assert
    assert isinstance(actual, np.ndarray)


def test_signal_fn_tuple_return_signal_has_correct_values(tuple_return_result):
    # Arrange
    result_signal, _ = tuple_return_result
    expected = np.array([2.0, 4.0, 6.0])
    # Act
    actual = result_signal
    # Assert
    assert np.allclose(actual, expected)


def test_signal_fn_tuple_return_metadata_unchanged(tuple_return_result):
    # Arrange
    _, result_metadata = tuple_return_result
    expected = {"factor": 2.0}
    # Act
    actual = result_metadata
    # Assert
    assert actual == expected


def test_signal_fn_with_empty_args_returns_tensor():
    # Arrange
    @signal_fn
    def function_no_args():
        return torch.tensor([1.0, 2.0, 3.0])

    # Act
    result = function_no_args()
    # Assert
    assert isinstance(result, torch.Tensor)


@pytest.fixture
def nested_decorator_result():
    # Arrange
    import scitex_decorators._signal_fn as signal_fn_module

    _orig_is_nested = signal_fn_module.is_nested_decorator
    signal_fn_module.is_nested_decorator = lambda: True
    try:

        @signal_fn
        def nested_function(signal):
            return signal

        input_signal = np.array([1.0, 2.0, 3.0])
        # Act
        result = nested_function(input_signal)
        return {"result": result, "input": input_signal}
    finally:
        signal_fn_module.is_nested_decorator = _orig_is_nested


def test_signal_fn_nested_decorator_bypasses_conversion(nested_decorator_result):
    # Arrange
    input_signal = nested_decorator_result["input"]
    # Act
    result = nested_decorator_result["result"]
    # Assert
    assert result is input_signal


def test_signal_fn_decorator_sets_is_wrapper_attribute():
    # Arrange
    @signal_fn
    def some_function(signal):
        return signal

    # Act
    actual = some_function._is_wrapper
    # Assert
    assert actual is True


def test_signal_fn_decorator_sets_decorator_type_attribute():
    # Arrange
    @signal_fn
    def some_function(signal):
        return signal

    # Act
    actual = some_function._decorator_type
    # Assert
    assert actual == "signal_fn"


@pytest.fixture
def kwargs_signal_result():
    # Arrange
    @signal_fn
    def signal_with_kwargs(signal, scale=1.0, offset=0.0):
        return signal * scale + offset

    input_signal = np.array([1.0, 2.0, 3.0])
    # Act
    result = signal_with_kwargs(input_signal, scale=2.0, offset=1.0)
    return {"result": result, "input": input_signal}


def test_signal_fn_with_kwargs_returns_ndarray(kwargs_signal_result):
    # Arrange
    expected_type = np.ndarray
    # Act
    actual = kwargs_signal_result["result"]
    # Assert
    assert isinstance(actual, expected_type)


def test_signal_fn_with_kwargs_returns_correct_values(kwargs_signal_result):
    # Arrange
    input_signal = kwargs_signal_result["input"]
    expected = input_signal * 2.0 + 1.0
    # Act
    actual = kwargs_signal_result["result"]
    # Assert
    assert np.allclose(actual, expected)


@pytest.fixture
def torch_identity_result():
    # Arrange
    @signal_fn
    def torch_identity(signal):
        return signal

    input_tensor = torch.tensor([1.0, 2.0, 3.0])
    # Act
    return {
        "result": torch_identity(input_tensor),
        "input": input_tensor,
    }


def test_signal_fn_torch_tensor_input_returns_tensor(torch_identity_result):
    # Arrange
    expected_type = torch.Tensor
    # Act
    actual = torch_identity_result["result"]
    # Assert
    assert isinstance(actual, expected_type)


def test_signal_fn_torch_tensor_input_preserves_values(torch_identity_result):
    # Arrange
    input_tensor = torch_identity_result["input"]
    # Act
    actual = torch_identity_result["result"]
    # Assert
    assert torch.allclose(actual, input_tensor)


@pytest.fixture
def complex_processing_result():
    # Arrange
    @signal_fn
    def complex_processing(signal, multiplier, add_noise=False):
        processed = signal * multiplier
        if add_noise:
            noise = torch.randn_like(processed) * 0.01
            processed = processed + noise
        return processed

    input_signal = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    # Act
    result = complex_processing(input_signal, multiplier=2.0, add_noise=False)
    return {"result": result, "input": input_signal}


def test_signal_fn_complex_processing_returns_ndarray(complex_processing_result):
    # Arrange
    expected_type = np.ndarray
    # Act
    actual = complex_processing_result["result"]
    # Assert
    assert isinstance(actual, expected_type)


def test_signal_fn_complex_processing_returns_correct_values(complex_processing_result):
    # Arrange
    input_signal = complex_processing_result["input"]
    expected = input_signal * 2.0
    # Act
    actual = complex_processing_result["result"]
    # Assert
    assert np.allclose(actual, expected)


def test_signal_fn_propagates_inner_function_error():
    # Arrange
    @signal_fn
    def function_with_error(signal):
        raise ValueError("Test error")

    input_signal = np.array([1.0, 2.0, 3.0])
    # Act
    ctx = pytest.raises(ValueError, match="Test error")
    # Assert
    with ctx:
        function_with_error(input_signal)


@pytest.fixture
def float64_passthrough_result():
    # Arrange
    @signal_fn
    def passthrough(signal):
        return signal

    arr_in = np.random.randn(64).astype(np.float64)
    # Act
    return {"out": passthrough(arr_in), "input": arr_in}


def test_signal_fn_float64_passthrough_returns_ndarray(float64_passthrough_result):
    # Arrange
    expected_type = np.ndarray
    # Act
    actual = float64_passthrough_result["out"]
    # Assert
    assert isinstance(actual, expected_type)


def test_signal_fn_float64_passthrough_preserves_dtype(float64_passthrough_result):
    # Arrange
    expected_dtype = np.float64
    # Act
    actual_dtype = float64_passthrough_result["out"].dtype
    # Assert
    assert actual_dtype == expected_dtype


@pytest.fixture
def float32_passthrough_result():
    # Arrange
    @signal_fn
    def passthrough(signal):
        return signal

    arr_in = np.random.randn(64).astype(np.float32)
    # Act
    return {"out": passthrough(arr_in), "input": arr_in}


def test_signal_fn_float32_passthrough_returns_ndarray(float32_passthrough_result):
    # Arrange
    expected_type = np.ndarray
    # Act
    actual = float32_passthrough_result["out"]
    # Assert
    assert isinstance(actual, expected_type)


def test_signal_fn_float32_passthrough_preserves_dtype(float32_passthrough_result):
    # Arrange
    expected_dtype = np.float32
    # Act
    actual_dtype = float32_passthrough_result["out"].dtype
    # Assert
    assert actual_dtype == expected_dtype


def test_signal_fn_preserves_float32_dtype_through_torch_op():
    # Arrange
    @signal_fn
    def scale(signal):
        return signal * 2.0

    arr_in = np.random.randn(32).astype(np.float32)
    # Act
    arr_out = scale(arr_in)
    # Assert
    assert arr_out.dtype == np.float32


def test_signal_fn_preserves_float64_dtype_through_torch_op():
    # Arrange
    @signal_fn
    def scale(signal):
        return signal * 2.0

    arr_in = np.random.randn(32).astype(np.float64)
    # Act
    arr_out = scale(arr_in)
    # Assert
    assert arr_out.dtype == np.float64


@pytest.fixture
def batched_passthrough_result():
    # Arrange
    @signal_fn
    def passthrough(signal):
        return signal

    arr_in = np.random.randn(8, 128).astype(np.float64)
    # Act
    return {"out": passthrough(arr_in), "input": arr_in}


def test_signal_fn_2d_batch_preserves_shape(batched_passthrough_result):
    # Arrange
    input_shape = batched_passthrough_result["input"].shape
    # Act
    out_shape = batched_passthrough_result["out"].shape
    # Assert
    assert out_shape == input_shape


def test_signal_fn_2d_batch_preserves_dtype(batched_passthrough_result):
    # Arrange
    expected_dtype = np.float64
    # Act
    actual_dtype = batched_passthrough_result["out"].dtype
    # Assert
    assert actual_dtype == expected_dtype


def test_signal_fn_to_torch_preserves_float64_dtype_directly():
    # Arrange
    from scitex_decorators._converters import _return_always, to_torch

    arr_in = np.random.randn(16).astype(np.float64)
    # Act
    converted = to_torch(arr_in, return_fn=_return_always)[0][0]
    # Assert
    assert converted.dtype == torch.float64


def test_signal_fn_to_torch_preserves_float32_dtype_directly():
    # Arrange
    from scitex_decorators._converters import _return_always, to_torch

    arr_in32 = np.random.randn(16).astype(np.float32)
    # Act
    converted32 = to_torch(arr_in32, return_fn=_return_always)[0][0]
    # Assert
    assert converted32.dtype == torch.float32


if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])

# EOF
