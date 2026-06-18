#!/usr/bin/env python3
"""
Static prerender for the SPA: turns hash routes into real path-based HTML files
that search engines + social crawlers can index without running JS.

For every route we want indexed, we emit `docs/<path>/index.html` based on the
master `src/index.html` template, with these patches:

  1. `<title>`, `<meta name="description">`, `<link rel="canonical">`, OG/Twitter
     tags swapped to be route-specific.
  2. JSON-LD block swapped to add route-specific schema (Course / Article /
     ItemList / FAQPage / BreadcrumbList) on top of the global Organization+
     WebSite schema.
  3. A small inline `<script>` is prepended that translates the path into a
     hash (`/courses/foo/` → `#course/foo`) and pre-seeds `location.hash`
     BEFORE the SPA's app.js runs. The user still ends up on the same SPA
     state — but with a clean URL in the address bar (we then `replaceState`
     back to the path so the hash never appears).
  4. Pre-rendered visible content (route h1 + lead + cover image for detail
     pages) is injected into the matching `<section data-route="...">` so
     Googlebot's first paint sees real text, not an empty shell.

Outputs:
  docs/index.html              (home, untouched copy from src/)
  docs/courses/index.html      (courses listing)
  docs/courses/<slug>/index.html
  docs/stories/index.html
  docs/stories/<slug>/index.html
  docs/book/index.html
  docs/resources/index.html
  docs/mentors/index.html
  docs/podcast/index.html
  docs/partners/index.html
  docs/faq/index.html
  docs/contact/index.html
"""

import datetime
import html
import json
import os
import re
import subprocess
import sys
from functools import lru_cache

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
# Output dir defaults to docs/ (production); override with EP_OUT=_local for local builds.
DOCS = os.path.join(ROOT, os.environ.get("EP_OUT", "docs"))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_config import (  # noqa: E402
    BASE_URL,
    BASE_PATH,
    SITE_BASE,
    TOP_ROUTES,
    RESOURCES_ALIASES,
    SITE_NAME,
    OG_IMAGE,
    SYSTEM_DESIGN_URL_SLUG,
)

# First publish date of the original v2 System Design set (used as datePublished
# in Article schema; dateModified is derived from each chapter's git history).
SD_V2_PUBLISHED = "2026-06-08"
_SD_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@lru_cache(maxsize=None)
def _git_last_date(path_rel: str) -> str | None:
    """Date (YYYY-MM-DD) of the last commit touching ``path_rel``, or None."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", path_rel],
            cwd=ROOT, capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    d = out.stdout.strip()
    return d if _SD_DATE_RE.match(d) else None


def content_last_mod(*path_rels: str) -> str:
    """Most-recent git commit date among the given sources; falls back to mtime/today."""
    dates = [d for p in path_rels if (d := _git_last_date(p))]
    if dates:
        return max(dates)
    for p in path_rels:
        ap = os.path.join(ROOT, p)
        if os.path.exists(ap):
            return datetime.date.fromtimestamp(os.path.getmtime(ap)).isoformat()
    return datetime.date.today().isoformat()


def _build_version() -> str:
    """A short token that changes per deploy, used to cache-bust JS/CSS assets
    so returning visitors never run stale app.js / data files after a deploy."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        )
        h = out.stdout.strip()
        if re.match(r"^[0-9a-f]{6,}$", h):
            return h
    except (OSError, subprocess.SubprocessError):
        pass
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


BUILD_VERSION = _build_version()


# ---------- helpers ----------------------------------------------------------

def load_data_array(filename: str, var_name: str) -> list[dict]:
    with open(os.path.join(SRC, "assets", filename), "r", encoding="utf-8") as f:
        raw = f.read()
    m = re.search(rf"window\.{var_name}\s*=\s*(\[.*\])\s*;", raw, re.S)
    return json.loads(m.group(1)) if m else []


def load_data_object(filename: str, var_name: str) -> dict:
    with open(os.path.join(SRC, "assets", filename), "r", encoding="utf-8") as f:
        raw = f.read()
    m = re.search(rf"window\.{var_name}\s*=\s*(\{{.*\}})\s*;", raw, re.S)
    return json.loads(m.group(1)) if m else {}


def load_sd_chapters() -> list[dict]:
    """Parse chapter rows from system-design-data.js (JS object literal, not strict JSON)."""
    path = os.path.join(SRC, "assets", "system-design-data.js")
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    chapters: list[dict] = []
    for line in raw.splitlines():
        if "slug:" not in line:
            continue
        n_m = re.search(r"n:\s*(\d+)", line)
        slug_m = re.search(r'slug:\s*"([^"]+)"', line)
        title_m = re.search(r'title:\s*"([^"]*)"', line)
        title_en_m = re.search(r'titleEn:\s*"([^"]*)"', line)
        avail_m = re.search(r"available:\s*(true|false)", line)
        if not (n_m and slug_m and title_m and title_en_m and avail_m):
            continue
        chapters.append({
            "n": int(n_m.group(1)),
            "slug": slug_m.group(1),
            "title": title_m.group(1),
            "titleEn": title_en_m.group(1),
            "available": avail_m.group(1) == "true",
        })
    return chapters


