"""Generate a promo poster for the Aug/Sep/Oct 2026 cohorts (crisp text via PIL)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "src", "assets", "img")
OUT = "/tmp/khai-giang-thang-8-9-10.png"

W, H = 1080, 1840
ORANGE = (255, 138, 51)
WHITE = (255, 255, 255)
SUB = (200, 214, 236)
MUTED = (150, 168, 196)
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FR = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(p, s):
    return ImageFont.truetype(p, s)


def rrect(size, r, fill):
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=r, fill=fill)
    return im


MONTHS = [
    ("THÁNG 7 · 2026", [
        ("14/07", "DSA Level 1", "Thứ 3 & Thứ 7 · 20:00–22:00"),
        ("18/07", "CS Fundamentals", "Thứ 7 · 16:00–18:00"),
        ("18/07", "Crash Course: Redis", "Thứ 7 · 20:00–22:00"),
        ("26/07", "DSA Level 2", "Thứ 4 & CN · 20:00–22:00"),
    ]),
    ("THÁNG 8 · 2026", [
        ("16/08", "System Design Interview L2", "Chủ nhật · 10:00–11:59"),
        ("23/08", "Behavioral Interview", "T2 tối & T7 chiều"),
        ("31/08", "ML / Agentic AI", "Tối T2 & T5 · 20:30–22:00"),
    ]),
    ("THÁNG 9 · 2026", [
        ("05/09", "DSA Level 3", "Thứ 7 · 14:00–16:00"),
        ("20/09", "System Design Interview L1", "Chủ nhật · 08:00–10:00"),
    ]),
    ("THÁNG 10 · 2026", [
        ("03/10", "Backend Golang L1", "Thứ 7 · 08:00–10:00"),
        ("13/10", "DSA Level 1", "Thứ 3 & Thứ 7 · 20:00–22:00"),
        ("25/10", "DSA Level 2", "Thứ 4 & CN · 20:00–22:00"),
    ]),
]


def main():
    # background: hero banner cover-fit + dark scrim
    bg = Image.open(os.path.join(IMG, "schedule-hero.png")).convert("RGB")
    scale = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * scale), int(bg.height * scale)))
    x = (bg.width - W) // 2
    y = (bg.height - H) // 2
    img = bg.crop((x, y, x + W, y + H)).convert("RGBA")
    scrim = Image.new("RGBA", (W, H), (8, 16, 36, 205))
    img = Image.alpha_composite(img, scrim)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=ORANGE)
    PAD = 64

    # logo chip
    logo = Image.open(os.path.join(IMG, "logo.png")).convert("RGB")
    diff = ImageChops.difference(logo, Image.new("RGB", logo.size, (255, 255, 255)))
    logo = logo.crop(diff.convert("L").getbbox())
    th = 74
    lw = int(logo.width * th / logo.height)
    logo = logo.resize((lw, th))
    cp = 18
    chip = rrect((lw + cp * 2, th + cp * 2), 18, (255, 255, 255, 255))
    chip.paste(logo, (cp, cp))
    img.alpha_composite(chip, (PAD, 48))

    # title
    d.text((PAD, 172), "LỊCH KHAI GIẢNG", font=font(FB, 74), fill=WHITE)
    d.text((PAD, 258), "Tháng 7 · 8 · 9 · 10 — 2026", font=font(FB, 40), fill=ORANGE)
    d.text((PAD, 316), "Học online qua Zoom · Mentor 100% Big Tech · giờ GMT+7",
           font=font(FR, 24), fill=SUB)

    yy = 396
    for title, rows in MONTHS:
        # month pill
        mf = font(FB, 30)
        tw = d.textlength(title, font=mf)
        d.rounded_rectangle([PAD, yy, PAD + tw + 40, yy + 46], radius=999,
                            fill=(255, 122, 24))
        d.text((PAD + 20, yy + 8), title, font=mf, fill=(10, 16, 36))
        yy += 66
        for dd, name, meta in rows:
            # date badge
            bw = 92
            d.rounded_rectangle([PAD, yy, PAD + bw, yy + 62], radius=12,
                                fill=(255, 255, 255), outline=None)
            dnum, dmon = dd.split("/")
            d.text((PAD + bw / 2 - d.textlength(dnum, font=font(FB, 30)) / 2, yy + 8),
                   dnum, font=font(FB, 30), fill=(11, 29, 58))
            d.text((PAD + bw / 2 - d.textlength("/" + dmon, font=font(FB, 18)) / 2, yy + 40),
                   "/" + dmon, font=font(FB, 18), fill=(255, 122, 24))
            tx = PAD + bw + 22
            d.text((tx, yy + 6), name, font=font(FB, 30), fill=WHITE)
            d.text((tx, yy + 42), meta, font=font(FR, 21), fill=MUTED)
            yy += 78
        yy += 14

    # bottom CTA
    cta = "💬 Inbox EngineerPro để giữ chỗ"
    d.text((PAD, H - 92), "engineerprogurus.com/lich-khai-giang",
           font=font(FB, 26), fill=ORANGE)
    d.text((PAD, H - 128), "Giữ chỗ sớm — mỗi lớp giới hạn 15–20 học viên",
           font=font(FR, 24), fill=SUB)

    img.convert("RGB").save(OUT, "PNG")
    print("wrote", OUT, "yy_end", yy)


if __name__ == "__main__":
    main()
