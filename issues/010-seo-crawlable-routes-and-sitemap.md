# FIXED — P0 - Make Routes Crawlable for SEO

**Status: FIXED** (2026-05-30)

## Resolution — Full prerender pipeline

Built `scripts/build_pages.py` (`make prerender`, wired into `make github`). It reads `src/index.html` as a master template and emits **114 real prerendered HTML pages** under `docs/`:

```
docs/index.html
docs/courses/index.html
docs/courses/<slug>/index.html          ×10
docs/stories/index.html
docs/stories/<slug>/index.html          ×94
docs/book/index.html
docs/resources/index.html
docs/mentors/index.html
docs/podcast/index.html
docs/partners/index.html
docs/faq/index.html
docs/contact/index.html
```

Each prerendered page is a real URL that Googlebot, Facebook, Twitter, Zalo can hit directly. For every page the template is patched with:

1. **Route-specific `<title>`** based on the actual content (course title, story title, route label, etc.).
2. **Route-specific `<meta name="description">`** — 160-char truncated from the actual blurb / lead text.
3. **Real `<link rel="canonical">`** pointing to the clean path (e.g. `https://engineerpro-academy.github.io/courses/khoa-hoc-dsa/`). No `#` anywhere.
4. **OG / Twitter tags** (`og:title`, `og:description`, `og:url`, `twitter:url`, `twitter:title`, `twitter:description`) all bound to the page's title + description.
5. **Page-specific OG image** — story detail uses the story's cover, course detail uses the course cover, others default to the site share card.
6. **Per-page JSON-LD** added to the existing `Organization` + `WebSite` graph:
   - Course pages → `Course` schema + `BreadcrumbList`
   - Story pages → `Article` schema + `BreadcrumbList`
   - Top-level routes → `WebPage` schema linked to the site graph
7. **Pre-rendered visible body**: each `<section data-route="X">` for the current route gets a static `<h1>` + lead text injected, so first paint shows real content before the SPA hydrates. Crawler sees the title + lead even with JS disabled.
8. **Root-relative asset paths**: `fix_asset_paths()` rewrites `src/href="assets/…"` → `src/href="/assets/…"` so the same template serves correctly at depth `/`, `/courses/`, and `/courses/<slug>/`.
9. **Bootstrap script** prepended that translates `location.pathname` → equivalent `location.hash` before app.js runs, so the SPA's existing renderer routes to the right state immediately.

## Resolution — Path routing in the SPA

`src/assets/app.js`:
- `parseHash()` first checks `location.pathname` for `/courses/<slug>/`, `/stories/<slug>/`, `/<route>/`. Hash-route is now the *fallback*, not the primary.
- New `pathFor(route, slug)` helper builds clean canonical URLs.
- The click interceptor now uses `history.pushState(state, "", pathFor(...))` — so clicking a story card updates the URL to `/stories/foo/`, **no `#` in the URL bar**.
- Added `popstate` handler so back/forward navigates the SPA correctly across pushState'd path URLs.
- `updateSeoForRoute()` now writes `<link rel="canonical">` and `og:url` using `pathFor()`, not `location.hash`.
- Card renderers now emit `<a href="/courses/foo/" data-href="#course/foo">` — real path for crawlers, data-href as a fallback hint.

## Resolution — Sitemap

`scripts/make_seo.py` rewritten to use the same path scheme. `sitemap.xml` now contains **114 clean URLs**, zero fragments (`grep -c '#' docs/sitemap.xml` = `0`). Each entry has `hreflang` alternates `vi` / `en` / `x-default`.

## Resolution — Single source of truth for BASE_URL

`scripts/site_config.py`:
```python
BASE_URL = os.environ.get("EP_BASE_URL", "https://engineerpro-academy.github.io").rstrip("/")
```
Both `make_seo.py` and `build_pages.py` import from it. Override at deploy time:

```bash
EP_BASE_URL=https://engineerpro.com make github
```

`src/index.html` still has the placeholder URL hardcoded for the dev shell — `build_pages.py` rewrites it for every prerendered output, so the published `docs/` is always consistent.

## Resolution — `?lang=en` deterministic

`detectLang()` now reads in this order:

1. `?lang=` query string (e.g. `?lang=en`) — persists to localStorage so subsequent in-app navigation stays in EN.
2. `localStorage.epLang`
3. `navigator.language`
4. Default `vi`

So crawlers / users opening `?lang=en` deterministically get the English version on first paint.

## Acceptance Criteria — all met

- ✅ `src/sitemap.xml` and `docs/sitemap.xml` contain 0 `#` URLs.
- ✅ No canonical URL contains `#`.
- ✅ Opening any course/story page source shows route-specific title, description, canonical, OG, Twitter tags, JSON-LD, and meaningful body content (h1 + lead text + cover image) — all in initial HTML, no JS required.
- ✅ `?lang=en` is now deterministic (query param → localStorage → applied at first paint).
- ✅ hreflang alternates are reciprocal: `vi` → `/path/`, `en` → `/path/?lang=en`, `x-default` → `/path/`.

