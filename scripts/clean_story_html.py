#!/usr/bin/env python3
"""
Post-clean originalHtml / originalHtmlEn inside src/assets/stories-data.js:

  1. Drop orphan "<li>Website: </li>" items (residue of the engineerprogurus
     URL strip we did earlier).
  2. Drop empty "Thông tin liên hệ:" / "Contact information:" intros that lead
     into a now-empty bullet list.
  3. Unwrap Google Doc redirect URLs:
       https://www.google.com/url?q=ACTUAL&sa=...&usg=...   →   ACTUAL

Idempotent — safe to re-run.
"""

import json
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORIES_PATH = os.path.join(ROOT, "src", "assets", "stories-data.js")

# Bullets we always want gone (label has no content after the colon).
DEAD_BULLETS = {"website"}

LI_RE = re.compile(
    r"<li>\s*([A-Za-z][A-Za-zÀ-ỹ\s]+?)\s*:\s*(?:&nbsp;|\s)*</li>",
    re.IGNORECASE,
)

# Empty <ul></ul> or <ul> with nothing but whitespace.
EMPTY_UL_RE = re.compile(r"<ul>\s*</ul>", re.IGNORECASE)

# "<p>Thông tin liên hệ:</p>" + (now empty) ul, in either language.
CONTACT_HEADER_RE = re.compile(
    r"<p>\s*(Thông tin liên hệ|Contact information|Contact info)\s*:?\s*</p>\s*(?=<ul>\s*</ul>|<h|<p>|$)",
    re.IGNORECASE,
)

GOOG_REDIR_RE = re.compile(
    r'https?://www\.google\.com/url\?q=([^"&\s\']+)(?:&amp;|&)[^"\s\']*',
    re.IGNORECASE,
)


def unwrap_google_url(html: str) -> str:
    def sub(m: re.Match) -> str:
        # The captured q= value is percent-encoded; decode once.
        return urllib.parse.unquote(m.group(1))
    return GOOG_REDIR_RE.sub(sub, html)


def drop_dead_bullets(html: str) -> str:
    def keep(m: re.Match) -> str:
        label = m.group(1).strip().lower()
        return "" if label in DEAD_BULLETS else m.group(0)
    return LI_RE.sub(keep, html)


def clean(html: str) -> str:
    if not html:
        return html
    out = drop_dead_bullets(html)
    out = unwrap_google_url(out)
    # Tidy up any UL that ended up empty after dropping bullets.
    for _ in range(3):
        new = EMPTY_UL_RE.sub("", out)
        new = CONTACT_HEADER_RE.sub("", new)
        if new == out:
            break
        out = new
    return out


def load_stories() -> tuple[str, str, list[dict]]:
    with open(STORIES_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"(.*?window\.STORIES\s*=\s*)(\[.*\])(\s*;\s*)$", text, re.S)
    if not m:
        raise SystemExit("Could not locate window.STORIES = [...] block")
    return m.group(1), m.group(3), json.loads(m.group(2))


def save_stories(head: str, tail: str, stories: list[dict]) -> None:
    arr_json = json.dumps(stories, ensure_ascii=False, indent=2)
    with open(STORIES_PATH, "w", encoding="utf-8") as f:
        f.write(head + arr_json + tail)


def main() -> int:
    head, tail, stories = load_stories()
    changed = 0
    for s in stories:
        before_html = s.get("originalHtml") or ""
        before_html_en = s.get("originalHtmlEn") or ""
        after_html = clean(before_html)
        after_html_en = clean(before_html_en)
        if after_html != before_html:
            s["originalHtml"] = after_html
            changed += 1
        if after_html_en != before_html_en:
            s["originalHtmlEn"] = after_html_en
            changed += 1
    save_stories(head, tail, stories)
    print(f"[clean_story_html] modified {changed} html fields across {len(stories)} stories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
