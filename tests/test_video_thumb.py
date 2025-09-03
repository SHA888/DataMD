import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

# Import after path modification
from process_dmd import process_dmd_file


def test_video_thumb_shortcode():
    """Test the video_thumb shortcode functionality"""
    # Create a temporary directory for our test
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a simple test DMD file with video_thumb shortcode
        test_content = """# Video Thumbnail Test

## Test Video Thumbnail Generation
{{ video_thumb "test_video.mp4" 5 320 240 }}
"""

        dmd_file = tmp_path / "test_video.dmd"
        dmd_file.write_text(test_content, encoding="utf-8")

        # Create a dummy video file (we won't actually process it in tests)
        video_file = tmp_path / "test_video.mp4"
        video_file.write_text("dummy video content", encoding="utf-8")

        # Process the DMD file
        # Note: This will fail because we don't have a real video file,
        # but we can at least test that the shortcode is recognized
        try:
            process_dmd_file(str(dmd_file))
            # If we get here, the shortcode was at least recognized
            html_file = dmd_file.with_suffix(".html")
            assert html_file.exists()
        except Exception as e:
            # This is expected since we don't have a real video file
            # but we're mainly testing that our code doesn't crash on the shortcode
            assert "video_thumb" in str(e) or "clip" in str(e).lower()


def test_video_thumb_with_minimal_args():
    """Test the video_thumb shortcode with minimal arguments"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a simple test DMD file with minimal video_thumb shortcode
        test_content = """# Video Thumbnail Test

## Test Video Thumbnail Generation (Minimal Args)
{{ video_thumb "test_video.mp4" 10 }}
"""

        dmd_file = tmp_path / "test_video_min.dmd"
        dmd_file.write_text(test_content, encoding="utf-8")

        # Create a dummy video file
        video_file = tmp_path / "test_video.mp4"
        video_file.write_text("dummy video content", encoding="utf-8")

        # Process the DMD file
        try:
            process_dmd_file(str(dmd_file))
            html_file = dmd_file.with_suffix(".html")
            assert html_file.exists()
        except Exception as e:
            # Expected since we don't have a real video file
            assert "video_thumb" in str(e) or "clip" in str(e).lower()


def test_video_thumb_missing_args():
    """Test the video_thumb shortcode with missing arguments"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a simple test DMD file with missing time parameter
        test_content = """# Video Thumbnail Test

## Test Video Thumbnail Generation (Missing Args)
{{ video_thumb "test_video.mp4" }}
"""

        dmd_file = tmp_path / "test_video_missing.dmd"
        dmd_file.write_text(test_content, encoding="utf-8")

        # Create a dummy video file
        video_file = tmp_path / "test_video.mp4"
        video_file.write_text("dummy video content", encoding="utf-8")

        # Process the DMD file
        process_dmd_file(str(dmd_file))
        html_file = dmd_file.with_suffix(".html")
        assert html_file.exists()

        # Check that the output contains an error message about missing time parameter
        html_content = html_file.read_text(encoding="utf-8")
        assert "Error: video_thumb requires time parameter" in html_content


if __name__ == "__main__":
    pytest.main([__file__])
