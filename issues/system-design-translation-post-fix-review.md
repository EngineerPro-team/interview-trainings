# Post-fix review: System Design VI translation

Date: 2026-06-07  
**Status: FIXED** (2026-06-07 — remediation applied in VI HTML + `scripts/review_system_design.py`)

Scope: current Claude-fixed VI files under `src/assets/content/system-design/vi` for the 23 case-study chapters.

Summary: the fix improved the translation a lot. Remaining correctness issues from this review have been addressed.

## Findings

| # | Severity | Issue | Status |
|---|----------|-------|--------|
| 1 | High | `Sloppy Quorum` / `Hinted Handoff` still mistranslated in `key-value-store.html` | **FIXED** |
| 2 | High | Payment chapter: reconciliation, idempotency key, `string` type literals | **FIXED** |
| 3 | Medium | Distributed Message Queue: writes/batching, segment writes, compensate wording | **FIXED** |
| 4 | Medium | Digital Wallet: typo `chúng I`, polling wording | **FIXED** |
| 5 | Medium | S3 Object Storage: bucket/object/versioning terms | **FIXED** (core glossary + Q&A lines) |
| 6 | Medium | Stock Exchange: market data publisher, subscriber | **FIXED** |

## Verification Notes

- Bonus sweep (2026-06-07): global rule `\bchúng I\b` → `chúng ta` fixed 7 more files (`ad-click-aggregation`, `digital-wallet`, `google-maps`, `hotel-reservation`, `metrics-monitoring`, `stock-exchange` ×2) beyond the single hit in `digital-wallet.html` from finding #4.
- Follow-up sweep: fixed remaining `long polling`, `ZooKeeper`, `leader replica`, `leader/follower`, `in-sync replica (ISR)`, payment `idempotency key/string`, and stock-exchange `market data publisher/subscriber/matching engine/sequencer` wording.
- Second follow-up sweep: fixed leftover `Apache ZooKeeper` mistranslations, `producer/consumer/subscriber` literals, `Response` API labels, and more stock-exchange `matching engine/sequencer/fill/Long` wording.
- Targeted follow-up checks now return zero hits for: `Đại biểu`, `Bàn giao gợi ý`, `khóa tạm thời`, `sợi dây`, `phong trào tiền bạc`, uppercase `BẰNG`, `bỏ phiếu dài`, `Bộ nhớ nhà nước`, `Người giữ vườn thú`, `người quản lý vườn thú`, `chúng I`, `thăm dò polling`, literal `nhà sản xuất/người tiêu dùng/người đăng ký`, `Phản ứng:`, and old stock-exchange publisher/subscriber phrases.
- Q/A labels: no remaining `Tôi:` hits in the 23 case-study VI files; `I:` is used consistently.
- Previous critical literals now have zero hits in the case-study set: `Tìm nguồn cung ứng sự kiện`, `Xô`, `Sự vật`, `6 giây`, `11 giây`, `Hòa giải`, `sổ đặt hàng`, `cửa hàng sự kiện`, `Mặt sau của phong bì`.
- No `<h2><img ...>` image-heading issue was detected in current EN/VI content.

## Re-run after future MT

```bash
python3 scripts/review_system_design.py
```
