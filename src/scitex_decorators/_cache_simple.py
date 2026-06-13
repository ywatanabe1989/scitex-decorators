#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-11-02 13:30:24 (ywatanabe)"
# File: ./src/scitex_decorators/_cache_simple.py
"""Simple unbounded `lru_cache` alias.

Ported from scitex_gen._introspect._cache (Phase B retirement wave).
This is the simple ``functools.lru_cache(maxsize=None)`` alias that
scitex-gen exposed as ``cache``. The richer disk / memory cache
decorators in this package live in ``_cache/`` (note the directory).
"""

from __future__ import annotations

from functools import lru_cache

# Pre-bound, unbounded LRU cache decorator. Use as ``@cache``.
cache = lru_cache(maxsize=None)


# EOF
