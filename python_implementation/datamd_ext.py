import json
import re
from pathlib import Path

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
                    if cmd == "csv":
                        sep = args[0] if args else ","
                        df = pd.read_csv(file_path, sep=sep)
                        new_lines.append(df.to_markdown(index=False))

                    elif cmd == "json":
                        flatten = args[0] == "true" if args else False
                        with open(file_path, "r") as f:
                            data = json.load(f)

                        if isinstance(data, list):
                            df = pd.json_normalize(data)
                            new_lines.append(df.to_markdown(index=False))
                        elif isinstance(data, dict):
                            if flatten:
                                df = pd.json_normalize([data])
                                new_lines.append(df.to_markdown(index=False))
                            else:
                                new_lines.append("```json")
                                new_lines.append(json.dumps(data, indent=2))
                                new_lines.append("```")
                        else:
                            new_lines.append(f"JSON content: {data}")

                    elif cmd in ["xlsx", "xls", "xlsm", "ods"]:
                        sheet = args[0] if args else 0
                        engine = "openpyxl"
                        if cmd == "xls":
                            engine = "xlrd"
                        elif cmd == "ods":
                            engine = "odf"

                        if sheet.isdigit():
                            sheet = int(sheet)

                        df = pd.read_excel(file_path, sheet_name=sheet, engine=engine)
                        new_lines.append(df.to_markdown(index=False))

                    elif cmd == "pdf":
                        pages = args[0] if args else "all"
                        with pdfplumber.open(file_path) as pdf:
                            if pages == "all":
                                text = "\n\n".join(
                                    page.extract_text() or "" for page in pdf.pages
                                )
                            else:
                                page_num = int(pages) - 1
                                text = pdf.pages[page_num].extract_text() or ""
                        new_lines.append(text.strip())

                    elif cmd == "pdf_table":
                        # Parse arguments for pdf_table
                        page = int(args[0]) - 1 if args and args[0].isdigit() else 0
                        horizontal_strategy = args[1] if len(args) > 1 else "lines"
                        vertical_strategy = args[2] if len(args) > 2 else "lines"

                        # Validate strategy parameters
                        valid_strategies = ["lines", "text", "explicit"]
                        if horizontal_strategy not in valid_strategies:
                            horizontal_strategy = "lines"
                        if vertical_strategy not in valid_strategies:
                            vertical_strategy = "lines"

                        with pdfplumber.open(file_path) as pdf:
                            # Use strategy parameters for table extraction
                            tables = pdf.pages[page].extract_tables(
                                {
                                    "horizontal_strategy": horizontal_strategy,
                                    "vertical_strategy": vertical_strategy,
                                }
                            )
                            if tables:
                                for i, table in enumerate(tables):
                                    if table and len(table) > 1:
                                        df = pd.DataFrame(table[1:], columns=table[0])
                                        new_lines.append(f"### Table {i+1}")
                                        new_lines.append(df.to_markdown(index=False))
                                        new_lines.append("")
                            else:
                                new_lines.append("No tables found on this page.")

                    elif cmd == "image_ocr":
                        lang = args[0] if args else "eng"
                        image = Image.open(file_path)
                        text = pytesseract.image_to_string(image, lang=lang)
                        new_lines.append(text.strip())

                    elif cmd == "video":
                        width = args[0] if len(args) > 0 else "640"
                        height = args[1] if len(args) > 1 else "480"
                        controls = args[2] if len(args) > 2 else "true"
                        autoplay = args[3] if len(args) > 3 else "false"

                        controls_attr = " controls" if controls == "true" else ""
                        autoplay_attr = " autoplay" if autoplay == "true" else ""

                        video_html = (
                            f'<video width="{width}" height="{height}"'
                            f"{controls_attr}{autoplay_attr}>\n"
                            f'  <source src="{file_path}" type="video/mp4">\n'
                            "  Your browser does not support the video tag.\n"
                            "</video>"
                        )
                        new_lines.append(video_html)

                    elif cmd == "video_thumb":
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
                            time = (
                                float(args[0])
                                if args[0].replace(".", "", 1).isdigit()
                                else 0
                            )
                            width = (
                                int(args[1])
                                if len(args) > 1 and args[1].isdigit()
                                else None
                            )
                            height = (
                                int(args[2])
                                if len(args) > 2 and args[2].isdigit()
                                else None
                            )

                            # Generate thumbnail using moviepy
                            clip = VideoFileClip(file_path)

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
                            file_path_obj = Path(file_path)
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
