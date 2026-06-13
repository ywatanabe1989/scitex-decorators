#!/usr/bin/env python3
# Time-stamp: "2026-01-04 (ywatanabe)"
# File: ./tests/scitex/gen/test__cache.py

"""Tests for cache module.

The cache module provides a re-export of functools.lru_cache with maxsize=None,
providing unlimited memoization capability.
"""

from functools import lru_cache

from scitex_decorators import cache


class TestCacheBasic:
    """Test basic cache functionality."""

    def test_cache_is_lru_cache(self):
        """Verify cache is the lru_cache decorator."""
        # cache should be lru_cache with maxsize=None
        # Arrange
        # Act
        # Assert
        assert callable(cache)

    def test_cache_memoizes_function_split_1(self):
        """Test that cache properly memoizes function calls."""
        # Arrange
        call_count = 0

        @cache
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        result1 = expensive_function(5)
        # Act
        # Assert
        assert result1 == 10

    def test_cache_memoizes_function_split_2(self):
        """Test that cache properly memoizes function calls."""
        # Arrange
        call_count = 0

        @cache
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        result1 = expensive_function(5)
        result1 == 10
        # Act
        # Assert
        assert call_count == 1

    def test_cache_memoizes_function_split_3(self):
        """Test that cache properly memoizes function calls."""
        # Arrange
        call_count = 0

        @cache
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        result1 = expensive_function(5)
        result1 == 10
        call_count == 1
        result2 = expensive_function(5)
        # Act
        # Assert
        assert result2 == 10

    def test_cache_memoizes_function_split_4(self):
        """Test that cache properly memoizes function calls."""
        # Arrange
        call_count = 0

        @cache
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        result1 = expensive_function(5)
        result1 == 10
        call_count == 1
        result2 = expensive_function(5)
        result2 == 10
        # Act
        # Assert
        assert call_count == 1

    def test_cache_memoizes_function_split_5(self):
        """Test that cache properly memoizes function calls."""
        # Arrange
        call_count = 0

        @cache
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        result1 = expensive_function(5)
        result1 == 10
        call_count == 1
        result2 = expensive_function(5)
        result2 == 10
        call_count == 1
        result3 = expensive_function(10)
        # Act
        # Assert
        assert result3 == 20

    def test_cache_memoizes_function_split_6(self):
        """Test that cache properly memoizes function calls."""
        # Arrange
        call_count = 0

        @cache
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        result1 = expensive_function(5)
        result1 == 10
        call_count == 1
        result2 = expensive_function(5)
        result2 == 10
        call_count == 1
        result3 = expensive_function(10)
        result3 == 20
        # Act
        # Assert
        assert call_count == 2

    def test_cache_with_multiple_arguments_split_1(self):
        """Test cache with functions that take multiple arguments."""
        # Arrange
        call_count = 0

        @cache
        def add(a, b):
            nonlocal call_count
            call_count += 1
            return a + b
        # Act
        # Assert
        assert add(1, 2) == 3

    def test_cache_with_multiple_arguments_split_2(self):
        """Test cache with functions that take multiple arguments."""
        # Arrange
        call_count = 0

        @cache
        def add(a, b):
            nonlocal call_count
            call_count += 1
            return a + b
        add(1, 2) == 3
        # Act
        # Assert
        assert call_count == 1

    def test_cache_with_multiple_arguments_split_3(self):
        """Test cache with functions that take multiple arguments."""
        # Arrange
        call_count = 0

        @cache
        def add(a, b):
            nonlocal call_count
            call_count += 1
            return a + b
        add(1, 2) == 3
        call_count == 1
        # Act
        # Assert
        assert add(1, 2) == 3

    def test_cache_with_multiple_arguments_split_4(self):
        """Test cache with functions that take multiple arguments."""
        # Arrange
        call_count = 0

        @cache
        def add(a, b):
            nonlocal call_count
            call_count += 1
            return a + b
        add(1, 2) == 3
        call_count == 1
        add(1, 2) == 3
        # Act
        # Assert
        assert call_count == 1

    def test_cache_with_multiple_arguments_split_5(self):
        """Test cache with functions that take multiple arguments."""
        # Arrange
        call_count = 0

        @cache
        def add(a, b):
            nonlocal call_count
            call_count += 1
            return a + b
        add(1, 2) == 3
        call_count == 1
        add(1, 2) == 3
        call_count == 1
        # Act
        # Assert
        assert add(2, 1) == 3

    def test_cache_with_multiple_arguments_split_6(self):
        """Test cache with functions that take multiple arguments."""
        # Arrange
        call_count = 0

        @cache
        def add(a, b):
            nonlocal call_count
            call_count += 1
            return a + b
        add(1, 2) == 3
        call_count == 1
        add(1, 2) == 3
        call_count == 1
        add(2, 1) == 3
        # Act
        # Assert
        assert call_count == 2


