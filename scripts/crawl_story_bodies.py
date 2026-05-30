#!/usr/bin/env python3
"""
Fetch the original article body for each Success Story from the Google Docs
linked in the Google Sheet, then embed the cleaned HTML as `originalHtml`
on each story record in src/assets/stories-data.js.

Pipeline:
  1. Download the source Sheet as .xlsx (preserves hyperlinks).
  2. Walk the rows, build STT → Google Doc URL map.
  3. For each story in stories-data.js, look up the doc by STT, fetch the
     doc HTML (Google Docs publish-as-HTML), clean it (drop Google Docs CSS,
     inline styles, junk attrs), and save as `originalHtml`.
  4. Re-write stories-data.js.

Run:  python3.11 scripts/crawl_story_bodies.py
"""
from __future__ import annotations

import html as html_lib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import base64
import io
import zipfile
import xml.etree.ElementTree as ET

from PIL import Image
from bs4 import BeautifulSoup, Comment, Tag

ROOT = Path(__file__).resolve().parent.parent
STORIES_JS = ROOT / "src" / "assets" / "stories-data.js"
IMG_DIR = ROOT / "src" / "assets" / "img" / "stories"
IMG_DIR.mkdir(parents=True, exist_ok=True)

SHEET_ID = "1duibacmbXGhnOAfTjMLgeFfmFiZaJVbLRTSUd-apBZY"
SHEET_XLSX_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"
SHEET_CACHE = Path("/tmp/ep_stories_sheet.xlsx")

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15"

DROP_TAGS = {"script", "style", "noscript", "meta", "link", "head"}
KEEP_ATTRS = {"href", "src", "alt", "title", "target", "rel", "loading", "type",
              "frameborder", "allow", "allowfullscreen"}


def fetch(url: str, binary: bool = False) -> bytes | str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", errors="replace")


def download_sheet() -> Path:
    if SHEET_CACHE.exists() and SHEET_CACHE.stat().st_size > 1000:
        return SHEET_CACHE
    print("→ downloading source sheet xlsx …")
    data = fetch(SHEET_XLSX_URL, binary=True)
    SHEET_CACHE.write_bytes(data)
    print(f"  cached → {SHEET_CACHE} ({len(data)//1024} KB)")
    return SHEET_CACHE


NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r":    "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def col_letter_to_index(letters: str) -> int:
    """Excel-style 'A'→0, 'F'→5, 'AA'→26."""
    n = 0
    for c in letters:
        n = n * 26 + (ord(c.upper()) - ord("A") + 1)
    return n - 1


def cell_row_col(coord: str) -> tuple[int, int]:
    """'F3' → (3, 5) (row, col_index)."""
    m = re.match(r"([A-Z]+)(\d+)", coord)
    if not m:
        return 0, 0
    return int(m.group(2)), col_letter_to_index(m.group(1))


