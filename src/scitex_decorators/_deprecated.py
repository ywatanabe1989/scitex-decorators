#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: /home/ywatanabe/proj/scitex-decorators/src/scitex_decorators/_deprecated.py

"""Thin re-export of the canonical ``@deprecated`` decorator from scitex-compat.

Per SOC.md (SSOT section), scitex-compat owns the ``deprecated`` impl.
scitex-decorators keeps the public ``from scitex_decorators import deprecated``
surface for backward compatibility, but the implementation lives in
scitex-compat — a zero-runtime-dep package that any Layer 0 leaf
(scitex-types / scitex-path / scitex-logging / scitex-config / scitex-dev)
can depend on without dragging numpy / tqdm into their install.

Long-term migration: prefer ``from scitex_compat import deprecated``.
"""

from __future__ import annotations

from scitex_compat import deprecated

__all__ = ["deprecated"]
