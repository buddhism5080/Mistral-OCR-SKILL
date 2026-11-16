#!/usr/bin/env python3
"""
Mistral OCR Tool - Convert PDF/images to Markdown/JSON/HTML

Usage:
    1. Set API key: export MISTRAL_API_KEY=your_api_key
    2. Optional: export MISTRAL_BASE_URL=https://your-api-host.example
    3. Run: python3 mistral_ocr.py -i input.pdf -f markdown

Get API key: https://console.mistral.ai/home
Default API base URL: https://api.mistral.ai
"""

from mistralai import Mistral
from pathlib import Path
import base64
import os
import argparse
import json


DEFAULT_API_BASE_URL = "https://api.mistral.ai"


def resolve_base_url(cli_base_url=None):
    """Return a custom API server root, or None for the SDK default.

    Precedence is --base-url, then MISTRAL_BASE_URL. The value is the server
    root, such as https://api.mistral.ai. The client appends /v1 itself.
    """
    if cli_base_url is not None:
        raw = cli_base_url
    else:
        raw = os.environ.get("MISTRAL_BASE_URL", "")

    base_url = raw.strip().strip("'\"").rstrip("/")
    if not base_url:
        return None
    if not (base_url.startswith("https://") or base_url.startswith("http://")):
        print(f"""
[!] Error: invalid API base URL: {base_url}

Use an absolute URL, for example:
  export MISTRAL_BASE_URL=https://api.mistral.ai
  python3 mistral_ocr.py -i input.pdf --base-url https://api.eu.mistral.ai
        """)
        raise SystemExit(1)
    if base_url.endswith("/v1"):
        print(f"""
[!] Error: base URL must be the server root, not a /v1 path: {base_url}

Use {base_url[:-3]} instead. Requests go to <base-url>/v1/ocr.
        """)
        raise SystemExit(1)
    return base_url


def get_api_key():
    """Get API Key from environment variable."""
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("""
[!] Error: MISTRAL_API_KEY environment variable is not set.

To use this tool, you need a Mistral API key:

1. Visit: https://console.mistral.ai/home
2. Sign up/Login and create an API key
3. Set the environment variable:
   
   export MISTRAL_API_KEY=your_api_key

For permanent setup, add the line above to your ~/.zshrc or ~/.bashrc
        """)
        raise SystemExit(1)
    return api_key


def replace_html_entities(text):
    """Replace HTML entities with regular characters (for Typora compatibility)."""
    replacements = {
        "&gt;": ">",
        "&lt;": "<",
        "&amp;": "&",
        "&quot;": '"',
        "&#39;": "'",
        "&nbsp;": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def save_images_from_page(page, images_dir, page_num):
    """Save images from page and return modified markdown."""
    page_images = {}
    
    for img in page.images:
        try:
            # Parse base64 data
            if "," in img.image_base64:
                img_data = base64.b64decode(img.image_base64.split(',')[1])
            else:
                img_data = base64.b64decode(img.image_base64)
            
            img_path = images_dir / f"page{page_num}_{img.id}.png"
            with open(img_path, 'wb') as f:
                f.write(img_data)
            page_images[img.id] = str(img_path)
        except Exception as e:
            print(f"[!] Failed to save image: {e}")
    
    # Replace image paths in markdown
    page_md = page.markdown
    for img_id, img_path in page_images.items():
        page_md = page_md.replace(f"![{img_id}]({img_id})", f"![{img_id}]({img_path})")
        page_md = page_md.replace(f"]({img_id})", f"]({img_path})")
    
    return page_md


def process_pdf(input_path, output_format="markdown", output_dir=None, base_url=None):
    """Process PDF file."""
    input_path = Path(input_path)
    
    if output_dir is None:
        output_dir = Path.cwd() / "ocr_result"
    else:
        output_dir = Path(output_dir)
    
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    resolved_base_url = resolve_base_url(base_url)
    client_kwargs = {"api_key": get_api_key()}
    if resolved_base_url:
        client_kwargs["server_url"] = resolved_base_url
        print(f"[*] API base URL: {resolved_base_url}")
    else:
        print(f"[*] API base URL: {DEFAULT_API_BASE_URL} (default)")
    try:
        client = Mistral(**client_kwargs)
    except TypeError as exc:
        if resolved_base_url and "server_url" in str(exc):
            print(
                "[!] This mistralai package does not support a custom base URL. "
                "Upgrade with: pip install -U 'mistralai>=1.0.0'"
            )
            raise SystemExit(1)
        raise
    
    print(f"[*] Processing: {input_path.name}")
    
    # Upload file
    uploaded_file = client.files.upload(
        file={
            "file_name": input_path.stem,
            "content": input_path.read_bytes(),
        },
        purpose="ocr",
    )
    
    # Get signed URL
    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
    
    # OCR processing
    result = client.ocr.process(
        document={"document_url": signed_url.url},
        model="mistral-ocr-latest",
        include_image_base64=True
    )
    
    print(f"[*] Total pages: {len(result.pages)}")
    
    if output_format == "markdown":
        all_markdown = []
        for i, page in enumerate(result.pages):
            page_md = save_images_from_page(page, images_dir, i + 1)
            page_md = replace_html_entities(page_md)
            all_markdown.append(page_md)
        
        output_path = output_dir / "result.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(all_markdown))
        print(f"[+] Markdown saved: {output_path}")
        
    elif output_format == "json":
        output_data = []
        for i, page in enumerate(result.pages):
            page_md = save_images_from_page(page, images_dir, i + 1)
            page_md = replace_html_entities(page_md)
            output_data.append({
                "page": i + 1,
                "markdown": page_md,
                "images": [img.id for img in page.images]
            })
        
        output_path = output_dir / "result.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"[+] JSON saved: {output_path}")
        
    elif output_format == "html":
        all_html = []
        for i, page in enumerate(result.pages):
            page_md = save_images_from_page(page, images_dir, i + 1)
            page_md = replace_html_entities(page_md)
            all_html.append(f"<div class='page'><h2>Page {i+1}</h2>{page_md}</div>")
        
        html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{input_path.stem}</title></head>
<body>{"".join(all_html)}</body>
</html>"""
        
        output_path = output_dir / "result.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[+] HTML saved: {output_path}")
    
    print(f"[*] Images saved: {images_dir}")
    return output_dir


def main():
    parser = argparse.ArgumentParser(
        description="Mistral OCR - Convert PDF/images to Markdown/JSON/HTML"
    )
    parser.add_argument("-i", "--input", required=True, help="Input file path")
    parser.add_argument("-f", "--format", choices=["markdown", "json", "html"], 
                       default="markdown", help="Output format")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument(
        "-b", "--base-url",
        help=(
            "API server root. Overrides MISTRAL_BASE_URL. "
            f"Default: {DEFAULT_API_BASE_URL}. Do not include /v1."
        ),
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"[!] File not found: {args.input}")
        return
    
    process_pdf(args.input, args.format, args.output, args.base_url)


if __name__ == "__main__":
    main()
