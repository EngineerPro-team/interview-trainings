#!/usr/bin/env python3
"""
Translate EN chapter HTML → VI using Google Translate (unofficial endpoint).
Skips already-translated files unless SD_FORCE=1.

  python3 scripts/translate_system_design.py
  python3 scripts/translate_system_design.py --slug scaling
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup, NavigableString

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_DIR = os.path.join(ROOT, "src", "assets", "content", "system-design", "en")
VI_DIR = os.path.join(ROOT, "src", "assets", "content", "system-design", "vi")

ENDPOINT = "https://translate.googleapis.com/translate_a/single"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15"
SENTINEL = "\n\n@@SPLIT@@\n\n"
MAX_BATCH_CHARS = 3200

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from system_design_config import CHAPTERS  # noqa: E402


def gt_translate(text: str, src: str = "en", dst: str = "vi", retries: int = 4) -> str:
    if not text.strip():
        return text
    qs = urllib.parse.urlencode({
        "client": "gtx", "sl": src, "tl": dst, "dt": "t", "q": text,
    })
    url = f"{ENDPOINT}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = json.loads(r.read().decode("utf-8"))
            return "".join(s[0] for s in (data[0] or []) if s and s[0])
        except Exception as e:
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Translate failed: {last_err}")


def chunk_texts(texts: list[str]) -> list[list[int]]:
    groups: list[list[int]] = []
    cur: list[int] = []
    cur_len = 0
    for i, t in enumerate(texts):
        tl = len(t) + len(SENTINEL)
        if cur and cur_len + tl > MAX_BATCH_CHARS:
            groups.append(cur)
            cur, cur_len = [], 0
        cur.append(i)
        cur_len += tl
    if cur:
        groups.append(cur)
    return groups


def translate_html(html: str) -> str:
    if not html.strip():
        return html
    soup = BeautifulSoup(html, "html.parser")
    nodes: list[NavigableString] = []
    texts: list[str] = []
    for node in soup.find_all(string=True):
        parent = node.parent
        if not parent or parent.name in ("script", "style", "code", "pre"):
            continue
        s = str(node)
        if not s.strip():
            continue
        nodes.append(node)
        texts.append(s)

    if not texts:
        return html

    translated = [None] * len(texts)
    for group in chunk_texts(texts):
        batch = SENTINEL.join(texts[i] for i in group)
        out = gt_translate(batch)
        parts = out.split(SENTINEL.strip())
        if len(parts) != len(group):
            parts = [gt_translate(texts[i]) for i in group]
        for idx, p in zip(group, parts):
            translated[idx] = p

    for node, new in zip(nodes, translated):
        if new is None:
            continue
        orig = str(node)
        lead = re.match(r"^\s*", orig).group(0)
        trail = re.search(r"\s*$", orig).group(0)
        node.replace_with(lead + new + trail)

    return str(soup)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", action="append", help="Only translate these slugs")
    args = parser.parse_args()
    force = os.environ.get("SD_FORCE") == "1"
    os.makedirs(VI_DIR, exist_ok=True)

    slugs = {c["slug"] for c in CHAPTERS}
    if args.slug:
        slugs &= set(args.slug)

    done = 0
    for slug in sorted(slugs):
        en_path = os.path.join(EN_DIR, f"{slug}.html")
        vi_path = os.path.join(VI_DIR, f"{slug}.html")
        if not os.path.isfile(en_path):
            print(f"  ! skip {slug}: no EN file", file=sys.stderr)
            continue
        if os.path.isfile(vi_path) and not force:
            print(f"  · {slug} already translated")
            done += 1
            continue
        html = open(en_path, encoding="utf-8").read()
        print(f"  → {slug} ({len(html)} chars)", flush=True)
        try:
            vi = translate_html(html)
            with open(vi_path, "w", encoding="utf-8") as f:
                f.write(vi + "\n")
            done += 1
            time.sleep(0.6)
        except Exception as e:
            print(f"    ! failed: {e}", file=sys.stderr)
            time.sleep(3)

    print(f"[translate_system_design] {done}/{len(slugs)} VI chapters in {VI_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
