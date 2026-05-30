# P0/P1 - SEO Follow-up: Localhost Canonicals and Remaining Prerender Regressions

Claude, after the latest fix pass, some infrastructure is better, but the current deploy artifact is still not SEO-ready. The biggest new regression is that production-facing `src/` and `docs/` SEO files now point to `http://localhost:8001`.

## Passing Checks

- `node --check src/assets/app.js` passes.
- `node --check docs/assets/app.js` passes.
- `python3.11 -m py_compile scripts/make_seo.py scripts/build_pages.py scripts/site_config.py` passes.
- `docs/sitemap.xml` has 114 URL entries, 0 hash URLs, and every entry maps to a generated `docs/**/index.html` page.

## P0 - Production SEO artifacts currently point to localhost

### Evidence

- `docs/index.html:27-30` emits canonical, `og:url`, and `og:image` with `http://localhost:8001`.
- Detail pages do the same, for example `docs/stories/anh-dang-microsoft/index.html:27-31`.
- `docs/robots.txt:4` points the sitemap to `http://localhost:8001/sitemap.xml`.
- `docs/sitemap.xml:5-10` starts with localhost `<loc>` and hreflang URLs.
- `docs/404.html:7`, `docs/404.html:16`, and `docs/404.html:21` redirect visitors to localhost.
- The tracked source SEO files are also polluted:
  - `src/robots.txt:4`
  - `src/sitemap.xml:5-10`
- Static scan results:
  - `docs/`: 117 files contain `http://localhost:8001`, with 3100 occurrences.
  - `src/`: 2 files contain `http://localhost:8001`, with 457 occurrences.

### Impact

Search engines and social scrapers will see localhost as the canonical site, sitemap origin, share URL, and 404 redirect target. On GitHub Pages, an unknown URL can also bounce real users to `http://localhost:8001/`.

### Likely Root Cause

`make local-build` says it keeps production artifacts untouched, but `scripts/make_seo.py` always writes to `src/sitemap.xml` and `src/robots.txt`:

- `Makefile:105-117` runs local SEO generation with `EP_BASE_URL=http://localhost:$(PORT)`.
- `scripts/make_seo.py:85-95` ignores `EP_OUT` and writes directly under `SRC`.

That explains why the tracked `src/` SEO files now contain localhost. `docs/` also needs a clean production rebuild.

### Suggested Fix

1. Make the final production base URL/path explicit and single-source:
   - Root deploy example: `EP_BASE_URL=https://engineerpro-academy.github.io EP_BASE_PATH= make github`
   - Project Pages example: `EP_BASE_URL=https://engineerpro-team.github.io EP_BASE_PATH=/interview-trainings make github`
2. Regenerate and commit `src/robots.txt`, `src/sitemap.xml`, and the whole `docs/` deploy artifact with that production base.
3. Fix `scripts/make_seo.py` so local builds can write to `EP_OUT` instead of mutating tracked `src/`.
4. Add a guard that fails production builds if `http://localhost` appears in `src/sitemap.xml`, `src/robots.txt`, `docs/404.html`, or `docs/**/*.html`.

## P1 - Prerendered detail body content is still hidden and creates duplicate IDs

### Evidence

- `scripts/build_pages.py:312-318` defines `SHOW_ROUTE_STYLE_TMPL`, but generated pages do not include it.
- CSS hides all hidden route sections: `src/assets/style.css:3685-3686`.
- Story detail example:
  - `docs/stories/anh-dang-microsoft/index.html:706` is still `<section class="route" data-route="story" hidden>`.
  - `docs/stories/anh-dang-microsoft/index.html:708` injects `id="storyArticle"`.
  - `docs/stories/anh-dang-microsoft/index.html:711` already has another `id="storyArticle"`.
- Course detail example:
  - `docs/courses/cracking-machine-coding-low-level-design-round/index.html:608` is still hidden.
  - `docs/courses/cracking-machine-coding-low-level-design-round/index.html:610` injects `id="courseArticle"`.
  - `docs/courses/cracking-machine-coding-low-level-design-round/index.html:613` already has another `id="courseArticle"`.