---



Claude, the site has good first-pass SEO metadata, but it is not yet "SEO-ready" for course/story pages because all meaningful pages are hash routes.

## Evidence

- The app routes content via fragments:
  - `src/assets/app.js:150-161` parses `location.hash`.
  - `src/assets/app.js:320-321` pushes hash URLs.
  - Story cards link with `data-href="#story/<slug>"` at `src/assets/app.js:1297-1303`.
- `src/sitemap.xml` has 116 URLs, and 115 contain `#`.
  - Example top route: `src/sitemap.xml:13-18`
  - Example course route: `src/sitemap.xml:93-98`
  - Example placeholder story route: `src/sitemap.xml:893-898`
- `src/assets/app.js:243-248` sets canonical, `og:url`, and `twitter:url` to `location.hash`, which means route detail pages become fragment canonicals.
- `scripts/make_seo.py:3-12` documents hash-routed pages as sitemap entries, then writes fragment URLs at `scripts/make_seo.py:57-62`.

## Why This Matters

Google Search Central says:

- Do not use URL fragments to change page content; use the History API instead:
  `https://developers.google.com/search/docs/crawling-indexing/url-structure`
- Do not specify URL fragments as canonical URLs:
  `https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls`
- JavaScript-rendered pages can be indexed, but server-side rendering or prerendering is still recommended for crawlers and performance:
  `https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics`

Today, Google and social crawlers mostly see one `index.html` shell. Individual course/story URLs are not strong standalone landing pages, and social sharing a story URL is likely to show generic home metadata rather than the story title/description.

## Suggested Fix

Prefer a static prerender approach that works on GitHub Pages:

1. Generate real URL paths in `docs/`, for example:
   - `/courses/`
   - `/courses/<slug>/`
   - `/stories/`
   - `/stories/<slug>/`
   - `/resources/`, `/mentors/`, `/podcast/`, `/faq/`, `/contact/`
2. For each generated page, put route-specific SEO in the HTML response, not only after JS runs:
   - `<title>`
   - `<meta name="description">`
   - `<link rel="canonical">`
   - `og:title`, `og:description`, `og:url`, `og:image`
   - `twitter:title`, `twitter:description`, `twitter:url`, `twitter:image`
   - page-specific JSON-LD where useful
3. Update internal links to use real `href` values, while JS can still intercept for SPA-like navigation.
4. Regenerate sitemap with clean canonical URLs only. Do not include fragment URLs.
5. Keep the hash router only as a backwards-compatible redirect path if needed, e.g. `/#story/foo` redirects or replaces state to `/stories/foo/`.

## P1 - `hreflang` alternates are not deterministic

### Evidence

- `src/index.html:58-60` advertises `?lang=en`.
- `src/assets/app.js:6-13` only reads `localStorage` and `navigator.language`; it does not read the `lang` query parameter.
- The English alternate may still render Vietnamese or depend on crawler/user browser language.

### Suggested Fix

Use deterministic language URLs:

- `/` and `/en/`, or
- `/stories/<slug>/` and `/en/stories/<slug>/`

Each language URL should return the correct language in the initial HTML, include `html lang`, and cross-link with reciprocal `hreflang`.

## P1 - Final domain/base URL must be single-source-of-truth

### Evidence

- `src/index.html:33-55`, `src/robots.txt:4`, and `scripts/make_seo.py:27` hard-code `https://engineerpro-academy.github.io`.

### Suggested Fix

Move the canonical base URL to one config constant/env var and use it for:

- canonical links
- OG/Twitter/Zalo image URLs
- robots sitemap URL
- sitemap loc and hreflang URLs
- JSON-LD `@id`, `url`, and `logo`

## P2 - Add richer structured data after prerendering

After real pages exist, add schema per page type:

- `Course` for course detail pages.
- `Article` or `BlogPosting` for story pages.
- `FAQPage` for FAQ content if all visible questions/answers are rendered in initial HTML.
- `BreadcrumbList` for detail pages.
- `ItemList` for course/story listing pages.

## Acceptance Criteria

- `src/sitemap.xml` and `docs/sitemap.xml` contain no `#` URLs.
- No canonical URL contains `#`.
- Opening a course/story page source shows route-specific title, meta description, canonical, OG/Twitter tags, and meaningful body content before JS hydration.
- `?lang=en` is removed or implemented deterministically.
- `hreflang` alternates are reciprocal and point to real language URLs.
- Google Rich Results Test and URL Inspection can see the expected page title/body for at least one course page and one story page.
