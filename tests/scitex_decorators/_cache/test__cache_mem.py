#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2026-05-18 (rewrite)"
# File: ./tests/scitex_decorators/_cache/test__cache_mem.py

"""Tests for memory caching decorator functionality."""

import time

import pytest

# Required for scitex_decorators module
pytest.importorskip("tqdm")


# ---------------------------------------------------------------------------
# test_cache_mem_import_exposes_callable
# ---------------------------------------------------------------------------
def test_cache_mem_import_exposes_callable():
    # Arrange
    from scitex_decorators import cache_mem
    # Act
    result = callable(cache_mem)
    # Assert
    assert result is True


# ---------------------------------------------------------------------------
# Basic functionality: first call executes, second call uses cache,
# different argument re-executes.
# ---------------------------------------------------------------------------
@pytest.fixture
def basic_simple_func_runner():
    """Build a counter-tracked cached function for basic-functionality tests."""
    # Arrange
    from scitex_decorators import cache_mem

    state = {"count": 0}

    @cache_mem
    def simple_func(x):
        state["count"] += 1
        return x * 2

    # Act (warm-up: first call executes, second call hits cache, third call new key)
    r1 = simple_func(5)
    r2 = simple_func(5)
    r3 = simple_func(10)
    return {"r1": r1, "r2": r2, "r3": r3, "count": state["count"]}


def test_cache_mem_basic_first_call_returns_doubled_value(basic_simple_func_runner):
    # Arrange
    info = basic_simple_func_runner
    # Act
    r1 = info["r1"]
    # Assert
    assert r1 == 10


def test_cache_mem_basic_second_call_returns_cached_value(basic_simple_func_runner):
    # Arrange
    info = basic_simple_func_runner
    # Act
    r2 = info["r2"]
    # Assert
    assert r2 == 10


def test_cache_mem_basic_third_call_returns_new_computation(basic_simple_func_runner):
    # Arrange
    info = basic_simple_func_runner
    # Act
    r3 = info["r3"]
    # Assert
    assert r3 == 20


def test_cache_mem_basic_total_executions_equals_unique_inputs(basic_simple_func_runner):
    # Arrange
    info = basic_simple_func_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 2


# ---------------------------------------------------------------------------
# Multiple arguments
# ---------------------------------------------------------------------------
@pytest.fixture
def multi_arg_runner():
    # Arrange
    from scitex_decorators import cache_mem

    state = {"count": 0}

    @cache_mem
    def multi_arg_func(x, y, z=10):
        state["count"] += 1
        return x + y + z

    # Act
    r1 = multi_arg_func(1, 2)
    r2 = multi_arg_func(1, 2)
    r3 = multi_arg_func(1, 2, z=20)
    r4 = multi_arg_func(1, 2, z=20)
    return {"r1": r1, "r2": r2, "r3": r3, "r4": r4, "count": state["count"]}


def test_cache_mem_multi_arg_first_call_computes_sum(multi_arg_runner):
    # Arrange
    info = multi_arg_runner
    # Act
    r1 = info["r1"]
    # Assert
    assert r1 == 13


def test_cache_mem_multi_arg_repeat_call_uses_cache(multi_arg_runner):
    # Arrange
    info = multi_arg_runner
    # Act
    r2 = info["r2"]
    # Assert
    assert r2 == 13


def test_cache_mem_multi_arg_different_kwarg_computes_new_value(multi_arg_runner):
    # Arrange
    info = multi_arg_runner
    # Act
    r3 = info["r3"]
    # Assert
    assert r3 == 23


def test_cache_mem_multi_arg_repeat_kwarg_call_uses_cache(multi_arg_runner):
    # Arrange
    info = multi_arg_runner
    # Act
    r4 = info["r4"]
    # Assert
    assert r4 == 23


def test_cache_mem_multi_arg_total_call_count_is_two(multi_arg_runner):
    # Arrange
    info = multi_arg_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 2


# ---------------------------------------------------------------------------
# Keyword arguments
# ---------------------------------------------------------------------------
@pytest.fixture
def keyword_arg_runner():
    # Arrange
    from scitex_decorators import cache_mem

    state = {"count": 0}

    @cache_mem
    def keyword_func(a, b=5, c=10):
        state["count"] += 1
        return a * b + c

    # Act
    r1 = keyword_func(2, b=3, c=4)
    r2 = keyword_func(2, b=3, c=4)
    return {"r1": r1, "r2": r2, "count": state["count"]}


def test_cache_mem_keyword_first_call_returns_correct_value(keyword_arg_runner):
    # Arrange
    info = keyword_arg_runner
    # Act
    r1 = info["r1"]
    # Assert
    assert r1 == 10