def build_stt_to_url(xlsx_path: Path) -> dict[int, str]:
    """Parse sheet1.xml + its rels to map STT (column E) → hyperlink target on the same row."""
    with zipfile.ZipFile(xlsx_path) as z:
        sheet_xml = z.read("xl/worksheets/sheet1.xml").decode("utf-8")
        rels_xml = z.read("xl/worksheets/_rels/sheet1.xml.rels").decode("utf-8")
        shared_strings_xml = z.read("xl/sharedStrings.xml").decode("utf-8") if "xl/sharedStrings.xml" in z.namelist() else ""

    # Build shared strings index
    strings: list[str] = []
    if shared_strings_xml:
        ss_root = ET.fromstring(shared_strings_xml)
        for si in ss_root.findall("main:si", NS):
            parts = []
            for t in si.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"):
                parts.append(t.text or "")
            strings.append("".join(parts))

    # Build rId → target
    rels_root = ET.fromstring(rels_xml)
    rid_target: dict[str, str] = {}
    for rel in rels_root:
        rid = rel.attrib.get("Id")
        target = rel.attrib.get("Target")
        if rid and target:
            rid_target[rid] = target

    # Parse worksheet — first collect all hyperlinks (cell ref → rId)
    sheet_root = ET.fromstring(sheet_xml)
    cell_to_url: dict[str, str] = {}
    hl_block = sheet_root.find("main:hyperlinks", NS)
    if hl_block is not None:
        for hl in hl_block.findall("main:hyperlink", NS):
            ref = hl.attrib.get("ref", "")
            rid = hl.attrib.get(f"{{{NS['r']}}}id") or hl.attrib.get("ref")
            target = hl.attrib.get("location") or rid_target.get(rid or "", "")
            if ref and target:
                cell_to_url[ref] = target

    # Walk rows: STT in column A (col_idx 0), article hyperlink in column E (col_idx 4).
    # Status hyperlink in G (col_idx 6) is the substack note link — also useful as fallback.
    out: dict[int, str] = {}
    for row in sheet_root.find("main:sheetData", NS).findall("main:row", NS):
        row_idx = int(row.attrib.get("r", "0"))
        stt: int | None = None
        for c in row.findall("main:c", NS):
            coord = c.attrib.get("r", "")
            _, col_i = cell_row_col(coord)
            if col_i != 0:  # column A
                continue
            t = c.attrib.get("t", "")
            v_el = c.find("main:v", NS)
            if v_el is None or v_el.text is None:
                continue
            raw = v_el.text
            try:
                if t == "s":
                    val = strings[int(raw)]
                    if val.strip().isdigit():
                        stt = int(val.strip())
                else:
                    f = float(raw)
                    if f.is_integer():
                        stt = int(f)
            except Exception:
                pass
        if stt is None:
            continue
        for col_letter in ("E", "G", "H", "F"):
            url = cell_to_url.get(f"{col_letter}{row_idx}")
            if url and url.startswith("http"):
                out[stt] = url
                break
    return out


def save_data_uri_image(data_uri: str, out_path_no_ext: Path) -> Path | None:
    """Decode a base64 data: URI image, downscale, save as WebP, return final path."""
    m = re.match(r"data:image/[a-zA-Z+]+;base64,(.+)", data_uri)
    if not m:
        return None
    try:
        raw = base64.b64decode(m.group(1))
    except Exception:
        return None
    try:
        img = Image.open(io.BytesIO(raw)).convert("RGB")
    except Exception:
        return None
    if img.width > 1200:
        ratio = 1200 / img.width
        img = img.resize((1200, int(img.height * ratio)), Image.LANCZOS)
    out = out_path_no_ext.with_suffix(".webp")
    img.save(out, "WEBP", quality=82, method=6)
    return out


def extract_doc_title(soup: BeautifulSoup) -> str:
    """Pull the first non-empty title-ish element from a Google Docs HTML export."""
    # Google Docs export uses inline-styled <p class="title"> for the document title.
    for sel in ("p.title", ".title", "h1", "h2"):
        n = soup.select_one(sel)
        if n:
            txt = n.get_text(" ", strip=True)
            if txt:
                return txt
    return ""


