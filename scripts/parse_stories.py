#!/usr/bin/env python3
"""
Parse the EngineerPro Google Sheet markdown export into a clean stories list,
generate catchy Vietnamese titles + structured article bodies, and emit a JS
data file for the Success Stories tab.

Input:  uploads/edit-0.md (the markdown export of the Google Sheet)
Output: src/assets/stories-data.js  →  window.STORIES = [{slug,title,body,...}]
"""
from __future__ import annotations

import json
import random
import os
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Order of resolution for the sheet markdown:
#   1. CLI arg              python parse_stories.py path/to/edit-0.md
#   2. EP_STORIES_MD env var
#   3. uploads/edit-0.md   (drop the file in repo for reproducible runs)
#   4. Author's local cursor uploads (legacy default)
_CLI = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else None
_ENV = Path(os.environ["EP_STORIES_MD"]).expanduser() if os.environ.get("EP_STORIES_MD") else None
_REPO = ROOT / "uploads" / "edit-0.md"
_AUTHOR = Path(
    "/Users/lamp/.cursor/projects/Users-lamp-Desktop-individual-projects-interview-trainings/uploads/edit-0.md"
)
SHEET_MD = next((p for p in (_CLI, _ENV, _REPO, _AUTHOR) if p and p.exists()), _REPO)
OUT = ROOT / "src" / "assets" / "stories-data.js"
MAX_OUTPUT = 100

# Tier ranking — lower number = higher priority (shown first)
TIER_MAP = {
    # Tier 1: top FAANG-adjacent
    "google":      1, "meta":         1, "facebook":   1, "amazon":     1,
    "microsoft":   1, "tiktok":       1, "uber":       1, "apple":      1,
    "tesla":       1, "nvidia":       1, "spotify":    1, "citadel":    1,
    "gfg":         2,  # Goldman Family Group / other — keep distinct, mid-tier
    # Tier 2: strong global / regional
    "grab":        2, "shopee":       2, "naver":      2, "nab":        2,
    "anz":         2, "sap":          2, "axon":       2, "caladan":    2,
    "motional":    2, "pendle":       2, "acronis":    2, "snap":       2,
    "money forward": 2, "moreh":      2, "ant":        2, "ant group":  2,
    "rakuten":     2, "goodnote":     2, "zendesk":    2, "wolt":       2,
    "siliconfi":   2, "silicon":      2, "deputy":     2, "remitano":   2,
    "ninja van":   2, "cake":         2, "fpt hitachi":3,
    # Tier 3 — bank / SI / Vietnamese tech
    "mb bank":     3, "vinbigdata":   3, "anduin":     3, "shopback":   3,
    "starcamp":    3, "tookitaki":    3, "spartan":    3, "thoughtwork":3,
    "cốc cốc":     3, "coc coc":      3,
    "employment hero": 2, "emloyment hero": 2,
}
DEFAULT_TIER = 4

# Common company aliases / normalization
ALIAS = {
    "gfg": "GFG",   # keep as-is; not assumed to be Google
    "ant": "Ant Group",
    "ant group": "Ant Group",
    "emloyment hero": "Employment Hero",
    "employment hero": "Employment Hero",
    "money forward": "Money Forward",
    "ninja van": "Ninja Van",
    "rakuten": "Rakuten",
    "wolt": "Wolt",
    "axon": "Axon",
    "anz": "ANZ",
    "naz": "ANZ",  # common typo in sheet for ANZ
    "nab": "NAB",
    "sap": "SAP",
    "grab": "Grab",
    "shopee": "Shopee",
    "google": "Google",
    "meta": "Meta",
    "amazon": "Amazon",
    "microsoft": "Microsoft",
    "tiktok": "TikTok",
    "uber": "Uber",
    "tesla": "Tesla",
    "nvidia": "Nvidia",
    "naver": "Naver",
    "spotify": "Spotify",
    "citadel": "Citadel",
    "caladan": "Caladan",
    "motional": "Motional",
    "pendle": "Pendle",
    "acronis": "Acronis",
    "snap": "Snap",
    "moreh": "Moreh",
    "anduin": "Anduin",
    "shopback": "Shopback",
    "starcamp": "Starcamp NAB",
    "tookitaki": "Tookitaki",
    "vinbigdata": "VinBigData",
    "mb bank": "MB Bank",
    "spartan": "Spartan",
    "thoughtwork": "ThoughtWorks",
    "cốc cốc": "Cốc Cốc",
    "coc coc": "Cốc Cốc",
    "deputy": "Deputy",
    "remitano": "Remitano",
    "cake": "Cake",
    "goodnote": "Goodnote",
    "zendesk": "Zendesk",
    "rakuten": "Rakuten",
    "fpt hitachi": "FPT Hitachi",
    "silicon": "Silicon",
}


KNOWN_COMPANIES = set(ALIAS.values())


def normalize_company(s: str) -> str | None:
    """Return the canonical company name if `s` matches a known brand, else None.
    Refuses junk fragments like 'Senior Tại Nab', 'Goodnote (4', 'Anh Sơn - Eh'."""
    key = s.strip().lower()
    # Direct alias hit
    if key in ALIAS:
        return ALIAS[key]
    # Sometimes the company part is a free-form note. Probe the lowercased text
    # for an embedded known brand keyword.
    for kw, label in ALIAS.items():
        if " " not in kw and re.search(rf"\b{re.escape(kw)}\b", key):
            return label
    # Last chance: if the original string IS exactly a canonical name (case-insensitive)
    for canonical in KNOWN_COMPANIES:
        if canonical.lower() == key:
            return canonical
    return None


