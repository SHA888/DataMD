# TODO

**Primary Focus**: Migrate DataMD from Python to Rust for 10x performance, memory safety, and single-binary distribution while maintaining 100% `.dmd` syntax compatibility.

**Approach**: Phase-based migration (11 weeks) with each phase delivering independent value. Python version remains available during transition.

---

## 🦀 Rust Migration Phases (P0 - Critical Path)

See detailed plan: `/.windsurf/plans/datamd-python-to-rust-migration-69541b.md`

### ✅ Phase 0: Planning & Documentation (Complete)
- [x] Create comprehensive migration plan
- [x] Document Rust architecture (`docs/RUST_ARCHITECTURE.md`)
- [x] Create migration guide (`docs/MIGRATION_FROM_PYTHON.md`)
- [x] Update README with Rust migration notes
- [x] Align TODO with phase-based approach

---

## Completed (Previously Implemented - Python)

These tasks were completed in earlier development phases. Preserved here for reference.

### Video Thumbnail Generation (F-001) ✅
- [x] Research moviepy capabilities for thumbnail generation
- [x] Design `video_thumb` shortcode syntax
- [x] Implement basic video thumbnail generation
- [x] Add support for custom dimensions and timecodes
- [x] Implement error handling for unsupported video formats
- [x] Create test cases for video thumbnail generation
- [x] Document video thumbnail feature in SYNTAX.md
- [x] Add example to examples/ directory

### Enhanced PDF Table Extraction (F-002) ✅
- [x] Review pdfplumber documentation for advanced options
- [x] Extend `pdf_table` shortcode with additional parameters
- [x] Implement horizontal/vertical strategy options
- [x] Add support for table detection thresholds
- [x] Improve handling of merged cells
- [x] Create test cases for enhanced PDF table extraction
- [x] Document enhanced PDF features in SYNTAX.md
- [x] Add example to examples/ directory

### File Path Validation (F-006) ✅
- [x] Design path validation and resolution approach
- [x] Implement path resolution function
- [x] Add directory traversal prevention
- [x] Create clear error messages for missing files
- [x] Integrate validation into all shortcode handlers
- [x] Create test cases for path validation
- [x] Document security considerations

### Input Sanitization (F-008) ✅
- [x] Identify all input parameters requiring sanitization
- [x] Implement input sanitization functions
- [x] Add file format validation
- [x] Implement basic security safeguards
- [x] Integrate sanitization into all shortcode handlers
- [x] Create test cases for input sanitization
- [x] Document security best practices

### Configuration System (F-005) ✅
- [x] Design configuration class structure
- [x] Implement default configuration values
- [x] Add JSON configuration file support
- [x] Implement environment variable overrides
- [x] Create configuration loading and validation
- [x] Integrate configuration system into existing code
- [x] Create test cases for configuration system
- [x] Document configuration options

### Data Transformation (F-003) ✅
- [x] Design data transformation syntax
- [x] Implement filtering capabilities
- [x] Add sorting functionality
- [x] Implement aggregation operations
- [x] Create simple query language parser
- [x] Integrate with existing data handlers (CSV, JSON, Excel)
- [x] Create test cases for data transformations
- [x] Document transformation syntax in SYNTAX.md

### Caching Mechanism (F-010) ✅
- [x] Design cache manager class
- [x] Implement file-based caching
- [x] Add automatic cache invalidation
- [x] Create configurable cache directory options
- [x] Integrate caching into shortcode handlers
- [x] Create test cases for caching functionality
- [x] Document caching behavior

### CLI Enhancement (F-011) ✅
- [x] Review current CLI options
- [x] Design new CLI parameters
- [x] Implement output customization options
- [x] Add batch processing capabilities
- [x] Implement verbose/debug mode
- [x] Update CLI documentation
- [x] Create test cases for CLI enhancements

### Chart Generation (F-004) ✅
- [x] Research visualization libraries (matplotlib, plotly, etc.)
- [x] Design chart shortcode syntax
- [x] Implement basic chart generation
- [x] Add support for multiple chart types
- [x] Create chart customization options
- [x] Integrate chart generation with data handlers
- [x] Create test cases for chart generation
- [x] Document chart features in SYNTAX.md

---

## P0 — Critical Path (Rust Migration)

### Phase 1: Foundation & Core (Weeks 1-2) ✅
**Goal**: Set up Rust project with core infrastructure

