-- DataMD Lua Filter for Quarto
-- Processes custom shortcodes for data format embedding

function Shortcode(s)
  -- CSV processing
  if s.name == "csv" then
    local file = s.arguments[1]
    local sep = s.arguments[2] or ","
    return pandoc.RawBlock("markdown",
      "```{python}\n" ..
      "#| echo: false\n" ..
      "#| output: asis\n" ..
      "import pandas as pd\n" ..
      "try:\n" ..
      "    df = pd.read_csv('" .. file .. "', sep='" .. sep .. "')\n" ..
      "    print(df.to_markdown(index=False))\n" ..
      "except Exception as e:\n" ..
      "    print(f'Error reading CSV: {e}')\n" ..
      "```")

  -- JSON processing
  elseif s.name == "json" then
    local file = s.arguments[1]
    local flatten = s.arguments[2] or "false"
    return pandoc.RawBlock("markdown",
      "```{python}\n" ..
      "#| echo: false\n" ..
      "#| output: asis\n" ..
      "import pandas as pd\n" ..
      "import json\n" ..
      "try:\n" ..
      "    with open('" .. file .. "', 'r') as f:\n" ..
      "        data = json.load(f)\n" ..
      "    if isinstance(data, list):\n" ..
      "        df = pd.json_normalize(data)\n" ..
      "        print(df.to_markdown(index=False))\n" ..
      "    elif isinstance(data, dict):\n" ..
      "        if " .. flatten .. ":\n" ..
      "            df = pd.json_normalize([data])\n" ..
      "            print(df.to_markdown(index=False))\n" ..
      "        else:\n" ..
      "            print('```json')\n" ..
      "            print(json.dumps(data, indent=2))\n" ..
      "            print('```')\n" ..
      "    else:\n" ..
      "        print(f'JSON content: {data}')\n" ..
      "except Exception as e:\n" ..
      "    print(f'Error reading JSON: {e}')\n" ..
      "```")

  -- Excel/XLSX processing
  elseif s.name == "xlsx" or s.name == "xls" or s.name == "xlsm" or s.name == "ods" then
    local file = s.arguments[1]
    local sheet = s.arguments[2] or "0"
    local engine = "openpyxl"
    if s.name == "xls" then
      engine = "xlrd"
    elseif s.name == "ods" then
      engine = "odf"
    end

    return pandoc.RawBlock("markdown",
      "```{python}\n" ..
      "#| echo: false\n" ..
      "#| output: asis\n" ..
      "import pandas as pd\n" ..
      "try:\n" ..
      "    if '" .. sheet .. "'.isdigit():\n" ..
      "        df = pd.read_excel('" .. file .. "', sheet_name=" .. sheet .. ", engine='" .. engine .. "')\n" ..
      "    else:\n" ..
      "        df = pd.read_excel('" .. file .. "', sheet_name='" .. sheet .. "', engine='" .. engine .. "')\n" ..
      "    print(df.to_markdown(index=False))\n" ..
      "except Exception as e:\n" ..
      "    print(f'Error reading Excel file: {e}')\n" ..
      "```")

  -- PDF processing
  elseif s.name == "pdf" then
    local file = s.arguments[1]
    local pages = s.arguments[2] or "all"
    return pandoc.RawBlock("markdown",
      "```{python}\n" ..
      "#| echo: false\n" ..
      "#| output: asis\n" ..
      "import pdfplumber\n" ..
      "try:\n" ..
      "    with pdfplumber.open('" .. file .. "') as pdf:\n" ..
      "        if '" .. pages .. "' == 'all':\n" ..
      "            text = '\\n\\n'.join(page.extract_text() or '' for page in pdf.pages)\n" ..
      "        else:\n" ..
      "            page_num = int('" .. pages .. "') - 1\n" ..
      "            text = pdf.pages[page_num].extract_text() or ''\n" ..
      "        print(text)\n" ..
      "except Exception as e:\n" ..
      "    print(f'Error reading PDF: {e}')\n" ..
      "```")

  -- PDF tables extraction
  elseif s.name == "pdf_table" then
    local file = s.arguments[1]
    local page = s.arguments[2] or "1"
    return pandoc.RawBlock("markdown",
      "```{python}\n" ..
      "#| echo: false\n" ..
      "#| output: asis\n" ..
      "import pdfplumber\n" ..
      "import pandas as pd\n" ..
      "try:\n" ..
      "    with pdfplumber.open('" .. file .. "') as pdf:\n" ..
      "        page_num = int('" .. page .. "') - 1\n" ..
      "        tables = pdf.pages[page_num].extract_tables()\n" ..
      "        if tables:\n" ..
      "            for i, table in enumerate(tables):\n" ..
      "                df = pd.DataFrame(table[1:], columns=table[0])\n" ..
      "                print(f'### Table {i+1}')\n" ..
      "                print(df.to_markdown(index=False))\n" ..
      "                print()\n" ..
      "        else:\n" ..
      "            print('No tables found on this page.')\n" ..
      "except Exception as e:\n" ..
      "    print(f'Error extracting PDF tables: {e}')\n" ..
      "```")

  -- Image OCR processing
  elseif s.name == "image_ocr" then
    local file = s.arguments[1]
    local lang = s.arguments[2] or "eng"
    return pandoc.RawBlock("markdown",
      "```{python}\n" ..
      "#| echo: false\n" ..
      "#| output: asis\n" ..
      "from PIL import Image\n" ..
      "import pytesseract\n" ..
      "try:\n" ..
      "    image = Image.open('" .. file .. "')\n" ..
      "    text = pytesseract.image_to_string(image, lang='" .. lang .. "')\n" ..
      "    print(text.strip())\n" ..
      "except Exception as e:\n" ..
      "    print(f'Error processing image OCR: {e}')\n" ..
      "```")

  -- Video embedding
  elseif s.name == "video" then
    local file = s.arguments[1]
    local width = s.arguments[2] or "640"
    local height = s.arguments[3] or "480"
    local controls = s.arguments[4] or "true"
    local autoplay = s.arguments[5] or "false"

    local controls_attr = ""
    local autoplay_attr = ""

    if controls == "true" then
      controls_attr = " controls"
    end

    if autoplay == "true" then
      autoplay_attr = " autoplay"
    end

    return pandoc.RawBlock("html",
      "<video width=\"" .. width .. "\" height=\"" .. height .. "\"" .. controls_attr .. autoplay_attr .. ">\n" ..
      "  <source src=\"" .. file .. "\" type=\"video/mp4\">\n" ..
      "  Your browser does not support the video tag.\n" ..
      "</video>")

  -- Video thumbnail extraction
  elseif s.name == "video_thumb" then
    local file = s.arguments[1]
    local time = s.arguments[2] or "5"
    return pandoc.RawBlock("markdown",
      "```{python}\n" ..
      "#| echo: false\n" ..
      "#| output: asis\n" ..
      "import moviepy.editor as mp\n" ..
      "import os\n" ..
      "try:\n" ..
      "    video = mp.VideoFileClip('" .. file .. "')\n" ..
      "    frame = video.get_frame(" .. time .. ")\n" ..
      "    thumb_path = '" .. file .. "_thumb.jpg'\n" ..
      "    mp.ImageClip(frame).save_frame(thumb_path)\n" ..
      "    print(f'![Video Thumbnail]({thumb_path})')\n" ..
      "    video.close()\n" ..
      "except Exception as e:\n" ..
      "    print(f'Error extracting video thumbnail: {e}')\n" ..
      "```")

  end

  return nil
end
