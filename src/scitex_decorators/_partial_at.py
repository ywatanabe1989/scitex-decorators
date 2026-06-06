#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""partial_at — fix one positional argument at a chosen index.

Ported from scitex-gen ``misc.py``. Standard :func:`functools.partial`
binds arguments left-to-right only; this helper lets you bind any
positional slot by index, which is occasionally useful for adapting
third-party APIs.
"""
from __future__ import annotations

from functools import wraps
from typing import Any, Callable


def partial_at(func: Callable[..., Any], index: int, value: Any) -> Callable[..., Any]:
    """Return a wrapper that always passes ``value`` at positional ``index``.

    Parameters
    ----------
    func : callable
        The function to partially apply.
    index : int
        Position at which to insert ``value`` in the eventual call.
    value : Any
        The bound positional value.

    Returns
    -------
    callable
        A new function. Calling it with positional ``rest`` and
        keyword ``kwargs`` invokes
        ``func(*rest[:index], value, *rest[index:], **kwargs)``.

    Example
    -------
    >>> def greet(greeting, name):
    ...     return f"{greeting}, {name}!"
    >>> hello = partial_at(greet, 0, "Hello")
    >>> hello("Alice")
    'Hello, Alice!'
    """

    @wraps(func)
    def result(*rest, **kwargs):
        args = []
        args.extend(rest[:index])
        args.append(value)
        args.extend(rest[index:])
        return func(*args, **kwargs)

    return result
