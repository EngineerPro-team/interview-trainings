"""Chapter metadata for System Design notes (v2 — original EngineerPro content).

The v2 chapters are hand-authored HTML (EN + VI) under
src/assets/content/system-design/{en,vi}/<slug>.html with original Mermaid
diagrams. They are NOT generated from an external markdown source, so the old
build_system_design.py markdown pipeline no longer applies to them; the manifest
src/assets/system-design-data.js is hand-maintained.
"""

from __future__ import annotations

CHAPTERS: list[dict] = [
    {"n": 1, "slug": "redis-in-memory-store", "title": "Redis (In-memory Store)",
     "titleEn": "Redis (In-memory Store)", "group": "Infra building blocks", "groupEn": "Infra building blocks"},
    {"n": 2, "slug": "cdn-system", "title": "CDN", "titleEn": "CDN",
     "group": "Infra building blocks", "groupEn": "Infra building blocks"},
    {"n": 3, "slug": "blob-storage", "title": "Blob Storage (S3-like)", "titleEn": "Blob Storage (S3-like)",
     "group": "Infra building blocks", "groupEn": "Infra building blocks"},
    {"n": 4, "slug": "coordination-service", "title": "Coordination / Lock Service",
     "titleEn": "Coordination / Lock Service", "group": "Infra building blocks", "groupEn": "Infra building blocks"},
    {"n": 5, "slug": "distributed-job-scheduler", "title": "Distributed Job Scheduler",
     "titleEn": "Distributed Job Scheduler", "group": "Infra building blocks", "groupEn": "Infra building blocks"},
    {"n": 6, "slug": "distributed-search-engine", "title": "Distributed Search Engine",
     "titleEn": "Distributed Search Engine", "group": "Infra building blocks", "groupEn": "Infra building blocks"},
    {"n": 7, "slug": "observability-pipeline", "title": "Observability Pipeline",
     "titleEn": "Observability Pipeline", "group": "Infra building blocks", "groupEn": "Infra building blocks"},
    {"n": 8, "slug": "llm-inference-platform", "title": "LLM Inference Platform",
     "titleEn": "LLM Inference Platform", "group": "AI / Agentic infra", "groupEn": "AI / Agentic infra"},
    {"n": 9, "slug": "rag-system", "title": "RAG System + Vector Search",
     "titleEn": "RAG System + Vector Search", "group": "AI / Agentic infra", "groupEn": "AI / Agentic infra"},
    {"n": 10, "slug": "agentic-ai-platform", "title": "Agentic AI Orchestration",
     "titleEn": "Agentic AI Orchestration", "group": "AI / Agentic infra", "groupEn": "AI / Agentic infra"},
    {"n": 11, "slug": "ai-coding-agent", "title": "AI Coding Agent Platform",
     "titleEn": "AI Coding Agent Platform", "group": "AI / Agentic infra", "groupEn": "AI / Agentic infra"},
    {"n": 12, "slug": "zoom-video-conferencing", "title": "Zoom (Video Conferencing)",
     "titleEn": "Zoom (Video Conferencing)", "group": "Realtime & Media", "groupEn": "Realtime & Media"},
    {"n": 13, "slug": "telegram-chat", "title": "Telegram (Chat System)",
     "titleEn": "Telegram (Chat System)", "group": "Social & Messaging", "groupEn": "Social & Messaging"},
    {"n": 14, "slug": "facebook-news-feed", "title": "Facebook News Feed",
     "titleEn": "Facebook News Feed", "group": "Social & Messaging", "groupEn": "Social & Messaging"},
    {"n": 15, "slug": "google-docs-collab", "title": "Google Docs (Collaborative Editing)",
     "titleEn": "Google Docs (Collaborative Editing)", "group": "Realtime & Media", "groupEn": "Realtime & Media"},
    {"n": 16, "slug": "netflix-streaming", "title": "Netflix (Video Streaming)",
     "titleEn": "Netflix (Video Streaming)", "group": "Realtime & Media", "groupEn": "Realtime & Media"},
    {"n": 17, "slug": "grab-food-delivery", "title": "Grab Food (Delivery)",
     "titleEn": "Grab Food (Delivery)", "group": "Marketplace & Booking", "groupEn": "Marketplace & Booking"},
    {"n": 18, "slug": "uber-ride-hailing", "title": "Uber (Ride-Hailing)",
     "titleEn": "Uber (Ride-Hailing)", "group": "Marketplace & Booking", "groupEn": "Marketplace & Booking"},
    {"n": 19, "slug": "online-auction", "title": "Auction System", "titleEn": "Auction System",
     "group": "Marketplace & Booking", "groupEn": "Marketplace & Booking"},
    {"n": 20, "slug": "flight-booking", "title": "Flight Booking", "titleEn": "Flight Booking",
     "group": "Marketplace & Booking", "groupEn": "Marketplace & Booking"},
    {"n": 21, "slug": "stock-exchange-v2", "title": "Stock Exchange", "titleEn": "Stock Exchange",
     "group": "Marketplace & Booking", "groupEn": "Marketplace & Booking"},
]

# All v2 chapters are shown on the site.
MANIFEST_CHAPTERS: list[dict] = list(CHAPTERS)
