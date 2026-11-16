---
name: mistral-ocr
description: Convert PDF/images to Markdown/JSON/HTML using Mistral OCR API. Supports image extraction, table recognition, header/footer handling, multi-column layouts, and a custom API base URL.
registry:
  homepage: https://github.com/buddhism5080/Mistral-OCR-SKILL
  author: YZDame
  credentials:
    required: true
    env_vars:
      - MISTRAL_API_KEY
---

# ⚠️ Privacy Warning - 隐私警告

**IMPORTANT - READ BEFORE INSTALLING:**

This tool **sends your files to the configured API host** in the `/v1/ocr` request. It does not upload them through `/v1/files`. The default host is Mistral (`https://api.mistral.ai`). A custom `base_url` sends files to that host instead.

**Do NOT use with sensitive or confidential documents** unless:
- You trust Mistral's data handling policies
- You have reviewed Mistral's privacy policy
- You accept that file contents will be transmitted and processed remotely

**For sensitive documents, use offline/local OCR tools instead.**

---

# Mistral OCR (OpenClaw Skill)

A powerful OCR tool that converts PDF files and images into Markdown, JSON, or HTML formats using Mistral's OCR API, or any compatible endpoint you configure.

Fork of [YZDame/Mistral-OCR-SKILL](https://github.com/YZDame/Mistral-OCR-SKILL) with a configurable API base URL.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)

## Features

- PDF to Markdown/JSON/HTML conversion
- Image extraction with automatic path replacement
- Table recognition
- Header/footer handling
- Multi-column layout support
- Batch processing via CLI

## Installation (for OpenClaw)

OpenClaw will automatically read this README and install dependencies.

**Manual Installation:**

```bash
# Clone or download this repository
git clone https://github.com/buddhism5080/Mistral-OCR-SKILL.git
cd Mistral-OCR-SKILL

# Install dependencies
pip install -r requirements.txt
```

## 🔑 API Key Setup (Required)

You need a Mistral API key to use this tool.

**Get your API key:**
👉 [https://console.mistral.ai/home](https://console.mistral.ai/home)

**Save it once** in `scripts/config.json`, next to `scripts/mistral_ocr.py`. This file is local and is not part of the repository.

```bash
cp scripts/config.example.json scripts/config.json
```

```json
{
  "api_key": "your_api_key_here",
  "base_url": "https://your-api-host.example"
}
```

`base_url` is optional. Leave it empty or omit it to use `https://api.mistral.ai`.

## API Base URL (Optional)

By default requests go to `https://api.mistral.ai`. Set `base_url` in `scripts/config.json`, or pass `--base-url` for one command. `MISTRAL_BASE_URL` overrides the file, and `--base-url` overrides both.

Use the server root. The client appends `/v1/...` itself, so do not include `/v1`.

```bash
# EU region
export MISTRAL_BASE_URL=https://api.eu.mistral.ai

# Or pass it for one command
python3 mistral_ocr.py -i input.pdf --base-url https://your-proxy.example
```

Official roots: `https://api.mistral.ai`, `https://api.eu.mistral.ai`, `https://api.us.mistral.ai`.

## CLI Usage

```bash
cd scripts

# Process PDF to Markdown
python3 mistral_ocr.py -i input.pdf

# Process PDF to JSON
python3 mistral_ocr.py -i input.pdf -f json

# Process PDF to HTML
python3 mistral_ocr.py -i input.pdf -f html

# Specify output directory
python3 mistral_ocr.py -i input.pdf -o ~/my_ocr_results

# Custom API base URL
python3 mistral_ocr.py -i input.pdf --base-url https://api.us.mistral.ai

# Process images
python3 mistral_ocr.py -i image.png -f markdown
```

## Arguments

| Flag | Description |
|------|-------------|
| `-i, --input` | Input file path (required) |
| `-f, --format` | Output format: markdown/json/html (default: markdown) |
| `-o, --output` | Output directory (default: ./ocr_result) |
| `-b, --base-url` | API server root. Overrides `scripts/config.json` and `MISTRAL_BASE_URL`. Default: `https://api.mistral.ai` |

## Output

After processing, you'll get:

- `result.md` / `result.json` / `result.html` - Main output file
- `images/` - Extracted images (for Markdown/HTML formats)

## Data Privacy

**What happens to your files:**
1. File bytes are sent in the `/v1/ocr` request to the configured API base URL (Mistral by default)
2. Files are processed on that server
3. Processing results are returned to you
4. Whether that host keeps the file depends on the host. Mistral's own policy says files are not stored on Mistral servers

**For more details, see:** https://mistral.ai/privacy-policy

## Troubleshooting

**"MISTRAL_API_KEY is not set" error:**

Copy `scripts/config.example.json` to `scripts/config.json` and set `api_key`. `MISTRAL_API_KEY` overrides that file when it is set.

**Requests hit the wrong host, or `/v1/v1/ocr`:**

Set the server root only, for example `https://api.mistral.ai`, not `https://api.mistral.ai/v1`.

## License

MIT License - feel free to use in your projects!

## Contributing

Pull requests are welcome. For major changes, please open an issue first.
