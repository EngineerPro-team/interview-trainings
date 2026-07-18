#!/usr/bin/env python3
"""
Anonymity hardening for Success Stories.

For every story flagged `anonymous: true`, make sure NO real name leaks:
  - name field neutralised to "Học viên EngineerPro"
  - title / lead / body regenerated name-free (via parse_stories generators,
    which now use a generic name for anonymous records)
  - the crawled real article (originalTitle / originalHtml, VI + EN) is BLANKED,
    since it repeats the student's real name — renderStoryDetail then falls back
    to our name-free generated title + summary.
  - these fields locked in `manualEdits` so future re-runs never undo them.

externalUrl is kept (used for crawler de-dup) but the "View original on
Substack" button is hidden for anonymous stories in app.js.

Run:  python3 scripts/scrub_anon_stories.py
"""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_stories as ps  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "assets" / "stories-data.js"

BLANK_FIELDS = ("originalTitle", "originalTitleEn", "originalHtml", "originalHtmlEn")
LOCK_FIELDS = (
    "name", "title", "titleEn", "lead", "leadEn", "body", "bodyEn",
    *BLANK_FIELDS,
)


def main() -> int:
    raw = OUT.read_text(encoding="utf-8")
    m = re.search(r"window\.STORIES\s*=\s*(\[.*\]);", raw, re.S)
    arr = json.loads(m.group(1))

    fixed = 0
    for rec in arr:
        if not rec.get("anonymous"):
            continue
        slug = rec.get("slug") or ps.slugify(rec.get("title", "story"))
        rec["name"] = "Học viên EngineerPro"

        rng_vi = random.Random(slug + "::vi")
        rng_en = random.Random(slug + "::en")
        rec["title"] = ps.generate_title(rec, rng_vi, "vi")
        rec["titleEn"] = ps.generate_title(rec, rng_en, "en")
        lead_vi, body_vi = ps.generate_body(rec, rng_vi, "vi")
        lead_en, body_en = ps.generate_body(rec, rng_en, "en")
        rec["lead"], rec["body"] = lead_vi, body_vi
        rec["leadEn"], rec["bodyEn"] = lead_en, body_en

        for f in BLANK_FIELDS:
            if f in rec:
                rec[f] = ""

        locks = set(rec.get("manualEdits") or [])
        locks.update(LOCK_FIELDS)
        rec["manualEdits"] = sorted(locks)
        fixed += 1

    payload = json.dumps(arr, ensure_ascii=False, indent=2)
    header = raw[: raw.index("window.STORIES")]
    OUT.write_text(header + f"window.STORIES = {payload};\n", encoding="utf-8")
    print(f"✓ scrubbed {fixed} anonymous stories (name-free title/body, blanked crawled originals)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
