#!/usr/bin/env python3
"""Smoke test for podcast_analysis_doc.

Checks whether the local environment can support the minimum workflow:
1. fetch a page report
2. export markdown to docx (macOS textutil path)
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
EXAMPLE_MD = SKILL_DIR / 'examples' / 'chunqiu_airlines_example.md'
TMP_DOCX = Path('/tmp/podcast_analysis_smoke_test.docx')
FETCH_SCRIPT = SKILL_DIR / 'scripts' / 'fetch_podcast_page.py'
EXPORT_SCRIPT = SKILL_DIR / 'scripts' / 'export_docx.py'


def run(cmd: list[str]) -> tuple[bool, str]:
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except Exception as e:
        return False, str(e)
    ok = res.returncode == 0
    output = (res.stdout or '') + (res.stderr or '')
    return ok, output.strip()


def main() -> int:
    print('== podcast_analysis_doc smoke test ==')
    print(f'skill_dir: {SKILL_DIR}')
    print(f'python3: {sys.executable}')
    print(f'textutil: {shutil.which("textutil") or "NOT FOUND"}')

    try:
        import requests  # noqa: F401
        print('requests: OK')
    except Exception as e:
        print(f'requests: FAIL ({e})')
        return 1

    ok, out = run([sys.executable, str(FETCH_SCRIPT), '--url', 'https://example.com'])
    print('\n[fetch_podcast_page.py]')
    print('ok:', ok)
    print(out[:800])
    if not ok:
        return 1

    ok, out = run([sys.executable, str(EXPORT_SCRIPT), str(EXAMPLE_MD), '-o', str(TMP_DOCX)])
    print('\n[export_docx.py]')
    print('ok:', ok)
    print(out[:800])
    if not ok:
        return 1

    exists = TMP_DOCX.exists()
    size = TMP_DOCX.stat().st_size if exists else 0
    print(f'exported_docx_exists: {exists}')
    print(f'exported_docx_size: {size}')

    if not exists or size == 0:
        return 1

    print('\nSMOKE TEST PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