def attr(s: str) -> str:
    """Escape for inside double-quoted HTML attribute."""
    return html.escape(str(s or ""), quote=True)


def text(s: str) -> str:
    return html.escape(str(s or ""), quote=False)


def truncate(s: str, n: int = 160) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------- template patching ------------------------------------------------

HEAD_REPLACEMENTS = [
    # (search regex, replacement template using {placeholders})
    (
        re.compile(
            r'<title>[^<]*</title>',
        ),
        "<title>{title}</title>",
    ),
    (
        re.compile(
            r'<meta\s+name="description"\s+content="[^"]*"\s*/?>',
        ),
        '<meta name="description" content="{description}" />',
    ),
    (
        re.compile(
            r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>',
        ),
        '<link rel="canonical" href="{canonical}" />',
    ),
    (
        re.compile(
            r'<meta\s+property="og:title"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="og:title" content="{og_title}" />',
    ),
    (
        re.compile(
            r'<meta\s+property="og:description"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="og:description" content="{description}" />',
    ),
    (
        re.compile(
            r'<meta\s+property="og:url"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="og:url" content="{canonical}" />',
    ),
    (
        re.compile(
            r'<meta\s+name="twitter:title"\s+content="[^"]*"\s*/?>',
        ),
        '<meta name="twitter:title" content="{og_title}" />',
    ),
    (
        re.compile(
            r'<meta\s+name="twitter:description"\s+content="[^"]*"\s*/?>',
        ),
        '<meta name="twitter:description" content="{description}" />',
    ),
    (
        re.compile(
            r'<meta\s+name="twitter:url"\s+content="[^"]*"\s*/?>',
        ),
        '<meta name="twitter:url" content="{canonical}" />',
    ),
    (
        re.compile(
            r'<link\s+rel="alternate"\s+hreflang="vi"\s+href="[^"]*"\s*/?>',
        ),
        '<link rel="alternate" hreflang="vi" href="{canonical}" />',
    ),
    # Strip the EN hreflang — until /en/ pages exist with their own English
    # source HTML + self-canonical, advertising ?lang=en is a Vietnamese page
    # canonicalising back to itself, which Google ignores as a language alt.
    (
        re.compile(
            r'<link\s+rel="alternate"\s+hreflang="en"\s+href="[^"]*"\s*/?>\s*\n?',
        ),
        '',
    ),
    (
        re.compile(
            r'<link\s+rel="alternate"\s+hreflang="x-default"\s+href="[^"]*"\s*/?>',
        ),
        '<link rel="alternate" hreflang="x-default" href="{canonical}" />',
    ),
    # OG image — keep but turn into absolute
    (
        re.compile(
            r'<meta\s+property="og:image"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="og:image" content="{og_image}" />',
    ),
    (
        re.compile(
            r'<meta\s+property="og:image:secure_url"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="og:image:secure_url" content="{og_image}" />',
    ),
    # MIME type should match the actual image extension (webp/png/jpg/svg).
    (
        re.compile(
            r'<meta\s+property="og:image:type"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="og:image:type" content="{og_image_type}" />',
    ),
    # Actual pixel dimensions of the per-page image (FB/Twitter render
    # better when these match; mismatched values cause ugly cropping).
    (
        re.compile(
            r'<meta\s+property="og:image:width"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="og:image:width" content="{og_image_w}" />',
    ),
    (
        re.compile(
            r'<meta\s+property="og:image:height"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="og:image:height" content="{og_image_h}" />',
    ),
    (
        re.compile(
            r'<meta\s+property="og:image:alt"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="og:image:alt" content="{og_image_alt}" />',
    ),
    (
        re.compile(
            r'<meta\s+name="twitter:image"\s+content="[^"]*"\s*/?>',
        ),
        '<meta name="twitter:image" content="{og_image}" />',
    ),
    # Zalo previews — use the same image/title as OG so detail pages don't
    # fall back to the generic home share card.
    (
        re.compile(
            r'<meta\s+property="zalo:title"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="zalo:title" content="{og_title}" />',
    ),
    (
        re.compile(
            r'<meta\s+property="zalo:image"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="zalo:image" content="{og_image}" />',
    ),
    # og:type per page kind (article vs website vs ...)
    (
        re.compile(
            r'<meta\s+property="og:type"\s+content="[^"]*"\s*/?>',
        ),
        '<meta property="og:type" content="{og_type}" />',
    ),
]


def image_dims(absolute_url: str) -> tuple[int, int]:
    """Read pixel dimensions of an image whose absolute URL maps to a
    file under docs/ (or src/). Falls back to (1200, 630) if missing —
    that's the FB-recommended default for the share card."""
    if not absolute_url:
        return 1200, 630
    rel = absolute_url
    for prefix in (SITE_BASE, BASE_URL):
        if prefix and rel.startswith(prefix):
            rel = rel[len(prefix):]
            break
    rel = rel.lstrip("/")
    for root in (DOCS, SRC):
        candidate = os.path.join(root, rel)
        if os.path.isfile(candidate):
            try:
                from PIL import Image
                with Image.open(candidate) as im:
                    return im.size
            except Exception:
                return 1200, 630
    return 1200, 630


def absolutise(url: str) -> str:
    """Make an asset URL absolute so social-network scrapers (Facebook
    Messenger, Twitter, LinkedIn, ...) can fetch it. Zalo is permissive
    and will resolve relative URLs against og:url; Facebook/Twitter
    won't, and silently drop the preview image."""
    if not url:
        return url
    if url.startswith(("http://", "https://")):
        return url
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return BASE_URL + url
    return f"{SITE_BASE}/{url.lstrip('./')}"


def _mime_for(url: str) -> str:
    """Best-effort MIME from URL extension; falls back to image/png."""
    u = (url or "").lower().split("?")[0].split("#")[0]
    if u.endswith(".webp"): return "image/webp"
    if u.endswith(".jpg") or u.endswith(".jpeg"): return "image/jpeg"
    if u.endswith(".svg"): return "image/svg+xml"
    if u.endswith(".gif"): return "image/gif"
    return "image/png"


PLACEHOLDER_ORIGIN = "https://engineerpro-academy.github.io"


def fix_asset_paths(template: str) -> str:
    """Patch the master template for the current deploy target:
      - Rewrite the placeholder origin (used in the source for OG/JSON-LD) to
        the real `SITE_BASE` (origin + subpath).
      - Convert relative `assets/...` URLs to absolute `{BASE_PATH}/assets/...`
        so subfolder prerendered pages still find them.
      - Rewrite internal `<a href="/courses/...">` to include the subpath.
      - Inject `window.EP_BASE_PATH` so app.js can construct subpath URLs at
        runtime.
    Works whether `BASE_PATH` is empty (root deploy) or non-empty (project
    Pages, e.g. `/interview-trainings`).
    """
    out = template
    # 1. Rewrite placeholder origin to the real deploy origin+subpath.
    out = out.replace(PLACEHOLDER_ORIGIN, SITE_BASE)
    # 2. Asset paths
    out = re.sub(r'(src|href)="assets/', rf'\1="{BASE_PATH}/assets/', out)
    # 3. Internal route links
    if BASE_PATH:
        out = re.sub(
            r'href="/(courses|book|system-design-material|mock|resources|mentors|stories|podcast|partners|faq|terms|contact)/"',
            rf'href="{BASE_PATH}/\1/"',
            out,
        )
    # 4. Embed BASE_PATH as a global before app.js loads
    base_path_inject = f'<script>window.EP_BASE_PATH = "{BASE_PATH}";</script>\n    '
    out = out.replace(
        f'<script src="{BASE_PATH}/assets/i18n.js">',
        base_path_inject + f'<script src="{BASE_PATH}/assets/i18n.js">',
    )
    # 5. Cache-bust local JS/CSS so a deploy never serves stale app.js / data.
    out = re.sub(
        r'(src|href)="([^"]*/assets/[^"?]+\.(?:js|css))"',
        rf'\1="\2?v={BUILD_VERSION}"',
        out,
    )
    return out


def patch_head(template: str, *, title: str, description: str, canonical: str,
               og_image: str, og_title: str | None = None,
               og_type: str = "website",
               og_image_alt: str | None = None) -> str:
    og_title = og_title or title
    w, h = image_dims(og_image)
    ctx = {
        "title": attr(title),
        "description": attr(description),
        "canonical": attr(canonical),
        "og_image": attr(og_image),
        "og_image_type": attr(_mime_for(og_image)),
        "og_image_w": str(w),
        "og_image_h": str(h),
        "og_image_alt": attr(og_image_alt or og_title),
        "og_title": attr(og_title),
        "og_type": attr(og_type),
    }
    out = template
    for pat, repl in HEAD_REPLACEMENTS:
        new_repl = repl.format(**ctx)
        out, _ = pat.subn(new_repl, out, count=1)
    return out


# Replace the global JSON-LD with global + per-page schema graph.
JSONLD_RE = re.compile(
    r'<script\s+type="application/ld\+json">\s*(\{.*?\})\s*</script>',
    re.S,
)


def patch_jsonld(template: str, extra_nodes: list[dict]) -> str:
    m = JSONLD_RE.search(template)
    if not m:
        return template
    try:
        base = json.loads(m.group(1))
    except json.JSONDecodeError:
        return template
    graph = base.get("@graph", []) + extra_nodes
    base["@graph"] = graph
    new_block = (
        '<script type="application/ld+json">\n'
        + json.dumps(base, indent=2, ensure_ascii=False)
        + "\n</script>"
    )
    return template[: m.start()] + new_block + template[m.end():]


# Prepend the bootstrap script that turns /courses/foo/ → #course/foo BEFORE
# app.js runs, so the SPA renders the right route immediately.
# The previous version of build_pages injected a boot script that did
# `location.hash = "#course/foo"` so a hash-based router could pick it up.
# That mutated clean URLs (/courses/foo/) into hash URLs (/courses/foo/#course/foo)
# which weakened the SPA's clean-URL UX. parseHash() in app.js now reads
# `location.pathname` directly, so no bootstrap is needed.
PATH_BOOT_SCRIPT = ""


def inject_boot_script(template: str) -> str:
    if not PATH_BOOT_SCRIPT:
        return template
    return template.replace("</head>", PATH_BOOT_SCRIPT + "  </head>", 1)


# Inject prerendered HTML INTO an existing mount node (e.g. the empty
# <article id="storyArticle"></article>) — replaces its inner contents in
# place. Prevents duplicate IDs and lets the SPA hydrate the same element.
def inject_into_mount(template: str, mount_id: str, inner_html: str) -> str:
    pat = re.compile(
        r'(<(\w+)[^>]*\bid="' + re.escape(mount_id) + r'"[^>]*>)(.*?)(</\2>)',
        re.S,
    )
    return pat.sub(
        lambda m: m.group(1) + "\n<!-- prerendered SEO content -->\n"
                  + inner_html + "\n<!-- /prerendered -->\n" + m.group(4),
        template,
        count=1,
    )


# For a single prerendered page, also un-hide the matching <section> so the
# crawler/no-JS user actually sees the body. The SPA's hashchange/popstate
# handler will continue to manage `hidden` after hydration.
SHOW_ROUTE_STYLE_TMPL = (
    "\n    <style id=\"prerenderShowRoute\">"
    "section.route[data-route=\"{route}\"][hidden]{{display:block !important;}}"
    "section.route[data-route=\"{route}\"]{{display:block !important;}}"
    "section.route:not([data-route=\"{route}\"]){{display:none !important;}}"
    "</style>\n"
)


def show_route_style(template: str, route: str) -> str:
    style = SHOW_ROUTE_STYLE_TMPL.format(route=route)
    return template.replace("</head>", style + "  </head>", 1)

# ---------- per-route builders ----------------------------------------------

# Per-route OG image override. Routes not listed here fall back to the generic
# site-wide OG_IMAGE so social shares of any unmapped route still get a usable
# preview card. Paths are relative to site root (will be absolutised).
ROUTE_OG_IMAGES = {
    "mock": "/assets/img/mock-interview-cover.jpg",
    SYSTEM_DESIGN_URL_SLUG: "/assets/img/system-design-cover.png",
}

SD_AUTHORS = [
    {"name": "Phạm Ngọc Lâm", "url": "https://www.linkedin.com/in/lam0895/"},
    {"name": "Lê Quang Hoà", "url": "https://www.linkedin.com/in/harry-le-quang-hoa-32210066/"},
]

SD_SOURCE_NOTE = "Nội dung gốc bởi EngineerPro"


def sd_author_schema() -> list[dict]:
    return [{"@type": "Person", "name": a["name"], "url": a["url"]} for a in SD_AUTHORS]


def sd_chapter_description(ch: dict) -> str:
    n = ch.get("n", "")
    title_vi = ch.get("title", "")
    return truncate(
        f"Chương {n}: {title_vi} — case study System Design Interview (VI & EN). "
        f"Biên soạn gốc bởi EngineerPro.",
        160,
    )


def sd_chapter_intro_snippet(slug: str, limit: int = 320) -> str:
    """First plain-text paragraph from VI chapter HTML for prerender/SEO."""
    path = os.path.join(SRC, "assets", "content", "system-design", "vi", f"{slug}.html")
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    m = re.search(r"<p[^>]*>(.*?)</p>", raw, re.DOTALL | re.IGNORECASE)
    source = m.group(1) if m else raw
    plain = re.sub(r"<[^>]+>", " ", source)
    plain = re.sub(r"\s+", " ", plain).strip()
    if not plain:
        return ""
    if len(plain) <= limit:
        return plain
    cut = plain[: limit - 1].rsplit(" ", 1)[0]
    return cut + "…"


def build_top_route(template: str, slug: str, title_vi: str, title_en: str,
                    description: str, snippet_html: str = "") -> str:
    title = f"{title_vi} · {SITE_NAME} — Luyện phỏng vấn Big Tech"
    canonical = f"{SITE_BASE}/{slug}/"
    og_image = SITE_BASE + ROUTE_OG_IMAGES.get(slug, OG_IMAGE)
    out = patch_head(template, title=title, description=description,
                     canonical=canonical,
                     og_image=og_image,
                     og_title=f"{title_vi} · {SITE_NAME}",
                     og_image_alt=f"{title_vi} — {SITE_NAME}")
    extra = [
        {
            "@type": "WebPage",
            "@id": canonical,
            "url": canonical,
            "name": f"{title_vi} · {SITE_NAME}",
            "description": description,
            "isPartOf": {"@id": f"{SITE_BASE}/#website"},
            "inLanguage": "vi",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": title_vi, "item": canonical},
            ],
        },
    ]
    out = patch_jsonld(out, extra)
    out = show_route_style(out, slug)
    out = inject_boot_script(out)
    return out


def build_home(template: str) -> str:
    title = f"{SITE_NAME} — Chinh phục Big Tech cùng mentor thực chiến"
    description = (
        "100% mentors đến từ Big Tech — Google, Amazon, TikTok, Shopee, Spotify, "
        "Uber. Lộ trình rõ ràng để chinh phục offer Big Tech."
    )
    canonical = f"{SITE_BASE}/"
    out = patch_head(template, title=title, description=description,
                     canonical=canonical, og_image=SITE_BASE + OG_IMAGE)

    # Tell Google the 9 top-level pages so it can pick sitelinks faster.
    nav_items = [
        {
            "@type": "SiteNavigationElement",
            "@id": f"{SITE_BASE}/{slug}/#nav",
            "name": title_vi,
            "alternateName": title_en,
            "url": f"{SITE_BASE}/{slug}/",
        }
        for slug, title_vi, title_en in TOP_ROUTES
    ]
    # Plus an ItemList that ranks them (Google prefers explicit ordering).
    item_list = {
        "@type": "ItemList",
        "@id": f"{SITE_BASE}/#mainnav",
        "name": f"{SITE_NAME} — Main navigation",
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "numberOfItems": len(TOP_ROUTES),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx,
                "name": title_vi,
                "url": f"{SITE_BASE}/{slug}/",
            }
            for idx, (slug, title_vi, _) in enumerate(TOP_ROUTES, start=1)
        ],
    }
    out = patch_jsonld(out, nav_items + [item_list])
    out = show_route_style(out, "home")
    return out


def build_course_detail(template: str, c: dict, en: dict) -> str:
    title_vi = c.get("title", "")
    title_en = (en.get("title") or title_vi)
    blurb_vi = c.get("blurb", "")
    blurb_en = (en.get("blurb") or blurb_vi)

    title = f"{title_vi} · {SITE_NAME} — Big Tech Interview Prep"
    description = truncate(blurb_vi, 160)
    canonical = f"{SITE_BASE}/courses/{c['slug']}/"
    cover = absolutise(c.get("cover") or (SITE_BASE + OG_IMAGE))

    out = patch_head(template, title=title, description=description,
                     canonical=canonical, og_image=cover, og_title=title_vi)

    extra = [{
        "@type": "Course",
        "@id": canonical + "#course",
        "name": title_vi,
        "alternateName": title_en,
        "description": blurb_vi,
        "url": canonical,
        "provider": {"@id": f"{SITE_BASE}/#org"},
        "inLanguage": "vi",
        "image": cover,
    }, {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Courses", "item": f"{SITE_BASE}/courses/"},
            {"@type": "ListItem", "position": 3, "name": title_vi, "item": canonical},
        ],
    }]
    out = patch_jsonld(out, extra)

    # Inner contents only — no wrapping <article id="courseArticle">, since we
    # inject INTO the existing mount in the template (avoid duplicate IDs).
    snippet = (
        f'  <header class="article__head">'
        f'    <h1>{text(title_vi)}</h1>'
        f'    <p class="article__lede">{text(blurb_vi)}</p>'
        f'    <p class="muted"><a href="{attr(BASE_PATH)}/courses/" data-href="#courses">← All courses</a></p>'
        f'  </header>'
        f'  <img class="article__cover" src="{attr(cover)}" alt="{attr(title_vi)}" loading="lazy" />'
    )
    out = inject_into_mount(out, "courseArticle", snippet)
    out = show_route_style(out, "course")
    out = inject_boot_script(out)
    return out


def build_story_detail(template: str, s: dict) -> str:
    title_vi = s.get("originalTitle") or s.get("title") or ""
    title_en = s.get("originalTitleEn") or s.get("titleEn") or title_vi
    lead_vi = re.sub(r"<[^>]+>", " ", s.get("lead", "")).strip()
    cover = absolutise(s.get("cover") or (SITE_BASE + OG_IMAGE))

    title = f"{title_vi} · {SITE_NAME}"
    description = truncate(lead_vi, 160) or f"Success story tại EngineerPro: {title_vi}"
    canonical = f"{SITE_BASE}/stories/{s['slug']}/"

    out = patch_head(template, title=title, description=description,
                     canonical=canonical, og_image=cover, og_title=title_vi,
                     og_type="article")

    extra = [{
        "@type": "Article",
        "@id": canonical + "#article",
        "headline": title_vi,
        "alternativeHeadline": title_en,
        "description": description,
        "url": canonical,
        "image": cover,
        "author": (
            {"@type": "Person", "name": s["name"]}
            if s.get("name") else {"@id": f"{SITE_BASE}/#org"}
        ),
        "publisher": {"@id": f"{SITE_BASE}/#org"},
        "inLanguage": "vi",
    }, {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Success Stories", "item": f"{SITE_BASE}/stories/"},
            {"@type": "ListItem", "position": 3, "name": title_vi, "item": canonical},
        ],
    }]
    out = patch_jsonld(out, extra)

    cos_html = ""
    for co in (s.get("companies") or [])[:5]:
        cos_html += f'<span class="story-card__co">{text(co)}</span>'

    name = s.get("name") or ""
    byline = f'<p class="muted">by {text(name)}</p>' if name else ""
    lede = f'<p class="article__lede">{text(lead_vi)}</p>' if lead_vi else ""

    snippet = (
        f'  <header class="story-detail__head">'
        f'    <div class="story-detail__chips">{cos_html}</div>'
        f'    <h1>{text(title_vi)}</h1>'
        f'    {byline}'
        f'  </header>'
        f'  <img class="story-detail__cover" src="{attr(cover)}" alt="{attr(title_vi)}" loading="lazy" />'
        f'  {lede}'
        f'  <p class="muted"><a href="{attr(BASE_PATH)}/stories/" data-href="#stories">← All stories</a></p>'
    )
    out = inject_into_mount(out, "storyArticle", snippet)
    out = show_route_style(out, "story")
    out = inject_boot_script(out)
    return out


def build_system_design_listing(template: str, title_vi: str, title_en: str,
                                description: str) -> str:
    chapters = [c for c in load_sd_chapters() if c.get("available")]
    canonical = f"{SITE_BASE}/{SYSTEM_DESIGN_URL_SLUG}/"
    title = f"{title_vi} · {SITE_NAME} — Luyện phỏng vấn Big Tech"
    og_image = SITE_BASE + ROUTE_OG_IMAGES.get(SYSTEM_DESIGN_URL_SLUG, OG_IMAGE)

    out = patch_head(
        template, title=title, description=description,
        canonical=canonical, og_image=og_image,
        og_title=f"{title_vi} · {SITE_NAME}",
        og_image_alt=f"{title_vi} — {SITE_NAME}",
    )

    item_list = {
        "@type": "ItemList",
        "@id": canonical + "#chapters",
        "name": f"{title_vi} — System Design case studies",
        "description": description,
        "numberOfItems": len(chapters),
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": c["n"],
                "name": c["title"],
                "url": f"{SITE_BASE}/{SYSTEM_DESIGN_URL_SLUG}/{c['slug']}/",
            }
            for c in chapters
        ],
    }
    extra = [
        {
            "@type": "CollectionPage",
            "@id": canonical,
            "url": canonical,
            "name": f"{title_vi} · {SITE_NAME}",
            "description": description,
            "isPartOf": {"@id": f"{SITE_BASE}/#website"},
            "inLanguage": "vi",
            "author": sd_author_schema(),
            "publisher": {"@id": f"{SITE_BASE}/#org"},
            "hasPart": {"@id": canonical + "#chapters"},
        },
        item_list,
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": title_vi, "item": canonical},
            ],
        },
    ]
    out = patch_jsonld(out, extra)

    links = ""
    for c in chapters:
        href = f"{attr(BASE_PATH)}/{SYSTEM_DESIGN_URL_SLUG}/{c['slug']}/"
        links += (
            f'    <a class="book-chapter" href="{href}" '
            f'data-href="#sd-chapter/{c["slug"]}">'
            f'<span class="book-chapter__n">{text(str(c["n"]))}</span>'
            f'<span class="book-chapter__title">{text(c["title"])}</span>'
            f"</a>\n"
        )
    snippet = (
        f'  <div class="book-group__items sd-prerender-chapters" aria-label="System Design chapters">\n'
        f"{links}"
        f"  </div>"
    )
    out = inject_into_mount(out, "sdChapters", snippet)
    out = show_route_style(out, "system-design")
    out = inject_boot_script(out)
    return out


def build_sd_chapter(template: str, ch: dict) -> str:
    title_vi = ch.get("title", "")
    title_en = ch.get("titleEn") or title_vi
    n = ch.get("n", "")
    slug = ch["slug"]

    title = f"{title_vi} · {SITE_NAME} — System Design"
    description = sd_chapter_description(ch)
    canonical = f"{SITE_BASE}/{SYSTEM_DESIGN_URL_SLUG}/{slug}/"
    intro = sd_chapter_intro_snippet(slug)

    og_image = SITE_BASE + OG_IMAGE
    out = patch_head(
        template, title=title, description=description,
        canonical=canonical, og_image=og_image, og_title=title_vi,
        og_type="article",
    )

    date_modified = content_last_mod(
        f"src/assets/content/system-design/vi/{slug}.html",
        f"src/assets/content/system-design/en/{slug}.html",
        "src/assets/system-design-data.js",
    )
    extra = [{
        "@type": "TechArticle",
        "@id": canonical + "#article",
        "headline": title_vi,
        "alternativeHeadline": title_en,
        "description": description,
        "url": canonical,
        "image": og_image,
        "datePublished": SD_V2_PUBLISHED,
        "dateModified": date_modified,
        "author": sd_author_schema(),
        "publisher": {"@id": f"{SITE_BASE}/#org"},
        "isPartOf": {"@id": f"{SITE_BASE}/{SYSTEM_DESIGN_URL_SLUG}/#chapters"},
        "inLanguage": ["vi", "en"],
    }, {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "System design material", "item": f"{SITE_BASE}/{SYSTEM_DESIGN_URL_SLUG}/"},
            {"@type": "ListItem", "position": 3, "name": title_vi, "item": canonical},
        ],
    }]
    out = patch_jsonld(out, extra)

    intro_html = f'<p class="article__lede">{text(intro)}</p>' if intro else ""
    snippet = (
        f'  <header class="article__head">'
        f'    <span class="badge">Ch. {text(str(n))}</span>'
        f'    <h1>{text(title_vi)}</h1>'
        f'    <p class="muted"><a href="{attr(BASE_PATH)}/{SYSTEM_DESIGN_URL_SLUG}/" data-href="#system-design">← System design material</a></p>'
        f'  </header>\n'
        f'  {intro_html}'
    )
    out = inject_into_mount(out, "sdChapterArticle", snippet)
    out = show_route_style(out, "sd-chapter")
    out = inject_boot_script(out)
    return out


