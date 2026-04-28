#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2025-12-09 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-code/src/scitex/decorators/_cache_disk.py
# ----------------------------------------
from __future__ import annotations

import os

__FILE__ = "./src/scitex/decorators/_cache_disk.py"
__DIR__ = os.path.dirname(__FILE__)
# ----------------------------------------

import functools
from pathlib import Path
from scitex_config._ecosystem import local_state


def _resolve_cache_dir() -> str:
    """Return cache directory.

    Resolution order:
      1. ``scitex.config.get_paths().function_cache`` if available.
      2. ``$SCITEX_CACHE_DIR/function_cache`` if set.
      3. ``$SCITEX_DIR/decorators/runtime/cache`` (defaults to
         ``~/.scitex/decorators/runtime/cache``).
    """
    try:
        from scitex.config import get_paths

        return str(get_paths().function_cache)
    except Exception:
        env = os.environ.get("SCITEX_CACHE_DIR")
        if env:
            return str(Path(env) / "function_cache")
        base = Path(os.environ.get("SCITEX_DIR", Path.home() / ".scitex"))
        return str(base / "decorators" / "runtime" / "cache")


def cache_disk(func):
    """Disk caching decorator that uses joblib.Memory.

    joblib is lazy-imported to keep ``import scitex.decorators`` (and the
    transitive ``import scitex.io`` chain) usable on venvs without joblib
    installed. Without lazy-import, the eager ``from joblib import Memory``
    raised ``ModuleNotFoundError: No module named 'joblib'`` at import
    time and broke any caller of scitex.io that didn't need caching at
    all (todo#442, same class as #441 / #279).

    Usage:
        @cache_disk
        def expensive_function(x):
            return x ** 2
    """
    cache_dir = _resolve_cache_dir()
    from joblib import Memory as _Memory  # lazy: see todo#442

    memory = _Memory(cache_dir, verbose=0)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cached_func = memory.cache(func)
        return cached_func(*args, **kwargs)

    return wrapper


# EOF