class TestCacheEdgeCases:
    """Test edge cases for cache."""

    def test_cache_with_no_args_split_1(self):
        """Test cache with functions that take no arguments."""
        # Arrange
        call_count = 0

        @cache
        def get_constant():
            nonlocal call_count
            call_count += 1
            return 42
        # Act
        # Assert
        assert get_constant() == 42

    def test_cache_with_no_args_split_2(self):
        """Test cache with functions that take no arguments."""
        # Arrange
        call_count = 0

        @cache
        def get_constant():
            nonlocal call_count
            call_count += 1
            return 42
        get_constant() == 42
        # Act
        # Assert
        assert call_count == 1

    def test_cache_with_no_args_split_3(self):
        """Test cache with functions that take no arguments."""
        # Arrange
        call_count = 0

        @cache
        def get_constant():
            nonlocal call_count
            call_count += 1
            return 42
        get_constant() == 42
        call_count == 1
        # Act
        # Assert
        assert get_constant() == 42

    def test_cache_with_no_args_split_4(self):
        """Test cache with functions that take no arguments."""
        # Arrange
        call_count = 0

        @cache
        def get_constant():
            nonlocal call_count
            call_count += 1
            return 42
        get_constant() == 42
        call_count == 1
        get_constant() == 42
        # Act
        # Assert
        assert call_count == 1

    def test_cache_with_keyword_args_split_1(self):
        """Test cache with keyword arguments."""
        # Arrange
        call_count = 0

        @cache
        def greet(name, greeting='Hello'):
            nonlocal call_count
            call_count += 1
            return f'{greeting}, {name}!'
        # Act
        # Assert
        assert greet('World') == 'Hello, World!'

    def test_cache_with_keyword_args_split_2(self):
        """Test cache with keyword arguments."""
        # Arrange
        call_count = 0

        @cache
        def greet(name, greeting='Hello'):
            nonlocal call_count
            call_count += 1
            return f'{greeting}, {name}!'
        greet('World') == 'Hello, World!'
        # Act
        # Assert
        assert call_count == 1

    def test_cache_with_keyword_args_split_3(self):
        """Test cache with keyword arguments."""
        # Arrange
        call_count = 0

        @cache
        def greet(name, greeting='Hello'):
            nonlocal call_count
            call_count += 1
            return f'{greeting}, {name}!'
        greet('World') == 'Hello, World!'
        call_count == 1
        # Act
        # Assert
        assert greet('World') == 'Hello, World!'

    def test_cache_with_keyword_args_split_4(self):
        """Test cache with keyword arguments."""
        # Arrange
        call_count = 0

        @cache
        def greet(name, greeting='Hello'):
            nonlocal call_count
            call_count += 1
            return f'{greeting}, {name}!'
        greet('World') == 'Hello, World!'
        call_count == 1
        greet('World') == 'Hello, World!'
        # Act
        # Assert
        assert call_count == 1

    def test_cache_with_keyword_args_split_5(self):
        """Test cache with keyword arguments."""
        # Arrange
        call_count = 0

        @cache
        def greet(name, greeting='Hello'):
            nonlocal call_count
            call_count += 1
            return f'{greeting}, {name}!'
        greet('World') == 'Hello, World!'
        call_count == 1
        greet('World') == 'Hello, World!'
        call_count == 1
        # Act
        # Assert
        assert greet('World', greeting='Hi') == 'Hi, World!'

    def test_cache_with_keyword_args_split_6(self):
        """Test cache with keyword arguments."""
        # Arrange
        call_count = 0

        @cache
        def greet(name, greeting='Hello'):
            nonlocal call_count
            call_count += 1
            return f'{greeting}, {name}!'
        greet('World') == 'Hello, World!'
        call_count == 1
        greet('World') == 'Hello, World!'
        call_count == 1
        greet('World', greeting='Hi') == 'Hi, World!'
        # Act
        # Assert
        assert call_count == 2

    def test_cache_unlimited_size_split_1(self):
        """Test that cache has unlimited size (maxsize=None)."""
        # Arrange

        @cache
        def identity(x):
            return x
        for i in range(1000):
            identity(i)
        info = identity.cache_info()
        # Act
        # Assert
        assert info.maxsize is None

    def test_cache_unlimited_size_split_2(self):
        """Test that cache has unlimited size (maxsize=None)."""
        # Arrange

        @cache
        def identity(x):
            return x
        for i in range(1000):
            identity(i)
        info = identity.cache_info()
        info.maxsize is None
        # Act
        # Assert
        assert info.currsize == 1000