HONORIFICS = ("anh", "chị", "chi", "bạn", "ban", "em", "cô", "co")
NOISE_TOKENS = {
    "ẩn danh", "k ảnh", "không ảnh", "có hình", "k để hình", "k de hinh",
    "mentor", "intern", "ẩn danh", "anonymous",
}


def _proper_case_vi(s: str) -> str:
    """Convert a person-name fragment to Title Case, preserving Vietnamese
    diacritics and avoiding weird intra-word caps like 'ANh'."""
    out = []
    for word in s.split():
        if not word:
            continue
        # Special-case common honorifics → capitalize first letter only
        low = word.lower()
        if low in HONORIFICS:
            out.append(low.capitalize())
        else:
            out.append(word[0].upper() + word[1:].lower())
    return " ".join(out)


def clean_name(raw: str) -> str:
    """Clean a person name field: drop tags, drop trailing 'intern/k ảnh/...',
    drop trailing '– Company' garbage, normalize caps."""
    s = raw.strip()
    # Strip markdown-escaped bracket tags  \[...\]  or  [...]
    s = re.sub(r"\\?\[[^\]]*\\?\]", "", s)
    # Strip leading "NNN. " or "NNN\\. "
    s = re.sub(r"^\d+\\?\.\s*", "", s)
    # Strip leading "web - phỏng vấn"
    s = re.sub(r"^web\s*[-–]\s*phỏng vấn\s*", "", s, flags=re.IGNORECASE)
    s = s.strip()

    # Drop "ẩn danh / k ảnh / k để hình / không ảnh / intern XYZ" trailing notes
    s = re.sub(r"\s*[–-]\s*(ẩn danh|k ảnh|không ảnh|k để hình|có hình).*$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+(ẩn danh|k ảnh|không ảnh|k để hình|có hình)\b.*$", "", s, flags=re.IGNORECASE)
    # Drop trailing "intern <company>" — info already in companies field
    s = re.sub(r"\s+intern\s+\S+.*$", "", s, flags=re.IGNORECASE)
    # If still has "– Company" at the end (e.g. "Anh Khoa – NAB – Money forward")
    # keep only the head before the first dash
    s = re.split(r"\s*[–]\s*", s, maxsplit=1)[0]
    s = s.strip(" -·,")
    if not s:
        return s
    return _proper_case_vi(s)


