# FIXED — P1 - Reconcile Course Inventory Across Data, README, PLAN, and Copy

**Status: FIXED** (2026-05-30)

## Resolution

The intended state is **10 courses** (15 crawled, 5 explicitly excluded via `EXCLUDED_SLUGS` in `scripts/crawl_courses.py`). Docs updated:

- `README.md:18` → `10 courses crawled from blog pages (5 internally-excluded slugs in scripts/crawl_courses.py)`
- `PLAN.md:24` → `10 courses (15 crawled from /blogs/khoa-hoc pages 1-4, 5 excluded in scripts/crawl_courses.py)`
- `Makefile` help text → `make crawl-courses   Just the course pages (~10 after EXCLUDED_SLUGS) → src/assets/courses-data.js`
- Live count on `#courses` page is dynamic from `courses.length` via `refreshLiveCounts()`.

The user explicitly asked to drop those 5 courses on 2026-05-30 ("Bỏ khoá nè hộ: [PREMIUM COURSE] LC 4.5 …, Tiếng Anh Giao Tiếp …, Introduction to Programming …, OOP + Database Design, FRONT END"). Decision is documented.

---



Claude, course inventory is inconsistent across the project.

## Evidence

- `src/assets/courses-data.js` currently contains `10` courses.
- `README.md:18` says `15 courses crawled from all 4 blog pages`.
- `PLAN.md:24` and `PLAN.md:34-57` document 15 courses.
- `scripts/crawl_courses.py` intentionally excludes 5 slugs via `EXCLUDED_SLUGS`, so the 10-course output may be intentional but the docs were not updated.
- Current excluded slugs:
  - `premium-course-lc-4-5-dsa-intensive-training-tai-engineer-pro`
  - `khoa-tieng-anh-giao-tiep-danh-rieng-cho-software-engineer`
  - `introduction-to-programming-with-python-java`
  - `oop-database-design`
  - `khoa-hoc-front-end`

## Suggested Fix

1. Decide whether the site should show 10 courses or all 15.
2. If 10 is intentional:
   - Update README and PLAN.
   - Document why each excluded course is excluded.
   - Ensure public copy says 10/dynamic count consistently.
3. If 15 is required:
   - Remove/update `EXCLUDED_SLUGS`.
   - Re-run the course crawler.
   - Add English title/blurb entries in `courses-i18n.js` for restored courses.
4. Add a simple content inventory check so docs do not drift again.

## Acceptance Criteria

- Course count is consistent in `src/assets/courses-data.js`, README, PLAN, and the UI.
- Excluded courses are either visible or explicitly documented as intentionally hidden.
- English course card translations exist for every visible course.
