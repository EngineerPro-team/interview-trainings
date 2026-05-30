#!/usr/bin/env python3
"""
Crawl every course detail page from engineerprogurus.com and emit a JS data file
that the static site embeds at build time.

Output: src/assets/courses-data.js
        window.COURSES = [ { slug, url, title, cover, blurb, html }, ... ]

Re-run any time you want to refresh the cache:
    python3 scripts/crawl_courses.py
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
#  Main
# ===================================================================
def main() -> int:
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


if __name__ == "__main__":
    sys.exit(main())
