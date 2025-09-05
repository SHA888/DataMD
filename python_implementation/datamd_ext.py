import json
import os
import re
import sys
from pathlib import Path

# Add the parent directory to the path for direct execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import pandas as pd
import pdfplumber
import pytesseract
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from PIL import Image

# Try to import moviepy - handle cases where it might not be available
try:
    from moviepy.video.io.VideoFileClip import VideoFileClip

    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    VideoFileClip = None

# Try to import matplotlib for chart generation
try:
    import matplotlib
    import matplotlib.pyplot as plt

    # Use non-interactive backend for server environments
    matplotlib.use("Agg")
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None

# Import configuration, data transformation, and caching
try:
    from .cache import get_cache_manager
    from .config import get_config
    from .data_transform import apply_transformations
except (ImportError, ValueError):  # pragma: no cover
    # When running directly
    from cache import get_cache_manager
    from data_transform import apply_transformations

    from config import get_config

# Get configuration and cache manager instances
config = get_config()
cache_manager = get_cache_manager()


def resolve_secure_path(file_path, base_dir=None):
    """
    Resolve a file path securely, preventing directory traversal attacks.

    Args:
        file_path (str): The file path to resolve
        base_dir (str, optional): The base directory to resolve relative paths
                                 against. If None, uses the current working
                                 directory.

    Returns:
        Path: The resolved secure path

    Raises:
        ValueError: If the path is invalid or attempts directory traversal
        FileNotFoundError: If the file doesn't exist
    """
    if base_dir is None:
        base_dir = os.getcwd()

    # Convert to Path objects
    base_path = Path(base_dir).resolve()
    target_path = Path(file_path)

    # Handle absolute paths - they must be within the base directory
    if target_path.is_absolute():
        resolved_path = target_path.resolve()
        try:
            # Check if the resolved path is within the base directory
            resolved_path.relative_to(base_path)
        except ValueError:
            error_msg = (
                f"Access to path outside of working directory is not allowed: "
                f"{file_path}"
            )
            raise ValueError(error_msg)
    else:
        # Handle relative paths
        resolved_path = (base_path / target_path).resolve()
        try:
            # Check if the resolved path is within the base directory
            resolved_path.relative_to(base_dir)
        except ValueError:
            raise ValueError(f"Path traversal attempt detected: {file_path}")

    # Check if file exists
    if not resolved_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return resolved_path


def sanitize_numeric_input(value, min_val=None, max_val=None, default=None):
    """
    Sanitize numeric input with optional min/max constraints.

    Args:
        value (str): The input value to sanitize
        min_val (float, optional): Minimum allowed value
        max_val (float, optional): Maximum allowed value
        default: Default value if input is invalid

    Returns:
        float or int: Sanitized numeric value, or default if invalid
    """
    if not value:
        return default

    try:
        # Try to convert to float first
        num_value = float(value)

        # Apply constraints
        if min_val is not None and num_value < min_val:
            num_value = min_val
        if max_val is not None and num_value > max_val:
            num_value = max_val

        # Return as int if it's a whole number
        if isinstance(num_value, float) and num_value.is_integer():
            return int(num_value)
        return num_value
    except (ValueError, TypeError):
        return default


def sanitize_boolean_input(value, default=False):
    """
    Sanitize boolean input.

    Args:
        value (str): The input value to sanitize
        default (bool): Default value if input is invalid

    Returns:
        bool: Sanitized boolean value
    """
    if not value:
        return default

    # If value is provided, check if it's in the true values list
    if value.lower() in ("true", "1", "yes", "on", "enabled"):
        return True
    elif value.lower() in ("false", "0", "no", "off", "disabled"):
        return False
    else:
        # If it's not a recognized boolean value, return the default
        return default


def sanitize_string_input(value, max_length=1000, allowed_chars=None):
    """
    Sanitize string input with length and character constraints.

    Args:
        value (str): The input value to sanitize
        max_length (int): Maximum allowed length
        allowed_chars (str, optional): String of allowed characters

    Returns:
        str: Sanitized string value
    """
    if not value:
        return ""

    # Truncate if too long
    if len(value) > max_length:
        value = value[:max_length]

    # Filter characters if specified
    if allowed_chars:
        value = "".join(c for c in value if c in allowed_chars)

    return value


def sanitize_language_code(lang_code):
    """
    Sanitize language code for OCR.

    Args:
        lang_code (str): The language code to sanitize

    Returns:
        str: Sanitized language code (default: 'eng')
    """
    if not lang_code:
        return config.get_default_ocr_language()

    # Check against supported languages
    supported_langs = config.get_supported_languages()
    if lang_code in supported_langs:
        return lang_code
    return config.get_default_ocr_language()


