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
# Where to write sitemap.xml + robots.txt. Default: src/ (so `make github`
# picks them up when copying src/ -> docs/). Local builds override via
# EP_OUT=_local to keep tracked src/ files clean.
OUT_DIR = os.path.join(ROOT, os.environ.get("EP_OUT", "src"))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_config import BASE_URL, BASE_PATH, SITE_BASE, TOP_ROUTES, RESOURCES_ALIASES  # noqa: E402

ROUTE_PRIORITY = {
    "courses":       (0.9, "weekly"),
    "stories":       (0.9, "weekly"),
    "book":          (0.8, "monthly"),
    "system-design": (0.8, "monthly"),
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


def load_sd_chapter_slugs() -> list[str]:
    from build_pages import load_sd_chapters  # noqa: WPS433 — shared parser

    return [ch["slug"] for ch in load_sd_chapters() if ch.get("available")]


def main() -> int:
    today = datetime.date.today().isoformat()
    urls: list[tuple[str, str, float, str]] = []

    # Home
    urls.append((f"{SITE_BASE}/", today, 1.0, "weekly"))

    # Top-level routes
    for slug, _vi, _en in TOP_ROUTES:
        prio, freq = ROUTE_PRIORITY.get(slug, (0.6, "monthly"))
        urls.append((f"{SITE_BASE}/{slug}/", today, prio, freq))

    # Course detail pages
    for s in load_slugs("courses-data.js", "COURSES"):
        urls.append((f"{SITE_BASE}/courses/{s}/", today, 0.7, "monthly"))

    # Story detail pages
    for s in load_slugs("stories-data.js", "STORIES"):
        urls.append((f"{SITE_BASE}/stories/{s}/", today, 0.6, "monthly"))

    # System Design chapter pages
    for s in load_sd_chapter_slugs():
        urls.append((f"{SITE_BASE}/system-design/{s}/", today, 0.65, "monthly"))

    # Resources deep-link sub-pages (/resources/hr-screen/, /resources/cs-fundamental/, …)
    for slug in RESOURCES_ALIASES:
        urls.append((f"{SITE_BASE}/resources/{slug}/", today, 0.75, "monthly"))

    # Build XML
    sm = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for loc, lastmod, prio, freq in urls:
        # NOTE: dropping hreflang="en" advertisements until we generate real
        # /en/ pages with English source HTML + self-canonicals. Re-add later.
        sm.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{prio}</priority>\n"
            f'    <xhtml:link rel="alternate" hreflang="vi" href="{loc}" />\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}" />\n'
            "  </url>"
        )
    sm.append("</urlset>\n")

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm))

    robots = (
        "# EngineerPro static site\n"
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {SITE_BASE}/sitemap.xml\n"
    )
    with open(os.path.join(OUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    rel_out = os.path.relpath(OUT_DIR, ROOT)
    print(f"[seo] wrote {rel_out}/sitemap.xml ({len(urls)} URLs) + robots.txt (base={SITE_BASE})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
