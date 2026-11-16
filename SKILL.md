---
name: mistral-ocr
description: "Convert PDF/images to Markdown/JSON/HTML using Mistral OCR API. Supports image extraction, table recognition, header/footer handling, multi-column layouts, and a custom API base URL via MISTRAL_BASE_URL or --base-url. Usage: Upload a file and say Use Mistral OCR to process this."
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

This skill **uploads your files to the configured API host** for OCR processing. The default host is Mistral (`https://api.mistral.ai`). A custom `MISTRAL_BASE_URL` sends files to that host instead.

**Do NOT use with sensitive or confidential documents** unless:
- You trust Mistral's data handling policies
- You have reviewed Mistral's privacy policy
- You accept that file contents will be transmitted and processed remotely

**For sensitive documents, use offline/local OCR tools instead.**

---

# Mistral OCR Skill

A powerful OCR tool that converts PDF files and images into Markdown, JSON, or HTML formats using Mistral's OCR API, or any compatible endpoint you configure.

Fork of [YZDame/Mistral-OCR-SKILL](https://github.com/YZDame/Mistral-OCR-SKILL) with a configurable API base URL.

## Installation

```bash
# Clone or download this repository
git clone https://github.com/buddhism5080/Mistral-OCR-SKILL.git
cd Mistral-OCR-SKILL

# Install dependencies
pip install -r requirements.txt
```

## 🔑 API Key Setup (Required)

**Get your API key:**
👉 https://console.mistral.ai/home

**Save the key and base URL once** in `~/.pi/agent/settings.json`, inside the existing `env` object. Every new Pi session reads it. You do not export it again.

```json
"env": {
  "MISTRAL_API_KEY": "your_api_key",
  "MISTRAL_BASE_URL": "https://your-api-host.example"
}
```

`MISTRAL_BASE_URL` is optional. Leave it out to use `https://api.mistral.ai`. Use the server root, not a `/v1` path. The client appends `/v1` itself.

A process environment variable with the same name overrides the file. `--base-url` overrides both for that one command.

## CLI Usage

```bash
cd scripts

# Process PDF to Markdown
python3 mistral_ocr.py -i input.pdf

# Process PDF to JSON
python3 mistral_ocr.py -i input.pdf -f json

# Specify output directory
python3 mistral_ocr.py -i input.pdf -o ~/my_ocr_results

# Custom API base URL
python3 mistral_ocr.py -i input.pdf --base-url https://your-proxy.example
```

## Arguments

| Flag | Description |
|------|-------------|
| `-i, --input` | Input file path (required) |
| `-f, --format` | Output format: markdown/json/html (default: markdown) |
| `-o, --output` | Output directory |
| `-b, --base-url` | API server root. Overrides `MISTRAL_BASE_URL`. Default: `https://api.mistral.ai` |

## Data Privacy

**What happens to your files:**
1. Files are uploaded to the configured API base URL (Mistral by default)
2. Files are processed on that server
3. Processing results are returned to you
4. Whether that host keeps the file depends on the host. Mistral's own policy says files are not stored on Mistral servers

**For more details, see:** https://mistral.ai/privacy-policy

## License

MIT
