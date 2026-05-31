#!/usr/bin/env python3
"""
Translate each story's originalHtml + originalTitle (Vietnamese) → English
using Google Translate's free unofficial endpoint, then write the result back
into src/assets/stories-data.js as originalHtmlEn / originalTitleEn.

Run: PYTHON=python3.11 make translate-stories  (or: python3.11 scripts/translate_stories.py)
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
STORIES_PATH = os.path.join(ROOT, "src", "assets", "stories-data.js")

ENDPOINT = "https://translate.googleapis.com/translate_a/single"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15"

# Sentinel inserted between text nodes when batching a single HTTP request.
# Picked so that Google Translate consistently passes it through unchanged.
SENTINEL = "\n\n@@SPLIT@@\n\n"
MAX_BATCH_CHARS = 3500   # stay well under the free endpoint's per-call limit


def gt_translate(text: str, src: str = "vi", dst: str = "en", retries: int = 3) -> str:
    """Translate a single string via the free Google endpoint."""
    if not text.strip():
        return text
    qs = urllib.parse.urlencode({
        "client": "gtx",
        "sl": src,
        "tl": dst,
        "dt": "t",
        "q": text,
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
    """Group indices so each batch stays below MAX_BATCH_CHARS."""
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
    """Translate every visible text node in the HTML, keeping tags intact."""
    if not html or not html.strip():
        return html
    soup = BeautifulSoup(html, "html.parser")

    # Collect translatable text nodes (skip scripts/styles & pure whitespace).
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
        # Build batch
        batch_payload = SENTINEL.join(texts[i] for i in group)
        out = gt_translate(batch_payload)
        parts = out.split(SENTINEL.strip())  # tolerate whitespace drift
        # Realign: Google sometimes re-flows whitespace around the sentinel.
        # Re-split with the canonical sentinel first, then fall back.
        if len(parts) != len(group):
            parts = out.split("@@SPLIT@@")
        if len(parts) != len(group):
            # last-resort: translate each piece individually
            parts = [gt_translate(texts[i]) for i in group]
        for idx, p in zip(group, parts):
            translated[idx] = p.strip("\n")

    # Replace in-place
    for node, new in zip(nodes, translated):
        if new is None:
            continue
        # Preserve leading/trailing whitespace from original (Google often trims).
        orig = str(node)
        lead = re.match(r"^\s*", orig).group(0)
        trail = re.search(r"\s*$", orig).group(0)
        node.replace_with(lead + new + trail)

    return str(soup)


def load_stories() -> tuple[str, str, list[dict]]:
    with open(STORIES_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"(.*?window\.STORIES\s*=\s*)(\[.*\])(\s*;\s*)$", text, re.S)
    if not m:
        raise SystemExit("Could not locate window.STORIES = [...] block")
    head, arr_json, tail = m.group(1), m.group(2), m.group(3)
    return head, tail, json.loads(arr_json)


def save_stories(head: str, tail: str, stories: list[dict]) -> None:
    arr_json = json.dumps(stories, ensure_ascii=False, indent=2)
    with open(STORIES_PATH, "w", encoding="utf-8") as f:
        f.write(head + arr_json + tail)


def main() -> int:
    head, tail, stories = load_stories()
    total = len(stories)
    todo = [
        s for s in stories
        if s.get("originalHtml") and not s.get("originalHtmlEn")
    ]
    print(f"[translate_stories] {len(todo)} of {total} stories need EN translation")

    for i, s in enumerate(stories, 1):
        html = s.get("originalHtml") or ""
        if not html.strip():
            continue
        if s.get("originalHtmlEn") and s.get("originalTitleEn"):
            continue  # already done; safe to re-run

        # manualEdits lock: skip stories whose EN body was hand-curated.
        locks = s.get("manualEdits") or []
        if "originalHtmlEn" in locks:
            continue

        slug = s.get("slug", "?")
        try:
            title_vi = (s.get("originalTitle") or "").strip()
            if title_vi and not s.get("originalTitleEn"):
                s["originalTitleEn"] = gt_translate(title_vi)
            print(f"  [{i}/{total}] {slug}  ({len(html)} chars)", flush=True)
            s["originalHtmlEn"] = translate_html(html)
            # Be polite to the free endpoint
            time.sleep(0.4)
            # Periodic checkpoint so a mid-run failure doesn't lose progress
            if i % 5 == 0:
                save_stories(head, tail, stories)
        except Exception as e:
            print(f"    ! failed: {e}", file=sys.stderr)
            time.sleep(3)

    save_stories(head, tail, stories)
    done = sum(1 for s in stories if s.get("originalHtmlEn"))
    print(f"[translate_stories] wrote originalHtmlEn for {done}/{total} stories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
