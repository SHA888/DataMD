#!/usr/bin/env python3
"""
Test script to verify video thumbnail functionality
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the python_implementation directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python_implementation'))

from datamd_ext import DataMDPreprocessor


def test_video_thumb_functionality():
    """Test the video_thumb functionality directly"""
    # Create a temporary directory for our test
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Create a dummy video file
        video_file = tmp_path / "sample.mp4"
        video_file.write_text("dummy video content", encoding="utf-8")
        
        # Test the video_thumb shortcode processing
        preprocessor = DataMDPreprocessor(None)
        
        # Test line with video_thumb shortcode
        test_line = f'{{{{ video_thumb "{video_file}" 5 }}}}'
        lines = [test_line]
        
        # Process the line
        result = preprocessor.run(lines)
        
        print("Input line:", test_line)
        print("Output lines:", result)
        
        # Check if we get an error about the file not being a valid video
        # (which is expected since it's just a text file)
        if result and "Error generating thumbnail" in result[0]:
            print("✓ Video thumbnail processing working (got expected error)")
            return True
        else:
            print("✗ Unexpected result")
            return False


if __name__ == "__main__":
    success = test_video_thumb_functionality()
    if success:
        print("Test passed!")
        sys.exit(0)
    else:
        print("Test failed!")
        sys.exit(1)