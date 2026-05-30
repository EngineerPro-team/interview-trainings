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

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
DOCS = os.path.join(ROOT, "docs")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_config import BASE_URL, BASE_PATH, SITE_BASE, TOP_ROUTES, SITE_NAME, OG_IMAGE  # noqa: E402


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
    (
        re.compile(
            r'<link\s+rel="alternate"\s+hreflang="en"\s+href="[^"]*"\s*/?>',
        ),
        '<link rel="alternate" hreflang="en" href="{canonical}?lang=en" />',
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
    (
        re.compile(
            r'<meta\s+name="twitter:image"\s+content="[^"]*"\s*/?>',
        ),
        '<meta name="twitter:image" content="{og_image}" />',
    ),
]


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
            r'href="/(courses|book|resources|mentors|stories|podcast|partners|faq|contact)/"',
            rf'href="{BASE_PATH}/\1/"',
            out,
        )
    # 4. Embed BASE_PATH as a global before app.js loads
    base_path_inject = f'<script>window.EP_BASE_PATH = "{BASE_PATH}";</script>\n    '
    out = out.replace(
        f'<script src="{BASE_PATH}/assets/i18n.js">',
        base_path_inject + f'<script src="{BASE_PATH}/assets/i18n.js">',
    )
    return out


def patch_head(template: str, *, title: str, description: str, canonical: str,
               og_image: str, og_title: str | None = None) -> str:
    og_title = og_title or title
    ctx = {
        "title": attr(title),
        "description": attr(description),
        "canonical": attr(canonical),
        "og_image": attr(og_image),
        "og_title": attr(og_title),
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
PATH_BOOT_SCRIPT = (
    "\n    <!-- Prerendered route bootstrap: translate path to hash before app.js runs -->\n"
    "    <script>\n"
    "      (function () {\n"
    "        try {\n"
    "          var basePath = \"" + BASE_PATH + "\";\n"
    "          var p = location.pathname.replace(/\\/index\\.html$/, \"\").replace(/\\/+$/, \"\");\n"
    "          if (basePath && p.indexOf(basePath) === 0) p = p.slice(basePath.length);\n"
    "          if (p) {\n"
    "            var m;\n"
    "            if ((m = p.match(/^\\/courses\\/([^/]+)$/))) location.hash = \"#course/\" + m[1];\n"
    "            else if ((m = p.match(/^\\/stories\\/([^/]+)$/))) location.hash = \"#story/\" + m[1];\n"
    "            else if ((m = p.match(/^\\/(courses|book|resources|mentors|stories|podcast|partners|faq|contact)$/)))\n"
    "              location.hash = \"#\" + m[1];\n"
    "          }\n"
    "        } catch (e) {}\n"
    "      })();\n"
    "    </script>\n"
)


def inject_boot_script(template: str) -> str:
    # Put it right before the closing </head>
    return template.replace("</head>", PATH_BOOT_SCRIPT + "  </head>", 1)


# Pre-render a snippet inside the right <section data-route="X"> so crawlers
# see real text before JS runs. The SPA's renderer will then overwrite/augment.
SECTION_INJECT_RE_TMPL = (
    r'(<section[^>]*\bdata-route="{route}"[^>]*>)'
)


def inject_section_content(template: str, route: str, snippet_html: str) -> str:
    pat = re.compile(SECTION_INJECT_RE_TMPL.format(route=re.escape(route)))
    return pat.sub(
        lambda m: m.group(1) + "\n<!-- prerendered SEO content -->\n" + snippet_html,
        template,
        count=1,
    )


# Show the right route on first paint (the SPA hides every .route until JS
# matches one). For prerendered pages, also un-hide the static snippet.
SHOW_ROUTE_STYLE_TMPL = """
    <style>
      /* Prerender: show only the current route on first paint, no JS needed */
      .route[data-route="{route}"] { display: block !important; }
      .route[data-route="{route}"][hidden] { display: block !important; }
    </style>
"""

# ---------- per-route builders ----------------------------------------------

def build_top_route(template: str, slug: str, title_vi: str, title_en: str,
                    description: str, snippet_html: str = "") -> str:
    title = f"{title_vi} · {SITE_NAME} — Luyện phỏng vấn Big Tech"
    canonical = f"{SITE_BASE}/{slug}/"
    out = patch_head(template, title=title, description=description,
                     canonical=canonical,
                     og_image=SITE_BASE + OG_IMAGE,
                     og_title=f"{title_vi} · {SITE_NAME}")
    # ItemList schema for listing pages
    extra = [{
        "@type": "WebPage",
        "@id": canonical,
        "url": canonical,
        "name": f"{title_vi} · {SITE_NAME}",
        "description": description,
        "isPartOf": {"@id": f"{SITE_BASE}/#website"},
        "inLanguage": "vi",
    }]
    out = patch_jsonld(out, extra)
    if snippet_html:
        out = inject_section_content(out, slug, snippet_html)
    out = inject_boot_script(out)
    return out


def build_home(template: str) -> str:
    title = f"{SITE_NAME} — Chinh phục Big Tech cùng mentor thực chiến"
    description = (
        "100% mentors đến từ Big Tech — Google, Amazon, TikTok, Shopee, Spotify, "
        "Uber. Lộ trình rõ ràng để chinh phục offer Big Tech."
    )
    canonical = f"{SITE_BASE}/"
    return patch_head(template, title=title, description=description,
                      canonical=canonical, og_image=SITE_BASE + OG_IMAGE)


def build_course_detail(template: str, c: dict, en: dict) -> str:
    title_vi = c.get("title", "")
    title_en = (en.get("title") or title_vi)
    blurb_vi = c.get("blurb", "")
    blurb_en = (en.get("blurb") or blurb_vi)

    title = f"{title_vi} · {SITE_NAME} — Big Tech Interview Prep"
    description = truncate(blurb_vi, 160)
    canonical = f"{SITE_BASE}/courses/{c['slug']}/"
    cover = c.get("cover") or (SITE_BASE + OG_IMAGE)
    if cover.startswith("//"):
        cover = "https:" + cover

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

    snippet = (
        f'<article class="article" id="courseArticle">'
        f'  <header class="article__head">'
        f'    <h1>{text(title_vi)}</h1>'
        f'    <p class="article__lede">{text(blurb_vi)}</p>'
        f'    <p class="muted"><a href="{attr(BASE_PATH)}/courses/" data-href="#courses">← All courses</a></p>'
        f'  </header>'
        f'  <img class="article__cover" src="{attr(cover)}" alt="{attr(title_vi)}" loading="lazy" />'
        f'</article>'
    )
    out = inject_section_content(out, "course", snippet)
    out = inject_boot_script(out)
    return out


def build_story_detail(template: str, s: dict) -> str:
    title_vi = s.get("originalTitle") or s.get("title") or ""
    title_en = s.get("originalTitleEn") or s.get("titleEn") or title_vi
    lead_vi = re.sub(r"<[^>]+>", " ", s.get("lead", "")).strip()
    cover = s.get("cover") or (SITE_BASE + OG_IMAGE)
    if cover.startswith("assets/"):
        cover = f"{SITE_BASE}/{cover}"

    title = f"{title_vi} · {SITE_NAME}"
    description = truncate(lead_vi, 160) or f"Success story tại EngineerPro: {title_vi}"
    canonical = f"{SITE_BASE}/stories/{s['slug']}/"

    out = patch_head(template, title=title, description=description,
                     canonical=canonical, og_image=cover, og_title=title_vi)

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
        f'<article class="article story-detail" id="storyArticle">'
        f'  <header class="story-detail__head">'
        f'    <div class="story-detail__chips">{cos_html}</div>'
        f'    <h1>{text(title_vi)}</h1>'
        f'    {byline}'
        f'  </header>'
        f'  <img class="story-detail__cover" src="{attr(cover)}" alt="{attr(title_vi)}" loading="lazy" />'
        f'  {lede}'
        f'  <p class="muted"><a href="{attr(BASE_PATH)}/stories/" data-href="#stories">← All stories</a></p>'
        f'</article>'
    )
    out = inject_section_content(out, "story", snippet)
    out = inject_boot_script(out)
    return out


