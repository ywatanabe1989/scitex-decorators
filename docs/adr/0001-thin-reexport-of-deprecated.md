# ADR-0001: Re-export `@deprecated` from scitex-compat (do not host the impl)

## Status
Accepted (2026-05-29)

## Context
`scitex_decorators._deprecated` historically hosted a ~200 LoC
implementation of the `deprecated(reason=None, forward_to=None)`
decorator, with call-forwarding via `importlib` and auto-generated
docstrings. The decorator was a fully working, well-tested feature of
this package.

At the same time, `scitex-compat` shipped a much simpler 12-line
`deprecated(new_name, removal_version="2.0")` — different signature,
warn-only, no forwarding.

A 2026-05-29 SoC audit established that **scitex-compat is the better
home** for `@deprecated`:

- scitex-compat has **zero runtime deps**. Layer 0 leaf packages
  (scitex-types, scitex-path, scitex-str, scitex-logging,
  scitex-config, scitex-dev) can import the decorator without pulling
  numpy / tqdm / scitex-config / scitex-dev — all of which
  scitex-decorators drags in.
- scitex-decorators sits **above** scitex-config and scitex-dev in the
  layered architecture (see `scitex-python/GITIGNORED/SOC.md`).
  If scitex-config wanted `@deprecated` it could not import from
  scitex-decorators without creating a cycle.
- Live-caller scan found that the only production caller
  (`scitex-gen/_legacy/_deprecated_*.py`) was already using the
  *rich* signature — not the simple one in scitex-compat. So moving
  the rich impl into scitex-compat (a) loses nothing, (b) gives every
  layer access.

See `scitex-compat/docs/adr/0001-canonical-deprecated-decorator.md`
for the full reasoning and verification.

## Decision
scitex-decorators **does not host** the `@deprecated` implementation.
It exposes the symbol via a thin re-export:

```python
# src/scitex_decorators/_deprecated.py
from __future__ import annotations
from scitex_compat import deprecated
__all__ = ["deprecated"]
```

**Contract**

1. `from scitex_decorators import deprecated` MUST keep working — the
   public surface of scitex-decorators does not regress. Existing
   callers do not need to migrate.
2. The implementation lives in `scitex_compat._compat`. Any bug fix,
   feature addition, or signature change happens there, not here.
3. `scitex-decorators` declares `scitex-compat>=0.1.0` in
   `[project] dependencies` so the import resolves at install time.
4. New code should prefer `from scitex_compat import deprecated`.
   The scitex-decorators re-export remains indefinitely as a
   backward-compat path — re-export has near-zero cost so there is no
   deadline to deprecate it.

**Placement principles**

1. **Don't host what you don't own.** scitex-decorators' identity is
   the numpy/torch/pandas/xarray converter family plus caching /
   batching / timeout / signal_fn — heavy, domain-specific decorators.
   `@deprecated` is generic compat plumbing; the heavy package is the
   wrong home for it.
2. **Re-export is not duplication.** Two `def deprecated(...)` bodies
   in two repos would drift (and *had* started to drift: the warning
   wording already differed pre-decision). One body + one re-export
   cannot drift.

## Consequences
- scitex-decorators install now also pulls scitex-compat. scitex-compat
  is dependency-free stdlib code, so install delta is negligible.
- `scitex_decorators._deprecated.py` shrinks from ~200 LoC to ~20 LoC.
  The historical implementation is preserved in git history and now
  lives in scitex-compat.
- Any future enhancement to `@deprecated` (e.g. emitting structured
  metadata for the linter) is implemented once, in scitex-compat, and
  picked up by both packages automatically.
- A semver-breaking change in the underlying signature would propagate
  to scitex-decorators callers too. The risk is acceptable: the rich
  signature is already what existing callers use.

## Notes
Surfaced 2026-05-29 during the broader SoC audit (R5/R6 in
`scitex-python/GITIGNORED/SOC.md`). The operator's framing question
was *"is scitex-compat still needed, or can it dissolve into
scitex-decorators?"* — the audit pointed the other way: scitex-compat
is needed precisely because it's zero-dep, and `@deprecated` should
*move into it*, not away from it.

Related:
- `scitex-compat/docs/adr/0001-canonical-deprecated-decorator.md`
  (the upstream ADR — that's where the implementation lives).
- `scitex-python/GITIGNORED/SOC.md` § "SSOT for `@deprecated`".
