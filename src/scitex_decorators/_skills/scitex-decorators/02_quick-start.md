---
description: |
  [TOPIC] scitex-decorators Quick start
  [DETAILS] Type-conversion (numpy_fn / torch_fn), caching (cache_disk / cache_mem), batching (batch_fn), lifecycle (deprecated / timeout).
tags: [scitex-decorators-quick-start]
---

# Quick Start

## Type-conversion — write once, accept anything

```python
from scitex_decorators import numpy_fn

@numpy_fn
def kernel(x):
    """x is numpy inside; return value is converted back to caller's type."""
    return x ** 2
```

`@torch_fn`, `@pandas_fn`, `@xarray_fn`, `@signal_fn` follow the same
pattern. Round-trip preserves caller's type and (for torch) device.

## Caching

```python
from scitex_decorators import cache_disk, cache_mem

@cache_disk     # joblib-backed; survives process restart
def expensive(x): ...

@cache_mem      # in-process LRU
def hot_path(x): ...
```

## Batching through GPU/memory limits

```python
from scitex_decorators import batch_fn, batch_torch_fn

@batch_fn(batch_size=256)
def per_item(x): ...

@batch_torch_fn(batch_size=64)
def gpu_item(x):           # batching + numpy↔torch composed
    ...
```

## Lifecycle

```python
from scitex_decorators import deprecated, not_implemented, timeout

@deprecated(reason="renamed", version="2.0", replacement="new_fn")
def old_fn(x): ...

@timeout(seconds=10)
def maybe_slow(x): ...
```

## Auto-order to skip stacking surprises

```python
from scitex_decorators import AutoOrderDecorator

@AutoOrderDecorator                # picks canonical decorator order
@cache_disk
@numpy_fn
def f(x): ...
```

See SKILL.md "Pitfalls" for why this matters.

## Next

- [03_python-api.md](03_python-api.md) — full surface
- [SKILL.md](SKILL.md) — four families overview + pitfalls
