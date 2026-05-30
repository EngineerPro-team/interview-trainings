---
name: update-content-counts
description: Update hero/section stat numbers (students, offers, YouTube/Substack subscribers, years operating) and verify all dependent counts stay in sync via `make stats`. Use when the user gives a new stat number (e.g. "10.9K YouTube") or wants to refresh hero numbers.
---

# Update content / hero counts

## Two flavours of counts

| Kind | Source of truth | Drift-safe? |
|---|---|---|
| **Data-driven** (mentor/story/course/podcast/faq counts) | Length of array in `*-data.js` | ✅ yes — runtime `refreshLiveCounts()` overwrites every `<span id="*Count">` after each i18n apply |
| **Manual stat strip** (2K+ students, 500+ offers, 10.9K+ YouTube, 1.6K+ Substack, N years) | `src/index.html` hero stats block | ❌ no — manual numbers |

## Update a manual stat

Hero stats live in `src/index.html`. Find by class `stat__num`:

```html
<div class="stat">
  <div class="stat__num">10.9K+</div>
  <div class="stat__label" data-i18n="stats.youtube">YouTube subscribers</div>
</div>
```

Change the number inline. Then:

```bash
EP_BASE_URL=https://engineerpro-team.github.io \
EP_BASE_PATH=/interview-trainings \
make github

git add -A && git commit -m "Stats: bump <metric> <old> → <new>" && git push
```

The "years" stat is computed at runtime from the founding date `2023-04-26` — don't hand-edit. See `app.js` `setStats()` IIFE.

## Update data-driven count

Don't edit `<span id="*Count">` directly — it's recomputed from `data.mentors.length` etc. at runtime. Instead, edit the underlying data file and `make stats` will catch any stale text references.

```bash
make stats   # auto-audit; non-zero exit = drift somewhere
```

The audit covers: `src/index.html` `<span id="*Count">` defaults, `src/assets/i18n.js` templates, runtime `ROUTE_DESC` in `app.js`, `scripts/build_pages.py` route descriptions, README/PLAN prose.

When `make stats` reports drift, it shows `file:line  expected N, got M` — just bump it.

## After updating

`make github` runs `make stats` as a precondition, so the build will fail if any text reference is stale. Fix and re-run.
