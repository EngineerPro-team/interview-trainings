"""Single source of truth for site-wide build config.

Override the deploy URL once before launch:

    EP_BASE_URL=https://engineerpro.com make github

All build scripts (make_seo.py, build_pages.py) read BASE_URL from here.
"""
import os

# Trailing slash is *not* included — scripts append paths explicitly.
BASE_URL: str = os.environ.get("EP_BASE_URL", "https://engineerpro-academy.github.io").rstrip("/")

SITE_NAME: str = "EngineerPro"
SITE_TAGLINE_VI: str = "Chinh phục Big Tech cùng mentor thực chiến"
SITE_TAGLINE_EN: str = "Conquering Big Tech with battle-tested mentors"

# Single share image for every prerendered page (override per-route in
# build_pages.py if you want a richer card per page).
OG_IMAGE: str = "/assets/img/og-share.png"

# Routes that should be prerendered as real paths (besides home which is "/").
# Order also drives navigation in the prerendered <noscript> fallback.
TOP_ROUTES = [
    ("courses",   "Khoá học",          "Courses"),
    ("book",      "Coding Book",       "Coding Book"),
    ("resources", "Interview Resources", "Interview Resources"),
    ("mentors",   "Giảng viên",        "Mentors"),
    ("stories",   "Success Stories",   "Success Stories"),
    ("podcast",   "Podcast",           "Podcast"),
    ("partners",  "Đối tác",           "Partners"),
    ("faq",       "Câu hỏi thường gặp", "FAQ"),
    ("contact",   "Liên hệ",           "Contact"),
]
