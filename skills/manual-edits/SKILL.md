# manual-edits

## When to use
Whenever you hand-curate a field on a story (replace a cover for IP safety,
scrub a real name from an anonymous post, rewrite a lead, fix machine-translated
EN body, etc.) — tag the story with a `manualEdits` array so future runs of
`make parse-stories` / `make crawl-story-images` / `make translate-stories`
don't silently undo your work.

## Schema

In `src/assets/stories-data.js`, each story object can carry:

```json
{
  "slug": "anh-quang-naver",
  "anonymous": true,
  "manualEdits": ["cover", "coverFrom", "lead", "leadEn",
                  "name", "originalHtml", "originalHtmlEn"]
}
```

Any field name listed here is "frozen" — the pipeline scripts read it but
never overwrite it.

## Which scripts honour the lock

| Script | Checked locks | Behaviour |
|---|---|---|
| `scripts/parse_stories.py` | every field in `manualEdits` | After generating the new row, copies the locked values forward from the previous `stories-data.js` before writing |
| `scripts/crawl_story_images.py` | `cover` | Skips the entire cover-resolution block — neither downloads Substack covers nor regenerates a placeholder |
| `scripts/translate_stories.py` | `originalHtmlEn` | Skips the GT translate call so a hand-curated EN body is never clobbered |

`scripts/fix_translations.py` is a pure text-cleanup pass and runs
unconditionally — that's fine since it never invents new content.

## Snapshot of locks set on 2026-05-31

| Field | Stories | Why |
|---|---|---|
| `cover`, `coverFrom` | 11 | Cover regenerated as original artwork because the crawled banner included a 3rd-party photo / logo we don't own. |
| `lead`, `leadEn`, `name`, `originalHtml`, `originalHtmlEn` | 45 | Anonymous students — real names scrubbed from snippets, byline, and body. `name_real` keeps the original value for internal records. |

Run `python3 -c "import re,json; raw=open('src/assets/stories-data.js').read(); data=json.loads(re.search(r'window\.STORIES\s*=\s*(\[.*\]);',raw,re.S).group(1)); print(sum(1 for s in data if s.get('manualEdits')))"` to see the current total.

## Adding a new lock

1. Make the edit in `stories-data.js` (cover swap, copy rewrite, etc.).
2. Add the field name(s) to that story's `manualEdits` array — create it
   if it doesn't exist. Sort alphabetically for diff-friendliness.
3. If you replaced an asset, **keep the original filename** so prerendered
   HTML / og:image URLs in `docs/` don't need rebuilding.
4. `make github && make local-build` then commit the data file + asset
   together. Mention `manualEdits` in the commit message.

## Removing a lock

Just delete the field name from the `manualEdits` array (or delete the
array entirely if empty). Next `make parse-stories` / re-crawl will then
freely overwrite the field again from the upstream source.
