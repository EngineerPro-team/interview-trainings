# P1/P2 - SEO Follow-up After Prerender Fix

Claude, the main SEO architecture is much better now: sitemap URLs are clean, real `docs/<route>/index.html` pages exist, and course/story pages have route-specific metadata and JSON-LD. A few implementation issues still need cleanup before calling this SEO-ready.

## Passing Checks

- `src/sitemap.xml` and `docs/sitemap.xml` have 114 URLs and 0 fragment (`#`) URLs.
- Every sitemap URL maps to an existing `docs/**/index.html` file.
- No canonical URL contains `#`.
- Course/story pages now have route-specific `<title>`, description, canonical, OG/Twitter URL, and JSON-LD.
- `node --check` passes for `src/assets/app.js` and `docs/assets/app.js`.
- `python3.11 -m py_compile` passes for `scripts/make_seo.py`, `scripts/build_pages.py`, and `scripts/site_config.py`.

## P1 - Prerendered body content is hidden and creates duplicate IDs

### Evidence

- `scripts/build_pages.py:280-286` defines `SHOW_ROUTE_STYLE_TMPL`, but generated pages do not include that style.
- The injected prerender snippet sits inside a `<section hidden>`:
  - `docs/stories/anh-dang-microsoft/index.html:703-706`
  - `docs/courses/cracking-machine-coding-low-level-design-round/index.html:605-608`
- CSS hides all hidden route sections with `display: none !important` at `src/assets/style.css:3685-3686`.
- Generated pages now have duplicate IDs:
  - `docs/stories/anh-dang-microsoft/index.html:706` and `docs/stories/anh-dang-microsoft/index.html:709` both use `id="storyArticle"`.
  - `docs/courses/cracking-machine-coding-low-level-design-round/index.html:608` and `docs/courses/cracking-machine-coding-low-level-design-round/index.html:611` both use `id="courseArticle"`.
- A full generated-page scan found duplicate `courseArticle`/`storyArticle` IDs on 104 pages.

### Impact

The source contains prerendered text, but first paint without JS still hides it. Duplicate IDs also make the HTML invalid and can cause `document.getElementById(...)` to target the injected snippet rather than the intended SPA mount node.

### Suggested Fix

Use one mount node per route:

1. Inject prerender content inside the existing `#courseArticle` / `#storyArticle` element instead of adding a second element with the same ID.
2. Add a per-page prerender style that reveals the intended route before JS loads, or remove the `hidden` attribute for that page's route in the generated HTML.
3. Ensure the SPA hydration replaces/enhances the same node instead of creating duplicate visible content.

## P1 - Prerender bootstrap mutates clean URLs back into hash URLs

### Evidence

- `scripts/build_pages.py:236-250` injects a script that sets `location.hash = "#course/..."` or `"#story/..."`.
- The generated page includes it at `docs/stories/anh-dang-microsoft/index.html:170-184`.
- There is no corresponding `history.replaceState(...)` cleanup in `src/assets/app.js`.

### Impact

Opening a clean URL like `/stories/anh-dang-microsoft/` will be mutated by JS to `/stories/anh-dang-microsoft/#story/anh-dang-microsoft`. That reintroduces fragment URLs in the browser, weakens the clean-route UX, and can create duplicate share URLs.

### Suggested Fix

Remove the bootstrap hash mutation. `src/assets/app.js:163-170` already resolves routes from `location.pathname`, so the hash pre-seed should not be needed. If a bootstrap remains, it must use `history.replaceState` to keep the visible URL clean.

## P1 - English hreflang URLs are still not true standalone English pages

### Evidence

- Generated pages advertise English alternates via query strings:
  - `docs/stories/anh-dang-microsoft/index.html:49-50`
  - `docs/courses/cracking-machine-coding-low-level-design-round/index.html:49-50`
- `src/assets/app.js:5-13` now reads `?lang=en`, which is good.
- But the HTML response for `?lang=en` is still the same Vietnamese source and canonicalizes to the non-query URL:
  - `docs/stories/anh-dang-microsoft/index.html:27`
  - runtime canonical is also rebuilt without query at `src/assets/app.js:270-274`.

### Impact

Google can render JavaScript, but the English URL is canonicalized to the Vietnamese URL, so the English alternate may not be treated as an indexable language variant. Social crawlers and simpler bots will also see Vietnamese title/description for the English alternate.

### Suggested Fix

Either:

1. Generate real English pages, e.g. `/en/`, `/en/courses/<slug>/`, `/en/stories/<slug>/`, with English source HTML, `html lang="en"`, self-canonical English URLs, and reciprocal hreflang.
2. Or temporarily remove `hreflang="en"` until English pages are truly canonical and source-rendered.

## P2 - Social preview tags are partially generic or inconsistent

### Evidence

- Story page OG image is WebP, but `og:image:type` remains `image/png`:
  - `docs/stories/anh-dang-microsoft/index.html:29-31`
  - scan result: 96 pages have an OG image MIME mismatch.
- Zalo tags remain generic on route pages:
  - `docs/stories/anh-dang-microsoft/index.html:45-46`
  - scan result: 113 non-home pages still use generic Zalo title/image.
- `og:type` is `website` on all 114 generated pages, including story article pages:
  - `docs/stories/anh-dang-microsoft/index.html:18`

### Suggested Fix

- Patch `og:image:type` based on the selected image extension or omit it when uncertain.
- Patch `zalo:title` and `zalo:image` alongside OG/Twitter route metadata.
- Use `og:type="article"` for story pages; keep `website` for listings/home, and choose the closest appropriate type for course pages.

## P2 - Stories route JS SEO description still says 95+

### Evidence

- Source data now has 94 stories.
- Static i18n and generated `/stories/` metadata use 94.
- Runtime route description still says 95+ at `src/assets/app.js:254`.

### Suggested Fix

Use `stories.length` or a shared count constant in `updateSeoForRoute` so rendered metadata cannot drift from source data.

## Acceptance Criteria

- Generated pages have no duplicate IDs.
- Prerendered route content is visible in a no-JS render.
- Opening `/courses/<slug>/` or `/stories/<slug>/` does not append a hash.
- English alternates are either fully source-rendered and self-canonical, or removed until supported.
- Zalo/OG/Twitter metadata all match the route page.
- `og:image:type` matches the actual image MIME type or is omitted.