- [x] Initialize Cargo workspace with proper structure
- [x] Set up error handling with `thiserror` and `anyhow`
- [x] Implement configuration system (serde for JSON/TOML)
- [x] Port security module (path validation, sanitization)
- [x] Port custom exception hierarchy to Rust error types
- [x] Set up logging with `tracing` or `env_logger`
- [x] Create comprehensive unit tests for foundation

**Key Crates**: `thiserror`, `anyhow`, `serde`, `serde_json`, `toml`, `regex`, `tracing`

### Phase 2: Data Processing (Weeks 3-4) 🔴
**Goal**: Port data transformation and file handlers

- [ ] Implement CSV processing with `csv` crate
- [ ] Implement JSON processing with `serde_json`
- [ ] Implement Excel support with `calamine`
- [ ] Port data transformation DSL (filter/sort/aggregate)
- [ ] Implement streaming for large files
- [ ] Add caching layer with file-based storage
- [ ] Create integration tests for each format

**Key Crates**: `csv`, `serde_json`, `calamine`, `polars` (or `arrow`)

### Phase 3: Document Processing (Weeks 5-6) 🔴
**Goal**: Port PDF, OCR, and video features

- [ ] Implement PDF text extraction with `pdf-extract` or `lopdf`
- [ ] Implement PDF table extraction (custom logic or bindings)
- [ ] Add OCR support via `tesseract-rs` or FFI to tesseract
- [ ] Implement video thumbnail generation via FFI to ffmpeg
- [ ] Handle image processing with `image` crate
- [ ] Test all document processing features

**Key Crates**: `lopdf`/`pdf-extract`, `tesseract-rs`, `image`, `ffmpeg-next`

### Phase 4: Visualization & Rendering (Week 7) 🔴
**Goal**: Port chart generation and HTML rendering

- [ ] Implement chart generation with `plotters` or `resvg`
- [ ] Port HTML template system
- [ ] Implement Markdown integration (pulldown-cmark)
- [ ] Add CSS styling support
- [ ] Test rendering pipeline end-to-end

**Key Crates**: `plotters`, `pulldown-cmark`, `tera`/`askama`

### Phase 5: CLI & Integration (Week 8) 🔴
**Goal**: Complete CLI and integration features

- [ ] Implement CLI with `clap` (derive API)
- [ ] Add file watching with `notify`
- [ ] Implement batch processing with `rayon` for parallelism
- [ ] Add progress indicators with `indicatif`
- [ ] Port all CLI flags (--strict, --watch, --verbose, etc.)
- [ ] Create comprehensive CLI tests

**Key Crates**: `clap`, `notify`, `rayon`, `indicatif`

### Phase 6: Python Bindings (Week 9) 🟡
**Goal**: Enable Python interoperability (Optional but recommended)

- [ ] Create PyO3 bindings for core functionality
- [ ] Expose `process_dmd_file()` to Python
- [ ] Expose `process_dmd_string()` for programmatic use
- [ ] Create Python package with maturin
- [ ] Test Python bindings thoroughly
- [ ] Document Python API

**Key Crates**: `pyo3`, `maturin`

### Phase 7: Testing & Documentation (Week 10) 🔴
**Goal**: Ensure production readiness

- [ ] Port all Python tests to Rust
- [ ] Add property-based tests with `proptest`
- [ ] Add fuzzing tests with `cargo-fuzz`
- [ ] Benchmark against Python implementation
- [ ] Update all documentation (README, SYNTAX, API docs)
- [ ] Create migration guide for users
- [ ] Document Rust architecture for contributors

### Phase 8: Release & Deployment (Week 11) 🔴
**Goal**: Ship production-ready Rust version

- [ ] Set up CI/CD for Rust (GitHub Actions)
- [ ] Create release binaries for Linux/macOS/Windows
- [ ] Publish to crates.io
- [ ] Optionally publish Python bindings to PyPI
- [ ] Update installation instructions
- [ ] Create deprecation timeline for Python version

---

### 📊 Migration Success Metrics
- ⚡ **Performance**: 10x faster on large files (>10MB)
- 💾 **Memory**: 50% lower peak memory usage
- 📦 **Binary Size**: Single executable <50MB
- ✅ **Test Coverage**: Maintain >85% coverage
- 🎯 **Feature Parity**: 100% of Python features working
- 👥 **User Migration**: Smooth transition with <5% issues reported

### 🔧 Key Technical Decisions
- **DataFrame library**: Polars (Rust-native, pandas-like API, lazy evaluation)
- **PDF table extraction**: Custom implementation with `lopdf`, fallback to FFI if needed
- **Video processing**: `ffmpeg-next` for native Rust solution
- **Chart generation**: `plotters` for pure Rust solution

