#!/usr/bin/env python3
"""Clean up EN/VI chapter HTML — images, artifacts, structure."""

from __future__ import annotations

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SD = os.path.join(ROOT, "src", "assets", "content", "system-design")


def fix_html(html: str) -> str:
    html = re.sub(r"\{(?:width|chiều rộng)=\d+\}", "", html, flags=re.I)
    # Images must not live inside headings (breaks outline + accessibility)
    html = re.sub(
        r"<h2>\s*(<img[^>]+>)\s*</h2>",
        r'<figure class="sd-figure">\1</figure>',
        html,
        flags=re.I,
    )
    html = re.sub(r"<p>\s*(<img[^>]+>)\s*</p>", r'<figure class="sd-figure">\1</figure>', html, flags=re.I)
    html = re.sub(
        r'<div style="[^"]*">\s*(<img[^>]+>)\s*</div>',
        r'<figure class="sd-figure">\1</figure>',
        html,
        flags=re.I,
    )
    # Escaped <img> inside <pre><code> (markdown artifact) → real figure
    html = re.sub(
        r'<pre><code>&lt;img src="([^"]+)" alt="([^"]*)" width="(\d+)"&gt;\s*</code></pre>',
        r'<figure class="sd-figure"><img src="\1" alt="\2" width="\3" loading="lazy" /></figure>',
        html,
        flags=re.I,
    )
    if "<table>" in html and 'class="sd-table"' not in html:
        html = html.replace("<table>", '<table class="sd-table">')
    return html


def main() -> int:
    n = 0
    for lang in ("en", "vi"):
        d = os.path.join(SD, lang)
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            if not name.endswith(".html"):
                continue
            path = os.path.join(d, name)
            orig = open(path, encoding="utf-8").read()
            out = fix_html(orig)
            if out != orig:
                open(path, "w", encoding="utf-8").write(out + "\n")
                n += 1
                print(f"  fixed {lang}/{name}")
    print(f"[fix_system_design_html] {n} files updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
