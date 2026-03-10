# Migration from Python to Rust

This guide describes how DataMD will transition from the current Python implementation to a Rust-based engine while keeping existing `.dmd` files, syntax, and workflows fully compatible.

## Goals
- Maintain feature parity with the Python engine
- Improve performance and memory efficiency (target 10x speedup on large files)
- Deliver a single binary for easier distribution
- Keep Python interoperability via bindings (PyO3/maturin)
- Preserve the `.dmd` format and shortcode syntax

## Migration Phases (Summary)
1. Foundation: config, security, error handling, logging
2. Data processing: CSV/JSON/Excel, transformations, caching, streaming
3. Documents: PDF text/table, OCR, video thumbnails
4. Visualization: chart rendering, HTML/Markdown integration
5. CLI & integration: flags parity, watch mode, batch processing, progress
6. Python bindings (optional but planned): expose core functions and CLI
7. Testing & docs: parity tests, benchmarks, architecture and migration docs
8. Release: CI/CD, binaries, crates.io/PyPI, deprecation timeline for Python

## Backward Compatibility
- `.dmd` syntax and outputs stay the same
- Configuration remains JSON (TOML may be added) with equivalent options
- CLI flags retained (`--strict`, `--watch`, styling options, etc.)
- Parallel installation allowed during transition (Python and Rust engines)

## Python Interoperability
- Provide PyO3 bindings for programmatic use (e.g., `process_dmd_file`, `process_dmd_string`)
- Publish a Python wheel via maturin for users who embed DataMD in Python apps

## User Migration Path
- **Drop-in**: Use the Rust binary to process existing `.dmd` files
- **Side-by-side**: Keep Python engine available during a beta period
- **Bindings**: For Python codebases, switch to the PyO3-backed wheel

## Risks & Mitigations
- PDF table extraction parity: start with Rust implementation; fallback to FFI if needed
- Video thumbnail parity: use ffmpeg bindings; fallback to external ffmpeg if required
- Chart fidelity: visual regression tests; fallback to matplotlib via FFI if gaps appear

## Tracking
- Detailed plan: `/.windsurf/plans/datamd-python-to-rust-migration-69541b.md`
- Rust architecture outline: `docs/RUST_ARCHITECTURE.md`
