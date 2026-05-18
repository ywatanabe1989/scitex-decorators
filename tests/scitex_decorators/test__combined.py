#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: tests/scitex_decorators/test__combined.py

"""Tests for the combined decorators in ``scitex_decorators._combined``.

The module re-exports composite decorators that stack a type-conversion
decorator (``torch_fn`` / ``numpy_fn`` / ``pandas_fn``) on top of
``batch_fn``. It also publishes alias names (``batch_torch_fn``, …).

Each test verifies exactly one observable property using real objects
(PA-306: no mocks) and follows the Arrange / Act / Assert structure
(PA-307). Pure mock-theater tests from the previous version (which only
asserted that mocked sub-decorators were *called*, telling us nothing
about behavior) have been removed.
"""

from __future__ import annotations

import pytest

# Required for scitex_decorators module
pytest.importorskip("tqdm")
# Optional dep (extra="pandas") - skip module if absent. See PA-303.
pytest.importorskip("pandas")


# ---------------------------------------------------------------------------
# Existence + callability of each composite decorator
# ---------------------------------------------------------------------------


def test_torch_batch_fn_is_callable_export():
    # Arrange
    from scitex_decorators import torch_batch_fn
    # Act
    is_callable = callable(torch_batch_fn)
    # Assert
    assert is_callable


def test_numpy_batch_fn_is_callable_export():
    # Arrange
    from scitex_decorators import numpy_batch_fn
    # Act
    is_callable = callable(numpy_batch_fn)
    # Assert
    assert is_callable


def test_pandas_batch_fn_is_callable_export():
    # Arrange
    from scitex_decorators import pandas_batch_fn
    # Act
    is_callable = callable(pandas_batch_fn)
    # Assert
    assert is_callable


def test_batch_torch_fn_alias_is_callable_export():
    # Arrange
    from scitex_decorators import batch_torch_fn
    # Act
    is_callable = callable(batch_torch_fn)
    # Assert
    assert is_callable


def test_batch_numpy_fn_alias_is_callable_export():
    # Arrange
    from scitex_decorators import batch_numpy_fn
    # Act
    is_callable = callable(batch_numpy_fn)
    # Assert
    assert is_callable


def test_batch_pandas_fn_alias_is_callable_export():
    # Arrange
    from scitex_decorators import batch_pandas_fn
    # Act
    is_callable = callable(batch_pandas_fn)
    # Assert
    assert is_callable


# ---------------------------------------------------------------------------
# Aliases reference the same object as the canonical name
# ---------------------------------------------------------------------------


def test_batch_torch_fn_alias_references_torch_batch_fn():
    # Arrange
    from scitex_decorators import batch_torch_fn, torch_batch_fn
    # Act
    same_object = batch_torch_fn is torch_batch_fn
    # Assert
    assert same_object


def test_batch_numpy_fn_alias_references_numpy_batch_fn():
    # Arrange
    from scitex_decorators import batch_numpy_fn, numpy_batch_fn
    # Act
    same_object = batch_numpy_fn is numpy_batch_fn
    # Assert
    assert same_object


def test_batch_pandas_fn_alias_references_pandas_batch_fn():
    # Arrange
    from scitex_decorators import batch_pandas_fn, pandas_batch_fn
    # Act
    same_object = batch_pandas_fn is pandas_batch_fn
    # Assert
    assert same_object


# ---------------------------------------------------------------------------
# Metadata preservation via ``functools.wraps``
# ---------------------------------------------------------------------------


def test_torch_batch_fn_preserves_wrapped_function_name():
    # Arrange
    from scitex_decorators import torch_batch_fn

    @torch_batch_fn
    def some_named_function(x, y=1):
        """Some named function docstring."""
        return x + y

    # Act
    observed_name = some_named_function.__name__
    # Assert
    assert observed_name == "some_named_function"


def test_torch_batch_fn_preserves_wrapped_function_docstring():
    # Arrange
    from scitex_decorators import torch_batch_fn

    @torch_batch_fn
    def some_named_function(x, y=1):
        """Some named function docstring."""
        return x + y

    # Act
    observed_doc = some_named_function.__doc__
    # Assert
    assert "Some named function docstring" in observed_doc


def test_numpy_batch_fn_preserves_wrapped_function_name():
    # Arrange
    from scitex_decorators import numpy_batch_fn

    @numpy_batch_fn
    def numpy_named_function(x):
        """numpy named function docstring."""
        return x

    # Act
    observed_name = numpy_named_function.__name__
    # Assert
    assert observed_name == "numpy_named_function"


def test_pandas_batch_fn_preserves_wrapped_function_name():
    # Arrange
    from scitex_decorators import pandas_batch_fn

    @pandas_batch_fn
    def pandas_named_function(x):
        """pandas named function docstring."""
        return x

    # Act
    observed_name = pandas_named_function.__name__
    # Assert
    assert observed_name == "pandas_named_function"


# ---------------------------------------------------------------------------
# ``__all__`` membership
# ---------------------------------------------------------------------------


def test_torch_batch_fn_listed_in_package_all_exports():
    # Arrange
    from scitex_decorators import __all__
    # Act
    is_listed = "torch_batch_fn" in __all__
    # Assert
    assert is_listed


def test_numpy_batch_fn_listed_in_package_all_exports():
    # Arrange
    from scitex_decorators import __all__
    # Act
    is_listed = "numpy_batch_fn" in __all__
    # Assert
    assert is_listed


def test_pandas_batch_fn_listed_in_package_all_exports():
    # Arrange
    from scitex_decorators import __all__
    # Act
    is_listed = "pandas_batch_fn" in __all__
    # Assert
    assert is_listed


def test_batch_torch_fn_listed_in_package_all_exports():
    # Arrange
    from scitex_decorators import __all__
    # Act
    is_listed = "batch_torch_fn" in __all__
    # Assert
    assert is_listed


def test_batch_numpy_fn_listed_in_package_all_exports():
    # Arrange
    from scitex_decorators import __all__
    # Act
    is_listed = "batch_numpy_fn" in __all__
    # Assert
    assert is_listed


def test_batch_pandas_fn_listed_in_package_all_exports():
    # Arrange
    from scitex_decorators import __all__
    # Act
    is_listed = "batch_pandas_fn" in __all__
    # Assert
    assert is_listed


# ---------------------------------------------------------------------------
# Underlying single-purpose decorators remain importable
# ---------------------------------------------------------------------------


def test_batch_fn_dependency_is_callable_export():
    # Arrange
    from scitex_decorators import batch_fn
    # Act
    is_callable = callable(batch_fn)
    # Assert
    assert is_callable


def test_torch_fn_dependency_is_callable_export():
    # Arrange
    from scitex_decorators import torch_fn
    # Act
    is_callable = callable(torch_fn)
    # Assert
    assert is_callable


def test_numpy_fn_dependency_is_callable_export():
    # Arrange
    from scitex_decorators import numpy_fn
    # Act
    is_callable = callable(numpy_fn)
    # Assert
    assert is_callable


def test_pandas_fn_dependency_is_callable_export():
    # Arrange
    from scitex_decorators import pandas_fn
    # Act
    is_callable = callable(pandas_fn)
    # Assert
    assert is_callable


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__)])

# EOF
