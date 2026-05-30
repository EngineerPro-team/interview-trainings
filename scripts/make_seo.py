#!/usr/bin/env python3
"""
Generate sitemap.xml + robots.txt for the static site.

Emits clean, fragment-free URLs (one per prerendered page) so search engines
can index every route as a real page. Base URL comes from site_config.BASE_URL
so we have a single source of truth.
"""

import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_config import BASE_URL, TOP_ROUTES  # noqa: E402

ROUTE_PRIORITY = {
    "courses":   (0.9, "weekly"),
    "stories":   (0.9, "weekly"),
    "book":      (0.8, "monthly"),
    "mentors":   (0.8, "monthly"),
    "resources": (0.8, "monthly"),
    "podcast":   (0.7, "weekly"),
    "faq":       (0.7, "monthly"),
    "partners":  (0.6, "monthly"),
    "contact":   (0.5, "yearly"),
}


def load_slugs(path: str, var_name: str) -> list[str]:
    with open(os.path.join(SRC, "assets", path), "r", encoding="utf-8") as f:
        raw = f.read()
    m = re.search(rf"window\.{var_name}\s*=\s*(\[.*\])\s*;", raw, re.S)
    if not m:
        return []
    arr = json.loads(m.group(1))
    return [item.get("slug") for item in arr if item.get("slug")]


def main() -> int:
    today = datetime.date.today().isoformat()
    urls: list[tuple[str, str, float, str]] = []

    # Home
    urls.append((f"{BASE_URL}/", today, 1.0, "weekly"))

    # Top-level routes
    for slug, _vi, _en in TOP_ROUTES:
        prio, freq = ROUTE_PRIORITY.get(slug, (0.6, "monthly"))
        urls.append((f"{BASE_URL}/{slug}/", today, prio, freq))

    # Course detail pages
    for s in load_slugs("courses-data.js", "COURSES"):
        urls.append((f"{BASE_URL}/courses/{s}/", today, 0.7, "monthly"))

    # Story detail pages
    for s in load_slugs("stories-data.js", "STORIES"):
        urls.append((f"{BASE_URL}/stories/{s}/", today, 0.6, "monthly"))

    # Build XML
    sm = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for loc, lastmod, prio, freq in urls:
        sm.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{prio}</priority>\n"
            f'    <xhtml:link rel="alternate" hreflang="vi" href="{loc}" />\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{loc}?lang=en" />\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}" />\n'
            "  </url>"
        )
    sm.append("</urlset>\n")

    with open(os.path.join(SRC, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm))

    robots = (
        "# EngineerPro static site\n"
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n"
    )
    with open(os.path.join(SRC, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    print(f"[seo] wrote sitemap.xml with {len(urls)} clean URLs + robots.txt (base={BASE_URL})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
