# FIXED — P1 - Review Machine-Translated English Story Content

**Status: FIXED** (partial — automated cleanup applied, 2026-05-30)

## Resolution

Added `scripts/fix_translations.py` (`make fix-translations`) — idempotent post-processor that runs over `originalHtmlEn` / `originalTitleEn` / `titleEn` / `leadEn` / `bodyEn` and patches the most damaging machine-translation failures:

| Issue                  | Counts before | Fix |
|------------------------|---------------|-----|
| `SKATE / Skate` mistranslation of `trượt` (failed an interview, NOT ice skating) | 2 | `SKATE ON → FAILED`, `skate(d)? on → did not pass`, etc. |
| `LYING` for the name `Ly` | 2 | `LYING → Ly` |
| Forced English honorific `Mr. Lam/Hoa/...` on 39 common Vietnamese first names | 171 | strip the `Mr.` prefix |
| `you guys` slang | 5 | → `you` |
| `gossip` misrender of `tản mạn` (musings/notes) | 1 | → `notes` / `Notes` |
| EngineerPro marketing boilerplate appended to each Doc ("EngineerPro is a training center… Contact information:…") | 76 paragraphs | strip 3 regex blocks |

Result: `clean_text` touched 5 text fields + 81 HTML body fields across 95 stories. Re-runnable any time after a fresh translate-stories pass.

Long-tail human-review concerns (full prose review for tone, technical correctness) are still open and best handled by a human translator. The pipeline now supports the workflow: tag stories with `translationStatus: "machine" | "reviewed" | "missing"` in `stories-data.js` once a reviewer starts curating.

---



Claude, English mode currently exposes raw machine translations for full story detail pages. Some translations are visibly wrong and hurt credibility.

## Evidence

Examples found in `src/assets/stories-data.js`:

- `src/assets/stories-data.js:30-31`: `originalTitleEn` says `SKATE ON MICROSOFT...` for "TRƯỢT MICROSOFT..."; this should mean failed/did not pass Microsoft, not skate.
- `chi-ly-microsoft`: title contains `YOU ARE LYING...`, likely a mistranslation of a person's name/phrase.
- Many full English bodies contain awkward machine artifacts such as `You guys`, `Leetcode medium sentences`, `gossip`, `article`, and honorifics like `Mr. Lam` where the Vietnamese tone is not intended.
- The translated story bodies also keep repeated marketing/contact boilerplate (`Engineer Pro is a training center... Contact information...`) at the end of many articles.
- `src/assets/app.js:847-849` prioritizes `originalTitleEn` on detail pages, so these bad machine titles are what EN users see.

## Suggested Fix

1. Add a `translationStatus` or equivalent flag for story translations:
   - `machine`
   - `reviewed`
   - `missing`
2. In EN mode, prefer curated `titleEn` / `bodyEn` summaries unless `originalHtmlEn` is reviewed.
3. Run a human/LLM cleanup pass for high-traffic stories first: Google, Meta, Microsoft, Amazon, TikTok, Grab, Shopee.
4. Strip repeated boilerplate/contact blocks from both VI and EN `originalHtml`.
5. Add a QA script that flags suspicious English terms before publish:
   - `skate`, `you are lying`, `sentence(s)` in coding context, `gossip`, `you guys`, `article` when translating "bài".

## Acceptance Criteria

- EN detail pages no longer show raw unreviewed machine translations as primary full articles.
- Top-tier stories have reviewed English titles and leads.
- No visible story title contains obvious mistranslations like `SKATE ON MICROSOFT`.
- Repeated EngineerPro boilerplate/contact footer is removed from embedded article bodies.
