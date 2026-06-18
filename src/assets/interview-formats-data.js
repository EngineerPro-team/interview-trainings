/** EngineerPro interview cheatsheet V2 — format tham khảo theo công ty */
window.INTERVIEW_FORMATS = [
  {
    id: "amazon",
    company: "Amazon",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "OA + Coding Medium–Hard, Bar Raiser coding" },
      { slug: "behaviour-interview-course", note: "Leadership Principles & Bar Raiser behavioural" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design (SDE II+)" },
      { slug: "cracking-machine-coding-low-level-design-round", note: "OOD / design nhẹ phone screen" },
      { slug: "mock", note: "Mock virtual onsite đúng format Amazon" },
    ],
    profiles: [
      {
        title: "SDE I & SDE II",
        sections: [
          {
            title: "1. Application & Screening",
            bullets: [
              "Submit Application qua portal hoặc referral.",
              "Recruiter Reach-out: sơ tuyển kinh nghiệm, trao đổi role, level SDE I/SDE II.",
              "Online Assessment (OA): coding trên Hackerrank/Codility — Array, Tree, Graph, DP, time & space complexity.",
            ],
          },
          {
            title: "2. Technical Phone Screens (1–2 vòng)",
            blocks: [
              {
                icon: "🔵",
                title: "Thuật toán & Coding",
                bullets: [
                  "Giải bài trên môi trường chia sẻ màn hình.",
                  "Chủ đề: Array, Strings, Linked List, Stack/Queue, Binary Search, Tree/BST.",
                ],
              },
              {
                icon: "🟢",
                title: "Design nhẹ (SDE II)",
                bullets: ["Cấu trúc class, API design nhỏ, Object-Oriented Design (OOD)."],
              },
            ],
          },
          {
            title: "3. Onsite (Virtual) — 4–5 vòng, ~45–60 phút/vòng",
            blocks: [
              { icon: "🔵", title: "1–2 vòng Coding", bullets: ["DSA, tối ưu giải pháp, discuss trade-off. Mức Medium → Hard (LeetCode)."] },
              { icon: "🟢", title: "1 vòng System Design (thường SDE II+)", bullets: ["High-level design: phân rã service, scale, DB schema, caching."] },
              { icon: "🟡", title: "1 vòng Bar Raiser / Leadership Principles", bullets: ["Tình huống thực tế, teamwork, conflict, thất bại."] },
              { icon: "🟠", title: "1 vòng Behavioural (LP)", bullets: ["14–17 Leadership Principles: Customer Obsession, Ownership, Invent & Simplify, Dive Deep…"] },
            ],
          },
          {
            title: "4. Decision & Offer",
            bullets: [
              "Tổng hợp feedback; Bar Raiser quyết định final.",
              "Level SDE I/II dựa trên performance & kinh nghiệm.",
            ],
          },
        ],
      },
    ],
  },
  {
    id: "google",
    company: "Google",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "2–3 vòng Algorithm Medium–Hard" },
      { slug: "computer-science-fundamental-interview", note: "CS fundamentals & clarify-before-code mindset" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design L4+" },
      { slug: "system-design-interview-level-2", note: "System Design L5 / senior signals" },
      { slug: "mock", note: "Mock Googliness + coding loop" },
    ],
    profiles: [
      {
        title: "SDE I (L3) — New Grad / Entry",
        sections: [
          { title: "1. Application & Recruiter Screen", bullets: ["Nộp CV, recruiter trao đổi kinh nghiệm. Có thể có Online Assessment (Google Coding Test)."] },
          {
            title: "2. Technical Interviews (3–4 vòng)",
            blocks: [
              { icon: "🔵", title: "Algorithm & Coding (2–3 vòng)", bullets: ["Array, String, DP, Graph, Trees, Stack/Queue. LeetCode Easy → Medium, ít Hard."] },
              { icon: "🟢", title: "System design: High level design (có thể không có)", bullets: ["Thiết kế class hoặc HL design service nhỏ."] },
              { icon: "🟡", title: "Googliness & Leadership", bullets: ["Teamwork, learning attitude, communication — không phải list LP như Amazon."] },
            ],
          },
        ],
      },
      {
        title: "SDE II (L4) — Mid-Level",
        sections: [
          { title: "1. Application & Recruiter Call", bullets: ["Trao đổi kỹ kinh nghiệm. Online Coding Test (tùy role)."] },
          {
            title: "2. Technical Interviews (4–5 vòng)",
            blocks: [
              { icon: "🔵", title: "Algorithm & Coding (2–3 vòng)", bullets: ["Medium–Hard DSA."] },
              { icon: "🟢", title: "System Design (1 vòng — có thể thay bằng DSA)", bullets: ["HL design 1 service nhỏ: rate limiter, news feed, search suggestion…"] },
              { icon: "🟡", title: "Googliness (1 vòng)", bullets: ["Conflict, collaboration, growth mindset."] },
            ],
          },
        ],
      },
      {
        title: "SDE III (L5) — Senior",
        sections: [
          { title: "1. Application & Recruiter Screen", bullets: ["Recruiter hỏi kỹ kinh nghiệm thiết kế, mentoring."] },
          {
            title: "2. Technical Interviews (4–6 vòng)",
            blocks: [
              { icon: "🔵", title: "Algorithm & Coding (2 vòng)", bullets: ["Medium–Hard, tối ưu thời gian & không gian."] },
              { icon: "🟢", title: "System Design (1–2 vòng)", bullets: ["End-to-end hệ thống lớn: distributed, scalability, storage, indexing, caching, sharding."] },
              { icon: "🟠", title: "Technical / Project Discussion (1 vòng)", bullets: ["Chi tiết dự án, quyết định kỹ thuật, trade-offs."] },
              { icon: "🟡", title: "Googliness & Leadership (1 vòng)", bullets: ["Teamwork, mentorship, influence."] },
            ],
          },
        ],
      },
    ],
    tips: {
      title: "Điểm chung Google",
      bullets: [
        "Clarify requirements trước khi code hoặc design.",
        "Communication & giải thích trade-offs, tối ưu.",
        "Googliness = teamwork, humility, growth mindset.",
      ],
    },
  },
  {
    id: "grab",
    company: "Grab",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "Coding Medium (G3) → Medium–Hard (G4)" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "High-level design G3 & G4+" },
      { slug: "behaviour-interview-course", note: "Culture fit & teamwork" },
      { slug: "mock", note: "Mock Grab onsite" },
    ],
    profiles: [
      {
        title: "SDE I (G3) — Junior",
        sections: [
          { title: "1. Application & Recruiter Screen", bullets: ["CV hoặc referral; trao đổi background."] },
          { title: "2. Online Assessment (tùy role)", bullets: ["LeetCode style, thường Easy/Medium."] },
          {
            title: "3. Technical Interviews (3–4 vòng)",
            blocks: [
              { icon: "🔵", title: "Algorithm & Coding (2 vòng)", bullets: ["Array, Hashing, Sorting, Stack/Queue, Tree, Graph. Medium trở xuống."] },
              { icon: "🟢", title: "System design: High level design", bullets: ["High-level design — trade-offs, scale, database schema cơ bản."] },
              { icon: "🟡", title: "Culture Fit & Behavioural", bullets: ["Teamwork, xử lý lỗi, nhận feedback."] },
            ],
          },
        ],
      },
      {
        title: "SDE II (G4) — Mid-Level",
        sections: [
          { title: "1. Application & Recruiter Screen", bullets: ["Hỏi kỹ kinh nghiệm tech & domain."] },
          {
            title: "2. Technical Interviews (4–5 vòng)",
            blocks: [
              { icon: "🔵", title: "Algorithm & Coding (2 vòng)", bullets: ["Medium–Hard: Graphs, DP, Sliding Window, Two Pointers, Heap."] },
              { icon: "🟢", title: "System Design (1 vòng)", bullets: ["Chat, URL shortener, Payment API — trade-offs, scale, DB schema."] },
              { icon: "🟠", title: "Project Discussion (1 vòng)", bullets: ["Kiến trúc dự án, debug, tối ưu performance."] },
              { icon: "🟡", title: "Culture Fit & Core Values", bullets: ["Conflict, teamwork, customer-centricity."] },
            ],
          },
        ],
      },
    ],
    tips: {
      title: "Lưu ý phỏng vấn Grab",
      bullets: [
        "Chú trọng teamwork, culture fit, customer-centricity.",
        "Coding thường Medium (dễ hơn FAANG) nhưng cần code sạch, tối ưu.",
        "G4+ cần tư duy kiến trúc và giao tiếp rõ ràng.",
      ],
    },
  },
  {
    id: "meta",
    company: "Meta",
    note: "Từ 2026: có thể có thêm vòng Coding with AI (coding kèm AI tool — format tùy team/role, mang tính tham khảo).",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "Coding Medium–Hard (E3→E5)" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design E4+" },
      { slug: "system-design-interview-level-2", note: "System Design E5 / scale" },
      { slug: "cracking-machine-coding-low-level-design-round", note: "OOD / design mix E3–E4" },
      { slug: "behaviour-interview-course", note: "Meta Values behavioural" },
      { slug: "mock", note: "Mock Meta loop (+ Coding with AI nếu có)" },
    ],
    profiles: [
      {
        title: "E3 (SDE I) — Entry (~0–2 năm)",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Background, sở thích team."] },
          { title: "2. Online Coding Test (nếu có)", bullets: ["1–2 bài Medium, có thể thêm Easy."] },
          {
            title: "3. Phone Screens (1–2 vòng)",
            blocks: [
              { icon: "🔵", title: "Algorithm & Coding", bullets: ["Medium: Array, String, Tree, Stack/Queue. Giao tiếp rõ, tối ưu time/space."] },
              { icon: "🟡", title: "Behavioral Fit", bullets: ["Teamwork, học hỏi, nhận feedback."] },
            ],
          },
          {
            title: "4. Onsite (3–4 vòng)",
            blocks: [
              { icon: "🔵", title: "2 vòng Coding", bullets: ["Medium–Hard: Graph, DP, Binary Search, Backtracking."] },
              { icon: "🤖", title: "Coding with AI (từ 2026 — tùy team)", bullets: ["Vòng mới: giải bài kèm AI assistant — clarify, iterate, explain trade-offs."] },
              { icon: "🟢", title: "System Design nhẹ (có thể có)", bullets: ["Chủ yếu OOD, class design."] },
              { icon: "🟡", title: "Behavioral (Meta Values)", bullets: ["Collaboration, Growth Mindset."] },
            ],
          },
        ],
      },
      {
        title: "E4 (SDE II) — Mid (~2–5 năm)",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Hiểu domain bạn từng làm."] },
          { title: "2. Technical Screens (1–2 vòng)", blocks: [{ icon: "🔵", title: "Algorithm & Coding", bullets: ["Medium–Hard: Graphs, DP, Search, Sliding Window."] }] },
          {
            title: "3. Onsite (5 vòng)",
            blocks: [
              { icon: "🔵", title: "2 vòng Coding", bullets: ["Medium–Hard."] },
              { icon: "🤖", title: "Coding with AI (từ 2026 — tùy team)", bullets: ["Vòng mới: giải bài kèm AI assistant — clarify, iterate, explain trade-offs."] },
              { icon: "🟢", title: "1 vòng System Design", bullets: ["Newsfeed, Messenger…"] },
              { icon: "🟠", title: "1 vòng Behavioral", bullets: ["Conflict, teamwork, ambiguity."] },
              { icon: "🟣", title: "1 vòng Coding/Design mix", bullets: ["Tùy role — có thể thêm OOD."] },
            ],
          },
        ],
      },
      {
        title: "E5 (SDE III) — Senior (~5–8 năm)",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Kinh nghiệm thiết kế và dẫn dắt team."] },
          { title: "2. Technical Screens (1–2 vòng)", blocks: [{ icon: "🔵", title: "Algorithm & Coding", bullets: ["Medium–Hard, Graphs, DP, distributed logic."] }] },
          {
            title: "3. Onsite (4–5 vòng)",
            blocks: [
              { icon: "🔵", title: "2 vòng Coding", bullets: ["Hard — tối ưu time/space."] },
              { icon: "🤖", title: "Coding with AI (từ 2026 — tùy team)", bullets: ["Vòng mới: giải bài kèm AI assistant — clarify, iterate, explain trade-offs."] },
              { icon: "🟢", title: "1–2 vòng System Design", bullets: ["Messenger, distributed cache, newsfeed at scale."] },
              { icon: "🟠", title: "Project Deep-dive (có thể)", bullets: ["Kiến trúc, trade-off, scalability, vận hành."] },
              { icon: "🟡", title: "Behavioral", bullets: ["Impact, leadership, mentoring, giúp team grow."] },
            ],
          },
        ],
      },
    ],
    tips: {
      title: "Meta thường đánh giá cao",
      bullets: [
        "Từ 2026: có thể có vòng Coding with AI — thể hiện cách dùng AI có kiểm soát, vẫn own solution & trade-offs.",
        "Communication: explain trade-offs và reasoning.",
        "Meta Values: Move fast, Focus on impact, Be open, Build social value.",
        "E5+ cần mentoring & driving decisions.",
      ],
    },
  },
  {
    id: "microsoft",
    company: "Microsoft",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "OA + 2–3 vòng Coding Medium–Hard" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design L61+" },
      { slug: "cracking-machine-coding-low-level-design-round", note: "Design/OOD nhẹ L59–L60" },
      { slug: "behaviour-interview-course", note: "Microsoft Values behavioural" },
      { slug: "mock", note: "Mock Microsoft onsite" },
    ],
    profiles: [
      {
        title: "SDE I (L59–L60) — Entry/Mid (~0–2 năm)",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Background, sở thích."] },
          { title: "2. Online Assessment", bullets: ["LeetCode-style Easy–Medium: Array, String, Binary Search, Stack/Queue."] },
          {
            title: "3. Phone Screens (1–2 vòng)",
            blocks: [{ icon: "🔵", title: "Algorithm & Coding", bullets: ["Medium — Strings, Two Pointers, Trees, Graphs, LinkedList, DP. Phân tích time/space."] }],
          },
          {
            title: "4. Onsite (3–4 vòng)",
            blocks: [
              { icon: "🔵", title: "2 vòng Coding & Algorithm", bullets: ["Medium — Arrays, Graphs, Stacks, Heaps, Sliding Window."] },
              { icon: "🟢", title: "1 vòng Design/OOD nhẹ", bullets: ["Thiết kế class, logic nghiệp vụ đơn giản."] },
              { icon: "🟡", title: "1 vòng Behavioral", bullets: ["Teamwork, conflict, growth mindset."] },
            ],
          },
        ],
      },
      {
        title: "SDE II (L61–L62) — Mid (~2–5 năm)",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Kinh nghiệm, dự án chi tiết."] },
          {
            title: "2. Technical Screens (1–2 vòng)",
            blocks: [{ icon: "🔵", title: "Algorithm & Coding", bullets: ["Medium–Hard: Graph, DP, Recursion, Backtracking, Priority Queue, Trie. Edge cases & tối ưu."] }],
          },
          {
            title: "3. Onsite (4–5 vòng)",
            blocks: [
              { icon: "🔵", title: "2–3 vòng Coding", bullets: ["Medium–Hard trên Trees, Graphs, DP, Sorting, Searching."] },
              { icon: "🟢", title: "1 vòng System Design", bullets: ["Notification, file sharing, rate limiter…"] },
              { icon: "🟠", title: "1 vòng Behavioral", bullets: ["Microsoft Values — conflict, hợp tác, phát triển bản thân & team."] },
            ],
          },
        ],
      },
    ],
  },
  {
    id: "axon",
    company: "Axon",
    note: "Từ 2026: có thể có thêm vòng Coding with AI (coding kèm AI tool — format tùy team/role, mang tính tham khảo).",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "Phone screen + Coding rounds" },
      { slug: "computer-science-fundamental-interview", note: "Vòng CS fundamentals (rất quan trọng)" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design SDE III" },
      { slug: "behaviour-interview-course", note: "Behavioural round" },
      { slug: "mock", note: "Mock Axon (+ Coding with AI nếu có)" },
    ],
    profiles: [
      {
        title: "SDE I",
        sections: [
          {
            title: "1. Phone Screen (1 vòng)",
            blocks: [
              { icon: "🔵", title: "Coding (DSA)", bullets: [] },
              { icon: "🧠", title: "CS Fundamentals", bullets: ["OS, Network, DB…"] },
            ],
          },
          {
            title: "2. Onsite (4–5 vòng, tùy team)",
            bullets: [
              "1. Coding (có thể kèm CS)",
              "2. Coding (có thể kèm CS)",
              "3. Coding with AI (từ 2026 — tùy team)",
              "4. Behavioral (teamwork, tình huống)",
              "5. Computer Science (CS fundamentals sâu hơn)",
            ],
          },
        ],
      },
      {
        title: "SDE II",
        sections: [
          {
            title: "1. Phone Screen (1 vòng)",
            blocks: [
              { icon: "🔵", title: "Coding (DSA)", bullets: [] },
              { icon: "🧠", title: "CS Fundamentals", bullets: ["OS, Network, DB…"] },
            ],
          },
          {
            title: "2. Onsite (4–5 vòng, tùy team)",
            bullets: [
              "1. Coding (có thể kèm CS)",
              "2. Coding (có thể kèm CS)",
              "3. Coding with AI (từ 2026 — tùy team)",
              "4. Behavioral (teamwork, tình huống)",
              "5. Computer Science (CS fundamentals sâu hơn)",
            ],
          },
        ],
      },
      {
        title: "SDE III (Senior)",
        sections: [
          {
            title: "1. Phone Screen",
            blocks: [
              { icon: "🔵", title: "Coding (DSA)", bullets: [] },
              { icon: "🧠", title: "CS Fundamentals", bullets: [] },
            ],
          },
          {
            title: "2. Onsite (4–5 vòng, tùy team)",
            bullets: [
              "1. Coding",
              "2. System Design (thay vòng Coding thứ 2 của SDE I/II)",
              "3. Coding with AI (từ 2026 — tùy team)",
              "4. Behavioral",
              "5. Computer Science",
            ],
          },
        ],
      },
    ],
    tips: {
      title: "Tóm lại Axon",
      bullets: [
        "SDE I & II: 2 Coding + 1 CS + 1 Behavioral (+ Coding with AI từ 2026, tùy team).",
        "SDE III: 1 Coding + 1 System Design + 1 CS + 1 Behavioral (+ Coding with AI từ 2026, tùy team).",
        "Vòng Coding with AI: giải bài kèm AI — vẫn cần explain approach, trade-offs, và verify output.",
        "Onsite thường 4 vòng (trước 2026); có thể thêm vòng AI → 5 vòng.",
      ],
    },
  },
  {
    id: "shopee",
    company: "Shopee",
    note: "Mỗi team có thể có process khác nhau — chỉ nên tham khảo.",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "2 vòng Coding Medium–Hard" },
      { slug: "computer-science-fundamental-interview", note: "CS fundamentals phone screen" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design Senior SE" },
      { slug: "cracking-machine-coding-low-level-design-round", note: "OOD / design nhẹ SE" },
      { slug: "behaviour-interview-course", note: "Behavioural & leadership" },
      { slug: "mock", note: "Mock Shopee onsite" },
    ],
    profiles: [
      {
        title: "Software Engineer (SE) — Entry/Mid",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Background, tech stack."] },
          { title: "2. Online Coding Test (có thể có)", bullets: ["1–2 bài Medium."] },
          { title: "3. Phone Screen (1 vòng)", bullets: ["Coding (Array, String, Two Pointers…); CS fundamentals sơ bộ."] },
          {
            title: "4. Onsite (3–4 vòng)",
            bullets: [
              "Algorithm & Coding 1 (Medium)",
              "Algorithm & Coding 2 (Medium)",
              "Behavioral Fit (teamwork, conflict, ownership)",
              "System Design nhẹ / OOD (class, kiến trúc nhỏ)",
            ],
          },
        ],
      },
      {
        title: "Senior Software Engineer (~4–7 năm)",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Background, dự án, kinh nghiệm technical."] },
          { title: "2. Online Test (có thể có)", bullets: ["Medium–Hard."] },
          {
            title: "3. Technical Screens (1–2 vòng)",
            bullets: ["Coding Medium–Hard (Graphs, DP, Backtracking); System Design nhẹ hoặc OOD."],
          },
          {
            title: "4. Onsite (4–5 vòng)",
            bullets: [
              "2 vòng Coding Medium–Hard (edge case, tối ưu)",
              "System Design end-to-end (chat, notification, order processing…)",
              "Behavioral — leadership, mentoring, giao tiếp team",
              "Project Deep-dive (tùy role) — troubleshooting, optimization",
            ],
          },
        ],
      },
    ],
    tips: {
      title: "Shopee thường đánh giá cao",
      bullets: ["Code sạch, tối ưu.", "Thiết kế hệ thống (Senior).", "Giao tiếp & collaboration."],
    },
  },
  {
    id: "nab",
    company: "NAB",
    tag: "Backend",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "Coding Medium (Codility)" },
      { slug: "computer-science-fundamental-interview", note: "CS + Java core nếu role Java-heavy" },
      { slug: "khoa-hoc-backend-java", note: "Backend Java stack" },
      { slug: "system-design-interview-level-2", note: "System Design Senior++" },
      { slug: "behaviour-interview-course", note: "HM behaviour + experience deep dive" },
      { slug: "mock", note: "Mock NAB backend loop" },
    ],
    profiles: [
      {
        title: "Backend Engineer",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Background, dự án, kinh nghiệm technical."] },
          { title: "2. Online Test (có thể có — Codility)", bullets: ["Coding Medium–Hard."] },
          {
            title: "3. Technical Screens (2–3 vòng)",
            bullets: [
              "Coding (Medium) + CS fundamental (Java core nếu role nặng Java).",
              "System Design — chỉ Senior++.",
              "Round cuối với HM: behavior + past experience deep dive.",
            ],
          },
        ],
      },
    ],
  },
  {
    id: "tiktok",
    company: "TikTok",
    tag: "Backend",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "Coding Medium–Hard" },
      { slug: "computer-science-fundamental-interview", note: "CS fundamental rounds" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design Junior++" },
      { slug: "cracking-machine-coding-low-level-design-round", note: "LLD / machine coding (phổ biến TikTok)" },
      { slug: "behaviour-interview-course", note: "HM behaviour round" },
      { slug: "mock", note: "Mock TikTok backend loop" },
    ],
    profiles: [
      {
        title: "Backend Engineer",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Background, dự án, kinh nghiệm."] },
          { title: "2. Online Test", bullets: ["Hackerrank — thường intern/new grad; Medium–Hard hoặc CS fundamental."] },
          {
            title: "3. Technical Screens (4–5 vòng)",
            bullets: [
              "Coding (Medium–Hard) + CS fundamental.",
              "System Design — Junior++.",
              "Round cuối HM: behavior + past experience deep dive.",
            ],
          },
        ],
      },
    ],
  },
  {
    id: "nvidia",
    company: "Nvidia",
    tag: "Backend / System Engineer",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "Coding Medium–Hard" },
      { slug: "computer-science-fundamental-interview", note: "CS fundamentals" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design" },
      { slug: "behaviour-interview-course", note: "HM behaviour + experience" },
      { slug: "mock", note: "Mock Nvidia loop (tùy team)" },
    ],
    profiles: [
      {
        title: "Backend — System Engineer",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Background, dự án, kinh nghiệm."] },
          {
            title: "2. Technical Screens (4–5 vòng, tùy team)",
            bullets: [
              "Coding (Medium–Hard) + CS fundamental.",
              "System Design.",
              "Round cuối HM: behavior + past experience deep dive.",
            ],
          },
        ],
      },
    ],
  },
  {
    id: "anz-hcl",
    company: "ANZ × HCL",
    tag: "Backend",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "2 vòng Coding Medium–Hard" },
      { slug: "computer-science-fundamental-interview", note: "CS fundamental mỗi round" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design Mid++" },
      { slug: "behaviour-interview-course", note: "Behaviour lồng trong các round" },
      { slug: "mock", note: "Mock ANZ×HCL loop" },
    ],
    profiles: [
      {
        title: "Backend Engineer",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Background, dự án, kinh nghiệm."] },
          {
            title: "2. Technical Screens (3 vòng, tùy team)",
            bullets: [
              "Coding (Medium–Hard) + CS fundamental — 2 rounds.",
              "System Design: Mid++ mới có; junior có thể thay bằng thêm 1 round coding.",
              "Các round đều có behavior.",
            ],
          },
        ],
      },
    ],
  },
  {
    id: "employment-hero",
    company: "Employment Hero",
    tag: "Backend",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "Codility + tech coding rounds" },
      { slug: "computer-science-fundamental-interview", note: "2 rounds CS fundamental" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design Mid/Senior" },
      { slug: "behaviour-interview-course", note: "Behaviour round đầu tiên" },
      { slug: "mock", note: "Mock Employment Hero loop" },
    ],
    profiles: [
      {
        title: "Backend Engineer",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Background, dự án, kinh nghiệm."] },
          { title: "2. Online Test (Codility)", bullets: ["Medium + Hard."] },
          {
            title: "3. Technical Screens (3 vòng, tùy team)",
            bullets: [
              "Round đầu: thường behavior trước, rồi technical.",
              "Tech: ~2 rounds CS fundamental + Coding (Medium–Hard).",
              "System Design: Senior chắc chắn có; Mid có thể có.",
            ],
          },
        ],
      },
    ],
  },
  {
    id: "worldquant",
    company: "Worldquant",
    tag: "Backend · Python · Data Engineer",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "DSA Hard — trọng tâm" },
      { slug: "computer-science-fundamental-interview", note: "CS fundamental rất sâu" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design Junior/Senior" },
      { slug: "behaviour-interview-course", note: "HM behaviour (+ tech có thể)" },
      { slug: "mock", note: "Mock Worldquant loop" },
    ],
    profiles: [
      {
        title: "Backend / Data Engineer (Python)",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Background, dự án, kinh nghiệm."] },
          { title: "2. Online Test (Hackerrank)", bullets: ["Medium + Hard (có thể không có tùy role)."] },
          {
            title: "3. Technical Screens (4–5 vòng, tùy team)",
            bullets: [
              "CS fundamental & DSA rất sâu (Hard).",
              "System Design có thể có cho Junior; WQ không có mid level; Senior chắc chắn có SD.",
              "Behavior với HM (có thể hỏi tech & past experience).",
              "Có thể hỏi thêm Python/C++ tùy role.",
            ],
          },
        ],
      },
    ],
  },
  {
    id: "anduin",
    company: "Anduin Transaction",
    tag: "SWE",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "DSA Hard — code đúng & tối ưu (CP-style)" },
      { slug: "computer-science-fundamental-interview", note: "CS fundamental rất sâu" },
      { slug: "system-design-interview-level-2", note: "System Design Senior" },
      { slug: "behaviour-interview-course", note: "HM behaviour" },
      { slug: "mock", note: "Mock Anduin loop" },
    ],
    profiles: [
      {
        title: "Software Engineer",
        sections: [
          { title: "1. Recruiter Screen", bullets: ["Background, dự án, kinh nghiệm."] },
          { title: "2. Online Test", bullets: ["Medium + Hard (có thể không có tùy role)."] },
          {
            title: "3. Technical Screens (4–5 vòng, tùy team)",
            bullets: [
              "CS fundamental & DSA rất sâu (Hard).",
              "Interviewer thường có background competitive programming — code đúng & tối ưu.",
              "Senior có System Design round.",
              "Behavior với Hiring Manager.",
            ],
          },
        ],
      },
    ],
  },
  {
    id: "sap",
    company: "SAP",
    tag: "SWE · Enterprise / ERP",
    note: "SAP đề cao hiểu biết kỹ thuật sâu + khả năng chuyển yêu cầu nghiệp vụ (ERP) phức tạp thành phần mềm scalable; nhấn structured thinking & communication rõ ràng.",
    recommendations: [
      { slug: "khoa-hoc-dsa", note: "Coding Screen (Medium) + Onsite Coding (Hard), debugging, clean code" },
      { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design: distributed, scale ERP, API idempotency" },
      { slug: "behaviour-interview-course", note: "Behavioral / Leadership: ownership, influence, conflict" },
      { slug: "computer-science-fundamental-interview", note: "Nền tảng CS vững cho các vòng technical" },
      { slug: "mock", note: "Mock full loop SAP (5 vòng)" },
    ],
    profiles: [
      {
        title: "Software Engineer",
        sections: [
          {
            title: "1. Recruiter Screen",
            bullets: [
              "Motivation, mức độ phù hợp role, logistics.",
              "Hiểu vị thế SAP trong thị trường SaaS/ERP — vì sao chọn SAP (thiếu context kinh doanh là lý do fail phổ biến).",
            ],
          },
          {
            title: "2. Coding Screen",
            blocks: [
              {
                icon: "🔵",
                title: "Algorithm & Coding",
                bullets: [
                  "Bài LeetCode-medium dưới áp lực thời gian.",
                  "Array, String, Hash, Tree; đôi khi data structure theo ngữ cảnh SaaS (vd đếm unique user theo cửa sổ thời gian).",
                ],
              },
            ],
          },
          {
            title: "3. System Design",
            blocks: [
              {
                icon: "🟢",
                title: "Distributed systems & trade-offs",
                bullets: [
                  "Thiết kế dưới ràng buộc scale; phân rã service, DB schema, caching, trade-offs.",
                  "Ngữ cảnh ERP: API upload file cấu hình lớn (reliability, idempotency, user feedback); scale dashboard analytics real-time hàng triệu event/phút.",
                ],
              },
            ],
          },
          {
            title: "4. Onsite Coding",
            blocks: [
              {
                icon: "🟠",
                title: "Coding sâu + Debugging",
                bullets: [
                  "LeetCode-hard, xử lý edge case, độ rõ của code.",
                  "Debug đoạn code backend lỗi (vd 500 error) — đọc hiểu & sửa.",
                  "Đặt tên biến rõ + comment hợp lý — code khó đọc là lý do fail phổ biến.",
                ],
              },
            ],
          },
          {
            title: "5. Behavioral / Leadership",
            bullets: [
              "Ownership: tự cầm trịch một vấn đề từ phát hiện đến giải quyết, kể cả khi ngoài phạm vi trách nhiệm.",
              "Influence: thuyết phục senior stakeholder / cross-functional khi ban đầu họ không đồng ý — nêu rõ chiến lược ảnh hưởng (đừng quy công cho riêng 'ý tưởng').",
              "Conflict resolution: xử lý xung đột trong dự án và kết quả đạt được.",
            ],
          },
        ],
      },
    ],
    tips: {
      title: "Điểm chung SAP",
      bullets: [
        "Hiểu vị thế SAP trong thị trường SaaS/ERP — tránh fail vì thiếu context kinh doanh.",
        "Clean code: đặt tên biến rõ + comment hợp lý.",
        "Behavioral nêu ví dụ cụ thể về influence & ownership, đừng nói chung chung.",
      ],
    },
  },
];