class TestCacheInfo:
    """Test cache_info functionality."""

    def test_cache_info_available_split_1(self):
        """Test that cache_info is available on decorated functions."""
        # Arrange

        @cache
        def func(x):
            return x
        func(1)
        func(2)
        func(1)
        info = func.cache_info()
        # Act
        # Assert
        assert info.hits == 1

    def test_cache_info_available_split_2(self):
        """Test that cache_info is available on decorated functions."""
        # Arrange

        @cache
        def func(x):
            return x
        func(1)
        func(2)
        func(1)
        info = func.cache_info()
        info.hits == 1
        # Act
        # Assert
        assert info.misses == 2

    def test_cache_info_available_split_3(self):
        """Test that cache_info is available on decorated functions."""
        # Arrange

        @cache
        def func(x):
            return x
        func(1)
        func(2)
        func(1)
        info = func.cache_info()
        info.hits == 1
        info.misses == 2
        # Act
        # Assert
        assert info.currsize == 2

    def test_cache_clear_call_count_equals_n_1_split_1(self):
        """Test that cache_clear works correctly."""
        # Arrange
        call_count = 0

        @cache
        def func(x):
            nonlocal call_count
            call_count += 1
            return x
        func(1)
        # Act
        # Assert
        assert call_count == 1

    def test_cache_clear_call_count_equals_n_1_split_2(self):
        """Test that cache_clear works correctly."""
        # Arrange
        call_count = 0

        @cache
        def func(x):
            nonlocal call_count
            call_count += 1
            return x
        func(1)
        call_count == 1
        func(1)
        # Act
        # Assert
        assert call_count == 1

    def test_cache_clear_call_count_equals_n_1_split_3(self):
        """Test that cache_clear works correctly."""
        # Arrange
        call_count = 0

        @cache
        def func(x):
            nonlocal call_count
            call_count += 1
            return x
        func(1)
        call_count == 1
        func(1)
        call_count == 1
        func.cache_clear()
        func(1)
        # Act
        # Assert
        assert call_count == 2


