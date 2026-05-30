# FIXED — P0 - Sanitize Generated/Crawled HTML Before `innerHTML`

**Status: FIXED** (2026-05-30)

## Resolution

Added a small runtime sanitizer `sanitizeHtml(html)` in `src/assets/app.js`. Strategy: parse the HTML in a detached `DOMParser`, walk every element, and:

- Drop `<script>`, `<style>`, `<object>`, `<embed>` entirely.
- Strip every attribute whose name starts with `on*` (event handlers).
- Strip `href`/`src`/`xlink:href` values that start with `javascript:`, `data:` or `vbscript:`.
- Allow `<iframe>` only when its `src` host is in the explicit allowlist: `youtube.com`, `youtube-nocookie.com`, `player.vimeo.com`, `drive.google.com`, `docs.google.com`, `www.facebook.com`. Anything else is removed.

Applied at the two highest-risk injection points:
- `renderCourseDetail()` → `sanitizeHtml(c.html)`
- `renderStoryDetail()` → `sanitizeHtml(stripDuplicateHeading(dispBody, dispTitle))`

`data-i18n-html` is left as-is because its values come from `src/assets/i18n.js` (we author them), not external crawled content. If we ever start sourcing i18n strings externally, the sanitizer is reusable as `sanitizeHtml(t(key))`.

---



Claude, the site injects crawled HTML directly into the DOM. The current crawlers strip some dangerous content, but the runtime path should still guard against bad upstream HTML.

## Evidence

- `src/assets/app.js:30-32` uses `innerHTML` for i18n HTML.
- `src/assets/app.js:417-425` injects `${c.html}` for course detail.
- `src/assets/app.js:842-845` interpolates `extUrl` directly into an HTML string.
- `src/assets/app.js:847-880` injects story body HTML into detail pages.
- Validation found `<iframe>` in all 10 course bodies. They appear to be YouTube embeds today, but there is no runtime allowlist.
- `scripts/crawl_courses.py` keeps iframe attributes and wraps iframes, but does not enforce an iframe host allowlist in the browser.

## Suggested Fix

1. Add a small runtime sanitizer for any crawled HTML before insertion:
   - allow tags needed for articles (`p`, `h2`, `h3`, `ul`, `ol`, `li`, `strong`, `em`, `a`, `img`, `table`, `iframe` if allowed).
   - strip `script`, `style`, event handlers (`on*`), `javascript:` URLs, unknown attributes.
   - allow iframe only for YouTube embed URLs (and any explicitly approved hosts).
2. Escape dynamic URL attributes when building HTML strings, or build those links with `createElement`.
3. Add `loading="lazy"` and a safe `allow`/`referrerpolicy` policy to iframes.
4. Keep crawler-side cleaning, but do not rely on it as the only defense.

## Acceptance Criteria

- A validation script flags zero `script`, `on*`, and `javascript:` occurrences in rendered article HTML.
- Non-allowlisted iframe hosts are removed or replaced with a link.
- Story/course detail pages still render legitimate YouTube embeds and images.
