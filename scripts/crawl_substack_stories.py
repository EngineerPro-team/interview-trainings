#!/usr/bin/env python3
"""
Crawl newsletter posts from the EngineerPro Substack and append them to the
Success Stories list (window.STORIES), de-duplicating against posts already
present (matched by the Substack /p/<slug>).

- Reads existing src/assets/stories-data.js
- Removes any slug in REMOVE_SLUGS
- Fetches https://engineerprovn.substack.com/api/v1/archive (newsletter posts)
- Skips posts already linked by an existing story (externalUrl/sourceUrl)
- Appends up to MAX_NEW new posts, tagged {"crawled": true}

Re-run:  python3 scripts/crawl_substack_stories.py
"""
from __future__ import annotations

import html as html_lib
import json
import re
import sys
import urllib.request
from pathlib import Path

# Reuse company normalization + tiering from the sheet parser.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_stories as ps  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "assets" / "stories-data.js"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15"
API = "https://engineerprovn.substack.com/api/v1/archive?sort=new&offset={offset}&limit={limit}"

MAX_NEW = 20
REMOVE_SLUGS = {"anh-tiep-axon"}

# Skip obvious non-story posts (course ads, schedule announcements, podcasts…)
SKIP_TITLE_KW = (
    "khai giảng", "tuyển sinh", "khoá học mới", "khóa học mới",
    "coffee with lam", "podcast", "thông báo", "ưu đãi", "giảm giá",
    "webinar", "recap sự kiện",
)


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())


def fetch_all() -> list[dict]:
    out: list[dict] = []
    limit, offset = 20, 0
    while True:
        chunk = fetch_json(API.format(offset=offset, limit=limit))
        if not chunk:
            break
        out.extend(chunk)
        if len(chunk) < limit:
            break
        offset += limit
        if offset >= 400:
            break
    return out


def strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html_lib.unescape(s)).strip()


def substack_post_slug(url: str) -> str | None:
    """Return the <slug> from a https://…substack.com/p/<slug> URL, else None."""
    if not url or "substack" not in url:
        return None
    m = re.search(r"/p/([\w-]+)", url)
    return m.group(1) if m else None


# Brand / proper-noun tokens to restore after sentence-casing an all-caps title.
EXTRA_BRANDS = [
    "EngineerPro", "Engineer Pro", "Big Tech", "New Grad", "Mid-level",
    "Zalo", "Tymex", "Silicon", "Part 2", "Part 3", "Part 1", "OA",
]
_BRAND_TOKENS = sorted(
    set(ps.KNOWN_COMPANIES) | set(EXTRA_BRANDS), key=len, reverse=True
)


def prettify_title(t: str) -> str:
    """Substack titles are often ALL CAPS. Convert to sentence case and restore
    known brand tokens (Grab, Amazon, EngineerPro, ANZ…) to proper casing."""
    t = t.strip()
    letters = [c for c in t if c.isalpha()]
    if letters and all(c.isupper() for c in letters):
        # sentence case: first alpha upper, rest lower
        t = t.lower()
        t = re.sub(r"([a-zàáâãèéêìíòóôõùúýăđĩũơư])", lambda m: m.group(1).upper(), t, count=1)
    for brand in _BRAND_TOKENS:
        t = re.sub(rf"\b{re.escape(brand)}\b", brand, t, flags=re.IGNORECASE)
    return t


def infer_companies(title: str) -> tuple[list[str], int]:
    low = title.lower()
    companies: list[str] = []
    tier = ps.DEFAULT_TIER
    for kw, label in ps.ALIAS.items():
        if re.search(rf"\b{re.escape(kw)}\b", low):
            if label not in companies:
                companies.append(label)
                tier = min(tier, ps.TIER_MAP.get(kw, ps.DEFAULT_TIER))
    return companies, tier


def load_existing() -> list[dict]:
    if not OUT.exists():
        return []
    raw = OUT.read_text(encoding="utf-8")
    m = re.search(r"window\.STORIES\s*=\s*(\[.*\]);", raw, re.S)
    return json.loads(m.group(1)) if m else []


