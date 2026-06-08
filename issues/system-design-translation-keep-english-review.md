# Review: Keep English terms (System Design VI)

Date: 2026-06-07  
**Status: FIXED** (round 3 sweep — policy in `scripts/review_system_design.py`)

## OpenAI / user feedback

Nhiều thuật ngữ System Design **không cần dịch sang tiếng Việt** — giữ tiếng Anh (hoặc hybrid) là ổn và thường rõ hơn trong phỏng vấn Big Tech.

## Policy

| Giữ tiếng Anh | Ví dụ trước (MT/dịch literal) |
|---------------|-------------------------------|
| Component headings | Thành phần, Linh kiện → **Components** |
| Infrastructure | cơ sở dữ liệu → **database**, máy chủ web → **web server** |
| Workers | nhân viên xử lý thư → **mail worker** |
| Storage | kho đối tượng → **object store** |
| Domain (news feed) | nguồn cấp dữ liệu → **news feed**, bạn bè → **friends** |
| Kafka | phân vùng → **partition**, bản sao (replica ctx) → **replica** |
| Protocols | NHẠC POP → **POP3** |
| S3 | lưu trữ đối tượng → **object storage** |
| API docs | Điểm cuối / Thông số / Tham số → **Endpoint** / **Parameters** / **query parameters**; `(xác thực)` → `(auth)` |
| News feed chapter | Xuất bản/Xây dựng news feed → **Feed publishing** / **News feed building**; Fanout on write/read; service names giữ EN |
| Push/pull | mô hình đẩy/kéo → **push/pull model**; kiến trúc đẩy/kéo → **push/pull architecture**; thông báo đẩy → **push notification** |
| Metadata / fetch | siêu dữ liệu → **metadata**; tìm nạp → **fetch** |
| Hashing / sharding | băm nhất quán → **consistent hashing**; phân mảnh → **sharding** |
| Replication | sao chép (infra) → **replicate/replication**; bản sao (DB) → **replica**; read replica, ISR |
| Queues | hàng đợi thư chết → **dead letter queue**; retry queue |
| Client / sync | máy khách → **client**; đồng bộ hóa → **sync**; Cò súng → **Long polling** |
| Services | Dịch vụ thanh toán/truy vấn/thông báo → **Payment/Query/Notification service** |
| Workers | Công nhân → **Worker** |
| Email (khác Kafka topic) | chủ đề (email) → **subject** |

Vẫn dịch câu giải thích tiếng Việt; chỉ **khóa jargon** phỏng vấn. Giữ **chủ đề** khi nghĩa “topic nội dung” (web crawler), không nhầm với Kafka **topic**.

## Applied in script

- `KEEP_ENGLISH_FIXES` — global safe replacements
- `FILE_FIXES` extended: `news-feed`, `nearby-friends`, `framework`, `distributed-message-queue`, `s3-object-storage`, `payment-system`
- Removed rule `Linh kiện → Thành phần` (now **Components**)

## Re-run after future MT

```bash
python3 scripts/review_system_design.py
```
