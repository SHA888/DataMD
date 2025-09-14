# TODO

## Configuration
- Normalize environment variable parsing (boolean, int) and document defaults.
- Add CLI option to override config file path.

## Error handling
- Replace prints with logging or exceptions in `process_dmd_file`.
- Ensure errors are surfaced to the user or logs.

## Type hints
- Add missing type annotations to public functions.
- Use mypy to enforce typing.

## Dependency pinning
- Pin exact dependency versions in `pyproject.toml` or use `pip-tools`.
- Add `requirements-dev.txt` for reproducible dev env.

## CLI Argument Parsing
- Refactor argparse to use subparsers (`process`, `watch`, `version`).
- Provide help and examples for each command.

## Performance
- Stream large files instead of reading all at once.
- Add configuration for chunk size in `process_dmd_file`.

## Testing
- Add integration tests for watch mode.
- Test error conditions for missing files.
- Add coverage threshold checks.

## Documentation
- Add quick‑start video or interactive notebook.
- Expand `docs/API_DOCUMENTATION.md` with sample code for new shortcodes.
- Include a table of supported shortcodes.

## Security
- Enforce `allow_directory_traversal` in file handlers.
- Validate file extensions against config.

## Packaging
- Add separate entry point `datamd-cli` for backward compatibility.
- Update `pyproject.toml` to expose both console scripts.
