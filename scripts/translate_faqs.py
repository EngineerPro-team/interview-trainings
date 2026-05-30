#!/usr/bin/env python3
"""
Add English translations to src/assets/faqs-data.js.

The crawler (crawl_faqs.py) populates question + html in Vietnamese; this
script merges hand-written EN translations onto each item by index.
Re-runs are safe — runs after the Vietnamese crawl.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAQS_JS = ROOT / "src" / "assets" / "faqs-data.js"

# Hand-translated EN content for each FAQ — keyed by Vietnamese question prefix
# so the match is robust even if order changes slightly.
EN_TRANSLATIONS = {
    "thi vào big tech có cần bằng tiếng anh": {
        "questionEn": "Do I need an English certificate (IELTS, TOEFL, TOEIC…) to interview at Big Tech?",
        "htmlEn":
            "<p>You don't need any specific certificate, but you do need strong "
            "communication skills in English to use it on the job.</p>",
    },
    "có cần bằng đại học để thi vào các big": {
        "questionEn": "Do I need a degree to interview at Big/Rich Tech or smaller companies?",
        "htmlEn":
            "<p>It depends on the company, but most Big Tech firms <strong>do require</strong> "
            "a degree in Computer Science / Software Engineering.</p>"
            "<ul><li><strong>Watch this video for more: "
            "<a href=\"https://youtu.be/XMfSSedM_Mw\" rel=\"noopener\" target=\"_blank\">"
            "https://youtu.be/XMfSSedM_Mw</a></strong></li></ul>"
            "<p><em>For small / mid-size companies, many still don't require one.</em></p>",
    },
    "vị trí nào nhiều positions nhất tại các big tech": {
        "questionEn": "Which role has the most positions at Big Tech (in Vietnam and abroad)?",
        "htmlEn":
            "<p><strong>Backend</strong> is the role with the most openings at Big Tech.</p>"
            "<p><strong>More info:</strong> "
            "<a href=\"https://www.youtube.com/watch?v=DCEGLAWoTUs&amp;t=3s\" rel=\"noopener\" target=\"_blank\">"
            "https://www.youtube.com/watch?v=DCEGLAWoTUs&amp;t=3s</a></p>",
    },
    "engineerpro/engineerpro academy có hỗ trợ học viên tìm việc": {
        "questionEn": "Does EngineerPro / EngineerPro Academy help students find jobs at Big Tech or smaller companies?",
        "htmlEn":
            "<p>Yes. EngineerPro / EngineerPro Academy commits to walking with students all "
            "the way to the offer — including internal talk training sessions. Message our "
            "fanpage for job-search support.</p>",
    },
    "sự khác biệt của engineerpro và engineerpro academy": {
        "questionEn": "What's the difference between EngineerPro and EngineerPro Academy?",
        "htmlEn":
            "<p><strong>EngineerPro</strong> focuses on interview-prep courses for Big Tech.</p>"
            "<ul><li>Fanpage: <a href=\"https://www.facebook.com/EngineerPro.Official\" rel=\"noopener\" target=\"_blank\">"
            "https://www.facebook.com/EngineerPro.Official</a></li></ul>"
            "<p><strong>EngineerPro Academy</strong> focuses on building rock-solid "
            "Computer Science foundations.</p>"
            "<ul><li>Fanpage: <a href=\"https://www.facebook.com/EngineerPro.Academy\" rel=\"noopener\" target=\"_blank\">"
            "https://www.facebook.com/EngineerPro.Academy</a></li></ul>",
    },
    "học gì để thi vào big tech": {
        "questionEn": "What should I study to interview at Big Tech?",
        "htmlEn":
            "<p>Big Tech interviews almost always cover Algorithms and Computer Science "
            "Fundamentals.</p>"
            "<p>Depending on the company, juniors may have a System Design round (mid-level "
            "and above will 100% have it).</p>"
            "<p>EngineerPro offers interview-prep training for Algorithms, System Design, "
            "and CS Fundamentals — DM the page for details: "
            "<a href=\"https://www.facebook.com/EngineerPro.Official\" rel=\"noopener\" target=\"_blank\">"
            "https://www.facebook.com/EngineerPro.Official</a></p>",
    },
    "hệ thống engineerpro có cung cấp lộ trình dành cho các bạn mất gốc": {
        "questionEn": "Does EngineerPro offer a path for beginners or people who lost the basics?",
        "htmlEn":
            "<p>Yes. The EngineerPro Academy team has a structured path to fill CS knowledge "
            "gaps and train you into a professional software engineer.</p>"
            "<ul><li>Fanpage for details: "
            "<a href=\"https://www.facebook.com/EngineerPro.Academy\" rel=\"noopener\" target=\"_blank\">"
            "https://www.facebook.com/EngineerPro.Academy</a></li>"
            "<li>More info: <a href=\"https://youtu.be/KnbNHKuSS4U\" rel=\"noopener\" target=\"_blank\">"
            "https://youtu.be/KnbNHKuSS4U</a></li></ul>",
    },
    "các khoá học của engineerpro và engineerpro academy dạy bằng tiếng việt": {
        "questionEn": "Are EngineerPro / EngineerPro Academy courses taught in Vietnamese or English?",
        "htmlEn":
            "<p>All EngineerPro / EngineerPro Academy courses are taught in Vietnamese.</p>",
    },
}


def main() -> int:
    if not FAQS_JS.exists():
        print(f"! {FAQS_JS} not found — run crawl_faqs.py first")
        return 1
    text = FAQS_JS.read_text()
    m = re.search(r"window\.FAQS = (\[.*\]);", text, re.S)
    items = json.loads(m.group(1))

    matched = 0
    for it in items:
        q = (it.get("question") or "").lower()
        for prefix, en in EN_TRANSLATIONS.items():
            if q.startswith(prefix) or prefix in q:
                it["questionEn"] = en["questionEn"]
                it["htmlEn"] = en["htmlEn"]
                matched += 1
                break

    header = text[: text.index("window.FAQS")]
    payload = json.dumps(items, ensure_ascii=False, indent=2)
    FAQS_JS.write_text(f"{header}window.FAQS = {payload};\n", encoding="utf-8")
    print(f"✓ added EN translation to {matched}/{len(items)} FAQs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
