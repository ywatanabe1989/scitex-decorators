#!/usr/bin/env python3
# Time-stamp: "2026-01-04 21:10:00 (ywatanabe)"
# File: ./tests/scitex/decorators/test__batch_fn.py

"""Test batch_fn decorator functionality.

The batch_fn decorator is designed for memory-efficient processing of large datasets.
It splits input data into batches, processes each batch independently, and combines
results by stacking. This is useful when data doesn't fit in memory all at once.

Key behaviors:
- Splits data along axis 0 (first dimension)
- Processes each batch independently
- Combines results via vstack (concatenation along axis 0)
- Suitable for row-wise operations, NOT global aggregations
"""

import numpy as np
import pytest

# Required for scitex_decorators module
pytest.importorskip("tqdm")

# Optional dependencies
torch = pytest.importorskip("torch")
pd = pytest.importorskip("pandas")

from scitex_decorators import batch_fn, numpy_fn, torch_fn


# --------------------------------------------------------------------------- #
# TestBatchFn — Core batching behaviour
# --------------------------------------------------------------------------- #
class TestBatchFn:
    """Test batch_fn decorator"""

    def test_batch_fn_preserves_row_wise_doubling_across_batches(self):
        """Batched application of ``x * 2`` over 12 rows split into 4 batches
        of 3 must produce the same result as the unbatched computation."""
        # Arrange
        @batch_fn
        def double_rows(x, batch_size=4):
            return x * 2

        data = np.random.randn(12, 5)
        # Act
        result = double_rows(data, batch_size=3)
        # Assert
        assert np.allclose(result, data * 2)

    def test_batch_fn_default_batch_size_splits_ten_into_three_calls(self):
        """With no ``batch_size`` kwarg supplied, batch_fn uses default 4 so
        10 rows yield exactly 3 underlying function invocations (4+4+2)."""
        # Arrange
        call_count = 0

        @batch_fn
        def count_calls(x, batch_size=4):
            nonlocal call_count
            call_count += 1
            return x

        data = np.arange(10).reshape(-1, 1)
        # Act
        count_calls(data)
        # Assert
        assert call_count == 3

    def test_batch_fn_default_batch_size_returns_data_unchanged(self):
        """Identity function passed through default batching must reproduce
        the original input values element-for-element."""
        # Arrange
        @batch_fn
        def count_calls(x, batch_size=4):
            return x

        data = np.arange(10).reshape(-1, 1)
        # Act
        result = count_calls(data)
        # Assert
        assert np.array_equal(result.flatten(), data.flatten())

    def test_batch_fn_processes_in_single_call_when_batch_exceeds_data(self):
        """When ``batch_size`` is larger than ``len(x)``, batch_fn should
        invoke the wrapped function exactly once with all data."""
        # Arrange
        call_count = 0

        @batch_fn
        def count_calls(x, batch_size=4):
            nonlocal call_count
            call_count += 1
            return x

        data = np.arange(5).reshape(-1, 1)
        # Act
        count_calls(data, batch_size=10)
        # Assert
        assert call_count == 1

    def test_batch_fn_returns_data_when_batch_exceeds_data_size(self):
        """When batch is larger than data, the single-shot result should
        equal the input data exactly."""
        # Arrange
        @batch_fn
        def count_calls(x, batch_size=4):
            return x

        data = np.arange(5).reshape(-1, 1)
        # Act
        result = count_calls(data, batch_size=10)
        # Assert
        assert np.array_equal(result.flatten(), data.flatten())

    def test_batch_fn_produces_independent_scalar_result_per_batch(self):
        """When each batch reduces to a scalar, the combined output is an
        array of per-batch scalars (no global aggregation)."""
        # Arrange
        @batch_fn
        def batch_mean(x, batch_size=4):
            return np.mean(x)

        data = np.arange(12).reshape(-1).astype(float)
        expected = np.array([1.5, 5.5, 9.5])
        # Act
        result = batch_mean(data, batch_size=4)
        # Assert
        assert np.allclose(result, expected)

    def test_batch_fn_handles_tuple_result_doubled_component(self):
        """When the wrapped function returns ``(x*2, x+1)``, the first
        tuple element of the combined output must equal ``x*2``."""
        # Arrange
        @batch_fn
        def transform_data(x, batch_size=4):
            return x * 2, x + 1

        data = np.random.randn(12, 5)
        # Act
        doubled, _incremented = transform_data(data, batch_size=3)
        # Assert
        assert np.allclose(doubled, data * 2)

    def test_batch_fn_handles_tuple_result_incremented_component(self):
        """When the wrapped function returns ``(x*2, x+1)``, the second
        tuple element of the combined output must equal ``x+1``."""
        # Arrange
        @batch_fn
        def transform_data(x, batch_size=4):
            return x * 2, x + 1

        data = np.random.randn(12, 5)
        # Act
        _doubled, incremented = transform_data(data, batch_size=3)
        # Assert
        assert np.allclose(incremented, data + 1)

    def test_batch_fn_mixed_tuple_array_component_is_vstacked(self):
        """Tuple results mixing an array and a non-stackable element should
        still vstack the array component correctly across batches."""
        # Arrange
        @batch_fn
        def describe_rows(x, batch_size=4):
            transformed = x * 2
            labels = ["doubled"]
            return transformed, labels

        data = np.random.randn(12, 5)
        # Act
        transformed, _labels = describe_rows(data, batch_size=3)
        # Assert
        assert np.allclose(transformed, data * 2)

    def test_batch_fn_mixed_tuple_non_stackable_uses_first_batch_value(self):
        """Non-stackable tuple elements (lists, strings, ...) take on the
        value produced by the first batch — they are NOT concatenated."""
        # Arrange
        @batch_fn
        def describe_rows(x, batch_size=4):
            return x * 2, ["doubled"]

        data = np.random.randn(12, 5)
        # Act
        _transformed, labels = describe_rows(data, batch_size=3)
        # Assert
        assert labels == ["doubled"]

    def test_batch_fn_with_torch_fn_preserves_2d_tensor_shape(self):
        """Stacking batch_fn over torch_fn for a 2D-preserving function
        must reproduce the unbatched torch result."""
        # Arrange
        @batch_fn
        @torch_fn
        def double_tensor(x, batch_size=4):
            return x * 2

        data = torch.randn(12, 5)
        # Act
        result = double_tensor(data, batch_size=3)
        # Assert
        assert torch.allclose(result, data * 2)

    def test_batch_fn_with_torch_fn_handles_multidim_column_slice(self):
        """A torch-backed batch function that slices columns (N, 5) -> (N, 2)
        must vstack correctly across batches and equal the direct slice."""
        # Arrange
        @batch_fn
        @torch_fn
        def reduce_to_2d(x, batch_size=4):
            return x[:, :2]

        data = torch.randn(12, 5)
        # Act
        result = reduce_to_2d(data, batch_size=3)
        # Assert
        assert torch.allclose(result, data[:, :2])

    def test_batch_fn_omits_batch_size_kwarg_when_function_lacks_param(self):
        """When the wrapped function's signature does not declare a
        ``batch_size`` parameter, batch_fn must not pass it through."""
        # Arrange
        @batch_fn
        def no_batch_param(x):
            return x * 2

        data = np.random.randn(12, 3)
        # Act
        result = no_batch_param(data, batch_size=3)
        # Assert
        assert np.allclose(result, data * 2)

    def test_batch_fn_forwards_additional_kwargs_to_wrapped_function(self):
        """User-supplied kwargs (other than ``batch_size``) must be passed
        through to the wrapped function unchanged across all batches."""
        # Arrange
        @batch_fn
        def scale_rows(x, scale=1.0, batch_size=4):
            return x * scale

        data = np.random.randn(12, 5)
        scale = 2.5
        # Act
        result = scale_rows(data, scale=scale, batch_size=3)
        # Assert
        assert np.allclose(result, data * scale)

    def test_batch_fn_handles_empty_input_array_gracefully(self):
        """An empty input array must round-trip through batch_fn without
        error and yield an empty result."""
        # Arrange
        @batch_fn
        def process(x, batch_size=4):
            return x * 2

        data = np.array([])
        # Act
        result = process(data)
        # Assert
        assert len(result) == 0

    def test_batch_fn_uneven_batches_track_expected_lengths(self):
        """For 10 inputs and batch_size=4 the wrapped function must see
        batches of sizes [4, 4, 2] in order."""
        # Arrange
        batch_sizes_seen = []

        @batch_fn
        def track_batch_size(x, batch_size=4):
            batch_sizes_seen.append(len(x))
            return x.reshape(-1, 1)

        data = np.arange(10)
        # Act
        track_batch_size(data, batch_size=4)
        # Assert
        assert batch_sizes_seen == [4, 4, 2]

    def test_batch_fn_uneven_batches_recombine_original_values(self):
        """Even when batch sizes are uneven, the recombined output values
        must equal the original input element-wise."""
        # Arrange
        @batch_fn
        def reshape_only(x, batch_size=4):
            return x.reshape(-1, 1)

        data = np.arange(10)
        # Act
        result = reshape_only(data, batch_size=4)
        # Assert
        assert np.array_equal(result.flatten(), data)

    def test_batch_fn_normalises_rows_independently_in_2d_arrays(self):
        """Row-wise normalisation (subtract row mean) batched across the
        first axis must equal the unbatched result."""
        # Arrange
        @batch_fn
        def normalize_rows(x, batch_size=4):
            return x - x.mean(axis=1, keepdims=True)

        data = np.random.randn(12, 5)
        expected = data - data.mean(axis=1, keepdims=True)
        # Act
        result = normalize_rows(data, batch_size=3)
        # Assert
        assert np.allclose(result, expected)


