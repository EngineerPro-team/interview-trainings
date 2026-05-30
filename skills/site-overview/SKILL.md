---
name: site-overview
description: High-level map of the EngineerPro static site repo — where everything lives, the build pipeline, and the i18n/data flow. Use when the user asks where to change something, or before touching unfamiliar code.
---

# EngineerPro static site — repo map

Pure static SPA hosted on GitHub Pages from `docs/`. Single source of truth for build config: `scripts/site_config.py` (`BASE_URL` + `BASE_PATH`).

## Layout

```
src/                          ← authored source (never edit docs/ directly)
├── index.html                ← master template (114 prerendered pages clone this)
├── assets/
│   ├── app.js                ← SPA: router, renderers, theme, i18n
│   ├── style.css             ← single stylesheet, ~3.7K lines, light + dark themes
│   ├── i18n.js               ← VI/EN dictionary, ~150 keys, dot.separated
│   ├── data.js               ← mentors, contact, book, roadmap, partners, companies
│   ├── courses-data.js       ← AUTO-GEN by scripts/crawl_courses.py (html=VI) + scripts/translate_courses.py (htmlEn=EN)
│   ├── courses-i18n.js       ← hand EN translations for course title/blurb
│   ├── podcasts-data.js      ← AUTO-GEN by scripts/crawl_podcasts.py
│   ├── faqs-data.js          ← AUTO-GEN by crawl_faqs.py + translate_faqs.py
│   ├── resources-data.js     ← AUTO-GEN by scripts/crawl_resources.py
│   ├── resources-i18n.js     ← hand EN translations for resources strings
│   ├── stories-data.js       ← AUTO-GEN by parse_stories + translate_stories
│   └── img/                  ← mentors/, companies/, stories/, partners/
├── sitemap.xml               ← AUTO-GEN by scripts/make_seo.py
└── robots.txt                ← AUTO-GEN by scripts/make_seo.py

docs/                          ← PROD build output (committed, served by Pages)
_local/                        ← LOCAL build output (gitignored)
scripts/                       ← Python: crawlers + builders
skills/                        ← this folder; agent how-to docs
Makefile                       ← single entry-point for every workflow
```

## Build pipeline (prod)

```
make github
  ├─ make stats          ← scripts/check_stats.py (fails if counts drift across docs/code)
  ├─ make seo            ← scripts/make_seo.py → src/sitemap.xml + src/robots.txt
  ├─ rm -rf docs && cp src/. docs/
  ├─ scripts/build_pages.py  → prerender 115 HTML pages into docs/
  └─ localhost-guard grep   ← fails if any docs file contains http://localhost
```

Override deploy target via env:
```bash
# Project Pages (current setup)
EP_BASE_URL=https://engineerpro-team.github.io \
EP_BASE_PATH=/interview-trainings \
make github

# Custom domain / user org pages (no subpath)
EP_BASE_URL=https://engineerpro.com EP_BASE_PATH= make github
```

## Local preview build (port 8001)

```bash
make dev    # = local-build + serve
```

`make local-build` writes to `_local/` (gitignored) with `EP_BASE_PATH=""` so served at localhost root works. Never serves from `docs/` — `docs/` has the subpath baked in.

## SPA router

`src/assets/app.js`:
- `parseHash()` reads `location.pathname` first (stripping BASE_PATH), then hash fallback.
- `pathFor(route, slug)` builds clean URLs `/courses/foo/` with subpath baked in.
- Click handler intercepts internal links via `history.pushState` so URL stays clean.
- `asset(p)` helper prefixes `BASE_PATH` for any `assets/...` URL — wrap any new dynamic image src with it.

## i18n

- Static text: `data-i18n="key"` (textContent) / `data-i18n-html="key"` (innerHTML) / `data-i18n-attr="alt|key"` (attribute) — automatically translated by `applyI18n()`.
- Dynamic counts (mentor/story/course): `<span id="*Count">N</span>` placeholder gets overwritten by `refreshLiveCounts()` after every i18n apply.
- Language toggle reads/writes `localStorage.epLang`. `?lang=en` query forces EN (deterministic for crawlers).

## Common task → skill mapping

| User asks | Skill |
|---|---|
| "Thêm mentor X" | `add-mentor` |
| "Thêm logo công ti X" | `add-company-logo` |
| "Đếm lại N students/stories/mentors" | `update-content-counts` |
| "Deploy / push / preview local" | `deploy-and-preview` |
| "Crawl lại stories / courses / podcast" | `content-pipeline` |
| Anything else / unclear | Read this overview first |
