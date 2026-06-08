# Claude post-fix review: remaining VI translation issues

Date: 2026-06-07 22:58 +07  
**Status: FIXED** (2026-06-07 23:05 — root cause: `apply_fixes` runs `re.sub` with `re.I`, so the `Tìm nạp → Fetch` rule also matched lowercase `tìm nạp` mid-sentence and capitalized it. Fixed via global ` Fetch ` → ` fetch ` cleanup + targeted sentence fixes in `scripts/review_system_design.py`.)

## Resolution

| # | Fix |
|---|-----|
| 1 | s3:218 `filename nơi Object storage` → `filename nơi object được lưu trữ` |
| 2 | metrics:144 added missing verb → `Collection agent thu thập metrics từ server và push...` |
| 3,4,6,7,9,10,11,13 | global ` Fetch ` → ` fetch ` (mid-sentence); component labels `<strong>Fetch ...:` untouched |
| 5 | digital-wallet:353 → `gửi command và poll response` |
| 8 | s3:155 → `Ví dụ GET request để fetch một object` |
| 12 | s3 mid-sentence `Client` → `client` (75, 166, 303, 304); list-initial `Client` (163, 299, 301) kept capitalized as correct sentence start |

Remaining `Fetch` (capital) only in component labels after `<strong>` — acceptable per this report's own exceptions.

Scope: current files under `src/assets/content/system-design/vi`.

## Summary

Good news: the verification patterns from the previous report are mostly clean now. The only old-pattern hit is `phân chia thành các miền lỗi` in `s3-object-storage.html:249`, and that is valid Vietnamese prose for failure-domain placement.

Remaining issues are not the old `idempotency` / `stock-exchange` / `payment` bugs. They are mostly:

- mechanical English insertion with wrong grammar (`Fetch`, `fetch`, `Client`, `NHẬN yêu cầu`)
- malformed hybrid phrases (`Collection agent từ máy chủ`, `filename nơi Object storage`)
- a few API / storage sentences whose meaning is now wrong or awkward

## Findings

| # | Severity | File | Line | Current text | Expected fix |
|---|----------|------|------|--------------|--------------|
| 1 | High | `s3-object-storage.html` | 218 | `<code>filename</code> nơi Object storage` | `<code>filename</code> nơi object được lưu trữ` or `<code>filename</code> where object is stored` |
| 2 | High | `metrics-monitoring.html` | 144 | `Collection agent từ máy chủ và push chúng tới metrics collector.` | `Collection agent thu thập metrics từ server và push chúng tới metrics collector.` |
| 3 | Medium | `metrics-monitoring.html` | 132 | `Metrics collector fetches metadata cấu hình...` | `Metrics collector fetches configuration metadata...` or `Metrics collector lấy metadata cấu hình...` |
| 4 | Medium | `metrics-monitoring.html` | 259 | `Alert manager fetch cấu hình cảnh báo từ cache.` | `Alert manager fetches alert configurations from cache.` or `Alert manager lấy cấu hình cảnh báo từ cache.` |
| 5 | Medium | `digital-wallet.html` | 353 | `reverse proxy ... gửi lệnh và polling phản hồi` | `reverse proxy ... gửi command và poll response thay mặt người dùng` |
| 6 | Medium | `digital-wallet.html` | 355 | `Fetch dữ liệu cho nhiều người dùng` | `fetch data cho nhiều người dùng` or `lấy dữ liệu cho nhiều người dùng` |
| 7 | Medium | `s3-object-storage.html` | 117 | `Fetch metadata ... Fetch nội dung tệp` | `fetch metadata ... fetch nội dung tệp` or fully Vietnamese `lấy metadata ... lấy nội dung tệp` |
| 8 | Medium | `s3-object-storage.html` | 155 | `Ví dụ NHẬN yêu cầu Fetch một object` | `Example GET request for fetching an object` or `Ví dụ GET request để fetch một object` |
| 9 | Medium | `s3-object-storage.html` | 264 | `Fetch riêng từng phần...` | `fetch riêng từng phần...` or `lấy riêng từng phần...` |
| 10 | Medium | `notification-system.html` | 119 | `Fetch metadata từ cache hoặc database` | `fetch metadata từ cache hoặc database` or `lấy metadata từ cache hoặc database` |
| 11 | Medium | `web-crawler.html` | 78 | `HTML Downloader Fetch URL...` | `HTML Downloader fetches URLs...` or `HTML Downloader fetch URL...` with consistent casing |
| 12 | Medium | `s3-object-storage.html` | 75, 163, 166, 299, 301, 303, 304 | `Client` is capitalized mid-sentence | Use lowercase `client` unless it is a component label. |
| 13 | Medium | Global `Fetch` replacement artifact | many files | `Fetch` appears in prose across `notification-system`, `google-maps`, `gaming-leaderboard`, `nearby-friends`, `news-feed`, `scaling`, `distributed-email`, `google-drive`, `proximity-service`, `s3-object-storage`, `digital-wallet`, `web-crawler` | Decide one style and apply consistently: either lowercase `fetch` as a kept technical verb, or Vietnamese `lấy/truy xuất`. Avoid capitalized `Fetch` mid-sentence. |

## Why This Matters

The previous “keep English” pass fixed many glossary problems, but these remaining lines read like search/replace artifacts. A reader can still understand most of them, but a few are technically wrong:

- `filename nơi Object storage` does not preserve the source meaning `filename where object is stored`.
- `Collection agent từ máy chủ...` is missing the verb `collects`.
- `polling phản hồi` is not a natural rendering of `polls for response`.

## Verification Commands

Run after the next Claude fix:

```bash
rg -n "\\bFetch\\b|NHẬN yêu cầu Fetch|filename.*Object storage|Collection agent từ|fetch metadata cấu hình|Alert manager fetch|polling phản hồi|Fetch dữ liệu|HTML Downloader Fetch|Fetch metadata" src/assets/content/system-design/vi
rg -n "\\bClient\\b" src/assets/content/system-design/vi/s3-object-storage.html
```

Acceptable exceptions:

- `Fetch` in code/API field names if any appear in code blocks.
- `Client` when used as an intentional component label, not normal prose.