# ---------- per-route descriptions for top routes ---------------------------

ROUTE_DESCRIPTIONS_VI = {
    "courses":   "10 khoá đào tạo chuyên sâu — DSA, System Design, Backend (Go/Java), Behavioural Interview, Machine Coding.",
    "book":      "Coding DSA Interview at Big Tech — 288 bài, 44 patterns, lời giải đầy đủ. Miễn phí cho cộng đồng.",
    "resources": "Tài nguyên phỏng vấn miễn phí từ EngineerPro — video lập trình nền tảng, template CV Big Tech, playlist review CV.",
    "mentors":   "17 mentor đang làm việc tại Google, Amazon, Meta, TikTok, Spotify, Shopee, Acronis, AWS…",
    "stories":   "94+ học viên EngineerPro đã nhận offer tại Google, Meta, Amazon, TikTok, Microsoft, Grab, Shopee, NAB, ANZ…",
    "podcast":   "Podcast EngineerPro trên Substack & Spotify — tips sự nghiệp & phỏng vấn từ mentor Big Tech.",
    "partners":  "Đối tác EngineerPro — các tổ chức cùng sứ mệnh đưa kỹ sư Việt vươn ra Big Tech.",
    "faq":       "Câu hỏi thường gặp về khoá học, mentor, lịch học và thủ tục đăng ký tại EngineerPro.",
    "contact":   "Liên hệ EngineerPro qua Messenger, Facebook, Zalo, Spotify, YouTube, Substack, Viblo.",
}


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

    print(f"[prerender] wrote {pages} HTML pages under docs/ (base={BASE_URL})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
