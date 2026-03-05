class DataMDError(Exception):
    """Base exception for DataMD errors."""


class FileResolutionError(DataMDError, ValueError):
    """Raised when resolving file paths fails or is unsafe."""


class ShortcodeError(DataMDError, RuntimeError):
    """Raised when processing a shortcode fails."""


class TransformError(DataMDError, ValueError):
    """Raised when data transformations fail."""
