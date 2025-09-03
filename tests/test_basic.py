from pathlib import Path

from python_implementation.process_dmd import process_dmd_file


def test_process_simple_example(tmp_path: Path):
    # Copy simple_example.dmd into temp dir to avoid polluting repo root
    repo_root = Path(__file__).resolve().parents[1]
    src = repo_root / "examples" / "simple_example.dmd"
    dst = tmp_path / "simple_example.dmd"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    # Also ensure data/config paths are accessible relative to temp dir
    # Create symlinks to repo data and config directories
    (tmp_path / "data").symlink_to(repo_root / "data")
    (tmp_path / "config").symlink_to(repo_root / "config")

    # Run processor
    ok = process_dmd_file(str(dst))
    assert ok is True

    # Check output exists
    out_file = dst.with_suffix(".html")
    assert out_file.exists()

    # Basic sanity check on content
    html = out_file.read_text(encoding="utf-8")
    assert "Sales Data" in html
    assert "App Configuration" in html
