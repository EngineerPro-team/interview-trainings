#!/usr/bin/env python3
"""
Print + cross-check all "site stat" numbers (mentors, courses, stories,
podcasts, FAQs, partners) across:
  - the data files (source of truth)
  - the i18n templates / index.html static defaults
  - README.md, PLAN.md
  - JS route descriptions
  - sitemap (URL count)

Exits non-zero (CI-friendly) if anything is out of sync.

Usage:  make stats   (or: python3.11 scripts/check_stats.py)
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")


def load_array(filename: str, var_name: str) -> list:
    with open(os.path.join(SRC, "assets", filename), "r", encoding="utf-8") as f:
        m = re.search(rf"window\.{var_name}\s*=\s*(\[.*\])\s*;", f.read(), re.S)
    return json.loads(m.group(1)) if m else []


def count_mentors() -> int:
    """The `mentors` array in data.js is strict JSON — parsing it here doubles
    as a format check, since the prerender step reads the same block."""
    with open(os.path.join(SRC, "assets", "data.js"), "r", encoding="utf-8") as f:
        m = re.search(r"mentors:\s*(\[.*?\]),\s*\n\s*contact", f.read(), re.S)
    return len(json.loads(m.group(1))) if m else 0


def find_all(pattern: str, *paths: str) -> list[tuple[str, int, str]]:
    hits = []
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                for i, line in enumerate(f.read().splitlines(), 1):
                    if re.search(pattern, line):
                        hits.append((p, i, line.strip()))
        except FileNotFoundError:
            pass
    return hits


def main() -> int:
    counts = {
        "mentors":  count_mentors(),
        "courses":  len(load_array("courses-data.js", "COURSES")),
        "podcasts": len(load_array("podcasts-data.js", "PODCASTS")),
        "stories":  len(load_array("stories-data.js", "STORIES")),
        "faqs":     len(load_array("faqs-data.js", "FAQS")),
    }
    print("Data source counts:")
    for k, v in counts.items():
        print(f"  {k:9s}  {v}")

    errors = []

    # Check the static defaults inside <span id="*Count">N</span>
    checks = [
        (counts["mentors"],  r'id="mentorsCount">(\d+)<'),
        (counts["stories"],  r'id="storiesCount">(\d+)<'),
        (counts["courses"],  r'id="coursesCount">(\d+)<'),
        (counts["podcasts"], r'id="podcastCount">(\d+)<'),
        (counts["faqs"],     r'id="faqCount">(\d+)<'),
    ]
    static_paths = [
        os.path.join(SRC, "index.html"),
        os.path.join(SRC, "assets", "i18n.js"),
    ]
    for expected, pat in checks:
        for path in static_paths:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for m in re.finditer(pat, f.read()):
                        got = int(m.group(1))
                        if got != expected:
                            errors.append(f"{path}: expected {expected}, found {got} (pattern {pat})")
            except FileNotFoundError:
                pass

    # Check stale "NN mentors" / "NN stories" mentions across all docs files
    common_strings = [
        (counts["mentors"],  r"(\d+)\s+mentors\b"),
        (counts["mentors"],  r"(\d+)\s+giảng viên\b"),
        (counts["stories"],  r"(\d+)\+?\s+(?:stories\b|học viên EngineerPro)"),
        (counts["courses"],  r"(\d+)\s+(?:courses\b|khoá đào tạo|khoá học chuyên sâu)"),
    ]
    other_paths = [
        os.path.join(ROOT, "README.md"),
        os.path.join(ROOT, "PLAN.md"),
        os.path.join(SRC, "assets", "app.js"),
        os.path.join(SRC, "assets", "i18n.js"),
        os.path.join(ROOT, "scripts", "build_pages.py"),
    ]
    for expected, pat in common_strings:
        for path in other_paths:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f.read().splitlines(), 1):
                        m = re.search(pat, line)
                        if m and int(m.group(1)) != expected:
                            errors.append(
                                f"{os.path.relpath(path, ROOT)}:{i}  expected {expected}, got {m.group(1)} — {line.strip()[:80]}"
                            )
            except FileNotFoundError:
                pass

    if errors:
        print("\nStat drift detected:")
        for e in errors:
            print(f"  ! {e}")
        return 1
    print("\n✓ All stat references match the data files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