# ---------- per-route descriptions for top routes ---------------------------

ROUTE_DESCRIPTIONS_VI = {
    "courses":   "11 khoá đào tạo chuyên sâu — DSA, System Design, Backend (Go/Java), Behavioural Interview, Machine Coding.",
    "book":          "Coding DSA Interview at Big Tech — 288 bài, 44 patterns, lời giải đầy đủ. Miễn phí cho cộng đồng.",
    SYSTEM_DESIGN_URL_SLUG: (
        "21 case study System Design Interview gốc — đọc từng chương (VI & EN). "
        "Nội dung gốc bởi EngineerPro."
    ),
    "mock":          "Mock Interview 1-1 với interviewer từ team EngineerPro — System Design, DSA, Behavioral theo style Big Tech (Google, Meta, TikTok, Amazon, Microsoft, Nvidia, WorldQuant, Axon…). Mock VI hoặc EN.",
    "resources": "Tài nguyên phỏng vấn miễn phí từ EngineerPro — checklist HR phone screen, video lập trình nền tảng, template CV Big Tech, playlist review CV.",
    "mentors":   "17 mentor đang làm việc tại Google, Amazon, Meta, TikTok, Spotify, Shopee, Acronis, AWS…",
    "stories":   "94+ học viên EngineerPro đã nhận offer tại Google, Meta, Amazon, TikTok, Microsoft, Grab, Shopee, NAB, ANZ…",
    "podcast":   "Podcast EngineerPro trên Substack & Spotify — tips sự nghiệp & phỏng vấn từ mentor Big Tech.",
    "partners":  "Đối tác EngineerPro — các tổ chức cùng sứ mệnh đưa kỹ sư Việt vươn ra Big Tech.",
    "faq":       "Câu hỏi thường gặp về khoá học, mentor, lịch học và thủ tục đăng ký tại EngineerPro.",
    "terms":     "Điều khoản dịch vụ EngineerPro — cam kết chất lượng, quyền sở hữu tài liệu, chính sách hoàn tiền và chuyển cọc.",
    "contact":   "Liên hệ EngineerPro qua email, Messenger, Facebook, Zalo, Spotify, YouTube, Substack, Viblo.",
}


