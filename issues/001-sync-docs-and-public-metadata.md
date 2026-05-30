# FIXED — P0 - Sync `docs/` With `src/` Before Publishing

**Status: FIXED** (2026-05-30)

## Resolution

1. Ran `make github` — `docs/` now mirrors `src/` exactly. `diff -qr src docs` reports only `Only in docs: .nojekyll` (expected).
2. All 4 social card image URLs now absolute (`https://engineerpro-academy.github.io/assets/img/og-share.png`): `og:image`, `og:image:secure_url`, `twitter:image`, `zalo:image`.
3. Added `<link rel="canonical">` + `<meta name="twitter:url">` + `<meta property="og:locale:alternate" content="en_US">`.
4. `make github` now depends on `seo` target so sitemap.xml + robots.txt get regenerated on every build, never drift.
5. The github.io URL is still the placeholder `https://engineerpro-academy.github.io/` — replace before final deploy if a custom domain is wired up. Single source of truth: `src/index.html` head + `scripts/make_seo.py BASE`.

---



Claude, please fix the deployment output drift before any launch/review link is shared.

## Evidence

- `diff -qr src docs` currently reports:
  - `Only in src/assets: resources-i18n.js`
  - `Files src/index.html and docs/index.html differ`
  - `Only in docs: .nojekyll`
- The `docs/index.html` copy is older than `src/index.html`; it misses newer `data-i18n` attributes for Book/Resources and does not load `assets/resources-i18n.js`.
- `src/index.html:16-30` says OG/Twitter images should be absolute, but `og:image`, `og:image:secure_url`, and `twitter:image` are still relative (`assets/img/og-share.png`).
- `src/index.html:28` has `og:url` set to `https://engineerpro-academy.github.io/`, which may be a placeholder or wrong final URL.

## Why This Matters

GitHub Pages serves `docs/`, not `src/`. A reviewer can see stale UI/i18n even when `src/` is correct. Social previews can also fail or show the wrong domain/image.

## Suggested Fix

1. Apply all source fixes in `src/`.
2. Run `make github` so `docs/` is regenerated from `src/`.
3. Set the final canonical base URL once, then update:
   - `og:url`
   - `og:image`
   - `og:image:secure_url`
   - `twitter:image`
   - add `twitter:url` if we want parity with the comment.
4. Keep `.nojekyll` only in `docs/`.

## Acceptance Criteria

- `diff -qr src docs` reports only `Only in docs: .nojekyll`.
- `docs/index.html` loads the same JS files as `src/index.html`.
- All social image URLs are absolute and point to the deployed site.
- README deploy instructions still match the actual output.
