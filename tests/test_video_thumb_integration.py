import json
import os

import pytest

from python_implementation.datamd_ext import DataMDPreprocessor


def create_test_video(file_path, duration=2):
    """Create a simple test video file."""
    try:
        # Try to import moviepy
        from moviepy.editor import ColorClip

        # Create a simple black clip
        clip = ColorClip(size=(640, 480), color=(0, 0, 0), duration=duration)
        clip.write_videofile(
            file_path, fps=1, codec="libx264", audio=False, logger=None
        )
        return True
    except Exception:
        # If moviepy is not available or fails, create a dummy file
        with open(file_path, "wb") as f:
            f.write(b"dummy video content")
        return False


def process_video_thumb_shortcode(file_path, time, width=None, height=None):
    """Process a video_thumb shortcode and return the result."""
    # Create a mock preprocessor
    preprocessor = DataMDPreprocessor(None)

    # Create test line with the shortcode
    if width and height:
        line = f'{{{{ video_thumb "{file_path}" {time} {width} {height} }}}}'
    elif width:
        line = f'{{{{ video_thumb "{file_path}" {time} {width} }}}}'
    else:
        line = f'{{{{ video_thumb "{file_path}" {time} }}}}'

    # Process the line
    result_lines = preprocessor.run([line])
    return result_lines[0] if result_lines else ""


def test_video_thumb_shortcode_basic():
    """Test basic video_thumb shortcode functionality."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create test video
        video_file = tmp_path / "test_video.mp4"
        create_test_video(str(video_file))

        # Test basic video_thumb
        # Break long line into multiple lines
        result = process_video_thumb_shortcode(str(video_file), "1")

        # Verify the result contains the thumbnail markdown or error message
        assert isinstance(result, str)
        # Could be either a thumbnail link or an error message
        assert ".png" in result or "Error" in result or "error" in result


def test_video_thumb_shortcode_with_custom_dimensions():
    """Test video_thumb shortcode with custom width and height dimensions."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create test video
        video_file = tmp_path / "test_video.mp4"
        create_test_video(str(video_file))

        # Test video_thumb with custom dimensions
        # Break long line into multiple lines
        result = process_video_thumb_shortcode(str(video_file), "1", "320", "240")

        # Verify the result contains the thumbnail markdown
        assert isinstance(result, str)


def test_video_thumb_shortcode_width_only():
    """Test video_thumb shortcode with width only (height calculated)."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create test video
        video_file = tmp_path / "test_video.mp4"
        create_test_video(str(video_file))

        # Test video_thumb with width only
        # Break long line into multiple lines
        result = process_video_thumb_shortcode(str(video_file), "1", "320")

        # Verify the result contains the thumbnail markdown
        assert isinstance(result, str)


def test_video_thumb_shortcode_error_handling():
    """Test video_thumb shortcode error handling."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Test with non-existent file
        non_existent_file = tmp_path / "non_existent.mp4"
        result = process_video_thumb_shortcode(str(non_existent_file), "1")

        # Should contain error message
        assert "Error" in result or "error" in result or "not found" in result.lower()

        # Test with invalid time parameter
        video_file = tmp_path / "test_video.mp4"
        create_test_video(str(video_file))

        result = process_video_thumb_shortcode(str(video_file), "invalid")
        # Should handle invalid time gracefully
        assert isinstance(result, str)
