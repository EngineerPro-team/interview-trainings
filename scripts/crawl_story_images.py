#!/usr/bin/env python3
"""
For each story in src/assets/stories-data.js, attach a cover image:
  1) Try to match a Substack post (by company + recency) and download its cover.
  2) If no match, generate a 1200×630 placeholder PNG with the story title +
     company chips on a navy/orange gradient.

Result: each story record gains a `cover` field (path under assets/img/stories/).
Updates src/assets/stories-data.js in-place.
"""
from __future__ import annotations

import json
import re
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
STORIES_JS = ROOT / "src" / "assets" / "stories-data.js"
IMG_DIR = ROOT / "src" / "assets" / "img" / "stories"
IMG_DIR.mkdir(parents=True, exist_ok=True)

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.5 Safari/605.1.15"
)
SUBSTACK_API = "https://engineerprovn.substack.com/api/v1/archive?sort=new&offset={o}&limit=12"
CACHE = Path("/tmp/ep_substack_archive.json")

NAVY = (11, 29, 58)
NAVY_2 = (16, 40, 73)
ORANGE = (255, 122, 24)
WHITE = (255, 255, 255)
MUTED = (200, 210, 220)
ORANGE_LIGHT = (255, 176, 102)


# ----- title normalisation for matching -----
def deaccent(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


CACHE_TTL_SECONDS = 24 * 3600  # 1 day

def fetch_substack_posts() -> list[dict]:
    """Return all Substack posts, with a 24h disk cache. Pass --refresh to force."""
    refresh = "--refresh" in sys.argv
    if CACHE.exists() and not refresh:
        age = time.time() - CACHE.stat().st_mtime
        if age < CACHE_TTL_SECONDS:
            try:
                return json.loads(CACHE.read_text())
            except Exception:
                pass
        else:
            print(f"→ Substack cache is {age/3600:.1f}h old (TTL {CACHE_TTL_SECONDS/3600:.0f}h) — refreshing")
    print("→ fetching all Substack posts (with covers) …")
    all_posts: list[dict] = []
    for offset in range(0, 600, 12):
        url = SUBSTACK_API.format(o=offset)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            chunk = json.loads(r.read())
        if not chunk:
            break
        all_posts.extend(chunk)
        if len(chunk) < 12:
            break
    CACHE.write_text(json.dumps(all_posts, ensure_ascii=False))
    print(f"  → cached {len(all_posts)} posts to {CACHE}")
    return all_posts


def best_match(story: dict, posts: list[dict]) -> dict | None:
    """Return the post that best matches a story, or None."""
    if not story.get("companies"):
        return None
    # Score by: #companies appearing in title (deaccented) + post recency (lower offset = better)
    cos_norm = [deaccent(c) for c in story["companies"]]
    # Also match story name if it's distinctive enough (>=2 chars and not a common Vietnamese word)
    name_norm = deaccent(story.get("name") or "")
    name_norm = re.sub(r"^(anh|chi|ban|em|co)\s+", "", name_norm)

    scored = []
    for p in posts:
        title = deaccent(p.get("title", ""))
        if not title:
            continue
        score = 0
        for c in cos_norm:
            # Require at least 3 chars match to avoid trivial substring noise
            if len(c) >= 3 and c in title:
                score += 10
        if name_norm and len(name_norm) >= 3 and name_norm in title:
            score += 5
        if score > 0:
            scored.append((score, p))
    if not scored:
        return None
    # Higher score wins; on tie, prefer newer post (post_date descending).
    scored.sort(key=lambda x: (-x[0], -_post_date_key(x[1])))
    return scored[0][1]


def _post_date_key(p: dict) -> float:
    """Best-effort numeric key from Substack post_date (ISO 8601 string)."""
    s = p.get("post_date") or ""
    if not s:
        return 0
    try:
        from datetime import datetime
        # Substack returns e.g. "2024-08-12T10:23:45.000Z"
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0


def download_image(url: str, out_path: Path) -> bool:
    """Download + compress to WebP, max width 1200px, quality 82."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        if len(data) < 1000:
            return False
        tmp = out_path.with_suffix(".raw")
        tmp.write_bytes(data)
        img = Image.open(tmp).convert("RGB")
        if img.width > 1200:
            ratio = 1200 / img.width
            img = img.resize((1200, int(img.height * ratio)), Image.LANCZOS)
        img.save(out_path, "WEBP", quality=82, method=6)
        tmp.unlink(missing_ok=True)
        return True
    except Exception as e:
        print(f"     ! download failed: {e}")
        return False


# ----- placeholder cover generator -----
def font(size: int, bold: bool = False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def make_placeholder(story: dict, out_path: Path) -> None:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), NAVY)
    # vertical gradient
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(NAVY[0] + (NAVY_2[0] - NAVY[0]) * t)
        g = int(NAVY[1] + (NAVY_2[1] - NAVY[1]) * t)
        b = int(NAVY[2] + (NAVY_2[2] - NAVY[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)

    # orange glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, a in [(420, 22), (320, 36), (220, 50), (140, 80)]:
        gd.ellipse((W - 200 - r, -200 - r // 3, W - 200 + r, -200 + r), fill=(*ORANGE, a))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    img.paste(glow, (0, 0), glow)

    d = ImageDraw.Draw(img)
    PADDING = 70

    # Brand strip top
    d.text((PADDING, PADDING - 10), "EngineerPro · Success Story", font=font(20), fill=ORANGE_LIGHT)

    # Person name + companies
    name = (story.get("name") or "Học viên EngineerPro").strip()
    cos = story.get("companies") or []
    fnm = font(36, bold=True)
    d.text((PADDING, PADDING + 30), name, font=fnm, fill=WHITE)

    if cos:
        # company chips horizontally
        chip_y = PADDING + 90
        fchip = font(20, bold=True)
        cx = PADDING
        for c in cos[:3]:
            tw = d.textbbox((0, 0), c, font=fchip)
            cw = (tw[2] - tw[0]) + 30
            d.rounded_rectangle((cx, chip_y, cx + cw, chip_y + 40), radius=20, fill=(*ORANGE, 240))
            d.text((cx + 15, chip_y + 8), c, font=fchip, fill=WHITE)
            cx += cw + 12

    # Title — wrap manually to fit width
    title = story.get("title") or name
    ftitle = font(58, bold=True)
    max_w = W - PADDING * 2
    words = title.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        candidate = (cur + " " + w).strip()
        if d.textbbox((0, 0), candidate, font=ftitle)[2] > max_w and cur:
            lines.append(cur)
            cur = w
        else:
            cur = candidate
    if cur:
        lines.append(cur)
    lines = lines[:4]

    y0 = 280
    for line in lines:
        d.text((PADDING, y0), line, font=ftitle, fill=WHITE)
        y0 += 72

    # bottom CTA
    fcta = font(22, bold=True)
    d.text((PADDING, H - 75), "engineerprogurus.com  ·  Đọc bài đầy đủ →", font=fcta, fill=ORANGE_LIGHT)

    img.save(out_path, "WEBP", quality=82, method=6)


# ----- main -----
def update_stories_file(stories: list[dict]) -> None:
    payload = json.dumps(stories, ensure_ascii=False, indent=2)
    STORIES_JS.write_text(
        "// AUTO-GENERATED by scripts/parse_stories.py + crawl_story_images.py.\n"
        "// Source: Google Sheet [PHỎNG VẤN] Tổng hợp bài PV - EP.\n"
        f"window.STORIES = {payload};\n",
        encoding="utf-8",
    )


def main() -> int:
    if not STORIES_JS.exists():
        print(f"! {STORIES_JS} not found — run parse_stories.py first")
        return 1
    text = STORIES_JS.read_text()
    m = re.search(r"window\.STORIES = (\[.*\]);", text, re.S)
    stories = json.loads(m.group(1))

    posts = fetch_substack_posts()
    posts_by_id = {p.get("id"): p for p in posts}

    matched = 0
    generated = 0
    kept_doc = 0
    for s in stories:
        slug = s["slug"]
        out = IMG_DIR / f"{slug}.webp"

        # Highest-priority cover comes from the linked Google Doc (set by
        # crawl_story_bodies.py). If we already have a doc cover, leave it.
        if s.get("coverFrom") == "googledoc" and s.get("cover"):
            kept_doc += 1
            continue

        # Try to match a Substack post by company keywords (best-effort)
        post = best_match(s, posts)
        if post and post.get("cover_image"):
            # Always remember which Substack post this story matches — used
            # downstream as the "View original on Substack" link.
            s["matchedSubstackUrl"] = post.get("canonical_url", "")
            if out.exists():
                s["cover"] = f"assets/img/stories/{out.name}"
                s["coverFrom"] = "substack"
                matched += 1
                continue
            ok = download_image(post["cover_image"], out)
            if ok:
                s["cover"] = f"assets/img/stories/{out.name}"
                s["coverFrom"] = "substack"
                matched += 1
                print(f"  [match] {slug:40s} → {post.get('title','')[:60]}")
                continue

        if not out.exists():
            make_placeholder(s, out)
        s["cover"] = f"assets/img/stories/{out.name}"
        s["coverFrom"] = "placeholder"
        generated += 1

    print(f"  kept {kept_doc} doc covers untouched")

    update_stories_file(stories)
    print()
    print(f"✓ done — matched {matched} from Substack, generated {generated} placeholders")
    return 0


if __name__ == "__main__":
    sys.exit(main())
