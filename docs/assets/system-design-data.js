// System Design notes manifest — chapter bodies are lazy-loaded from
// assets/content/system-design/{vi|en}/<slug>.html (not bundled here).
window.SYSTEM_DESIGN = {
  title: "System Design Notes",
  titleEn: "System Design Notes",
  intro:
    "Ghi chú tóm tắt cuốn System Design Interview (Alex Xu, Vol 1 & 2). Đọc trực tiếp trên site — nội dung từng chương chỉ tải khi bạn mở.",
  introEn:
    "Notes summarising System Design Interview (Alex Xu, Vol 1 & 2). Read in-browser — each chapter loads on demand.",
  attribution:
    "Dựa trên System Design Interview — An Insider's Guide (Alex Xu). Ghi chú gốc: liquidslr/system-design-notes.",
  attributionEn:
    "Based on System Design Interview — An Insider's Guide (Alex Xu). Source notes: liquidslr/system-design-notes.",
  chapters: [
    { n: 1, slug: "scaling", title: "Scale từ 0 đến hàng triệu người dùng", titleEn: "Scale from Zero to Millions of Users", group: "Nền tảng", groupEn: "Fundamentals", available: true },
    { n: 2, slug: "back-of-envelope", title: "Ước lượng Back-of-the-Envelope", titleEn: "Back-of-the-Envelope Estimation", group: "Nền tảng", groupEn: "Fundamentals", available: true },
    { n: 3, slug: "framework", title: "Framework phỏng vấn System Design", titleEn: "A Framework for System Design Interviews", group: "Nền tảng", groupEn: "Fundamentals", available: false },
    { n: 4, slug: "rate-limiter", title: "Thiết kế Rate Limiter", titleEn: "Design a Rate Limiter", group: "Nền tảng", groupEn: "Fundamentals", available: false },
    { n: 5, slug: "consistent-hashing", title: "Thiết kế Consistent Hashing", titleEn: "Design Consistent Hashing", group: "Nền tảng", groupEn: "Fundamentals", available: false },
    { n: 6, slug: "key-value-store", title: "Thiết kế Key-Value Store", titleEn: "Design a Key-Value Store", group: "Vol 1 — Case study", groupEn: "Vol 1 — Case studies", available: false },
    { n: 7, slug: "unique-id-generator", title: "Unique ID Generator phân tán", titleEn: "Design a Unique ID Generator", group: "Vol 1 — Case study", groupEn: "Vol 1 — Case studies", available: false },
    { n: 8, slug: "url-shortener", title: "Thiết kế URL Shortener", titleEn: "Design a URL Shortener", group: "Vol 1 — Case study", groupEn: "Vol 1 — Case studies", available: false },
    { n: 9, slug: "web-crawler", title: "Thiết kế Web Crawler", titleEn: "Design a Web Crawler", group: "Vol 1 — Case study", groupEn: "Vol 1 — Case studies", available: false },
    { n: 10, slug: "notification-system", title: "Thiết kế Notification System", titleEn: "Design a Notification System", group: "Vol 1 — Case study", groupEn: "Vol 1 — Case studies", available: false },
    { n: 11, slug: "news-feed", title: "Thiết kế News Feed", titleEn: "Design a News Feed System", group: "Vol 1 — Case study", groupEn: "Vol 1 — Case studies", available: false },
    { n: 12, slug: "chat-system", title: "Thiết kế Chat System", titleEn: "Design a Chat System", group: "Vol 1 — Case study", groupEn: "Vol 1 — Case studies", available: false },
    { n: 13, slug: "search-autocomplete", title: "Thiết kế Search Autocomplete", titleEn: "Design a Search Autocomplete System", group: "Vol 1 — Case study", groupEn: "Vol 1 — Case studies", available: false },
    { n: 14, slug: "youtube", title: "Thiết kế YouTube", titleEn: "Design YouTube", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 15, slug: "google-drive", title: "Thiết kế Google Drive", titleEn: "Design Google Drive", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 16, slug: "proximity-service", title: "Proximity Service", titleEn: "Proximity Service", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 17, slug: "nearby-friends", title: "Nearby Friends", titleEn: "Nearby Friends", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 18, slug: "google-maps", title: "Thiết kế Google Maps", titleEn: "Design Google Maps", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 19, slug: "distributed-message-queue", title: "Distributed Message Queue", titleEn: "Distributed Message Queue", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 20, slug: "metrics-monitoring", title: "Metrics Monitoring & Alerting", titleEn: "Metrics Monitoring and Alerting System", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 21, slug: "ad-click-aggregation", title: "Ad Click Event Aggregation", titleEn: "Ad Click Event Aggregation", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 22, slug: "hotel-reservation", title: "Hotel Reservation System", titleEn: "Hotel Reservation System", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 23, slug: "distributed-email", title: "Distributed Email Service", titleEn: "Distributed Email Service", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 24, slug: "s3-object-storage", title: "S3-like Object Storage", titleEn: "S3-like Object Storage", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 25, slug: "gaming-leaderboard", title: "Real-time Gaming Leaderboard", titleEn: "Real-time Gaming Leaderboard", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 26, slug: "payment-system", title: "Payment System", titleEn: "Payment System", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 27, slug: "digital-wallet", title: "Digital Wallet", titleEn: "Digital Wallet", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
    { n: 28, slug: "stock-exchange", title: "Stock Exchange", titleEn: "Stock Exchange", group: "Vol 2 — Case study", groupEn: "Vol 2 — Case studies", available: false },
  ],
};
