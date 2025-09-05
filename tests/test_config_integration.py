import json
import os
import sys
import tempfile
from pathlib import Path

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest

from config import get_config, reset_config


def test_config_loading_with_file():
    """Test loading configuration from a file"""
    # Create a temporary config file
    config_data = {
        "application": {"name": "Test App", "version": "2.0.0"},
        "features": {"ocr_enabled": False},
    }

    # Use TemporaryDirectory instead of NamedTemporaryDirectory
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create config file
        config_file = tmp_path / "test_config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f)

        # Reset config singleton and load from file
        reset_config()
        config = get_config(str(config_file))

        # Test that values were loaded from file
        assert config.get_application_name() == "Test App"
        assert config.get_application_version() == "2.0.0"
        assert config.is_feature_enabled("ocr_enabled") is False


def test_config_singleton_reset():
    """Test that configuration singleton can be reset"""
    reset_config()
    # This test just verifies the reset function exists and runs
    assert True


if __name__ == "__main__":
    pytest.main([__file__])
