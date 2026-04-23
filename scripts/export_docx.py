#!/usr/bin/env python3
"""Convert a simple Markdown analysis draft into a .docx on macOS via textutil.

Design goal:
- no third-party Python deps
- works for the podcast_analysis_doc skill's default Markdown structure
- keeps headings, paragraphs, and bullet lists readable in Word

Usage:
  python scripts/export_docx.py input.md -o output.docx
"""

from __future__ import annotations

import argparse
import html
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_md", help="Path to the Markdown source")
    parser.add_argument("-o", "--output", help="Path to output .docx")
    parser.add_argument("--title", default="", help="Optional document title metadata")
    return parser.parse_args()


def ensure_textutil() -> str:
    path = shutil.which("textutil")
    if not path:
        raise SystemExit("textutil not found. This export path currently supports macOS only.")
    return path


def html_page(title: str, body: str) -> str:
    safe_title = html.escape(title or "Podcast Analysis")
    return f"""<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\" />
  <title>{safe_title}</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
      line-height: 1.65;
      color: #111;
      font-size: 12pt;
      margin: 36px;
    }}
    h1 {{ font-size: 24pt; margin: 0 0 16px 0; }}
    h2 {{ font-size: 16pt; margin: 24px 0 10px 0; }}
    h3 {{ font-size: 13pt; margin: 18px 0 8px 0; }}
    p {{ margin: 0 0 10px 0; }}
    ul {{ margin: 6px 0 12px 20px; padding: 0; }}
    li {{ margin: 6px 0; }}
    .chapter-label {{ font-weight: 700; }}
    .muted {{ color: #555; }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def convert_inline(text: str) -> str:
    out = html.escape(text)
    # extremely small inline markdown support
    replacements = [
        ("**", "strong"),
        ("__", "strong"),
        ("`", "code"),
    ]
    for marker, tag in replacements:
        parts = out.split(marker)
        if len(parts) > 1:
            rebuilt = []
            for idx, part in enumerate(parts):
                if idx % 2 == 1:
                    rebuilt.append(f"<{tag}>{part}</{tag}>")
                else:
                    rebuilt.append(part)
            out = "".join(rebuilt)
    return out


def markdown_to_html(md_text: str) -> tuple[str, str]:
    lines = md_text.splitlines()
    blocks: list[str] = []
    title = ""
    i = 0
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            blocks.append("</ul>")
            in_list = False

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            close_list()
            i += 1
            continue

        if stripped.startswith("# "):
            close_list()
            title = stripped[2:].strip()
            blocks.append(f"<h1>{convert_inline(title)}</h1>")
            i += 1
            continue

        if stripped.startswith("## "):
            close_list()
            blocks.append(f"<h2>{convert_inline(stripped[3:].strip())}</h2>")
            i += 1
            continue

        if stripped.startswith("### "):
            close_list()
            blocks.append(f"<h3>{convert_inline(stripped[4:].strip())}</h3>")
            i += 1
            continue

        if stripped.startswith(("- ", "* ")):
            if not in_list:
                blocks.append("<ul>")
                in_list = True
            item = stripped[2:].strip()
            continuation: list[str] = []
            j = i + 1
            while j < len(lines):
                nxt = lines[j].rstrip("\n")
                if not nxt.strip():
                    break
                if nxt.strip().startswith(("- ", "* ", "# ", "## ", "### ")):
                    break
                if nxt.startswith("  ") or nxt.startswith("\t"):
                    continuation.append(nxt.strip())
                    j += 1
                    continue
                break
            item_html = convert_inline(item)
            if continuation:
                extra = "<br/>".join(convert_inline(x) for x in continuation)
                item_html = f"<span class=\"chapter-label\">{item_html}</span><br/><span>{extra}</span>"
            blocks.append(f"<li>{item_html}</li>")
            i = j if continuation else i + 1
            continue

        close_list()
        para_lines = [stripped]
        j = i + 1
        while j < len(lines):
            nxt = lines[j].strip()
            if not nxt:
                break
            if nxt.startswith(("# ", "## ", "### ", "- ", "* ")):
                break
            para_lines.append(nxt)
            j += 1
        paragraph = " ".join(para_lines)
        blocks.append(f"<p>{convert_inline(paragraph)}</p>")
        i = j

    close_list()
    return title or Path("document").stem, "\n".join(blocks)


def main() -> int:
    args = parse_args()
    textutil = ensure_textutil()

    input_path = Path(args.input_md).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    output_path = Path(args.output).expanduser().resolve() if args.output else input_path.with_suffix(".docx")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    md_text = input_path.read_text(encoding="utf-8")
    detected_title, body = markdown_to_html(md_text)
    title = args.title or detected_title
    page = html_page(title, body)

    with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8", delete=False) as tmp:
        tmp.write(page)
        tmp_html = tmp.name

    try:
        cmd = [textutil, "-convert", "docx", tmp_html, "-output", str(output_path), "-title", title]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            sys.stderr.write(result.stderr or result.stdout)
            return result.returncode
        print(str(output_path))
        return 0
    finally:
        try:
            os.remove(tmp_html)
        except OSError:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
