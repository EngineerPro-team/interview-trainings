#!/usr/bin/env python3
"""
Generate a 1200x630 Open Graph share image at src/assets/img/og-share.png
- Navy gradient background
- EngineerPro logo on the left
- Big tagline on the right
- Bottom strip with company logos / chips

Run:  python3.11 scripts/make_og_image.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "assets" / "img" / "og-share.png"
LOGO = ROOT / "src" / "assets" / "img" / "logo.png"

W, H = 1200, 630
NAVY = (11, 29, 58)
NAVY2 = (16, 40, 73)
ORANGE = (255, 122, 24)
ORANGE_LIGHT = (255, 176, 102)
CREAM = (248, 245, 239)
WHITE = (255, 255, 255)
MUTED = (200, 210, 220)


def font(size: int, bold: bool = False):
    """Try a few common macOS font paths, fall back to default."""
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def build_background() -> Image.Image:
    img = Image.new("RGB", (W, H), NAVY)
    # vertical gradient
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(NAVY[0] + (NAVY2[0] - NAVY[0]) * t)
        g = int(NAVY[1] + (NAVY2[1] - NAVY[1]) * t)
        b = int(NAVY[2] + (NAVY2[2] - NAVY[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)

    # Orange radial glow upper-right
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, a in [(420, 24), (320, 38), (220, 56), (140, 80), (80, 110)]:
        gd.ellipse((W - 200 - r, -200 - r // 3, W - 200 + r, -200 + r), fill=(*ORANGE, a))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    img.paste(glow, (0, 0), glow)

    # Blue radial glow lower-left
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, a in [(380, 22), (260, 34), (180, 50)]:
        gd.ellipse((-100 - r, H - 100 - r, -100 + r, H - 100 + r), fill=(40, 100, 220, a))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img.paste(glow, (0, 0), glow)

    return img


def draw_logo_tile(img: Image.Image, x: int, y: int, size: int = 120) -> None:
    """Draw a white rounded square with the EP logo centered inside."""
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.rounded_rectangle((0, 0, size, size), radius=22, fill=(255, 255, 255, 255))
    # paste logo
    if LOGO.exists():
        logo = Image.open(LOGO).convert("RGBA")
        inset = int(size * 0.16)
        target = size - inset * 2
        logo.thumbnail((target, target), Image.LANCZOS)
        lw, lh = logo.size
        tile.paste(logo, ((size - lw) // 2, (size - lh) // 2), logo)
    img.paste(tile, (x, y), tile)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    img = build_background()
    d = ImageDraw.Draw(img)

    PADDING = 70
    draw_logo_tile(img, PADDING, PADDING, size=110)

    # Brand text next to the logo tile
    fbrand = font(40, bold=True)
    d.text((PADDING + 130, PADDING + 28), "EngineerPro", font=fbrand, fill=WHITE)
    fbrand_sub = font(20)
    d.text((PADDING + 130, PADDING + 78), "Software Education · Mastering Engineer",
           font=fbrand_sub, fill=ORANGE_LIGHT)

    # Headline
    fhead1 = font(82, bold=True)
    fhead2 = font(82, bold=True)
    y_head = 240
    d.text((PADDING, y_head), "Chinh phục", font=fhead1, fill=WHITE)
    w1, _ = text_size(d, "Chinh phục ", fhead1)
    d.text((PADDING + w1, y_head), "Big Tech", font=fhead2, fill=ORANGE)
    d.text((PADDING, y_head + 95), "cùng mentor thực chiến.", font=fhead1, fill=WHITE)

    # Subline
    fsub = font(26)
    sub = "100% mentors từ Google · Amazon · TikTok · Shopee · Spotify · Uber"
    d.text((PADDING, y_head + 215), sub, font=fsub, fill=MUTED)

    # Bottom chip row
    chips = [
        ("2K+", "Học viên"),
        ("500+", "Offers"),
        ("19", "Mentor Big Tech"),
        ("10", "Khoá học"),
        ("3+ năm", "Từ 04·2023"),
    ]
    chip_y = H - 130
    fchip_num = font(34, bold=True)
    fchip_lbl = font(18)
    chip_x = PADDING
    for num, lbl in chips:
        wn, _ = text_size(d, num, fchip_num)
        wl, _ = text_size(d, lbl, fchip_lbl)
        cw = max(wn, wl) + 60
        # background pill
        d.rounded_rectangle(
            (chip_x, chip_y, chip_x + cw, chip_y + 90),
            radius=18,
            fill=(255, 255, 255, 28),
            outline=(255, 255, 255, 60),
            width=1,
        )
        d.text((chip_x + (cw - wn) // 2, chip_y + 12), num, font=fchip_num, fill=ORANGE)
        d.text((chip_x + (cw - wl) // 2, chip_y + 58), lbl, font=fchip_lbl, fill=MUTED)
        chip_x += cw + 14

    # Save (slightly compressed PNG)
    img.save(OUT, format="PNG", optimize=True)
    print(f"✓ wrote {OUT.relative_to(ROOT)}  ({OUT.stat().st_size // 1024} KB, {W}x{H})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
