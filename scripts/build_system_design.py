#!/usr/bin/env python3
"""
Build EN chapter HTML + copy images from system-design-notes source.

  python3 scripts/build_system_design.py
  SD_SOURCE=/path/to/system-design-notes-main python3 scripts/build_system_design.py
"""

from __future__ import annotations

import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_OUT = os.path.join(ROOT, "src", "assets", "content", "system-design")
DATA_JS = os.path.join(ROOT, "src", "assets", "system-design-data.js")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from system_design_config import CHAPTERS, MANIFEST_CHAPTERS, DEFAULT_SOURCE  # noqa: E402

try:
    import markdown as md_lib

    def md_to_html(text: str) -> str:
        return md_lib.markdown(
            text,
            extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
        )
except ImportError:
    def md_to_html(text: str) -> str:
        # Minimal fallback — install markdown for better output
        html = text
        html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.M)
        html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.M)
        html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.M)
        html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
        html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
        html = re.sub(r"^---\s*$", "<hr />", html, flags=re.M)
        html = re.sub(r"^[-*] (.+)$", r"<li>\1</li>", html, flags=re.M)
        html = re.sub(r"(<li>.*</li>\n?)+", r"<ul>\g<0></ul>", html)
        return f"<p>{html.replace(chr(10)+chr(10), '</p><p>')}</p>"


def find_readme(folder: str) -> str | None:
    for name in ("Readme.md", "README.md", "readme.md"):
        p = os.path.join(folder, name)
        if os.path.isfile(p):
            return p
    return None


def strip_leading_h1(md: str) -> str:
  lines = md.splitlines()
  i = 0
  while i < len(lines) and not lines[i].strip():
    i += 1
  if i < len(lines) and lines[i].startswith("# "):
    lines.pop(i)
    while i < len(lines) and not lines[i].strip():
      lines.pop(i)
  return "\n".join(lines).strip()


def preprocess_md(md: str) -> str:
    """Convert HTML img/div blocks in source MD to markdown-friendly form."""
    # <div>...<img src="./images/foo.png" ...></div>
    def repl_div(m: re.Match) -> str:
        src = m.group(1)
        alt = m.group(2) or ""
        width = m.group(3) or "500"
        return f'![{alt}]({src}){{width={width}}}'

    md = re.sub(
        r'<div[^>]*>\s*<img\s+src="([^"]+)"(?:\s+alt="([^"]*)")?[^>]*width="?(\d+)"?[^>]*/>\s*</div>',
        repl_div,
        md,
        flags=re.I | re.S,
    )
    md = re.sub(
        r'<img\s+src="([^"]+)"(?:\s+alt="([^"]*)")?[^>]*width="?(\d+)"?[^>]*/>',
        repl_div,
        md,
        flags=re.I,
    )
    return md


def postprocess_html(html: str, img_prefix: str) -> str:
    html = re.sub(
        r'src="(?:\./)?images/([^"]+)"',
        lambda m: f'src="assets/content/system-design/images/{img_prefix}/{m.group(1)}"',
        html,
    )
    html = re.sub(
        r'src="(?:\./)?images//([^"]+)"',
        lambda m: f'src="assets/content/system-design/images/{img_prefix}/{m.group(1)}"',
        html,
    )
    # markdown image syntax leftovers
    html = re.sub(
        r'!\[([^\]]*)\]\((?:\./)?images/([^)]+)\)(?:\{width=(\d+)\})?',
        lambda m: (
            f'<figure class="sd-figure"><img src="assets/content/system-design/images/'
            f'{img_prefix}/{m.group(2)}" alt="{m.group(1)}" width="{m.group(3) or "500"}" loading="lazy" /></figure>'
        ),
        html,
    )
    html = html.replace("<table>", '<table class="sd-table">')
    html = re.sub(
        r"<img([^>]*)(?<!loading=)(?<!loading=\")(?<!loading=')(/?)>",
        lambda m: f"<img{m.group(1)} loading=\"lazy\"{m.group(2)}>",
        html,
    )
    # Wrap bare imgs in figure if not already
    html = re.sub(
        r'(?<!<figure class="sd-figure">)(<img src="assets/content/system-design[^"]+"[^>]*/>)',
        r'<figure class="sd-figure">\1</figure>',
        html,
    )
    html = re.sub(r"<h1[^>]*>.*?</h1>", "", html, count=1, flags=re.S)
    html = re.sub(r"\{(?:width|chiều rộng)=\d+\}", "", html, flags=re.I)
    # Unwrap <p><img...></p> → figure
    html = re.sub(
        r"<p>\s*(<img[^>]+>)\s*</p>",
        r'<figure class="sd-figure">\1</figure>',
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<div[^>]*>\s*(<img[^>]+>)\s*</div>",
        r'<figure class="sd-figure">\1</figure>',
        html,
        flags=re.I,
    )
    return html.strip()


