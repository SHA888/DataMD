#!/usr/bin/env python3
"""
Data Markdown (DataMD) Processor Script
Processes .dmd files using the Python-Markdown extension
"""

import argparse
import os
import sys
import time
from pathlib import Path

import markdown

try:
    # When installed as a package (CLI path)
    from .datamd_ext import DataMDExtension
except ImportError:  # pragma: no cover
    # When running the script directly (python python_implementation/process_dmd.py)
    from datamd_ext import DataMDExtension


def process_dmd_file(input_file, output_file=None):
    """Process a single .dmd file and convert to HTML"""

    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found")
        return False

    # Read the .dmd file
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Process with DataMD extension
    md = markdown.Markdown(extensions=[DataMDExtension()])
    html_content = md.convert(content)

    # Generate output filename if not provided
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.with_suffix(".html")

    # Create basic HTML document
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Markdown (DataMD) Document</title>
    <style>
        body {{
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                'Segoe UI',
                Roboto,
                sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        video {{
            max-width: 100%;
            height: auto;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""

    # Write output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Processed {input_file} -> {output_file}")
    return True


def process_directory(directory):
    """Process all .dmd files in a directory"""
    directory = Path(directory)
    dmd_files = list(directory.glob("*.dmd"))

    if not dmd_files:
        print(f"No .dmd files found in {directory}")
        return

    for dmd_file in dmd_files:
        process_dmd_file(str(dmd_file))


def watch_path(target_path):
    """Watch a file or directory for changes and reprocess .dmd files."""
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except Exception:
        print(
            (
                "Error: --watch requires the 'watchdog' package. Install with: "
                "pip install watchdog"
            )
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
                    print(f"Change detected: {p}. Rebuilding...")
                    process_dmd_file(str(p))

    print(f"Watching: {target.resolve()} (press Ctrl+C to stop)")
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, str(watch_dir), recursive=target.is_dir())
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping watcher...")
        observer.stop()
    observer.join()


def main():
    parser = argparse.ArgumentParser(
        description="Process Data Markdown (DataMD) (.dmd) files"
    )
    parser.add_argument("input", help="Input .dmd file or directory")
    parser.add_argument(
        "-o", "--output", help="Output HTML file (for single file processing)"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch for file changes (requires watchdog)",
    )

    args = parser.parse_args()

    is_file = os.path.isfile(args.input)
    is_dir = os.path.isdir(args.input)

    if is_file:
        if not args.input.endswith(".dmd"):
            print("Error: Input file must have .dmd extension")
            sys.exit(1)
        process_dmd_file(args.input, args.output)
        if args.watch:
            watch_path(args.input)
    elif is_dir:
        process_directory(args.input)
        if args.watch:
            watch_path(args.input)
    else:
        print(f"Error: {args.input} is not a valid file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
