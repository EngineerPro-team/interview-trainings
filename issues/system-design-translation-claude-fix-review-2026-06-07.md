# Claude fix review: System Design VI translation

Date: 2026-06-07 17:10 +07  
**Status: FIXED** (2026-06-07 — idempotency glossary locked in `scripts/review_system_design.py` → `GLOSSARY_FIXES`)

Scope: current VI files under `src/assets/content/system-design/vi`, focused on the 23 case-study chapters from `key-value-store` through `stock-exchange`.

## Summary

The previous high-risk patterns now pass targeted checks:

- `Tôi:`, uppercase `BẰNG`, `bỏ phiếu dài`, `Người quản lý vườn thú`, `nhà sản xuất/người tiêu dùng/người đăng ký`, `Phản ứng:`
- old stock-exchange literals such as `công cụ khớp`, `trình sắp xếp thứ tự`, `Luồng giao dịch`
- old payment literals such as `phong trào tiền bạc`, `sợi dây`, `thăm dò khóa ngoại`
- image-heading labels such as `Image N` / `Hình ảnh N`

All 9 idempotency findings fixed. Verification `rg` for mistranslation patterns returns zero hits in case-study VI files.

## Findings

| # | Severity | File | Line | Current text | Expected fix |
|---|----------|------|------|--------------|--------------|
| 1 | High | `payment-system.html` | 160 | `UUID cho mục đích tạm thời` | `UUID cho mục đích idempotency` |
| 2 | High | `payment-system.html` | 221 | `cơ chế bình thường` | `cơ chế idempotency` |
| 3 | High | `payment-system.html` | 223 | `Tính tạm thời được quản lý...` | `Idempotency được quản lý...` or `Tính idempotent được quản lý...` |
| 4 | High | `payment-system.html` | 225 | `Tính bình thường có thể đạt được...` | `Idempotency có thể đạt được...` |
| 5 | High | `payment-system.html` | 229 | `Tính bình đẳng cũng được áp dụng...` and `cùng một lần hai lần` | `Idempotency cũng được áp dụng...` and `cùng một nonce hai lần` |
| 6 | Medium | `hotel-reservation.html` | 67 | `reservationID là một chìa khóa bình thường` | `reservationID là một idempotency key` |
| 7 | Medium | `hotel-reservation.html` | 179 | `API tạm thời` | `Idempotent API` |
| 8 | Medium | `digital-wallet.html` | 59 | `id giao dịch (khóa bình thường)` | `transaction_id (idempotency key)` |
| 9 | Medium | `ad-click-aggregation.html` | 279 | `xử lý kết quả tổng hợp một cách bình thường` | `xử lý kết quả tổng hợp theo cách idempotent` |

## Why This Matters

`Idempotency` is a core distributed-systems/payment concept. Translating it as `bình thường`, `tạm thời`, or `bình đẳng` makes the text technically wrong, especially in the payment, reservation, and wallet chapters where duplicate processing is the main failure mode being discussed.

## Verification Commands

```bash
rg -n "chìa khóa bình thường|khóa bình thường|API tạm thời|Tính tạm thời|Tính bình thường|Tính bình đẳng|cơ chế bình thường|mục đích tạm thời|cùng một lần hai lần|một cách bình thường" src/assets/content/system-design/vi
```

After fixing, this command should return zero hits except for genuinely non-technical uses of `bình thường`.

