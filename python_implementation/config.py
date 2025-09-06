import json
import os
from typing import Any, Dict, List, Optional


class Configuration:
    """
    Configuration class for DataMD application.

    Manages application settings from JSON config file, environment variables,
    and provides default values.
    """

    # Default configuration values
    DEFAULTS = {
        "application": {
            "name": "DataMD Processor",
            "version": "1.0.0",
            "environment": "production",
        },
        "features": {
            "ocr_enabled": True,
            "pdf_processing": True,
            "video_support": True,
            "excel_formats": ["xlsx", "xls", "xlsm", "ods"],
        },
        "limits": {
            "max_file_size_mb": 100,
            "max_pages_pdf": 50,
            "supported_languages": ["eng", "spa", "fra", "deu", "ind"],
        },
        "processing": {
            "default_csv_separator": ",",
            "default_pdf_strategy": "lines",
            "default_ocr_language": "eng",
            "video_thumb_width": 320,
            "video_thumb_height": 240,
        },
        "performance": {
            "chunk_size": 10000,
            "max_memory_mb": 100,
            "streaming_threshold_mb": 10,
        },
        "security": {
            "allow_directory_traversal": False,
            "max_filename_length": 255,
            "allowed_file_extensions": [
                ".csv",
                ".json",
                ".xlsx",
                ".xls",
                ".xlsm",
                ".ods",
                ".pdf",
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".bmp",
                ".mp4",
                ".avi",
                ".mov",
                ".wmv",
            ],
        },
    }

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_file (str, optional): Path to JSON configuration file
        """
        self.config_file = config_file
        self._config = self.DEFAULTS.copy()
        self._load_config()

    def _load_config(self):
        """Load configuration from file and environment variables."""
        # Load from file if provided
        if self.config_file and os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    file_config = json.load(f)
                self._merge_config(file_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")

        # Load from environment variables
        self._load_from_environment()

    def _merge_config(self, new_config: Dict[str, Any]):
        """
        Merge new configuration with existing config.

        Args:
            new_config (dict): New configuration to merge
        """
        for section, section_config in new_config.items():
            if section in self._config:
                # Merge sections
                if isinstance(section_config, dict):
                    self._config[section].update(section_config)
                else:
                    self._config[section] = section_config
            else:
                # Add new section
                self._config[section] = section_config

    def _load_from_environment(self):
        """Load configuration from environment variables."""
        # Application settings
        env_app_name = os.environ.get("DATAMD_APP_NAME")
        if env_app_name:
            self._config["application"]["name"] = env_app_name

        env_app_version = os.environ.get("DATAMD_APP_VERSION")
        if env_app_version:
            self._config["application"]["version"] = env_app_version

        env_environment = os.environ.get("DATAMD_ENVIRONMENT")
        if env_environment:
            self._config["application"]["environment"] = env_environment

        # Feature settings
        env_ocr_enabled = os.environ.get("DATAMD_OCR_ENABLED")
        if env_ocr_enabled is not None:
            self._config["features"]["ocr_enabled"] = env_ocr_enabled.lower() in (
                "true",
                "1",
                "yes",
            )

        env_pdf_processing = os.environ.get("DATAMD_PDF_PROCESSING")
        if env_pdf_processing is not None:
            self._config["features"]["pdf_processing"] = env_pdf_processing.lower() in (
                "true",
                "1",
                "yes",
            )

        env_video_support = os.environ.get("DATAMD_VIDEO_SUPPORT")
        if env_video_support is not None:
            self._config["features"]["video_support"] = env_video_support.lower() in (
                "true",
                "1",
                "yes",
            )

        # Limit settings
        env_max_file_size = os.environ.get("DATAMD_MAX_FILE_SIZE_MB")
        if env_max_file_size and env_max_file_size.isdigit():
            self._config["limits"]["max_file_size_mb"] = int(env_max_file_size)

        env_max_pages_pdf = os.environ.get("DATAMD_MAX_PAGES_PDF")
        if env_max_pages_pdf and env_max_pages_pdf.isdigit():
            self._config["limits"]["max_pages_pdf"] = int(env_max_pages_pdf)

        # Processing settings
        env_default_csv_sep = os.environ.get("DATAMD_DEFAULT_CSV_SEPARATOR")
        if env_default_csv_sep:
            self._config["processing"]["default_csv_separator"] = env_default_csv_sep

        env_default_pdf_strategy = os.environ.get("DATAMD_DEFAULT_PDF_STRATEGY")
        if env_default_pdf_strategy:
            self._config["processing"][
                "default_pdf_strategy"
            ] = env_default_pdf_strategy

        env_default_ocr_lang = os.environ.get("DATAMD_DEFAULT_OCR_LANGUAGE")
        if env_default_ocr_lang:
            self._config["processing"]["default_ocr_language"] = env_default_ocr_lang

        # Security settings
        env_allow_traversal = os.environ.get("DATAMD_ALLOW_DIRECTORY_TRAVERSAL")
        if env_allow_traversal is not None:
            self._config["security"][
                "allow_directory_traversal"
            ] = env_allow_traversal.lower() in ("true", "1", "yes")

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key_path (str): Dot-separated path to configuration value
                           (e.g., "features.ocr_enabled")
            default (Any): Default value if key is not found

        Returns:
            Any: Configuration value or default
        """
        keys = key_path.split(".")
        value = self._config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation.

        Args:
            key_path (str): Dot-separated path to configuration value
            value (Any): Value to set
        """
        keys = key_path.split(".")
        config_section = self._config

        # Navigate to the parent section
        for key in keys[:-1]:
            if key not in config_section:
                config_section[key] = {}
            config_section = config_section[key]

        # Set the value
        config_section[keys[-1]] = value

    def get_application_name(self) -> str:
        """Get application name."""
        return self.get("application.name", "DataMD Processor")

    def get_application_version(self) -> str:
        """Get application version."""
        return self.get("application.version", "1.0.0")

    def is_feature_enabled(self, feature: str) -> bool:
        """
        Check if a feature is enabled.

        Args:
            feature (str): Feature name (ocr_enabled, pdf_processing, video_support)

        Returns:
            bool: True if feature is enabled
        """
        return self.get(f"features.{feature}", False)

    def get_supported_excel_formats(self) -> List[str]:
        """Get list of supported Excel formats."""
        return self.get("features.excel_formats", [])

    def get_max_file_size_mb(self) -> int:
        """Get maximum allowed file size in MB."""
        return self.get("limits.max_file_size_mb", 100)

    def get_max_pdf_pages(self) -> int:
        """Get maximum allowed PDF pages."""
        return self.get("limits.max_pages_pdf", 50)

    def get_supported_languages(self) -> List[str]:
        """Get list of supported OCR languages."""
        return self.get("limits.supported_languages", ["eng"])

    def get_default_csv_separator(self) -> str:
        """Get default CSV separator."""
        return self.get("processing.default_csv_separator", ",")

    def get_default_pdf_strategy(self) -> str:
        """Get default PDF table extraction strategy."""
        return self.get("processing.default_pdf_strategy", "lines")

    def get_default_ocr_language(self) -> str:
        """Get default OCR language."""
        return self.get("processing.default_ocr_language", "eng")

    def get_video_thumb_dimensions(self) -> tuple:
        """Get default video thumbnail dimensions."""
        width = self.get("processing.video_thumb_width", 320)
        height = self.get("processing.video_thumb_height", 240)
        return (width, height)

    def get_chunk_size(self) -> int:
        """Get default chunk size for streaming processing."""
        return self.get("performance.chunk_size", 10000)

    def get_max_memory_mb(self) -> int:
        """Get maximum memory usage for processing in MB."""
        return self.get("performance.max_memory_mb", 100)

    def get_streaming_threshold_mb(self) -> int:
        """Get file size threshold for switching to streaming mode in MB."""
        return self.get("performance.streaming_threshold_mb", 10)

    def is_directory_traversal_allowed(self) -> bool:
        """Check if directory traversal is allowed (security setting)."""
        return self.get("security.allow_directory_traversal", False)

    def get_allowed_file_extensions(self) -> List[str]:
        """Get list of allowed file extensions."""
        return self.get("security.allowed_file_extensions", [])

    def get_max_filename_length(self) -> int:
        """Get maximum allowed filename length."""
        return self.get("security.max_filename_length", 255)

    def to_dict(self) -> Dict[str, Any]:
        """
        Get complete configuration as dictionary.

        Returns:
            dict: Complete configuration
        """
        return self._config.copy()

    def save_to_file(self, filepath: str):
        """
        Save current configuration to JSON file.

        Args:
            filepath (str): Path to save configuration file
        """
        try:
            with open(filepath, "w") as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            raise IOError(f"Could not save configuration to {filepath}: {e}")


# Global configuration instance
_config_instance = None


def get_config(config_file: Optional[str] = None) -> Configuration:
    """
    Get singleton configuration instance.

    Args:
        config_file (str, optional): Path to JSON configuration file

    Returns:
        Configuration: Configuration instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Configuration(config_file)
    return _config_instance


def reset_config():
    """Reset configuration singleton instance."""
    global _config_instance
    _config_instance = None
