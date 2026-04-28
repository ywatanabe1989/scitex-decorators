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
canonical-location: scitex-decorators/src/scitex_decorators/_skills/scitex-decorators/SKILL.md
tags: [scitex-decorators, scitex-package, decorators, numpy, torch, pandas, caching]
---

> **Interfaces:** Python ⭐⭐⭐ (primary) · CLI — · MCP — · Skills ⭐⭐ · Hook — · HTTP —

# scitex-decorators

Decorator library covering the four common scientific-Python pain
points: array-type conversion, caching, batching, and lifecycle.

## Type-conversion family

Declare what your function expects natively; accept anything.

```python
from scitex_decorators import numpy_fn, torch_fn, pandas_fn, xarray_fn, signal_fn

@numpy_fn
def my_kernel(x):           # x is guaranteed numpy.ndarray inside
    return x ** 2           # whatever you return is converted back
                            # to the caller's type

@torch_fn
def gpu_kernel(x):          # x is on caller's device + dtype; nested
    return x.relu()         # torch_fn calls don't double-convert
```

Round-trip rules: caller passes torch → numpy_fn → numpy in, **torch
out** (matches caller). cuda preserved.

## Caching family

```python
from scitex_decorators import cache_disk, cache_mem, cache_disk_async

@cache_disk          # joblib-backed; survives process restart
def expensive(x): ...

@cache_mem           # in-process LRU with explicit invalidation
def hot_path(x): ...
```

Cache lives under `local_state.runtime_path("decorators", "cache")`
(`$SCITEX_DIR/decorators/runtime/cache/`).

## Batching

```python
from scitex_decorators import batch_fn, batch_torch_fn

@batch_fn(batch_size=256)
def per_item(x): ...        # called with the *batched* input; you
                            # write the inner loop / matmul

@batch_torch_fn(batch_size=64)
def per_item_gpu(x): ...    # batch + numpy↔torch conversion composed
```

Combinator family (`batch_numpy_fn`, `batch_pandas_fn`,
`numpy_batch_fn`, …) lets you express both orderings depending on
which decorator's frame you want as outermost.

## Lifecycle

- `@deprecated(reason="...", since="0.5.0")` — emits warning on call
- `@not_implemented` — raises `NotImplementedError` with a clean
  signature
- `@timeout(seconds=30)` — kills slow calls
- `@preserve_doc` — copies wrapped function's docstring/signature onto
  a wrapper
- `@wrap` — minimal wrapper utility for ad-hoc decoration

## AutoOrderDecorator

Stacking type-conversion + batching + caching by hand is error-prone
(does cache see numpy or torch?). `@AutoOrderDecorator` resolves the
canonical order so you don't memorise it:

```python
from scitex_decorators import AutoOrderDecorator, enable_auto_order

enable_auto_order()
# Now writing @numpy_fn @batch_fn @cache_disk works regardless of
# the order you wrote them in source.
```

Disable per-call with `disable_auto_order()` if you need the manual
order back.

## When to use

- ✅ A pure numerical function that should accept numpy or torch
  inputs
- ✅ Expensive function calls that should survive process restart
  (`@cache_disk`)
- ✅ Per-item logic that needs GPU-batch wrapping
- ❌ I/O functions — cache_disk uses pickle; pickle the result, not
  the file handle
- ❌ Functions with random state — cache the seed too, or use
  `@cache_mem` with explicit invalidation

## Common mistakes

- **Stacking @cache_disk above @numpy_fn manually**: cache key
  includes the input array's *type* — pass numpy on call N, torch on
  call N+1, and you cache twice. Use `@AutoOrderDecorator` or stack
  `@numpy_fn` outermost.
- **Forgetting `signal_fn` for time-series**: `@signal_fn` handles
  axis-aware conversion (channel-first vs sample-first) that
  `@numpy_fn` doesn't.
- **`@cache_disk` on functions that return non-picklable objects**:
  swap to `@cache_mem` or restructure to return raw arrays.

## See also

- `scitex-config` — `local_state.runtime_path` is where the cache
  directory comes from
- General skill `01_arch_06_local-state-directories.md` — cache
  layout policy

<!-- EOF -->
