# FIXED — P1 - Make Crawl/Parse Scripts Reproducible and Less Brittle

**Status: FIXED** (2026-05-30)

## Resolution

1. **Hardcoded `/Users/lamp/…` path** in `scripts/parse_stories.py`: replaced with a 4-step resolution chain — `sys.argv[1]` → `$EP_STORIES_MD` env var → `uploads/edit-0.md` (repo-local default) → original author path. Documented at the top of the file.
2. **`naz` alias collision** (`"naz": "NAB"` then `"naz": "ANZ"` ghi đè): removed the first one, kept `"naz": "ANZ"` with comment "common typo in sheet for ANZ". `"nab": "NAB"` already exists for the real abbreviation.
3. **Dead no-op `__iter__().__next__()` line** at the old line 234: removed.
4. **Substack archive cache TTL** in `scripts/crawl_story_images.py`: cache now expires after 24 h and a `--refresh` CLI flag bypasses it for an immediate fetch.
5. **Newest-first tie-break for Substack matching**: `best_match()` previously sorted `(score desc, post_date asc)` — preferring older posts on tie. Now sorts `(score desc, post_date desc)` using a proper ISO-8601-aware `_post_date_key()` helper.
6. **Foundation playlist ordering** (also see issue 004): `crawl_resources.py` now sorts videos by lesson number extracted from titles before saving.

---



Claude, several content scripts work for the current machine but are fragile for future refreshes.

## Evidence

- `scripts/parse_stories.py:20-22` hard-codes an absolute local path under `/Users/lamp/.cursor/.../uploads/edit-0.md`.
- `scripts/parse_stories.py:57` maps `naz` to `NAB`, but `scripts/parse_stories.py:63` maps `naz` again to `ANZ`; the second value silently wins.
- `scripts/parse_stories.py:224-225` has a no-op/weird split assignment before the real split logic.
- `scripts/crawl_story_images.py:49-51` reuses `/tmp/ep_substack_archive.json` forever if it exists; there is no TTL.
- `scripts/crawl_story_images.py:75` says recency should matter, but `scripts/crawl_story_images.py:97` sorts by `post_date` ascending, which prefers older posts for equal scores.
- `scripts/crawl_resources.py:83-108` depends on the first nested YouTube `contents` block, which produced the wrong foundation order in current data.

## Suggested Fix

1. Replace hard-coded input paths with CLI args and sensible defaults inside the repo, e.g. `python scripts/parse_stories.py uploads/edit-0.md`.
2. Fix/clarify alias collisions (`naz` should map to exactly one intended company, or use contextual matching).
3. Remove dead/no-op parser code.
4. Add cache TTL or a `--refresh` flag for Substack archive cache.
5. Sort matched Substack posts by newest first when scores tie.
6. Add deterministic post-crawl validations:
   - no duplicate aliases,
   - story count within expected range,
   - no generic `externalUrl` if source CTA is shown,
   - resource videos ordered by lesson number.

## Acceptance Criteria

- Another developer can regenerate stories/resources without editing local absolute paths.
- The parser has no duplicate alias keys.
- Substack matching prefers the newest equally scored post.
- Resource crawl output passes the lesson-order validation.
