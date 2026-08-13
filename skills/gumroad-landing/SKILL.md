---
name: gumroad-landing
description: Build, preview, and publish the custom Gumroad product landing pages for Forty Seconds and Cafe Talk. Covers the build.py generator, the Gumroad CLI commands, the sanitizer allowlist, and the pricing/discount rules. Use when the user asks to edit, rebuild, or publish a Gumroad landing page, change the price display, or says "landing", "gumroad", "publish trang bán sách".
---

# Gumroad landing pages

Two published pages, both generated from one template so they never drift apart:

| Product | ID | Output file | Live URL |
|---|---|---|---|
| Forty Seconds: Ten Real CVs That Passed Big Tech | `8c0LPb6cFSN-w7PLMO4JTw==` | `landing.html` | https://engineerprovn.gumroad.com/l/Forty-Seconds-Ten-Real-CVs-That-Passed-Big-Tech |
| Cafe Talk: The Interview and Career Playbook | `jaehu` | `landing-cafe-talk.html` | https://engineerprovn.gumroad.com/l/cafe-talk-the-interview-and-career-playbook |

Each page foregrounds its own book and cross-sells the other one.

## Never hand-edit the HTML

`landing.html` and `landing-cafe-talk.html` are build artifacts. Edit the sources, then rebuild:

```
scripts/gumroad_landing/
  build.py                 # content config + HTML template + render loop
  base.css                 # everything shared: tokens, layout, components
  hero-forty-seconds.css   # CV-scan art (Forty Seconds only)
  hero-cafe-talk.css       # scorecard art (Cafe Talk only)
```

```bash
python3 scripts/gumroad_landing/build.py
```

It prints byte size, buy-element count, and live-field count per page. If buy elements drop to 0, the page will not sell — Gumroad needs at least one `data-gumroad-action="buy"`.

Per-book copy lives in the `FORTY` and `CAFE` dicts. Anything that differs between the two books belongs there, not in the template.

## The product description is the source of copy

Each product already has a long, carefully written Description on Gumroad. **Never invent landing copy.** Pull the real description first and write from it:

```bash
gumroad products view <id> --json > /tmp/p.json   # the "description" key holds HTML
```

Both descriptions follow the same shape, and each part has a home on the landing page:

| Description section | Lands in |
|---|---|
| Opening hook | `hero_h1` + `hero_sub` |
| "Nội dung chính" (the numbered parts) | `inside_parts` |
| "Vài điều khiến cuốn sách này khác" | `self.bullets` + `chips` |
| Company lists | `proof.items` |
| "Về hai tác giả" | the shared `AUTHORS` block + per-book `authors_note` |
| "Thông tin bản sách" | `self.meta` + `dock_meta` |

**Name every company, never truncate to "…".** The full fourteen-company list is the proof that these CVs are real; an abbreviated list reads as an unbacked claim. Same for concrete numbers already in the description (60 ngày, 85%, mười hai lỗi, tám nơi cùng lúc) — they convert better than adjectives, and they are already verified copy.

After editing copy, diff the landing text against the description to catch anything dropped: strip tags from both, then check that each distinctive phrase from the description appears somewhere on the page.

## Publish

```bash
# Dry run — shows exactly what the sanitizer strips
gumroad products page preview '8c0LPb6cFSN-w7PLMO4JTw==' ./landing.html
gumroad products page preview jaehu ./landing-cafe-talk.html

# Ship
gumroad products page publish '8c0LPb6cFSN-w7PLMO4JTw==' ./landing.html
gumroad products page publish jaehu ./landing-cafe-talk.html
```

Always preview before publishing. Quote the Forty Seconds ID — it contains `==`.

CLI gotchas: `preview`/`publish` take the product ID as a positional arg (there is no `--product` flag), and `products view` wants the ID, not the slug. If `gumroad auth login` returns HTTP 429, use `gumroad auth login --web` and authorize in the browser quickly, the device flow gets rate-limited hard.

## Sanitizer

A clean preview strips exactly three things — `<meta charset>`, `<meta viewport>`, and `<title>` — because Gumroad supplies its own `<head>`. Anything else in the removal table is a real problem to fix.

Confirmed to survive: `<style>`, `<script>`, `<s>`, `<code>`, `<figure>`, `<details>`, `data-gumroad-*`, inline `style` attributes, `data:` URIs. Confirmed stripped: `fetchpriority`.

## Images — only one host works

`public-files.gumroad.com` is the **only** host a custom page may load images from. Upload with:

```bash
gumroad media upload ./thing.webp --name "What it is"   # prints the public URL
gumroad media list
```

Do **not** use `gumroad files upload` — those land in private storage and the page fails moderation. WebP with alpha uploads and serves fine (`content-type: image/webp`).

Anything shown on both pages (author photo, logos) should be uploaded once and referenced by URL from a module-level constant in `build.py`, not inlined as a data URI — inlining doubles the page weight and defeats CDN caching.

**Make photo backgrounds transparent.** A baked-in cream background looks correct in light mode and like a glowing white slab in dark mode. The author combo image was processed to transparent circles before upload; see the recipe below.

## Image processing notes

