#!/usr/bin/env python3
"""
Data Markdown (DataMD) Processor Script
Processes .dmd files using the Python-Markdown extension
"""

import argparse
import logging
import os
import sys
import time
from pathlib import Path

# Add the python_implementation directory to the path for direct execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import markdown

logger = logging.getLogger(__name__)

# Handle imports for both package and direct script execution
try:
    # When installed as a package (CLI path)
    from .config import get_config
    from .datamd_ext import DataMDExtension
    from .exceptions import ShortcodeError
except (ImportError, ValueError):  # pragma: no cover
    # When running the script directly (python python_implementation/process_dmd.py)
    from datamd_ext import DataMDExtension
    from exceptions import ShortcodeError

    from config import get_config


def process_dmd_file(
    input_file,
    output_file=None,
    output_format="html",
    style_options=None,
    verbose=False,
    chunk_size=None,
    max_memory_mb=None,
    strict=False,
):
    """Process a single .dmd file and convert to specified format"""

    if not os.path.exists(input_file):
        logger.error("File not found", extra={"input_file": input_file})
        return False

    if verbose:
        logger.info("Processing file", extra={"input_file": input_file})

    # Read the .dmd file
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        # Process with DataMD extension, include source path for contextual errors
        md = markdown.Markdown(extensions=[DataMDExtension(source_path=input_file)])
        html_content = md.convert(content)
    except Exception as exc:
        logger.error(
            "Shortcode processing failed",
            extra={"input_file": input_file, "error": str(exc)},
        )
        if strict:
            raise
        return False

    # Generate output filename if not provided
    if output_file is None:
        input_path = Path(input_file)
        if output_format == "html":
            output_file = input_path.with_suffix(".html")
        else:
            output_file = input_path.with_suffix(f".{output_format}")

    # Create output based on format
    if output_format == "html":
        # Apply style options
        body_style = (
            "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', "
            "Roboto, sans-serif; max-width: 800px; margin: 0 auto; "
            "padding: 20px; line-height: 1.6;"
        )
        table_style = "border-collapse: collapse; width: 100%; margin: 20px 0;"
        cell_style = "border: 1px solid #ddd; padding: 8px; text-align: left;"
        header_style = "background-color: #f2f2f2; font-weight: bold;"
        pre_style = (
            "background-color: #f4f4f4; padding: 15px; border-radius: 5px; "
            "overflow-x: auto;"
        )
        video_style = "max-width: 100%; height: auto;"
        img_style = "max-width: 100%; height: auto;"

        # Override styles if provided
        if style_options:
            if "body" in style_options:
                body_style = style_options["body"]
            if "table" in style_options:
                table_style = style_options["table"]
            if "cell" in style_options:
                cell_style = style_options["cell"]
            if "header" in style_options:
                header_style = style_options["header"]
            if "pre" in style_options:
                pre_style = style_options["pre"]
            if "video" in style_options:
                video_style = style_options["video"]
            if "img" in style_options:
                img_style = style_options["img"]

        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{get_config().get_application_name()} Document</title>
    <style>
        body {{
            {body_style}
        }}
        table {{
            {table_style}
        }}
        th, td {{
            {cell_style}
        }}
        th {{
            {header_style}
        }}
        pre {{
            {pre_style}
        }}
        video {{
            {video_style}
        }}
        img {{
            {img_style}
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        output_content = full_html
    else:
        # For other formats, just output the converted content
        output_content = html_content

    # Write output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_content)

    logger.info(
        "Processed file",
        extra={"input_file": input_file, "output_file": str(output_file)},
    )
    return True


def process_directory(
    directory,
    output_format="html",
    style_options=None,
    verbose=False,
    chunk_size=None,
    max_memory_mb=None,
    strict=False,
):
    """Process all .dmd files in a directory"""
    directory = Path(directory)
    dmd_files = list(directory.glob("*.dmd"))

    if not dmd_files:
        logger.warning("No .dmd files found", extra={"directory": str(directory)})
        return

    logger.info(
        "Processing directory",
        extra={"count": len(dmd_files), "directory": str(directory)},
    )

    success = True
    for dmd_file in dmd_files:
        if verbose:
            logger.info(
                "Processing file in directory",
                extra={"file": dmd_file.name, "directory": str(directory)},
            )
        ok = process_dmd_file(
            str(dmd_file),
            output_format=output_format,
            style_options=style_options,
            verbose=verbose,
            chunk_size=chunk_size,
            max_memory_mb=max_memory_mb,
            strict=strict,
        )
        if not ok:
            success = False
            if strict:
                break
    return success


def watch_path(
    target_path,
    output_format="html",
    style_options=None,
    verbose=False,
    chunk_size=None,
    max_memory_mb=None,
    strict=False,
):
    """Watch a file or directory for changes and reprocess .dmd files."""
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except Exception:
        logger.error(
            "--watch requires the 'watchdog' package. "
            "Install with: pip install watchdog"
        )
        sys.exit(1)

    target = Path(target_path)
    watch_dir = target if target.is_dir() else target.parent

    class Handler(FileSystemEventHandler):
        def __init__(self):
            super().__init__()
            self._last_run = {}

        def _should_run(self, path_str, debounce=0.5):
            now = time.time()
            last = self._last_run.get(path_str, 0)
            if now - last < debounce:
                return False
            self._last_run[path_str] = now
            return True

        def on_modified(self, event):
            self._handle_event(event)

        def on_created(self, event):
            self._handle_event(event)

        def _handle_event(self, event):
            if event.is_directory:
                return
            p = Path(event.src_path)
            # If specific file was given, only rebuild for that file
            if target.is_file() and p.resolve() != target.resolve():
                return
            if p.suffix == ".dmd":
                if self._should_run(str(p)):
                    logger.info(
                        "Change detected; rebuilding",
                        extra={"path": str(p)},
                    )
                    process_dmd_file(
                        str(p),
                        output_format=output_format,
                        style_options=style_options,
                        verbose=verbose,
                        chunk_size=chunk_size,
                        max_memory_mb=max_memory_mb,
                        strict=strict,
                    )

    logger.info(
        "Watching for changes",
        extra={"target": str(target.resolve()), "recursive": target.is_dir()},
    )
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, str(watch_dir), recursive=target.is_dir())
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping watcher")
        observer.stop()
    observer.join()


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Process Data Markdown (DataMD) (.dmd) files"
    )
    parser.add_argument("input", help="Input .dmd file or directory")
    parser.add_argument(
        "-o", "--output", help="Output file (for single file processing)"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch for file changes (requires watchdog)",
    )
    parser.add_argument(
        "--config",
        help="Path to configuration file",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["html"],
        default="html",
        help="Output format (currently only HTML is supported)",
    )
    parser.add_argument("--style-body", help="Custom CSS for body element")
    parser.add_argument("--style-table", help="Custom CSS for table elements")
    parser.add_argument("--style-cell", help="Custom CSS for table cell elements")
    parser.add_argument("--style-header", help="Custom CSS for table header elements")
    parser.add_argument("--style-pre", help="Custom CSS for pre elements")
    parser.add_argument("--style-video", help="Custom CSS for video elements")
    parser.add_argument("--style-img", help="Custom CSS for img elements")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        help="Set chunk size for streaming processing (default: 10000)",
    )
    parser.add_argument(
        "--max-memory",
        type=int,
        help="Set maximum memory usage in MB (default: 100)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero on any shortcode failure",
    )

    parsed_args = parser.parse_args(args)

    # Allow environment variable override for config file path
    if not parsed_args.config:
        env_config = os.getenv("DATAMD_CONFIG_FILE")
        if env_config:
            parsed_args.config = env_config

    # Load configuration if specified
    if parsed_args.config:
        get_config(parsed_args.config)

    # Update configuration with CLI options if provided
    if parsed_args.chunk_size:
        get_config().set("performance.chunk_size", parsed_args.chunk_size)
    if parsed_args.max_memory:
        get_config().set("performance.max_memory_mb", parsed_args.max_memory)

    # Prepare style options
    style_options = {}
    if parsed_args.style_body:
        style_options["body"] = parsed_args.style_body
    if parsed_args.style_table:
        style_options["table"] = parsed_args.style_table
    if parsed_args.style_cell:
        style_options["cell"] = parsed_args.style_cell
    if parsed_args.style_header:
        style_options["header"] = parsed_args.style_header
    if parsed_args.style_pre:
        style_options["pre"] = parsed_args.style_pre
    if parsed_args.style_video:
        style_options["video"] = parsed_args.style_video
    if parsed_args.style_img:
        style_options["img"] = parsed_args.style_img

    is_file = os.path.isfile(parsed_args.input)
    is_dir = os.path.isdir(parsed_args.input)

    if parsed_args.verbose:
        logger.info(
            "DataMD Processor started",
            extra={"format": parsed_args.format},
        )
        if style_options:
            logger.info(
                "Custom styles applied", extra={"styles": list(style_options.keys())}
            )

    try:
        success = True

        if is_file:
            if not parsed_args.input.endswith(".dmd"):
                logger.error("Input file must have .dmd extension")
                sys.exit(1)
            success = process_dmd_file(
                parsed_args.input,
                parsed_args.output,
                parsed_args.format,
                style_options,
                parsed_args.verbose,
                parsed_args.chunk_size,
                parsed_args.max_memory,
                parsed_args.strict,
            )
            if parsed_args.watch:
                watch_path(
                    parsed_args.input,
                    parsed_args.format,
                    style_options,
                    parsed_args.verbose,
                    parsed_args.chunk_size,
                    parsed_args.max_memory,
                    parsed_args.strict,
                )
        elif is_dir:
            success = process_directory(
                parsed_args.input,
                parsed_args.format,
                style_options,
                parsed_args.verbose,
                parsed_args.chunk_size,
                parsed_args.max_memory,
                parsed_args.strict,
            )
            if parsed_args.watch:
                watch_path(
                    parsed_args.input,
                    parsed_args.format,
                    style_options,
                    parsed_args.verbose,
                    parsed_args.chunk_size,
                    parsed_args.max_memory,
                    parsed_args.strict,
                )
        else:
            logger.error(
                "Input path is not a valid file or directory",
                extra={"input": parsed_args.input},
            )
            sys.exit(1)

        if not success:
            sys.exit(1)
    except ShortcodeError as exc:
        logger.error(
            "Shortcode error during processing",
            extra={"input": parsed_args.input, "error": str(exc)},
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
