"""Quickstart for scitex_decorators.

Demonstrates `@cache_mem`, `@numpy_fn` (transparent torch->numpy bridging),
and `@deprecated`.
"""

import warnings

import numpy as np

import scitex_decorators as sd


@sd.cache_mem
def slow_square_sum(n: int) -> int:
    # Pretend this is expensive
    return sum(i * i for i in range(n))


@sd.numpy_fn
def standardize(x):
    """Z-score along the last axis. Accepts np.ndarray or torch.Tensor."""
    return (x - x.mean(axis=-1, keepdims=True)) / x.std(axis=-1, keepdims=True)


@sd.deprecated(reason="use standardize() instead")
def zscore(x):
    return standardize(x)


def main() -> int:
    # Memoised: first call computes, second is a cache hit
    a = slow_square_sum(10000)
    b = slow_square_sum(10000)
    print(f"slow_square_sum(10000) = {a} (cached: {a == b})")

    # numpy_fn accepts torch tensors transparently if torch is available.
    # The decorator lazily imports torch during arg-conversion; without the
    # [torch] extra (CI's default install) that import raises
    # ModuleNotFoundError. Skip the standardize block in that case.
    arr = np.arange(12, dtype=np.float64).reshape(3, 4)
    try:
        out = standardize(arr)
    except ModuleNotFoundError as e:
        print(f"standardize unavailable ({e}); skipping torch-decorated path.")
        return 0
    print(f"standardize numpy in -> shape={out.shape}, mean≈{out.mean():.2e}")

    try:
        import torch

        t = torch.arange(12, dtype=torch.float64).reshape(3, 4)
        out_t = standardize(t)
        print(
            f"standardize torch in -> type={type(out_t).__name__}, mean≈{float(out_t.mean()):.2e}"
        )
    except ImportError:
        print("torch not installed; skipping torch path")

    # deprecated: emits a DeprecationWarning but still runs
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        zscore(arr)
        depr = [w for w in caught if issubclass(w.category, DeprecationWarning)]
        print(f"deprecated() emitted {len(depr)} DeprecationWarning(s)")
        assert depr
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
