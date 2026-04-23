#!/usr/bin/env python3
"""Fetch a podcast page and output a lightweight inspection report.

This script is intentionally conservative:
- uses requests + Python stdlib only
- helps the agent decide whether a link contains transcript/show notes only
- does not claim semantic understanding of the full episode

Usage:
  python scripts/fetch_podcast_page.py --url https://example.com/episode --output report.json
"""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from typing import Any

import requests


class MetaHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.in_script = False
        self.in_style = False
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.meta: dict[str, str] = {}
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k.lower(): (v or "") for k, v in attrs}
        tag = tag.lower()
        if tag == "title":
            self.in_title = True
        elif tag == "script":
            self.in_script = True
        elif tag == "style":
            self.in_style = True
        elif tag == "meta":
            name = attr.get("name") or attr.get("property") or attr.get("itemprop")
            content = attr.get("content", "")
            if name and content:
                self.meta[name.lower()] = content.strip()
        elif tag == "a":
            href = attr.get("href", "").strip()
            text_hint = attr.get("title", "").strip()
            if href:
                self.links.append({"href": href, "hint": text_hint})

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "script":
            self.in_script = False
        elif tag == "style":
            self.in_style = False

    def handle_data(self, data: str) -> None:
        if self.in_script or self.in_style:
            return
        text = data.strip()
        if not text:
            return
        if self.in_title:
            self.title_parts.append(text)
        self.text_parts.append(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--max-text-chars", type=int, default=5000)
    return parser.parse_args()


def find_timestamp_examples(text: str) -> list[str]:
    pattern = re.compile(r"\b(?:\d{1,2}:)?\d{1,2}:\d{2}\b")
    seen: list[str] = []
    for match in pattern.findall(text):
        if match not in seen:
            seen.append(match)
        if len(seen) >= 12:
            break
    return seen


def classify_page(text: str, meta: dict[str, str], links: list[dict[str, str]]) -> dict[str, Any]:
    lower = text.lower()
    transcript_hits = len(re.findall(r"\btranscript\b|全文|逐字稿|字幕", lower, flags=re.I))
    show_notes_hits = len(re.findall(r"show notes|shownotes|节目简介|本期介绍|章节", lower, flags=re.I))
    timestamp_examples = find_timestamp_examples(text)

    link_hints = []
    for item in links[:300]:
        blob = f"{item.get('href','')} {item.get('hint','')}".lower()
        if any(key in blob for key in ["transcript", "caption", "subtitle", "shownotes", "episode"]):
            link_hints.append(item)
    link_hints = link_hints[:20]

    if transcript_hits >= 2 or (len(timestamp_examples) >= 6 and len(text) > 4000):
        level = "transcript_like"
    elif show_notes_hits >= 1 or len(timestamp_examples) >= 2:
        level = "show_notes_like"
    else:
        level = "summary_like"

    return {
        "content_level": level,
        "transcript_hits": transcript_hits,
        "show_notes_hits": show_notes_hits,
        "timestamp_examples": timestamp_examples,
        "candidate_links": link_hints,
        "has_many_timestamps": len(timestamp_examples) >= 6,
    }


def main() -> int:
    args = parse_args()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari"
    }
    resp = requests.get(args.url, headers=headers, timeout=args.timeout)
    resp.raise_for_status()

    parser = MetaHTMLParser()
    parser.feed(resp.text)

    title = " ".join(parser.title_parts).strip()
    raw_text = re.sub(r"\s+", " ", " ".join(parser.text_parts)).strip()
    excerpt = raw_text[: args.max_text_chars]

    report = {
        "url": args.url,
        "final_url": resp.url,
        "status_code": resp.status_code,
        "title": title,
        "meta": {
            "description": parser.meta.get("description") or parser.meta.get("og:description") or "",
            "og_title": parser.meta.get("og:title") or "",
            "published_time": parser.meta.get("article:published_time") or parser.meta.get("datepublished") or "",
            "author": parser.meta.get("author") or "",
        },
        "inspection": classify_page(raw_text, parser.meta, parser.links),
        "text_excerpt": excerpt,
    }

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(payload)
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
