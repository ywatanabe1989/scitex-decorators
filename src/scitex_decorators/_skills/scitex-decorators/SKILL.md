---
name: scitex-decorators
description: Decorator library for SciTeX scientific code. Type-conversion family (`@numpy_fn`, `@torch_fn`, `@pandas_fn`, `@xarray_fn`, `@signal_fn`) lets a function declare its native array type and accept any of the others — the decorator converts on entry and back on exit, including `cuda` round-trips. Caching family (`@cache_disk`, `@cache_disk_async`, `@cache_mem`) memoizes pure functions. `@batch_fn` chunks large inputs through GPU/memory limits; combinator decorators (`batch_numpy_fn`, `batch_torch_fn`, …) compose batching with type conversion. Lifecycle: `@deprecated`, `@not_implemented`, `@timeout`, `@preserve_doc`, `@wrap`. `@AutoOrderDecorator` resolves stacking order so users don't memorise the right decorator ordering. Drop-in replacement for hand-rolled `if isinstance(x, torch.Tensor): x = x.cpu().numpy()` boilerplate, ad-hoc functools.lru_cache that doesn't survive process restart, and per-script for-loop GPU batching.
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 2
  hook: 0
  http: 0
tags: [scitex-decorators, scitex-package, decorators, numpy, torch, pandas, caching]
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
