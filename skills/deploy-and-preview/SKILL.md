---
name: deploy-and-preview
description: Build, preview locally on port 8001, push to GitHub Pages. Covers the prod vs local build split, BASE_URL/BASE_PATH config, and the localhost-guard build-failure mode. Use when the user says "deploy", "push lên", "preview", "make dev", or asks why their local/prod looks different.
---

# Deploy + local preview

## Two distinct build outputs

| Target | Folder | URL | When |
|---|---|---|---|
| **Production** | `docs/` | https://engineerpro-team.github.io/interview-trainings/ | Committed + pushed → GitHub Pages serves it |
| **Local preview** | `_local/` | http://localhost:8001/ | `_local/` is gitignored; never committed |

Each build sets a different `EP_BASE_PATH` so asset URLs resolve correctly at the matching root. **Never mix them up** — if you serve `docs/` at `localhost:8001/`, assets 404 because they're prefixed `/interview-trainings/...`.

## Production build + push

```bash
EP_BASE_URL=https://engineerpro-team.github.io \
EP_BASE_PATH=/interview-trainings \
make github

git add -A
git commit -m "<concise message>"
git push
```

`make github` chain:
1. `make stats` — fails if counts drifted (mentor/story/course/podcast/faq).
2. `make seo` — regenerates `src/sitemap.xml` + `src/robots.txt`.
3. Clean `docs/` + copy `src/` over.
4. `scripts/build_pages.py` — 115 prerendered HTML pages.
5. localhost-guard grep — fails if any `docs/` file contains `http://localhost`.

If `make github` fails, **never push** until the failure is fixed. Common failures:

- **stats drift**: `make stats` lists the file + line. Bulk-substitute the old → new number.
- **localhost in docs/**: someone ran `make local-build` with the wrong env vars. Just re-run `make github` with the prod env above.

## Local preview

```bash
make dev    # = local-build + serve
```

or manually:

```bash
make local-build
make serve   # serves _local/ on port 8001
```

If a server is already running, kill + restart:
```bash
lsof -ti:8001 | xargs kill -9
make dev
```

## After pushing

GitHub Pages CDN takes 1–2 minutes to deploy the new commit. Tell the user to **hard reload (Cmd+Shift+R)** — they'll often see the previous version because of browser cache.

Verify the live site has the latest code:
```bash
curl -sI https://engineerpro-team.github.io/interview-trainings/assets/app.js | grep -i last-modified
```

## Switching deploy targets

Custom domain or repo rename? Override at build time and re-push:

```bash
# Root deploy (custom domain or user/org pages)
EP_BASE_URL=https://engineerpro.com EP_BASE_PATH= make github

# Different project subpath
EP_BASE_URL=https://engineerpro-team.github.io EP_BASE_PATH=/new-name make github
```

Single source of truth: `scripts/site_config.py` reads `EP_BASE_URL` + `EP_BASE_PATH` env vars and exposes them as `BASE_URL`, `BASE_PATH`, `SITE_BASE` to every script that needs them.

## Enabling GitHub Pages (one-time)

If site is 404'ing for the first time:
1. Settings → Pages → Source: **Deploy from a branch**
2. Branch: `main` / Folder: `/docs`
3. Save, wait 1–2 minutes