def copy_images(src_folder: str, dest_folder: str) -> int:
    img_dir = os.path.join(src_folder, "images")
    if not os.path.isdir(img_dir):
        return 0
    os.makedirs(dest_folder, exist_ok=True)
    n = 0
    for name in os.listdir(img_dir):
        if name.startswith("."):
            continue
        shutil.copy2(os.path.join(img_dir, name), os.path.join(dest_folder, name))
        n += 1
    return n


def write_data_js() -> None:
    lines = [
        "// System Design notes manifest — chapter bodies lazy-loaded from",
        "// assets/content/system-design/{vi|en}/<slug>.html",
        "// AUTO-GEN: scripts/build_system_design.py + translate/review scripts",
        "window.SYSTEM_DESIGN = {",
        '  title: "System Design Notes",',
        '  titleEn: "System Design Notes",',
        '  intro:',
        '    "23 case study kinh điển — đọc trực tuyến, mỗi chương tải khi cần. Chỉ mang tính tham khảo; để rèn kỹ năng trình bày và đáp ứng chuẩn tuyển dụng theo level, xem khóa học và mock bên dưới.",',
        '  introEn:',
        '    "23 classic case studies — read online, one chapter at a time. Reference only; for presentation practice and level-matched hiring-bar prep, see courses & mock below.",',
        '  credit:',
        '    "Tổng hợp & dịch tiếng Việt bởi Phạm Ngọc Lâm & Lê Quang Hoà (EngineerPro).",',
        '  creditEn:',
        '    "Compiled & Vietnamese translation by Phạm Ngọc Lâm & Lê Quang Hoà (EngineerPro).",',
        '  attribution:',
        '    "Nguồn: liquidslr/system-design-notes",',
        '  attributionEn:',
        '    "Source: liquidslr/system-design-notes",',
        "  authors: [",
        '    { name: "Phạm Ngọc Lâm", role: "ex-Senior Software Engineer @ TikTok · Grab", roleEn: "ex-Senior Software Engineer @ TikTok · Grab", photo: "assets/img/mentors/lam-pham.jpg", linkedin: "https://www.linkedin.com/in/lam0895/", portfolio: "https://lampn95.github.io/" },',
        '    { name: "Lê Quang Hoà", role: "ex-Tech Lead @ TikTok", roleEn: "ex-Tech Lead @ TikTok", photo: "assets/img/mentors/harry-le-quang-hoa.jpg", linkedin: "https://www.linkedin.com/in/harry-le-quang-hoa-32210066/" },',
        "  ],",
        "  chapters: [",
    ]
    for idx, ch in enumerate(MANIFEST_CHAPTERS, start=1):
        lines.append(
            f'    {{ n: {idx}, slug: "{ch["slug"]}", '
            f'title: "{ch["title"]}", titleEn: "{ch["titleEn"]}", available: true }},'
        )
    lines += ["  ],", "};", ""]
    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> int:
    source = os.environ.get("SD_SOURCE", DEFAULT_SOURCE)
    if not os.path.isdir(source):
        print(f"✗ Source not found: {source}", file=sys.stderr)
        return 1

    en_dir = os.path.join(SRC_OUT, "en")
    img_root = os.path.join(SRC_OUT, "images")
    os.makedirs(en_dir, exist_ok=True)

    total_imgs = 0
    for ch in CHAPTERS:
        folder = os.path.join(source, ch["folder"])
        readme = find_readme(folder)
        if not readme:
            print(f"  ! missing readme: {ch['folder']}", file=sys.stderr)
            continue
        raw = open(readme, encoding="utf-8").read()
        body_md = preprocess_md(strip_leading_h1(raw))
        html = postprocess_html(md_to_html(body_md), f"ch{ch['n']:02d}")
        out_path = os.path.join(en_dir, f"{ch['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html + "\n")
        dest_imgs = os.path.join(img_root, f"ch{ch['n']:02d}")
        n = copy_images(folder, dest_imgs)
        total_imgs += n
        print(f"  ch{ch['n']:02d} {ch['slug']:<28} {len(html):>6} chars  {n:>2} imgs")

    write_data_js()
    print(f"[build_system_design] {len(CHAPTERS)} EN chapters, {total_imgs} images → {SRC_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
