#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scitex_decorators.partial_at."""
from __future__ import annotations

from scitex_decorators import partial_at


def greet(greeting, name):
    return f"{greeting}, {name}!"


def three_args(a, b, c):
    return (a, b, c)


class TestPartialAt:
    def test_bind_first_positional(self):
        hello = partial_at(greet, 0, "Hello")
        assert hello("Alice") == "Hello, Alice!"
        assert hello("Bob") == "Hello, Bob!"

    def test_bind_middle_positional(self):
        f = partial_at(three_args, 1, "B")
        assert f("A", "C") == ("A", "B", "C")

    def test_bind_last_positional(self):
        f = partial_at(three_args, 2, "C")
        assert f("A", "B") == ("A", "B", "C")

    def test_kwargs_pass_through(self):
        def keyword_fn(a, b, *, mode="x"):
            return (a, b, mode)
        f = partial_at(keyword_fn, 0, "A")
        assert f("B", mode="y") == ("A", "B", "y")

    def test_wraps_preserves_name(self):
        hello = partial_at(greet, 0, "Hi")
        assert hello.__name__ == "greet"
