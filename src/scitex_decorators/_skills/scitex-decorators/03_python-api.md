---
description: |
  [TOPIC] scitex-decorators Python API
  [DETAILS] Public callables grouped — type-conversion, caching, batching, lifecycle, ordering, helpers.
tags: [scitex-decorators-python-api]
---

# Python API

## Imports

```python
from scitex_decorators import (
    # Type conversion
    numpy_fn, torch_fn, pandas_fn, xarray_fn, signal_fn,
    # Caching
    cache_disk, cache_disk_async, cache_mem,
    # Batching
    batch_fn, batch_numpy_fn, batch_pandas_fn, batch_torch_fn,
    numpy_batch_fn, pandas_batch_fn, torch_batch_fn,
    # Lifecycle
    deprecated, not_implemented, timeout, preserve_doc, wrap,
    # Ordering
    AutoOrderDecorator, enable_auto_order, disable_auto_order,
    # Conversion helpers
    to_numpy, to_torch,
    is_cuda, is_torch, is_nested_decorator,
    ConversionWarning,
)
```

## Type-conversion decorators

| Decorator    | Native type inside | Notes                        |
|--------------|--------------------|------------------------------|
| `@numpy_fn`  | `numpy.ndarray`    | always available             |
| `@torch_fn`  | `torch.Tensor`     | needs `[torch]` extra        |
| `@pandas_fn` | `pandas.DataFrame` | needs `[pandas]` extra       |
| `@xarray_fn` | `xarray.DataArray` | needs `[xarray]` extra       |
| `@signal_fn` | numpy + axis-aware | for time-series              |

## Caching

| Decorator           | Backend        | Survives restart? |
|---------------------|----------------|-------------------|
| `@cache_disk`       | joblib         | yes               |
| `@cache_disk_async` | joblib (async) | yes               |
| `@cache_mem`        | LRU in-process | no                |

Cache lives at `local_state.runtime_path("decorators", "cache")`.

## Batching

`@batch_fn(batch_size=N)` slices the input, calls the wrapped function
per batch, and concatenates outputs. The combinators
(`batch_numpy_fn`, `numpy_batch_fn`, `batch_torch_fn`, …) compose batching
with type-conversion in both stacking orders, so you don't need to
worry about which goes outermost.

## Lifecycle

| Decorator           | Purpose                                   |
|---------------------|-------------------------------------------|
| `@deprecated(...)`  | Emit `DeprecationWarning` on call         |
| `@not_implemented`  | Raise `NotImplementedError` on call       |
| `@timeout(seconds)` | Raise on timeout                          |
| `@preserve_doc`     | Preserve docstring through other wrappers |
| `@wrap`             | functools.wraps with extra hygiene        |

## Ordering

`@AutoOrderDecorator` resolves the canonical stacking order so you
don't need to memorize which conversion goes outside the cache.
`enable_auto_order()` / `disable_auto_order()` toggle the global
default.

## Conversion helpers

`to_numpy(x)`, `to_torch(x, device=...)` — explicit conversions.
`is_cuda(t)`, `is_torch(x)`, `is_nested_decorator()`, plus
`ConversionWarning` for use in your own code.

## Two import paths

```python
import scitex_decorators        # standalone
import scitex.decorators        # umbrella (requires `pip install scitex`)
```
