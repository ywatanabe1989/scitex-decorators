# Changelog

All notable changes to `scitex-decorators` are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

- fix: resolve cache dir under `decorators/runtime/` via `local_state.runtime_path`
- fix: correct `SciTeX_DIR` → `SCITEX_DIR` env var casing in tests (Linux is case-sensitive)
- docs: update README cache-dir resolution to match actual code
- chore: add `.gitignore` entries for `.scitex/*/runtime/`

## [0.1.12] — 2026-05-25

- fix(tests): guard auto-order integration tests against umbrella import
- fix(ci): repair tests + quality + docs workflows
- ci(codecov): disable PR comments to reduce email noise
- ci(docs): make sphinx_html commit-back step non-fatal
- fix(workflows): resync release pipeline and standardize to scitex-dev canonical set
- Build and release pipeline overhaul

## [0.1.9]

- Initial CHANGELOG entry — see git log for prior history.