### Large File Handling (F-009)

> **Note**: Large file handling will be significantly improved in the Rust migration (Phase 2). These Python tasks are optional and may be skipped in favor of the Rust implementation.

- [ ] Profile current memory usage with files at 10MB, 50MB, 100MB (baseline for Rust comparison)
- [ ] ~~Implement generator-based CSV reading~~ → Rust Phase 2 (streaming with `csv` crate)
- [ ] ~~Implement streaming JSON parsing~~ → Rust Phase 2 (streaming with `serde_json`)
- [ ] ~~Implement chunked Excel reading~~ → Rust Phase 2 (`calamine` with streaming)
- [ ] ~~Add configurable `chunk_size`~~ → Rust Phase 1 (config system)
- [ ] ~~Add memory usage guardrails~~ → Rust inherent (predictable memory)
- [ ] Test with files >10MB, >50MB, >100MB — verify no OOM (both Python baseline and Rust)
- [ ] Document performance characteristics and limits (after Rust migration)

### Security Hardening

> **Note**: Security improvements will be re-implemented in Rust (Phase 1). Python security tasks are lower priority but useful for immediate hardening.

- [ ] Audit and enforce `allow_directory_traversal` across all file handlers → Also in Rust Phase 1
- [ ] Validate file extensions against configurable allowlist → Also in Rust Phase 1 (security module)
- [ ] Sanitize all user-provided strings used in HTML output (prevent XSS) → Also in Rust Phase 1
- [ ] Add maximum file size enforcement (configurable, default: 100MB) → Also in Rust Phase 1
- [ ] Review path resolution for symlink traversal attacks → Also in Rust Phase 1
- [ ] Document threat model and security boundaries → Rust Phase 7 (comprehensive docs)

---

## P1 — Quality & Reliability

### Test Coverage

> **Note**: Comprehensive test suite will be ported to Rust in Phase 7. Python tests serve as specification and baseline.

- [ ] Audit current test coverage with `pytest-cov` — establish baseline percentage (reference for Rust)
- [ ] Set minimum coverage threshold (target: 85%) and enforce in CI → Rust Phase 7
- [ ] **Unit tests — shortcode handlers:** (will be ported to Rust in Phase 7)
  - [ ] `csv` handler: normal, missing file, malformed CSV, unicode, large file
  - [ ] `json` handler: normal, nested objects, arrays, malformed JSON
  - [ ] `excel` handler: xlsx/xls/xlsm/ods, multi-sheet, merged cells
  - [ ] `pdf_table` handler: all strategy combos, threshold params, multi-page
  - [ ] `pdf_text` handler: normal, encrypted PDF, empty pages
  - [ ] `ocr` handler: normal, unreadable image, missing tesseract
  - [ ] `video_thumb` handler: valid video, invalid timecode, missing ffmpeg
  - [ ] `chart` handler: bar/line/pie, missing columns, empty data
  - [ ] Data transformations: filter/sort/groupby/sum/limit/offset chaining
- [ ] **Unit tests — infrastructure:** (will be ported to Rust in Phase 7)
  - [ ] Path resolution and validation
  - [ ] Input sanitization functions
  - [ ] Configuration loading (JSON, env vars, defaults, precedence)
  - [ ] Cache manager (store, retrieve, invalidate, expiry)
- [ ] **Integration tests:** (will be ported to Rust in Phase 7)
  - [ ] End-to-end `.dmd` file processing → HTML output
  - [ ] Watch mode: file change detection and rebuild
  - [ ] Batch directory processing
  - [ ] CLI argument combinations
- [ ] **Edge case tests:** (will be ported to Rust in Phase 7)
  - [ ] Empty `.dmd` file
  - [ ] `.dmd` file with no shortcodes (pure Markdown)
  - [ ] Shortcode with missing closing braces
  - [ ] Nested shortcodes (if supported)
  - [ ] File paths with spaces, unicode characters, special chars
- [ ] Set up CI pipeline (GitHub Actions): lint, type-check, test, coverage → Rust Phase 8

### Type Safety

> **Note**: Rust has compile-time type safety built-in. Python type safety tasks are optional for Python version maintenance.

- [ ] ~~Add type annotations~~ → Rust inherent (compile-time type checking)
- [ ] ~~Run `mypy --strict`~~ → Rust inherent (rustc type checking)
- [ ] ~~Add `mypy` to CI~~ → Rust Phase 8 (cargo check/clippy in CI)
- [ ] ~~Add `py.typed` marker~~ → Rust Phase 6 (PyO3 bindings will be typed)

