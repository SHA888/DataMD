# TODO

Detailed task breakdown by priority. Check the box when complete.

---
## Completed (Previously Implemented)

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

## P0 — Critical Path (Blocking Production Use)

### Error Handling & Logging
- [x] Replace all `print()` calls with structured logging (`logging` module) in `process_dmd_file`
- [x] Define custom exception hierarchy: `DataMDError`, `ShortcodeError`, `FileResolutionError`, `TransformError`
- [x] Ensure every shortcode handler propagates errors to the caller (no silent swallowing)
- [ ] Add contextual error messages with file path, line number, and shortcode text
- [ ] Surface errors to CLI output with clear user-facing messages
- [ ] Add `--strict` CLI flag that exits non-zero on any shortcode failure

### Large File Handling (F-009)
- [ ] Profile current memory usage with files at 10MB, 50MB, 100MB
- [ ] Implement generator-based CSV reading (chunked `pandas.read_csv` or raw `csv.reader`)
- [ ] Implement streaming JSON parsing for large JSON arrays (`ijson` or line-delimited JSON)
- [ ] Implement chunked Excel reading via `openpyxl` read-only mode
- [ ] Add configurable `chunk_size` in config system (default: 10,000 rows)
- [ ] Add memory usage guardrails: warn when estimated memory exceeds threshold
- [ ] Test with files >10MB, >50MB, >100MB — verify no OOM
- [ ] Document performance characteristics and limits

### Security Hardening
- [ ] Audit and enforce `allow_directory_traversal` across all file handlers
- [ ] Validate file extensions against configurable allowlist (default: csv, json, xlsx, xls, xlsm, ods, pdf, png, jpg, jpeg, mp4, webm)
- [ ] Sanitize all user-provided strings used in HTML output (prevent XSS in generated HTML)
- [ ] Add maximum file size enforcement (configurable, default: 100MB)
- [ ] Review path resolution for symlink traversal attacks
- [ ] Document threat model and security boundaries

---

## P1 — Quality & Reliability

### Test Coverage
- [ ] Audit current test coverage with `pytest-cov` — establish baseline percentage
- [ ] Set minimum coverage threshold (target: 85%) and enforce in CI
- [ ] **Unit tests — shortcode handlers:**
  - [ ] `csv` handler: normal, missing file, malformed CSV, unicode, large file
  - [ ] `json` handler: normal, nested objects, arrays, malformed JSON
  - [ ] `excel` handler: xlsx/xls/xlsm/ods, multi-sheet, merged cells
  - [ ] `pdf_table` handler: all strategy combos, threshold params, multi-page
  - [ ] `pdf_text` handler: normal, encrypted PDF, empty pages
  - [ ] `ocr` handler: normal, unreadable image, missing tesseract
  - [ ] `video_thumb` handler: valid video, invalid timecode, missing ffmpeg
  - [ ] `chart` handler: bar/line/pie, missing columns, empty data
  - [ ] Data transformations: filter/sort/groupby/sum/limit/offset chaining
- [ ] **Unit tests — infrastructure:**
  - [ ] Path resolution and validation
  - [ ] Input sanitization functions
  - [ ] Configuration loading (JSON, env vars, defaults, precedence)
  - [ ] Cache manager (store, retrieve, invalidate, expiry)
- [ ] **Integration tests:**
  - [ ] End-to-end `.dmd` file processing → HTML output
  - [ ] Watch mode: file change detection and rebuild
  - [ ] Batch directory processing
  - [ ] CLI argument combinations
- [ ] **Edge case tests:**
  - [ ] Empty `.dmd` file
  - [ ] `.dmd` file with no shortcodes (pure Markdown)
  - [ ] Shortcode with missing closing braces
  - [ ] Nested shortcodes (if supported)
  - [ ] File paths with spaces, unicode characters, special chars
- [ ] Set up CI pipeline (GitHub Actions): lint, type-check, test, coverage

### Type Safety
- [ ] Add type annotations to all public functions and methods
- [ ] Add type annotations to all class attributes
- [ ] Run `mypy --strict` and resolve all errors
- [ ] Add `mypy` to CI pipeline
- [ ] Add `py.typed` marker for downstream consumers

### Dependency Management
- [ ] Pin exact versions in `pyproject.toml` (or add `requirements.txt` via `pip-compile`)
- [ ] Create `requirements-dev.txt` with test/lint/type-check dependencies
- [ ] Audit dependencies for known vulnerabilities (`pip-audit`)
- [ ] Add `dependabot.yml` for automated update PRs
- [ ] Document minimum Python version (and test against it in CI)

---

## P2 — Developer Experience & Polish

### CLI Improvements
- [ ] Refactor argparse to use subcommands:
  - [ ] `datamd process <file_or_dir>` — main processing
  - [ ] `datamd watch <dir>` — live rebuild mode
  - [ ] `datamd version` — print version info
  - [ ] `datamd config` — print resolved configuration
