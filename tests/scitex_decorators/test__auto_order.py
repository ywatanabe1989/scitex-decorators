#!/usr/bin/env python3
# Time-stamp: "2025-06-01 10:45:00 (ywatanabe)"
# File: ./scitex_repo/tests/scitex/decorators/test__auto_order.py

"""Test auto-ordering decorator system"""

import numpy as np
import pytest

# Required for scitex_decorators module
pytest.importorskip("tqdm")

# Optional dependencies
torch = pytest.importorskip("torch")
pd = pytest.importorskip("pandas")

import scitex_decorators
from scitex_decorators import (
    batch_fn,
    disable_auto_order,
    enable_auto_order,
    numpy_fn,
    pandas_fn,
    torch_fn,
)


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #
@pytest.fixture
def _autoorder_off():
    """Provide a clean baseline with auto-ordering disabled before and after
    each test that uses it."""
    disable_auto_order()
    yield
    disable_auto_order()


@pytest.fixture
def _autoorder_on():
    """Enable auto-ordering for the duration of the test, then restore the
    standard decorators afterwards."""
    disable_auto_order()
    enable_auto_order()
    yield
    disable_auto_order()


@pytest.fixture
def _torch_batch_mean_results(_autoorder_on):
    """Run the same ``x.mean()`` function once with ``@batch_fn @ torch_fn``
    and once with the swapped order, returning ``(result1, result2)``."""

    @scitex_decorators.batch_fn
    @scitex_decorators.torch_fn
    def func1(x):
        return x.mean()

    @scitex_decorators.torch_fn
    @scitex_decorators.batch_fn
    def func2(x):
        return x.mean()

    data = np.random.randn(10, 5)
    return func1(data), func2(data)


@pytest.fixture
def _counting_func_first_call(_autoorder_on):
    """Build an ``@batch_fn @ torch_fn`` function and invoke it once; expose
    the function object so tests can inspect its post-call attributes."""

    @scitex_decorators.batch_fn
    @scitex_decorators.torch_fn
    def counting_func(x):
        return x.sum()

    counting_func(np.array([1, 2, 3]))
    return counting_func


@pytest.fixture
def _documented_func(_autoorder_on):
    """Build a docstring-bearing function under auto-ordering so the metadata
    can be inspected without re-doing the decoration in each test."""

    @scitex_decorators.batch_fn
    @scitex_decorators.torch_fn
    def documented_func(x):
        """This is a documented function"""
        return x * 2

    return documented_func