def sanitize_sheet_name(sheet):
    """
    Sanitize sheet name/index for Excel files.

    Args:
        sheet (str): The sheet name or index

    Returns:
        str or int: Sanitized sheet name or index
    """
    if not sheet:
        return 0

    # If it's a digit, treat as index
    if sheet.isdigit():
        return int(sheet)

    # For sheet names, sanitize but allow most characters
    return sanitize_string_input(sheet, max_length=31)  # Excel sheet name limit


def sanitize_strategy(strategy):
    """
    Sanitize PDF table extraction strategy.

    Args:
        strategy (str): The strategy to sanitize

    Returns:
        str: Sanitized strategy (default: 'lines')
    """
    if not strategy:
        return config.get_default_pdf_strategy()

    valid_strategies = {"lines", "text", "explicit"}
    if strategy in valid_strategies:
        return strategy
    return config.get_default_pdf_strategy()


def sanitize_chart_type(chart_type):
    """
    Sanitize chart type for chart generation.

    Args:
        chart_type (str): The chart type to sanitize

    Returns:
        str: Sanitized chart type (default: 'bar')
    """
    if not chart_type:
        return "bar"

    valid_chart_types = {"bar", "line", "pie", "scatter", "histogram"}
    if chart_type.lower() in valid_chart_types:
        return chart_type.lower()
    return "bar"


def sanitize_chart_options(options_str):
    """
    Sanitize chart options string.

    Args:
        options_str (str): Chart options string in format "key1=value1,key2=value2"

    Returns:
        dict: Dictionary of chart options
    """
    if not options_str:
        return {}

    options = {}
    pairs = options_str.split(",")
    for pair in pairs:
        if "=" in pair:
            key, value = pair.split("=", 1)
            key = key.strip().lower()
            value = value.strip()

            # Convert numeric values
            if value.isdigit():
                value = int(value)
            elif value.replace(".", "").isdigit():
                value = float(value)
            elif value.lower() in ("true", "false"):
                value = value.lower() == "true"

            options[key] = value

    return options


def read_csv_chunked(file_path, chunk_size=10000, **kwargs):
    """
    Read CSV file in chunks to reduce memory usage for large files.

    Args:
        file_path (str): Path to CSV file
        chunk_size (int): Number of rows per chunk
        **kwargs: Additional arguments for pd.read_csv

    Yields:
        pd.DataFrame: Chunks of the CSV file
    """
    try:
        for chunk in pd.read_csv(file_path, chunksize=chunk_size, **kwargs):
            yield chunk
    except Exception as e:
        raise Exception(f"Error reading CSV file in chunks: {str(e)}")


def read_excel_chunked(file_path, sheet_name=0, chunk_size=10000, engine="openpyxl"):
    """
    Read Excel file in chunks (simplified implementation).

    Args:
        file_path (str): Path to Excel file
        sheet_name (str or int): Sheet name or index
        chunk_size (int): Number of rows per chunk
        engine (str): Excel engine to use

    Yields:
        pd.DataFrame: Chunks of the Excel file
    """
    # For Excel, we'll read the entire file but process in chunks
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine=engine)

    # Split into chunks
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i : i + chunk_size]


def process_large_csv(file_path, sep=",", transform="", max_memory_mb=100):
    """
    Process large CSV files with memory optimization.

    Args:
        file_path (str): Path to CSV file
        sep (str): CSV separator
        transform (str): Transformation string
        max_memory_mb (int): Maximum memory usage in MB

    Returns:
        str: Markdown representation of processed data
    """
    # Estimate chunk size based on max memory
    # Rough estimate: 1000 rows ≈ 1MB for typical data
    chunk_size = max(1000, int(max_memory_mb * 1000 / 100))

    try:
        # Process first chunk to get column structure
        first_chunk = next(read_csv_chunked(file_path, chunk_size=chunk_size, sep=sep))

        # Apply transformations if specified (on first chunk for preview)
        if transform:
            first_chunk = apply_transformations(first_chunk, transform)

        # For large files, we might want to just show a sample or summary
        # Here we'll show the first few rows as a preview
        if len(first_chunk) > 100:
            # Show only first 100 rows for large files
            preview_df = first_chunk.head(100)
            markdown_result = preview_df.to_markdown(index=False)
            markdown_result += (
                f"\n\n*Note: Large file detected. Showing first 100 rows. "
                f"Total rows: {len(first_chunk)}*"
            )
        else:
            markdown_result = first_chunk.to_markdown(index=False)

        return markdown_result
    except StopIteration:
        # Empty file
        return "Empty CSV file"
    except Exception as e:
        raise Exception(f"Error processing large CSV file: {str(e)}")


