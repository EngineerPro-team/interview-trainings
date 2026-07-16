"""Generate a compact syllabus image for the ML / Agentic AI course.

Renders 10 lecture cards (crisp text via PIL) on a branded dark card. Run:
    python3 scripts/make_ml_syllabus.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "src", "assets", "img", "courses", "ml-agentic-ai-syllabus.png")

FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FR = "/System/Library/Fonts/Supplemental/Arial.ttf"

BLUE = (36, 122, 255)
ORANGE = (255, 138, 51)
WHITE = (238, 244, 252)
MUTED = (150, 168, 196)
CARD = (22, 34, 58)
CARD_BORDER = (44, 63, 99)

LECTURES = [
    ("Foundations & Formulation", "ML vs SW · framing · metrics", "1–2"),
    ("Architecture & Data Pipelines", "MVP · ingestion · labeling", "3–4"),
    ("Feature Engineering", "actors · stores · online/offline", "5"),
    ("Modeling & Offline Eval", "model selection · training · metrics", "6"),
    ("Prediction & Serving", "batch/online · ANN · edge", "7"),
    ("Experimentation & Monitoring", "A/B · drift · continual learning", "8–9"),
    ("Recommendation Systems", "candidate gen · ranking · LTR", "★"),
    ("Search, Ranking & Ads", "retrieval · LTR · multi-stage", "★"),
    ("NLP · CV · Trust & Safety", "pipelines · moderation · fraud", "★"),
    ("GenAI / LLM & Capstone", "RAG · agents · eval · mock", "★"),
]


def font(p, s):
    return ImageFont.truetype(p, s)


def main():
    W = 1200
    MARGIN = 48
    HEAD_H = 172
    ROW_H = 150
    ROW_GAP = 16
    COL_GAP = 28
    rows = 5
    H = HEAD_H + rows * ROW_H + (rows - 1) * ROW_GAP + MARGIN
    colw = (W - 2 * MARGIN - COL_GAP) // 2

    img = Image.new("RGB", (W, H), (10, 16, 36))
    d = ImageDraw.Draw(img)
    # top accent bar
    d.rectangle([0, 0, W, 6], fill=BLUE)
    for i in range(W // 2, W):
        pass
    d.rectangle([W // 2, 0, W, 6], fill=ORANGE)

    # Header
    d.text((MARGIN, 40), "ML SYSTEM DESIGN", font=font(FB, 46), fill=WHITE)
    d.text((MARGIN, 96), "10 lectures · 9-step formula · production ML → GenAI / Agentic AI",
            font=font(FR, 24), fill=MUTED)

    y0 = HEAD_H
    for idx, (title, focus, step) in enumerate(LECTURES):
        r = idx // 2
        c = idx % 2
        x = MARGIN + c * (colw + COL_GAP)
        y = y0 + r * (ROW_H + ROW_GAP)
        # card
        d.rounded_rectangle([x, y, x + colw, y + ROW_H], radius=16,
                            fill=CARD, outline=CARD_BORDER, width=1)
        # number badge
        n = idx + 1
        badge = ORANGE if idx == 9 else BLUE
        bx, by, br = x + 44, y + ROW_H // 2, 30
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=badge)
        num = str(n)
        nf = font(FB, 30)
        tw = d.textlength(num, font=nf)
        d.text((bx - tw / 2, by - 20), num, font=nf, fill=(10, 16, 36))
        # texts
        tx = x + 92
        d.text((tx, y + 34), title, font=font(FB, 26), fill=WHITE)
        d.text((tx, y + 74), focus, font=font(FR, 20), fill=MUTED)
        # step chip
        chip = f"Step {step}" if step != "★" else "Full formula"
        cf = font(FB, 17)
        cw = d.textlength(chip, font=cf)
        chx2 = x + colw - 18
        chx1 = chx2 - cw - 20
        d.rounded_rectangle([chx1, y + 16, chx2, y + 44], radius=999,
                            fill=(30, 44, 72))
        d.text((chx1 + 10, y + 21), chip, font=cf, fill=(122, 168, 255))

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
