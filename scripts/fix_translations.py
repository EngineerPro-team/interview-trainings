#!/usr/bin/env python3
"""
Post-process the machine translations in stories-data.js to clean up the most
common artifacts. Idempotent — safe to re-run.

Targets the known MT failure modes found in the Google-translated EN bodies:
  1. "SKATE/Skate" → "failed/missed"           (Vietnamese "trượt" mistranslated as "ice skate")
  2. "LYING" → "Ly"                             (proper name "Ly" mistranslated as the verb)
  3. "Mr. Lam/Hoa/..." → "Lam/Hoa/..."         (forced English honorific for Vietnamese names)
  4. "gossip" → "casual notes"                  (Vietnamese "tản mạn" / "chia sẻ")
  5. "you guys" → "you"                         (Vietnamese "các bạn" is plural-you, not slang)
  6. Strip EngineerPro marketing boilerplate that was appended to every Google Doc
     ("Engineer Pro is a training center... Contact information...")
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORIES_PATH = os.path.join(ROOT, "src", "assets", "stories-data.js")

# Vietnamese first names that the translator forced into "Mr. X" — but most of
# our stories are casual/informal blog posts, the "Mr." prefix sounds weird.
HONORIFIC_NAMES = [
    "Lam", "Hoa", "Hieu", "Khoa", "Bach", "Long", "Hoang", "Quang",
    "Anh", "Tu", "Tien", "Tuan", "Bao", "Nguyen", "Manh", "Khanh",
    "Nhi", "Cuong", "Duy", "Giang", "Huy", "Son", "Sang", "Tan",
    "Tony", "Triet", "Tung", "Hung", "Phong", "Thanh", "My", "Loi",
    "Linh", "Phuong", "Trang", "Trinh", "Ly", "Casey", "Kyle",
]

# (pattern, replacement, flags) — applied to both originalHtmlEn and the titleEn/originalTitleEn
SUBS = [
    # "TRƯỢT" / "trượt" mistranslated as ice skating
    (re.compile(r"\bSKATE\s+ON\b"), "FAILED"),
    (re.compile(r"\bSKATE\b"), "FAILED"),
    (re.compile(r"\b(?:Skate|skate)\s+on\b"), "missed"),
    (re.compile(r"\bskated\s+on\b"), "did not pass"),
    (re.compile(r"\bskate(?:s|d)?\b"), "miss"),
    # Common noun-name mistakes
    (re.compile(r"\bLYING\b"), "Ly"),
    (re.compile(r"\bLying\s+(?=[A-Z])"), "Ly "),
    # Forced "Mr." honorific for Vietnamese first names
    (re.compile(r"\bMr\.\s+(" + "|".join(HONORIFIC_NAMES) + r")\b"), r"\1"),
    # "You guys" → "you" (Vietnamese "các bạn" is plural-you, not informal)
    (re.compile(r"\bYou guys\b"), "You"),
    (re.compile(r"\byou guys\b"), "you"),
    # "Gossip" misrender of Vietnamese "tản mạn" (musings, notes)
    (re.compile(r"\bgossip\b"), "notes"),
    (re.compile(r"\bGossip\b"), "Notes"),
]

# Marketing boilerplate appended to almost every Google Doc — strip it.
# Pattern: "Engineer Pro is a training center ... Contact information: ..."
BOILERPLATE_BLOCKS = [
    re.compile(
        r"<p>\s*Engineer Pro is a (?:training center|software training)[\s\S]{0,500}?</p>",
        re.IGNORECASE,
    ),
    re.compile(
        r"<p>\s*Engineer Pro is\b[\s\S]{0,400}?(?:big tech|Big Tech)\.\s*</p>",
        re.IGNORECASE,
    ),
    re.compile(
        r"<p>\s*Contact information:?\s*</p>\s*<ul>[\s\S]*?</ul>",
        re.IGNORECASE,
    ),
]


def clean_text(s: str) -> str:
    if not s:
        return s
    for pat, repl in SUBS:
        s = pat.sub(repl, s)
    return s


def clean_html(html: str) -> str:
    if not html:
        return html
    out = clean_text(html)
    for pat in BOILERPLATE_BLOCKS:
        out = pat.sub("", out)
    # Collapse any double-empty paragraphs left behind
    out = re.sub(r"(?:<p>\s*</p>\s*){2,}", "<p></p>", out)
    return out


def load() -> tuple[str, str, list[dict]]:
    with open(STORIES_PATH, "r", encoding="utf-8") as f:
        raw = f.read()
    m = re.match(r"(.*?window\.STORIES\s*=\s*)(\[.*\])(\s*;\s*)$", raw, re.S)
    if not m:
        raise SystemExit("Could not locate window.STORIES = [...] block")
    return m.group(1), m.group(3), json.loads(m.group(2))


def save(head: str, tail: str, data: list[dict]) -> None:
    with open(STORIES_PATH, "w", encoding="utf-8") as f:
        f.write(head + json.dumps(data, indent=2, ensure_ascii=False) + tail)


def main() -> int:
    head, tail, data = load()
    n_text = 0
    n_html = 0
    for s in data:
        # Plain-text title fields
        for k in ("titleEn", "originalTitleEn", "leadEn"):
            v = s.get(k) or ""
            new = clean_text(v)
            if new != v:
                s[k] = new
                n_text += 1
        # HTML body fields
        for k in ("bodyEn", "originalHtmlEn"):
            v = s.get(k) or ""
            new = clean_html(v)
            if new != v:
                s[k] = new
                n_html += 1
    save(head, tail, data)
    print(f"[fix_translations] cleaned {n_text} text fields + {n_html} html fields across {len(data)} stories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