def clean_doc_html(html: str, slug: str) -> tuple[str, str, str]:
    """Parse a Google Docs export. Return (cleaned_html, title, cover_path).

    cover_path is the local relative path to a saved WebP if we found an inline
    image in the doc — otherwise empty string.
    """
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body or soup

    title = extract_doc_title(soup)

    # Drop noise tags
    for t in DROP_TAGS:
        for n in body.find_all(t):
            n.decompose()
    for c in body.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    # Strip all inline classes / ids / style — Google Docs spams them
    for el in body.find_all(True):
        if el.name in ("span", "font"):
            el.unwrap()
            continue
        for attr in list(el.attrs.keys()):
            if attr not in KEEP_ATTRS:
                del el.attrs[attr]

    # Walk images. Save up to N base64 images locally as <slug>-imgK.webp,
    # rewrite each src to point at the local file. Drop placeholder paths.
    saved_imgs: list[str] = []
    max_imgs = 8  # cap per article to avoid blowing up size
    img_idx = 0
    for img in list(body.find_all("img")):
        src = img.get("src", "")
        if not src or src.startswith("images/") or src.startswith("./images/"):
            img.decompose()
            continue
        if src.startswith("data:"):
            if img_idx >= max_imgs:
                img.decompose()
                continue
            local = save_data_uri_image(src, IMG_DIR / f"{slug}-img{img_idx + 1}")
            if local:
                img["src"] = f"assets/img/stories/{local.name}"
                img["loading"] = "lazy"
                saved_imgs.append(f"assets/img/stories/{local.name}")
                img_idx += 1
            else:
                img.decompose()
        # else: external https URL — keep as-is

    # Scrub references to the legacy engineerprogurus.com site — strip the
    # anchors entirely; if a paragraph is only this URL, drop the paragraph.
    for a in list(body.find_all("a")):
        href = (a.get("href") or "").lower()
        if "engineerprogurus.com" in href:
            parent = a.parent
            a.unwrap()
            if parent and parent.name in ("p", "div", "li") and not parent.get_text(strip=True):
                parent.decompose()
    # Replace plain-text mentions of the old domain in remaining text nodes.
    for txt in list(body.find_all(string=True)):
        if isinstance(txt, Comment):
            continue
        s = str(txt)
        if "engineerprogurus" in s.lower():
            new = re.sub(r"https?://(www\.)?engineerprogurus\.com/?\S*", "", s, flags=re.IGNORECASE)
            new = re.sub(r"engineerprogurus\.com\S*", "", new, flags=re.IGNORECASE)
            txt.replace_with(new)

    # Drop empty paragraphs / divs left over
    changed = True
    while changed:
        changed = False
        for tag in ("p", "div", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5"):
            for n in list(body.find_all(tag)):
                if n.find(["img", "iframe", "video"]):
                    continue
                if not n.get_text(strip=True):
                    n.decompose()
                    changed = True

    # Demote H1s to H2 (we render our own H1 with the story title)
    for h1 in body.find_all("h1"):
        h1.name = "h2"

    cover = saved_imgs[0] if saved_imgs else ""
    return "".join(str(c) for c in body.children).strip(), title, cover


def doc_export_url(view_url: str) -> str:
    """Convert a Google Docs URL like /document/d/<ID>/edit to /export?format=html"""
    m = re.search(r"/document/d/([a-zA-Z0-9_-]+)", view_url)
    if not m:
        return ""
    return f"https://docs.google.com/document/d/{m.group(1)}/export?format=html"


def load_stories() -> list[dict]:
    text = STORIES_JS.read_text()
    m = re.search(r"window\.STORIES = (\[.*\]);", text, re.S)
    return json.loads(m.group(1))


def write_stories(stories: list[dict]) -> None:
    text = STORIES_JS.read_text()
    header = text[: text.index("window.STORIES")]
    payload = json.dumps(stories, ensure_ascii=False, indent=2)
    STORIES_JS.write_text(f"{header}window.STORIES = {payload};\n", encoding="utf-8")


def main() -> int:
    xlsx = download_sheet()
    stt_to_url = build_stt_to_url(xlsx)
    print(f"→ sheet has {len(stt_to_url)} rows with hyperlinks")

    stories = load_stories()
    matched = 0
    failed = 0
    for s in stories:
        stt = s.get("stt")
        url = stt_to_url.get(stt) if stt else None
        if not url:
            continue
        exp = doc_export_url(url)
        if not exp:
            # not a Google Doc — keep as-is (substack note links etc.)
            s["sourceUrl"] = url
            continue
        s["sourceUrl"] = url
        try:
            print(f"  [{stt:>3}] fetching → {url[:80]}…")
            html = fetch(exp)
            cleaned, real_title, real_cover = clean_doc_html(html, s["slug"])
            if len(cleaned) < 200:
                failed += 1
                continue
            s["originalHtml"] = cleaned
            if real_title:
                s["originalTitle"] = real_title
            if real_cover:
                s["cover"] = real_cover
                s["coverFrom"] = "googledoc"
            matched += 1
            time.sleep(0.15)
        except Exception as e:
            print(f"        ! failed: {e}")
            failed += 1

    write_stories(stories)
    print(f"\n✓ embedded original body for {matched} stories (failed: {failed})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
