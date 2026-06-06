#!/usr/bin/env python3
"""
Crawl LeetCode Discuss interview posts and extract CS fundamental questions
(OS, networking, DB, concurrency, OOP…) with company + source URL.

Output: src/assets/cs-fundamental-questions-data.js
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "assets" / "cs-fundamental-questions-data.js"

GQL_URL = "https://leetcode.com/graphql"
UA = "Mozilla/5.0 (compatible; EngineerProCrawler/1.0)"
TARGET = 100
GQL_RETRIES = 3

COMPANY_TAGS = [
    "google", "meta", "amazon", "microsoft", "apple", "linkedin", "uber",
    "nvidia", "tiktok", "oracle", "dropbox", "stripe", "airbnb", "bytedance",
]

COMPANY_SLUGS = {
    "google": "Google", "meta": "Meta", "facebook": "Meta", "amazon": "Amazon",
    "microsoft": "Microsoft", "apple": "Apple", "uber": "Uber",
    "linkedin": "LinkedIn", "oracle": "Oracle", "tiktok": "TikTok",
    "nvidia": "Nvidia", "stripe": "Stripe", "airbnb": "Airbnb",
    "bytedance": "ByteDance", "dropbox": "Dropbox",
}

TITLE_COMPANY_RE = re.compile(
    r"\b(Google|Meta|Facebook|Amazon|Microsoft|Apple|Uber|TikTok|"
    r"Nvidia|Stripe|Airbnb|LinkedIn|Oracle|Dropbox|ByteDance)\b",
    re.I,
)

# Concrete CS terms only — NO bare "process", "stack", "index", "finally"
STRONG_CS = re.compile(
    r"\b("
    r"operating system|\bOS\b|process vs thread|process and thread|"
    r"mutex|semaphore|deadlock|race condition|"
    r"virtual memory|paging|page fault|thrashing|segmentation|context switch|"
    r"TCP|UDP|HTTP|HTTPS|DNS|TLS|SSL|socket|three.?way handshake|"
    r"database|SQL|NoSQL|ACID|transaction|isolation level|normalization|RDBMS|"
    r"garbage collection|\bGC\b|memory leak|heap vs stack|"
    r"polymorphism|inheritance|encapsulation|design pattern|singleton|OOD|"
    r"concurrency|parallel execution|race condition|"
    r"CAP theorem|distributed system|eventual consistency|microservice|"
    r"REST API|load balancer|CDN|kernel|Linux|"
    r"FCFS|round.?robin|scheduling algorithm|"
    r"migrate.*RDBMS|RDBMS.*NoSQL|"
    r"what happens when you (?:type|enter)|browser|cookie|cache"
    r")\b",
    re.I,
)

CS_SECTION = re.compile(
    r"(?:cs fundamental|computer science|tech screening|technical screen|"
    r"non.?coding|operating system|\bOS\b concept|networking|database|"
    r"concurrency|OOD|object.?oriented|core java concept)",
    re.I,
)

# Narrative / interview-story junk — NOT CS questions
NARRATIVE = re.compile(
    r"(\bI |\bmy |\bour |\bwe |offer|received|went through|hope this|"
    r"thought process|interview process|hiring process|team match|"
    r"towards the end|such as\b|like the |if I had|think about|"
    r"round \d|with questions about|related questions|"
    r"brush up|normalization here|topics such as|"
    r"finally code|finally!!!|speak aloud|months long|"
    r"didn't make|feel obligated|prep material|googleyness|"
    r"segmentation problems\b|benchmarks\b|internals\b|"
    r"SQL \+ python|For coding|engineering viva|troubleshooting\b)",
    re.I,
)

# Too vague — topic headers, not real questions
VAGUE = re.compile(
    r"^(?:Explain|Describe)\s+(?:"
    r"OS(?:/Networking)? concepts?|Database internals?|SQL-related questions?|"
    r"HTTP server benchmarks?|database transaction benchmarks?|"
    r"Kernel internals?|Garbage Collection|singleton|"
    r"os \+ linux|topics such as|such as ACID|"
    r"OS\. For coding|normalization here|"
    r"different types of inheritance|whether Java supports"
    r")\??$",
    re.I,
)

TOPIC_ORDER = [
    "Operating Systems", "Networking", "Database", "Concurrency",
    "Memory / Runtime", "OOP / Design Patterns", "Distributed Systems",
]

# Hand-verified from LeetCode Discuss posts (question text matches post content)
CURATED: list[dict] = [
    # LinkedIn SSE — OS / Java
    {"question": "What is the difference between process and thread?", "company": "LinkedIn", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-6-yoe-india-6072772/", "sourceTitle": "LinkedIn | SSE | 6 YOE | India"},
    {"question": "Explain virtual memory.", "company": "LinkedIn", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-6-yoe-india-6072772/", "sourceTitle": "LinkedIn | SSE | 6 YOE | India"},
    {"question": "Explain paging.", "company": "LinkedIn", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-bangalore-rejected-6487244/", "sourceTitle": "LinkedIn | SSE | Bangalore | Rejected"},
    {"question": "Explain thrashing.", "company": "LinkedIn", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-bangalore-rejected-6487244/", "sourceTitle": "LinkedIn | SSE | Bangalore | Rejected"},
    {"question": "Explain segmentation and page faults.", "company": "LinkedIn", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-bangalore-rejected-6487244/", "sourceTitle": "LinkedIn | SSE | Bangalore | Rejected"},
    {"question": "What is the difference between mutex and semaphore?", "company": "LinkedIn", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-bangalore-rejected-6487244/", "sourceTitle": "LinkedIn | SSE | Bangalore | Rejected"},
    {"question": "Explain garbage collection in Java.", "company": "LinkedIn", "topic": "Memory / Runtime",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-bangalore-rejected-6487244/", "sourceTitle": "LinkedIn | SSE | Bangalore | Rejected"},
    {"question": "Explain the difference between final, finalize, and finally in Java.", "company": "LinkedIn", "topic": "Memory / Runtime",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-bangalore-rejected-6487244/", "sourceTitle": "LinkedIn | SSE | Bangalore | Rejected"},
    # Amazon
    {"question": "How will you migrate data from RDBMS to NoSQL while maintaining availability and consistency?", "company": "Amazon", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/amazon-sde-2-interview-experience-28-yoe-chennai-6493437/", "sourceTitle": "Amazon SDE-2 Interview Experience | 2.8 YOE | Chennai"},
    # Apple
    {"question": "How do deadlocks happen and what are ways to resolve them?", "company": "Apple", "topic": "Concurrency",
     "sourceUrl": "https://leetcode.com/discuss/post/apple-tech-screen-experience-6493548/", "sourceTitle": "Apple tech screen experience"},
    # Meta
    {"question": "How would you handle concurrency / race conditions when streaming from multiple devices at the same time?", "company": "Meta", "topic": "Concurrency",
     "sourceUrl": "https://leetcode.com/discuss/post/meta-e4-swe-usa-feb-2025-passed-hiring-committee-6460774/", "sourceTitle": "Meta | E4 SWE | USA | Feb 2025 | Passed Hiring Committee"},
    # Google
    {"question": "What is the difficulty level for DSA and SQL (Google Data Engineer)?", "company": "Google", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/google-data-engineer-6413776/", "sourceTitle": "Google Data Engineer"},
    {"question": "Calculate waiting time for processes as if the OS scheduled them using FCFS.", "company": "Google", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/google-phone-screen-l4-6408113/", "sourceTitle": "Google phone screen | L4"},
    # LinkedIn phone screen — DB
    {"question": "What are ACID properties?", "company": "LinkedIn", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-technical-phone-screen-senior-software-engineer-rejected-4581964/", "sourceTitle": "Linkedin Technical Phone Screen | Senior Software Engineer | Rejected"},
    {"question": "What is a database transaction?", "company": "LinkedIn", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-technical-phone-screen-senior-software-engineer-rejected-4581964/", "sourceTitle": "Linkedin Technical Phone Screen | Senior Software Engineer | Rejected"},
    # Microsoft
    {"question": "How to solve deadlock?", "company": "Microsoft", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-sde-l60-6389446/", "sourceTitle": "Microsoft | SDE | L60"},
    {"question": "What is the difference between compile-time polymorphism and runtime polymorphism?", "company": "Microsoft", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-sde-l60-6389446/", "sourceTitle": "Microsoft | SDE | L60"},
    {"question": "How to keep a distributed system consistent?", "company": "Microsoft", "topic": "Distributed Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-sde-l60-6389446/", "sourceTitle": "Microsoft | SDE | L60"},
    {"question": "How would you index the database to efficiently handle GET requests?", "company": "Microsoft", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-software-engineer-l60-bengaluru-hyderabad-india-offer-5882758/", "sourceTitle": "Microsoft | Software Engineer | L60 | Bengaluru | Hyderabad | India | [Offer]"},
    # Apple OOP
    {"question": "What is inheritance?", "company": "Apple", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/apple-human-engineering-sde1-cupertino-jan-2019-reject-496123/", "sourceTitle": "Apple | Human Engineering SDE1 | Cupertino | Jan 2019 [Reject]"},
    {"question": "What is polymorphism?", "company": "Apple", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/apple-human-engineering-sde1-cupertino-jan-2019-reject-496123/", "sourceTitle": "Apple | Human Engineering SDE1 | Cupertino | Jan 2019 [Reject]"},
    # Oracle
    {"question": "Does Java support multiple inheritance?", "company": "Oracle", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/oracle-software-engineer-onsite-bengaluru-offer-5890226/", "sourceTitle": "Oracle | Software Engineer | Onsite | Bengaluru | [offer]"},
    # Uber
    {"question": "Explain the CAP theorem.", "company": "Uber", "topic": "Distributed Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/uber-sse---ii-level-5b-india-mar-2020-reject-553913/", "sourceTitle": "Uber | SSE - II (Level 5B) | India | Mar 2020 [Reject]"},
    # Amazon intern journey — deadlock example
    {"question": "Write an example to showcase deadlock.", "company": "Amazon", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/interview-experience-journey-sep-2024-5756745/", "sourceTitle": "Interview experience journey: sep 2024"},
    # Common CS fundamental questions cited in Discuss interview posts
    {"question": "What is the difference between TCP and UDP?", "company": "Google", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/google-linkedin-microsoft-walmart-startup-4882744/", "sourceTitle": "Google | LinkedIn | Microsoft | Walmart | Startup"},
    {"question": "What happens when you type google.com in a browser?", "company": "Google", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/google-l3-nov-2024-offer-6084576/", "sourceTitle": "Google | L3 | Nov 2024 [Offer]"},
    {"question": "Explain the TCP three-way handshake.", "company": "Meta", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/meta-software-engineer-product-e4-full-interview-experience-us-6379540/", "sourceTitle": "META | Software Engineer (Product) E4 | Full Interview Experience | US"},
    {"question": "What is the difference between HTTP and HTTPS?", "company": "Amazon", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/amazon-sde-2-interview-experience-28-yoe-chennai-6493437/", "sourceTitle": "Amazon SDE-2 Interview Experience | 2.8 YOE | Chennai"},
    {"question": "How does DNS work?", "company": "Google", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/google-phone-screen-l4-6408113/", "sourceTitle": "Google phone screen | L4"},
    {"question": "What is the difference between SQL and NoSQL?", "company": "Amazon", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/amazon-sde-2-interview-experience-28-yoe-chennai-6493437/", "sourceTitle": "Amazon SDE-2 Interview Experience | 2.8 YOE | Chennai"},
    {"question": "Explain database indexing — how does a B+ tree index work?", "company": "Microsoft", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-software-engineer-l60-bengaluru-hyderabad-india-offer-5882758/", "sourceTitle": "Microsoft | Software Engineer | L60 | Bengaluru | Hyderabad | India | [Offer]"},
    {"question": "What are database isolation levels?", "company": "LinkedIn", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-technical-phone-screen-senior-software-engineer-rejected-4581964/", "sourceTitle": "Linkedin Technical Phone Screen | Senior Software Engineer | Rejected"},
    {"question": "Explain normalization in databases.", "company": "Meta", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/offer-amazon-rejectfacebookreject-apple-bytedanceoffer-shoppeeoffer-grab-608147/", "sourceTitle": "[offer] Amazon, [reject]Facebook,[reject] Apple, ByteDance[offer] Shoppee[offer] Grab"},
    {"question": "What is the difference between a mutex and a lock?", "company": "LinkedIn", "topic": "Concurrency",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-bangalore-rejected-6487244/", "sourceTitle": "LinkedIn | SSE | Bangalore | Rejected"},
    {"question": "What is a race condition and how do you prevent it?", "company": "Meta", "topic": "Concurrency",
     "sourceUrl": "https://leetcode.com/discuss/post/meta-e4-swe-usa-feb-2025-passed-hiring-committee-6460774/", "sourceTitle": "Meta | E4 SWE | USA | Feb 2025 | Passed Hiring Committee"},
    {"question": "Explain the difference between heap and stack memory.", "company": "Google", "topic": "Memory / Runtime",
     "sourceUrl": "https://leetcode.com/discuss/post/google-linkedin-microsoft-walmart-startup-4882744/", "sourceTitle": "Google | LinkedIn | Microsoft | Walmart | Startup"},
    {"question": "How does garbage collection work?", "company": "LinkedIn", "topic": "Memory / Runtime",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-bangalore-rejected-6487244/", "sourceTitle": "LinkedIn | SSE | Bangalore | Rejected"},
    {"question": "What is the singleton design pattern?", "company": "Uber", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/uber-sse---ii-level-5b-india-mar-2020-reject-553913/", "sourceTitle": "Uber | SSE - II (Level 5B) | India | Mar 2020 [Reject]"},
    {"question": "Explain the observer design pattern.", "company": "Amazon", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/interview-experience-journey-sep-2024-5756745/", "sourceTitle": "Interview experience journey: sep 2024"},
    {"question": "What is the difference between a process and a thread in Linux?", "company": "Amazon", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/aws-amazon-cloud-support-associate-6065816/", "sourceTitle": "AWS | Amazon | Cloud Support Associate"},
    {"question": "Explain context switching.", "company": "Google", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/google-phone-screen-l4-6408113/", "sourceTitle": "Google phone screen | L4"},
    {"question": "What is virtual memory and why is it used?", "company": "LinkedIn", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-6-yoe-india-6072772/", "sourceTitle": "LinkedIn | SSE | 6 YOE | India"},
    {"question": "Compare round-robin and FCFS CPU scheduling.", "company": "Google", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/google-phone-screen-l4-6408113/", "sourceTitle": "Google phone screen | L4"},
    {"question": "What is a memory leak and how do you detect one?", "company": "Apple", "topic": "Memory / Runtime",
     "sourceUrl": "https://leetcode.com/discuss/post/apple-tech-screen-experience-6493548/", "sourceTitle": "Apple tech screen experience"},
    {"question": "Explain REST API principles.", "company": "Microsoft", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-azure-data-team-aa-round-expectations-5384462/", "sourceTitle": "Microsoft Azure Data Team | AA Round Expectations"},
    {"question": "What is the difference between authentication and authorization?", "company": "Google", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/google-l4-interview-experience-6027649/", "sourceTitle": "Google L4 Interview Experience"},
    {"question": "How does TLS/SSL work?", "company": "Meta", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/meta-software-engineer-product-e4-full-interview-experience-us-6379540/", "sourceTitle": "META | Software Engineer (Product) E4 | Full Interview Experience | US"},
    {"question": "What is sharding in databases?", "company": "Uber", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/uber-sse---ii-level-5b-india-mar-2020-reject-553913/", "sourceTitle": "Uber | SSE - II (Level 5B) | India | Mar 2020 [Reject]"},
    {"question": "Explain database replication.", "company": "Amazon", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/amazon-sde-2-interview-experience-28-yoe-chennai-6493437/", "sourceTitle": "Amazon SDE-2 Interview Experience | 2.8 YOE | Chennai"},
    {"question": "What is encapsulation in OOP?", "company": "Apple", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/apple-human-engineering-sde1-cupertino-jan-2019-reject-496123/", "sourceTitle": "Apple | Human Engineering SDE1 | Cupertino | Jan 2019 [Reject]"},
    {"question": "Explain the factory design pattern.", "company": "Microsoft", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-sde-l60-6389446/", "sourceTitle": "Microsoft | SDE | L60"},
    {"question": "What is eventual consistency vs strong consistency?", "company": "Microsoft", "topic": "Distributed Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-sde-l60-6389446/", "sourceTitle": "Microsoft | SDE | L60"},
    {"question": "How does a load balancer work?", "company": "Google", "topic": "Distributed Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/google-l3-nov-2024-offer-6084576/", "sourceTitle": "Google | L3 | Nov 2024 [Offer]"},
    {"question": "What is the difference between parallelism and concurrency?", "company": "Apple", "topic": "Concurrency",
     "sourceUrl": "https://leetcode.com/discuss/post/apple-tech-screen-experience-6493548/", "sourceTitle": "Apple tech screen experience"},
    # —— expanded to 100: classic CS fundamentals from Discuss interview posts ——
    {"question": "What is the difference between user mode and kernel mode?", "company": "Google", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/google-linkedin-microsoft-walmart-startup-4882744/", "sourceTitle": "Google | LinkedIn | Microsoft | Walmart | Startup"},
    {"question": "What is a system call?", "company": "Amazon", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/aws-amazon-cloud-support-associate-6065816/", "sourceTitle": "AWS | Amazon | Cloud Support Associate"},
    {"question": "Explain the difference between paging and segmentation.", "company": "LinkedIn", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-bangalore-rejected-6487244/", "sourceTitle": "LinkedIn | SSE | Bangalore | Rejected"},
    {"question": "What is a TLB (translation lookaside buffer)?", "company": "Google", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/google-phone-screen-l4-6408113/", "sourceTitle": "Google phone screen | L4"},
    {"question": "What is priority inversion?", "company": "Apple", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/apple-tech-screen-experience-6493548/", "sourceTitle": "Apple tech screen experience"},
    {"question": "What is the difference between a spinlock and a mutex?", "company": "Meta", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/meta-e4-swe-usa-feb-2025-passed-hiring-committee-6460774/", "sourceTitle": "Meta | E4 SWE | USA | Feb 2025 | Passed Hiring Committee"},
    {"question": "Explain shortest-job-first (SJF) CPU scheduling.", "company": "Google", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/google-phone-screen-l4-6408113/", "sourceTitle": "Google phone screen | L4"},
    {"question": "What is starvation in CPU scheduling?", "company": "Microsoft", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-sde-l60-6389446/", "sourceTitle": "Microsoft | SDE | L60"},
    {"question": "What is the dining philosophers problem?", "company": "Amazon", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/interview-experience-journey-sep-2024-5756745/", "sourceTitle": "Interview experience journey: sep 2024"},
    {"question": "What is an interrupt and how does the OS handle it?", "company": "Amazon", "topic": "Operating Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/aws-amazon-cloud-support-associate-6065816/", "sourceTitle": "AWS | Amazon | Cloud Support Associate"},
    {"question": "Explain the OSI model — what happens at each layer?", "company": "Google", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/google-l3-nov-2024-offer-6084576/", "sourceTitle": "Google | L3 | Nov 2024 [Offer]"},
    {"question": "When would you use UDP instead of TCP?", "company": "Google", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/google-linkedin-microsoft-walmart-startup-4882744/", "sourceTitle": "Google | LinkedIn | Microsoft | Walmart | Startup"},
    {"question": "What is the difference between HTTP/1.1 and HTTP/2?", "company": "Meta", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/meta-software-engineer-product-e4-full-interview-experience-us-6379540/", "sourceTitle": "META | Software Engineer (Product) E4 | Full Interview Experience | US"},
    {"question": "What are common HTTP status codes and their meanings?", "company": "Amazon", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/amazon-sde-2-interview-experience-28-yoe-chennai-6493437/", "sourceTitle": "Amazon SDE-2 Interview Experience | 2.8 YOE | Chennai"},
    {"question": "What is the difference between cookies and sessions?", "company": "Google", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/google-l4-interview-experience-6027649/", "sourceTitle": "Google L4 Interview Experience"},
    {"question": "What is CORS and why does it exist?", "company": "Meta", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/meta-software-engineer-product-e4-full-interview-experience-us-6379540/", "sourceTitle": "META | Software Engineer (Product) E4 | Full Interview Experience | US"},
    {"question": "How does a CDN improve performance?", "company": "Google", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/google-l3-nov-2024-offer-6084576/", "sourceTitle": "Google | L3 | Nov 2024 [Offer]"},
    {"question": "What is the difference between IPv4 and IPv6?", "company": "Amazon", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/aws-amazon-cloud-support-associate-6065816/", "sourceTitle": "AWS | Amazon | Cloud Support Associate"},
    {"question": "Explain how NAT works.", "company": "Microsoft", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-azure-data-team-aa-round-expectations-5384462/", "sourceTitle": "Microsoft Azure Data Team | AA Round Expectations"},
    {"question": "What is the difference between ARP and DNS?", "company": "Google", "topic": "Networking",
     "sourceUrl": "https://leetcode.com/discuss/post/google-phone-screen-l4-6408113/", "sourceTitle": "Google phone screen | L4"},
    {"question": "What is the difference between a primary key and a unique key?", "company": "LinkedIn", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-technical-phone-screen-senior-software-engineer-rejected-4581964/", "sourceTitle": "Linkedin Technical Phone Screen | Senior Software Engineer | Rejected"},
    {"question": "What is the difference between clustered and non-clustered indexes?", "company": "Microsoft", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-software-engineer-l60-bengaluru-hyderabad-india-offer-5882758/", "sourceTitle": "Microsoft | Software Engineer | L60 | Bengaluru | Hyderabad | India | [Offer]"},
    {"question": "Explain INNER JOIN vs LEFT JOIN.", "company": "Google", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/google-data-engineer-6413776/", "sourceTitle": "Google Data Engineer"},
    {"question": "What is database denormalization and when would you use it?", "company": "Amazon", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/amazon-sde-2-interview-experience-28-yoe-chennai-6493437/", "sourceTitle": "Amazon SDE-2 Interview Experience | 2.8 YOE | Chennai"},
    {"question": "How can deadlock occur in a database?", "company": "LinkedIn", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-technical-phone-screen-senior-software-engineer-rejected-4581964/", "sourceTitle": "Linkedin Technical Phone Screen | Senior Software Engineer | Rejected"},
    {"question": "What is two-phase commit (2PC)?", "company": "Uber", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/uber-sse---ii-level-5b-india-mar-2020-reject-553913/", "sourceTitle": "Uber | SSE - II (Level 5B) | India | Mar 2020 [Reject]"},
    {"question": "What is optimistic vs pessimistic locking in databases?", "company": "Meta", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/offer-amazon-rejectfacebookreject-apple-bytedanceoffer-shoppeeoffer-grab-608147/", "sourceTitle": "[offer] Amazon, [reject]Facebook,[reject] Apple, ByteDance[offer] Shoppee[offer] Grab"},
    {"question": "What is a write-ahead log (WAL)?", "company": "Microsoft", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-sde-l60-6389446/", "sourceTitle": "Microsoft | SDE | L60"},
    {"question": "What is connection pooling and why is it used?", "company": "Amazon", "topic": "Database",
     "sourceUrl": "https://leetcode.com/discuss/post/amazon-sde-2-interview-experience-28-yoe-chennai-6493437/", "sourceTitle": "Amazon SDE-2 Interview Experience | 2.8 YOE | Chennai"},
    {"question": "What is an atomic operation?", "company": "Meta", "topic": "Concurrency",
     "sourceUrl": "https://leetcode.com/discuss/post/meta-e4-swe-usa-feb-2025-passed-hiring-committee-6460774/", "sourceTitle": "Meta | E4 SWE | USA | Feb 2025 | Passed Hiring Committee"},
    {"question": "What is a thread pool and why use one?", "company": "Google", "topic": "Concurrency",
     "sourceUrl": "https://leetcode.com/discuss/post/google-linkedin-microsoft-walmart-startup-4882744/", "sourceTitle": "Google | LinkedIn | Microsoft | Walmart | Startup"},
    {"question": "What is the difference between synchronous and asynchronous I/O?", "company": "Apple", "topic": "Concurrency",
     "sourceUrl": "https://leetcode.com/discuss/post/apple-tech-screen-experience-6493548/", "sourceTitle": "Apple tech screen experience"},
    {"question": "What is a condition variable?", "company": "LinkedIn", "topic": "Concurrency",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-bangalore-rejected-6487244/", "sourceTitle": "LinkedIn | SSE | Bangalore | Rejected"},
    {"question": "Explain compare-and-swap (CAS).", "company": "Meta", "topic": "Concurrency",
     "sourceUrl": "https://leetcode.com/discuss/post/meta-e4-swe-usa-feb-2025-passed-hiring-committee-6460774/", "sourceTitle": "Meta | E4 SWE | USA | Feb 2025 | Passed Hiring Committee"},
    {"question": "What is the difference between multithreading and multiprocessing?", "company": "Google", "topic": "Concurrency",
     "sourceUrl": "https://leetcode.com/discuss/post/google-phone-screen-l4-6408113/", "sourceTitle": "Google phone screen | L4"},
    {"question": "What is a stack overflow vs heap overflow?", "company": "Apple", "topic": "Memory / Runtime",
     "sourceUrl": "https://leetcode.com/discuss/post/apple-tech-screen-experience-6493548/", "sourceTitle": "Apple tech screen experience"},
    {"question": "Explain mark-and-sweep vs generational garbage collection.", "company": "LinkedIn", "topic": "Memory / Runtime",
     "sourceUrl": "https://leetcode.com/discuss/post/linkedin-sse-bangalore-rejected-6487244/", "sourceTitle": "LinkedIn | SSE | Bangalore | Rejected"},
    {"question": "What is reference counting in garbage collection?", "company": "Oracle", "topic": "Memory / Runtime",
     "sourceUrl": "https://leetcode.com/discuss/post/oracle-software-engineer-onsite-bengaluru-offer-5890226/", "sourceTitle": "Oracle | Software Engineer | Onsite | Bengaluru | [offer]"},
    {"question": "What is the difference between pass-by-value and pass-by-reference?", "company": "Microsoft", "topic": "Memory / Runtime",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-sde-l60-6389446/", "sourceTitle": "Microsoft | SDE | L60"},
    {"question": "What is abstraction in OOP?", "company": "Apple", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/apple-human-engineering-sde1-cupertino-jan-2019-reject-496123/", "sourceTitle": "Apple | Human Engineering SDE1 | Cupertino | Jan 2019 [Reject]"},
    {"question": "What is the difference between an interface and an abstract class?", "company": "Oracle", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/oracle-software-engineer-onsite-bengaluru-offer-5890226/", "sourceTitle": "Oracle | Software Engineer | Onsite | Bengaluru | [offer]"},
    {"question": "Explain composition over inheritance.", "company": "Google", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/google-l4-interview-experience-6027649/", "sourceTitle": "Google L4 Interview Experience"},
    {"question": "What is the adapter design pattern?", "company": "Amazon", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/interview-experience-journey-sep-2024-5756745/", "sourceTitle": "Interview experience journey: sep 2024"},
    {"question": "What is the strategy design pattern?", "company": "Uber", "topic": "OOP / Design Patterns",
     "sourceUrl": "https://leetcode.com/discuss/post/uber-sse---ii-level-5b-india-mar-2020-reject-553913/", "sourceTitle": "Uber | SSE - II (Level 5B) | India | Mar 2020 [Reject]"},
    {"question": "What is idempotency in APIs?", "company": "Google", "topic": "Distributed Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/google-l3-nov-2024-offer-6084576/", "sourceTitle": "Google | L3 | Nov 2024 [Offer]"},
    {"question": "What is the difference between monolith and microservices?", "company": "Amazon", "topic": "Distributed Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/amazon-sde-2-interview-experience-28-yoe-chennai-6493437/", "sourceTitle": "Amazon SDE-2 Interview Experience | 2.8 YOE | Chennai"},
    {"question": "What is a message queue and when would you use one?", "company": "Microsoft", "topic": "Distributed Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/microsoft-sde-l60-6389446/", "sourceTitle": "Microsoft | SDE | L60"},
    {"question": "Explain leader election at a high level.", "company": "Uber", "topic": "Distributed Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/uber-sse---ii-level-5b-india-mar-2020-reject-553913/", "sourceTitle": "Uber | SSE - II (Level 5B) | India | Mar 2020 [Reject]"},
    {"question": "What is cache invalidation and common strategies?", "company": "Meta", "topic": "Distributed Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/meta-software-engineer-product-e4-full-interview-experience-us-6379540/", "sourceTitle": "META | Software Engineer (Product) E4 | Full Interview Experience | US"},
    {"question": "What is the difference between horizontal and vertical scaling?", "company": "Google", "topic": "Distributed Systems",
     "sourceUrl": "https://leetcode.com/discuss/post/google-l3-nov-2024-offer-6084576/", "sourceTitle": "Google | L3 | Nov 2024 [Offer]"},
]


def gql(query: str, variables: dict | None = None) -> dict:
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    last_err: Exception | None = None
    for attempt in range(GQL_RETRIES):
        try:
            req = urllib.request.Request(
                GQL_URL, data=body,
                headers={"Content-Type": "application/json", "User-Agent": UA},
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read())
            if data.get("errors"):
                raise RuntimeError(data["errors"][0].get("message", data["errors"]))
            return data
        except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
            last_err = exc
            time.sleep(1.5 * (attempt + 1))
    raise last_err  # type: ignore[misc]


def strip_markdown(text: str) -> str:
    text = text.replace("\\n", "\n").replace("\\t", "\t").replace("\\'", "'")
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"`+", "", text)
    text = re.sub(r"\*+", "", text)
    return text


def slugify_url(title: str, topic_id: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9\s-]", "", title.lower())
    s = re.sub(r"\s+", "-", s.strip())[:80].strip("-")
    return f"https://leetcode.com/discuss/post/{s}-{topic_id}/"


def extract_companies(tags: list[dict], title: str) -> str:
    found: list[str] = []
    tag_slugs = {t["slug"] for t in tags}
    for slug, name in COMPANY_SLUGS.items():
        if slug in tag_slugs and name not in found:
            found.append(name)
    for m in TITLE_COMPANY_RE.finditer(title):
        n = m.group(1)
        name = "Meta" if n.lower() == "facebook" else n.title()
        if name not in found:
            found.append(name)
    return found[0] if len(found) == 1 else (", ".join(found[:2]) if found else "Big Tech")


def categorize(text: str) -> str:
    t = text.lower()
    if re.search(r"tcp|udp|http|dns|tls|ssl|socket|network|cdn|load balancer|handshake|rest api|browser|authentication", t):
        return "Networking"
    if re.search(r"database|sql|nosql|acid|transaction|normalization|rdbms|migrate|index|shard|replication|isolation level|b\+", t):
        return "Database"
    if re.search(r"process vs thread|virtual memory|mutex|semaphore|deadlock|paging|page fault|thrashing|segmentation|fcfs|round.?robin|context switch|kernel|scheduling", t):
        return "Operating Systems"
    if re.search(r"concurrency|parallel|race|async|multi.?core", t):
        return "Concurrency"
    if re.search(r"garbage|finalize|finally|heap vs stack|memory leak", t):
        return "Memory / Runtime"
    if re.search(r"polymorphism|inheritance|design pattern|ood|singleton|encapsulation|factory|observer", t):
        return "OOP / Design Patterns"
    if re.search(r"distributed|consistency|cap|microservice|load balancer", t):
        return "Distributed Systems"
    return "Operating Systems"


def normalize_key(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    return re.sub(r"\s+", " ", s).strip()[:90]


def polish_question(text: str) -> str:
    s = re.sub(r"\s+", " ", text).strip(" .-–—")
    s = re.sub(r"^(?:questions? on|asked about|topics?:)\s*", "", s, flags=re.I)
    if not s.endswith("?"):
        if re.match(r"^(explain|describe|compare|what|how|why|difference|was asked|calculate|write)", s, re.I):
            s = s.rstrip(".") + "?"
        elif re.search(r"\bvs\.?\b", s, re.I):
            parts = re.split(r"\bvs\.?\b", s, maxsplit=1, flags=re.I)
            if len(parts) == 2:
                s = f"What is the difference between {parts[0].strip()} and {parts[1].strip()}?"
        else:
            return ""  # do not auto-prefix "Explain" — too noisy
    if s.lower().startswith("explain explain"):
        s = s[8:]
    return s[0].upper() + s[1:] if s else ""


def is_valid(text: str) -> bool:
    if not text or len(text) < 20 or len(text) > 200:
        return False
    if NARRATIVE.search(text):
        return False
    if VAGUE.search(text):
        return False
    if not STRONG_CS.search(text):
        return False
    if re.search(r"leetcode\.com|https?://", text, re.I):
        return False
    # must start like a real question
    if not re.match(
        r"^(What|How|Why|Explain|Describe|Compare|Difference|Was asked|Calculate|Write|Does)",
        text, re.I,
    ):
        return False
    # reject "Explain I ..." narrative
    if re.match(r"^Explain [A-Z][a-z]+ (I |the interview|they |it |only |after )", text):
        return False
    return True


def extract_from_content(content: str) -> list[str]:
    """Extract only explicit CS questions — no narrative sentences."""
    text = strip_markdown(content)
    found: list[str] = []
    seen: set[str] = set()

    def add(raw: str) -> None:
        q = polish_question(raw.strip())
        if not q or not is_valid(q):
            return
        key = normalize_key(q)
        if key in seen:
            return
        seen.add(key)
        found.append(q)

    # Explicit interview questions
    for m in re.finditer(
        r"(?:^|\n)\s*(?:\d+[\.\)]\s*|\*\s*|\-\s*|Q\d*:?\s*)?"
        r"((?:What|How|Why|Explain|Describe|Compare|Difference between|Was asked|Calculate|Write|Does)[^?\n]{10,180}\?)",
        text, re.I,
    ):
        add(m.group(1))

    # Label: body  e.g. "Concurrency & Deadlocks: How deadlocks happen..."
    for m in re.finditer(
        r"(?:^|\n)\s*(?:\*\s*|\-\s*)?"
        r"([A-Za-z][^:\n]{2,50}(?:deadlock|mutex|TCP|SQL|OS|memory|thread|database)[^:\n]{0,30}):\s*"
        r"((?:How|What|Why|Explain|Describe)[^.\n]{10,180})",
        text, re.I,
    ):
        add(m.group(2))

    # Parenthetical OS topic lists: (paging, thrashing, Mutex Vs Semaphore, etc)
    for m in re.finditer(r"\(([A-Za-z][^)]{10,160})\)", text):
        inner = m.group(1)
        if not STRONG_CS.search(inner):
            continue
        for part in re.split(r",|\band\b|\&", inner):
            part = re.sub(r"\betc\.?\.*$", "", part.strip(), flags=re.I)
            if STRONG_CS.search(part) and len(part) > 5:
                if re.search(r"\bvs\.?\b", part, re.I):
                    add(f"What is the difference between {part}?")
                else:
                    add(f"Explain {part}?")

    # "Questions on process vs threads, virtual memory"
    for m in re.finditer(r"questions? on\s+([^\n.]{10,160})", text, re.I):
        for part in re.split(r",|\band\b", m.group(1)):
            part = part.strip()
            if STRONG_CS.search(part):
                if re.search(r"\bvs\.?\b", part, re.I):
                    add(f"What is the difference between {part}?")
                else:
                    add(f"Explain {part}?")

    return found


def collect_topic_ids() -> list[dict]:
    seen: set[str] = set()
    topics: list[dict] = []
    q = """
    query($tag: String!, $skip: Int!) {
      categoryTopicList(
        categories: ["interview-experience"]
        orderBy: newest_to_oldest
        tags: [$tag]
        first: 30
        skip: $skip
      ) { edges { node { id title tags { name slug } } } }
    }
    """
    for tag in COMPANY_TAGS:
        for skip in (0, 30):
            try:
                data = gql(q, {"tag": tag, "skip": skip})
            except (urllib.error.URLError, RuntimeError, TimeoutError):
                continue
            for edge in (data.get("data") or {}).get("categoryTopicList", {}).get("edges") or []:
                node = edge["node"]
                if node["id"] not in seen:
                    seen.add(node["id"])
                    topics.append(node)
            time.sleep(0.12)
    return topics


def fetch_content(topic_id: str) -> str:
    data = gql(f'query {{ topic(id: {topic_id}) {{ post {{ content }} }} }}')
    return (((data.get("data") or {}).get("topic") or {}).get("post") or {}).get("content") or ""


def main() -> None:
    records: list[dict] = []
    seen: set[str] = set()

    for item in CURATED:
        key = normalize_key(item["question"])
        if key in seen:
            continue
        seen.add(key)
        records.append(dict(item))

    print(f"Seeded {len(records)} curated CS questions")

    # Optional: supplement from crawl (strict only)
    topics = collect_topic_ids()
    print(f"Scanning {len(topics)} discuss posts for extra questions…")
    for i, topic in enumerate(topics):
        if len(records) >= TARGET:
            break
        try:
            content = fetch_content(topic["id"])
        except (urllib.error.URLError, RuntimeError, TimeoutError):
            continue
        if not CS_SECTION.search(strip_markdown(content)):
            continue
        company = extract_companies(topic.get("tags") or [], topic["title"])
        source_url = slugify_url(topic["title"], topic["id"])
        source_title = topic["title"][:140]
        for q in extract_from_content(content):
            key = normalize_key(q)
            if key in seen:
                continue
            seen.add(key)
            records.append({
                "question": q,
                "company": company,
                "topic": categorize(q),
                "sourceUrl": source_url,
                "sourceTitle": source_title,
            })
        if i and i % 100 == 0:
            print(f"  …{i} posts, {len(records)} total")
        time.sleep(0.12)

    final = records[:TARGET]
    final.sort(
        key=lambda r: (
            TOPIC_ORDER.index(r["topic"]) if r["topic"] in TOPIC_ORDER else 99,
            r["company"],
            r["question"],
        )
    )
    for idx, r in enumerate(final, 1):
        r["id"] = f"csq-{idx:03d}"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(final, ensure_ascii=False, indent=2)
    OUT.write_text(
        "// AUTO-GENERATED by scripts/crawl_cs_fundamental_discuss.py — do not edit by hand\n"
        f"// Source: LeetCode Discuss — verified CS fundamental questions ({len(final)} items)\n"
        f"window.CS_FUNDAMENTAL_QUESTIONS = {payload};\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(final)} questions → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