def test_cache_mem_keyword_second_call_returns_same_value(keyword_arg_runner):
    # Arrange
    info = keyword_arg_runner
    # Act
    r2 = info["r2"]
    # Assert
    assert r2 == 10


def test_cache_mem_keyword_repeat_call_does_not_increase_count(keyword_arg_runner):
    # Arrange
    info = keyword_arg_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 1


# ---------------------------------------------------------------------------
# Return types
# ---------------------------------------------------------------------------
@pytest.fixture
def return_types_runner():
    # Arrange
    from scitex_decorators import cache_mem

    state = {"count": 0}

    @cache_mem
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
    none2 = return_various_types("none")
    return {
        "list1": list1,
        "list2": list2,
        "dict1": dict1,
        "none1": none1,
        "none2": none2,
        "count": state["count"],
    }


def test_cache_mem_return_list_value_correct(return_types_runner):
    # Arrange
    info = return_types_runner
    # Act
    list1 = info["list1"]
    # Assert
    assert list1 == [1, 2, 3]


def test_cache_mem_return_list_cached_on_repeat(return_types_runner):
    # Arrange
    info = return_types_runner
    # Act
    list2 = info["list2"]
    # Assert
    assert list2 == [1, 2, 3]


def test_cache_mem_return_dict_value_correct(return_types_runner):
    # Arrange
    info = return_types_runner
    # Act
    dict1 = info["dict1"]
    # Assert
    assert dict1 == {"key": "value"}


def test_cache_mem_return_none_value_is_none(return_types_runner):
    # Arrange
    info = return_types_runner
    # Act
    none1 = info["none1"]
    # Assert
    assert none1 is None


def test_cache_mem_return_none_cached_on_repeat(return_types_runner):
    # Arrange
    info = return_types_runner
    # Act
    none2 = info["none2"]
    # Assert
    assert none2 is None


def test_cache_mem_return_types_total_call_count_is_three(return_types_runner):
    # Arrange
    info = return_types_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 3


# ---------------------------------------------------------------------------
# Hashable (tuple) input caching
# ---------------------------------------------------------------------------
@pytest.fixture
def hashable_input_runner():
    # Arrange
    from scitex_decorators import cache_mem

    state = {"count": 0}

    @cache_mem
    def process_list(lst):
        state["count"] += 1
        return sum(lst)

    # Act
    r1 = process_list((1, 2, 3))
    r2 = process_list((1, 2, 3))
    return {"r1": r1, "r2": r2, "count": state["count"]}


def test_cache_mem_hashable_input_first_call_returns_sum(hashable_input_runner):
    # Arrange
    info = hashable_input_runner
    # Act
    r1 = info["r1"]
    # Assert
    assert r1 == 6


def test_cache_mem_hashable_input_second_call_returns_cached_value(hashable_input_runner):
    # Arrange
    info = hashable_input_runner
    # Act
    r2 = info["r2"]
    # Assert
    assert r2 == 6


def test_cache_mem_hashable_input_repeat_call_does_not_re_execute(hashable_input_runner):
    # Arrange
    info = hashable_input_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 1


# ---------------------------------------------------------------------------
# Performance improvement: second call faster than first
# ---------------------------------------------------------------------------
def test_cache_mem_performance_second_call_faster_than_first():
    # Arrange
    from scitex_decorators import cache_mem

    @cache_mem
    def slow_function(n):
        time.sleep(0.02)
        return n**2

    t0 = time.time()
    _ = slow_function(5)
    first_time = time.time() - t0
    t1 = time.time()
    _ = slow_function(5)
    second_time = time.time() - t1
    # Act
    ratio_ok = second_time < first_time / 2
    # Assert
    assert ratio_ok is True


# ---------------------------------------------------------------------------
# cache_info — lru_cache attribute behaviors
# ---------------------------------------------------------------------------
@pytest.fixture
def cache_info_runner():
    # Arrange
    from scitex_decorators import cache_mem

    @cache_mem
    def inner_func(x):
        return x * 2

    # Act
    initial_info = inner_func.cache_info()
    inner_func(5)
    after_first_info = inner_func.cache_info()
    inner_func(5)
    after_second_info = inner_func.cache_info()
    return {
        "has_cache_info": hasattr(inner_func, "cache_info"),
        "initial": initial_info,
        "after_first": after_first_info,
        "after_second": after_second_info,
    }


def test_cache_mem_cache_info_attribute_exists(cache_info_runner):
    # Arrange
    info = cache_info_runner
    # Act
    has_attr = info["has_cache_info"]
    # Assert
    assert has_attr is True


