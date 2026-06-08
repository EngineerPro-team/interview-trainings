# Full review (round 4): System Design VI translation

Date: 2026-06-07 23:00 +07 (model: Opus 4.8)  
**Status: FIXED** — comprehensive sweep across all 23 case-study chapters, beyond the OpenAI-provided reports.

Scope: all files under `src/assets/content/system-design/vi`. This pass was a full-content review (not just the issues flagged by OpenAI), looking for any remaining literal/awkward MT of standard interview jargon, plus genuine MT bugs.

## MT bug found and fixed

| File | Bug | Fix |
|------|-----|-----|
| `proximity-service.html:104` | `các cột logarit và vĩ độ` (MT translated *longitude* → *logarit*) | `longitude và latitude` |

## Keep-English jargon normalized (global)

| Category | Before (literal) | After |
|----------|------------------|-------|
| Heartbeat | nhịp tim / Cơ chế nhịp tim | **heartbeat / Heartbeat mechanism** |
| Cold storage | kho lạnh | **cold storage** |
| Hotspot | điểm nóng / vấn đề điểm nóng / topic nóng / cache nóng | **hotspot / hotspot problem / hot topic / hot cache** |
| Critical path | đường dẫn quan trọng | **critical path** |
| WAL | Nhật ký ghi trước (WAL) | **Write-ahead log (WAL)** |
| Celebrity problem | Vấn đề về người nổi tiếng | **Celebrity problem** |
| Denormalize | khử chuẩn hóa | **denormalize** |
| Garbage collection | Thu gom rác / Trình thu gom rác / sự kiện thu gom rác | **Garbage collection / Garbage collector** |

## Per-chapter fixes

- **proximity-service** — `proximity service`, `quadtree` (cây tứ giác), `boundary issue`, `nearby businesses`, `neighboring grids/geohashes`, longitude bug.
- **gaming-leaderboard** — `hash map`, `skip list`, `sorted linked list`, `multi-level index`, `write sharding`, `keyspace command`, `hash partitioning`, `global secondary index`.
- **stock-exchange** — `event sourcing schema`, `event store`, `leader` / `leader election`, `Ring buffer (circular buffer)`, garbage collection events.
- **chat-system** — `Heartbeat mechanism`, `presence server`, `client`.
- **scaling** — `multi-master và circular replication`.

## Verification (all return zero hits)

```bash
python3 scripts/review_system_design.py   # idempotent; re-run safe
# then grep VI dir for these — all clean:
#   logarit | cây tứ giác | nhịp tim | kho lạnh | điểm nóng | đường dẫn quan trọng
#   dịch vụ lân cận | thu gom rác | lược đồ nguồn sự kiện | kho sự kiện
#   người dẫn đầu | bầu cử lãnh đạo | Cache vòng
```

## Intentionally kept in Vietnamese (not bugs)

Common, well-understood VN prose — translating to English would be over-engineering:
`phân tán`, `truy vấn`, `độ trễ`, `thông lượng`, `khả năng mở rộng`, `khả năng chịu lỗi`,
`tính sẵn sàng cao`, `nhất quán cuối cùng`, `thời gian thực`, `phân đoạn`, `chỉ mục`,
`tuần tự hóa`, `tranh chấp khóa`, `chủ đề` (web-crawler = content topic, not Kafka topic).

## Re-run after future MT

```bash
python3 scripts/review_system_design.py
python3 scripts/fix_system_design_html.py
make local-build
```
