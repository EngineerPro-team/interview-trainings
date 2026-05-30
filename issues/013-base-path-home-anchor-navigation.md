# FIXED — P1 - Home Anchor Navigation Drops the GitHub Pages Base Path

**Status: FIXED** (2026-05-30)

## Resolution

`src/assets/app.js:399` — the anchor-style `#home-roadmap` / `#home-format` click handler now uses `pathFor("home", null)` instead of the hardcoded `"/"`. On project Pages deploys (`BASE_PATH=/interview-trainings`), `pathFor("home", null)` returns `/interview-trainings/`, so the URL stays under the project path. Root deploys (`BASE_PATH=""`) still get `/`.

The scroll-into-view behaviour is unchanged. No new hash URLs are emitted to sitemap or canonical metadata — the change is purely in the click-time `history.pushState` URL.

---



Claude, the latest SEO fixes look good overall, but there is one remaining clean-URL/base-path bug in the runtime router.

## Evidence

- Project Pages deploy uses `BASE_PATH=/interview-trainings`, and generated links/assets correctly include it, e.g. `docs/index.html:335` links to `/interview-trainings/courses/`.
- Home anchor links are present across generated pages:
  - `docs/index.html:139` has `href="#home-roadmap" data-href="#home-roadmap"`.
  - `docs/index.html:986` has the footer roadmap link.
  - `docs/index.html:990` has the footer format link.
- The click handler special-cases these anchors but pushes the origin root:
  - `src/assets/app.js:394-400`
  - `docs/assets/app.js:394-400`

```js
if (anchor && anchor.startsWith("#home-")) {
  e.preventDefault();
  const anchorId = anchor.slice(1);
  history.pushState(null, "", "/");
  showRoute({ route: "home", slug: null });
  ...
}
```

## Impact

On the production GitHub Pages URL `https://engineerpro-team.github.io/interview-trainings/`, clicking `Lộ trình` or `Hình thức học` changes the browser URL to `https://engineerpro-team.github.io/`. The SPA does not reload immediately, so the UI appears to work, but the visible URL is now outside the deployed project path. Refreshing or sharing from that state can land users on the wrong site/root 404.

## Suggested Fix

Use the existing clean-route helper instead of hard-coding `/`:

```js
history.pushState(null, "", pathFor("home", null));
```

If preserving the anchor in the URL is desired, make it base-path aware:

```js
history.pushState(null, "", pathFor("home", null) + anchor);
```

Then ensure `parseHash()` treats `#home-roadmap` / `#home-format` as home anchors instead of unknown routes.

## Acceptance Criteria

- On `/interview-trainings/...`, clicking any `#home-roadmap` or `#home-format` link keeps the URL under `/interview-trainings/`.
- Root deploys with `EP_BASE_PATH=` still work.
- The scroll behavior still lands on the intended home section.
- No new hash URLs are added to sitemap/canonical output.
