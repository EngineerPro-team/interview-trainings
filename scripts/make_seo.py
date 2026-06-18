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
import subprocess
import sys
from functools import lru_cache

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
# Where to write sitemap.xml + robots.txt. Default: src/ (so `make github`
# picks them up when copying src/ -> docs/). Local builds override via
# EP_OUT=_local to keep tracked src/ files clean.
OUT_DIR = os.path.join(ROOT, os.environ.get("EP_OUT", "src"))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_config import (  # noqa: E402
    BASE_URL,
    BASE_PATH,
    SITE_BASE,
    TOP_ROUTES,
    RESOURCES_ALIASES,
    SYSTEM_DESIGN_URL_SLUG,
)

# --- Accurate <lastmod> ------------------------------------------------------
# Google only trusts <lastmod> when it is "verifiably accurate"; if every URL
# is stamped with the build date it concludes the value is junk and ignores it
# (and crawls/indexes lazily). So we derive each URL's lastmod from the last
# git commit that touched the *content source* behind that page, not the build
# clock. Shell-driven pages fall back to the SPA shell's own commit date.

# Repo-relative source files that render every prerendered page (used as a
# fallback / for pages without a dedicated data file).
SHELL_SOURCES = ("src/index.html", "src/assets/app.js")

# Per top-level route → the content source(s) that actually drive it.
TOP_ROUTE_SOURCES = {
    "courses": ("src/assets/courses-data.js",),
    SYSTEM_DESIGN_URL_SLUG: ("src/assets/system-design-data.js",),
    "resources": ("src/assets/resources-data.js",),
    "mentors": ("src/assets/data.js",),
    "stories": ("src/assets/stories-data.js",),
    "podcast": ("src/assets/podcasts-data.js",),
    "partners": ("src/assets/data.js",),
    "faq": ("src/assets/faqs-data.js",),
    "contact": ("src/assets/data.js",),
}

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@lru_cache(maxsize=None)
def _git_last_date(path_rel: str) -> str | None:
    """Date (YYYY-MM-DD) of the last commit touching ``path_rel``, or None."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", path_rel],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    date = out.stdout.strip()
    return date if _DATE_RE.match(date) else None


def last_mod(*path_rels: str) -> str:
    """Most-recent git commit date among the given repo-relative source files.

    Falls back to filesystem mtime, then today, so the sitemap always carries a
    value — but a real, content-derived one whenever git history is available.
    """
    dates = [d for p in path_rels if (d := _git_last_date(p))]
    if dates:
        return max(dates)
    for p in path_rels:
        ap = os.path.join(ROOT, p)
        if os.path.exists(ap):
            return datetime.date.fromtimestamp(os.path.getmtime(ap)).isoformat()
    return datetime.date.today().isoformat()


ROUTE_PRIORITY = {
    "courses":       (0.9, "weekly"),
    "stories":       (0.9, "weekly"),
    "book":          (0.8, "monthly"),
    SYSTEM_DESIGN_URL_SLUG: (0.8, "monthly"),
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
    urls: list[tuple[str, str, float, str]] = []

    # Home — driven by the SPA shell + hand-curated site data.
    urls.append((f"{SITE_BASE}/", last_mod(*SHELL_SOURCES, "src/assets/data.js"), 1.0, "weekly"))

    # Top-level routes — lastmod tracks each route's real content source.
    for slug, _vi, _en in TOP_ROUTES:
        prio, freq = ROUTE_PRIORITY.get(slug, (0.6, "monthly"))
        sources = TOP_ROUTE_SOURCES.get(slug, SHELL_SOURCES)
        urls.append((f"{SITE_BASE}/{slug}/", last_mod(*sources), prio, freq))

    # Course detail pages
    courses_mod = last_mod("src/assets/courses-data.js")
    for s in load_slugs("courses-data.js", "COURSES"):
        urls.append((f"{SITE_BASE}/courses/{s}/", courses_mod, 0.7, "monthly"))

    # Story detail pages
    stories_mod = last_mod("src/assets/stories-data.js")
    for s in load_slugs("stories-data.js", "STORIES"):
        urls.append((f"{SITE_BASE}/stories/{s}/", stories_mod, 0.6, "monthly"))

    # System Design chapter pages — per-chapter content files give real dates.
    for s in load_sd_chapter_slugs():
        mod = last_mod(
            f"src/assets/content/system-design/vi/{s}.html",
            f"src/assets/content/system-design/en/{s}.html",
            "src/assets/system-design-data.js",
        )
        urls.append((f"{SITE_BASE}/{SYSTEM_DESIGN_URL_SLUG}/{s}/", mod, 0.65, "monthly"))

    # Resources deep-link sub-pages (/resources/hr-screen/, /resources/cs-fundamental/, …)
    resources_mod = last_mod("src/assets/resources-data.js", "scripts/site_config.py")
    # The interview-formats block is driven by its own data file, so track that too.
    formats_mod = last_mod(
        "src/assets/interview-formats-data.js",
        "src/assets/resources-data.js",
        "scripts/site_config.py",
    )
    for slug in RESOURCES_ALIASES:
        mod = formats_mod if slug == "interview-formats" else resources_mod
        urls.append((f"{SITE_BASE}/resources/{slug}/", mod, 0.75, "monthly"))

    # Per-company Interview Format landing pages (prerendered, indexable).
    from build_pages import load_interview_format_companies  # noqa: WPS433 — shared parser
    for cid, _cname in load_interview_format_companies():
        urls.append((f"{SITE_BASE}/resources/interview-formats/{cid}/", formats_mod, 0.6, "monthly"))

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
