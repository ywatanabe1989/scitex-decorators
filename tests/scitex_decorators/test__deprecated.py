#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: tests/scitex_decorators/test__deprecated.py

"""Tests for the ``deprecated`` decorator.

The decorator emits a ``DeprecationWarning`` of the form
``"<func_name> is deprecated: <reason>"`` and then calls the wrapped
function, returning its result unchanged.

Each test verifies exactly one behavior using real warning capture
(PA-306: no mocks) and follows the Arrange / Act / Assert structure
(PA-307).
"""

from __future__ import annotations

import functools
import warnings

import pytest

# Required for scitex_decorators module
pytest.importorskip("tqdm")

from scitex_decorators import deprecated


# ---------------------------------------------------------------------------
# Decorator export
# ---------------------------------------------------------------------------


def test_deprecated_decorator_is_callable_export():
    # Arrange
    decorator_factory = deprecated
    # Act
    is_callable = callable(decorator_factory)
    # Assert
    assert is_callable


# ---------------------------------------------------------------------------
# Return-value preservation
# ---------------------------------------------------------------------------


def test_deprecated_preserves_simple_return_value():
    # Arrange
    @deprecated("This function is old")
    def old_function(x):
        return x * 2

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = old_function(5)
    # Assert
    assert observed == 10


def test_deprecated_preserves_return_value_without_reason():
    # Arrange
    @deprecated()
    def no_reason_function():
        return "test"

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = no_reason_function()
    # Assert
    assert observed == "test"


def test_deprecated_preserves_return_value_with_explicit_none_reason():
    # Arrange
    @deprecated(None)
    def none_reason_function():
        return "test"

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = none_reason_function()
    # Assert
    assert observed == "test"


def test_deprecated_preserves_return_value_with_positional_and_keyword_args():
    # Arrange
    @deprecated("Use new_math_function")
    def old_math_function(a, b, c=10):
        return a + b + c

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = old_math_function(1, 2, c=3)
    # Assert
    assert observed == 6


def test_deprecated_preserves_return_value_with_varargs_and_kwargs():
    # Arrange
    @deprecated("Flexible argument function deprecated")
    def flexible_function(*args, **kwargs):
        return sum(args) + sum(kwargs.values())

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = flexible_function(1, 2, 3, x=4, y=5)
    # Assert
    assert observed == 15


def test_deprecated_preserves_list_return_value():
    # Arrange
    @deprecated("Returns list")
    def return_list():
        return [1, 2, 3]

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = return_list()
    # Assert
    assert observed == [1, 2, 3]


def test_deprecated_preserves_dict_return_value():
    # Arrange
    @deprecated("Returns dict")
    def return_dict():
        return {"key": "value"}

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = return_dict()
    # Assert
    assert observed == {"key": "value"}


def test_deprecated_preserves_none_return_value():
    # Arrange
    @deprecated("Returns None")
    def return_none():
        return None

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = return_none()
    # Assert
    assert observed is None


def test_deprecated_preserves_tuple_return_value():
    # Arrange
    @deprecated("Returns tuple")
    def return_tuple():
        return (1, 2, 3)

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = return_tuple()
    # Assert
    assert observed == (1, 2, 3)


def test_deprecated_preserves_generator_output_sequence():
    # Arrange
    @deprecated("Generator function deprecated")
    def deprecated_generator(n):
        for i in range(n):
            yield i * 2

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = list(deprecated_generator(3))
    # Assert
    assert observed == [0, 2, 4]


# ---------------------------------------------------------------------------
# Warning emission
# ---------------------------------------------------------------------------


def test_deprecated_emits_deprecation_warning_category():
    # Arrange
    @deprecated("Category check")
    def some_function():
        return None

    # Act
    ctx = pytest.warns(DeprecationWarning)
    # Assert
    with ctx:
        some_function()


def test_deprecated_warning_names_decorated_function():
    # Arrange
    @deprecated("Some reason")
    def specifically_named_function():
        return None

    # Act
    ctx = pytest.warns(
        DeprecationWarning, match="specifically_named_function is deprecated"
    )
    # Assert
    with ctx:
        specifically_named_function()


def test_deprecated_warning_includes_reason_text():
    # Arrange
    @deprecated("This function is old")
    def old_function():
        return None

    # Act
    ctx = pytest.warns(DeprecationWarning, match="This function is old")
    # Assert
    with ctx:
        old_function()


def test_deprecated_warning_uses_none_literal_when_no_reason_supplied():
    # Arrange
    @deprecated()
    def no_reason_function():
        return None

    # Act
    ctx = pytest.warns(
        DeprecationWarning, match="no_reason_function is deprecated: None"
    )
    # Assert
    with ctx:
        no_reason_function()


def test_deprecated_warning_uses_none_literal_when_reason_is_explicit_none():
    # Arrange
    @deprecated(None)
    def none_reason_function():
        return None

    # Act
    ctx = pytest.warns(
        DeprecationWarning, match="none_reason_function is deprecated: None"
    )
    # Assert
    with ctx:
        none_reason_function()


def test_deprecated_warning_includes_complex_multi_sentence_reason():
    # Arrange
    complex_reason = (
        "Use new_function() instead. This will be removed in v2.0. "
        "See documentation at example.com"
    )

    @deprecated(complex_reason)
    def complex_function():
        return None

    # Act
    ctx = pytest.warns(
        DeprecationWarning, match="See documentation at example.com"
    )
    # Assert
    with ctx:
        complex_function()