- Full generated-page scan still finds duplicate `courseArticle` / `storyArticle` IDs on 104 pages.

### Impact

No-JS crawlers/users still do not get visible detail body content, and the HTML is invalid. Runtime `document.getElementById(...)` can also target the injected SEO snippet instead of the intended SPA mount node.

### Suggested Fix

Inject the prerendered snippet inside the existing mount element instead of adding a second element with the same ID. Also reveal the matching route in generated HTML, either by removing that page's `hidden` attribute or by actually injecting the per-page prerender style.

## P1 - Clean URLs are still mutated into hash URLs on initial load

### Evidence

- `scripts/build_pages.py:266-285` still injects a bootstrap script that sets `location.hash`.
- Generated detail pages include it, for example `docs/stories/anh-dang-microsoft/index.html:170-182`.
- `src/assets/app.js:205-220` already parses clean path URLs directly.
- Initial routing runs at `src/assets/app.js:1775`.
- Hash cleanup currently happens for click navigation only at `src/assets/app.js:429-432`, not for initial page load.

### Impact

Opening `/stories/anh-dang-microsoft/` can become `/stories/anh-dang-microsoft/#story/anh-dang-microsoft` in the browser. That weakens the clean-route UX and creates extra shareable URL variants.

### Suggested Fix

Remove the bootstrap hash mutation entirely and let `parseHash()` route from `location.pathname`. If a bootstrap remains, it should use `history.replaceState(...)` and keep the visible URL hash-free.

## P1 - English hreflang URLs are still not standalone English pages

### Evidence

- `scripts/make_seo.py:78-80` emits English alternates as `?lang=en`.
- `scripts/build_pages.py:150-164` emits the same hreflang pattern into page heads.
- Generated examples:
  - `docs/stories/anh-dang-microsoft/index.html:49-50`
  - `docs/courses/cracking-machine-coding-low-level-design-round/index.html:49-50`
- The HTML source for `?lang=en` is still the Vietnamese page and canonicalizes to the non-query URL, for example `docs/stories/anh-dang-microsoft/index.html:27`.
- Runtime canonical generation also drops `?lang=en`: `src/assets/app.js:313-317`.

### Impact

The English alternate is advertised, but it is not a self-canonical, source-rendered English document. Google may ignore it as a language alternate, and non-JS crawlers/social scrapers will still see Vietnamese metadata.

### Suggested Fix

Either generate real English pages (`/en/`, `/en/courses/<slug>/`, `/en/stories/<slug>/`) with English source HTML and self-canonicals, or remove `hreflang="en"` until that exists.

## P2 - Social preview tags remain generic or inconsistent

### Evidence

- Story pages still use `og:type="website"` instead of article-like metadata, e.g. `docs/stories/anh-dang-microsoft/index.html:18`.
- Story cover is WebP, but `og:image:type` says PNG at `docs/stories/anh-dang-microsoft/index.html:29-31`.
- Zalo tags remain generic on route/detail pages, e.g. `docs/stories/anh-dang-microsoft/index.html:45-46`.
- Full generated-page scan found:
  - 96 pages with `og:image:type` mismatching the actual image extension.
  - 113 non-home pages with generic Zalo title/image.
  - 114 generated pages with `og:type="website"`.

### Suggested Fix

Patch `og:image:type` based on the selected image extension or omit it when uncertain. Patch Zalo tags from the same route metadata as OG/Twitter. Use `article` for story pages and keep `website` for home/listing pages.

## Acceptance Criteria

- No production artifact contains `http://localhost`.
- `make local-build` does not mutate tracked `src/sitemap.xml` or `src/robots.txt`.
- Generated detail pages have no duplicate IDs.
- No-JS source shows the current route's prerendered content visibly.
- Opening a clean detail URL does not append a hash.
- English hreflang links either point to real self-canonical English pages or are removed.
- Social metadata matches the route and image MIME types.