### Dependency Management

> **Note**: Rust uses Cargo.toml for dependency management with built-in version locking (Cargo.lock).

- [ ] ~~Pin exact versions~~ → Rust Phase 1 (Cargo.toml with semver)
- [ ] ~~Create requirements-dev.txt~~ → Rust Phase 1 (dev-dependencies in Cargo.toml)
- [ ] ~~Audit dependencies for vulnerabilities~~ → Rust Phase 8 (cargo-audit in CI)
- [ ] Add `dependabot.yml` for automated update PRs → Rust Phase 8 (supports Cargo)
- [ ] ~~Document minimum Python version~~ → Rust: document MSRV (Minimum Supported Rust Version)

---

## P2 — Developer Experience & Polish

### CLI Improvements

> **Note**: Modern CLI will be implemented in Rust Phase 5 with `clap`. Python CLI improvements are lower priority.

- [ ] ~~Refactor argparse to use subcommands~~ → Rust Phase 5 (clap with derive API)
  - [ ] `datamd process <file_or_dir>` → Rust Phase 5
  - [ ] `datamd watch <dir>` → Rust Phase 5 (with `notify` crate)
  - [ ] `datamd version` → Rust Phase 5
  - [ ] `datamd config` → Rust Phase 5
- [ ] ~~Add `--config` flag~~ → Rust Phase 5
- [ ] ~~Add `--output-dir` flag~~ → Rust Phase 5
- [ ] ~~Add `--dry-run` flag~~ → Rust Phase 5
- [ ] ~~Add `--format` flag~~ → Rust Phase 5
- [ ] ~~Generate shell completions~~ → Rust Phase 5 (clap supports bash/zsh/fish)
- [ ] ~~Provide `--help` examples~~ → Rust Phase 5 (clap built-in)
- [ ] ~~Add separate entry point~~ → Rust Phase 8 (binary distribution)

### Configuration Enhancements
- [x] Normalize environment variable parsing (boolean, int) and document defaults
- [ ] ~~Add `datamd config --init`~~ → Rust Phase 5 (CLI subcommand)
- [ ] ~~Add config schema validation~~ → Rust Phase 1 (serde with validation)
- [ ] ~~Support TOML config files~~ → Rust Phase 1 (serde_json + toml)
- [ ] Document all config keys → Rust Phase 7 (comprehensive docs)
- [ ] ~~Support per-directory `.datamdrc`~~ → Rust Phase 1 (config merging)

### Documentation

> **Note**: Documentation will be updated for Rust in Phase 7. Current docs serve as specification.

- [ ] Create quick-start guide with a 5-minute walkthrough → Update for Rust in Phase 7
- [ ] Add quick-start video or interactive notebook → Update for Rust in Phase 7
- [ ] Add shortcode reference table to SYNTAX.md → Keep (syntax unchanged in Rust)
- [ ] Expand `docs/API_DOCUMENTATION.md` → Rewrite for Rust API in Phase 7
- [ ] Write `docs/EXTENDING_SHORTCODES.md` → Rewrite for Rust traits in Phase 7
- [ ] Include a table of supported shortcodes → Keep (feature parity)
- [x] Update README.md to reflect Rust migration plan
- [ ] Add architecture overview diagram → Create for Rust in Phase 7
- [ ] Add troubleshooting / FAQ section → Update for Rust in Phase 7
- [ ] Add changelog (CHANGELOG.md) → Start with Rust v1.0.0 in Phase 8

---

## P3 — Feature Enhancements

### Chart Generation Improvements

> **Note**: Chart enhancements will be implemented in Rust Phase 4 with `plotters`.

- [ ] Add scatter plot type → Rust Phase 4 (plotters supports scatter)
- [ ] Add stacked bar chart support → Rust Phase 4
- [ ] Add multi-series line charts → Rust Phase 4
- [ ] Add configurable color palettes → Rust Phase 4
- [ ] Add chart size parameters (width, height) → Rust Phase 4
- [ ] Support chart output as SVG (in addition to PNG) → Rust Phase 4 (plotters supports both)
- [ ] Add `legend` position parameter → Rust Phase 4

### Data Transformation Extensions

> **Note**: Transform extensions will be implemented in Rust Phase 2 with `polars`.

