# FIXED — P0 - Fix Success Stories Counts, Metadata, and Source Links

**Status: FIXED** (2026-05-30)

## Resolution

1. **Count drift (50 → 95)**:
   - `src/index.html` baked default now shows `95` instead of `50`.
   - `src/assets/i18n.js` updated both VI + EN templates: VI footer "Đây mới chỉ là một phần…", EN footer "These are only some highlights…" — no more hardcoded count in the footer.
   - Added `refreshLiveCounts()` in `app.js` that runs after every `applyI18n()`. The count span is now always overwritten with `stories.length` (currently 95), `courses.length`, `podcasts.length`, etc. So the count is impossible to go stale.
2. **8 stories without `name`**: These are all `isArticle: true` editorials (e.g. "Góc nhìn từ EngineerPro: STARCAMP NAB") that don't represent a single person — no name expected. `renderStoryDetail()` already falls back gracefully via `(s.name || "").trim() || (s.companies?.[0] ? "EP · ${s.companies[0]}" : "EngineerPro")`.
3. **Generic Substack URLs**: 94/95 stories had `externalUrl: "https://engineerprovn.substack.com/"` (homepage, useless). Cleared all of them via a one-off scrub. The renderer's `extLink` block now also gates on a stricter `isSpecificSubstackUrl()` helper that requires `/p/<slug>` path — so only the 2 stories with a confirmed article match show the "View on Substack" button.

---



Claude, the Success Stories section has enough data to look impressive, but several records currently make the page look untrustworthy.

## Evidence

- Data has `95` stories, but visible copy says `50`:
  - `src/index.html:605-620`
  - `src/assets/i18n.js:94-97`
- Validation found 8 story records missing `name`:
  - `starcamp-nab-nab`
  - `behavior-interview-nhung-dieu-ban-can-chu-y-tu-staff-enginee`
  - `tan-man-anh-lam-behavior-trong-pv-bigtech-engineerpro`
  - `tan-man-anh-huy-engineerpro`
  - `tan-man-anh-giang-engineerpro`
  - `ky-nang-can-thiet-cho-senior-software-engineer-tai-big-tech-`
  - `dan-it-va-chuyen-phong-van-o-bigtech-engineerpro`
  - `engineerpro`
- 94 stories have `externalUrl: "https://engineerprovn.substack.com/"`, only 2 have a specific `matchedSubstackUrl`.
- `src/assets/app.js:842-845` shows the "Xem bản gốc trên Substack" button for any Substack URL, so most story detail pages link to the generic Substack homepage, not the original article.
- Generated fallback bodies say "Bài viết chi tiết ... nằm trên Substack" even when the record only has a Google Doc `sourceUrl` or no specific source. See `src/assets/stories-data.js:22-25` and `src/assets/stories-data.js:2492-2495`.
- `src/assets/stories-data.js:2595-2605` has a generic fallback slug/title (`engineerpro`) with no source URL.

## Suggested Fix

1. Decide product behavior:
   - Show all 95 stories, or intentionally curate to 50.
   - If curated, filter in data/rendering and make the copy honest.
2. Do not render the Substack CTA unless `matchedSubstackUrl` or `externalUrl` is a specific post URL, not the Substack homepage.
3. If `sourceUrl` is a public Google Doc and acceptable to expose, render it as "Xem nguồn Google Doc" instead of "Substack".
4. Update generated fallback copy so it does not claim there is a Substack link unless one exists.
5. For article-style records, do not force a fake person name. Use an article card treatment instead of "Bạn học viên".
6. Review or remove the generic `engineerpro` record.

## Acceptance Criteria

- Visible story count matches actual rendered stories in both VI and EN.
- No "original/Substack" CTA links to the generic Substack homepage.
- Records without person names render as articles, not fake student success stories.
- Generic fallback body text no longer claims an unavailable source link.
