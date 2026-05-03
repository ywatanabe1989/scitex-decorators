---
name: scitex-decorators
description: |
  [WHAT] Decorator library — type-conversion (`@numpy_fn`, `@torch_fn`, `@pandas_fn`, `@xarray_fn`, `@signal_fn`), caching (`@cache_disk`, `@cache_mem`), batching (`@batch_fn` + combinators), lifecycle (`@deprecated`, `@timeout`, ...), and `@AutoOrderDecorator` for stacking.
  [WHEN] Writing functions that should accept any array type, memoize across processes, batch through GPU/memory limits, or be marked deprecated/timeout-bounded.
  [HOW] `from scitex_decorators import numpy_fn, cache_disk, batch_fn, deprecated, ...` — apply as decorators; combinators compose batching with conversion.
tags: [scitex-decorators]
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 2
  http: 0
---

> **Interfaces:** Python ⭐⭐⭐ (primary) · Skills ⭐⭐

# scitex-decorators

Four families: type-conversion, caching, batching, lifecycle.

## Type-conversion

Declare the native type; accept anything. Round-trip preserves caller's
type and (for torch) device.

```python
from scitex_decorators import numpy_fn, torch_fn, pandas_fn, xarray_fn, signal_fn

@numpy_fn
def kernel(x): return x ** 2     # x is numpy inside; return matches caller
```

## Caching

```python
from scitex_decorators import cache_disk, cache_mem

@cache_disk         # joblib-backed; survives process restart
def expensive(x): ...

@cache_mem          # in-process LRU
def hot_path(x): ...
```

Cache lives at `local_state.runtime_path("decorators", "cache")`.

## Batching

```python
from scitex_decorators import batch_fn, batch_torch_fn

@batch_fn(batch_size=256)
def per_item(x): ...

@batch_torch_fn(batch_size=64)
def gpu_item(x): ...   # batch + numpy↔torch conversion composed
```

Combinators: `batch_numpy_fn`, `batch_pandas_fn`, `numpy_batch_fn`, …
(both orderings, depending on which decorator should be outermost).

## Lifecycle

`@deprecated`, `@not_implemented`, `@timeout(seconds=N)`,
`@preserve_doc`, `@wrap`.

## AutoOrderDecorator

`@AutoOrderDecorator` resolves canonical stacking order so you don't
memorize it. `enable_auto_order()` / `disable_auto_order()`.

## Pitfalls

- `@cache_disk` above `@numpy_fn` manually: cache key includes input type — same input as numpy then torch caches twice. Use `@AutoOrderDecorator` or `@numpy_fn` outermost.
- `@signal_fn` vs `@numpy_fn` for time-series: `signal_fn` handles axis-aware conversion.
- `@cache_disk` on non-picklable returns: swap to `@cache_mem`.

See `scitex-config` for `local_state.runtime_path`; general `01_arch_06_local-state-directories.md` for cache layout policy.
