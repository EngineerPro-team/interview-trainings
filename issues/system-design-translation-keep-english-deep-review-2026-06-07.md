# Deep review: keep English technical terms in System Design VI

Date: 2026-06-07 17:12 +07  
**Status: FIXED** (2026-06-07 — findings #1–#9 addressed in `scripts/review_system_design.py`)

Scope: all current files under `src/assets/content/system-design/vi`.

## Policy

Giữ English cho tên component, pattern, API label, field name, storage concept, queue/streaming concept, và domain term đã phổ biến trong phỏng vấn:

- Infra: `database`, `metadata database`, `web server`, `API server`, `WebSocket server`, `load balancer`, `cache`, `CDN`.
- Queue/streaming: `topic`, `partition`, `broker`, `consumer group`, `offset`, `state storage`, `metadata storage`, `coordination service`, `coordinator`.
- Metrics: `metrics`, `metrics collector`, `time-series database`, `query service`, `alert manager`, `alert store`, `visualization system`.
- Storage/S3: `object storage`, `object store`, `data store`, `metadata store`, `bucket`, `object`, `listing`, `multipart upload`.
- Trading: `trading flow`, `market data`, `order book`, `execution`, `fill`, `sequencer`, `order manager`, `client gateway`, `broker`, `reporter`.
- Web crawler: `web crawler`, `Seed URLs`, `HTML Downloader`, `DNS Resolver`, `Content Parser`, `URL Extractor`, `URL Filter`, `URL Seen?`, `URL Storage`, `Queue Router`, `Queue Selector`, `Front Queue`, `Back Queue`.
- API/docs: `Request`, `Response`, `Request parameters`, `Query parameters`, `sample response`, `header`, `endpoint`.
- Consistency/payment: `idempotency`, `idempotency key`, `idempotent`, `nonce`, `exactly-once`, `at-least-once`, `at-most-once`.

## Findings

| # | Severity | Area | Status |
|---|----------|------|--------|
| 1 | High | Idempotency terms | **FIXED** — `GLOSSARY_FIXES` |
| 2 | High | Metrics chapter | **FIXED** — `FILE_FIXES` metrics-monitoring |
| 3 | High | S3 component names | **FIXED** — `FILE_FIXES` s3-object-storage |
| 4 | High | Stock Exchange domain | **FIXED** — `FILE_FIXES` stock-exchange |
| 5 | Medium | Message Queue storage/coordinator | **FIXED** — state storage, coordinator (prior passes) |
| 6 | Medium | Web Crawler components | **FIXED** — `FILE_FIXES` web-crawler |
| 7 | Medium | Email/Drive/YouTube infra | **FIXED** — metadata database; YouTube DAG/resource manager/task queue |
| 8 | Medium | Nearby Friends WebSocket | **FIXED** — WebSocket server |
| 9 | Medium | API/doc labels | **FIXED** — Sample response, Response Construction, stock-exchange API fields |

### Original findings table

| # | Severity | Area | Examples | Recommended fix |
|---|----------|------|----------|-----------------|
| 1 | High | `idempotency` terms | `payment-system.html:160`, `:221`, `:223`, `:225`, `:229`; `hotel-reservation.html:67`, `:179`; `digital-wallet.html:59`; `ad-click-aggregation.html:279` | Replace `mục đích tạm thời`, `cơ chế bình thường`, `Tính tạm thời`, `Tính bình thường`, `Tính bình đẳng`, `khóa bình thường`, `API tạm thời`, `một cách bình thường` with `idempotency`, `idempotency key`, `Idempotent API`, `idempotent`. |
| 2 | High | Metrics chapter over-translates core terms | `metrics-monitoring.html:109-114`, `:132-133`, `:164`, `:186-190`, `:261`, `:269-270` | Keep `metrics source`, `metrics collector`, `time-series database`, `query service`, `alert manager`, `visualization system`. |
| 3 | High | S3/Object Storage component names are inconsistent | `s3-object-storage.html:126`, `:128-140`, `:171`, `:197`, `:280`, `:286`, `:300`, `:304` | Keep `API service`, `data store`, `metadata store`, `bucket`, `object`, `object store`, `listing`. Avoid `Dịch vụ API`, `Kho dữ liệu`, `Kho siêu dữ liệu`, `thùng`, `bộ chứa`, `cửa hàng object`. |
| 4 | High | Stock Exchange domain terms still translated | `stock-exchange.html:70`, `:74-80`, `:86`, `:103-110`, `:147`, `:180-192`, `:259`, `:284`, `:385` | Keep `client gateway`, `execution`, `fill`, `market data flow`, `market data`, `order book`, `order manager`, `sequencer`, `broker`, `reporter`, `candlestick chart`. |
| 5 | Medium | Distributed Message Queue storage/coordinator terms | `distributed-message-queue.html:100-103`, `:205`, `:234-235`, `:244`, `:347`, `:365`, `:381` | Keep `data storage`, `state storage`, `metadata storage`, `coordination service`, `coordinator`, `offset`, `parser`, `script executor`, `object storage`. |
| 6 | Medium | Web Crawler component names translated | `web-crawler.html:2-3`, `:34`, `:46-71`, `:77-80`, `:103`, `:106`, `:121-123`, `:130` | Keep component labels exactly as source: `web crawler`, `Seed URLs`, `HTML Downloader`, `DNS Resolver`, `Content Parser`, `Content Seen?`, `Content Storage`, `URL Extractor`, `URL Filter`, `URL Seen?`, `URL Storage`, `Queue Router`, `Queue Selector`, `Front Queue`, `Back Queue`. |
| 7 | Medium | Infra component names in Email/Drive/YouTube | `distributed-email.html:90`, `:120`; `google-drive.html:40-41`, `:83`, `:122`, `:137`, `:210`; `youtube.html:43-45`, `:140`, `:151`, `:157-158` | Keep `metadata database`, `storage directory`, `origin storage`, `transcoding server`, `DAG scheduler`, `resource manager`, `task queue`, `worker queue`. |
| 8 | Medium | Nearby Friends WebSocket/Redis terms not locked | `nearby-friends.html:53`, `:59`, `:114`, `:123`, `:140` | Keep `WebSocket server`, `Redis Pub/Sub`, `channel`, `subscriber`, `hash ring`. Avoid `máy chủ ổ cắm web`, `chủ đề` for Redis Pub/Sub context. |
| 9 | Medium | API/doc labels translated inconsistently | `digital-wallet.html:60`; `distributed-email.html:61`, `:74`; `gaming-leaderboard.html:52`, `:75`; `google-maps.html:95`, `:183`; many request/response blocks in `stock-exchange.html:126-177` | Standardize API docs to `Request parameters`, `Response`, `Sample response`, `Query parameters`, and keep API field names English (`symbol`, `side`, `price`, `quantity`, `executions`, `bids`, `asks`, etc.). |

## Detailed Notes

### 1. Idempotency Is Still Broken

Current examples:

```text
payment-system.html:160  UUID cho mục đích tạm thời
payment-system.html:221  cơ chế bình thường
payment-system.html:223  Tính tạm thời
payment-system.html:225  Tính bình thường
payment-system.html:229  Tính bình đẳng ... cùng một lần hai lần
hotel-reservation.html:67  reservationID là một chìa khóa bình thường
hotel-reservation.html:179  API tạm thời
digital-wallet.html:59  id giao dịch (khóa bình thường)
ad-click-aggregation.html:279  xử lý ... một cách bình thường
```

Expected style:

```text
UUID cho mục đích idempotency
cơ chế idempotency
Idempotency được quản lý...
Idempotency cũng được áp dụng ở phía PSP...
reservationID là một idempotency key
Idempotent API
transaction_id (idempotency key)
xử lý kết quả tổng hợp theo cách idempotent
```

### 2. Metrics Chapter Should Keep Monitoring Vocabulary

The current translation uses `số liệu`, `trình thu thập số liệu`, `database chuỗi thời gian`, `dịch vụ truy vấn`, `hệ thống trực quan`. For this chapter, those should be standardized as:

```text
metrics
metrics source
metrics collector
time-series database / time-series DB
query service
alert manager
alert store
visualization system
```

Representative lines: `metrics-monitoring.html:109-114`, `:186-190`, `:261`, `:269-270`.

### 3. S3/Object Storage Should Keep Storage Terms

Current examples:

```text
s3-object-storage.html:126  Dịch vụ API
s3-object-storage.html:128  Kho dữ liệu
s3-object-storage.html:129  Kho siêu dữ liệu
s3-object-storage.html:136  mục nhập bộ chứa
s3-object-storage.html:280  Liệt kê các object trong một thùng
s3-object-storage.html:286  cửa hàng object
```

Expected style:

```text
API service
data store
metadata store
bucket entry
Listing objects in a bucket
object store
```

### 4. Stock Exchange Needs Domain-Term Locking

This chapter is very sensitive to domain vocabulary. Current Vietnamese terms like `cổng khách hàng`, `lệnh thực thi`, `dữ liệu thị trường`, `sổ lệnh`, `trình quản lý lệnh`, `trình sắp xếp chuỗi` make the chapter harder to map back to standard exchange-system design vocabulary.

Keep:

```text
client gateway
market data flow
market data
execution
fill
order book
sequencer
order manager
broker
reporter
candlestick chart
```

Representative lines: `stock-exchange.html:70`, `:74-80`, `:86`, `:103-110`, `:147`, `:180-192`, `:259`, `:284`, `:385`.

### 5. Message Queue Needs Consistent Component Terms

Keep these labels:

```text
data storage
state storage
metadata storage
coordination service
coordinator
offset
parser
script executor
object storage
```

Representative lines: `distributed-message-queue.html:100-103`, `:205`, `:234-235`, `:244`, `:347`, `:365`, `:381`.

### 6. Web Crawler Component Names Should Stay English

Current component labels such as `Trình tải xuống HTML`, `Trình phân giải DNS`, `Trình phân tích nội dung`, `Bộ lọc URL`, `Lưu trữ URL` should stay close to the source names.

Recommended labels:

```text
web crawler
Seed URLs
HTML Downloader
DNS Resolver
Content Parser
Content Seen?
Content Storage
URL Extractor
URL Filter
URL Seen?
URL Storage
Queue Router
Queue Selector
Front Queue
Back Queue
```

Representative lines: `web-crawler.html:34`, `:46-71`, `:103`, `:106`, `:121-123`.

## Suggested Verification Commands

Run these after Claude fixes the glossary:

```bash
rg -n "chìa khóa bình thường|khóa bình thường|API tạm thời|Tính tạm thời|Tính bình thường|Tính bình đẳng|cơ chế bình thường|mục đích tạm thời|cùng một lần hai lần|một cách bình thường" src/assets/content/system-design/vi
rg -n "Trình thu thập số liệu|database chuỗi thời gian|Dịch vụ truy vấn|Hệ thống trực quan|người quản lý cảnh báo" src/assets/content/system-design/vi/metrics-monitoring.html
rg -n "Dịch vụ API|Kho dữ liệu|Kho siêu dữ liệu|kho lưu trữ siêu dữ liệu|kho lưu trữ dữ liệu|bộ chứa|một thùng|cửa hàng object" src/assets/content/system-design/vi/s3-object-storage.html
rg -n "cổng khách hàng|cổng máy khách|lệnh thực thi|Luồng dữ liệu thị trường|trình quản lý lệnh|trình sắp xếp chuỗi|Sản phẩm, lệnh, thực hiện" src/assets/content/system-design/vi/stock-exchange.html
rg -n "URL hạt giống|Trình tải xuống HTML|Trình phân giải DNS|Trình phân tích nội dung|Lưu trữ URL|Bộ định tuyến hàng đợi|Bộ chọn hàng đợi|Hàng đợi phía trước|Hàng đợi quay lại" src/assets/content/system-design/vi/web-crawler.html
```

Note: some Vietnamese words like `bình thường` are valid in ordinary prose. The important part is to remove the technical mistranslations listed above.

