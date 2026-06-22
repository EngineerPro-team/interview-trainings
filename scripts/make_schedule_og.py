"""Generate a branded OG share image for /lich-khai-giang/.

Composites the schedule hero banner + a dark scrim + the EngineerPro logo
(on a white rounded chip) + crisp Vietnamese title text. Run:

    python3 scripts/make_schedule_og.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "src", "assets", "img")

W, H = 1200, 630
ORANGE = (255, 138, 51)
WHITE = (255, 255, 255)
SUB = (214, 224, 240)

FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FR = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def rounded_card(size, radius, fill):
    card = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=fill)
    return card


def main():
    # 1. Background: cover-fit the hero banner to 1200x630
    bg = Image.open(os.path.join(IMG, "schedule-hero.png")).convert("RGB")
    scale = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * scale), int(bg.height * scale)))
    x = (bg.width - W) // 2
    y = (bg.height - H) // 2
    bg = bg.crop((x, y, x + W, y + H)).convert("RGBA")

    # 2. Dark scrim — stronger on the left for text legibility
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(W):
        a = int(225 * (1 - i / W)) + 55
        od.line([(i, 0), (i, H)], fill=(8, 16, 36, max(0, min(238, a))))
    img = Image.alpha_composite(bg, overlay)

    draw = ImageDraw.Draw(img)
    PAD = 70

    # 3. Logo on a white rounded chip (logo art has a white background already)
    logo = Image.open(os.path.join(IMG, "logo.png")).convert("RGB")
    diff = ImageChops.difference(logo, Image.new("RGB", logo.size, (255, 255, 255)))
    bbox = diff.convert("L").getbbox()
    logo = logo.crop(bbox)
    target_h = 92
    lw = int(logo.width * target_h / logo.height)
    logo = logo.resize((lw, target_h))
    cpad = 22
    card = rounded_card((lw + cpad * 2, target_h + cpad * 2), 22, (255, 255, 255, 255))
    card.paste(logo, (cpad, cpad))
    img.alpha_composite(card, (PAD, 52))

    # 4. Eyebrow
    eb_y = 52 + card.height + 34
    draw.text((PAD, eb_y), "KHAI GIẢNG · THÁNG 6 – 7 · 2026",
              font=font(FB, 30), fill=ORANGE)

    # 5. Title (two lines)
    t_y = eb_y + 50
    draw.text((PAD, t_y), "LỊCH KHAI GIẢNG", font=font(FB, 92), fill=WHITE)
    draw.text((PAD, t_y + 100), "CÁC LỚP MỚI", font=font(FB, 92), fill=WHITE)

    # 6. Bottom block: courses + mentor note + URL, all left-aligned
    c_y = t_y + 232
    draw.text((PAD, c_y),
              "DSA · System Design · CS Fundamentals · Backend Go · Redis",
              font=font(FR, 30), fill=SUB)
    draw.text((PAD, c_y + 44), "Mentor 100% Big Tech · Học online (GMT+7)",
              font=font(FR, 27), fill=SUB)
    draw.text((PAD, c_y + 90), "engineerprogurus.com/lich-khai-giang",
              font=font(FB, 29), fill=ORANGE)

    out = os.path.join(IMG, "schedule-og.png")
    img.convert("RGB").save(out, "PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
