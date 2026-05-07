# scitex-decorators

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-blue-cropped.png" alt="SciTeX" width="400">
  </a>
</p>

<p align="center"><b>Decorator library — type conversion (numpy/torch/pandas/xarray), caching, batching, lifecycle.</b></p>

<p align="center">
  <a href="https://scitex-decorators.readthedocs.io/">Full Documentation</a> · <code>pip install scitex-decorators</code>
</p>

<!-- scitex-badges:start -->
<p align="center">
  <a href="https://pypi.org/project/scitex-decorators/"><img src="https://img.shields.io/pypi/v/scitex-decorators.svg" alt="PyPI"></a>
  <a href="https://pypi.org/project/scitex-decorators/"><img src="https://img.shields.io/pypi/pyversions/scitex-decorators.svg" alt="Python"></a>
  <a href="https://github.com/ywatanabe1989/scitex-decorators/actions/workflows/test.yml"><img src="https://github.com/ywatanabe1989/scitex-decorators/actions/workflows/test.yml/badge.svg" alt="Tests"></a>
  <a href="https://github.com/ywatanabe1989/scitex-decorators/actions/workflows/install-test.yml"><img src="https://github.com/ywatanabe1989/scitex-decorators/actions/workflows/install-test.yml/badge.svg" alt="Install Test"></a>
  <a href="https://codecov.io/gh/ywatanabe1989/scitex-decorators"><img src="https://codecov.io/gh/ywatanabe1989/scitex-decorators/graph/badge.svg" alt="Coverage"></a>
  <a href="https://scitex-decorators.readthedocs.io/en/latest/"><img src="https://readthedocs.org/projects/scitex-decorators/badge/?version=latest" alt="Docs"></a>
  <a href="https://www.gnu.org/licenses/agpl-3.0"><img src="https://img.shields.io/badge/license-AGPL_v3-blue.svg" alt="License: AGPL v3"></a>
</p>
<!-- scitex-badges:end -->

---

## Installation

```bash
pip install scitex-decorators              # core (numpy only)
pip install "scitex-decorators[caching]"   # + joblib for cache_disk
pip install "scitex-decorators[torch]"     # + torch_fn / batch_torch_fn
pip install "scitex-decorators[all]"       # everything
```

## Architecture

```mermaid
flowchart LR
    AO["@auto_order"] --> CV["@*_fn converters"]
    CV --> NP["@numpy_fn"]
    CV --> PD["@pandas_fn"]
    CV --> XR["@xarray_fn"]
    CV --> TR["@torch_fn"]
    CV --> SG["@signal_fn"]
    BF["@batch_fn"] --> CV
    CD["@cache_disk<br/>(joblib)"] -.-> NP & PD & TR
    PD2["@preserve_doc"] -.-> NP & PD & TR & XR & SG
    DEP["@deprecated"] -.-> NP & PD & TR
    TO["@timeout"] -.-> CV
    NI["@not_implemented"] -.-> CV
    CO["@combined<br/>(stack of @*_fn)"] --> NP & PD & TR
```

Each `@<type>_fn` decorator converts inputs to the named type, calls the
wrapped function, then converts back to the caller's original type. The
diagram above shows how `_combined.py`, `_auto_order.py`, and the
caching/timeout decorators compose around the converter family.

## Quick Start

```python
import scitex_decorators as dec

@dec.numpy_fn
def kernel(x):
    return x ** 2     # x is numpy inside; return matches caller's type

@dec.cache_disk
def expensive(x): ...
```

## 1 Interfaces

<details open>
<summary><strong>Python API</strong></summary>

<br>

```python
import scitex_decorators as dec

# Type-conversion decorators
@dec.numpy_fn  ; @dec.torch_fn  ; @dec.pandas_fn  ; @dec.xarray_fn
@dec.signal_fn

# Caching (joblib for disk, dict for mem)
@dec.cache_disk        ; @dec.cache_disk_async    ; @dec.cache_mem

# Batching
@dec.batch_fn          ; @dec.batch_numpy_fn / batch_torch_fn / batch_pandas_fn

# Lifecycle
@dec.deprecated(reason="…")
@dec.not_implemented
@dec.preserve_doc
@dec.timeout(seconds=10)
@dec.wrap

# Auto-ordering machinery
dec.enable_auto_order() ; dec.disable_auto_order()

# Conversion helpers
dec.to_numpy(x) ; dec.to_torch(x)
dec.is_torch(x) ; dec.is_cuda(x)
```

</details>

## Cache directory resolution

`cache_disk` / `cache_disk_async` resolve the cache dir in this order:

1. `scitex.config.get_paths().function_cache` (only if scitex is installed)
2. `${SCITEX_CACHE_DIR}/function_cache`
3. `${XDG_CACHE_HOME}/scitex-decorators/function_cache`
4. `~/.cache/scitex-decorators/function_cache`

So the package works without the umbrella scitex installed.

## Demo

```mermaid
flowchart LR
    C["caller passes pandas.DataFrame"] --> D["@numpy_fn"]
    D --> N["function body sees numpy.ndarray"]
    N --> R["function returns numpy.ndarray"]
    R --> O["caller receives pandas.DataFrame<br/>(original type restored)"]
```

## Status

Standalone fork of `scitex.decorators`. Zero scitex.* runtime deps. The
umbrella package's `scitex.decorators` import path is preserved via a
`sys.modules`-alias bridge.

## Part of SciTeX

`scitex-decorators` is part of [**SciTeX**](https://scitex.ai). Install via
the umbrella with `pip install scitex[decorators]` to use as
`scitex.decorators` (Python) or `scitex decorators ...` (CLI).

>Four Freedoms for Research
>
>0. The freedom to **run** your research anywhere — your machine, your terms.
>1. The freedom to **study** how every step works — from raw data to final manuscript.
>2. The freedom to **redistribute** your workflows, not just your papers.
>3. The freedom to **modify** any module and share improvements with the community.
>
>AGPL-3.0 — because we believe research infrastructure deserves the same freedoms as the software it runs on.

## License

AGPL-3.0-only (see [LICENSE](./LICENSE)).

---

<p align="center">
  <a href="https://scitex.ai" target="_blank"><img src="docs/scitex-icon-navy-inverted.png" alt="SciTeX" width="40"/></a>
</p>