def test_cache_mem_cache_info_initial_hits_are_zero(cache_info_runner):
    # Arrange
    info = cache_info_runner
    # Act
    hits = info["initial"].hits
    # Assert
    assert hits == 0


def test_cache_mem_cache_info_initial_misses_are_zero(cache_info_runner):
    # Arrange
    info = cache_info_runner
    # Act
    misses = info["initial"].misses
    # Assert
    assert misses == 0


def test_cache_mem_cache_info_after_first_call_has_one_miss(cache_info_runner):
    # Arrange
    info = cache_info_runner
    # Act
    misses = info["after_first"].misses
    # Assert
    assert misses == 1


def test_cache_mem_cache_info_after_first_call_has_zero_hits(cache_info_runner):
    # Arrange
    info = cache_info_runner
    # Act
    hits = info["after_first"].hits
    # Assert
    assert hits == 0


def test_cache_mem_cache_info_after_second_call_has_one_hit(cache_info_runner):
    # Arrange
    info = cache_info_runner
    # Act
    hits = info["after_second"].hits
    # Assert
    assert hits == 1


def test_cache_mem_cache_info_after_second_call_misses_unchanged(cache_info_runner):
    # Arrange
    info = cache_info_runner
    # Act
    misses = info["after_second"].misses
    # Assert
    assert misses == 1


# ---------------------------------------------------------------------------
# cache_clear functionality
# ---------------------------------------------------------------------------
@pytest.fixture
def cache_clear_runner():
    # Arrange
    from scitex_decorators import cache_mem

    state = {"count": 0}

    @cache_mem
    def inner_func(x):
        state["count"] += 1
        return x * 2

    # Act
    inner_func(5)
    inner_func(5)
    count_before_clear = state["count"]
    inner_func.cache_clear()
    inner_func(5)
    count_after_clear = state["count"]
    return {"before": count_before_clear, "after": count_after_clear}


def test_cache_mem_cache_clear_initial_calls_count_one(cache_clear_runner):
    # Arrange
    info = cache_clear_runner
    # Act
    count = info["before"]
    # Assert
    assert count == 1


def test_cache_mem_cache_clear_re_executes_after_clear(cache_clear_runner):
    # Arrange
    info = cache_clear_runner
    # Act
    count = info["after"]
    # Assert
    assert count == 2


# ---------------------------------------------------------------------------
# Unlimited size
# ---------------------------------------------------------------------------
@pytest.fixture
def unlimited_size_runner():
    # Arrange
    from scitex_decorators import cache_mem

    state = {"count": 0}

    @cache_mem
    def inner_func(x):
        state["count"] += 1
        return x

    # Act
    for i in range(1000):
        inner_func(i)
    after_first_pass = state["count"]
    for i in range(1000):
        inner_func(i)
    after_second_pass = state["count"]
    return {"first": after_first_pass, "second": after_second_pass}


def test_cache_mem_unlimited_size_first_pass_executes_each(unlimited_size_runner):
    # Arrange
    info = unlimited_size_runner
    # Act
    first = info["first"]
    # Assert
    assert first == 1000


def test_cache_mem_unlimited_size_second_pass_uses_cache(unlimited_size_runner):
    # Arrange
    info = unlimited_size_runner
    # Act
    second = info["second"]
    # Assert
    assert second == 1000


# ---------------------------------------------------------------------------
# Exception handling — exceptions not cached
# ---------------------------------------------------------------------------
@pytest.fixture
def exception_handling_runner():
    # Arrange
    from scitex_decorators import cache_mem

    state = {"count": 0}

    @cache_mem
    def error_func(x):
        state["count"] += 1
        if x < 0:
            raise ValueError("Negative value")
        return x * 2

    return {"func": error_func, "state": state}


def test_cache_mem_exception_first_call_raises_value_error(exception_handling_runner):
    # Arrange
    func = exception_handling_runner["func"]
    # Act
    ctx = pytest.raises(ValueError)
    # Assert
    with ctx:
        func(-1)


def test_cache_mem_exception_repeat_call_re_raises(exception_handling_runner):
    # Arrange
    func = exception_handling_runner["func"]
    try:
        func(-1)
    except ValueError:
        pass
    # Act
    ctx = pytest.raises(ValueError)
    # Assert
    with ctx:
        func(-1)


def test_cache_mem_exception_is_not_cached_increments_count(exception_handling_runner):
    # Arrange
    func = exception_handling_runner["func"]
    state = exception_handling_runner["state"]
    try:
        func(-1)
    except ValueError:
        pass
    try:
        func(-1)
    except ValueError:
        pass
    # Act
    count = state["count"]
    # Assert
    assert count == 2