# --------------------------------------------------------------------------- #
# TestBatchFnWithOtherDecorators — Stacking with type-converter decorators
# --------------------------------------------------------------------------- #
class TestBatchFnWithOtherDecorators:
    """Test batch_fn combined with other decorators"""

    def test_batch_fn_with_torch_fn_scales_numpy_input_correctly(self):
        """batch_fn → torch_fn on numpy input must scale the rows by 3
        and return a numpy-compatible result equal to ``data * 3``."""
        # Arrange
        @batch_fn
        @torch_fn
        def torch_scale(x, batch_size=4):
            return x * 3

        data = np.random.randn(12, 5)
        # Act
        result = torch_scale(data, batch_size=3)
        # Assert
        assert np.allclose(result, data * 3, rtol=1e-6)

    def test_batch_fn_with_numpy_fn_scales_torch_input_correctly(self):
        """batch_fn → numpy_fn on torch input must scale rows by 2.5 and
        return a numpy-compatible result equal to ``data.numpy() * 2.5``."""
        # Arrange
        @batch_fn
        @numpy_fn
        def numpy_scale(x, batch_size=4):
            return x * 2.5

        data = torch.randn(12, 5)
        # Act
        result = numpy_scale(data, batch_size=3)
        # Assert
        assert np.allclose(result, data.numpy() * 2.5, rtol=1e-6)

    def test_batch_fn_with_torch_fn_increments_torch_input_correctly(self):
        """Nested batch_fn → torch_fn over a torch tensor must add 1 to
        every element and match the unbatched torch result."""
        # Arrange
        @batch_fn
        @torch_fn
        def nested_func(x, batch_size=4):
            return x + 1

        data = torch.randn(12, 5)
        # Act
        result = nested_func(data, batch_size=3)
        # Assert
        assert torch.allclose(result, data + 1)


