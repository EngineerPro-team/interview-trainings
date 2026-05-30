# OPEN — P1 - Replace Mentor Placeholders Before Launch

**Status: PARTIALLY ADDRESSED** (2026-05-30) — needs user verification to fully close

## What was attempted

1. Re-ran `scripts/retry_linkedin.py` with a fresh IP for 13 mentor LinkedIn profiles. Result: **0 / 13 success, 21 / 21 attempts returned HTTP 999** (LinkedIn's hard bot-block) regardless of IP rotation. LinkedIn fingerprints on UA + behavioural pattern, not just IP, so a new IP alone doesn't unblock. Results written to `scripts/linkedin-retry-results.json` for the partial run before kill.

2. UI cosmetic: the renderer now translates the "Đang cập nhật" string to "Coming soon" when in EN mode, so at least the placeholder reads naturally in both languages.

## What still needs the user

These 4 mentors still ship placeholder labels in `src/assets/data.js`:

- `Việt` — `current: { role: "Senior Software Engineer", company: "Big Tech" }` (specific company hidden per user request)
- `Chấn Thành (Thomas Quach)` — `current.company: "Đang cập nhật"`
- `Lợi Nguyễn` — `current.company: "Đang cập nhật"`
- `Mạnh` — `current: { role: "Senior Software Engineer", company: "Big Tech" }`

Plus `Chương` has `linkedin: null`.

## Suggested next step

Manual update to `src/assets/data.js`: replace each `"Big Tech"` / `"Đang cập nhật"` with the confirmed public company name. If a mentor explicitly wants to stay anonymous, add a one-line comment noting the decision so it doesn't look like a typo.

---



Claude, mentor data still contains placeholders that conflict with the "100% Big Tech mentor" positioning.

## Evidence

`src/assets/data.js`:

- `Chương` has `linkedin: null` at `src/assets/data.js:55-58`.
- `Việt` has current company `Big Tech` at `src/assets/data.js:61-64`.
- `Chấn Thành (Thomas Quach)` has current company `Đang cập nhật` at `src/assets/data.js:98-101`.
- `Lợi Nguyễn` has current company `Đang cập nhật` at `src/assets/data.js:110-113`.
- `Mạnh` has current company `Big Tech` at `src/assets/data.js:116-119`.
- Header copy says mentors are currently at named companies including Google/Amazon/Meta/TikTok/Spotify/Shopee/Acronis/AWS (`src/assets/i18n.js:87-88` and EN equivalent).

## Suggested Fix

1. Verify current role/company/LinkedIn for the placeholder mentors.
2. Replace `Big Tech` and `Đang cập nhật` with concrete, approved public labels.
3. If a mentor cannot be verified publicly:
   - hide the profile,
   - or mark it explicitly as private/anonymous,
   - or move them out of the public mentor grid.
4. Add `verifiedAt` or a short source note for manually verified mentor records.

## Acceptance Criteria

- No visible mentor card shows `Big Tech` or `Đang cập nhật` as a company.
- No primary mentor card has a dead/missing LinkedIn CTA unless intentionally hidden.
- The mentor intro copy matches actual visible mentor data.
