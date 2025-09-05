import os
import sys
import tempfile
import time
from pathlib import Path

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest
from cache import get_cache_manager, reset_cache


def test_cache_integration():
    """Test cache manager integration"""
    # Reset cache to ensure clean state
    reset_cache()

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Get cache manager with specific directory
        cache_manager = get_cache_manager(tmp_dir)

        # Create a test file
        test_file = Path(tmp_dir) / "test.csv"
        test_file.write_text("name,age\nAlice,30\nBob,25")

        # Wait a bit to ensure different timestamps
        time.sleep(0.1)

        # Test data
        test_data = {"processed": True, "rows": 2}

        # Cache the data
        cache_key = f"test:{test_file}"
        assert cache_manager.set(cache_key, test_data) is True

        # Retrieve the data
        cached_data = cache_manager.get(cache_key)
        assert cached_data == test_data

        # Check cache info
        info = cache_manager.get_cache_info()
        assert info["cache_files"] >= 1


def test_cache_invalidation_integration():
    """Test cache invalidation integration"""
    reset_cache()

    with tempfile.TemporaryDirectory() as tmp_dir:
        cache_manager = get_cache_manager(tmp_dir)

        # Create a test file
        test_file = Path(tmp_dir) / "source.csv"
        test_file.write_text("name,age\nAlice,30\nBob,25")

        # Wait a bit to ensure different timestamps
        time.sleep(0.1)

        # Cache some data
        cache_key = f"test:{test_file}"
        test_data = {"processed": True}
        assert cache_manager.set(cache_key, test_data) is True

        # Data should be retrievable
        cached_data = cache_manager.get(cache_key)
        assert cached_data == test_data, f"Expected {test_data}, got {cached_data}"

        # Modify source file
        time.sleep(1)  # Ensure file modification time changes
        test_file.write_text("name,age\nAlice,30\nBob,25\nCharlie,35")

        # Force a stat refresh
        test_file.stat()

        # Cache should now be invalid
        cached_data = cache_manager.get(cache_key)
        assert cached_data is None, f"Expected None, got {cached_data}"


if __name__ == "__main__":
    pytest.main([__file__])
