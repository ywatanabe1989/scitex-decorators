#!/usr/bin/env python3
# Time-stamp: "2026-05-18 (rewrite)"
# File: ./tests/scitex_decorators/_cache/test__cache_disk_async.py

"""Test cache_disk_async decorator functionality.

The cache_disk_async decorator provides disk-based caching for async functions
using joblib.Memory.
"""

import asyncio
import inspect

import pytest

pytest.importorskip("joblib")

from scitex_decorators import cache_disk_async


# ---------------------------------------------------------------------------
# Import check
# ---------------------------------------------------------------------------
def test_cache_disk_async_import_exposes_callable():
    # Arrange
    from scitex_decorators import cache_disk_async as imported
    # Act
    result = callable(imported)
    # Assert
    assert result is True


# ---------------------------------------------------------------------------
# Basic functionality — first and second call return same result
# ---------------------------------------------------------------------------
@pytest.fixture
def basic_async_runner():
    # Arrange
    state = {"count": 0}

    @cache_disk_async
    async def async_square(x):
        state["count"] += 1
        await asyncio.sleep(0.01)
        return x**2

    # Act
    r1 = asyncio.run(async_square(5))
    r2 = asyncio.run(async_square(5))
    return {"r1": r1, "r2": r2}


def test_cache_disk_async_basic_first_call_returns_square(basic_async_runner):
    # Arrange
    info = basic_async_runner
    # Act
    r1 = info["r1"]
    # Assert
    assert r1 == 25


def test_cache_disk_async_basic_second_call_returns_same(basic_async_runner):
    # Arrange
    info = basic_async_runner
    # Act
    r2 = info["r2"]
    # Assert
    assert r2 == 25


# ---------------------------------------------------------------------------
# Different arguments produce different cached results
# ---------------------------------------------------------------------------
@pytest.fixture
def different_args_async_runner():
    # Arrange
    @cache_disk_async
    async def async_multiply(x, y):
        await asyncio.sleep(0.01)
        return x * y

    # Act
    r1 = asyncio.run(async_multiply(3, 4))
    r2 = asyncio.run(async_multiply(5, 6))
    return {"r1": r1, "r2": r2}


def test_cache_disk_async_different_args_first_product(different_args_async_runner):
    # Arrange
    info = different_args_async_runner
    # Act
    r1 = info["r1"]
    # Assert
    assert r1 == 12


def test_cache_disk_async_different_args_second_product(different_args_async_runner):
    # Arrange
    info = different_args_async_runner
    # Act
    r2 = info["r2"]
    # Assert
    assert r2 == 30


# ---------------------------------------------------------------------------
# Keyword arguments produce distinct cache entries
# ---------------------------------------------------------------------------
@pytest.fixture
def kwargs_async_runner():
    # Arrange
    @cache_disk_async
    async def async_power(base, exponent=2):
        await asyncio.sleep(0.01)
        return base**exponent

    # Act
    r_default = asyncio.run(async_power(3))
    r_custom = asyncio.run(async_power(3, exponent=3))
    return {"default": r_default, "custom": r_custom}


def test_cache_disk_async_kwargs_default_exponent_returns_nine(kwargs_async_runner):
    # Arrange
    info = kwargs_async_runner
    # Act
    val = info["default"]
    # Assert
    assert val == 9


def test_cache_disk_async_kwargs_custom_exponent_returns_twentyseven(kwargs_async_runner):
    # Arrange
    info = kwargs_async_runner
    # Act
    val = info["custom"]
    # Assert
    assert val == 27


# ---------------------------------------------------------------------------
# Caching dict return type
# ---------------------------------------------------------------------------
def test_cache_disk_async_returns_dict_value_correctly():
    # Arrange
    @cache_disk_async
    async def async_return_dict(key, value):
        await asyncio.sleep(0.01)
        return {key: value}

    # Act
    result = asyncio.run(async_return_dict("test", 42))
    # Assert
    assert result == {"test": 42}


# ---------------------------------------------------------------------------
# Function metadata preservation
# ---------------------------------------------------------------------------
@pytest.fixture
def metadata_async_runner():
    # Arrange
    @cache_disk_async
    async def documented_async_func(x):
        """This is a documented async function"""
        return x * 2

    return documented_async_func


def test_cache_disk_async_preserves_function_name(metadata_async_runner):
    # Arrange
    func = metadata_async_runner
    # Act
    name = func.__name__
    # Assert
    assert name == "documented_async_func"


def test_cache_disk_async_preserves_function_docstring(metadata_async_runner):
    # Arrange
    func = metadata_async_runner
    # Act
    doc = func.__doc__
    # Assert
    assert doc == "This is a documented async function"


# ---------------------------------------------------------------------------
# Decorated function remains a coroutine function
# ---------------------------------------------------------------------------
def test_cache_disk_async_decorated_function_is_coroutine():
    # Arrange
    @cache_disk_async
    async def async_identity(x):
        return x

    # Act
    is_coro = inspect.iscoroutinefunction(async_identity)
    # Assert
    assert is_coro is True


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__)])

# EOF
