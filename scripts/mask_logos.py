#!/usr/bin/env python3
"""
Convert colored raster brand logos to monochrome silhouettes suitable for use
with CSS `mask-image`. Detects the dominant background colour from the image
edges, makes that transparent, and turns the remaining pixels into solid black
with full alpha. Output preserves the original aspect ratio + a small padding.

Run:  python3.11 scripts/mask_logos.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
IN_DIR = ROOT / "src" / "assets" / "img" / "companies"

# mode = "fg": keep pixels close to `color`, drop the rest.
# mode = "bg": drop pixels close to `color`, keep the rest.
# threshold: how close (sum of absolute channel diffs) a pixel must be.
JOBS = [
    {"src": "axon.png",            "mode": "fg", "color": (255, 220, 0),   "threshold": 220, "out": "axon-mask.png"},
    {"src": "worldquant.png",      "mode": "fg", "color": (10, 10, 10),    "threshold": 150, "out": "worldquant-mask.png"},
    {"src": "employment-hero.png", "mode": "fg", "color": (255, 255, 255), "threshold": 80,  "out": "employment-hero-mask.png"},
    {"src": "anz.png",             "mode": "fg", "color": (0, 130, 200),   "threshold": 300, "out": "anz-mask.png"},
    {"src": "shopee.png",          "mode": "fg", "color": (238, 77, 45),   "threshold": 220, "out": "shopee-mask.png"},
    {"src": "okx.png",             "mode": "fg", "color": (255, 255, 255), "threshold": 80,  "out": "okx-mask.png"},
    {"src": "sap.png",             "mode": "fg", "color": (255, 255, 255), "threshold": 80,  "out": "sap-mask.png"},
    {"src": "cognizant.png",       "mode": "bg", "color": (255, 255, 255), "threshold": 120, "out": "cognizant-mask.png"},
    {"src": "robinhood.png",       "mode": "fg", "color": (0, 0, 0),       "threshold": 200, "out": "robinhood-mask.png"},
    {"src": "goldman-sachs.png",   "mode": "fg", "color": (255, 255, 255), "threshold": 90,  "out": "goldman-sachs-mask.png"},
    {"src": "naver.png",           "mode": "fg", "color": (3, 199, 90),    "threshold": 220, "out": "naver-mask.png"},
]


def dominant_edge_color(img: Image.Image) -> tuple[int, int, int]:
    """Sample pixels along the four edges to estimate background colour."""
    w, h = img.size
    samples = []
    for x in range(0, w, max(1, w // 50)):
        samples.append(img.getpixel((x, 0))[:3])
        samples.append(img.getpixel((x, h - 1))[:3])
    for y in range(0, h, max(1, h // 50)):
        samples.append(img.getpixel((0, y))[:3])
        samples.append(img.getpixel((w - 1, y))[:3])
    # take the mean colour as background estimate
    r = sum(s[0] for s in samples) // len(samples)
    g = sum(s[1] for s in samples) // len(samples)
    b = sum(s[2] for s in samples) // len(samples)
    return (r, g, b)


def colour_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def to_mask(src: Path, out: Path, mode: str, color, threshold: int, pad: int = 14) -> None:
    img = Image.open(src).convert("RGBA")
    color = tuple(color)
    print(f"  · {src.name}: mode={mode} target=rgb{color} threshold={threshold}")

    w, h = img.size
    out_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    in_px = img.load()
    out_px = out_img.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = in_px[x, y]
            if a < 30:
                continue
            d = colour_distance((r, g, b), color)
            keep = (mode == "fg" and d <= threshold) or (mode == "bg" and d >= threshold)
            if keep:
                out_px[x, y] = (0, 0, 0, 255)

    bbox = out_img.getbbox()
    if bbox:
        out_img = out_img.crop(bbox)
        out_img = ImageOps.expand(out_img, border=pad, fill=(0, 0, 0, 0))
    out_img.save(out, format="PNG", optimize=True)
    print(f"     → {out.relative_to(ROOT)} ({out_img.size[0]}x{out_img.size[1]}, {out.stat().st_size // 1024} KB)")


def main() -> int:
    print(f"→ converting {len(JOBS)} logos to silhouette masks …")
    for job in JOBS:
        src = IN_DIR / job["src"]
        if not src.exists():
            print(f"  ! missing: {src}")
            continue
        to_mask(src, IN_DIR / job["out"], job["mode"], job["color"], job["threshold"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
