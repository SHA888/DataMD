"""
Data Markdown (DataMD) Python-Markdown Extension
Alternative implementation for environments without Quarto
"""

import json
import re

import pandas as pd
import pdfplumber
import pytesseract
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from PIL import Image


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
                        page = int(args[0]) - 1 if args else 0
                        with pdfplumber.open(file_path) as pdf:
                            tables = pdf.pages[page].extract_tables()
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

                    else:
                        new_lines.append(f"Unknown Data Markdown (DataMD) command: {cmd}")

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
