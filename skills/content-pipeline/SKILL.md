---
name: content-pipeline
description: Re-crawl, re-parse, or re-translate the auto-generated content (courses, podcasts, FAQs, success stories, YouTube resources). Use when the user asks to refresh upstream data, fix bad story bodies, or add a new content source.
---

# Content pipeline

All content other than mentors / contact / book / roadmap / partners is **auto-generated** from external sources. Each `*-data.js` has a header comment saying which script generated it.

## Make targets (run individually)

```bash
make crawl-courses        # engineerprogurus.com/blogs/khoa-hoc → courses-data.js
make crawl-podcasts       # Substack archive (audio-only) → podcasts-data.js
make crawl-faqs           # engineerprogurus.com/blogs/faqs → faqs-data.js
make crawl-resources      # YouTube playlists + oEmbed → resources-data.js
make translate-courses    # Translate full course body Vietnamese → English (htmlEn field)

# Success stories — 3-stage pipeline
make parse-stories        # Google Sheet (Markdown) → stories-data.js
make crawl-story-bodies   # Google Docs HTML → originalHtml + originalTitle + cover
make crawl-story-images   # Substack covers as fallback
make clean-story-html     # strip Google redirects, dead bullets, etc.
make translate-stories    # Google Translate free endpoint → originalHtmlEn (Vietnamese → English)
make fix-translations     # post-process MT artifacts (SKATE → FAILED, Mr. honorifics, "Bạn học viên" → "Our student", etc.)

make crawl                # = crawl-courses + crawl-podcasts + crawl-faqs + crawl-resources
```

## Success-stories pipeline (most complex)

Stories live in a private Google Sheet. The Markdown export must be on disk:

1. **Stash the sheet** at `uploads/edit-0.md` (gitignored) OR pass via `EP_STORIES_MD=...` env / CLI arg.
2. **Parse**:
   ```bash
   make parse-stories                  # default path
   # or
   EP_STORIES_MD=path/to/edit-0.md make parse-stories
   ```
3. **Crawl Google Doc bodies** (one per story, extracts `originalHtml` + first inline image as cover):
   ```bash
   make crawl-story-bodies
   ```
4. **Fallback cover images** from Substack for stories without a Google Doc image:
   ```bash
   make crawl-story-images   # only fills stories without a cover yet
   # or force refresh of the Substack cache:
   python3.11 scripts/crawl_story_images.py --refresh
   ```
5. **Cleanup** (idempotent):
   ```bash
   make clean-story-html     # strip "Website:" orphan bullets, Google redirects
   ```
6. **Translate to English** (long — ~6 min for 94 stories via Google Translate free endpoint):
   ```bash
   make translate-stories    # adds originalHtmlEn + originalTitleEn
   make fix-translations     # post-process MT artifacts
   ```
7. **Build**: `make github` (will fail at `make stats` if story count changed but textual refs didn't update).

## Adding / removing a story

- Stories are filtered to `MAX_OUTPUT = 100` in `parse_stories.py`.
- To exclude a specific record (e.g. low-quality placeholder), parse normally then manually delete the entry from `src/assets/stories-data.js` and bump every story count reference. `make stats` will tell you what's stale.

## Adding hand-written content to a crawled course

Upstream (`engineerprogurus.com`) owns every course body, so editing `html` /
`htmlEn` in `courses-data.js` by hand gets wiped on the next `make crawl-courses`.
Declare the addition in `scripts/data/course_extra_blocks.json` instead — the
crawler re-injects those blocks at the end of every run.

```json
[
  {
    "slug": "system-design-interview-level-2",
    "id": "techtalk-tiktok-realtime",
    "insertBefore": { "vi": "<h2><strong>FEEDBACK từ học viên</strong></h2>",
                      "en": "<h2><strong>FEEDBACK from students</strong></h2>" },
    "vi": "<h2>…</h2><p>…</p>",
    "en": "<h2>…</h2><p>…</p>"
  }
]
```

- Each block is wrapped in `<div class="course-extra" data-extra="{id}">` so a
  re-run updates it in place instead of duplicating it.
- `insertBefore` is a literal substring, per language (the EN anchor lives in the
  machine-translated `htmlEn`, so it reads differently). No match → appended, so
  content is never silently dropped when upstream rewrites a heading.
- Apply without touching the network — and without losing the existing `htmlEn`
  translations, which a full re-crawl would drop:
  ```bash
  make course-extras          # = crawl_courses.py --extras-only
  ```
- Idempotent: re-running leaves the file byte-identical. Verify with
  `md5 -q src/assets/courses-data.js` before and after.
- Order matters after a real re-crawl: `make crawl-courses` (injects the VI
  block) → `make translate-courses` (regenerates `htmlEn`, machine-translating
  our block along the way) → `make course-extras` (swaps that MT output back for
  the curated EN copy).
- Embeds: reuse `<div class="embed-16x9">` and point iframes at
  `www.youtube-nocookie.com`. `sanitizeHtml()` in `app.js` drops any iframe whose
  host isn't in `IFRAME_HOST_ALLOWLIST`.

Currently declared: the community TikTok-realtime System Design techtalk on both
System Design courses (`khoa-hoc-system-design-interview-big-tech`,
`system-design-interview-level-2`).

## Course exclusions

`scripts/crawl_courses.py` has `EXCLUDED_SLUGS` to drop specific blog posts (per-user request — e.g. dropped Python intro, Frontend, OOP+DB Design, English course, LC 4.5 intensive). To re-include or add, edit that set and re-crawl.

## Podcast audio-only filter

`scripts/crawl_podcasts.py` only keeps items where `podcast_duration > 0` — Substack returns written posts under the "podcast" feed too. Don't relax this filter unless you want them back.

## YouTube playlist videos

`scripts/crawl_resources.py` sorts Foundation playlist by lesson number from titles (`Foundation N`). If you add a new playlist that doesn't follow this pattern, edit `lesson_key()`.

## Course translation pipeline (similar to stories)

`scripts/translate_courses.py` mirrors `translate_stories.py` exactly but operates on `courses-data.js`. For each course it walks `html` text nodes, batches them through Google Translate's free endpoint with `@@SPLIT@@` sentinels, then stores the result back as `htmlEn`. Idempotent — re-running skips courses that already have `htmlEn`.

Workflow when course content changes upstream:

```bash
make crawl-courses        # refresh from EngineerPro blog
# (delete htmlEn from any changed course in courses-data.js if you want it re-translated)
make translate-courses    # ~60s for 10 courses
make github               # build + ship
```

`renderCourseDetail()` in `src/assets/app.js` picks `c.htmlEn` when in EN mode and falls back to `c.html` + a "use browser translate" banner if `htmlEn` is missing.

## Tooling

All scripts use **stdlib + BeautifulSoup4 + Pillow** only. No paid APIs.
- LinkedIn scraping is **hard-blocked** (HTTP 999 even after IP rotation). `scripts/retry_linkedin.py` exists but expect 100% failure rate — mentor data must be entered by hand.
- Google Translate free endpoint sometimes garbles separators. `scripts/fix_translations.py` cleans the most common artifacts (SKATE, LYING, Mr. honorifics, "you guys", "gossip", "Bạn học viên", "tản mạn", marketing boilerplate). Add new SUBS rules to the `SUBS` list as new artifacts surface.