def test_cache_mem_exception_successful_call_returns_value(exception_handling_runner):
    # Arrange
    func = exception_handling_runner["func"]
    # Act
    result = func(5)
    # Assert
    assert result == 10


def test_cache_mem_exception_successful_call_is_cached(exception_handling_runner):
    # Arrange
    func = exception_handling_runner["func"]
    state = exception_handling_runner["state"]
    func(7)  # first execution for x=7
    count_before = state["count"]
    func(7)  # cached
    # Act
    count_after = state["count"]
    # Assert
    assert count_after == count_before


# ---------------------------------------------------------------------------
# Class methods — note lru_cache caches across instances when wrapping methods
# ---------------------------------------------------------------------------
@pytest.fixture
def class_method_runner():
    # Arrange
    from scitex_decorators import cache_mem

    class TestClass:
        def __init__(self):
            self.call_count = 0

        @cache_mem
        def cached_method(self, x):
            self.call_count += 1
            return x * 2

    obj = TestClass()
    # Act
    r1 = obj.cached_method(5)
    count_after_first = obj.call_count
    r2 = obj.cached_method(5)
    count_after_second = obj.call_count
    return {
        "r1": r1,
        "r2": r2,
        "count_after_first": count_after_first,
        "count_after_second": count_after_second,
    }


def test_cache_mem_class_method_first_call_returns_doubled(class_method_runner):
    # Arrange
    info = class_method_runner
    # Act
    r1 = info["r1"]
    # Assert
    assert r1 == 10


def test_cache_mem_class_method_second_call_returns_cached(class_method_runner):
    # Arrange
    info = class_method_runner
    # Act
    r2 = info["r2"]
    # Assert
    assert r2 == 10


def test_cache_mem_class_method_first_call_increments_count(class_method_runner):
    # Arrange
    info = class_method_runner
    # Act
    count = info["count_after_first"]
    # Assert
    assert count == 1


def test_cache_mem_class_method_second_call_does_not_increment(class_method_runner):
    # Arrange
    info = class_method_runner
    # Act
    count = info["count_after_second"]
    # Assert
    assert count == 1


# ---------------------------------------------------------------------------
# Decorated function attributes
# ---------------------------------------------------------------------------
@pytest.fixture
def decorated_attrs_runner():
    # Arrange
    from scitex_decorators import cache_mem

    @cache_mem
    def documented_func(x):
        """This is a test function."""
        return x

    return documented_func


def test_cache_mem_decorated_function_has_cache_info_attribute(decorated_attrs_runner):
    # Arrange
    func = decorated_attrs_runner
    # Act
    has_it = hasattr(func, "cache_info")
    # Assert
    assert has_it is True


def test_cache_mem_decorated_function_has_cache_clear_attribute(decorated_attrs_runner):
    # Arrange
    func = decorated_attrs_runner
    # Act
    has_it = hasattr(func, "cache_clear")
    # Assert
    assert has_it is True


def test_cache_mem_decorated_function_cache_info_is_callable(decorated_attrs_runner):
    # Arrange
    func = decorated_attrs_runner
    # Act
    is_callable = callable(func.cache_info)
    # Assert
    assert is_callable is True


def test_cache_mem_decorated_function_cache_clear_is_callable(decorated_attrs_runner):
    # Arrange
    func = decorated_attrs_runner
    # Act
    is_callable = callable(func.cache_clear)
    # Assert
    assert is_callable is True


# ---------------------------------------------------------------------------
# lru_cache wrapper behaviour
# ---------------------------------------------------------------------------
def test_cache_mem_wraps_lru_cache_with_no_maxsize_limit():
    # Arrange
    from scitex_decorators import cache_mem

    @cache_mem
    def inner_func(x):
        return x * 2

    # Act
    maxsize = inner_func.cache_info().maxsize
    # Assert
    assert maxsize is None


# ---------------------------------------------------------------------------
# Concurrent-like rapid access — only one execution
# ---------------------------------------------------------------------------
@pytest.fixture
def concurrent_access_runner():
    # Arrange
    from scitex_decorators import cache_mem

    state = {"count": 0}

    @cache_mem
    def inner_func(x):
        state["count"] += 1
        return x * 2

    # Act
    results = [inner_func(42) for _ in range(10)]
    return {"results": results, "count": state["count"]}


def test_cache_mem_concurrent_results_are_all_equal(concurrent_access_runner):
    # Arrange
    info = concurrent_access_runner
    # Act
    all_equal = all(r == 84 for r in info["results"])
    # Assert
    assert all_equal is True


def test_cache_mem_concurrent_function_executes_only_once(concurrent_access_runner):
    # Arrange
    info = concurrent_access_runner
    # Act
    count = info["count"]
    # Assert
    assert count == 1


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__)])

# EOF
