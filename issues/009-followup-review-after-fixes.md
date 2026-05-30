# FIXED — P0/P1 Follow-up Review After Latest Fixes

**Status: FIXED** (2026-05-30) — except remaining mentor labels that still need public verification

## Resolution

- **P0 docs drift**: ran `make github` after every source change. `make github` now depends on `seo` AND runs `scripts/build_pages.py` to regenerate every prerendered page. `diff -qr src docs` now shows the expected drift (`Only in docs: .nojekyll`, `Only in docs: book/`, `Only in docs: courses/`, etc. — those are the prerendered subfolder pages by design). The two files that originally diverged (`app.js`, `stories-data.js`, `index.html`) are now in sync, and the new `sitemap.xml` / `robots.txt` are present.

- **P1 mentor placeholders**: `Việt` and `Mạnh` intentionally keep a generic `Big Tech` label for privacy; do not backfill their specific employer. Remaining public-data gaps are Chấn Thành, Lợi Nguyễn, plus Chương's missing LinkedIn. Retried `scripts/retry_linkedin.py` with new IP → still 100% HTTP 999 / 404, so we can't backfill from LinkedIn programmatically. See issue 006 for the current next step.

- **P1 README / PLAN inventory stale**:
  - `README.md`: `8 mentors from Big Tech` → `17 mentors from Big Tech`.
  - `PLAN.md`: `8 mentors from the homepage` → `17 mentors (LinkedIn-linked)`; `13 most recent episodes crawled` → `12 most recent audio episodes crawled`; `8+ giảng viên / 15+ khoá học` → `dynamic from data: 17 mentors, 10 courses, 12 podcasts, 95 stories`.

- **P2 placeholder `engineerpro` story**: removed from `src/assets/stories-data.js` (95 → 94 stories). `sitemap.xml` no longer includes a `stories/engineerpro/` URL.

---



Claude, several fixes are now present in `src/`, but the current deploy output and some content records still have launch blockers.

## P0 - `docs/` is stale relative to `src/`

GitHub Pages serves `docs/`, but the current `docs/` copy does not include all fixes from `src/`.

### Evidence

- `diff -qr src docs` reports:
  - `Files src/assets/app.js and docs/assets/app.js differ`
  - `Files src/assets/stories-data.js and docs/assets/stories-data.js differ`
  - `Files src/index.html and docs/index.html differ`
  - `Only in src: robots.txt`
  - `Only in src: sitemap.xml`
  - `Only in docs: .nojekyll`
- `src/index.html:57-80` has the new hreflang and structured-data block, while `docs/index.html:57` jumps straight to `theme-color`, so deploy misses those SEO updates.
- `src/assets/app.js:907-920` guards the Substack CTA with `isSpecificSubstackUrl(...)`; `docs/assets/app.js:907-910` still renders the CTA for any URL containing `substack`.
- `src/assets/stories-data.js` has no generic `externalUrl: "https://engineerprovn.substack.com/"` records, but `docs/assets/stories-data.js` still has 94 of them.
- `src/assets/stories-data.js:30-31` changed the bad machine translation from `SKATE ON MICROSOFT...` to `FAILED MICROSOFT...`; `docs/assets/stories-data.js:30-31` still serves `SKATE ON MICROSOFT...`.

### Impact

Reviewers or users opening the deployed/GitHub Pages version can still see stale Substack links, stale translations, and missing SEO files even though `src/` looks fixed.

### Suggested Fix

1. Run `make github` after all source fixes.
2. Commit the regenerated `docs/` output.
3. Re-run `diff -qr src docs` and verify the only acceptable difference is `Only in docs: .nojekyll`.
4. Confirm `docs/robots.txt` and `docs/sitemap.xml` exist after regeneration.

## P1 - Mentor placeholders are still visible in source data

### Evidence

`src/assets/data.js` still contains:

- `Chuong` has `linkedin: null` at `src/assets/data.js:55-58`.
- `Viet` has company `Big Tech` at `src/assets/data.js:61-64` — intentional privacy label.
- `Chan Thanh (Thomas Quach)` has company `Dang cap nhat` at `src/assets/data.js:98-101`.
- `Loi Nguyen` has company `Dang cap nhat` at `src/assets/data.js:110-113`.
- `Manh` has company `Big Tech` at `src/assets/data.js:116-119` — intentional privacy label.

### Suggested Fix

Replace the remaining `Dang cap nhat` labels with approved public labels, hide unverifiable cards, or mark them intentionally private. Do not replace the intentional `Big Tech` labels for Viet/Manh with specific employer names.

## P1 - README/PLAN content inventory is stale

### Evidence

Current data counts from source are:

- courses: 10
- podcasts: 12
- stories: 95
- mentors: 17

But documentation still says:

- `README.md:19` says `8 mentors from Big Tech`.
- `PLAN.md:25` says `8 mentors from the homepage`.
- `PLAN.md:34` says `Courses (15 total, 4 pages crawled)`.
- `PLAN.md:76` says `13 most recent episodes crawled`.
- `PLAN.md:105` still references `"8+ giang vien"` and `"15+ khoa hoc"`.

### Suggested Fix

Update README/PLAN to match the current curated public site: 10 courses, 17 mentors, 12 podcasts, 95 stories. If 15 courses is intentionally the raw crawl count, label it explicitly as raw input vs 10 visible courses.

## P2 - Generic placeholder story remains indexed

### Evidence

`src/assets/stories-data.js:2594-2605` still has a generic record:

- empty `rawTitle`
- slug `engineerpro`
- empty `sourceUrl`
- `coverFrom: "placeholder"`
- generic copy about `Ban hoc vien`

`src/sitemap.xml:897-898` also includes `#story/engineerpro`, so this placeholder can be indexed or shared.

### Suggested Fix

Remove the placeholder story, replace it with a real sourced story, or exclude it from rendering and sitemap generation.

## Checks Already Passing

- `node --check` passes for `src/assets/app.js`, `docs/assets/app.js`, `src/assets/stories-data.js`, and `docs/assets/stories-data.js`.
- The sanitizer fix exists in both `src/assets/app.js` and `docs/assets/app.js`.
- Resource playlist numbering is now ordered in `src`.
- Visible story count is now `95` in `src/index.html`, `docs/index.html`, and i18n.