class TestCacheWithHashableTypes:
    """Test cache with various hashable types."""

    def test_cache_with_tuple_args_split_1(self):
        """Test cache with tuple arguments."""
        # Arrange

        @cache
        def process_tuple(t):
            return sum(t)
        # Act
        # Assert
        assert process_tuple((1, 2, 3)) == 6

    def test_cache_with_tuple_args_split_2(self):
        """Test cache with tuple arguments."""
        # Arrange

        @cache
        def process_tuple(t):
            return sum(t)
        process_tuple((1, 2, 3)) == 6
        # Act
        # Assert
        assert process_tuple((1, 2, 3)) == 6

    def test_cache_with_tuple_args_split_3(self):
        """Test cache with tuple arguments."""
        # Arrange

        @cache
        def process_tuple(t):
            return sum(t)
        process_tuple((1, 2, 3)) == 6
        process_tuple((1, 2, 3)) == 6
        # Act
        # Assert
        assert process_tuple((4, 5, 6)) == 15

    def test_cache_with_string_args_split_1(self):
        """Test cache with string arguments."""
        # Arrange

        @cache
        def reverse_string(s):
            return s[::-1]
        # Act
        # Assert
        assert reverse_string('hello') == 'olleh'

    def test_cache_with_string_args_split_2(self):
        """Test cache with string arguments."""
        # Arrange

        @cache
        def reverse_string(s):
            return s[::-1]
        reverse_string('hello') == 'olleh'
        # Act
        # Assert
        assert reverse_string('hello') == 'olleh'

    def test_cache_with_string_args_split_3(self):
        """Test cache with string arguments."""
        # Arrange

        @cache
        def reverse_string(s):
            return s[::-1]
        reverse_string('hello') == 'olleh'
        reverse_string('hello') == 'olleh'
        # Act
        # Assert
        assert reverse_string('world') == 'dlrow'

    def test_cache_with_none_split_1(self):
        """Test cache with None argument."""
        # Arrange

        @cache
        def handle_none(x):
            return x is None
        # Act
        # Assert
        assert handle_none(None) is True

    def test_cache_with_none_split_2(self):
        """Test cache with None argument."""
        # Arrange

        @cache
        def handle_none(x):
            return x is None
        handle_none(None) is True
        # Act
        # Assert
        assert handle_none(None) is True

    def test_cache_with_none_split_3(self):
        """Test cache with None argument."""
        # Arrange

        @cache
        def handle_none(x):
            return x is None
        handle_none(None) is True
        handle_none(None) is True
        # Act
        # Assert
        assert handle_none(0) is False


class TestCacheComparison:
    """Test that scitex_gen.cache matches functools.lru_cache behavior."""

    def test_same_behavior_as_lru_cache_split_1(self):
        """Verify cache behaves like lru_cache(maxsize=None)."""
        # Arrange
        call_count_scitex = 0
        call_count_functools = 0

        @cache
        def func_scitex(x):
            nonlocal call_count_scitex
            call_count_scitex += 1
            return x * 2

        @lru_cache(maxsize=None)
        def func_functools(x):
            nonlocal call_count_functools
            call_count_functools += 1
            return x * 2
        # Act
        # Assert
        for val in [1, 2, 3, 1, 2, 3]:
            result1 = func_scitex(val)
            result2 = func_functools(val)
            assert result1 == result2

    def test_same_behavior_as_lru_cache_split_2(self):
        """Verify cache behaves like lru_cache(maxsize=None)."""
        # Arrange
        call_count_scitex = 0
        call_count_functools = 0

        @cache
        def func_scitex(x):
            nonlocal call_count_scitex
            call_count_scitex += 1
            return x * 2

        @lru_cache(maxsize=None)
        def func_functools(x):
            nonlocal call_count_functools
            call_count_functools += 1
            return x * 2
        for val in [1, 2, 3, 1, 2, 3]:
            result1 = func_scitex(val)
            result2 = func_functools(val)
            result1 == result2
        # Act
        # Assert
        assert call_count_scitex == call_count_functools


if __name__ == "__main__":
    import os

    import pytest

    pytest.main([os.path.abspath(__file__)])

# --------------------------------------------------------------------------------
# Start of Source Code from: /home/ywatanabe/proj/scitex-code/src/scitex/gen/_cache.py
# --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-11-02 13:30:24 (ywatanabe)"
# # File: ./scitex_repo/src/scitex/gen/_cache.py
#
# from functools import lru_cache
#
# cache = lru_cache(maxsize=None)
#
#
# # EOF

# --------------------------------------------------------------------------------
# End of Source Code from: /home/ywatanabe/proj/scitex-code/src/scitex/gen/_cache.py
# --------------------------------------------------------------------------------