- [ ] Add `select:col1,col2` → Rust Phase 2 (polars select)
- [ ] Add `rename:old=new` → Rust Phase 2 (polars rename)
- [ ] Add `distinct` → Rust Phase 2 (polars unique)
- [ ] Add `avg`, `min`, `max`, `count` aggregations → Rust Phase 2 (polars agg)
- [ ] Add `pivot` transformation → Rust Phase 2 (polars pivot)
- [ ] Add `join` to merge two data sources → Rust Phase 2 (polars join)
- [ ] Document full transformation DSL grammar → Rust Phase 7

### Output Format Expansion

> **Note**: Output formats will be implemented in Rust Phase 4.

- [ ] Support Markdown output → Rust Phase 4 (pulldown-cmark)
- [ ] Support PDF output via HTML → PDF → Rust Phase 4 (or external tool)
- [ ] Support JSON output (structured extraction) → Rust Phase 4 (serde_json)
- [ ] Add `--template` flag for custom HTML templates → Rust Phase 4 (tera/askama)

### Caching Improvements

> **Note**: Caching enhancements will be implemented in Rust Phase 2.

- [ ] Add `--no-cache` CLI flag → Rust Phase 5 (CLI flag)
- [ ] Add `--clear-cache` CLI flag → Rust Phase 5 (CLI flag)
- [ ] Add cache size limit with LRU eviction → Rust Phase 2 (cache manager)
- [ ] Add cache statistics reporting → Rust Phase 2
- [ ] Support cache sharing across runs → Rust Phase 2 (content-addressed keys)

---

## P4 — Ecosystem & Packaging

### Packaging & Distribution

> **Note**: Rust distribution will be via crates.io and binary releases. Python bindings optional via PyPI.

- [ ] ~~Publish to PyPI as `datamd`~~ → Rust Phase 8 (crates.io + optional PyPI via maturin)
- [ ] ~~Add `__version__`~~ → Rust Phase 8 (built-in via Cargo.toml)
- [ ] Create Docker image → Rust Phase 8 (multi-stage build with Rust binary)
- [ ] Create GitHub release workflow → Rust Phase 8 (Linux/macOS/Windows binaries)
- [ ] ~~Add `Makefile` or `justfile`~~ → Rust Phase 8 (Cargo handles builds)
- [ ] ~~Update `pyproject.toml`~~ → Rust Phase 6 (PyO3 bindings if needed)

### Integration

> **Note**: Integration features will be implemented in Rust with optional Python bindings.

- [ ] ~~Python API: `process_dmd_string()`~~ → Rust Phase 6 (PyO3 bindings)
- [ ] ~~Python API: `process_shortcode()`~~ → Rust Phase 6 (PyO3 bindings)
- [ ] Jupyter integration: magic command `%datamd` → Rust Phase 6 (via PyO3 bindings)
- [ ] VS Code extension: syntax highlighting for `.dmd` files → Post-Rust (language agnostic)
- [ ] Pre-commit hook: validate `.dmd` files → Rust Phase 8 (binary-based hook)

---

## 📊 Phase Tracking

### Rust Migration Progress (11-Week Timeline)

| Phase | Timeline | Goal | Status |
|---|---|---|---|
| Phase 0 | Complete | Planning & Documentation | ✅ Done |
| Phase 1 | Weeks 1-2 | Foundation & Core | 🔴 Not Started |
| Phase 2 | Weeks 3-4 | Data Processing | 🔴 Not Started |
| Phase 3 | Weeks 5-6 | Document Processing | � Not Started |
| Phase 4 | Week 7 | Visualization & Rendering | 🔴 Not Started |
| Phase 5 | Week 8 | CLI & Integration | 🔴 Not Started |
| Phase 6 | Week 9 | Python Bindings (Optional) | 🟡 Planned |
| Phase 7 | Week 10 | Testing & Documentation | 🔴 Not Started |
| Phase 8 | Week 11 | Release & Deployment | � Not Started |

### Python Version Status (Maintenance Mode)

| Area | Status | Notes |
|---|---|---|
| Error Handling & Logging | ✅ Complete | Serves as spec for Rust |
| Large File Handling | 🟡 Deferred | Will be addressed in Rust Phase 2 |
| Security Hardening | 🟡 Partial | F-006, F-008 done; rest in Rust Phase 1 |
| Test Coverage | � Baseline | Existing tests serve as specification |
| Type Safety | 🟡 Deferred | Rust has compile-time type safety |
| CLI Improvements | 🟡 Partial | F-011 done; modern CLI in Rust Phase 5 |
| Documentation | � Updated | Migration docs added; full update in Rust Phase 7 |
