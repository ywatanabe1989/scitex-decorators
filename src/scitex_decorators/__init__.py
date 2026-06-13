#!/usr/bin/env python3
"""scitex-decorators — decorator library extracted from scitex.decorators (standalone).

Includes type-conversion (numpy_fn, torch_fn, pandas_fn, xarray_fn, signal_fn),
caching (cache_disk, cache_disk_async, cache_mem), batching, deprecation,
timeout, and ordering helpers.
"""

from __future__ import annotations

try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _v

    try:
        __version__ = _v("scitex-decorators")
    except PackageNotFoundError:
        __version__ = "0.0.0+local"
    del _v, PackageNotFoundError
except ImportError:  # pragma: no cover — only on ancient Pythons
    __version__ = "0.0.0+local"
from scitex_dev import try_import_optional

from ._alternate_kwarg import alternate_kwarg
from ._auto_order import (
    AutoOrderDecorator,
    batch_fn,
    disable_auto_order,
    enable_auto_order,
    numpy_fn,
    pandas_fn,
    torch_fn,
)
from ._batch_fn import batch_fn
from ._cache._cache_disk import cache_disk
from ._cache._cache_disk_async import cache_disk_async
from ._cache._cache_mem import cache_mem
from ._cache_simple import cache
from ._combined import (
    batch_numpy_fn,
    batch_pandas_fn,
    batch_torch_fn,
    numpy_batch_fn,
    pandas_batch_fn,
    torch_batch_fn,
)
from ._converters import (
    ConversionWarning,
    is_cuda,
    is_nested_decorator,
    is_torch,
    to_numpy,
    to_torch,
)
from ._deprecated import deprecated
from ._not_implemented import not_implemented
from ._numpy_fn import numpy_fn
from ._partial_at import partial_at
from ._preserve_doc import preserve_doc
from ._signal_fn import signal_fn
from ._timeout import timeout
from ._wrap import wrap

# Heavy-extra decorators — gated via `try_import_optional`. Each public name
# stays in `__all__` regardless (Pattern A from
# `_skills/general/03_interface_01_python-api/04_lazy-imports-and-optional-deps.md`)
# so user code probes with `is None` and surfaces an installable hint.
torch_fn = try_import_optional(
    "._torch_fn",
    attr="torch_fn",
    extra="torch",
    pkg="scitex-decorators",
    package=__name__,
)
pandas_fn = try_import_optional(
    "._pandas_fn",
    attr="pandas_fn",
    extra="pandas",
    pkg="scitex-decorators",
    package=__name__,
)
xarray_fn = try_import_optional(
    "._xarray_fn",
    attr="xarray_fn",
    extra="xarray",
    pkg="scitex-decorators",
    package=__name__,
)

__all__ = [
    "__version__",
    "AutoOrderDecorator",
    "ConversionWarning",
    "alternate_kwarg",
    "batch_fn",
    "batch_fn",
    "batch_numpy_fn",
    "batch_pandas_fn",
    "batch_torch_fn",
    "cache",
    "cache_disk",
    "cache_disk_async",
    "cache_mem",
    "deprecated",
    "disable_auto_order",
    "enable_auto_order",
    "is_cuda",
    "is_nested_decorator",
    "is_torch",
    "not_implemented",
    "numpy_batch_fn",
    "numpy_fn",
    "numpy_fn",
    "pandas_batch_fn",
    "pandas_fn",
    "pandas_fn",
    "partial_at",
    "preserve_doc",
    "signal_fn",
    "timeout",
    "to_numpy",
    "to_torch",
    "torch_batch_fn",
    "torch_fn",
    "torch_fn",
    "wrap",
    "xarray_fn",
]
