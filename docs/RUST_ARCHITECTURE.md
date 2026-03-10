# Rust Architecture (DataMD)

This document outlines the proposed Rust architecture for DataMD. It will guide the migration from the current Python implementation while keeping the door open for Python interoperability (PyO3 bindings) and preserving the `.dmd` format.

## Goals
- Feature parity with the Python engine (shortcodes, config, CLI flags)
- Performance and memory efficiency suitable for large files
- Safe concurrency for batch/parallel processing
- Single-binary distribution, with optional Python bindings

## Module Layout (Proposed)
```
src/
├── main.rs               # CLI entry
├── lib.rs                # Library entry (re-exports)
├── config/               # Config loading (JSON/TOML/env)
├── cache/                # File-based cache manager
├── security/             # Path resolution, input sanitization
├── transform/            # DSL parsing and ops (filter/sort/aggregate/limit)
├── shortcodes/           # csv/json/excel/pdf/ocr/video/chart handlers
├── processor/            # Markdown/shortcode parsing & rendering
├── error.rs              # Error types (thiserror/anyhow)
└── bindings/python.rs    # PyO3 bindings (optional)
```

## Data Flow (High Level)
1. CLI parses args (clap) → config resolved (serde JSON/TOML + env)
2. Processor parses Markdown/shortcodes (regex/pulldown-cmark)
3. Handlers load data (csv/json/excel/pdf/ocr/video), apply transforms (polars/serde), cache results
4. Renderer builds HTML/markdown output
5. Errors bubble as structured types; `--strict` exits non-zero

## Key Crates (Initial Choices)
- Core: `clap`, `serde`, `serde_json`, `toml`, `regex`, `thiserror`, `anyhow`, `tracing`
- Data: `polars` (or `arrow` if needed), `csv`, `serde_json`, `calamine`
- Docs: `lopdf`/`pdf-extract`, `tesseract-rs`, `image`, `ffmpeg-next`
- Charts/HTML: `plotters`, `pulldown-cmark`, `tera`/`askama`
- Concurrency: `rayon`
- Watch: `notify`
- Python bindings: `pyo3`, `maturin` (optional)

## Compatibility & Interop
- Preserve `.dmd` syntax and shortcode semantics
- Configuration: keep JSON; add TOML support
- CLI: maintain existing flags (`--strict`, `--watch`, styling options)
- Python: expose `process_dmd_file`/`process_dmd_string` via PyO3

## Testing Strategy
- Unit tests per module (handler, transform, security)
- Integration tests for end-to-end `.dmd` → HTML/markdown
- Property-based tests (`proptest`) for transforms and sanitization
- Fuzzing (`cargo-fuzz`) for parser/security-sensitive code
- Visual regression tests for charts (golden images)

## Build & Distribution
- Development: `cargo fmt`, `cargo clippy`, `cargo test`
- Release: `cargo build --release`
- Binaries: Linux/macOS/Windows targets
- Optional: publish to crates.io and PyPI (via maturin)

## Migration Links
- Plan: `/.windsurf/plans/datamd-python-to-rust-migration-69541b.md`
- Migration guide: `docs/MIGRATION_FROM_PYTHON.md`