def process_large_excel(
    file_path, sheet_name=0, transform="", engine="openpyxl", max_memory_mb=100
):
    """
    Process large Excel files with memory optimization.

    Args:
        file_path (str): Path to Excel file
        sheet_name (str or int): Sheet name or index
        transform (str): Transformation string
        engine (str): Excel engine to use
        max_memory_mb (int): Maximum memory usage in MB

    Returns:
        str: Markdown representation of processed data
    """
    try:
        # Process first chunk to get column structure
        first_chunk = next(
            read_excel_chunked(file_path, sheet_name=sheet_name, engine=engine)
        )

        # Apply transformations if specified
        if transform:
            first_chunk = apply_transformations(first_chunk, transform)

        # For large files, show a preview
        if len(first_chunk) > 100:
            # Show only first 100 rows for large files
            preview_df = first_chunk.head(100)
            markdown_result = preview_df.to_markdown(index=False)
            markdown_result += (
                f"\n\n*Note: Large file detected. Showing first 100 rows. "
                f"Total rows: {len(first_chunk)}*"
            )
        else:
            markdown_result = first_chunk.to_markdown(index=False)

        return markdown_result
    except StopIteration:
        # Empty file
        return "Empty Excel file"
    except Exception as e:
        raise Exception(f"Error processing large Excel file: {str(e)}")


class DataMDPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        for line in lines:
            # Match shortcode pattern: {{ command "file" arg1 arg2 }}
            match = re.match(r'\{\{\s*(\w+)\s+"([^"]+)"(?:\s+([^}]*))?\s*\}\}', line)
            if match:
                cmd = match.group(1)
                file_path = match.group(2)
                args = match.group(3).split() if match.group(3) else []

                try:
                    # Resolve the file path securely
                    try:
                        secure_path = resolve_secure_path(file_path)
                    except (ValueError, FileNotFoundError) as e:
                        new_lines.append(f"Error: {str(e)}")
                        continue

                    if cmd == "csv":
                        sep = sanitize_string_input(
                            args[0] if args else config.get_default_csv_separator(),
                            max_length=10,
                        )
                        transform = sanitize_string_input(
                            " ".join(args[1:]) if len(args) > 1 else "", max_length=1000
                        )

                        # Check file size for large file handling
                        file_size_mb = secure_path.stat().st_size / (1024 * 1024)
                        max_file_size_mb = config.get_max_file_size_mb()

                        # Try to get from cache first
                        cache_key = f"csv:{secure_path}:{sep}:{transform}"
                        df = cache_manager.get(
                            str(secure_path), sep=sep, transform=transform
                        )

                        if df is None:
                            if file_size_mb > max_file_size_mb:
                                # Use large file processing
                                df = process_large_csv(
                                    str(secure_path),
                                    sep=sep,
                                    transform=transform,
                                    max_memory_mb=max_file_size_mb,
                                )
                            else:
                                # Normal processing
                                df = pd.read_csv(secure_path, sep=sep)
                                # Apply transformations if specified
                                if transform:
                                    df = apply_transformations(df, transform)
                            # Cache the result
                            cache_manager.set(
                                str(secure_path), df, sep=sep, transform=transform
                            )

                        # Handle string result from large file processing
                        if isinstance(df, str):
                            new_lines.append(df)
                        else:
                            new_lines.append(df.to_markdown(index=False))

                    elif cmd == "json":
                        flatten = sanitize_boolean_input(args[0] if args else False)
                        transform = sanitize_string_input(
                            " ".join(args[1:]) if len(args) > 1 else "", max_length=1000
                        )

                        # Check file size for large file handling
                        file_size_mb = secure_path.stat().st_size / (1024 * 1024)
                        max_file_size_mb = config.get_max_file_size_mb()

                        # Try to get from cache first
                        cache_key = f"json:{secure_path}:{flatten}:{transform}"
                        result = cache_manager.get(
                            str(secure_path), flatten=flatten, transform=transform
                        )

                        if result is None:
                            if file_size_mb > max_file_size_mb:
                                # For large JSON files, we might want to implement
                                # streaming. For now, we'll just add a warning
                                with open(secure_path, "r") as f:
                                    data = json.load(f)

                                if isinstance(data, list):
                                    df = pd.json_normalize(data)
                                    # Apply transformations if specified
                                    if transform:
                                        df = apply_transformations(df, transform)
                                    # For large files, show preview
                                    if len(df) > 1000:
                                        preview_df = df.head(100)
                                        result = preview_df.to_markdown(index=False)
                                        result += (
                                            f"\n\n*Note: Large JSON file detected. "
                                            f"Showing first 100 records. "
                                            f"Total records: {len(df)}*"
                                        )
                                    else:
                                        result = df.to_markdown(index=False)
                                elif isinstance(data, dict):
                                    if flatten:
                                        df = pd.json_normalize([data])
                                        # Apply transformations if specified
                                        if transform:
                                            df = apply_transformations(df, transform)
                                        result = df.to_markdown(index=False)
                                    else:
                                        result = (
                                            "```json\n"
                                            + json.dumps(data, indent=2)
                                            + "\n```"
                                        )
                                else:
                                    result = f"JSON content: {data}"
                            else:
                                # Normal processing
                                with open(secure_path, "r") as f:
                                    data = json.load(f)

                                if isinstance(data, list):
                                    df = pd.json_normalize(data)
                                    # Apply transformations if specified
                                    if transform:
                                        df = apply_transformations(df, transform)
                                    result = df.to_markdown(index=False)
                                elif isinstance(data, dict):
                                    if flatten:
                                        df = pd.json_normalize([data])
                                        # Apply transformations if specified
                                        if transform:
                                            df = apply_transformations(df, transform)
                                        result = df.to_markdown(index=False)
                                    else:
                                        result = (
                                            "```json\n"
                                            + json.dumps(data, indent=2)
                                            + "\n```"
                                        )
                                else:
                                    result = f"JSON content: {data}"
                            # Cache the result
                            cache_manager.set(
                                str(secure_path),
                                result,
                                flatten=flatten,
                                transform=transform,
                            )

                        new_lines.append(result)

                    elif cmd in ["xlsx", "xls", "xlsm", "ods"]:
                        # Check if this format is enabled
                        if not config.is_feature_enabled("excel_support"):
                            new_lines.append("Error: Excel processing is disabled")
                            continue

                        sheet = sanitize_sheet_name(args[0] if args else 0)
                        transform = sanitize_string_input(
                            " ".join(args[1:]) if len(args) > 1 else "", max_length=1000
                        )
                        engine = "openpyxl"
                        if cmd == "xls":
                            engine = "xlrd"
                        elif cmd == "ods":
                            engine = "odf"

                        # Check file size for large file handling
                        file_size_mb = secure_path.stat().st_size / (1024 * 1024)
                        max_file_size_mb = config.get_max_file_size_mb()

                        # Try to get from cache first
                        cache_key = f"excel:{secure_path}:{sheet}:{engine}:{transform}"
                        df = cache_manager.get(
                            str(secure_path),
                            sheet=sheet,
                            engine=engine,
                            transform=transform,
                        )

                        if df is None:
                            if file_size_mb > max_file_size_mb:
                                # Use large file processing
                                df = process_large_excel(
                                    str(secure_path),
                                    sheet_name=sheet,
                                    transform=transform,
                                    engine=engine,
                                    max_memory_mb=max_file_size_mb,
                                )
                            else:
                                # Normal processing
                                df = pd.read_excel(
                                    secure_path, sheet_name=sheet, engine=engine
                                )
                                # Apply transformations if specified
                                if transform:
                                    df = apply_transformations(df, transform)
                            # Cache the result
                            cache_manager.set(
                                str(secure_path),
                                df,
                                sheet=sheet,
                                engine=engine,
                                transform=transform,
                            )

                        # Handle string result from large file processing
                        if isinstance(df, str):
                            new_lines.append(df)
                        else:
                            new_lines.append(df.to_markdown(index=False))

                    elif cmd == "pdf":
                        # Check if PDF processing is enabled
                        if not config.is_feature_enabled("pdf_processing"):
                            new_lines.append("Error: PDF processing is disabled")
                            continue

                        pages = sanitize_string_input(
                            args[0] if args else "all", max_length=20
                        )

                        # Try to get from cache first
                        cache_key = f"pdf:{secure_path}:{pages}"
                        text = cache_manager.get(str(secure_path), pages=pages)

                        if text is None:
                            with pdfplumber.open(secure_path) as pdf:
                                if pages == "all":
                                    text = "\n\n".join(
                                        page.extract_text() or "" for page in pdf.pages
                                    )
                                else:
                                    page_num = (
                                        int(
                                            sanitize_numeric_input(
                                                pages, min_val=1, default=1
                                            )
                                        )
                                        - 1
                                    )
                                    text = pdf.pages[page_num].extract_text() or ""
                            # Cache the result
                            cache_manager.set(str(secure_path), text, pages=pages)
                        new_lines.append(text.strip())

                    elif cmd == "pdf_table":
                        # Check if PDF processing is enabled
                        if not config.is_feature_enabled("pdf_processing"):
                            new_lines.append("Error: PDF processing is disabled")
                            continue

                        # Parse arguments for pdf_table
                        page = (
                            int(sanitize_numeric_input(args[0], min_val=1, default=1))
                            - 1
                            if args and args[0]
                            else 0
                        )
                        horizontal_strategy = sanitize_strategy(
                            args[1]
                            if len(args) > 1
                            else config.get_default_pdf_strategy()
                        )
                        vertical_strategy = sanitize_strategy(
                            args[2]
                            if len(args) > 2
                            else config.get_default_pdf_strategy()
                        )

                        # Parse threshold parameters (new feature)
                        snap_tolerance = None
                        edge_tolerance = None
                        intersection_tolerance = None

                        # Look for threshold parameters in the remaining arguments
                        for i in range(3, len(args)):
                            if args[i].startswith("snap=") and len(args[i]) > 5:
                                try:
                                    snap_tolerance = sanitize_numeric_input(
                                        args[i][5:], min_val=0, max_val=100
                                    )
                                except (ValueError, TypeError):
                                    pass
                            elif args[i].startswith("edge=") and len(args[i]) > 5:
                                try:
                                    edge_tolerance = sanitize_numeric_input(
                                        args[i][5:], min_val=0, max_val=100
                                    )
                                except (ValueError, TypeError):
                                    pass
                            elif args[i].startswith("intersect=") and len(args[i]) > 10:
                                try:
                                    intersection_tolerance = sanitize_numeric_input(
                                        args[i][10:], min_val=0, max_val=100
                                    )
                                except (ValueError, TypeError):
                                    pass

                        # Prepare table settings with threshold parameters
                        table_settings = {
                            "horizontal_strategy": horizontal_strategy,
                            "vertical_strategy": vertical_strategy,
                        }

                        # Add threshold parameters if provided
                        if snap_tolerance is not None:
                            table_settings["snap_tolerance"] = snap_tolerance
                        if edge_tolerance is not None:
                            table_settings["edge_tolerance"] = edge_tolerance
                        if intersection_tolerance is not None:
                            table_settings["intersection_tolerance"] = (
                                intersection_tolerance
                            )

                        # Try to get from cache first
                        cache_key = (
                            f"pdf_table:{secure_path}:{page}:{horizontal_strategy}:"
                            f"{vertical_strategy}"
                        )
                        if snap_tolerance is not None:
                            cache_key += f":snap={snap_tolerance}"
                        if edge_tolerance is not None:
                            cache_key += f":edge={edge_tolerance}"
                        if intersection_tolerance is not None:
                            cache_key += f":intersect={intersection_tolerance}"

                        tables_result = cache_manager.get(
                            str(secure_path),
                            page=page,
                            horizontal_strategy=horizontal_strategy,
                            vertical_strategy=vertical_strategy,
                            snap_tolerance=snap_tolerance,
                            edge_tolerance=edge_tolerance,
                            intersection_tolerance=intersection_tolerance,
                        )

                        if tables_result is None:
                            with pdfplumber.open(secure_path) as pdf:
                                # Use strategy parameters and threshold parameters
                                # for table extraction
                                tables = pdf.pages[page].extract_tables(table_settings)
                                if tables:
                                    tables_result = []
                                    for i, table in enumerate(tables):
                                        if table and len(table) > 1:
                                            df = pd.DataFrame(
                                                table[1:], columns=table[0]
                                            )
                                            tables_result.append(f"### Table {i+1}")
                                            tables_result.append(
                                                df.to_markdown(index=False)
                                            )
                                            tables_result.append("")
                                else:
                                    tables_result = ["No tables found on this page."]
                            # Cache the result
                            cache_manager.set(
                                str(secure_path),
                                tables_result,
                                page=page,
                                horizontal_strategy=horizontal_strategy,
                                vertical_strategy=vertical_strategy,
                                snap_tolerance=snap_tolerance,
                                edge_tolerance=edge_tolerance,
                                intersection_tolerance=intersection_tolerance,
                            )

                        new_lines.extend(tables_result)

                    elif cmd == "image_ocr":
                        # Check if OCR is enabled
                        if not config.is_feature_enabled("ocr_enabled"):
                            new_lines.append("Error: OCR processing is disabled")
                            continue

                        lang = sanitize_language_code(
                            args[0] if args else config.get_default_ocr_language()
                        )

                        # Try to get from cache first
                        cache_key = f"ocr:{secure_path}:{lang}"
                        text = cache_manager.get(str(secure_path), lang=lang)

                        if text is None:
                            image = Image.open(secure_path)
                            text = pytesseract.image_to_string(image, lang=lang)
                            # Cache the result
                            cache_manager.set(str(secure_path), text, lang=lang)
                        new_lines.append(text.strip())

                    elif cmd == "video":
                        # Check if video support is enabled
                        if not config.is_feature_enabled("video_support"):
                            new_lines.append("Error: Video processing is disabled")
                            continue

                        width = sanitize_numeric_input(
                            args[0] if len(args) > 0 else "640",
                            min_val=1,
                            max_val=5000,
                            default=640,
                        )
                        height = sanitize_numeric_input(
                            args[1] if len(args) > 1 else "480",
                            min_val=1,
                            max_val=5000,
                            default=480,
                        )
                        controls = sanitize_boolean_input(
                            args[2] if len(args) > 2 else "true", default=True
                        )
                        autoplay = sanitize_boolean_input(
                            args[3] if len(args) > 3 else "false", default=False
                        )

                        controls_attr = " controls" if controls else ""
                        autoplay_attr = " autoplay" if autoplay else ""

                        video_html = (
                            f'<video width="{width}" height="{height}"'
                            f"{controls_attr}{autoplay_attr}>\n"
                            f'  <source src="{secure_path}" type="video/mp4">\n'
                            "  Your browser does not support the video tag.\n"
                            "</video>"
                        )
                        new_lines.append(video_html)

                    elif cmd == "video_thumb":
                        # Check if video support is enabled
                        if not config.is_feature_enabled("video_support"):
                            new_lines.append("Error: Video processing is disabled")
                            continue

                        # Check if moviepy is available
                        if not MOVIEPY_AVAILABLE:
                            new_lines.append(
                                "Error: moviepy not available for video "
                                + "thumbnail generation"
                            )
                            continue

                        # Extract time parameter (required)
                        if not args:
                            new_lines.append(
                                "Error: video_thumb requires time parameter"
                            )
                            continue

                        try:
                            time = sanitize_numeric_input(args[0], min_val=0, default=0)
                            width = sanitize_numeric_input(
                                args[1] if len(args) > 1 else None,
                                min_val=1,
                                max_val=5000,
                            )
                            height = sanitize_numeric_input(
                                args[2] if len(args) > 2 else None,
                                min_val=1,
                                max_val=5000,
                            )

                            # Generate thumbnail using moviepy
                            clip = VideoFileClip(str(secure_path))

                            # Extract frame at specified time
                            frame = clip.get_frame(t=time)

                            # Convert to PIL Image
                            image = Image.fromarray(frame)

                            # Resize if dimensions provided
                            if width or height:
                                if not width:
                                    # Calculate width to maintain aspect ratio
                                    aspect_ratio = image.width / image.height
                                    width = int(height * aspect_ratio)
                                elif not height:
                                    # Calculate height to maintain aspect ratio
                                    aspect_ratio = image.height / image.width
                                    height = int(width * aspect_ratio)
                                image = image.resize((width, height))

                            # Generate thumbnail filename
                            file_path_obj = Path(secure_path)
                            thumb_filename = f"{file_path_obj.stem}_thumb_{time}s.png"
                            thumb_path = file_path_obj.parent / thumb_filename

                            # Save thumbnail
                            image.save(thumb_path, "PNG")

                            # Generate markdown image tag
                            new_lines.append(
                                f"![Video Thumbnail at {time}s]({thumb_path})"
                            )

                            # Clean up
                            clip.close()

                        except Exception as e:
                            new_lines.append(f"Error generating thumbnail: {str(e)}")

                    elif cmd == "chart":
                        # Check if matplotlib is available
                        if not MATPLOTLIB_AVAILABLE:
                            error_msg = "Error: Chart generation requires matplotlib"
                            new_lines.append(error_msg)
                            continue

                        # Parse chart arguments
                        chart_type = sanitize_chart_type(args[0] if args else "bar")
                        x_column = sanitize_string_input(
                            args[1] if len(args) > 1 else "", max_length=100
                        )
                        y_column = sanitize_string_input(
                            args[2] if len(args) > 2 else "", max_length=100
                        )
                        options_str = " ".join(args[3:]) if len(args) > 3 else ""
                        options = sanitize_chart_options(options_str)

                        # Generate chart filename
                        file_path_obj = Path(secure_path)
                        chart_filename = f"{file_path_obj.stem}_chart_{chart_type}.png"
                        chart_path = file_path_obj.parent / chart_filename

                        # Try to get from cache first
                        cache_key = (
                            f"chart:{secure_path}:{chart_type}:{x_column}:"
                            f"{y_column}:{options_str}"
                        )
                        cached_chart_path = cache_manager.get(
                            str(secure_path),
                            chart_type=chart_type,
                            x_column=x_column,
                            y_column=y_column,
                            options=options_str,
                        )

                        if cached_chart_path is None or not os.path.exists(
                            cached_chart_path
                        ):
                            try:
                                # Read data
                                file_ext = secure_path.suffix.lower()
                                if file_ext == ".csv":
                                    df = pd.read_csv(secure_path)
                                elif file_ext in [".xlsx", ".xls", ".xlsm"]:
                                    engine = (
                                        "openpyxl" if file_ext != ".xls" else "xlrd"
                                    )
                                    df = pd.read_excel(secure_path, engine=engine)
                                elif file_ext == ".json":
                                    with open(secure_path, "r") as f:
                                        data = json.load(f)
                                    df = (
                                        pd.json_normalize(data)
                                        if isinstance(data, list)
                                        else pd.DataFrame([data])
                                    )
                                else:
                                    error_msg = (
                                        "Error: Unsupported file format for chart "
                                        "generation"
                                    )
                                    new_lines.append(error_msg)
                                    continue

                                # Apply transformations if specified in options
                                if "transform" in options:
                                    df = apply_transformations(df, options["transform"])

                                # Validate columns
                                if x_column and x_column not in df.columns:
                                    error_msg = (
                                        f"Error: X column '{x_column}' not found "
                                        f"in data"
                                    )
                                    new_lines.append(error_msg)
                                    continue
                                if y_column and y_column not in df.columns:
                                    error_msg = (
                                        f"Error: Y column '{y_column}' not found "
                                        f"in data"
                                    )
                                    new_lines.append(error_msg)
                                    continue

                                # Generate chart
                                plt.figure(figsize=(10, 6))

                                if chart_type == "bar":
                                    if x_column and y_column:
                                        df.plot(
                                            x=x_column,
                                            y=y_column,
                                            kind="bar",
                                            ax=plt.gca(),
                                        )
                                    elif y_column:
                                        df[y_column].plot(kind="bar", ax=plt.gca())
                                    else:
                                        df.plot(kind="bar", ax=plt.gca())
                                elif chart_type == "line":
                                    if x_column and y_column:
                                        df.plot(
                                            x=x_column,
                                            y=y_column,
                                            kind="line",
                                            ax=plt.gca(),
                                        )
                                    elif y_column:
                                        df[y_column].plot(kind="line", ax=plt.gca())
                                    else:
                                        df.plot(kind="line", ax=plt.gca())
                                elif chart_type == "pie":
                                    if y_column:
                                        if x_column:
                                            df.plot(
                                                x=x_column,
                                                y=y_column,
                                                kind="pie",
                                                ax=plt.gca(),
                                                ylabel="",
                                            )
                                        else:
                                            df[y_column].plot(
                                                kind="pie", ax=plt.gca(), ylabel=""
                                            )
                                    else:
                                        error_msg = (
                                            "Error: Pie charts require a Y column"
                                        )
                                        new_lines.append(error_msg)
                                        plt.close()
                                        continue
                                elif chart_type == "scatter":
                                    if x_column and y_column:
                                        df.plot(
                                            x=x_column,
                                            y=y_column,
                                            kind="scatter",
                                            ax=plt.gca(),
                                        )
                                    else:
                                        error_msg = (
                                            "Error: Scatter plots require both X "
                                            "and Y columns"
                                        )
                                        new_lines.append(error_msg)
                                        plt.close()
                                        continue
                                elif chart_type == "histogram":
                                    if y_column:
                                        df[y_column].plot(kind="hist", ax=plt.gca())
                                    else:
                                        # Use first numeric column
                                        numeric_cols = df.select_dtypes(
                                            include=["number"]
                                        ).columns
                                        if len(numeric_cols) > 0:
                                            df[numeric_cols[0]].plot(
                                                kind="hist", ax=plt.gca()
                                            )
                                        else:
                                            error_msg = (
                                                "Error: No numeric columns found "
                                                "for histogram"
                                            )
                                            new_lines.append(error_msg)
                                            plt.close()
                                            continue

                                # Apply customizations from options
                                if "title" in options:
                                    plt.title(options["title"])
                                if "xlabel" in options:
                                    plt.xlabel(options["xlabel"])
                                if "ylabel" in options:
                                    plt.ylabel(options["ylabel"])

                                # Generate chart with enhanced customization
                                figsize = (10, 6)
                                if "width" in options and "height" in options:
                                    figsize = (options["width"], options["height"])
                                elif "width" in options:
                                    figsize = (options["width"], figsize[1])
                                elif "height" in options:
                                    figsize = (figsize[0], options["height"])

                                plt.figure(figsize=figsize)

                                # Handle color parameter
                                color = options.get("color", None)

                                # Handle other styling options
                                alpha = options.get("alpha", 1.0)  # Transparency
                                linestyle = options.get(
                                    "linestyle", "-"
                                )  # Line style for line charts
                                marker = options.get(
                                    "marker", None
                                )  # Marker for line charts

                                if chart_type == "bar":
                                    if x_column and y_column:
                                        df.plot(
                                            x=x_column,
                                            y=y_column,
                                            kind="bar",
                                            ax=plt.gca(),
                                            color=color,
                                            alpha=alpha,
                                        )
                                    elif y_column:
                                        df[y_column].plot(
                                            kind="bar",
                                            ax=plt.gca(),
                                            color=color,
                                            alpha=alpha,
                                        )
                                    else:
                                        df.plot(
                                            kind="bar",
                                            ax=plt.gca(),
                                            color=color,
                                            alpha=alpha,
                                        )
                                elif chart_type == "line":
                                    if x_column and y_column:
                                        df.plot(
                                            x=x_column,
                                            y=y_column,
                                            kind="line",
                                            ax=plt.gca(),
                                            color=color,
                                            alpha=alpha,
                                            linestyle=linestyle,
                                            marker=marker,
                                        )
                                    elif y_column:
                                        df[y_column].plot(
                                            kind="line",
                                            ax=plt.gca(),
                                            color=color,
                                            alpha=alpha,
                                            linestyle=linestyle,
                                            marker=marker,
                                        )
                                    else:
                                        df.plot(
                                            kind="line",
                                            ax=plt.gca(),
                                            color=color,
                                            alpha=alpha,
                                            linestyle=linestyle,
                                            marker=marker,
                                        )
                                elif chart_type == "pie":
                                    if y_column:
                                        if x_column:
                                            df.plot(
                                                x=x_column,
                                                y=y_column,
                                                kind="pie",
                                                ax=plt.gca(),
                                                ylabel="",
                                                color=color,
                                            )
                                        else:
                                            df[y_column].plot(
                                                kind="pie",
                                                ax=plt.gca(),
                                                ylabel="",
                                                color=color,
                                            )
                                    else:
                                        error_msg = (
                                            "Error: Pie charts require a Y column"
                                        )
                                        new_lines.append(error_msg)
                                        plt.close()
                                        continue
                                elif chart_type == "scatter":
                                    if x_column and y_column:
                                        # Handle scatter plot specific options
                                        s = options.get("size", 20)  # Marker size
                                        df.plot(
                                            x=x_column,
                                            y=y_column,
                                            kind="scatter",
                                            ax=plt.gca(),
                                            color=color,
                                            alpha=alpha,
                                            s=s,
                                        )
                                    else:
                                        error_msg = (
                                            "Error: Scatter plots require both X "
                                            "and Y columns"
                                        )
                                        new_lines.append(error_msg)
                                        plt.close()
                                        continue
                                elif chart_type == "histogram":
                                    # Handle histogram specific options
                                    bins = options.get("bins", 10)  # Number of bins
                                    if y_column:
                                        df[y_column].plot(
                                            kind="hist",
                                            ax=plt.gca(),
                                            color=color,
                                            alpha=alpha,
                                            bins=bins,
                                        )
                                    else:
                                        # Use first numeric column
                                        numeric_cols = df.select_dtypes(
                                            include=["number"]
                                        ).columns
                                        if len(numeric_cols) > 0:
                                            df[numeric_cols[0]].plot(
                                                kind="hist",
                                                ax=plt.gca(),
                                                color=color,
                                                alpha=alpha,
                                                bins=bins,
                                            )
                                        else:
                                            error_msg = (
                                                "Error: No numeric columns found "
                                                "for histogram"
                                            )
                                            new_lines.append(error_msg)
                                            plt.close()
                                            continue

                                # Apply grid if requested
                                if options.get("grid", False):
                                    plt.grid(True)

                                # Save chart
                                plt.tight_layout()
                                plt.savefig(chart_path)
                                plt.close()

                                # Cache the chart path
                                cache_manager.set(
                                    str(secure_path),
                                    str(chart_path),
                                    chart_type=chart_type,
                                    x_column=x_column,
                                    y_column=y_column,
                                    options=options_str,
                                )

                                cached_chart_path = str(chart_path)
                            except Exception as e:
                                if plt:
                                    plt.close()
                                error_msg = f"Error generating chart: {str(e)}"
                                new_lines.append(error_msg)
                                continue

                        # Generate markdown image tag
                        alt_text = f"{chart_type.capitalize()} chart"
                        if "title" in options:
                            alt_text = options["title"]
                        new_lines.append(f"![{alt_text}]({cached_chart_path})")

                    else:
                        new_lines.append(
                            f"Unknown Data Markdown (DataMD) command: {cmd}"
                        )

                except Exception as e:
                    new_lines.append(
                        f"Error processing {cmd} file {file_path}: {str(e)}"
                    )

                continue

            new_lines.append(line)

        return new_lines


class DataMDExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(DataMDPreprocessor(md), "datamd", 175)


def makeExtension(**kwargs):
    return DataMDExtension(**kwargs)
