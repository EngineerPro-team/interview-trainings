# Follow-up deep review: System Design VI keep-English glossary

Date: 2026-06-07 17:22 +07  
**Status: FIXED** (2026-06-07 — follow-up sweep in `scripts/review_system_design.py`)

Scope: current files under `src/assets/content/system-design/vi`.

## Summary

The earlier high-risk bugs are mostly fixed:

- `idempotency` mistranslations now return zero hits.
- Old `stock-exchange` literals such as `công cụ khớp`, `trình sắp xếp thứ tự`, `Luồng giao dịch` return zero hits.
- Old `payment-system` artifacts such as `phong trào tiền bạc`, `sợi dây`, `thăm dò khóa ngoại` return zero hits.
- Old image-heading / `Tôi:` / uppercase `BẰNG` checks return zero hits.

All 7 finding groups addressed. Verification `rg` patterns from this report return zero hits (except `phân chia thành các miền lỗi` in erasure-coding prose — intentional VN explanation).

## Findings

| # | Severity | Area | Status |
|---|----------|------|--------|
| 1 | High | metrics-monitoring hybrid phrases | **FIXED** |
| 2 | High | s3-object-storage terms | **FIXED** |
| 3 | High | API/doc labels | **FIXED** (Sample response, Response Construction) |
| 4 | Medium | web-crawler intro/terms | **FIXED** |
| 5 | Medium | YouTube/ad-click resource terms | **FIXED** |
| 6 | Medium | stock-exchange API fields | **FIXED** |
| 7 | Medium | distributed-message-queue | **FIXED** |

### Original findings table

| # | Severity | Area | Examples | Recommended fix |
|---|----------|------|----------|-----------------|
| 1 | High | `metrics-monitoring.html` still mixes `metrics` with `số liệu` and has malformed hybrid phrases | `:132` `Metrics collector Fetch metadata`; `:135`, `:137`, `:141`, `:144`, `:146`, `:158`, `:183`; `:185` `Visualization system hóa`; `:187-192` `DB chuỗi thời gian` | Standardize chapter-wide to `metrics`, `metrics collector`, `time-series DB`, `collector`, `Visualization system`; fix grammar after replacements. |
| 2 | High | `s3-object-storage.html` still has wrong/awkward object-storage terms | `:114` `vật thể`; `:126` `kho Object storage`; `:129` `metadata storage object`; `:322-325` `kho Object storage`, `lập phiên bản`, `replication coding và xóa`, `tải lên nhiều phần`, `phân chia` | Use `object`, `object storage`, `metadata store stores object metadata`, `versioning`, `erasure coding`, `multipart upload`, `sharding`. |
| 3 | High | API/doc labels are still translated inconsistently across chapters | `digital-wallet.html:60`; `distributed-email.html:61`, `:74`; `gaming-leaderboard.html:52`, `:75`; `google-maps.html:95`, `:183`; `search-autocomplete.html:105` | Standardize to `Response`, `Sample response`, `Response Construction`, `Request parameters`, `Query parameters`. |
| 4 | Medium | `web-crawler.html` intro and remaining crawler terms should keep English | `:2-3` `trình thu thập dữ liệu web`, `nhện`; `:156` `Bẫy nhện`; `:163-164` translated `web crawler`, `politeness`, `priority` | Keep `web crawler`, `spider`, `spider trap`, `politeness`, `priority`, `search engine indexing`. |
| 5 | Medium | YouTube/ad-click resource terms still translated | `youtube.html:44-46`, `:54`, `:63-64`, `:66`; `ad-click-aggregation.html:309-310` | Keep `origin storage`, `transcoding server`, `transcoded storage`, `blob storage`, `resource manager`. |
| 6 | Medium | `stock-exchange.html` API field names/types still partially translated | `:147` `thực thi`; `:162-163` `giá thầu`, `hỏi`; `:173-177` `nến`, `Gấp đôi` | Keep field names and types: `executions`, `bids`, `asks`, `candles`, `open`, `close`, `high`, `low`, `Double`, `Array`. |
| 7 | Medium | `distributed-message-queue.html` still has coordinator/storage/offset terms translated or malformed | `:100`, `:103`, `:196`, `:205`, `:219`, `:235`, `:347`, `:365`, `:381` | Keep `data storage`, `coordination service`, `coordinator`, `offset`, `parser`, `script executor`, `Historical data archive`, `object storage`; fix `consumer Fetch` casing. |

## Detailed Notes

### 1. Metrics Chapter Needs Another Consistency Pass

Examples from current `metrics-monitoring.html`:

