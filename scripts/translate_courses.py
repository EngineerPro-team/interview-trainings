#!/usr/bin/env python3
"""
Translate each course's body HTML (Vietnamese) → English using Google
Translate's free unofficial endpoint, then store the result back in
src/assets/courses-data.js as a new `htmlEn` field on each course.

Run:  make translate-courses  (or: python3.11 scripts/translate_courses.py)
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup, NavigableString

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSES_PATH = os.path.join(ROOT, "src", "assets", "courses-data.js")

ENDPOINT = "https://translate.googleapis.com/translate_a/single"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15"
SENTINEL = "\n\n@@SPLIT@@\n\n"
MAX_BATCH_CHARS = 3500


def gt_translate(text: str, src: str = "vi", dst: str = "en", retries: int = 3) -> str:
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
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
            return "".join(s[0] for s in (data[0] or []) if s and s[0])
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Translate failed after {retries} retries: {last_err}")


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
    if not html or not html.strip():
        return html
    soup = BeautifulSoup(html, "html.parser")
    nodes: list[NavigableString] = []
    texts: list[str] = []
    for node in soup.find_all(string=True):
        parent_name = (node.parent.name if node.parent else "") or ""
        if parent_name.lower() in ("script", "style"):
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
        batch_payload = SENTINEL.join(texts[i] for i in group)
        out = gt_translate(batch_payload)
        parts = out.split(SENTINEL.strip())
        if len(parts) != len(group):
            parts = out.split("@@SPLIT@@")
        if len(parts) != len(group):
            parts = [gt_translate(texts[i]) for i in group]
        for idx, p in zip(group, parts):
            translated[idx] = p.strip("\n")

    for node, new in zip(nodes, translated):
        if new is None:
            continue
        orig = str(node)
        lead = re.match(r"^\s*", orig).group(0)
        trail = re.search(r"\s*$", orig).group(0)
        node.replace_with(lead + new + trail)

    return str(soup)


def load_courses() -> tuple[str, str, list[dict]]:
    with open(COURSES_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"(.*?window\.COURSES\s*=\s*)(\[.*\])(\s*;\s*)$", text, re.S)
    if not m:
        raise SystemExit("Could not locate window.COURSES = [...] block")
    return m.group(1), m.group(3), json.loads(m.group(2))


def save_courses(head: str, tail: str, courses: list[dict]) -> None:
    arr_json = json.dumps(courses, ensure_ascii=False, indent=2)
    with open(COURSES_PATH, "w", encoding="utf-8") as f:
        f.write(head + arr_json + tail)


def main() -> int:
    head, tail, courses = load_courses()
    print(f"[translate_courses] {len(courses)} courses to process")

    for i, c in enumerate(courses, 1):
        html = c.get("html") or ""
        if not html.strip():
            continue
        if c.get("htmlEn"):
            # Already translated; skip (idempotent re-runs)
            print(f"  [{i}/{len(courses)}] {c['slug']}  → already done, skipping")
            continue
        print(f"  [{i}/{len(courses)}] {c['slug']}  ({len(html)} chars)", flush=True)
        try:
            c["htmlEn"] = translate_html(html)
            time.sleep(0.4)
            if i % 3 == 0:
                save_courses(head, tail, courses)
        except Exception as e:
            print(f"    ! failed: {e}", file=sys.stderr)
            time.sleep(3)

    save_courses(head, tail, courses)
    done = sum(1 for c in courses if c.get("htmlEn"))
    print(f"[translate_courses] wrote htmlEn for {done}/{len(courses)} courses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
