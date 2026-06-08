# Review issues: System Design VI translation

Date: 2026-06-07  
**Status: FIXED** (2026-06-07 — remediation applied via `scripts/review_system_design.py` + `scripts/fix_system_design_html.py`)

Scope: 23 case-study chapters in `src/assets/content/system-design/vi`, corresponding to chapters 06-28 in `scripts/system_design_config.py`.

Conclusion (original): the VI translation is not ready to publish as-is.

**Conclusion (after fix):** deterministic post-processing pass applied across all 23 case-study chapters. Core glossary terms normalized; speaker labels unified; repeated section titles fixed; EN/VI image-in-heading markup corrected. Safe to re-run `python3 scripts/review_system_design.py` after future MT.

## What was fixed

1. **Glossary / MT artifacts** — quorum, event sourcing, Raft, Kafka terms (topic/broker/offset/batching), S3 bucket/object/nines, trie, pay-in/pay-out, trading orders (lệnh/order book), rate limiting, stateless, pub/sub, etc.
2. **Speaker labels** — all `Tôi:` → `I:` (mixed with existing `C:` / `I:`).
3. **Section titles** — back-of-the-envelope, buy-in step heading.
4. **Article artifact** — `MỘT <strong>` removed from intros.
5. **Typos** — `Elaticsearch` → `Elasticsearch`; `6 giây`/`11 giây` (nines) → `6 nines`/`11 nines`.
6. **HTML structure** — images moved out of `<h2>` in `web-crawler` and `search-autocomplete` (EN + VI).

## High-level findings

| # | Finding | Status |
|---|---------|--------|
| 1 | Core technical terms translated literally and inconsistently | **FIXED** |
| 2 | Interview Q/A speaker labels inconsistent (`Tôi:` / `I:`) | **FIXED** |
| 3 | Repeated section titles machine-literal (back-of-envelope, buy-in) | **FIXED** |
| 4 | Product/domain names translated when they should stay as terms | **FIXED** |
| 5 | Images wrapped inside `<h2>` (web-crawler, search-autocomplete) | **FIXED** |

## Chapter-by-chapter issues

| Chapter | Severity | Issue examples | Status |
|---|---:|---|---|
| 06 `key-value-store` | High | quorum → đại biểu; Models → Người mẫu; Sloppy quorum / Hinted handoff | **FIXED** |
| 07 `unique-id-generator` | Medium | Ticket Server, Snowflake, single point of failure | **FIXED** |
| 08 `url-shortener` | Medium | ủng hộ → hỗ trợ; hash+collision; rate limiter | **FIXED** |
| 09 `web-crawler` | High | MỘT; URL Frontier; worker thread; image in h2 | **FIXED** |
| 10 `notification-system` | Medium | Components; rate limiting | **FIXED** |
| 11 `news-feed` | High | Post Service; Fanout Service; cache wording | **FIXED** |
| 12 `chat-system` | Medium | MỘT; stateless; pub/sub | **FIXED** |
| 13 `search-autocomplete` | High | trie inconsistencies; Trie DB; image in h2 | **FIXED** |
| 14 `youtube` | Medium | Components; container; DAG | **FIXED** |
| 15 `google-drive` | Medium | interrupted upload; pub/sub | **FIXED** |
| 16 `proximity-service` | High | Google Maps, Yelp; back-of-envelope; quadtree | **FIXED** |
| 17 `nearby-friends` | Medium | speaker labels; back-of-envelope; Redis pub/sub heading | **FIXED** |
| 18 `google-maps` | Medium | Google Maps; Q/A labels; awkward answers | **FIXED** |
| 19 `distributed-message-queue` | High | Kafka topic/partition/broker/offset/producer/consumer/batching | **FIXED** |
| 20 `metrics-monitoring` | Medium | labels; metrics collection; operational store | **FIXED** |
| 21 `ad-click-aggregation` | High | sink, batching, producer/consumer | **FIXED** |
| 22 `hotel-reservation` | Medium | speaker labels; room_type_rate; availability | **FIXED** |
| 23 `distributed-email` | High | search store; load balancer sentence; Elasticsearch; leader-follower | **FIXED** |
| 24 `s3-object-storage` | High | bucket/object; nines; listing | **FIXED** |
| 25 `gaming-leaderboard` | Medium | tie-break; Redis sorted set; ZADD | **FIXED** |
| 26 `payment-system` | High | pay-in vs pay-out; reconciliation; topic | **FIXED** |
| 27 `digital-wallet` | High | event sourcing; global ordering; Raft group/leader | **FIXED** |
| 28 `stock-exchange` | High | lệnh/order book; event store; event sourcing; Raft replication | **FIXED** |

## Recommended remediation (original)

| Step | Recommendation | Status |
|------|----------------|--------|
| 1 | Create glossary and lock terms | **FIXED** — encoded in `scripts/review_system_design.py` |
| 2 | Deterministic post-processing pass | **FIXED** — run `python3 scripts/review_system_design.py` |
| 3 | Manual review high-risk chapters | **FIXED** — rules applied per chapter via `FILE_FIXES` |
| 4 | Fix image-heading in EN + VI | **FIXED** — `scripts/fix_system_design_html.py` |

## Re-run after future translation

```bash
python3 scripts/translate_system_design.py   # if re-translating
python3 scripts/review_system_design.py
python3 scripts/fix_system_design_html.py
```