SPA_FALLBACK_404 = """<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <title>EngineerPro — Page not found</title>
  <meta name="robots" content="noindex" />
  <meta http-equiv="refresh" content="0;url={base}/" />
  <script>
    // GitHub Pages serves /404.html for any unknown URL. Stash the originally-
    // requested path so the SPA can route there after we land on /.
    (function () {{
      try {{
        var p = location.pathname + location.search + location.hash;
        sessionStorage.setItem("ep_redirect", p);
      }} catch (e) {{}}
      location.replace("{base}/");
    }})();
  </script>
</head>
<body>
  <p>Page not found. <a href="{base}/">Back to home</a>.</p>
</body>
</html>
"""


# Standalone HTML for a legacy → new-URL redirect. GH Pages can't issue real
# HTTP 301s, so we approximate as closely as a static host can:
#   1. <link rel="canonical"> tells search engines the new URL is authoritative
#      → they will eventually de-index the legacy path and transfer ranking.
#   2. <meta name="robots" content="noindex"> on the legacy URL itself so it
#      doesn't compete with the canonical in SERP.
#   3. <meta http-equiv="refresh" content="0;…"> for visitors with JS disabled.
#   4. location.replace() for visitors with JS — instant, no extra history entry
#      (clicking Back doesn't bounce them back to the legacy URL).
#   5. Visible fallback <a> for accessibility / screen-reader users.
LEGACY_REDIRECT_HTML = """<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <title>Redirecting → {target_path} · EngineerPro</title>
  <meta name="robots" content="noindex,follow" />
  <link rel="canonical" href="{target_url}" />
  <meta http-equiv="refresh" content="0;url={target_url}" />
  <script>location.replace({target_url!r});</script>
</head>
<body>
  <p>This page has moved. If you are not redirected automatically,
     <a href="{target_url}">click here to continue to {target_path}</a>.</p>
</body>
</html>
"""