`numpy` segfaults in this sandbox, so do image work with **pure Pillow**. Useful pattern for knocking out a flat background behind circular photos, which avoids fringing entirely because it never relies on a tolerance flood fill:

1. `ImageChops.difference` against a flat fill of the corner pixel, then `ImageChops.lighter` across the split channels to get a max-channel delta map.
2. Threshold it, blank out any region you want to discard (e.g. baked-in caption text), then `getbbox()` each half of the image to locate each circle.
3. Draw the circles into an `L` mask at 4x scale with `ImageDraw.ellipse`, inset ~2px to drop the anti-aliased outer edge, then `resize(..., LANCZOS)` back down for a smooth alpha.
4. `putalpha`, crop to the alpha bbox with padding, save as WebP.

Always composite the result over both a dark and a light swatch and look at it before uploading.

## Pricing — the discount is invisible unless you spell it out

The `EngineerProAug` offer code takes **$5 off and auto-applies at checkout**. So `data-gumroad-field="price"` interpolates the *discounted* figure ($14.99 / $10.99), not the list price shown in `gumroad products list` ($19.99 / $15.99).

That mismatch burned an hour once: the page looked like it was overstating a discount when it was actually just showing the real price. The rule now is that every price on the page shows the list price struck through, the live discounted price, and the saving, so buyers can see they are getting a deal.

Single knob at the top of `build.py`:

```python
OFFER = {"amount": "$5", "code": "EngineerProAug"}
```

Set `OFFER = None` and rebuild when the promo ends — every struck-through price, badge, and "tự động áp" note disappears in one pass. Leaving a dead strikethrough up is false advertising.

Keep `price` in `src/assets/ebooks-data.js` and the cross-sell card prices in sync with the **effective** (post-discount) price, not the list price.

## Reviews

Gumroad exposes only the **aggregate** on a custom page: `data-gumroad-field="rating"` and `data-gumroad-field="review-count"`. There is no field for individual review text, so the page can show a score and a count but not quotes. To feature a specific review, paste it in as a testimonial by hand.

Only verified buyers can rate, so there is no public "write a review" control to put on the page. Two things drive reviews instead:

- The last FAQ entry (`FAQ_REVIEW`, shared by both pages) points buyers at `https://app.gumroad.com/library`.
- Each product has a `custom_receipt` asking for a rating after they read. Set it with `gumroad products update <id> --custom-receipt "..."`.

**The rating row starts `hidden` and a script reveals it only when `review-count > 0`,** using `Math.floor` on the score so it never shows a star that was not earned. Two traps here:

- A CSS `display` rule beats the `hidden` attribute. `base.css` has `[hidden] { display: none !important; }` to restore it — do not remove that rule.
- Locally the fields render their **fallback** text, so localhost always looks like zero reviews. Only the published page shows real numbers. Check ratings on the live URL, never on `localhost:8002`.

## Layout rules learned the hard way

**Show the cover in the hero.** The first version used a CSS-only animation as the hero visual and buyers never saw the book. The real cover image is now the hero, tilted and shadowed, with a small `.cover-hero__pill` badge. The CSS art moved down into the "inside the book" two-column section where it supports the chapter copy instead of replacing the product.

**Three routes to the storefront.** `https://engineerprovn.gumroad.com/` is reachable from the header brand mark, the `.store` call-out under the two book cards, and the footer link. The call-out is the prominent one; keep it below the book cards so it never competes with the buy CTA above it.

**Authors go high, with real faces.** The authors section sits directly under the hero — buyers want to know who wrote this before they read the pitch. Real photos, not initials in a gradient circle. Section backgrounds alternate plain / `.band` down the page; if you reorder sections, re-check that two `.band` sections never end up adjacent.

**Never translate the book titles.** "Forty Seconds: Ten Real CVs That Passed Big Tech" and "Cafe Talk: The Interview and Career Playbook" appear in English everywhere, including the hero `<h1>`, which is the title split across two lines with the subtitle in `<em>`. Earlier versions used Vietnamese riffs on the titles as the headline ("Bốn mươi giây để qua cửa", "Đỗ phỏng vấn là chương một") and they read as awkward and disconnected from the cover art sitting right next to them. The body copy is Vietnamese; the titles are not.

**Never put `data-gumroad-field="name"` inside a button.** It interpolates the full product title ("Forty Seconds: Ten Real CVs That Passed Big Tech") and blows out the layout. Buttons use the static `name_fallback`; the full name is fine in card headings and the mobile dock.

## Verify before calling it done

Serve the repo on port 8002 and run the Playwright helpers in `/tmp` (`landing-a11y.js`, `mobprice.js`, `verify-price.js`).

The contrast auditor must report **0 failures in both light and dark**. It composites alpha and checks every gradient stop, so its failures are real. Common offenders are orange on cream and white on the orange gradient — the fixes are the `--orange-ink`, `--tint-ink`, and `--tint-green` tokens in `base.css`.

Check mobile at 390px too. The narrow breakpoint (`max-width: 560px`) repositions the cover pill below the cover so it stops covering the logo.

After publishing, load the live URLs and read the prices out of the landing iframe. Every `data-gumroad-field="price"` node should read the same discounted figure, and the struck-through prices should be the list prices.