- [ ] Add `--config` flag to override config file path
- [ ] Add `--output-dir` flag for custom output location
- [ ] Add `--dry-run` flag that reports what would be processed without writing
- [ ] Add `--format` flag (html, md) for output format selection
- [ ] Generate shell completions (bash, zsh, fish) via argparse or `shtab`
- [ ] Provide `--help` examples for each subcommand
- [ ] Add separate `datamd-cli` entry point in `pyproject.toml` for backward compatibility

### Configuration Enhancements
- [x] Normalize environment variable parsing (boolean, int) and document defaults
- [ ] Add `datamd config --init` to generate a starter config file
- [ ] Add config schema validation (JSON Schema or Pydantic)
- [ ] Support TOML config files alongside JSON
- [ ] Document all config keys, types, defaults, and env var overrides in a single reference table
- [ ] Support per-directory `.datamdrc` config files (merge with global)

### Documentation
- [ ] Create quick-start guide with a 5-minute walkthrough
- [ ] Add quick-start video or interactive notebook
- [ ] Add shortcode reference table (all shortcodes, params, examples) to SYNTAX.md
- [ ] Expand `docs/API_DOCUMENTATION.md` with code examples for every public function
- [ ] Write `docs/EXTENDING_SHORTCODES.md` with step-by-step guide for adding new handlers
- [ ] Include a table of supported shortcodes
- [ ] Update README.md to reflect current feature set accurately
- [ ] Add architecture overview diagram (processing pipeline)
- [ ] Add troubleshooting / FAQ section
- [ ] Add changelog (CHANGELOG.md) with semantic versioning

---

## P3 — Feature Enhancements

### Chart Generation Improvements
- [ ] Add scatter plot type
- [ ] Add stacked bar chart support
- [ ] Add multi-series line charts
- [ ] Add configurable color palettes
- [ ] Add chart size parameters (width, height)
- [ ] Support chart output as SVG (in addition to PNG)
- [ ] Add `legend` position parameter

### Data Transformation Extensions
- [ ] Add `select:col1,col2` to pick specific columns
- [ ] Add `rename:old=new` to rename columns
- [ ] Add `distinct` to deduplicate rows
- [ ] Add `avg`, `min`, `max`, `count` aggregations
- [ ] Add `pivot` transformation
- [ ] Add `join` to merge two data sources by key
- [ ] Document full transformation DSL grammar

### Output Format Expansion
- [ ] Support Markdown output (strip shortcodes, inline results as Markdown tables)
- [ ] Support PDF output via HTML → PDF pipeline (weasyprint or similar)
- [ ] Support JSON output (structured extraction results)
- [ ] Add `--template` flag for custom HTML templates

### Caching Improvements
- [ ] Add `--no-cache` CLI flag to force reprocessing
- [ ] Add `--clear-cache` CLI flag to purge cache directory
- [ ] Add cache size limit with LRU eviction
- [ ] Add cache statistics reporting (hit/miss ratio, size)
- [ ] Support cache sharing across runs (content-addressed keys)

---

## P4 — Ecosystem & Packaging

### Packaging & Distribution
- [ ] Publish to PyPI as `datamd`
- [ ] Add `__version__` to package and expose via CLI
- [ ] Create Docker image for reproducible processing
- [ ] Create GitHub release workflow (tag → build → publish)
- [ ] Add `Makefile` or `justfile` with common dev commands
- [ ] Update `pyproject.toml` to expose both console scripts

### Integration
- [ ] Python API: expose `process_dmd_string()` for programmatic use
- [ ] Python API: expose `process_shortcode()` for individual shortcode evaluation
- [ ] Jupyter integration: magic command `%datamd` for cell processing
- [ ] VS Code extension: syntax highlighting for `.dmd` files
- [ ] Pre-commit hook: validate `.dmd` files on commit

---

## Tracking

| Priority | Area | Status |
|---|---|---|
| P0 | Error Handling & Logging | 🔴 Not Started |
| P0 | Large File Handling | 🔴 Not Started |
| P0 | Security Hardening | 🟡 Partial (F-006, F-008 done) |
| P1 | Test Coverage | 🔴 Not Started |
| P1 | Type Safety | 🔴 Not Started |
| P1 | Dependency Management | 🔴 Not Started |
| P2 | CLI Improvements | 🟡 Partial (F-011 done) |
| P2 | Configuration Enhancements | 🟡 Partial (F-005 done) |
| P2 | Documentation | 🔴 Not Started |
| P3 | Chart Enhancements | 🟡 Partial (F-004 done) |
| P3 | Transform Extensions | 🟡 Partial (F-003 done) |
| P3 | Output Formats | 🔴 Not Started |
| P3 | Caching Improvements | 🟡 Partial (F-010 done) |
| P4 | Packaging & Distribution | 🔴 Not Started |
| P4 | Integration | 🔴 Not Started |
