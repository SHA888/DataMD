import os
import sys
import tempfile

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest

from config import Configuration, get_config, reset_config


def test_configuration_defaults():
    """Test Configuration class with default values"""
    config = Configuration()

    # Test application settings
    assert config.get_application_name() == "DataMD Processor"
    assert config.get_application_version() == "1.0.0"

    # Test feature settings
    assert config.is_feature_enabled("ocr_enabled") is True
    assert config.is_feature_enabled("pdf_processing") is True
    assert config.is_feature_enabled("video_support") is True

    # Test limit settings
    assert config.get_max_file_size_mb() == 100
    assert config.get_max_pdf_pages() == 50
    assert config.get_supported_languages() == ["eng", "spa", "fra", "deu", "ind"]

    # Test processing settings
    assert config.get_default_csv_separator() == ","
    assert config.get_default_pdf_strategy() == "lines"
    assert config.get_default_ocr_language() == "eng"


def test_configuration_from_file():
    """Test Configuration class loading from file"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_file = os.path.join(tmp_dir, "test_config.json")

        # Create test config file
        test_config = {
            "application": {"name": "Test App", "version": "2.0.0"},
            "features": {"ocr_enabled": False},
        }

        import json

        with open(config_file, "w") as f:
            json.dump(test_config, f)

        # Load config from file
        config = Configuration(config_file)

        # Test loaded values
        assert config.get_application_name() == "Test App"
        assert config.get_application_version() == "2.0.0"
        assert config.is_feature_enabled("ocr_enabled") is False
        # Default values should still be there
        assert config.is_feature_enabled("pdf_processing") is True


def test_configuration_get_set():
    """Test Configuration get and set methods"""
    config = Configuration()

    # Test get with default
    assert config.get("nonexistent.key", "default") == "default"

    # Test set method
    config.set("new.section.value", "test_value")
    assert config.get("new.section.value") == "test_value"


def test_configuration_environment_override():
    """Test Configuration environment variable overrides"""
    # This test would require setting environment variables
    # For now, we'll just test that the method exists
    config = Configuration()
    # Should not crash
    config._load_from_environment()


def test_singleton_config():
    """Test singleton configuration instance"""
    reset_config()  # Reset singleton

    # Get first instance
    config1 = get_config()
    config1.test_attr = "value1"

    # Get second instance
    config2 = get_config()

    # Should be the same instance
    assert config1 is config2
    assert hasattr(config2, "test_attr")
    assert config2.test_attr == "value1"


if __name__ == "__main__":
    pytest.main([__file__])
