#!/usr/bin/env python3
# Time-stamp: "2026-05-18 (rewrite)"
# File: ./tests/scitex_decorators/_cache/test__cache_disk.py

"""Tests for disk caching decorator functionality."""

import functools
import os
import shutil
import tempfile
import time

import pytest

# Required for scitex_decorators module
pytest.importorskip("tqdm")

# joblib was changed from top-level eager import to lazy-import inside the
# decorator body (todo#442). The legacy tests in this file depend on
# joblib being available (they construct Memory objects directly).
joblib = pytest.importorskip(
    "joblib",
    reason="legacy cache_disk tests need joblib; lazy-import regression in test__lazy_imports.py",
)
Memory = joblib.Memory


# ---------------------------------------------------------------------------
# Helper: build an isolated cache_disk decorator backed by a tmp dir.
# ---------------------------------------------------------------------------
def _make_cache_disk_decorator(cache_dir):
    """Create a fresh cache_disk decorator with a specific cache directory."""
    memory = Memory(cache_dir, verbose=0)

    def cache_disk(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cached_func = memory.cache(func)
            return cached_func(*args, **kwargs)

        return wrapper

    return cache_disk


@pytest.fixture
def disk_cache_tmp_dir():
    """Yield a fresh temp directory for disk-cache tests."""
    # Arrange
    tmp = tempfile.mkdtemp()
    try:
        yield tmp
    finally:
        if os.path.exists(tmp):
            shutil.rmtree(tmp)


# ---------------------------------------------------------------------------
# Import check
# ---------------------------------------------------------------------------
def test_cache_disk_import_exposes_callable():
    # Arrange
    from scitex_decorators import cache_disk

    # Act
    result = callable(cache_disk)
    # Assert
    assert result is True


# ---------------------------------------------------------------------------
# Basic functionality — split into one-assert tests
# ---------------------------------------------------------------------------
@pytest.fixture
def basic_disk_cache_runner(disk_cache_tmp_dir):
    # Arrange
    cache_disk = _make_cache_disk_decorator(disk_cache_tmp_dir)
    state = {"count": 0}

    @cache_disk
    def simple_func(x):
        state["count"] += 1
        return x * 2

    # Act
    r1 = simple_func(5)
    count_after_first = state["count"]
    r2 = simple_func(5)
    count_after_second = state["count"]
    r3 = simple_func(10)
    count_after_third = state["count"]
    return {
        "r1": r1,
        "r2": r2,
        "r3": r3,
        "after_first": count_after_first,
        "after_second": count_after_second,
        "after_third": count_after_third,
    }


def test_cache_disk_basic_first_call_returns_doubled(basic_disk_cache_runner):
    # Arrange
    info = basic_disk_cache_runner
    # Act
    r1 = info["r1"]
    # Assert
    assert r1 == 10


def test_cache_disk_basic_first_call_executes_function(basic_disk_cache_runner):
    # Arrange
    info = basic_disk_cache_runner
    # Act
    count = info["after_first"]
    # Assert
    assert count == 1


def test_cache_disk_basic_second_call_returns_cached_value(basic_disk_cache_runner):
    # Arrange
    info = basic_disk_cache_runner
    # Act
    r2 = info["r2"]
    # Assert
    assert r2 == 10


def test_cache_disk_basic_second_call_does_not_re_execute(basic_disk_cache_runner):
    # Arrange
    info = basic_disk_cache_runner
    # Act
    count = info["after_second"]
    # Assert
    assert count == 1


def test_cache_disk_basic_third_call_returns_new_value(basic_disk_cache_runner):
    # Arrange
    info = basic_disk_cache_runner
    # Act
    r3 = info["r3"]
    # Assert
    assert r3 == 20


def test_cache_disk_basic_third_call_re_executes_for_new_arg(basic_disk_cache_runner):
    # Arrange
    info = basic_disk_cache_runner
    # Act
    count = info["after_third"]
    # Assert
    assert count == 2


# ---------------------------------------------------------------------------
# Multiple positional/keyword arguments
# ---------------------------------------------------------------------------
@pytest.fixture
def multi_arg_disk_runner(disk_cache_tmp_dir):
    # Arrange
    cache_disk = _make_cache_disk_decorator(disk_cache_tmp_dir)
    state = {"count": 0}

    @cache_disk
    def multi_arg_func(x, y, z=10):
        state["count"] += 1
        return x + y + z

    # Act
    r1 = multi_arg_func(1, 2)
    r2 = multi_arg_func(1, 2)
    r3 = multi_arg_func(1, 2, z=20)
    return {"r1": r1, "r2": r2, "r3": r3, "count": state["count"]}


def test_cache_disk_multi_arg_first_call_returns_sum(multi_arg_disk_runner):
    # Arrange
    info = multi_arg_disk_runner
    # Act
    r1 = info["r1"]
    # Assert
    assert r1 == 13


def test_cache_disk_multi_arg_second_call_returns_cached(multi_arg_disk_runner):
    # Arrange
    info = multi_arg_disk_runner
    # Act
    r2 = info["r2"]
    # Assert
    assert r2 == 13


def test_cache_disk_multi_arg_third_call_returns_new_sum(multi_arg_disk_runner):
    # Arrange
    info = multi_arg_disk_runner
    # Act
    r3 = info["r3"]
    # Assert
    assert r3 == 23


def test_cache_disk_multi_arg_total_executions_match_unique(multi_arg_disk_runner):
    # Arrange
    info = multi_arg_disk_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 2


# ---------------------------------------------------------------------------
# Keyword arguments
# ---------------------------------------------------------------------------
@pytest.fixture
def keyword_disk_runner(disk_cache_tmp_dir):
    # Arrange
    cache_disk = _make_cache_disk_decorator(disk_cache_tmp_dir)
    state = {"count": 0}

    @cache_disk
    def keyword_func(a, b=5, c=10):
        state["count"] += 1
        return a * b + c

    # Act
    r1 = keyword_func(2, b=3, c=4)
    r2 = keyword_func(2, b=3, c=4)
    return {"r1": r1, "r2": r2, "count": state["count"]}


def test_cache_disk_keyword_first_call_returns_correct_value(keyword_disk_runner):
    # Arrange
    info = keyword_disk_runner
    # Act
    r1 = info["r1"]
    # Assert
    assert r1 == 10


def test_cache_disk_keyword_second_call_returns_cached(keyword_disk_runner):
    # Arrange
    info = keyword_disk_runner
    # Act
    r2 = info["r2"]
    # Assert
    assert r2 == 10


def test_cache_disk_keyword_repeat_call_uses_cache(keyword_disk_runner):
    # Arrange
    info = keyword_disk_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 1


# ---------------------------------------------------------------------------
# Return types
# ---------------------------------------------------------------------------
@pytest.fixture
def return_types_disk_runner(disk_cache_tmp_dir):
    # Arrange
    cache_disk = _make_cache_disk_decorator(disk_cache_tmp_dir)
    state = {"count": 0}

    @cache_disk
    def return_various_types(type_name):
        state["count"] += 1
        if type_name == "list":
            return [1, 2, 3]
        elif type_name == "dict":
            return {"key": "value"}
        elif type_name == "tuple":
            return (1, 2, 3)
        elif type_name == "none":
            return None
        else:
            return type_name

    # Act
    list1 = return_various_types("list")
    list2 = return_various_types("list")
    dict1 = return_various_types("dict")
    none1 = return_various_types("none")
    return {
        "list1": list1,
        "list2": list2,
        "dict1": dict1,
        "none1": none1,
        "count": state["count"],
    }


def test_cache_disk_return_list_value_correct(return_types_disk_runner):
    # Arrange
    info = return_types_disk_runner
    # Act
    list1 = info["list1"]
    # Assert
    assert list1 == [1, 2, 3]


def test_cache_disk_return_list_cached_on_repeat(return_types_disk_runner):
    # Arrange
    info = return_types_disk_runner
    # Act
    list2 = info["list2"]
    # Assert
    assert list2 == [1, 2, 3]


def test_cache_disk_return_dict_value_correct(return_types_disk_runner):
    # Arrange
    info = return_types_disk_runner
    # Act
    dict1 = info["dict1"]
    # Assert
    assert dict1 == {"key": "value"}


def test_cache_disk_return_none_value_is_none(return_types_disk_runner):
    # Arrange
    info = return_types_disk_runner
    # Act
    none1 = info["none1"]
    # Assert
    assert none1 is None


def test_cache_disk_return_types_total_call_count_is_three(return_types_disk_runner):
    # Arrange
    info = return_types_disk_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 3


# ---------------------------------------------------------------------------
# Persistence across calls in the same session
# ---------------------------------------------------------------------------
@pytest.fixture
def persistence_disk_runner(disk_cache_tmp_dir):
    # Arrange
    cache_disk = _make_cache_disk_decorator(disk_cache_tmp_dir)
    state = {"count": 0}

    @cache_disk
    def persistent_func(x):
        state["count"] += 1
        return x**2

    # Act
    r1 = persistent_func(5)
    r2 = persistent_func(5)
    return {"r1": r1, "r2": r2, "count": state["count"]}


def test_cache_disk_persistence_first_call_returns_square(persistence_disk_runner):
    # Arrange
    info = persistence_disk_runner
    # Act
    r1 = info["r1"]
    # Assert
    assert r1 == 25


def test_cache_disk_persistence_second_call_returns_cached(persistence_disk_runner):
    # Arrange
    info = persistence_disk_runner
    # Act
    r2 = info["r2"]
    # Assert
    assert r2 == 25


def test_cache_disk_persistence_second_call_uses_cache(persistence_disk_runner):
    # Arrange
    info = persistence_disk_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 1


# ---------------------------------------------------------------------------
# Performance improvement
# ---------------------------------------------------------------------------
@pytest.fixture
def performance_disk_runner(disk_cache_tmp_dir):
    # Arrange
    cache_disk = _make_cache_disk_decorator(disk_cache_tmp_dir)

    @cache_disk
    def slow_function(n):
        time.sleep(0.05)
        return n**2

    # Act
    t0 = time.time()
    r1 = slow_function(5)
    first_time = time.time() - t0
    t1 = time.time()
    r2 = slow_function(5)
    second_time = time.time() - t1
    return {
        "r1": r1,
        "r2": r2,
        "first_time": first_time,
        "second_time": second_time,
    }


def test_cache_disk_performance_results_equal(performance_disk_runner):
    # Arrange
    info = performance_disk_runner
    # Act
    are_equal = info["r1"] == info["r2"] == 25
    # Assert
    assert are_equal is True


def test_cache_disk_performance_second_call_faster_than_first(performance_disk_runner):
    # Arrange
    info = performance_disk_runner
    # Act
    is_faster = info["second_time"] < info["first_time"] * 0.5
    # Assert
    assert is_faster is True


# ---------------------------------------------------------------------------
# SCITEX_DIR environment variable handling — using manual save/restore
# ---------------------------------------------------------------------------
@pytest.fixture
def scitex_dir_env_runner():
    # Arrange
    tmp = tempfile.mkdtemp()
    custom_scitex_dir = os.path.join(tmp, "custom_scitex") + os.sep
    _save = os.environ.get("SCITEX_DIR")
    os.environ["SCITEX_DIR"] = custom_scitex_dir
    try:
        from scitex_decorators import cache_disk

        @cache_disk
        def env_func(x):
            return x * 2

        # Act
        result = env_func(5)
        yield {"result": result}
    finally:
        if _save is None:
            os.environ.pop("SCITEX_DIR", None)
        else:
            os.environ["SCITEX_DIR"] = _save
        if os.path.exists(tmp):
            shutil.rmtree(tmp)


def test_cache_disk_respects_scitex_dir_env_returns_value(scitex_dir_env_runner):
    # Arrange
    info = scitex_dir_env_runner
    # Act
    result = info["result"]
    # Assert
    assert result == 10


# ---------------------------------------------------------------------------
# Default cache location (no env var) using helper-built decorator
# ---------------------------------------------------------------------------
def test_cache_disk_default_location_returns_correct_value(disk_cache_tmp_dir):
    # Arrange
    cache_disk = _make_cache_disk_decorator(disk_cache_tmp_dir)

    @cache_disk
    def default_loc_func(x):
        return x * 3

    # Act
    result = default_loc_func(7)
    # Assert
    assert result == 21


# ---------------------------------------------------------------------------
# Complex data structures
# ---------------------------------------------------------------------------
@pytest.fixture
def complex_data_disk_runner(disk_cache_tmp_dir):
    # Arrange
    cache_disk = _make_cache_disk_decorator(disk_cache_tmp_dir)
    state = {"count": 0}

    @cache_disk
    def complex_data_func(data_type):
        state["count"] += 1
        if data_type == "nested_dict":
            return {"level1": {"level2": {"values": [1, 2, 3, 4, 5]}}}
        elif data_type == "nested_list":
            return [[1, 2], [3, 4], [5, [6, 7]]]
        else:
            return {"simple": "data"}

    # Act
    r1 = complex_data_func("nested_dict")
    r2 = complex_data_func("nested_dict")
    return {"r1": r1, "r2": r2, "count": state["count"]}


def test_cache_disk_complex_data_first_call_returns_expected(complex_data_disk_runner):
    # Arrange
    expected = {"level1": {"level2": {"values": [1, 2, 3, 4, 5]}}}
    # Act
    r1 = complex_data_disk_runner["r1"]
    # Assert
    assert r1 == expected


def test_cache_disk_complex_data_second_call_returns_cached(complex_data_disk_runner):
    # Arrange
    expected = {"level1": {"level2": {"values": [1, 2, 3, 4, 5]}}}
    # Act
    r2 = complex_data_disk_runner["r2"]
    # Assert
    assert r2 == expected


def test_cache_disk_complex_data_repeat_does_not_re_execute(complex_data_disk_runner):
    # Arrange
    info = complex_data_disk_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 1


# ---------------------------------------------------------------------------
# Function signature preservation
# ---------------------------------------------------------------------------
@pytest.fixture
def signature_preservation_runner():
    # Arrange
    from scitex_decorators import cache_disk

    @cache_disk
    def documented_func(x, y=10):
        """This is a test function with documentation."""
        return x + y

    return documented_func


def test_cache_disk_preserves_function_name(signature_preservation_runner):
    # Arrange
    func = signature_preservation_runner
    # Act
    name = func.__name__
    # Assert
    assert name == "documented_func"


def test_cache_disk_preserves_function_docstring(signature_preservation_runner):
    # Arrange
    func = signature_preservation_runner
    # Act
    doc = func.__doc__
    # Assert
    assert "test function with documentation" in doc


# ---------------------------------------------------------------------------
# Exception handling — error not cached but successful results are.
# ---------------------------------------------------------------------------
@pytest.fixture
def exceptions_disk_runner(disk_cache_tmp_dir):
    # Arrange
    cache_disk = _make_cache_disk_decorator(disk_cache_tmp_dir)
    state = {"count": 0}

    @cache_disk
    def error_func(x):
        state["count"] += 1
        if x < 0:
            raise ValueError("Negative value not allowed")
        return x * 2

    return {"func": error_func, "state": state}


def test_cache_disk_exception_raises_value_error(exceptions_disk_runner):
    # Arrange
    func = exceptions_disk_runner["func"]
    # Act
    ctx = pytest.raises(ValueError)
    # Assert
    with ctx:
        func(-1)


def test_cache_disk_exception_increments_count_once(exceptions_disk_runner):
    # Arrange
    func = exceptions_disk_runner["func"]
    state = exceptions_disk_runner["state"]
    try:
        func(-1)
    except ValueError:
        pass
    # Act
    count = state["count"]
    # Assert
    assert count == 1


def test_cache_disk_successful_call_returns_doubled(exceptions_disk_runner):
    # Arrange
    func = exceptions_disk_runner["func"]
    # Act
    result = func(5)
    # Assert
    assert result == 10


def test_cache_disk_successful_call_is_cached(exceptions_disk_runner):
    # Arrange
    func = exceptions_disk_runner["func"]
    state = exceptions_disk_runner["state"]
    func(8)  # first call
    count_before = state["count"]
    func(8)  # cached
    # Act
    count_after = state["count"]
    # Assert
    assert count_after == count_before


# ---------------------------------------------------------------------------
# Cache directory creation under custom SCITEX_DIR — manual env save/restore
# ---------------------------------------------------------------------------
@pytest.fixture
def cache_directory_creation_runner():
    # Arrange
    tmp = tempfile.mkdtemp()
    custom_scitex_dir = os.path.join(tmp, "test_scitex") + os.sep
    _save = os.environ.get("SCITEX_DIR")
    os.environ["SCITEX_DIR"] = custom_scitex_dir
    try:
        from scitex_decorators import cache_disk

        @cache_disk
        def square_func(x):
            return x**2

        # Act
        result = square_func(4)
        yield {"result": result}
    finally:
        if _save is None:
            os.environ.pop("SCITEX_DIR", None)
        else:
            os.environ["SCITEX_DIR"] = _save
        if os.path.exists(tmp):
            shutil.rmtree(tmp)


def test_cache_disk_with_custom_dir_returns_correct_value(
    cache_directory_creation_runner,
):
    # Arrange
    info = cache_directory_creation_runner
    # Act
    result = info["result"]
    # Assert
    assert result == 16


# ---------------------------------------------------------------------------
# Multiple decorated functions on the same backend
# ---------------------------------------------------------------------------
@pytest.fixture
def multiple_functions_disk_runner(disk_cache_tmp_dir):
    # Arrange
    cache_disk = _make_cache_disk_decorator(disk_cache_tmp_dir)
    state = {"c1": 0, "c2": 0}

    @cache_disk
    def func1(x):
        state["c1"] += 1
        return x * 2

    @cache_disk
    def func2(x):
        state["c2"] += 1
        return x * 3

    # Act
    r1_first = func1(5)
    r2_first = func2(5)
    r1_cached = func1(5)
    r2_cached = func2(5)
    return {
        "r1_first": r1_first,
        "r2_first": r2_first,
        "r1_cached": r1_cached,
        "r2_cached": r2_cached,
        "c1": state["c1"],
        "c2": state["c2"],
    }


def test_cache_disk_multi_func_first_returns_doubled(multiple_functions_disk_runner):
    # Arrange
    info = multiple_functions_disk_runner
    # Act
    r1 = info["r1_first"]
    # Assert
    assert r1 == 10


def test_cache_disk_multi_func_first_returns_tripled(multiple_functions_disk_runner):
    # Arrange
    info = multiple_functions_disk_runner
    # Act
    r2 = info["r2_first"]
    # Assert
    assert r2 == 15


def test_cache_disk_multi_func_first_uses_cache(multiple_functions_disk_runner):
    # Arrange
    info = multiple_functions_disk_runner
    # Act
    c1 = info["c1"]
    # Assert
    assert c1 == 1


def test_cache_disk_multi_func_second_uses_cache(multiple_functions_disk_runner):
    # Arrange
    info = multiple_functions_disk_runner
    # Act
    c2 = info["c2"]
    # Assert
    assert c2 == 1


def test_cache_disk_multi_func_first_cached_value_correct(
    multiple_functions_disk_runner,
):
    # Arrange
    info = multiple_functions_disk_runner
    # Act
    r1c = info["r1_cached"]
    # Assert
    assert r1c == 10


def test_cache_disk_multi_func_second_cached_value_correct(
    multiple_functions_disk_runner,
):
    # Arrange
    info = multiple_functions_disk_runner
    # Act
    r2c = info["r2_cached"]
    # Assert
    assert r2c == 15


# ---------------------------------------------------------------------------
# Concurrent-like rapid access — only one execution
# ---------------------------------------------------------------------------
@pytest.fixture
def concurrent_disk_runner(disk_cache_tmp_dir):
    # Arrange
    cache_disk = _make_cache_disk_decorator(disk_cache_tmp_dir)
    state = {"count": 0}

    @cache_disk
    def rapid_func(x):
        state["count"] += 1
        return x * 2

    # Act
    results = [rapid_func(42) for _ in range(5)]
    return {"results": results, "count": state["count"]}


def test_cache_disk_concurrent_results_are_all_equal(concurrent_disk_runner):
    # Arrange
    info = concurrent_disk_runner
    # Act
    all_equal = all(r == 84 for r in info["results"])
    # Assert
    assert all_equal is True


def test_cache_disk_concurrent_function_executes_only_once(concurrent_disk_runner):
    # Arrange
    info = concurrent_disk_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 1


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])

# EOF
