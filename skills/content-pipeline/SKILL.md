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

# Success stories — 3-stage pipeline
make parse-stories        # Google Sheet (Markdown) → stories-data.js
make crawl-story-bodies   # Google Docs HTML → originalHtml + originalTitle + cover
make crawl-story-images   # Substack covers as fallback
make clean-story-html     # strip Google redirects, dead bullets, etc.
make translate-stories    # Google Translate free endpoint → originalHtmlEn (Vietnamese → English)
make fix-translations     # post-process MT artifacts (SKATE → FAILED, Mr. honorifics, etc.)

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

## Course exclusions

`scripts/crawl_courses.py` has `EXCLUDED_SLUGS` to drop specific blog posts (per-user request — e.g. dropped Python intro, Frontend, OOP+DB Design, English course, LC 4.5 intensive). To re-include or add, edit that set and re-crawl.

## Podcast audio-only filter

`scripts/crawl_podcasts.py` only keeps items where `podcast_duration > 0` — Substack returns written posts under the "podcast" feed too. Don't relax this filter unless you want them back.

## YouTube playlist videos

`scripts/crawl_resources.py` sorts Foundation playlist by lesson number from titles (`Foundation N`). If you add a new playlist that doesn't follow this pattern, edit `lesson_key()`.

## Tooling

All scripts use **stdlib + BeautifulSoup4 + Pillow** only. No paid APIs.
- LinkedIn scraping is **hard-blocked** (HTTP 999 even after IP rotation). `scripts/retry_linkedin.py` exists but expect 100% failure rate — mentor data must be entered by hand.
- Google Translate free endpoint sometimes garbles separators. `scripts/fix_translations.py` cleans the most common artifacts.
