import hashlib
import os
import pickle
from pathlib import Path
from typing import Any, Dict, Optional


class CacheManager:
    """
    Cache manager for DataMD application.

    Provides file-based caching with automatic invalidation based on file
    modification times.
    """

    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize cache manager.

        Args:
            cache_dir (str, optional): Directory to store cache files.
                                     If None, uses ~/.cache/datamd or ./cache
        """
        if cache_dir is None:
            # Try to use user cache directory
            home = Path.home()
            if home.name != "root":  # Avoid root user cache
                cache_dir = home / ".cache" / "datamd"
            else:
                # Fallback to local cache directory
                cache_dir = Path("./cache")

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, file_path: str, **kwargs) -> str:
        """
        Generate a cache key based on file path and parameters.

        Args:
            file_path (str): Path to the file
            **kwargs: Additional parameters that affect caching

        Returns:
            str: Cache key
        """
        # Create a hash of the file path and parameters
        hash_input = file_path
        for key, value in sorted(kwargs.items()):
            hash_input += f"|{key}={value}"

        return hashlib.md5(hash_input.encode()).hexdigest()

    def _get_cache_file_path(self, cache_key: str) -> Path:
        """
        Get the path to the cache file.

        Args:
            cache_key (str): Cache key

        Returns:
            Path: Path to cache file
        """
        return self.cache_dir / f"{cache_key}.cache"

    def _is_cache_valid(self, cache_file: Path, source_file: str) -> bool:
        """
        Check if cache is valid (not expired and source file hasn't changed).

        Args:
            cache_file (Path): Path to cache file
            source_file (str): Path to source file

        Returns:
            bool: True if cache is valid
        """
        print(f"Validating cache: cache_file={cache_file}, source_file={source_file}")
        print(f"Cache file exists: {cache_file.exists()}")

        if not cache_file.exists():
            return False

        # If source file doesn't exist, we can't validate the cache
        # Check if the source_file is a real file path or a prefixed key
        source_exists = os.path.exists(source_file)
        print(f"Source file exists: {source_exists}")

        if not source_exists:
            # Try to extract actual file path from prefixed key
            # Look for common prefixes and extract the file path part
            prefixes = [
                "csv:",
                "json:",
                "excel:",
                "pdf:",
                "pdf_table:",
                "ocr:",
                "video:",
                "test:",
            ]
            actual_file_path = source_file
            for prefix in prefixes:
                if source_file.startswith(prefix):
                    actual_file_path = source_file[len(prefix) :]
                    # Try to find the first colon or space to separate the file
                    # path from other parameters
                    separators = [":", " "]
                    for sep in separators:
                        if sep in actual_file_path:
                            actual_file_path = actual_file_path.split(sep, 1)[0]
                    break

            # Check if the extracted path exists
            source_exists = os.path.exists(actual_file_path)
            print(f"Extracted file path: {actual_file_path}, exists: {source_exists}")

            if not source_exists:
                # In this case, we'll assume the cache is valid if it exists
                # This allows caching of processed data even if source is
                # temporarily unavailable
                return True

        # If we have a valid source file path, check modification times
        try:
            cache_mtime = cache_file.stat().st_mtime
            source_mtime = os.path.getmtime(
                actual_file_path if "actual_file_path" in locals() else source_file
            )
            result = cache_mtime > source_mtime
            print(
                f"Cache validation: cache_mtime={cache_mtime}, "
                f"source_mtime={source_mtime}, valid={result}"
            )
            return result
        except OSError as e:
            print(f"Error getting modification times: {e}")
            # If we can't get modification times, assume cache is valid
            return True

    def get(self, file_path: str, **kwargs) -> Optional[Any]:
        """
        Get cached data for a file.

        Args:
            file_path (str): Path to the file
            **kwargs: Additional parameters that affect caching

        Returns:
            Any: Cached data or None if not found or invalid
        """
        cache_key = self._get_cache_key(file_path, **kwargs)
        cache_file = self._get_cache_file_path(cache_key)

        # Check if cache is valid
        is_valid = self._is_cache_valid(cache_file, file_path)
        print(
            f"Cache GET: file_path={file_path}, cache_key={cache_key}, valid={is_valid}"
        )

        if not is_valid:
            return None

        # Load cached data
        try:
            with open(cache_file, "rb") as f:
                data = pickle.load(f)
            return data
        except (pickle.PickleError, IOError, EOFError):
            # If cache is corrupted, remove it
            try:
                cache_file.unlink()
            except OSError:
                pass
            return None

    def set(self, file_path: str, data: Any, **kwargs) -> bool:
        """
        Cache data for a file.

        Args:
            file_path (str): Path to the file
            data (Any): Data to cache
            **kwargs: Additional parameters that affect caching

        Returns:
            bool: True if caching was successful
        """
        cache_key = self._get_cache_key(file_path, **kwargs)
        cache_file = self._get_cache_file_path(cache_key)

        print(f"Cache SET: file_path={file_path}, cache_key={cache_key}")

        try:
            # Serialize and save data
            with open(cache_file, "wb") as f:
                pickle.dump(data, f)
            return True
        except (pickle.PickleError, IOError):
            return False

    def clear(self) -> bool:
        """
        Clear all cached data.

        Returns:
            bool: True if clearing was successful
        """
        try:
            for cache_file in self.cache_dir.glob("*.cache"):
                cache_file.unlink()
            return True
        except OSError:
            return False

    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about the cache.

        Returns:
            dict: Cache information
        """
        cache_files = list(self.cache_dir.glob("*.cache"))
        total_size = sum(f.stat().st_size for f in cache_files if f.exists())

        return {
            "cache_dir": str(self.cache_dir),
            "cache_files": len(cache_files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
        }


# Global cache manager instance
_cache_manager = None


def get_cache_manager(cache_dir: Optional[str] = None) -> CacheManager:
    """
    Get singleton cache manager instance.

    Args:
        cache_dir (str, optional): Directory to store cache files

    Returns:
        CacheManager: Cache manager instance
    """
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager(cache_dir)
    return _cache_manager


def reset_cache():
    """Reset cache manager singleton instance."""
    global _cache_manager
    _cache_manager = None