# --------------------------------------------------------------------------- #
# TestBatchFnEdgeCases — Boundary conditions
# --------------------------------------------------------------------------- #
class TestBatchFnEdgeCases:
    """Test edge cases for batch_fn"""

    def test_batch_fn_handles_single_row_2d_array_input(self):
        """A single-row 2D input must round-trip through batch_fn with
        ``x * 2`` semantics applied to that one row."""
        # Arrange
        @batch_fn
        def process(x, batch_size=4):
            return x * 2

        data = np.array([[1, 2, 3]])
        # Act
        result = process(data, batch_size=4)
        # Assert
        assert np.array_equal(result, data * 2)

    def test_batch_fn_exact_batch_boundary_makes_three_calls(self):
        """When ``len(x)`` is an exact multiple of ``batch_size`` the
        wrapped function must be called exactly ``len(x)/batch_size`` times."""
        # Arrange
        call_count = 0

        @batch_fn
        def count_calls(x, batch_size=4):
            nonlocal call_count
            call_count += 1
            return x

        data = np.arange(12).reshape(-1, 1)
        # Act
        count_calls(data, batch_size=4)
        # Assert
        assert call_count == 3

    def test_batch_fn_exact_batch_boundary_returns_input_values(self):
        """When ``len(x)`` is an exact multiple of ``batch_size`` the
        recombined output must equal the input element-wise."""
        # Arrange
        @batch_fn
        def identity(x, batch_size=4):
            return x

        data = np.arange(12).reshape(-1, 1)
        # Act
        result = identity(data, batch_size=4)
        # Assert
        assert np.array_equal(result.flatten(), data.flatten())

    def test_batch_fn_preserves_float32_dtype_through_batching(self):
        """A float32 input must remain float32 after recombination through
        batch_fn's vstack step."""
        # Arrange
        @batch_fn
        def identity(x, batch_size=4):
            return x

        data = np.array([[1, 2], [3, 4], [5, 6]], dtype=np.float32)
        # Act
        result = identity(data, batch_size=2)
        # Assert
        assert result.dtype == np.float32


if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])

# EOF
