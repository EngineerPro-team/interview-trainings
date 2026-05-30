#!/usr/bin/env python3
"""
Crawl YouTube playlist + oEmbed data for the Interview Resources tab.

Output: src/assets/resources-data.js
        window.RESOURCES = { foundation: {...}, cv: {...} }

Re-run:  python3.11 scripts/crawl_resources.py
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "assets" / "resources-data.js"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.5 Safari/605.1.15"
)

PLAYLISTS = {
    "foundation": {
        "id": "PLy5vBFMmXuxdeF5Bg9E1sfZWPMIplA_aC",
        "title": "Programming Foundation",
        "subtitle": "16 video nền tảng lập trình (C++ · Java · Golang · Python)",
        "description": (
            "Series free 16 video do EngineerPro thực hiện — cover từ Introduction, "
            "Conditional, Loop, Function, Array, String, Class, Recursion, Sorting, "
            "Linked List, HashMap/HashSet, Tree đến Graph. Mỗi video song ngữ "
            "4 ngôn ngữ phổ biến: C++, Java, Golang, Python."
        ),
    },
    "cv_review": {
        "id": "PLy5vBFMmXuxeSmllX7VZHm_N1ryWbbtM6",
        "title": "Review CV",
        "subtitle": "Mentors Big Tech review CV thật của học viên",
        "description": (
            "Series 50+ tập do mentor EngineerPro review CV của học viên — "
            "chỉ ra các lỗi phổ biến, cách phrasing impact, cách layout hợp lý. "
            "Tham khảo để né lỗi & viết CV chuẩn Big Tech."
        ),
    },
}

CV_TOOL_VIDEO_ID = "qeRpppuEz6c"
OVERLEAF_URL = (
    "https://www.overleaf.com/latex/templates/software-engineer-resume/gqxmqsvsbdjf"
)
SAMPLE_CV_DRIVE_ID = "1CThTmY7j50mpbQuK3qfV6DJmpCJNMMgb"
SAMPLE_CV_LABEL = "EngineerPro-GooglePass-CV.png"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def _walk(obj, key, depth=0):
    if depth > 20:
        return
    if isinstance(obj, dict):
        if key in obj and isinstance(obj[key], list):
            yield obj[key]
        for v in obj.values():
            yield from _walk(v, key, depth + 1)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v, key, depth + 1)


def parse_playlist_videos(html: str) -> list[dict]:
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not m:
        return []
    data = json.loads(m.group(1))
    for lst in _walk(data, "contents"):
        if any(isinstance(it, dict) and "playlistVideoRenderer" in it for it in lst):
            out = []
            for it in lst:
                v = it.get("playlistVideoRenderer")
                if not v:
                    continue
                vid = v.get("videoId", "")
                title = (
                    v.get("title", {}).get("runs", [{}])[0].get("text", "")
                    or v.get("title", {}).get("simpleText", "")
                )
                dur = v.get("lengthText", {}).get("simpleText", "")
                out.append({
                    "videoId": vid,
                    "title": (title or "").strip(),
                    "duration": dur,
                    "thumbnail": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
                    "url": f"https://www.youtube.com/watch?v={vid}&list={PLAYLISTS_BY_VID.get(vid, '')}",
                })
            return out
    return []


PLAYLISTS_BY_VID: dict[str, str] = {}


def crawl_playlist(slug: str, info: dict) -> dict:
    print(f"  · {slug}: fetching playlist {info['id']} …")
    url = f"https://www.youtube.com/playlist?list={info['id']}"
    html = fetch(url)
    # First pass to know which playlist each vid belongs to (for URL building)
    raw = re.findall(r'"videoId":"([^"]+)"', html)
    for vid in raw:
        PLAYLISTS_BY_VID.setdefault(vid, info["id"])
    videos = parse_playlist_videos(html)
    # Patch the list URL with the correct playlist id for this slug
    for v in videos:
        v["url"] = f"https://www.youtube.com/watch?v={v['videoId']}&list={info['id']}"
        # Normalise the well-known typo in the foundation series.
        v["title"] = v["title"].replace("((", "(")
    # Sort by the lesson number embedded in titles like "... Foundation 12: ..."
    def lesson_key(v):
        m = re.search(r"\b(?:Foundation|Lesson|Episode|Tập|Phần)\s+(\d+)", v.get("title", ""), re.I)
        return int(m.group(1)) if m else 10_000
    videos.sort(key=lesson_key)
    print(f"    → {len(videos)} videos")
    return {
        "playlistId": info["id"],
        "title": info["title"],
        "subtitle": info["subtitle"],
        "description": info["description"],
        "url": f"https://www.youtube.com/playlist?list={info['id']}",
        "videos": videos,
    }


def crawl_single_video(vid: str) -> dict:
    print(f"  · single video {vid}: fetching oEmbed …")
    oe = fetch_json(
        f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    )
    return {
        "videoId": vid,
        "title": oe.get("title", ""),
        "author": oe.get("author_name", ""),
        "thumbnail": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
        "url": f"https://www.youtube.com/watch?v={vid}",
    }


def main() -> int:
    print("→ crawling Interview Resources …")
    foundation = crawl_playlist("foundation", PLAYLISTS["foundation"])
    cv_review = crawl_playlist("cv_review", PLAYLISTS["cv_review"])
    cv_tool = crawl_single_video(CV_TOOL_VIDEO_ID)

    payload = {
        "foundation": foundation,
        "cv": {
            "intro": (
                "4 nguồn tham khảo để bạn viết CV chuẩn Big Tech — CV mẫu đã pass "
                "Google, template LaTeX, video review CV thật, và tool generate CV nhanh."
            ),
            "sample": {
                "title": "CV mẫu — đã pass phỏng vấn Google",
                "subtitle": "Real CV của học viên EngineerPro · format & câu chữ tham khảo",
                "label": SAMPLE_CV_LABEL,
                "driveId": SAMPLE_CV_DRIVE_ID,
                "previewUrl": f"https://drive.google.com/file/d/{SAMPLE_CV_DRIVE_ID}/preview",
                "viewUrl": f"https://drive.google.com/file/d/{SAMPLE_CV_DRIVE_ID}/view",
            },
            "overleaf": {
                "title": "Overleaf — Software Engineer Resume Template",
                "subtitle": "LaTeX template chuyên cho SWE — sạch, ATS-friendly",
                "url": OVERLEAF_URL,
                "kind": "template",
            },
            "review": cv_review,
            "tool": cv_tool,
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    js = json.dumps(payload, ensure_ascii=False, indent=2)
    OUT.write_text(
        "// AUTO-GENERATED by scripts/crawl_resources.py — do not edit by hand.\n"
        "// Sources: YouTube playlist + oEmbed + Overleaf template URL\n"
        f"window.RESOURCES = {js};\n",
        encoding="utf-8",
    )
    print(f"✓ wrote → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