def main() -> int:
    with open(os.path.join(SRC, "index.html"), "r", encoding="utf-8") as f:
        template = f.read()
    template = fix_asset_paths(template)

    # 0. Home page — patch head + write to docs/index.html
    home = build_home(template)
    write(os.path.join(DOCS, "index.html"), home)
    pages = 1

    # 1. Top routes
    for slug, vi, en in TOP_ROUTES:
        desc = ROUTE_DESCRIPTIONS_VI[slug]
        if slug == SYSTEM_DESIGN_URL_SLUG:
            html_out = build_system_design_listing(template, vi, en, desc)
        else:
            html_out = build_top_route(template, slug, vi, en, desc)
        write(os.path.join(DOCS, slug, "index.html"), html_out)
        pages += 1

    # 2. Course details
    courses = load_data_array("courses-data.js", "COURSES")
    # COURSES_EN is JS object literal (unquoted keys, trailing commas), not JSON —
    # parse the entries we care about (slug → {title, blurb}) with regex.
    courses_en_map: dict[str, dict] = {}
    try:
        with open(os.path.join(SRC, "assets", "courses-i18n.js"), "r", encoding="utf-8") as f:
            txt = f.read()
        for m in re.finditer(
            r'"([^"]+)":\s*\{\s*title:\s*"([^"]*)",\s*blurb:\s*\n?\s*"([^"]*)"',
            txt, re.S,
        ):
            courses_en_map[m.group(1)] = {"title": m.group(2), "blurb": m.group(3)}
    except FileNotFoundError:
        pass
    for c in courses:
        en = courses_en_map.get(c["slug"], {})
        html_out = build_course_detail(template, c, en)
        write(os.path.join(DOCS, "courses", c["slug"], "index.html"), html_out)
        pages += 1

    # 3. Story details
    stories = load_data_array("stories-data.js", "STORIES")
    for s in stories:
        html_out = build_story_detail(template, s)
        write(os.path.join(DOCS, "stories", s["slug"], "index.html"), html_out)
        pages += 1

    # 3b. System Design chapter pages (available chapters only)
    for ch in load_sd_chapters():
        if not ch.get("available"):
            continue
        html_out = build_sd_chapter(template, ch)
        write(os.path.join(DOCS, SYSTEM_DESIGN_URL_SLUG, ch["slug"], "index.html"), html_out)
        pages += 1

    # 4. Home anchor shortcuts: /roadmap and /format land on the home page
    # and the SPA scrolls past the hero to the requested section via
    # parseHash() -> scrollTo. We prerender them as copies of home (so the
    # URL serves 200, never 404) with their own canonical so Google can
    # surface the deep link as a distinct landing page. No-JS visitors still
    # see the full home page; just the smooth-scroll is lost.
    home_html = build_home(template)
    for slug, _anchor_id in [("roadmap", "home-roadmap"), ("format", "home-format")]:
        page = home_html
        anchor_url = f"{SITE_BASE}/{slug}/"
        page = re.sub(
            r'<link rel="canonical" href="[^"]*"',
            f'<link rel="canonical" href="{anchor_url}"',
            page, count=1,
        )
        page = re.sub(
            r'<meta property="og:url" content="[^"]*"',
            f'<meta property="og:url" content="{anchor_url}"',
            page, count=1,
        )
        write(os.path.join(DOCS, slug, "index.html"), page)
        pages += 1

    # Deep-link sub-sections of /resources/. Same shape as the home anchor
    # aliases above: prerender a clone of /resources/index.html under each
    # sub-slug so the URL serves 200; the SPA's parseHash() + showRoute()
    # handle the scroll to the matching block on hydration.
    resources_html = build_top_route(
        template, "resources", "Interview Resources", "Interview Resources",
        ROUTE_DESCRIPTIONS_VI["resources"],
    )
    for slug, (title_prefix, desc) in RESOURCES_ALIASES.items():
        page = resources_html
        anchor_url = f"{SITE_BASE}/resources/{slug}/"
        title = f"{title_prefix}Interview Resources · {SITE_NAME}"
        page = re.sub(
            r'<title>[^<]*</title>',
            f'<title>{attr(title)}</title>',
            page, count=1,
        )
        page = re.sub(
            r'<link rel="canonical" href="[^"]*"',
            f'<link rel="canonical" href="{anchor_url}"',
            page, count=1,
        )
        page = re.sub(
            r'<meta property="og:url" content="[^"]*"',
            f'<meta property="og:url" content="{anchor_url}"',
            page, count=1,
        )
        page = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{attr(desc)}"',
            page, count=1,
        )
        write(os.path.join(DOCS, "resources", slug, "index.html"), page)
        pages += 1

    # 5. Legacy URL redirects. The old Shopify site used Vietnamese-slug paths
    # under /pages/ and /blogs/ which we want to keep linkable from external
    # backlinks (Substack, FB posts, etc.). For each entry below we emit a
    # standalone HTML file that does an immediate client-side redirect to the
    # new path, with rel="canonical" so Google transfers ranking to the new URL
    # over time (GH Pages can't issue real HTTP 301s).
    legacy_redirects = {
        "/pages/dieu-khoan-dich-vu":  "/terms/",
        "/system-design": f"/{SYSTEM_DESIGN_URL_SLUG}/",
        # Add more legacy paths here as we discover them:
        # "/blogs/faqs":              "/faq/",
        # "/pages/lien-he":           "/contact/",
    }
    for ch in load_sd_chapters():
        if ch.get("available"):
            legacy_redirects[f"/system-design/{ch['slug']}"] = (
                f"/{SYSTEM_DESIGN_URL_SLUG}/{ch['slug']}/"
            )
    for old_path, new_path in legacy_redirects.items():
        rel_dir = old_path.strip("/")
        target_url = f"{SITE_BASE}{new_path}"
        write(
            os.path.join(DOCS, rel_dir, "index.html"),
            LEGACY_REDIRECT_HTML.format(
                target_url=target_url,
                target_path=new_path,
                site_base=SITE_BASE,
            ),
        )
        pages += 1
    print(f"[prerender] wrote {len(legacy_redirects)} legacy redirect page(s)")

    # 6. SPA fallback for any URL not prerendered (typos, future slugs, etc.)
    write(os.path.join(DOCS, "404.html"), SPA_FALLBACK_404.format(base=SITE_BASE.rstrip("/")))
    pages += 1

    out_label = os.path.relpath(DOCS, ROOT)
    print(f"[prerender] wrote {pages} HTML pages under {out_label}/ (base={SITE_BASE})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
