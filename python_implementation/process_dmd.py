#!/usr/bin/env python3
"""
DataMD Processor Script
Processes .dmd files using the Python-Markdown extension
"""

import argparse
import os
import sys
from pathlib import Path

import markdown
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
    <title>DataMD Document</title>
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


def main():
    parser = argparse.ArgumentParser(description="Process DataMD (.dmd) files")
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

    if os.path.isfile(args.input):
        if not args.input.endswith(".dmd"):
            print("Error: Input file must have .dmd extension")
            sys.exit(1)
        process_dmd_file(args.input, args.output)
    elif os.path.isdir(args.input):
        process_directory(args.input)
    else:
        print(f"Error: {args.input} is not a valid file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
