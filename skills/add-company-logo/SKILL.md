---
name: add-company-logo
description: Add a company logo to the home-page marquee strip — save the raster image, generate a monochrome mask via mask_logos.py, register it in data.js, rebuild. Use when the user sends a company logo image or says "thêm logo X" / "add logo".
---

# Add a company logo to the marquee

## When SVG is available (prefer)

If the company has a clean SVG (Google, Meta, IBM, etc.) — drop it at `src/assets/img/companies/<name>.svg` and add to `data.js` directly:

```js
{ name: "AcmeCorp", logo: "assets/img/companies/acmecorp.svg" },
```

The marquee uses CSS `mask-image: url(...)` + `background: currentColor`, so the SVG must be a single-color silhouette (paths use `currentColor` or `fill="#000"`).

## When only a raster logo (PNG / JPG) is available

The user usually sends a PNG with a colored brand background. We convert it to a monochrome silhouette via `scripts/mask_logos.py`.

### Steps

1. **Save the raw image** to `src/assets/img/companies/<name>.png` (keep extension as-is).
2. **Inspect the logo** to identify foreground vs background color:
   ```python
   from PIL import Image
   im = Image.open('src/assets/img/companies/<name>.png')
   print('size:', im.size, 'mode:', im.mode)
   print('center:', im.getpixel((im.size[0]//2, im.size[1]//2)))
   print('corner:', im.getpixel((10, 10)))
   ```
3. **Register a mask job** in `scripts/mask_logos.py` `JOBS` list:
   ```python
   {"src": "<name>.png", "mode": "fg", "color": (R, G, B), "threshold": 200, "out": "<name>-mask.png"},
   ```
   - `mode: "fg"` → keep pixels close to `color` (good when logo is on a solid background; `color` = the logo color itself).
   - `mode: "bg"` → drop pixels close to `color`, keep everything else (good when background is white but logo is multi-color; `color` = the white).
   - `threshold` around 150–220 usually works; raise if the silhouette has holes, lower if it leaks.
4. **Run it**: `python3.11 scripts/mask_logos.py 2>&1 | grep -i <name>` — confirms output filename + size.
5. **Verify visually**: read the generated `src/assets/img/companies/<name>-mask.png` and check the silhouette is clean.
6. **Register in `src/assets/data.js`** at the end of `companies: [...]`:
   ```js
   { name: "AcmeCorp", logo: "assets/img/companies/acmecorp-mask.png" },
   ```
7. **Build + push**:
   ```bash
   EP_BASE_URL=https://engineerpro-team.github.io \
   EP_BASE_PATH=/interview-trainings \
   make github
   git add -A && git commit -m "Add company logo: <Name>" && git push
   ```

## Examples already in the repo

See the `JOBS` list at `scripts/mask_logos.py:23` for working examples:
- **fg + black** (Robinhood): `(0, 0, 0), threshold: 200`
- **fg + white** (Goldman Sachs, SAP, OKX, Employment Hero): `(255, 255, 255), threshold: 80-90`
- **fg + brand color** (Shopee `(238, 77, 45)`, ANZ `(0, 130, 200)`, Axon `(255, 220, 0)`, Naver `(3, 199, 90)`, WorldQuant `(10, 10, 10)`)
- **bg + white** (Cognizant): `(255, 255, 255), threshold: 120` — when logo has multiple colors but white background to drop

If neither mode works cleanly, manually trace the logo in Figma → export single-color SVG → register as SVG (skip masking entirely).

## Note

The `<img>` raster source PNG stays in `src/assets/img/companies/` for re-running the mask if `mask_logos.py` parameters need tuning. It's not orphan — don't delete.
