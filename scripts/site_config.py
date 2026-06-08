"""Single source of truth for site-wide build config.

Override at deploy time:

    # Root deploy (custom domain or user/org pages):
    EP_BASE_URL=https://engineerpro.com make github

    # GitHub Pages project subpath (default for repo-name.github.io/repo/):
    EP_BASE_URL=https://engineerpro-team.github.io \
    EP_BASE_PATH=/interview-trainings \
    make github

All build scripts (make_seo.py, build_pages.py) read these from here.
"""
import os

# Origin only — no trailing slash. e.g. "https://engineerprogurus.com"
BASE_URL: str = os.environ.get("EP_BASE_URL", "https://engineerprogurus.com").rstrip("/")

# Subpath prefix (with leading slash, no trailing slash) — empty string for root
# / custom-domain deploys, "/interview-trainings" for the bare github.io
# project Pages URL.
_raw_path = os.environ.get("EP_BASE_PATH", "").strip()
if _raw_path and not _raw_path.startswith("/"):
    _raw_path = "/" + _raw_path
BASE_PATH: str = _raw_path.rstrip("/")

# Full canonical URL prefix (origin + subpath, no trailing slash) — what every
# loc/canonical/og:url uses.
SITE_BASE: str = BASE_URL + BASE_PATH

SITE_NAME: str = "EngineerPro"
SITE_TAGLINE_VI: str = "Chinh phục Big Tech cùng mentor thực chiến"
SITE_TAGLINE_EN: str = "Conquering Big Tech with battle-tested mentors"

# Single share image for every prerendered page (override per-route in
# build_pages.py if you want a richer card per page).
OG_IMAGE: str = "/assets/img/og-share.png"

# Public URL segment for System Design material tab (SPA route id stays "system-design").
SYSTEM_DESIGN_URL_SLUG: str = "system-design-material"

# Routes that should be prerendered as real paths (besides home which is "/").
# Order also drives navigation in the prerendered <noscript> fallback.
TOP_ROUTES = [
    ("courses",   "Khoá học",          "Courses"),
    ("book",          "Coding Book",       "Coding Book"),
    (SYSTEM_DESIGN_URL_SLUG, "System design material", "System design material"),
    ("mock",          "Mock Interview 1-1", "Mock Interview 1-1"),
    ("resources", "Interview Resources", "Interview Resources"),
    ("mentors",   "Giảng viên",        "Mentors"),
    ("stories",   "Success Stories",   "Success Stories"),
    ("podcast",   "Podcast",           "Podcast"),
    ("partners",  "Đối tác",           "Partners"),
    ("faq",       "Câu hỏi thường gặp", "FAQ"),
    ("terms",     "Điều khoản dịch vụ", "Terms of Service"),
    ("contact",   "Liên hệ",           "Contact"),
]

# Deep-link sub-sections under /resources/ (prerendered + sitemap).
RESOURCES_ALIASES: dict[str, tuple[str, str]] = {
    "hr-screen":      ("HR Phone Screen Checklist · ", "Checklist chuẩn bị HR/recruiter call — self-intro, STAR, project depth, motivation. Gợi ý khóa Behaviour Interview."),
    "pip-big-tech":   ("PIP at Big Tech · ", "Guide xử lý PIP — Axon, Grab, TikTok, Shopee, Nvidia, Google, Amazon… Thoát PIP khó; ưu tiên negotiate mutual severance N+1, N+2."),
    "cs-fundamental": ("CS Fundamental Interview Questions · ", "~100 câu hỏi CS Fundamentals từ LeetCode Discuss + khóa live CS Fundamental Interview (12 buổi qua Zoom)."),
    "interview-formats": ("Interview Format by Company · ", "Format phỏng vấn tham khảo — Amazon, Google, Meta, Grab, Axon, Shopee, TikTok, Nvidia… EngineerPro cheatsheet V2."),
    "foundation":     ("Programming Foundation · ", "16 video nền tảng lập trình free (C++ / Java / Golang / Python) từ EngineerPro."),
    "golang-tour":    ("Golang Tour · ", "3 video free học Golang cơ bản cùng Senior SWE tại Shopee Singapore."),
    "cv-kit":         ("Viết CV chuẩn Big Tech · ", "Bộ tài liệu viết CV chuẩn Big Tech — CV mẫu đã pass Google, template LaTeX, playlist review CV."),
}