```text
132  Metrics collector Fetch metadata cấu hình...
135  bộ thu thập số liệu
137  bộ thu thập số liệu duy nhất
141  push metrics ... đến bộ thu thập số liệu
144  metrics collector số liệu
146  gửi chúng đến người thu thập
158  bộ thu thập số liệu ... bộ load balancer
183  gửi nó đến bộ thu thập số liệu
185  Visualization system hóa
187  DB chuỗi thời gian
192  DB chuỗi thời gian
232  | số liệu | dấu thời gian | tên máy chủ |
```

Suggested normalized style:

```text
Metrics collector fetches metadata cấu hình...
một metrics collector duy nhất
push metrics đến metrics collector
collector
Visualization system
time-series DB
| metric | timestamp | hostname | metric_value |
```

### 2. S3/Object Storage Still Has A Few Literal Terms

Examples:

```text
s3-object-storage.html:114  Hỗ trợ cả vật thể nhỏ và lớn
s3-object-storage.html:126  kho Object storage
s3-object-storage.html:129  metadata storage object
s3-object-storage.html:322  Thiết kế kho Object storage giống S3
s3-object-storage.html:325  replication coding và xóa, tải lên nhiều phần, phân chia
```

Suggested style:

```text
Hỗ trợ cả object nhỏ và lớn
object storage
Metadata store - stores object metadata
erasure coding, multipart upload, sharding
```

### 3. API Labels Should Be English Everywhere

Current examples:

```text
digital-wallet.html:60           Phản hồi mẫu
distributed-email.html:61        Phản hồi ví dụ
gaming-leaderboard.html:52       Phản hồi ví dụ
google-maps.html:95              Phản hồi ví dụ
search-autocomplete.html:105     Xây dựng phản hồi
```

Suggested style:

```text
Sample response
Response
Response Construction
```

### 4. Web Crawler Still Has Literal Component/Concept Terms

Examples:

```text
web-crawler.html:2   trình thu thập dữ liệu web, nhện
web-crawler.html:3   Ứng dụng của trình thu thập dữ liệu web
web-crawler.html:156 Bẫy nhện
web-crawler.html:163 Trình thu thập dữ liệu web
web-crawler.html:164 lịch sự, sự ưu tiên
```

Suggested style:

```text
web crawler, spider
Applications of web crawler
Spider trap
web crawler
politeness, priority
```

### 5. YouTube / Resource Management Terms

Examples:

```text
youtube.html:44  Lưu trữ gốc
youtube.html:45  Máy chủ chuyển mã
youtube.html:46  Lưu trữ được chuyển mã
youtube.html:54  bộ nhớ gốc
youtube.html:63  bộ nhớ blob
youtube.html:64  Máy chủ chuyển mã
ad-click-aggregation.html:309-310  trình quản lý tài nguyên / Trình quản lý tài nguyên
```

Suggested style:

```text
origin storage
transcoding server
transcoded storage
blob storage
resource manager
```

## Verification Commands

Run these after the next fix:

```bash
rg -n "Fetch metadata|collector số liệu|bộ thu thập số liệu|người thu thập|DB chuỗi thời gian|Visualization system hóa|\\| số liệu \\| dấu thời gian" src/assets/content/system-design/vi/metrics-monitoring.html
rg -n "vật thể|kho Object storage|metadata storage object|replication coding và xóa|lập phiên bản|tải lên nhiều phần|phân chia" src/assets/content/system-design/vi/s3-object-storage.html
rg -n "Phản hồi mẫu|Phản hồi ví dụ|Xây dựng phản hồi|phản hồi:" src/assets/content/system-design/vi
rg -n "trình thu thập dữ liệu web|nhện|Bẫy nhện|lịch sự|sự ưu tiên" src/assets/content/system-design/vi/web-crawler.html
rg -n "Lưu trữ gốc|Máy chủ chuyển mã|Lưu trữ được chuyển mã|bộ nhớ gốc|bộ nhớ blob|trình quản lý tài nguyên|Trình quản lý tài nguyên" src/assets/content/system-design/vi/youtube.html src/assets/content/system-design/vi/ad-click-aggregation.html
rg -n "thực thi -|giá thầu|hỏi -|nến -|Gấp đôi" src/assets/content/system-design/vi/stock-exchange.html
rg -n "Dịch vụ điều phối|dịch vụ điều phối|người điều phối|Người điều phối|Lưu trữ dữ liệu|phần bù|trình phân tích cú pháp|trình thực thi tập lệnh|kho lưu trữ dung lượng cao|lưu trữ đối tượng|consumer Fetch" src/assets/content/system-design/vi/distributed-message-queue.html
```

