#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-11-02 13:30:41 (ywatanabe)"
# File: ./src/scitex_decorators/_alternate_kwarg.py
"""Tiny kwargs-normalisation helper.

Ported from scitex_gen._introspect._alternate_kwarg (Phase B retirement
wave). Promotes ``alternate_key`` into ``primary_key`` if the primary is
absent or falsy. Useful for backward-compatible parameter renames inside
function bodies.
"""

from __future__ import annotations


def alternate_kwarg(kwargs, primary_key, alternate_key):
    """Promote ``alternate_key`` -> ``primary_key`` in kwargs.

    Pops ``alternate_key`` from *kwargs* (default ``None``) and sets
    ``kwargs[primary_key]`` to the existing primary value or the popped
    alternate, whichever is truthy first.

    Returns the same dict (mutated in place).

    Example
    -------
    >>> alternate_kwarg({"new": None, "old": 5}, "new", "old")
    {'new': 5}
    """
    alternate_value = kwargs.pop(alternate_key, None)
    kwargs[primary_key] = kwargs.get(primary_key) or alternate_value
    return kwargs


# EOF
