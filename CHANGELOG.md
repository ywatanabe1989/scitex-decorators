# Changelog

All notable changes to `scitex-decorators` are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.2.0] — 2026-06-07

- feat: port `cache` (the `functools.lru_cache(maxsize=None)` alias) and
  `alternate_kwarg` (kwargs-rename helper) from `scitex_gen` (Phase B of
  the scitex-gen full retirement wave).
- feat: port `partial_at` from `scitex_gen` `misc.py` — a `functools.partial`
  variant that fixes one positional argument at a chosen index.
- Note: `wrap` is NOT being re-imported. The version that ships here
  (`_wrap.py`) is strictly more capable than scitex_gen's (attaches
  `_original_func` / `_is_wrapper` introspection markers), and the
  scitex_gen variant will be dropped (not ported) in the scitex_gen
  retirement PR.

## [0.1.12] — 2026-05-25

- fix(tests): guard auto-order integration tests against umbrella import
- fix(ci): repair tests + quality + docs workflows
- ci(codecov): disable PR comments to reduce email noise
- ci(docs): make sphinx_html commit-back step non-fatal
- fix(workflows): resync release pipeline and standardize to scitex-dev canonical set
- Build and release pipeline overhaul

## [0.1.9]

- Initial CHANGELOG entry — see git log for prior history.
