# FIXED — P1 - Fix Programming Foundation Video Order

**Status: FIXED** (2026-05-30)

## Resolution

1. `scripts/crawl_resources.py` now sorts the `foundation` playlist by lesson number extracted from titles `(?:Foundation|Lesson|Episode|Tập|Phần)\s+(\d+)` — strictly ascending. Falls back to 10_000 for any title without a number (sorted to the end).
2. Also normalises the well-known double-paren typo `Foundation 6: Array Part 2 ((With…` → `(With…`.
3. Same sort + typo-fix applied in-place to the current `src/assets/resources-data.js` (no need to re-crawl). Order is now strictly `1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16`.
4. The renderer's `#01`, `#02`, … indices now line up with the lesson numbers.

---



Claude, the Resources page lists Programming Foundation videos out of lesson order. Because the UI numbers cards by array index, this makes the curriculum look scrambled.

## Evidence

`src/assets/resources-data.js:10-120` orders the foundation playlist as:

`1, 6, 13, 15, 9, 7, 14, 4, 11, 16, 8, 10, 2, 5, 12, 3`

The app renders `#01`, `#02`, etc. from the array index in `src/assets/app.js:1195-1213`, so the second displayed card is labeled `#02` but its title is `Programming Foundation 6`.

`scripts/crawl_resources.py:83-108` takes the first nested `contents` block containing `playlistVideoRenderer`; YouTube's embedded JSON order is not guaranteed to be the visible playlist order.

## Suggested Fix

1. Sort `foundation.videos` by the lesson number extracted from `Programming Foundation N`.
2. Prefer a real playlist position field from `playlistVideoRenderer` if available; fall back to title number.
3. Normalize minor title typo while regenerating: `Programming Foundation 6: Array Part 2 ((With...` has double `((`.
4. Add a validation check that fails if extracted lesson numbers are not strictly ascending.

## Acceptance Criteria

- Foundation videos render in order `1..16`.
- UI index matches the lesson number.
- Regenerating `src/assets/resources-data.js` preserves the correct order.
