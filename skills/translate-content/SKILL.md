---
name: translate-content
description: Translate or re-translate Vietnamese content to English — stories, courses, or new sections. Covers the Google Translate free-endpoint pattern, post-process cleanup, and EN-side audit. Use when the user says "dịch sang English", "translate", or notices VI text leaking into EN mode.
---

# Translate content to English

The site is bilingual VI ↔ EN. Three layers of translation strategy:

## Layer 1: Static UI strings → `src/assets/i18n.js`

Hand-written EN dictionary. Add to both `vi:` and `en:` blocks; `make github`'s `make stats` won't catch parity drift but the build will reference `t("key")` and fall back to VI if EN is missing.

When you add a new `data-i18n="X"` attribute in HTML or a new `t("X")` call in JS, you MUST add the matching key in BOTH `vi:` and `en:` blocks in `i18n.js`.

## Layer 2: Curated content with hand EN siblings

Some data files have parallel `xxxEn` fields written by hand:

- `src/assets/data.js`: roadmap stages (`titleEn`/`subtitleEn`/`goalEn`/`blurbEn` per module), partners (`taglineEn`/`descriptionEn`/`quoteEn`/`ctaEn`/`statsEn`/`mentorsEn`), book (`highlightsEn`).
- `src/assets/courses-i18n.js`: per-course `title` + `blurb` keyed by slug.
- `src/assets/resources-i18n.js`: foundation + cv strings keyed by purpose.
- `src/assets/faqs-data.js`: each FAQ has `questionEn` + `htmlEn` (populated by `scripts/translate_faqs.py`).

Renderer pattern (search in `app.js`):
```js
const en = currentLang === "en";
const label = (en && obj.fooEn) ? obj.fooEn : obj.foo;
```

## Layer 3: Long-form HTML via Google Translate free endpoint

For full course bodies (`courses-data.js#html`) and story bodies (`stories-data.js#originalHtml`), translation is automated via scripts that hit `translate.googleapis.com/translate_a/single`. Both scripts use the same battle-tested pattern:

| Script | Source field | Output field | Target | Time |
|---|---|---|---|---|
| `scripts/translate_courses.py` | `html` | `htmlEn` | `courses-data.js` | ~60s for 10 |
| `scripts/translate_stories.py` | `originalHtml`, `originalTitle` | `originalHtmlEn`, `originalTitleEn` | `stories-data.js` | ~8min for 94 |

Both are **idempotent** — re-running skips records that already have the EN field.

### Make targets

```bash
make translate-courses    # 10 courses → adds htmlEn
make translate-stories    # 94 stories → adds originalHtmlEn + originalTitleEn
make fix-translations     # post-process common MT artifacts
```

### Translation strategy (in case you write a new translator)

The shared pattern in both scripts:

1. Parse HTML with BeautifulSoup, collect every visible text node (skip `<script>`/`<style>`).
2. Batch text nodes into chunks ≤ 3500 chars, joined with sentinel `\n\n@@SPLIT@@\n\n` — Google Translate preserves this sentinel verbatim.
3. POST chunk to free endpoint, split on sentinel, recompose HTML.
4. Preserve leading/trailing whitespace per text node (Google trims).
5. Save to disk every N records so a mid-run failure doesn't lose work.

### MT artifacts and how to fix them

`scripts/fix_translations.py` is a post-processor with a `SUBS` list of regex substitutions for known artifacts:

| Vietnamese source | Bad MT output | Fix in `SUBS` |
|---|---|---|
| `trượt` (failed an interview) | `SKATE` | `SKATE → FAILED` |
| `Ly` (person name) | `LYING` | `LYING → Ly` |
| Vietnamese first names | `Mr. Lam`, `Mr. Hoa`, ... | strip `Mr.` |
| `các bạn` (plural-you) | `you guys` | `you guys → you` |
| `tản mạn` (musings) | `gossip` | `gossip → notes`; in titles use `Reflections` |
| `Bạn học viên` (anonymous fallback) | left as VI | `Our student` / `our student` |
| EngineerPro marketing footer | left as-is | strip 3 regex blocks |

When you find a new artifact, add a `(re.compile(...), "replacement")` tuple to `SUBS` in `fix_translations.py`, then run `make fix-translations`. Idempotent.

## EN-side audit

Quick check that EN-tagged fields don't contain stray Vietnamese:

```bash
python3.11 -c "
import json, re
VI = re.compile(r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀ-Ỹ]')
# Adapt path/var as needed
with open('src/assets/stories-data.js') as f:
    data = json.loads(re.search(r'window\.STORIES\s*=\s*(\[.*\]);', f.read(), re.S).group(1))
for s in data:
    for k in ('titleEn','leadEn','originalTitleEn'):
        v = s.get(k) or ''
        if VI.search(v): print(s['slug'], k, v[:80])
"
```

Note: proper names (Anh Đăng, Chị Ly, Cốc Cốc, etc.) legitimately keep their diacritics in EN — don't try to anglicise them.