# --------------------------------------------------------------------------- #
# TestAutoOrder — Enabling, disabling, ordering, metadata
# --------------------------------------------------------------------------- #
class TestAutoOrder:
    """Test auto-ordering functionality"""

    def test_enable_auto_order_replaces_torch_fn_with_decorator_class(
        self, _autoorder_off
    ):
        """After ``enable_auto_order()``, the module-level ``torch_fn`` must
        be an instance of ``AutoOrderDecorator``."""
        # Arrange
        # Act
        enable_auto_order()
        # Assert
        assert (
            scitex_decorators.torch_fn.__class__.__name__
            == "AutoOrderDecorator"
        )

    def test_enable_auto_order_replaces_numpy_fn_with_decorator_class(
        self, _autoorder_off
    ):
        """After ``enable_auto_order()``, the module-level ``numpy_fn`` must
        be an instance of ``AutoOrderDecorator``."""
        # Arrange
        # Act
        enable_auto_order()
        # Assert
        assert (
            scitex_decorators.numpy_fn.__class__.__name__
            == "AutoOrderDecorator"
        )

    def test_enable_auto_order_replaces_pandas_fn_with_decorator_class(
        self, _autoorder_off
    ):
        """After ``enable_auto_order()``, the module-level ``pandas_fn`` must
        be an instance of ``AutoOrderDecorator``."""
        # Arrange
        # Act
        enable_auto_order()
        # Assert
        assert (
            scitex_decorators.pandas_fn.__class__.__name__
            == "AutoOrderDecorator"
        )

    def test_enable_auto_order_replaces_batch_fn_with_decorator_class(
        self, _autoorder_off
    ):
        """After ``enable_auto_order()``, the module-level ``batch_fn`` must
        be an instance of ``AutoOrderDecorator``."""
        # Arrange
        # Act
        enable_auto_order()
        # Assert
        assert (
            scitex_decorators.batch_fn.__class__.__name__
            == "AutoOrderDecorator"
        )

    def test_disable_auto_order_restores_original_torch_fn(
        self, _autoorder_off
    ):
        """After ``enable_auto_order()`` followed by ``disable_auto_order()``,
        the module's ``torch_fn`` must be the original function-named one."""
        # Arrange
        enable_auto_order()
        # Act
        disable_auto_order()
        # Assert
        assert scitex_decorators.torch_fn.__name__ == "torch_fn"

    def test_disable_auto_order_restores_original_numpy_fn(
        self, _autoorder_off
    ):
        """After ``enable_auto_order()`` followed by ``disable_auto_order()``,
        the module's ``numpy_fn`` must be the original function-named one."""
        # Arrange
        enable_auto_order()
        # Act
        disable_auto_order()
        # Assert
        assert scitex_decorators.numpy_fn.__name__ == "numpy_fn"

    def test_disable_auto_order_restores_original_pandas_fn(
        self, _autoorder_off
    ):
        """After ``enable_auto_order()`` followed by ``disable_auto_order()``,
        the module's ``pandas_fn`` must be the original function-named one."""
        # Arrange
        enable_auto_order()
        # Act
        disable_auto_order()
        # Assert
        assert scitex_decorators.pandas_fn.__name__ == "pandas_fn"

    def test_disable_auto_order_restores_original_batch_fn(
        self, _autoorder_off
    ):
        """After ``enable_auto_order()`` followed by ``disable_auto_order()``,
        the module's ``batch_fn`` must be the original function-named one."""
        # Arrange
        enable_auto_order()
        # Act
        disable_auto_order()
        # Assert
        assert scitex_decorators.batch_fn.__name__ == "batch_fn"

    def test_auto_ordering_makes_torch_batch_order_irrelevant(
        self, _torch_batch_mean_results
    ):
        """With auto-ordering, computing ``x.mean()`` under
        ``@batch_fn @ torch_fn`` and ``@torch_fn @ batch_fn`` must yield the
        same numerical result."""
        # Arrange
        result1, result2 = _torch_batch_mean_results
        # Act
        equal = np.allclose(result1, result2)
        # Assert
        assert equal

    def test_auto_ordering_handles_multiple_type_converters_on_torch_input(
        self, _autoorder_on
    ):
        """Stacking ``@batch_fn @ numpy_fn @ torch_fn`` on a torch input must
        return a numeric-compatible result, not raise."""
        # Arrange
        @scitex_decorators.batch_fn
        @scitex_decorators.numpy_fn
        @scitex_decorators.torch_fn
        def func(x):
            return x.mean()

        data = torch.randn(10, 5)
        # Act
        result = func(data)
        # Assert
        assert isinstance(result, (torch.Tensor, np.ndarray, np.floating, float))

    def test_auto_ordering_supports_complex_pandas_torch_stacking(
        self, _autoorder_on
    ):
        """Stacking ``@pandas_fn @ torch_fn`` on numpy input must return a
        ``pd.Series`` once auto-ordering reorders the converters."""
        # Arrange
        @scitex_decorators.pandas_fn
        @scitex_decorators.torch_fn
        def complex_func(x):
            if isinstance(x, torch.Tensor) and x.is_cuda:
                x = x.cpu()
            return pd.Series(x.flatten())

        data = np.random.randn(8, 5)
        # Act
        result = complex_func(data)
        # Assert
        assert isinstance(result, pd.Series)

    def test_auto_ordering_clears_pending_decorators_after_first_call(
        self, _counting_func_first_call
    ):
        """The ``_pending_decorators`` attribute is consumed on the first
        invocation and must not be present afterwards."""
        # Arrange
        counting_func = _counting_func_first_call
        # Act
        has_pending = hasattr(counting_func, "_pending_decorators")
        # Assert
        assert not has_pending

    def test_auto_ordering_installs_final_func_after_first_call(
        self, _counting_func_first_call
    ):
        """After the first invocation, the AutoOrderDecorator must cache the
        composed pipeline as ``_final_func`` on the wrapper."""
        # Arrange
        counting_func = _counting_func_first_call
        # Act
        has_final = hasattr(counting_func, "_final_func")
        # Assert
        assert has_final

    def test_auto_ordering_preserves_function_docstring(self, _documented_func):
        """``@functools.wraps``-style metadata must be preserved: the wrapped
        function's ``__doc__`` survives the decorator stack."""
        # Arrange
        documented_func = _documented_func
        # Act
        doc = documented_func.__doc__
        # Assert
        assert doc == "This is a documented function"

    def test_auto_ordering_preserves_function_name(self, _documented_func):
        """``@functools.wraps``-style metadata must be preserved: the wrapped
        function's ``__name__`` survives the decorator stack."""
        # Arrange
        documented_func = _documented_func
        # Act
        name = documented_func.__name__
        # Assert
        assert name == "documented_func"