def test_deprecated_warning_handles_unicode_reason_text():
    # Arrange
    unicode_reason = "Funcao obsoleta — use funcao_nova()"

    @deprecated(unicode_reason)
    def unicode_function():
        return None

    # Act
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        unicode_function()
    # Assert
    assert unicode_reason in str(captured[0].message)


def test_deprecated_warning_carries_very_long_reason_text():
    # Arrange
    long_reason = (
        "This is a very long deprecation reason that explains in great detail "
        "why this function is deprecated and what alternatives should be used. "
    ) * 10

    @deprecated(long_reason)
    def long_reason_function():
        return None

    # Act
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        long_reason_function()
    # Assert
    assert long_reason in str(captured[0].message)


def test_deprecated_warning_handles_special_characters_in_reason():
    # Arrange
    special_reason = "Use new_func() -> str | None instead. Cost: $0.00"

    @deprecated(special_reason)
    def special_chars_function():
        return None

    # Act
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        special_chars_function()
    # Assert
    assert special_reason in str(captured[0].message)


def test_deprecated_emits_one_warning_per_invocation():
    # Arrange
    @deprecated("Multi-call test")
    def multi_call_function():
        return "called"

    # Act
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        for _ in range(3):
            multi_call_function()
    # Assert
    assert len(captured) == 3


# ---------------------------------------------------------------------------
# Function metadata
# ---------------------------------------------------------------------------


def test_deprecated_preserves_wrapped_function_name():
    # Arrange
    @deprecated("Function with name")
    def documented_function(x, y=5):
        return x + y

    # Act
    observed_name = documented_function.__name__
    # Assert
    assert observed_name == "documented_function"


def test_deprecated_preserves_wrapped_function_docstring():
    # Arrange
    @deprecated("Function with docs")
    def documented_function(x, y=5):
        """This function adds two numbers."""
        return x + y

    # Act
    observed_doc = documented_function.__doc__
    # Assert
    assert "adds two numbers" in observed_doc


def test_deprecated_sets_dunder_wrapped_attribute():
    # Arrange
    @deprecated("Function with wrapped")
    def documented_function(x, y=5):
        return x + y

    # Act
    has_wrapped = hasattr(documented_function, "__wrapped__")
    # Assert
    assert has_wrapped


# ---------------------------------------------------------------------------
# Exception propagation
# ---------------------------------------------------------------------------


def test_deprecated_propagates_exception_from_wrapped_body():
    # Arrange
    @deprecated("This error function is deprecated")
    def error_function():
        raise ValueError("Test error")

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ctx = pytest.raises(ValueError, match="Test error")
    # Assert
    with ctx:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            error_function()


def test_deprecated_still_emits_warning_when_wrapped_raises():
    # Arrange
    @deprecated("This error function is deprecated")
    def error_function():
        raise ValueError("Test error")

    # Act
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        try:
            error_function()
        except ValueError:
            pass
    # Assert
    assert any("error_function is deprecated" in str(w.message) for w in captured)


# ---------------------------------------------------------------------------
# Class / method support
# ---------------------------------------------------------------------------


def test_deprecated_preserves_instance_method_return_value():
    # Arrange
    class Owner:
        @deprecated("Method is deprecated")
        def old_method(self, value):
            return value * 2

    owner = Owner()
    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = owner.old_method(5)
    # Assert
    assert observed == 10


def test_deprecated_warning_names_instance_method_call():
    # Arrange
    class Owner:
        @deprecated("Method is deprecated")
        def old_method(self, value):
            return value * 2

    owner = Owner()
    # Act
    ctx = pytest.warns(DeprecationWarning, match="old_method is deprecated")
    # Assert
    with ctx:
        owner.old_method(5)


def test_deprecated_preserves_static_method_return_value():
    # Arrange
    class Owner:
        @deprecated("Static method deprecated")
        @staticmethod
        def old_static_method(value):
            return value * 3

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = Owner.old_static_method(5)
    # Assert
    assert observed == 15


def test_deprecated_preserves_class_method_return_value():
    # Arrange
    class Owner:
        @classmethod
        @deprecated("Class method deprecated")
        def old_class_method(cls, value):
            return value * 4

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = Owner.old_class_method(5)
    # Assert
    assert observed == 20


# ---------------------------------------------------------------------------
# Decorator stacking
# ---------------------------------------------------------------------------


def test_deprecated_composes_with_outer_decorator_correctly():
    # Arrange
    def double_result(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) * 2

        return wrapper

    @deprecated("Multi-decorator test")
    @double_result
    def multi_decorated_function(x):
        return x + 1

    # Act
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        observed = multi_decorated_function(5)
    # Assert
    assert observed == 12


# ---------------------------------------------------------------------------
# Function name handling
# ---------------------------------------------------------------------------


def test_deprecated_warning_names_private_function():
    # Arrange
    @deprecated("Special name test")
    def _private_function():
        return "private"

    # Act
    ctx = pytest.warns(DeprecationWarning, match="_private_function is deprecated")
    # Assert
    with ctx:
        _private_function()


def test_deprecated_warning_names_function_with_digits():
    # Arrange
    @deprecated("Number name test")
    def func_2():
        return "numbered"

    # Act
    ctx = pytest.warns(DeprecationWarning, match="func_2 is deprecated")
    # Assert
    with ctx:
        func_2()


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__)])

# EOF
