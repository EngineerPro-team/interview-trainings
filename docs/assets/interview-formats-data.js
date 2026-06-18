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
    en: {
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "OA + Coding Medium–Hard, Bar Raiser coding" },
        { slug: "behaviour-interview-course", note: "Leadership Principles & Bar Raiser behavioural" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design (SDE II+)" },
        { slug: "cracking-machine-coding-low-level-design-round", note: "OOD / light design phone screen" },
        { slug: "mock", note: "Mock virtual onsite in Amazon's exact format" },
      ],
      profiles: [
        {
          title: "SDE I & SDE II",
          sections: [
            {
              title: "1. Application & Screening",
              bullets: [
                "Submit application via portal or referral.",
                "Recruiter Reach-out: initial experience screen, discuss role and level (SDE I/SDE II).",
                "Online Assessment (OA): coding on Hackerrank/Codility — Array, Tree, Graph, DP, time & space complexity.",
              ],
            },
            {
              title: "2. Technical Phone Screens (1–2 rounds)",
              blocks: [
                {
                  icon: "🔵",
                  title: "Algorithms & Coding",
                  bullets: [
                    "Solve problems in a shared-screen environment.",
                    "Topics: Array, Strings, Linked List, Stack/Queue, Binary Search, Tree/BST.",
                  ],
                },
                {
                  icon: "🟢",
                  title: "Light design (SDE II)",
                  bullets: ["Class structure, small API design, Object-Oriented Design (OOD)."],
                },
              ],
            },
            {
              title: "3. Onsite (Virtual) — 4–5 rounds, ~45–60 min/round",
              blocks: [
                { icon: "🔵", title: "1–2 Coding rounds", bullets: ["DSA, optimize the solution, discuss trade-offs. Medium → Hard (LeetCode)."] },
                { icon: "🟢", title: "1 System Design round (typically SDE II+)", bullets: ["High-level design: service decomposition, scale, DB schema, caching."] },
                { icon: "🟡", title: "1 Bar Raiser / Leadership Principles round", bullets: ["Real-world situations, teamwork, conflict, failure."] },
                { icon: "🟠", title: "1 Behavioural round (LP)", bullets: ["14–17 Leadership Principles: Customer Obsession, Ownership, Invent & Simplify, Dive Deep…"] },
              ],
            },
            {
              title: "4. Decision & Offer",
              bullets: [
                "Consolidate feedback; the Bar Raiser makes the final decision.",
                "Level SDE I/II based on performance & experience.",
              ],
            },
          ],
        },
      ],
    },
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
    en: {
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "2–3 Algorithm rounds Medium–Hard" },
        { slug: "computer-science-fundamental-interview", note: "CS fundamentals & clarify-before-code mindset" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design L4+" },
        { slug: "system-design-interview-level-2", note: "System Design L5 / senior signals" },
        { slug: "mock", note: "Mock Googliness + coding loop" },
      ],
      profiles: [
        {
          title: "SDE I (L3) — New Grad / Entry",
          sections: [
            { title: "1. Application & Recruiter Screen", bullets: ["Submit CV; recruiter discusses your experience. May include an Online Assessment (Google Coding Test)."] },
            {
              title: "2. Technical Interviews (3–4 rounds)",
              blocks: [
                { icon: "🔵", title: "Algorithm & Coding (2–3 rounds)", bullets: ["Array, String, DP, Graph, Trees, Stack/Queue. LeetCode Easy → Medium, few Hard."] },
                { icon: "🟢", title: "System design: high-level design (may not be present)", bullets: ["Class design or high-level design of a small service."] },
                { icon: "🟡", title: "Googliness & Leadership", bullets: ["Teamwork, learning attitude, communication — not an LP list like Amazon."] },
              ],
            },
          ],
        },
        {
          title: "SDE II (L4) — Mid-Level",
          sections: [
            { title: "1. Application & Recruiter Call", bullets: ["In-depth experience discussion. Online Coding Test (varies by role)."] },
            {
              title: "2. Technical Interviews (4–5 rounds)",
              blocks: [
                { icon: "🔵", title: "Algorithm & Coding (2–3 rounds)", bullets: ["Medium–Hard DSA."] },
                { icon: "🟢", title: "System Design (1 round — may be replaced by DSA)", bullets: ["High-level design of one small service: rate limiter, news feed, search suggestion…"] },
                { icon: "🟡", title: "Googliness (1 round)", bullets: ["Conflict, collaboration, growth mindset."] },
              ],
            },
          ],
        },
        {
          title: "SDE III (L5) — Senior",
          sections: [
            { title: "1. Application & Recruiter Screen", bullets: ["Recruiter probes your design and mentoring experience."] },
            {
              title: "2. Technical Interviews (4–6 rounds)",
              blocks: [
                { icon: "🔵", title: "Algorithm & Coding (2 rounds)", bullets: ["Medium–Hard, optimize time & space."] },
                { icon: "🟢", title: "System Design (1–2 rounds)", bullets: ["End-to-end large systems: distributed, scalability, storage, indexing, caching, sharding."] },
                { icon: "🟠", title: "Technical / Project Discussion (1 round)", bullets: ["Project details, technical decisions, trade-offs."] },
                { icon: "🟡", title: "Googliness & Leadership (1 round)", bullets: ["Teamwork, mentorship, influence."] },
              ],
            },
          ],
        },
      ],
      tips: {
        title: "Google in a nutshell",
        bullets: [
          "Clarify requirements before coding or designing.",
          "Communication & explaining trade-offs and optimizations.",
          "Googliness = teamwork, humility, growth mindset.",
        ],
      },
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
    en: {
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
            { title: "1. Application & Recruiter Screen", bullets: ["CV or referral; discuss your background."] },
            { title: "2. Online Assessment (varies by role)", bullets: ["LeetCode style, typically Easy/Medium."] },
            {
              title: "3. Technical Interviews (3–4 rounds)",
              blocks: [
                { icon: "🔵", title: "Algorithm & Coding (2 rounds)", bullets: ["Array, Hashing, Sorting, Stack/Queue, Tree, Graph. Medium or below."] },
                { icon: "🟢", title: "System design: high-level design", bullets: ["High-level design — trade-offs, scale, basic database schema."] },
                { icon: "🟡", title: "Culture Fit & Behavioural", bullets: ["Teamwork, handling mistakes, receiving feedback."] },
              ],
            },
          ],
        },
        {
          title: "SDE II (G4) — Mid-Level",
          sections: [
            { title: "1. Application & Recruiter Screen", bullets: ["In-depth questions on tech & domain experience."] },
            {
              title: "2. Technical Interviews (4–5 rounds)",
              blocks: [
                { icon: "🔵", title: "Algorithm & Coding (2 rounds)", bullets: ["Medium–Hard: Graphs, DP, Sliding Window, Two Pointers, Heap."] },
                { icon: "🟢", title: "System Design (1 round)", bullets: ["Chat, URL shortener, Payment API — trade-offs, scale, DB schema."] },
                { icon: "🟠", title: "Project Discussion (1 round)", bullets: ["Project architecture, debugging, performance optimization."] },
                { icon: "🟡", title: "Culture Fit & Core Values", bullets: ["Conflict, teamwork, customer-centricity."] },
              ],
            },
          ],
        },
      ],
      tips: {
        title: "Notes for Grab interviews",
        bullets: [
          "Emphasis on teamwork, culture fit, customer-centricity.",
          "Coding is typically Medium (easier than FAANG) but requires clean, optimized code.",
          "G4+ requires architectural thinking and clear communication.",
        ],
      },
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
    en: {
      note: "From 2026: may include an additional Coding with AI round (coding with an AI tool — format varies by team/role, for reference).",
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "Coding Medium–Hard (E3→E5)" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design E4+" },
        { slug: "system-design-interview-level-2", note: "System Design E5 / scale" },
        { slug: "cracking-machine-coding-low-level-design-round", note: "OOD / design mix E3–E4" },
        { slug: "behaviour-interview-course", note: "Meta Values behavioural" },
        { slug: "mock", note: "Mock Meta loop (+ Coding with AI if applicable)" },
      ],
      profiles: [
        {
          title: "E3 (SDE I) — Entry (~0–2 years)",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Background, team preferences."] },
            { title: "2. Online Coding Test (if applicable)", bullets: ["1–2 Medium problems, possibly an Easy one too."] },
            {
              title: "3. Phone Screens (1–2 rounds)",
              blocks: [
                { icon: "🔵", title: "Algorithm & Coding", bullets: ["Medium: Array, String, Tree, Stack/Queue. Clear communication, optimize time/space."] },
                { icon: "🟡", title: "Behavioral Fit", bullets: ["Teamwork, learning, receiving feedback."] },
              ],
            },
            {
              title: "4. Onsite (3–4 rounds)",
              blocks: [
                { icon: "🔵", title: "2 Coding rounds", bullets: ["Medium–Hard: Graph, DP, Binary Search, Backtracking."] },
                { icon: "🤖", title: "Coding with AI (from 2026 — varies by team)", bullets: ["New round: solve a problem with an AI assistant — clarify, iterate, explain trade-offs."] },
                { icon: "🟢", title: "Light System Design (may be present)", bullets: ["Mostly OOD, class design."] },
                { icon: "🟡", title: "Behavioral (Meta Values)", bullets: ["Collaboration, Growth Mindset."] },
              ],
            },
          ],
        },
        {
          title: "E4 (SDE II) — Mid (~2–5 years)",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Understand the domains you've worked in."] },
            { title: "2. Technical Screens (1–2 rounds)", blocks: [{ icon: "🔵", title: "Algorithm & Coding", bullets: ["Medium–Hard: Graphs, DP, Search, Sliding Window."] }] },
            {
              title: "3. Onsite (5 rounds)",
              blocks: [
                { icon: "🔵", title: "2 Coding rounds", bullets: ["Medium–Hard."] },
                { icon: "🤖", title: "Coding with AI (from 2026 — varies by team)", bullets: ["New round: solve a problem with an AI assistant — clarify, iterate, explain trade-offs."] },
                { icon: "🟢", title: "1 System Design round", bullets: ["Newsfeed, Messenger…"] },
                { icon: "🟠", title: "1 Behavioral round", bullets: ["Conflict, teamwork, ambiguity."] },
                { icon: "🟣", title: "1 Coding/Design mix round", bullets: ["Varies by role — may add OOD."] },
              ],
            },
          ],
        },
        {
          title: "E5 (SDE III) — Senior (~5–8 years)",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Design experience and leading a team."] },
            { title: "2. Technical Screens (1–2 rounds)", blocks: [{ icon: "🔵", title: "Algorithm & Coding", bullets: ["Medium–Hard, Graphs, DP, distributed logic."] }] },
            {
              title: "3. Onsite (4–5 rounds)",
              blocks: [
                { icon: "🔵", title: "2 Coding rounds", bullets: ["Hard — optimize time/space."] },
                { icon: "🤖", title: "Coding with AI (from 2026 — varies by team)", bullets: ["New round: solve a problem with an AI assistant — clarify, iterate, explain trade-offs."] },
                { icon: "🟢", title: "1–2 System Design rounds", bullets: ["Messenger, distributed cache, newsfeed at scale."] },
                { icon: "🟠", title: "Project Deep-dive (possible)", bullets: ["Architecture, trade-offs, scalability, operations."] },
                { icon: "🟡", title: "Behavioral", bullets: ["Impact, leadership, mentoring, helping the team grow."] },
              ],
            },
          ],
        },
      ],
      tips: {
        title: "Meta typically values",
        bullets: [
          "From 2026: may include a Coding with AI round — show controlled, accountable use of AI while still owning the solution & trade-offs.",
          "Communication: explain trade-offs and reasoning.",
          "Meta Values: Move fast, Focus on impact, Be open, Build social value.",
          "E5+ requires mentoring & driving decisions.",
        ],
      },
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
    en: {
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "OA + 2–3 Coding rounds Medium–Hard" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design L61+" },
        { slug: "cracking-machine-coding-low-level-design-round", note: "Light Design/OOD L59–L60" },
        { slug: "behaviour-interview-course", note: "Microsoft Values behavioural" },
        { slug: "mock", note: "Mock Microsoft onsite" },
      ],
      profiles: [
        {
          title: "SDE I (L59–L60) — Entry/Mid (~0–2 years)",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Background, preferences."] },
            { title: "2. Online Assessment", bullets: ["LeetCode-style Easy–Medium: Array, String, Binary Search, Stack/Queue."] },
            {
              title: "3. Phone Screens (1–2 rounds)",
              blocks: [{ icon: "🔵", title: "Algorithm & Coding", bullets: ["Medium — Strings, Two Pointers, Trees, Graphs, LinkedList, DP. Analyze time/space."] }],
            },
            {
              title: "4. Onsite (3–4 rounds)",
              blocks: [
                { icon: "🔵", title: "2 Coding & Algorithm rounds", bullets: ["Medium — Arrays, Graphs, Stacks, Heaps, Sliding Window."] },
                { icon: "🟢", title: "1 Light Design/OOD round", bullets: ["Class design, simple business logic."] },
                { icon: "🟡", title: "1 Behavioral round", bullets: ["Teamwork, conflict, growth mindset."] },
              ],
            },
          ],
        },
        {
          title: "SDE II (L61–L62) — Mid (~2–5 years)",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Experience, detailed projects."] },
            {
              title: "2. Technical Screens (1–2 rounds)",
              blocks: [{ icon: "🔵", title: "Algorithm & Coding", bullets: ["Medium–Hard: Graph, DP, Recursion, Backtracking, Priority Queue, Trie. Edge cases & optimization."] }],
            },
            {
              title: "3. Onsite (4–5 rounds)",
              blocks: [
                { icon: "🔵", title: "2–3 Coding rounds", bullets: ["Medium–Hard on Trees, Graphs, DP, Sorting, Searching."] },
                { icon: "🟢", title: "1 System Design round", bullets: ["Notification, file sharing, rate limiter…"] },
                { icon: "🟠", title: "1 Behavioral round", bullets: ["Microsoft Values — conflict, collaboration, growing yourself & the team."] },
              ],
            },
          ],
        },
      ],
    },
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
    en: {
      note: "From 2026: may include an additional Coding with AI round (coding with an AI tool — format varies by team/role, for reference).",
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "Phone screen + Coding rounds" },
        { slug: "computer-science-fundamental-interview", note: "CS fundamentals round (very important)" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design SDE III" },
        { slug: "behaviour-interview-course", note: "Behavioural round" },
        { slug: "mock", note: "Mock Axon (+ Coding with AI if applicable)" },
      ],
      profiles: [
        {
          title: "SDE I",
          sections: [
            {
              title: "1. Phone Screen (1 round)",
              blocks: [
                { icon: "🔵", title: "Coding (DSA)", bullets: [] },
                { icon: "🧠", title: "CS Fundamentals", bullets: ["OS, Network, DB…"] },
              ],
            },
            {
              title: "2. Onsite (4–5 rounds, varies by team)",
              bullets: [
                "1. Coding (may include CS)",
                "2. Coding (may include CS)",
                "3. Coding with AI (from 2026 — varies by team)",
                "4. Behavioral (teamwork, scenarios)",
                "5. Computer Science (deeper CS fundamentals)",
              ],
            },
          ],
        },
        {
          title: "SDE II",
          sections: [
            {
              title: "1. Phone Screen (1 round)",
              blocks: [
                { icon: "🔵", title: "Coding (DSA)", bullets: [] },
                { icon: "🧠", title: "CS Fundamentals", bullets: ["OS, Network, DB…"] },
              ],
            },
            {
              title: "2. Onsite (4–5 rounds, varies by team)",
              bullets: [
                "1. Coding (may include CS)",
                "2. Coding (may include CS)",
                "3. Coding with AI (from 2026 — varies by team)",
                "4. Behavioral (teamwork, scenarios)",
                "5. Computer Science (deeper CS fundamentals)",
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
              title: "2. Onsite (4–5 rounds, varies by team)",
              bullets: [
                "1. Coding",
                "2. System Design (replaces the second Coding round of SDE I/II)",
                "3. Coding with AI (from 2026 — varies by team)",
                "4. Behavioral",
                "5. Computer Science",
              ],
            },
          ],
        },
      ],
      tips: {
        title: "Axon in a nutshell",
        bullets: [
          "SDE I & II: 2 Coding + 1 CS + 1 Behavioral (+ Coding with AI from 2026, varies by team).",
          "SDE III: 1 Coding + 1 System Design + 1 CS + 1 Behavioral (+ Coding with AI from 2026, varies by team).",
          "Coding with AI round: solve with AI — you still need to explain the approach, trade-offs, and verify the output.",
          "Onsite is typically 4 rounds (before 2026); the AI round may be added → 5 rounds.",
        ],
      },
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
    en: {
      note: "Each team may have a different process — for reference only.",
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "2 Coding rounds Medium–Hard" },
        { slug: "computer-science-fundamental-interview", note: "CS fundamentals phone screen" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design Senior SE" },
        { slug: "cracking-machine-coding-low-level-design-round", note: "OOD / light design SE" },
        { slug: "behaviour-interview-course", note: "Behavioural & leadership" },
        { slug: "mock", note: "Mock Shopee onsite" },
      ],
      profiles: [
        {
          title: "Software Engineer (SE) — Entry/Mid",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Background, tech stack."] },
            { title: "2. Online Coding Test (may be present)", bullets: ["1–2 Medium problems."] },
            { title: "3. Phone Screen (1 round)", bullets: ["Coding (Array, String, Two Pointers…); preliminary CS fundamentals."] },
            {
              title: "4. Onsite (3–4 rounds)",
              bullets: [
                "Algorithm & Coding 1 (Medium)",
                "Algorithm & Coding 2 (Medium)",
                "Behavioral Fit (teamwork, conflict, ownership)",
                "Light System Design / OOD (class, small architecture)",
              ],
            },
          ],
        },
        {
          title: "Senior Software Engineer (~4–7 years)",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Background, projects, technical experience."] },
            { title: "2. Online Test (may be present)", bullets: ["Medium–Hard."] },
            {
              title: "3. Technical Screens (1–2 rounds)",
              bullets: ["Coding Medium–Hard (Graphs, DP, Backtracking); light System Design or OOD."],
            },
            {
              title: "4. Onsite (4–5 rounds)",
              bullets: [
                "2 Coding rounds Medium–Hard (edge cases, optimization)",
                "End-to-end System Design (chat, notification, order processing…)",
                "Behavioral — leadership, mentoring, team communication",
                "Project Deep-dive (varies by role) — troubleshooting, optimization",
              ],
            },
          ],
        },
      ],
      tips: {
        title: "Shopee typically values",
        bullets: ["Clean, optimized code.", "System design (Senior).", "Communication & collaboration."],
      },
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
    en: {
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "Coding Medium (Codility)" },
        { slug: "computer-science-fundamental-interview", note: "CS + Java core if the role is Java-heavy" },
        { slug: "khoa-hoc-backend-java", note: "Backend Java stack" },
        { slug: "system-design-interview-level-2", note: "System Design Senior++" },
        { slug: "behaviour-interview-course", note: "HM behaviour + experience deep dive" },
        { slug: "mock", note: "Mock NAB backend loop" },
      ],
      profiles: [
        {
          title: "Backend Engineer",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Background, projects, technical experience."] },
            { title: "2. Online Test (may be present — Codility)", bullets: ["Coding Medium–Hard."] },
            {
              title: "3. Technical Screens (2–3 rounds)",
              bullets: [
                "Coding (Medium) + CS fundamentals (Java core if the role is Java-heavy).",
                "System Design — Senior++ only.",
                "Final round with the HM: behavior + past experience deep dive.",
              ],
            },
          ],
        },
      ],
    },
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
    en: {
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "Coding Medium–Hard" },
        { slug: "computer-science-fundamental-interview", note: "CS fundamental rounds" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design Junior++" },
        { slug: "cracking-machine-coding-low-level-design-round", note: "LLD / machine coding (common at TikTok)" },
        { slug: "behaviour-interview-course", note: "HM behaviour round" },
        { slug: "mock", note: "Mock TikTok backend loop" },
      ],
      profiles: [
        {
          title: "Backend Engineer",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Background, projects, experience."] },
            { title: "2. Online Test", bullets: ["Hackerrank — typically intern/new grad; Medium–Hard or CS fundamentals."] },
            {
              title: "3. Technical Screens (4–5 rounds)",
              bullets: [
                "Coding (Medium–Hard) + CS fundamentals.",
                "System Design — Junior++.",
                "Final HM round: behavior + past experience deep dive.",
              ],
            },
          ],
        },
      ],
    },
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
    en: {
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "Coding Medium–Hard" },
        { slug: "computer-science-fundamental-interview", note: "CS fundamentals" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design" },
        { slug: "behaviour-interview-course", note: "HM behaviour + experience" },
        { slug: "mock", note: "Mock Nvidia loop (varies by team)" },
      ],
      profiles: [
        {
          title: "Backend — System Engineer",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Background, projects, experience."] },
            {
              title: "2. Technical Screens (4–5 rounds, varies by team)",
              bullets: [
                "Coding (Medium–Hard) + CS fundamentals.",
                "System Design.",
                "Final HM round: behavior + past experience deep dive.",
              ],
            },
          ],
        },
      ],
    },
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
    en: {
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "2 Coding rounds Medium–Hard" },
        { slug: "computer-science-fundamental-interview", note: "CS fundamentals each round" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design Mid++" },
        { slug: "behaviour-interview-course", note: "Behaviour embedded in each round" },
        { slug: "mock", note: "Mock ANZ×HCL loop" },
      ],
      profiles: [
        {
          title: "Backend Engineer",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Background, projects, experience."] },
            {
              title: "2. Technical Screens (3 rounds, varies by team)",
              bullets: [
                "Coding (Medium–Hard) + CS fundamentals — 2 rounds.",
                "System Design: only for Mid++; juniors may have an extra coding round instead.",
                "Every round includes behavior.",
              ],
            },
          ],
        },
      ],
    },
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
    en: {
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "Codility + tech coding rounds" },
        { slug: "computer-science-fundamental-interview", note: "2 rounds CS fundamentals" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design Mid/Senior" },
        { slug: "behaviour-interview-course", note: "Behaviour as the first round" },
        { slug: "mock", note: "Mock Employment Hero loop" },
      ],
      profiles: [
        {
          title: "Backend Engineer",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Background, projects, experience."] },
            { title: "2. Online Test (Codility)", bullets: ["Medium + Hard."] },
            {
              title: "3. Technical Screens (3 rounds, varies by team)",
              bullets: [
                "First round: typically behavior first, then technical.",
                "Tech: ~2 rounds CS fundamentals + Coding (Medium–Hard).",
                "System Design: definitely for Senior; possible for Mid.",
              ],
            },
          ],
        },
      ],
    },
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
    en: {
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "DSA Hard — the main focus" },
        { slug: "computer-science-fundamental-interview", note: "Very deep CS fundamentals" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design Junior/Senior" },
        { slug: "behaviour-interview-course", note: "HM behaviour (+ tech possible)" },
        { slug: "mock", note: "Mock Worldquant loop" },
      ],
      profiles: [
        {
          title: "Backend / Data Engineer (Python)",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Background, projects, experience."] },
            { title: "2. Online Test (Hackerrank)", bullets: ["Medium + Hard (may not be present depending on role)."] },
            {
              title: "3. Technical Screens (4–5 rounds, varies by team)",
              bullets: [
                "Very deep CS fundamentals & DSA (Hard).",
                "System Design may apply to Junior; WQ has no mid level; Senior definitely has SD.",
                "Behavior with the HM (may also ask about tech & past experience).",
                "May also ask about Python/C++ depending on role.",
              ],
            },
          ],
        },
      ],
    },
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
    en: {
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "DSA Hard — correct & optimized code (CP-style)" },
        { slug: "computer-science-fundamental-interview", note: "Very deep CS fundamentals" },
        { slug: "system-design-interview-level-2", note: "System Design Senior" },
        { slug: "behaviour-interview-course", note: "HM behaviour" },
        { slug: "mock", note: "Mock Anduin loop" },
      ],
      profiles: [
        {
          title: "Software Engineer",
          sections: [
            { title: "1. Recruiter Screen", bullets: ["Background, projects, experience."] },
            { title: "2. Online Test", bullets: ["Medium + Hard (may not be present depending on role)."] },
            {
              title: "3. Technical Screens (4–5 rounds, varies by team)",
              bullets: [
                "Very deep CS fundamentals & DSA (Hard).",
                "Interviewers often have a competitive programming background — correct & optimized code.",
                "Senior has a System Design round.",
                "Behavior with the Hiring Manager.",
              ],
            },
          ],
        },
      ],
    },
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
    en: {
      note: "SAP values deep technical understanding plus the ability to turn complex business (ERP) requirements into scalable software; it emphasizes structured thinking and clear communication.",
      recommendations: [
        { slug: "khoa-hoc-dsa", note: "Coding Screen (Medium) + Onsite Coding (Hard), debugging, clean code" },
        { slug: "khoa-hoc-system-design-interview-big-tech", note: "System Design: distributed, ERP scale, API idempotency" },
        { slug: "behaviour-interview-course", note: "Behavioral / Leadership: ownership, influence, conflict" },
        { slug: "computer-science-fundamental-interview", note: "Solid CS foundation for the technical rounds" },
        { slug: "mock", note: "Mock the full SAP loop (5 rounds)" },
      ],
      profiles: [
        {
          title: "Software Engineer",
          sections: [
            {
              title: "1. Recruiter Screen",
              bullets: [
                "Motivation, role fit, logistics.",
                "Understand SAP's position in the SaaS/ERP market — why SAP (lack of business context is a common failure).",
              ],
            },
            {
              title: "2. Coding Screen",
              blocks: [
                {
                  icon: "🔵",
                  title: "Algorithm & Coding",
                  bullets: [
                    "LeetCode-medium problems under time pressure.",
                    "Array, String, Hash, Tree; sometimes a SaaS-flavored data structure (e.g. count unique users within a time window).",
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
                    "Design under scale constraints; service decomposition, DB schema, caching, trade-offs.",
                    "ERP context: API to upload large config files (reliability, idempotency, user feedback); scaling a real-time analytics dashboard to millions of events/min.",
                  ],
                },
              ],
            },
            {
              title: "4. Onsite Coding",
              blocks: [
                {
                  icon: "🟠",
                  title: "Deeper coding + debugging",
                  bullets: [
                    "LeetCode-hard, edge cases, code clarity.",
                    "Debug a buggy backend snippet (e.g. 500 error) — read and fix.",
                    "Clear variable names + sensible comments — unclear code is a common failure.",
                  ],
                },
              ],
            },
            {
              title: "5. Behavioral / Leadership",
              bullets: [
                "Ownership: drive a problem from discovery to resolution, even beyond your remit.",
                "Influence: persuade senior stakeholders / cross-functional teams who initially disagree — articulate the influence strategy (don't credit the 'idea' alone).",
                "Conflict resolution: how you handled a conflict in a project and the outcome.",
              ],
            },
          ],
        },
      ],
      tips: {
        title: "SAP in a nutshell",
        bullets: [
          "Understand SAP's SaaS/ERP market position — don't fail for lack of business context.",
          "Clean code: clear variable names + sensible comments.",
          "In behavioral rounds, give concrete examples of influence & ownership, not generic statements.",
        ],
      },
    },
  },
];