def build_story(post: dict, stt: int) -> dict:
    title = prettify_title((post.get("title") or "").strip())
    subtitle = strip_html(post.get("subtitle") or post.get("description") or "")
    if not subtitle:
        subtitle = "Câu chuyện thực chiến từ cộng đồng EngineerPro — hành trình ôn luyện và phỏng vấn."
    url = post.get("canonical_url") or ""
    cover = post.get("cover_image") or ""
    date = (post.get("post_date") or "")[:10]
    premium = (post.get("audience") or "everyone") != "everyone"
    anonymous = "ẩn danh" in title.lower()
    companies, tier = infer_companies(title)

    base_slug = post.get("slug") or ps.slugify(title)
    body_vi = (
        f"<p class=\"story__lead\">{html_lib.escape(subtitle)}</p>"
        f"<p>Đây là bài chia sẻ được đăng trên Substack của EngineerPro. "
        f"Bấm nút bên dưới để đọc toàn bộ bài viết gốc.</p>"
    )
    body_en = (
        f"<p class=\"story__lead\">{html_lib.escape(subtitle)}</p>"
        f"<p>This piece was published on the EngineerPro Substack. "
        f"Use the button below to read the full original post.</p>"
    )
    return {
        "stt": stt,
        "name": "",
        "rawHeading": title,
        "isArticle": False,
        "companies": companies,
        "tier": tier,
        "anonymous": anonymous,
        "noPhoto": False,
        "premium": premium,
        "slug": base_slug,
        "title": title,
        "titleEn": title,
        "originalTitle": title,
        "lead": subtitle,
        "leadEn": subtitle,
        "body": body_vi,
        "bodyEn": body_en,
        "externalUrl": url,
        "sourceUrl": url,
        "matchedSubstackUrl": url,
        "cover": cover,
        "date": date,
        "crawled": True,
    }


def main() -> int:
    existing = load_existing()
    before = len(existing)
    existing = [s for s in existing if s.get("slug") not in REMOVE_SLUGS]
    removed = before - len(existing)
    print(f"→ loaded {before} stories; removed {removed} ({', '.join(REMOVE_SLUGS)})")

    # Build dedupe sets: existing site slugs + existing Substack post slugs.
    used_slugs = {s.get("slug") for s in existing}
    seen_posts: set[str] = set()
    for s in existing:
        for u in (s.get("externalUrl"), s.get("sourceUrl"), s.get("matchedSubstackUrl")):
            ps_slug = substack_post_slug(u or "")
            if ps_slug:
                seen_posts.add(ps_slug)

    print("→ fetching Substack archive …")
    posts = fetch_all()
    posts = [p for p in posts if (p.get("type") or "newsletter") == "newsletter"]
    print(f"  {len(posts)} newsletter posts fetched")

    max_stt = max((s.get("stt") or 0) for s in existing) if existing else 0
    added: list[dict] = []
    for p in posts:
        if len(added) >= MAX_NEW:
            break
        title = (p.get("title") or "").strip()
        if not title:
            continue
        if any(kw in title.lower() for kw in SKIP_TITLE_KW):
            continue
        pslug = p.get("slug") or substack_post_slug(p.get("canonical_url") or "")
        if pslug and pslug in seen_posts:
            continue  # duplicate of an existing story
        # unique site slug
        slug = pslug or ps.slugify(title)
        base = slug
        i = 2
        while slug in used_slugs:
            slug = f"{base}-{i}"
            i += 1
        used_slugs.add(slug)
        if pslug:
            seen_posts.add(pslug)
        max_stt += 1
        rec = build_story(p, max_stt)
        rec["slug"] = slug
        added.append(rec)

    print(f"  → adding {len(added)} new stories (skipped duplicates + non-stories)")
    for a in added:
        print(f"     + [{a['date']}] {a['title'][:70]}  #{a['slug']}")

    merged = added + existing  # newest crawled first
    payload = json.dumps(merged, ensure_ascii=False, indent=2)
    OUT.write_text(
        "// AUTO-GENERATED by scripts/parse_stories.py — do not edit by hand.\n"
        "// Source: Google Sheet [PHỎNG VẤN] Tổng hợp bài PV - EP (uploaded as edit-0.md).\n"
        "// Stories carrying a `manualEdits: [...]` array have those listed\n"
        "// fields preserved across re-runs (see merge logic in main()).\n"
        "// Stories with `crawled: true` were pulled from the Substack archive\n"
        "// by scripts/crawl_substack_stories.py and are preserved across sheet re-runs.\n"
        f"window.STORIES = {payload};\n",
        encoding="utf-8",
    )
    print(f"\n✓ wrote {len(merged)} stories → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
