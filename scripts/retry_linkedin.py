#!/usr/bin/env python3
"""
Stubborn retry of LinkedIn profile fetches we couldn't get last time.
- Random delay 15-40s between requests
- Rotates user agents (Mac Safari / Windows Chrome / iPhone Safari)
- Up to 3 attempts per slug
- Extracts og:title / og:description / og:image when HTTP 200
- Downloads og:image to src/assets/img/mentors/<slug>.jpg if it's a real photo
  (not the static LinkedIn fallback icon)

Usage:  python3 scripts/retry_linkedin.py
"""
from __future__ import annotations

import json
import random
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "src" / "assets" / "img" / "mentors"
PHOTOS.mkdir(parents=True, exist_ok=True)

# Slug → preferred local filename mapping
SLUGS = {
    "tungtran309":                "tung-tran",
    "hoangdquang":                "quang-hoang",
    "vu-thi-thien-anh":           "thien-anh",
    "nguyen-anh-viet":            "viet-nguyen",
    "kylenguyen141":              "kyle-nguyen",
    "tranhieu23":                 "hieu-tran",
    "ntlam94":                    "tung-lam",
    "thomas-quach-669818117":     "thomas-quach",
    "lam0895":                    "lam-pham",
    "loi-nguyen-thang":           "loi-nguyen",
    "manhdx":                     "manh",
    # Already-known cases we want to refresh og:image for, in case profile updated
    "huytq56":                    "huy-tran",
    "vuducnhi":                   "nhi-vu",
}

UAS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
]


def fetch(url: str, ua: str) -> tuple[int, bytes]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/avif,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Upgrade-Insecure-Requests": "1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception:
        return 0, b""


def extract_og(html: str) -> dict:
    out = {}
    for key in ("title", "description", "image"):
        m = re.search(rf'og:{key}"\s+content="([^"]+)"', html)
        if m:
            out[key] = m.group(1).replace("&amp;", "&")
    return out


def looks_like_real_photo(url: str) -> bool:
    """LinkedIn's default fallback icon URL contains 'static.licdn.com'.
    Real photos live on 'media.licdn.com/dms/image/...'."""
    return "media.licdn.com" in url and "profile-displayphoto" in url


def download_photo(url: str, out_path: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UAS[0]})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
        if len(data) < 1000:
            return False
        out_path.write_bytes(data)
        return True
    except Exception:
        return False


def try_one(slug: str, max_attempts: int = 3) -> dict:
    url = f"https://www.linkedin.com/in/{slug}/"
    for attempt in range(1, max_attempts + 1):
        ua = random.choice(UAS)
        delay = random.uniform(18, 38)
        print(f"  [{slug}] attempt {attempt}/{max_attempts}  sleep {delay:.0f}s …", end=" ", flush=True)
        time.sleep(delay)
        code, body = fetch(url, ua)
        print(f"HTTP {code} ({len(body)}B)")
        if code != 200 or len(body) < 5000:
            continue
        html = body.decode("utf-8", errors="replace")
        og = extract_og(html)
        if og.get("title", "").startswith("Just a moment") or "Just a moment" in og.get("title", ""):
            continue
        return og
    return {}


def main() -> int:
    print(f"→ retrying {len(SLUGS)} LinkedIn profiles (this will take ~5-10 min) …\n")
    results = {}
    for i, (slug, local) in enumerate(SLUGS.items(), 1):
        print(f"[{i}/{len(SLUGS)}] {slug}  →  {local}.jpg")
        og = try_one(slug)
        if not og:
            print(f"    ✗ blocked or no data")
            results[slug] = {"status": "blocked"}
            continue
        title = og.get("title", "")
        # Split "Name - Company | LinkedIn" → ("Name", "Company")
        name, company = "", ""
        if " | LinkedIn" in title:
            head = title.replace(" | LinkedIn", "").strip()
            if " - " in head:
                name, company = [s.strip() for s in head.split(" - ", 1)]
            else:
                name = head
        photo_ok = False
        img_url = og.get("image", "")
        if img_url and looks_like_real_photo(img_url):
            ok = download_photo(img_url, PHOTOS / f"{local}.jpg")
            photo_ok = ok
            print(f"    ✓ name={name!r} company={company!r} photo={'YES' if ok else 'fail'}")
        else:
            print(f"    ✓ name={name!r} company={company!r} photo=(default icon)")
        results[slug] = {
            "status": "ok",
            "name": name,
            "company": company,
            "description": og.get("description", "")[:200],
            "photo_url": img_url,
            "photo_saved": photo_ok,
            "local_photo": f"assets/img/mentors/{local}.jpg" if photo_ok else None,
        }

    print("\n=== SUMMARY ===")
    ok = [s for s, r in results.items() if r.get("status") == "ok"]
    blocked = [s for s, r in results.items() if r.get("status") == "blocked"]
    with_photo = [s for s, r in results.items() if r.get("photo_saved")]
    print(f"OK:      {len(ok)}/{len(SLUGS)}  → {ok}")
    print(f"Blocked: {len(blocked)}/{len(SLUGS)} → {blocked}")
    print(f"Photos:  {len(with_photo)}/{len(SLUGS)} → {with_photo}")

    (ROOT / "scripts" / "linkedin-retry-results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False)
    )
    print(f"\nDetailed results → scripts/linkedin-retry-results.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