def parse_row(row_cells: list[str]) -> dict | None:
    """row_cells = E F G H I cols (excl. leading A row-number)."""
    if len(row_cells) < 2:
        return None
    stt = row_cells[0].strip()
    title = row_cells[1].strip() if len(row_cells) > 1 else ""
    status = row_cells[2].strip() if len(row_cells) > 2 else ""
    link_col = row_cells[3].strip() if len(row_cells) > 3 else ""
    note_col = row_cells[4].strip() if len(row_cells) > 4 else ""

    if not title or not stt.isdigit():
        return None
    if status and "đã đăng" not in status.lower():
        return None  # skip CHƯA ĐĂNG

    # If the title field itself is a URL (some rows have that)
    direct_url = ""
    if title.startswith("http"):
        direct_url = title
        title = ""

    # Substack URL hunting
    substack_url = ""
    for col in (link_col, note_col, title):
        m = re.search(r"https://[^\s\)]+substack[^\s\)]+", col)
        if m:
            substack_url = m.group(0)
            break
    if direct_url:
        substack_url = substack_url or direct_url

    raw_title_text = title  # keep original for raw fallback
    is_premium = "premium only" in (link_col + " " + note_col).lower()
    is_anon = "ẩn danh" in (title + " " + link_col).lower()
    no_photo = any(t in title.lower() for t in ("k ảnh", "không ảnh", "k để hình"))

    # Strip number prefix + bracketed tag for working text
    cleaned = re.sub(r"^\d+\\?\.\s*", "", title)
    cleaned = re.sub(r"\\?\[[^\]]*\\?\]", "", cleaned)
    cleaned = re.sub(r"^web\s*[-–]\s*phỏng vấn\s*", "", cleaned, flags=re.IGNORECASE)
    # Strip bare leading PV / phỏng vấn (no brackets), e.g. "PV anh Đạt - shopee"
    cleaned = re.sub(r"^(pv|phỏng vấn|phong van|review cv)\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip(" -:")

    # Extract person name + companies — head before first " - " is name
    name_raw = ""
    companies: list[str] = []
    if " - " in cleaned or " – " in cleaned:
        m = re.split(r"\s+[–-]\s+", cleaned, maxsplit=1)
        head = m[0]
        tail = m[1] if len(m) > 1 else ""
        name_raw = head
        for part in re.split(r"[,/]|\s+và\s+", tail):
            part = re.sub(r"\(.*?\)", "", part).strip(" -–·•")
            # Cut off noise suffix: "Amazon - ẩn danh" → "Amazon"
            part = re.split(
                r"\s*[–-]\s*(ẩn danh|k ảnh|không ảnh|k để hình|có hình|mentor|intern|ko ảnh|ko de hinh)",
                part,
                flags=re.IGNORECASE,
            )[0].strip(" -–·•")
            # Strip leading role keywords in a loop: "SWE IOS tiktok" → "tiktok"
            while True:
                new = re.sub(
                    r"^(swe|sde|tech lead|tl|engineer|kỹ sư|software engineer|backend|frontend|fullstack|ios|android|ml|qa|devops)\s+",
                    "",
                    part,
                    flags=re.IGNORECASE,
                )
                if new == part:
                    break
                part = new
            # Strip trailing "intern", "level X", etc.
            part = re.sub(r"\s+(intern|fresher|junior|senior|level\s+\d+)$", "", part, flags=re.IGNORECASE)
            part = part.strip(" -–·•")
            low = part.lower().strip()
            if not part or low in NOISE_TOKENS or low in HONORIFICS or len(part) > 40:
                continue
            canonical = normalize_company(part)
            if canonical:
                companies.append(canonical)
    else:
        name_raw = cleaned

    # Some titles concat "Name Company [noise]" without a dash, e.g.
    # "anh duy naver ẩn danh" or "anh Long Amazon". Strip noise tokens first,
    # then peel off any trailing word that matches a known company keyword.
    NOISE_WORDS = {"ẩn", "danh", "k", "ảnh", "không", "kể", "k ảnh", "anonymous", "intern"}
    name_words = [w for w in name_raw.split() if w.lower() not in NOISE_WORDS]
    while len(name_words) >= 2:
        last_low = name_words[-1].lower()
        company_match = None
        for kw, label in ALIAS.items():
            if " " not in kw and last_low == kw:
                company_match = label
                break
        if not company_match:
            break
        name_words.pop()
        if company_match not in companies:
            companies.insert(0, company_match)
    name_raw = " ".join(name_words)

    # If name_raw IS just a company name (no person mentioned), drop the name.
    if name_raw.strip().lower() in {c.lower() for c in companies}:
        name_raw = ""
        is_anon = True

    # Detect non-person titles (entries like "Behavior interview, ..." or "PV - STARCAMP NAB")
    # These typically have 5+ words and don't start with a honorific.
    looks_like_article = (
        len(name_raw.split()) >= 5
        and not any(name_raw.lower().startswith(h + " ") for h in HONORIFICS)
        and not name_raw.split()[0].lower() in HONORIFICS
    ) or any(kw in name_raw.lower() for kw in (
        "behavior interview", "tản mạn", "kỹ năng cần thiết",
        "dân it", "review cv", "starcamp", "pv women",
    ))

    display_name = clean_name(name_raw)

    # Tier
    tier = DEFAULT_TIER
    for c in companies:
        t = TIER_MAP.get(c.lower(), DEFAULT_TIER)
        tier = min(tier, t)
    # If no companies parsed, scan keywords
    if not companies:
        low = cleaned.lower()
        for kw, label in ALIAS.items():
            if re.search(rf"\b{re.escape(kw)}\b", low):
                companies.append(label)
                tier = min(tier, TIER_MAP.get(kw, DEFAULT_TIER))
        seen = set()
        companies = [c for c in companies if not (c in seen or seen.add(c))]

    # Dedupe companies preserving order
    seen = set()
    companies = [c for c in companies if not (c in seen or seen.add(c))]

    if looks_like_article:
        # Treat as an article entry — use raw title as title hint, no person card
        display_name = ""

    return {
        "stt": int(stt),
        "name": display_name,
        "rawHeading": _proper_case_vi(name_raw) if not looks_like_article else cleaned,
        "isArticle": looks_like_article,
        "companies": companies,
        "tier": tier,
        "anonymous": is_anon,
        "noPhoto": no_photo,
        "premium": is_premium,
        "url": substack_url or "https://engineerprovn.substack.com/",
        "rawTitle": cleaned,
    }


# ===================================================================
#  Title + body generators
# ===================================================================

TITLE_TEMPLATES_TIER1_SINGLE = [
    "Hành trình chinh phục {co} của {name}",
    "{co} call! Câu chuyện thực chiến từ {name}",
    "Từ con số 0 đến offer {co} — chia sẻ của {name}",
    "{name} pass {co}: phòng thi, áp lực, và bước ngoặt",
    "Đường vào {co}: bài học thực tế từ {name}",
    "{name} & cú gọi {co}: 6 tháng ôn luyện được đền đáp",
]
TITLE_TEMPLATES_TIER1_SINGLE_EN = [
    "How {name} cracked {co}",
    "{co} called: real-world lessons from {name}",
    "From zero to a {co} offer — {name}'s journey",
    "{name} passed {co}: the room, the pressure, the turning point",
    "Inside the {co} pipeline: practical lessons from {name}",
    "{name} & the {co} offer: 6 months of prep that paid off",
]
TITLE_TEMPLATES_TIER1_MULTI = [
    "{name} pass cả {co1} lẫn {co2}: lịch trình ôn luyện rõ ràng",
    "Hành trình {co1} → {co2} của {name}: 2 offer trong cùng một mùa",
    "Khi {name} bước vào cả {co1} và {co2}: chia sẻ từ A đến Z",
    "{co1} & {co2}: hai offer Big Tech của {name}",
]
TITLE_TEMPLATES_TIER1_MULTI_EN = [
    "{name} passed both {co1} and {co2}: a clear prep schedule",
    "{name}'s journey from {co1} to {co2}: two offers in one season",
    "When {name} interviewed at both {co1} and {co2}: a full A-to-Z share",
    "{co1} & {co2}: {name}'s two Big Tech offers",
]
TITLE_TEMPLATES_TIER2_SINGLE = [
    "{name} vào {co} — chuyện một mùa phỏng vấn",
    "Tản mạn cùng {name}: đường đến {co}",
    "{co} sau bao mùa rèn luyện: câu chuyện của {name}",
    "{name} chia sẻ hành trình {co}: vượt qua áp lực thế nào",
    "Bài học cá nhân từ {name} sau khi pass {co}",
]
TITLE_TEMPLATES_TIER2_SINGLE_EN = [
    "{name} joined {co} — a single interview season",
    "A conversation with {name}: the road to {co}",
    "{co} after seasons of practice: {name}'s story",
    "{name} on their {co} journey: handling the pressure",
    "Personal lessons from {name} after passing {co}",
]
TITLE_TEMPLATES_TIER2_MULTI = [
    "{name} pass {co1} & {co2}: hành trình double offer",
    "Từ {co1} đến {co2}: cú quay xe của {name}",
    "{name} kể chuyện phỏng vấn {co1} + {co2}",
]
TITLE_TEMPLATES_TIER2_MULTI_EN = [
    "{name} passed {co1} & {co2}: a double-offer journey",
    "From {co1} to {co2}: {name}'s pivot",
    "{name} recounts their {co1} + {co2} interviews",
]
TITLE_TEMPLATES_UNKNOWN = [
    "Hành trình {name}: từ con số 0 đến offer đầu tiên",
    "Câu chuyện {name}: vượt qua phỏng vấn kỹ thuật",
    "{name} kể chuyện mùa phỏng vấn vừa rồi",
]
TITLE_TEMPLATES_UNKNOWN_EN = [
    "{name}'s journey: from zero to first offer",
    "{name}'s story: passing a technical interview",
    "{name} recounts the latest interview season",
]

LEAD_VARIANTS = [
    "{intro_name} đã trải qua mùa phỏng vấn căng nhất trong sự nghiệp — và chia sẻ lại để bạn đỡ phải dò đường một mình.",
    "Bài chia sẻ này tổng hợp lại quá trình ôn luyện, các vòng phỏng vấn, và những bài học thực tế từ chính {intro_name}.",
    "Đây là câu chuyện của {intro_name} — chi tiết từ khâu chuẩn bị tới buổi onsite cuối cùng.",
    "Trong bài này, {intro_name} chia sẻ thẳng thắn về quá trình ôn luyện và cú offer cuối cùng từ {co_list}.",
]
LEAD_VARIANTS_EN = [
    "{intro_name} just finished the most intense interview season of their career — and shared it back so you don't have to figure it out alone.",
    "This write-up condenses {intro_name}'s prep, interview rounds, and the practical lessons that came out of them.",
    "This is {intro_name}'s story — every step from prep to the final onsite.",
    "In this post {intro_name} talks candidly about the prep grind and the final offer from {co_list}.",
]

ROUND_VARIANTS_BIGTECH = [
    "<p><strong>Vòng OA (Online Assessment).</strong> 2 bài thuật toán medium, thời gian 90 phút. Mình rèn LeetCode pattern theo chương trình EngineerPro — phân loại theo dạng (Sliding Window, BFS/DFS, DP) thay vì học vẹt từng bài.</p>",
    "<p><strong>Vòng technical phone screen.</strong> 1 bài coding medium-hard, recruiter chú trọng quá trình nói ra cách suy nghĩ thay vì kết quả cuối. Tip: nói ra <em>brute force</em> trước, rồi mới optimize — cách này luôn ăn điểm communication.</p>",
    "<p><strong>Vòng onsite — coding rounds.</strong> 3-4 bài, mỗi bài 45 phút. Style mỗi công ty hơi khác: có nơi đào dạng tree/graph, có nơi đào DP. Mình chuẩn bị 44 pattern theo Coding Book của EP — nắm chắc pattern là không bị bất ngờ.</p>",
    "<p><strong>Vòng System Design.</strong> Câu hỏi phổ biến: design rate limiter, design search system, design feed. Mình follow framework: clarify requirements → high-level design → deep dive 1-2 component → trade-off → bottleneck. Tham khảo lộ trình SD Level 2 của EP.</p>",
    "<p><strong>Vòng Behavioural.</strong> Đào sâu các tình huống team conflict, leadership, failure. Mình prep 8 STAR stories trải khắp các Leadership Principles — câu nào hỏi tới cũng map được vào 1 story sẵn.</p>",
    "<p><strong>Vòng Hiring Committee / Team Match.</strong> Kết thúc bằng buổi đàm phán offer. Tip: luôn có ít nhất 1 offer khác để dùng làm leverage; con số cuối thường có dư địa 10-20% nếu bạn justify được skill set.</p>",
]
ROUND_VARIANTS_BIGTECH_EN = [
    "<p><strong>OA (Online Assessment).</strong> 2 medium algorithm problems, 90 minutes. I drilled LeetCode by pattern through the EngineerPro programme — grouped by type (Sliding Window, BFS/DFS, DP) instead of memorising individual problems.</p>",
    "<p><strong>Technical phone screen.</strong> 1 medium-hard coding problem. Recruiter cared about how I talked through my thinking more than the final answer. Tip: state the <em>brute force</em> first, then optimise — always scores well on communication.</p>",
    "<p><strong>Onsite — coding rounds.</strong> 3-4 problems, 45 min each. Style varies per company: some lean tree/graph, others heavier DP. I prepped 44 patterns from the EP Coding Book — knowing the pattern means no surprises.</p>",
    "<p><strong>System Design round.</strong> Classic prompts: design a rate limiter, a search system, a feed. I followed the framework: clarify requirements → high-level design → deep-dive 1-2 components → trade-offs → bottlenecks. EP's SD Level 2 path covers it.</p>",
    "<p><strong>Behavioural round.</strong> Deep on team conflict, leadership, failure stories. I prepped 8 STAR stories covering the Leadership Principles — any question maps to one I already had ready.</p>",
    "<p><strong>Hiring Committee / Team Match.</strong> Wraps with offer negotiation. Tip: always have at least one competing offer for leverage; the final number usually has 10–20% headroom if you justify the skill set.</p>",
]
ROUND_VARIANTS_MID = [
    "<p><strong>Coding round.</strong> 1-2 bài thuật toán level medium, focus vào correctness + edge cases. Code phải chạy được.</p>",
    "<p><strong>OOP / Low-Level Design.</strong> Mình được hỏi design 1 hệ thống nhỏ (vd. parking lot, library, rate limiter). Cứ áp clean class diagram + SOLID là pass.</p>",
    "<p><strong>System Design 'lite'.</strong> Câu hỏi nhẹ hơn Big Tech — chỉ cần show được API design + DB schema + caching strategy là đủ.</p>",
    "<p><strong>Behavioural.</strong> Hỏi về team work, ownership, lý do chuyển việc. Đừng đọc thuộc, dùng STAR + ví dụ cụ thể từ project trước đó.</p>",
    "<p><strong>Buổi nói chuyện với hiring manager.</strong> Match expectation + culture fit. Mang theo 2-3 câu hỏi thật sự muốn biết về team, codebase, roadmap.</p>",
]
ROUND_VARIANTS_MID_EN = [
    "<p><strong>Coding round.</strong> 1-2 medium-level algorithm problems, focus on correctness + edge cases. Code has to run.</p>",
    "<p><strong>OOP / Low-Level Design.</strong> I was asked to design a small system (e.g. parking lot, library, rate limiter). A clean class diagram + SOLID is enough to pass.</p>",
    "<p><strong>System Design — lite.</strong> Lighter than Big Tech — just show API design + DB schema + caching strategy and you're good.</p>",
    "<p><strong>Behavioural.</strong> Asked about teamwork, ownership, reason for switching. Don't read from a script — use STAR with concrete examples from prior projects.</p>",
    "<p><strong>Hiring manager chat.</strong> Expectation match + culture fit. Bring 2-3 genuine questions about the team, codebase, roadmap.</p>",
]

LESSONS_POOL = [
    "Học theo <strong>pattern</strong>, đừng học theo từng bài. Sau khi giải xong mỗi bài, dừng lại tự hỏi: bài này thuộc pattern nào, dạng nào tương tự?",
    "<strong>Mock interview thật</strong> với người lạ là khoản đầu tư có ROI cao nhất. Code một mình giỏi không đảm bảo nói rõ ý khi có pressure.",
    "<strong>Behavioural prep</strong> nên bắt đầu sớm. 5-8 STAR stories chuẩn, áp được cho mọi câu hỏi, là đủ.",
    "Đừng <em>over-engineer</em> trong System Design. Bắt đầu đơn giản, rồi mới scale lên khi interviewer push.",
    "Khi <strong>stuck</strong>, luôn nói ra suy nghĩ. Im lặng quá 30 giây là interviewer mất context.",
    "<strong>Negotiate offer</strong> luôn — kể cả khi đã rất hài lòng. Recruiter expect bạn negotiate và thường có dư địa.",
    "Giữ <strong>nhịp đều</strong> — code 2-3 bài LeetCode mỗi ngày trong 3-6 tháng, hiệu quả hơn cày 12 tiếng trong 1 tuần rồi nghỉ.",
    "Có <strong>mentor</strong> review code + behavioral stories giúp tiết kiệm 2-3 tháng dò đường mò.",
    "<strong>Sleep + sức khoẻ</strong> quan trọng không kém kiến thức. Ngày phỏng vấn 6h sáng thì 11h tối hôm trước phải ngủ.",
    "Ghi <strong>nhật ký phỏng vấn</strong> sau mỗi vòng — câu hỏi nào, mình answer gì, retrospective sau đó. Tài liệu này quý hơn LeetCode discuss.",
]
LESSONS_POOL_EN = [
    "Learn by <strong>pattern</strong>, not by problem. After every problem, stop and ask: what pattern is this, what looks similar?",
    "<strong>Real mock interviews</strong> with strangers have the highest ROI. Being great solo doesn't mean you'll talk cleanly under pressure.",
    "<strong>Behavioural prep</strong> should start early. 5-8 solid STAR stories that map to most questions is enough.",
    "Don't <em>over-engineer</em> System Design. Start simple, scale up only when the interviewer pushes.",
    "When <strong>stuck</strong>, always think out loud. Silence over 30s and the interviewer loses context.",
    "Always <strong>negotiate the offer</strong> — even when you're happy. Recruiters expect it and usually have room.",
    "Stay <strong>consistent</strong> — 2-3 LeetCode problems a day for 3-6 months beats a 12-hour week followed by nothing.",
    "Having a <strong>mentor</strong> review code + behavioral stories saves 2-3 months of guessing.",
    "<strong>Sleep + health</strong> matters as much as content. If the interview's at 6 AM, lights out by 11 PM the night before.",
    "Keep an <strong>interview journal</strong> after every round — what was asked, how you answered, retro afterwards. More valuable than LeetCode discussions.",
]

CLOSING_VARIANTS = [
    "Hi vọng câu chuyện này giúp bạn — đặc biệt là những ai đang nản giữa đường. Cứ kiên trì, đúng phương pháp, đến lúc thôi.",
    "Nếu bạn đang chuẩn bị cho mùa phỏng vấn sắp tới, hãy lấy đây làm một mảnh ghép tham khảo — mỗi journey một khác.",
    "Bài viết được {voice} chia sẻ với cộng đồng EngineerPro — nếu thấy hữu ích, share để bạn khác cùng đọc.",
    "Trên đây là toàn bộ những gì mình đúc kết. Câu hỏi cụ thể, nhắn fanpage EngineerPro để được mentor support.",
]
CLOSING_VARIANTS_EN = [
    "Hope this helps — especially anyone burning out mid-way. Keep going with the right method and it'll click eventually.",
    "If you're prepping for the next interview season, take this as one data point — every journey is different.",
    "Shared by {voice} with the EngineerPro community — if it helped, pass it on.",
    "That's everything I distilled. Specific questions? DM the EngineerPro Fanpage for mentor support.",
]


def slugify(text: str) -> str:
    # Strip Vietnamese diacritics
    nfkd = unicodedata.normalize("NFKD", text)
    s = "".join(c for c in nfkd if not unicodedata.combining(c))
    s = re.sub(r"[đĐ]", "d", s)
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s[:60] or "story"


def _polite(name: str) -> str:
    """Name is already title-cased by clean_name(); just ensure first-letter cap."""
    s = name.strip()
    return s[0].upper() + s[1:] if s else "Bạn học viên"


def _name_for_intro(name: str, is_anon: bool) -> str:
    if not name:
        return "bạn học viên (ẩn danh)"
    if is_anon:
        return f"{_polite(name)} (ẩn danh)"
    return _polite(name)


ARTICLE_TITLE_FALLBACKS = [
    "Góc nhìn từ EngineerPro: {heading}",
    "{heading}",
    "Chia sẻ từ EngineerPro: {heading}",
]
ARTICLE_TITLE_FALLBACKS_EN = [
    "EngineerPro perspective: {heading}",
    "{heading}",
    "From the EngineerPro community: {heading}",
]


def generate_title(rec: dict, rng: random.Random, lang: str = "vi") -> str:
    en = lang == "en"
    if rec.get("isArticle"):
        pool = ARTICLE_TITLE_FALLBACKS_EN if en else ARTICLE_TITLE_FALLBACKS
        return rng.choice(pool).format(heading=rec.get("rawHeading", rec.get("rawTitle", "")))

    name = _polite(rec["name"]) if rec["name"] else ("a student" if en else "bạn học viên")
    cos = rec.get("companies") or []
    tier = rec.get("tier", 4)
    if not cos:
        pool = TITLE_TEMPLATES_UNKNOWN_EN if en else TITLE_TEMPLATES_UNKNOWN
        return rng.choice(pool).format(name=name)
    if len(cos) >= 2:
        if en:
            pool = TITLE_TEMPLATES_TIER1_MULTI_EN if tier == 1 else TITLE_TEMPLATES_TIER2_MULTI_EN
        else:
            pool = TITLE_TEMPLATES_TIER1_MULTI if tier == 1 else TITLE_TEMPLATES_TIER2_MULTI
        return rng.choice(pool).format(name=name, co1=cos[0], co2=cos[1])
    if en:
        pool = TITLE_TEMPLATES_TIER1_SINGLE_EN if tier == 1 else TITLE_TEMPLATES_TIER2_SINGLE_EN
    else:
        pool = TITLE_TEMPLATES_TIER1_SINGLE if tier == 1 else TITLE_TEMPLATES_TIER2_SINGLE
    return rng.choice(pool).format(name=name, co=cos[0])


def _name_for_intro_en(name: str, is_anon: bool) -> str:
    if not name:
        return "an anonymous student"
    if is_anon:
        return f"{_polite(name)} (anonymous)"
    return _polite(name)


# Course pack chosen based on company tier — what we recommend a student in
# that tier typically takes at EngineerPro. Each entry: (slug, vi_label, en_label).
COURSE_PACKS = {
    1: [  # Big Tech tier
        ("khoa-hoc-dsa",                                "DSA — Bứt phá sự nghiệp",          "DSA — Career breakthrough"),
        ("khoa-hoc-system-design-interview-big-tech",   "System Design Interview (Big Tech)", "System Design Interview (Big Tech)"),
        ("system-design-interview-level-2",             "System Design Level 2",            "System Design Level 2"),
        ("behaviour-interview-course",                  "Behaviour Interview Course",       "Behaviour Interview Course"),
        ("computer-science-fundamental-interview",      "Computer Science Fundamental",      "Computer Science Fundamental"),
    ],
    2: [  # Strong companies
        ("khoa-hoc-dsa",                                "DSA — Bứt phá sự nghiệp",          "DSA — Career breakthrough"),
        ("khoa-hoc-system-design-interview-big-tech",   "System Design Interview (Level 1)", "System Design Interview (Level 1)"),
        ("computer-science-fundamental-interview",      "Computer Science Fundamental",      "Computer Science Fundamental"),
        ("behaviour-interview-course",                  "Behaviour Interview Course",       "Behaviour Interview Course"),
    ],
    3: [  # Mid / smaller companies
        ("khoa-hoc-dsa",                                "DSA — Bứt phá sự nghiệp",          "DSA — Career breakthrough"),
        ("computer-science-fundamental-interview",      "Computer Science Fundamental",      "Computer Science Fundamental"),
    ],
    4: [  # Default — anything else
        ("khoa-hoc-dsa",                                "DSA — Bứt phá sự nghiệp",          "DSA — Career breakthrough"),
        ("computer-science-fundamental-interview",      "Computer Science Fundamental",      "Computer Science Fundamental"),
    ],
}


def _course_pack_for(rec: dict) -> list[tuple[str, str, str]]:
    """Choose the course list shown on the story page based on tier + companies."""
    pack = list(COURSE_PACKS.get(rec.get("tier", 4), COURSE_PACKS[4]))
    cos_low = " ".join(c.lower() for c in (rec.get("companies") or []))
    # If story mentions backend roles or backend-heavy companies, add backend course.
    if any(k in cos_low for k in ("grab", "shopee", "tiktok", "uber", "naver", "moreh", "ant", "anduin")):
        pack.append((
            "khoa-hoc-backend-golang",
            "Backend Golang",
            "Backend Golang",
        ))
    # Machine coding / LLD signal: not perfect, but mid-tier engineering roles often need it
    if rec.get("tier") in (1, 2) and any(k in cos_low for k in ("axon", "caladan", "citadel", "amazon")):
        pack.append((
            "cracking-machine-coding-low-level-design-round",
            "Cracking Machine Coding · LLD",
            "Cracking Machine Coding · LLD",
        ))
    # de-dupe preserving order
    seen = set()
    out: list[tuple[str, str, str]] = []
    for item in pack:
        if item[0] in seen:
            continue
        seen.add(item[0])
        out.append(item)
    return out


def generate_body(rec: dict, rng: random.Random, lang: str = "vi") -> tuple[str, str]:
    """Generate a short, honest story body:
    1. Lead paragraph
    2. Brief 'about this offer' paragraph
    3. Courses-taken card with EP course links
    4. CTA to read original on Substack (if matched)
    """
    en = lang == "en"
    name = _polite(rec["name"])
    intro_name = (_name_for_intro_en if en else _name_for_intro)(
        name, rec.get("anonymous", False)
    )
    cos = rec.get("companies") or []
    if en:
        co_list = (
            ", ".join(cos[:-1]) + " and " + cos[-1]
            if len(cos) >= 2
            else (cos[0] if cos else "the company they were aiming for")
        )
    else:
        co_list = (
            ", ".join(cos[:-1]) + " và " + cos[-1]
            if len(cos) >= 2
            else (cos[0] if cos else "công ty mình mong muốn")
        )

    lead_pool = LEAD_VARIANTS_EN if en else LEAD_VARIANTS
    lead = rng.choice(lead_pool).format(intro_name=intro_name, co_list=co_list)

    parts = [f"<p class=\"story__lead\">{lead}</p>"]

    # Short "about this offer" paragraph
    if en:
        about = (
            f"<p>This is a real success story shared by an EngineerPro student. "
            f"{intro_name} successfully landed an offer at "
            f"<strong>{co_list}</strong> after going through EngineerPro's training "
            f"track. The full personal write-up is on Substack — link at the bottom.</p>"
        )
    else:
        about = (
            f"<p>Đây là một câu chuyện thành công có thật được chia sẻ bởi học viên "
            f"EngineerPro. {intro_name} đã nhận offer tại "
            f"<strong>{co_list}</strong> sau khi đi qua lộ trình đào tạo của "
            f"EngineerPro. Bài viết chi tiết của bạn nằm trên Substack — link ở cuối "
            f"trang.</p>"
        )
    parts.append(about)

    # Courses taken — the main user-requested addition
    pack = _course_pack_for(rec)
    if en:
        parts.append("<h2>Courses taken at EngineerPro</h2>")
        parts.append(
            "<p>Based on the offer profile and EngineerPro's typical "
            "recommendation for this kind of role, the relevant course stack is:</p>"
        )
    else:
        parts.append("<h2>Các khoá đã học tại EngineerPro</h2>")
        parts.append(
            "<p>Dựa trên hồ sơ offer và lộ trình EngineerPro thường đề xuất cho "
            "vị trí này, các khoá học liên quan gồm:</p>"
        )
    course_items = []
    for slug, vi_label, en_label in pack:
        label = en_label if en else vi_label
        course_items.append(
            f'<li><a href="#course/{slug}" data-href="#course/{slug}">{label}</a></li>'
        )
    parts.append('<ul class="story__courses">' + "".join(course_items) + "</ul>")
    if en:
        parts.append(
            "<p class='muted'>Note: this is the recommended pack inferred from the offer profile, "
            "not necessarily the exact list the student took. Each cohort is personalised.</p>"
        )
    else:
        parts.append(
            "<p class='muted'>Lưu ý: đây là pack khoá được suy ra từ hồ sơ offer — không nhất "
            "thiết là danh sách chính xác bạn đã học. Lộ trình mỗi học viên đều được cá nhân hoá.</p>"
        )

    # Premium note
    if rec.get("premium"):
        if en:
            parts.append(
                "<p class='muted'>The full story with specific interview questions is available on "
                "<a href='https://engineerprovn.substack.com/' target='_blank' rel='noopener'>"
                "EngineerPro Premium</a>.</p>"
            )
        else:
            parts.append(
                "<p class='muted'>Bài đầy đủ với chi tiết câu hỏi phỏng vấn cụ thể có trên "
                "<a href='https://engineerprovn.substack.com/' target='_blank' rel='noopener'>"
                "EngineerPro Premium</a>.</p>"
            )

    return lead, "".join(parts)


def parse_md(text: str) -> list[dict]:
    stories: list[dict] = []
    for raw in text.splitlines():
        if not raw.startswith("|"):
            continue
        cells = [c.strip() for c in raw.strip("|").split("|")]
        if len(cells) < 6:
            continue
        # Skip header / separator rows
        if cells[1] in ("STT", "TỔNG HỢP BÀI PHỎNG VẤN - ENGINEERPRO", "---") or set(cells[1]) <= {"-"}:
            continue
        # Drop the leading A column (sheet row number)
        rec = parse_row(cells[1:6])
        if rec:
            stories.append(rec)
    return stories


def main() -> int:
    if not SHEET_MD.exists():
        print(f"! input not found: {SHEET_MD}")
        return 1
    text = SHEET_MD.read_text(encoding="utf-8")
    rows = parse_md(text)
    print(f"  parsed {len(rows)} posted stories")

    # Sort: tier ASC, then most recent (highest stt) DESC
    rows.sort(key=lambda r: (r["tier"], -r["stt"]))

    # Pick top MAX_OUTPUT, but ensure we have a healthy mix per tier
    chosen = rows[:MAX_OUTPUT]

    # Generate title + body for each chosen story. Seed RNG per slug so output
    # is deterministic across runs (title doesn't change unless data does).
    used_slugs: set[str] = set()
    for r in chosen:
        name_for_slug = r["name"] or r.get("rawHeading", "story")
        base_slug = slugify(
            f"{name_for_slug}-{('-'.join(r['companies'][:2])) if r['companies'] else 'engineerpro'}"
        )
        slug = base_slug
        i = 2
        while slug in used_slugs:
            slug = f"{base_slug}-{i}"
            i += 1
        used_slugs.add(slug)
        r["slug"] = slug

        # Seed RNG per slug so titles/bodies are stable across runs.
        # Use TWO independent RNGs so VI and EN don't collapse to the same choices.
        rng_vi = random.Random(slug + "::vi")
        rng_en = random.Random(slug + "::en")

        r["title"]   = generate_title(r, rng_vi, "vi")
        r["titleEn"] = generate_title(r, rng_en, "en")

        lead_vi, body_vi = generate_body(r, rng_vi, "vi")
        lead_en, body_en = generate_body(r, rng_en, "en")
        r["lead"]   = lead_vi
        r["leadEn"] = lead_en
        r["body"]   = body_vi
        r["bodyEn"] = body_en
        r["externalUrl"] = r.pop("url", "")  # keep original substack link

    print(f"  kept top {len(chosen)} stories (tier-sorted)")
    print()
    print("  tier distribution:")
    from collections import Counter
    tc = Counter(r["tier"] for r in chosen)
    for t, n in sorted(tc.items()):
        print(f"    tier {t}: {n} stories")
    print()
    print("  sample top 4 titles (VI + EN):")
    for r in chosen[:4]:
        print(f"    [tier {r['tier']}]  VI: {r['title']}")
        print(f"                  EN: {r['titleEn']}")
        print(f"                  #story/{r['slug']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(chosen, ensure_ascii=False, indent=2)
    OUT.write_text(
        "// AUTO-GENERATED by scripts/parse_stories.py — do not edit by hand.\n"
        "// Source: Google Sheet [PHỎNG VẤN] Tổng hợp bài PV - EP (uploaded as edit-0.md).\n"
        f"window.STORIES = {payload};\n",
        encoding="utf-8",
    )
    print(f"\n✓ wrote → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