# --------------------------------------------------------------------------- #
# TestAutoOrderIntegration — Real-world usage scenarios
# --------------------------------------------------------------------------- #
class TestAutoOrderIntegration:
    """Test auto-ordering with real use cases"""

    def test_stats_describe_returns_expected_first_output_shape(
        self, _autoorder_on
    ):
        """``scitex.stats.describe`` invoked under auto-ordering on a
        4-D tensor with ``dim=(1,2,3)`` returns a stats array of shape
        ``(87, 7)``."""
        # Arrange
        from scitex.stats import describe

        features_pac_z = np.random.randn(87, 5, 50, 30)
        tensor_input = torch.tensor(features_pac_z)
        # Act
        out = describe(tensor_input, dim=(1, 2, 3))
        # Assert
        assert out[0].shape == (87, 7)

    def test_stats_describe_returns_seven_stat_labels(self, _autoorder_on):
        """``scitex.stats.describe`` invoked under auto-ordering returns a
        labels list of length 7 (one per summarised statistic)."""
        # Arrange
        from scitex.stats import describe

        features_pac_z = np.random.randn(87, 5, 50, 30)
        tensor_input = torch.tensor(features_pac_z)
        # Act
        out = describe(tensor_input, dim=(1, 2, 3))
        # Assert
        assert len(out[1]) == 7

    def test_torch_fn_under_auto_order_accepts_nested_python_lists(
        self, _autoorder_on
    ):
        """Under auto-ordering, ``@torch_fn`` must accept nested Python lists
        and return a result equal to ``np.array(nested).mean()``."""
        # Arrange
        @scitex_decorators.torch_fn
        def process_nested(x):
            return x.mean()

        nested_data = [[1, 2, 3], [4, 5, 6]]
        expected = np.array(nested_data).mean()
        # Act
        result = process_nested(nested_data)
        # Assert
        assert np.allclose(result, expected)

    def test_torch_fn_under_auto_order_preserves_scalar_kwargs_as_float(
        self, _autoorder_on
    ):
        """Under auto-ordering, ``@torch_fn`` must forward scalar kwargs as
        floats so the body's ``isinstance(scale, float)`` assertion holds
        and the returned tensor equals ``data * scale``."""
        # Arrange
        @scitex_decorators.torch_fn
        def scale_tensor(x, scale=2.5):
            if not isinstance(scale, float):
                raise TypeError("scale must be a float")
            return x * scale

        data = torch.tensor([1, 2, 3])
        expected = data * 3.0
        # Act
        result = scale_tensor(data, scale=3.0)
        # Assert
        assert torch.allclose(result, expected)


if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])

# EOF
