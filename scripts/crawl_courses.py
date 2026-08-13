#!/usr/bin/env python3
"""
Crawl every course detail page from engineerprogurus.com and emit a JS data file
that the static site embeds at build time.

Output: src/assets/courses-data.js
        window.COURSES = [ { slug, url, title, cover, blurb, html }, ... ]

Re-run any time you want to refresh the cache:
    python3 scripts/crawl_courses.py

Re-apply only the hand-curated blocks from data/course_extra_blocks.json, with
no network calls and no loss of the existing htmlEn translations:
    python3 scripts/crawl_courses.py --extras-only
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

BASE = "https://engineerprogurus.com"
LIST_URL = BASE + "/blogs/khoa-hoc"
PAGES = 4
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.5 Safari/605.1.15"
)
OUT = Path(__file__).resolve().parent.parent / "src" / "assets" / "courses-data.js"

# Slugs to skip — courses we don't want to surface on the rebuild site.
# Edit this set instead of post-processing the generated data file.
EXCLUDED_SLUGS = {
    "premium-course-lc-4-5-dsa-intensive-training-tai-engineer-pro",
    "khoa-tieng-anh-giao-tiep-danh-rieng-cho-software-engineer",
    "introduction-to-programming-with-python-java",
    "oop-database-design",
    "khoa-hoc-front-end",
}

# ----- attributes / tags we strip from every node --------------------------------
DROP_ATTRS = {
    "style",
    "class",
    "id",
    "data-mce-style",
    "data-mce-fragment",
    "data-mce-href",
    "data-mce-src",
    "data-mce-selected",
    "color",
    "size",
    "width",
    "height",
    "align",
    "valign",
    "bgcolor",
    "cellpadding",
    "cellspacing",
    "border",
    "face",
    "font",
}
KEEP_ATTRS = {
    "href",
    "src",
    "alt",
    "title",
    "target",
    "rel",
    "loading",
    "type",
    "frameborder",
    "allow",
    "allowfullscreen",
}
DROP_TAGS = {"script", "style", "noscript", "ins", "meta", "link"}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


# ===================================================================
#  HTML cleaning helpers
# ===================================================================
def clean_attrs(node: Tag) -> None:
    for attr in list(node.attrs.keys()):
        if attr in DROP_ATTRS:
            del node.attrs[attr]
        elif attr not in KEEP_ATTRS:
            del node.attrs[attr]


def unwrap_inline_wrappers(node: Tag) -> None:
    """Recursively unwrap <span>/<font>/<u> that have no meaningful semantics —
    these come from Google Docs / TinyMCE paste output and just nest endlessly."""
    # bottom-up to keep traversal stable
    for tag_name in ("font", "u"):
        for n in list(node.find_all(tag_name)):
            n.unwrap()
    # spans: unwrap everything (we lose color/size, which we don't want anyway)
    for n in list(node.find_all("span")):
        n.unwrap()


def normalise_whitespace(html_text: str) -> str:
    # collapse runs of whitespace inside text nodes; preserve <pre>/<code> as-is
    return re.sub(r"[ \t]{2,}", " ", html_text)


def absolutise_img_srcs(node: Tag) -> None:
    for img in node.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        if src.startswith("//"):
            src = "https:" + src
        elif src.startswith("/"):
            src = BASE + src
        if src:
            img["src"] = src
        img.attrs["loading"] = "lazy"
        clean_attrs(img)


def harden_links(node: Tag) -> None:
    for a in node.find_all("a"):
        href = a.get("href") or ""
        if href.startswith("/"):
            a["href"] = BASE + href
        if a.get("href", "").startswith("http"):
            a["target"] = "_blank"
            a["rel"] = "noopener"


def strip_junk(node: Tag) -> None:
    bad_selectors = [
        "script",
        "style",
        "noscript",
        "iframe[src*='facebook.com/plugins']",
        ".fb-comments",
        ".addthis_inline_share_toolbox",
        ".social-share",
    ]
    for sel in bad_selectors:
        for n in node.select(sel):
            n.decompose()
    for t in DROP_TAGS:
        for n in node.find_all(t):
            n.decompose()
    for c in node.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()


def drop_empty_blocks(node: Tag) -> None:
    """Remove <p>, <div>, <ul>, <li> that hold only whitespace and no images/iframes."""
    changed = True
    while changed:
        changed = False
        for tag_name in ("p", "div", "li", "ul", "ol", "h1", "h2", "h3", "h4"):
            for n in list(node.find_all(tag_name)):
                if n.find(["img", "iframe", "video", "table"]):
                    continue
                if not n.get_text(strip=True):
                    n.decompose()
                    changed = True


# Patterns that mark the start of the boilerplate trailer found at the bottom
# of every course page (contact info, generic "about EngineerPro" pitch).
# Triggers must be specific enough that they only appear in the footer block,
# not in regular body text.
TRAILER_TRIGGERS = (
    "thông tin liên hệ",                  # always a footer heading
    "thong tin lien he",
    "engineer pro là một trung tâm đào tạo",
    "engineerpro là một trung tâm đào tạo",
    "✅website",
    "✅fanpage",
    "✅email",
)


def trim_trailer(node: Tag) -> None:
    """Drop the trailing boilerplate (contact + generic about block + tag links).
    Safety: only trim if the original body has at least 5 children, so we don't
    accidentally wipe a short page that happens to mention a trigger early on."""
    children = list(node.children)
    tag_children = [c for c in children if isinstance(c, Tag)]
    if len(tag_children) < 5:
        return
    cut_idx = None
    for i, c in enumerate(children):
        if not isinstance(c, Tag):
            continue
        text = c.get_text(" ", strip=True).lower()
        if not text:
            continue
        if any(t in text for t in TRAILER_TRIGGERS):
            cut_idx = i
            break
    if cut_idx is not None:
        for c in children[cut_idx:]:
            if isinstance(c, Tag):
                c.decompose()
            else:
                c.extract()
    # Strip standalone separator lines that the editor leaves behind.
    for n in list(node.find_all(["p", "div"])):
        txt = n.get_text(strip=True)
        if txt and set(txt) <= {"_", "-", "—", "─", "*", " ", "·"} and len(txt) >= 6:
            n.decompose()


def scrub_external_refs(node: Tag) -> None:
    """Remove anchors pointing to the old engineerprogurus site and tagged blog
    listings; replace inline 'engineerprogurus.com' text with plain wording."""
    for a in list(node.find_all("a")):
        href = (a.get("href") or "").lower()
        if "engineerprogurus.com" in href:
            # If the link is the entire paragraph content, drop the paragraph.
            parent = a.parent
            a.unwrap()
            if parent and parent.name in ("p", "div", "li") and not parent.get_text(strip=True):
                parent.decompose()
    # Replace any remaining bare text mentions of the old domain.
    for txt in list(node.find_all(string=True)):
        if isinstance(txt, Comment):
            continue
        s = str(txt)
        if "engineerprogurus" in s.lower():
            new = re.sub(r"https?://(www\.)?engineerprogurus\.com/?\S*", "", s, flags=re.IGNORECASE)
            new = re.sub(r"engineerprogurus\.com\S*", "", new, flags=re.IGNORECASE)
            txt.replace_with(new)


def youtube_responsive(node: Tag, soup: BeautifulSoup) -> None:
    """Wrap raw <iframe> in a responsive container for nicer rendering."""
    for iframe in node.find_all("iframe"):
        clean_attrs(iframe)
        if iframe.parent and iframe.parent.name == "div" and iframe.parent.get("class"):
            continue
        wrapper = soup.new_tag("div", attrs={"class": "embed-16x9"})
        iframe.insert_before(wrapper)
        wrapper.append(iframe.extract())


# ===================================================================
#  Listing-page discovery
# ===================================================================
def discover_courses() -> list[dict]:
    """Return list of {slug, url, title, cover} dicts, de-duplicated, in page order."""
    seen: dict[str, dict] = {}
    for p in range(1, PAGES + 1):
        url = f"{LIST_URL}?page={p}"
        html = fetch(url)
        soup = BeautifulSoup(html, "html.parser")

        # Pass 1: pick a cover image for each slug by scanning every <a><img></a>
        # where the anchor href targets a course slug.
        slug_to_cover: dict[str, str] = {}
        for a in soup.find_all("a"):
            href = a.get("href") or ""
            if not href.startswith("/blogs/khoa-hoc/"):
                continue
            slug = href.rstrip("/").split("/")[-1]
            if not slug or "?" in slug or slug == "khoa-hoc":
                continue
            img = a.find("img")
            if not img:
                continue
            src = img.get("src") or img.get("data-src") or ""
            if not src:
                continue
            if src.startswith("//"):
                src = "https:" + src
            elif src.startswith("/"):
                src = BASE + src
            # prefer the first match (usually the largest hero), don't overwrite
            slug_to_cover.setdefault(slug, src)

        # Pass 2: pick the title from <h2 a> or <h4 a>
        for h in soup.select("h1 a, h2 a, h3 a, h4 a"):
            href = h.get("href") or ""
            if not href.startswith("/blogs/khoa-hoc/"):
                continue
            slug = href.rstrip("/").split("/")[-1]
            if not slug or "?" in slug or slug == "khoa-hoc" or slug in seen:
                continue
            if slug in EXCLUDED_SLUGS:
                continue
            seen[slug] = {
                "slug": slug,
                "url": urljoin(BASE, href),
                "title": h.get_text(" ", strip=True),
                "cover": slug_to_cover.get(slug, ""),
            }
    return list(seen.values())


# ===================================================================
#  Detail-page extraction
# ===================================================================
def first_paragraph(node: Tag, max_chars: int = 240) -> str:
    text = " ".join(t.strip() for t in node.stripped_strings)
    text = re.sub(r"\s+", " ", text)
    if len(text) > max_chars:
        text = text[: max_chars - 1].rsplit(" ", 1)[0] + "…"
    return text


def extract_article(html: str, fallback_title: str, fallback_cover: str) -> tuple[str, str, str, str]:
    """Return (title, blurb, cover, cleaned_html_inner)."""
    soup = BeautifulSoup(html, "html.parser")

    title_node = soup.select_one(".article-title, h1.post-title, h1")
    title = title_node.get_text(" ", strip=True) if title_node else fallback_title

    body = soup.select_one(".entry-content.notopmargin") or soup.select_one(".entry-content")
    if not body:
        return title, "", fallback_cover, ""

    strip_junk(body)
    unwrap_inline_wrappers(body)
    for n in body.find_all(True):
        clean_attrs(n)
    absolutise_img_srcs(body)
    harden_links(body)
    youtube_responsive(body, soup)
    trim_trailer(body)
    scrub_external_refs(body)
    drop_empty_blocks(body)

    blurb = first_paragraph(body)

    # Cover: prefer the listing-page thumbnail; if missing, fall back to first img in body
    cover = fallback_cover
    if not cover:
        first_img = body.find("img")
        if first_img and first_img.get("src"):
            cover = first_img["src"]

    # Return inner HTML (without the wrapping div) so the site can wrap it in its own container.
    inner = "".join(str(c) for c in body.children)
    inner = normalise_whitespace(inner)
    return title, blurb, cover, inner


# ===================================================================
#  Extra hand-curated courses (not present on engineerprogurus.com)
# ===================================================================
EXTRA_COURSES_FILE = Path(__file__).resolve().parent / "data" / "extra_courses.json"


def load_extra_courses() -> list[dict]:
    """Read hand-curated course entries (e.g. the rotating Crash Course) and
    merge them into the crawl output so they survive every re-crawl."""
    if not EXTRA_COURSES_FILE.exists():
        return []
    try:
        extras = json.loads(EXTRA_COURSES_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ! failed to load {EXTRA_COURSES_FILE}: {e}")
        return []
    print(f"  + merging {len(extras)} hand-curated course(s) from {EXTRA_COURSES_FILE.name}")
    return extras


# ===================================================================
#  Extra hand-curated blocks injected into an upstream course body
# ===================================================================
# Upstream (engineerprogurus.com) is the source of truth for course bodies, so
# anything we add by hand would be wiped on the next crawl. Blocks declared in
# this file are re-injected after every crawl instead.
EXTRA_BLOCKS_FILE = Path(__file__).resolve().parent / "data" / "course_extra_blocks.json"


def load_extra_blocks() -> list[dict]:
    if not EXTRA_BLOCKS_FILE.exists():
        return []
    try:
        return json.loads(EXTRA_BLOCKS_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ! failed to load {EXTRA_BLOCKS_FILE.name}: {e}")
        return []


def _wrap_block(block_id: str, body_html: str) -> str:
    return f'<div class="course-extra" data-extra="{block_id}">{body_html}</div>'


def _replace_block(body: str, block_id: str, wrapped: str) -> str | None:
    """Swap an already-present block for the current curated version.

    Returns None when the block isn't there yet, and the untouched body when it
    is already up to date — that keeps us from re-serialising (and subtly
    reformatting) bodies that need no change.
    """
    if f'data-extra="{block_id}"' not in body:
        return None
    soup = BeautifulSoup(body, "html.parser")
    node = soup.find(attrs={"data-extra": block_id})
    if node is None:
        return None
    replacement = BeautifulSoup(wrapped, "html.parser").find(attrs={"data-extra": block_id})
    # Compare both sides after a parse round-trip; a raw-string compare would
    # always differ on attribute normalisation (allowfullscreen -> ="").
    if str(node) == str(replacement):
        return body
    node.replace_with(replacement)
    return str(soup)


def inject_extra_blocks(courses: list[dict]) -> None:
    """Splice hand-curated HTML into the crawled course bodies, in place.

    Safe to run repeatedly: a block already in the body is updated rather than
    duplicated. That also repairs the `htmlEn` case where a re-crawl dropped the
    translations and `translate_courses.py` machine-translated our curated
    English copy back out of the Vietnamese body.

    Blocks land before their per-language `insertBefore` anchor. If upstream ever
    rewrites that anchor away we append instead, so the content is never lost.
    """
    blocks = load_extra_blocks()
    if not blocks:
        return
    by_slug = {c["slug"]: c for c in courses}
    for block in blocks:
        course = by_slug.get(block["slug"])
        if course is None:
            print(f"  ! extra block target missing: {block['slug']}")
            continue
        for lang, field in (("vi", "html"), ("en", "htmlEn")):
            body, addition = course.get(field), block.get(lang)
            if not body or not addition:
                continue
            wrapped = _wrap_block(block["id"], addition)
            replaced = _replace_block(body, block["id"], wrapped)
            if replaced is not None:
                if replaced == body:
                    continue
                course[field] = replaced
                where = "refreshed in place"
            else:
                anchor = (block.get("insertBefore") or {}).get(lang)
                if anchor and anchor in body:
                    course[field] = body.replace(anchor, wrapped + anchor, 1)
                    where = "inserted before anchor"
                else:
                    course[field] = body + wrapped
                    where = "appended (anchor not found)"
            print(f"  + {block['slug']} [{field}]: {block['id']} {where}")


# ===================================================================
#  Main
# ===================================================================
def load_existing() -> list[dict]:
    """Parse the courses already on disk, so --extras-only can patch them
    without a full re-crawl (which would drop every htmlEn translation)."""
    raw = OUT.read_text(encoding="utf-8")
    m = re.search(r"window\.COURSES\s*=\s*(\[.*\]);", raw, re.S)
    if not m:
        raise SystemExit(f"! could not parse {OUT.name}")
    return json.loads(m.group(1))


def write_out(results: list[dict]) -> int:
    # Normalise legacy brand naming — the upstream blog uses the long form
    # "EngineerPro / EngineerPro Academy" in many course bodies. We only
    # operate under "EngineerPro" now.
    def _strip_academy(s: str) -> str:
        s = re.sub(r'EngineerPro\s*/\s*EngineerPro Academy', 'EngineerPro', s)
        s = re.sub(r'EngineerPro và EngineerPro Academy', 'EngineerPro', s)
        return s.replace(' tại EngineerPro Academy', ' tại EngineerPro') \
                .replace(' at EngineerPro Academy', ' at EngineerPro') \
                .replace('EngineerPro Academy', 'EngineerPro')

    for c in results:
        for k in ("title", "blurb", "html", "htmlEn"):
            if isinstance(c.get(k), str):
                c[k] = _strip_academy(c[k])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(results, ensure_ascii=False, indent=2)
    OUT.write_text(
        "// AUTO-GENERATED by scripts/crawl_courses.py — do not edit by hand.\n"
        "// Source: engineerprogurus.com/blogs/khoa-hoc (pages 1-4)\n"
        f"window.COURSES = {payload};\n",
        encoding="utf-8",
    )
    rel = OUT.relative_to(OUT.parent.parent.parent)
    print(f"✓ wrote {len(results)} courses → {rel}")
    return 0


def main() -> int:
    if "--extras-only" in sys.argv:
        print(f"→ re-injecting extra blocks into {OUT.name} (no crawl) …")
        results = load_existing()
        inject_extra_blocks(results)
        return write_out(results)

    print(f"→ discovering slugs across {PAGES} listing pages …")
    courses = discover_courses()
    print(f"  found {len(courses)} unique courses")

    results = []
    for i, c in enumerate(courses, 1):
        print(f"  [{i:>2}/{len(courses)}] {c['slug']}")
        try:
            html = fetch(c["url"])
        except Exception as e:
            print(f"     ! fetch failed: {e}")
            continue
        title, blurb, cover, body = extract_article(html, c["title"], c["cover"])
        if not body:
            print("     ! no body extracted, skipping")
            continue
        results.append(
            {
                "slug": c["slug"],
                "url": c["url"],
                "title": title.strip(),
                "cover": cover,
                "blurb": blurb,
                "html": body,
            }
        )
        time.sleep(0.2)

    results.extend(load_extra_courses())
    inject_extra_blocks(results)

    return write_out(results)


if __name__ == "__main__":
    sys.exit(main())
