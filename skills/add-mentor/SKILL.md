---
name: add-mentor
description: Add a new mentor to the EngineerPro mentor grid — save + crop their photo, add a `data.js` entry, bump every count reference, build, push. Use when the user sends a mentor photo + LinkedIn / company info, or says "thêm mentor" / "add mentor".
---

# Add a new mentor

## Inputs you need from the user

1. Photo (any aspect ratio — script crops to 400×400 center-square).
2. Display name (e.g. "Đông Trương" — keep Vietnamese diacritics).
3. LinkedIn URL.
4. Current role + company (e.g. "Software Engineer @ Uber USA").
5. Optional ex-role + ex-company (e.g. "ex-Staff Engineer @ OKX").

If the user only sends a photo + name, ask once for role/company, OR use the `"Đang cập nhật"` placeholder (`Coming soon` shows in EN automatically).

## Steps

### 1. Save + crop the photo

Filename convention: lowercase, hyphen-separated, derived from LinkedIn slug or user-provided handle. Save to `src/assets/img/mentors/<handle>.jpg`.

```python
from PIL import Image
im = Image.open('<user-supplied-path>').convert('RGB')
w, h = im.size
side = min(w, h)
# Center-square crop. For portrait photos where face is at the top,
# bias the top: top = max(0, int(h * 0.05))
im = im.crop(((w-side)//2, (h-side)//2, (w+side)//2, (h+side)//2)).resize((400, 400), Image.LANCZOS)
im.save('src/assets/img/mentors/<handle>.jpg', 'JPEG', quality=85, optimize=True)
```

Inspect the result. If the face is cropped out, redo with a biased crop (top/right/etc.).

### 2. Add the entry in `src/assets/data.js`

Append BEFORE the closing `],` of `mentors: [...]`:

```js
{
  name: "Đông Trương",
  photo: "assets/img/mentors/dong-truong.jpg",
  current:  { role: "Software Engineer",  company: "Uber (USA)" },
  previous: { role: "Staff Engineer",     company: "OKX" },          // or null
  linkedin: "https://www.linkedin.com/in/dong-truong-56297a145/",   // or null
},
```

### 3. Bump every mentor-count reference

`make github` runs `make stats` which fails the build if any count drifts. The references that need updating:

- `src/index.html`: `<span id="mentorsCount">N</span>`
- `src/assets/i18n.js`: two `<span id="mentorsCount">N</span>` (vi + en blocks)
- `src/assets/app.js`: any `ROUTE_DESC.mentors` literal (currently derived from `data.mentors.length` — verify)
- `scripts/build_pages.py`: `ROUTE_DESCRIPTIONS_VI` mentors entry
- `README.md`, `PLAN.md`: prose counts

Fastest path: bulk-substitute the old number → new number, then `make stats` will say what's stale.

```bash
OLD=19 NEW=20  # adjust
sed -i '' "s|mentorsCount\">$OLD</span>|mentorsCount\">$NEW</span>|g" src/index.html src/assets/i18n.js
sed -i '' "s|$OLD mentors|$NEW mentors|g" src/assets/i18n.js scripts/build_pages.py README.md PLAN.md
make stats   # zero exit = aligned
```

### 4. Build + push

```bash
EP_BASE_URL=https://engineerpro-team.github.io \
EP_BASE_PATH=/interview-trainings \
make github

git add -A
git commit -m "Add mentor: <Name> (<role> @ <company>)"
git push
```

GitHub Pages rebuilds in ~1 min. Tell the user to hard-reload.

## Existing photo-handle map (for reference)

`scripts/retry_linkedin.py` has the canonical LinkedIn-slug → local-filename map. Reuse those filenames if the LinkedIn slug already appears.
