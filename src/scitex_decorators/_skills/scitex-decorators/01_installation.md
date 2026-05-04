---
description: |
  [TOPIC] scitex-decorators Installation
  [DETAILS] pip install scitex-decorators with optional [caching], [pandas], [torch], [xarray], [all] extras for the decorators that need those libraries.
tags: [scitex-decorators-installation]
---

# Installation

## Standard

```bash
pip install scitex-decorators
```

Pure-Python core. Type-conversion / batching / lifecycle decorators all
work out-of-the-box; the type-conversion decorators that target a
specific library (`@torch_fn`, `@pandas_fn`, `@xarray_fn`) only become
useful once that library is installed.

## Optional extras

| Extra      | Adds      | Why                                           |
|------------|-----------|-----------------------------------------------|
| `caching`  | joblib    | enable `@cache_disk` / `@cache_disk_async`    |
| `pandas`   | pandas    | enable `@pandas_fn` round-trips               |
| `torch`    | torch     | enable `@torch_fn`, `@batch_torch_fn`         |
| `xarray`   | xarray    | enable `@xarray_fn`                            |
| `all`      | all above |                                                |

```bash
pip install 'scitex-decorators[caching,torch]'
pip install 'scitex-decorators[all]'
```

## Verify

```bash
python -c "import scitex_decorators; print(scitex_decorators.__version__)"
python -c "from scitex_decorators import numpy_fn, batch_fn, deprecated, timeout; print('ok')"
```

## Editable install (development)

```bash
git clone https://github.com/ywatanabe1989/scitex-decorators
cd scitex-decorators
pip install -e '.[dev]'
```
