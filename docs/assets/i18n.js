// i18n dictionary — keys are dot.separated.namespace
// Used by applyI18n() in app.js. Mark elements with:
//   data-i18n="key"               → replace textContent
//   data-i18n-html="key"          → replace innerHTML (use for content with markup)
//   data-i18n-attr="attr|key"     → set attribute, e.g. data-i18n-attr="placeholder|faq.searchPh"

window.I18N = {
  vi: {
    "lang.switch.alt": "Chuyển sang English",
    "lang.switch.label": "EN",

    // ============== NAV ==============
    "nav.home":       "Trang chủ",
    "nav.roadmap":    "Lộ trình",
    "nav.courses":    "Khoá học",
    "nav.book":       "Coding Book",
    "nav.mock":       "Mock 1-1",
    "nav.resources":  "Resources",
    "nav.mentors":    "Giảng viên",
    "nav.stories":    "Success Stories",
    "nav.podcast":    "Podcast",
    "nav.contact":    "Liên hệ",

    // ============== HERO ==============
    "hero.eyebrow":   "Software Education • Mastering Engineer",
    "hero.since":     "· est. 26·04·2023",
    "hero.title.html":
      'Chinh phục <span class="grad">Big Tech</span><br />cùng mentor thực chiến.',
    "hero.sub.html":
      "100% giảng viên đến từ Google, Amazon, TikTok, Shopee, Uber, Spotify… Lộ trình rõ ràng từ fresher đến senior. Học live trên Zoom trong <strong>lớp nhỏ 15–20 học viên</strong>, hỗ trợ 24/7 trên Discord. Học viên xuất sắc còn được mentor <strong>refer trực tiếp vào Big Tech</strong> (Google, Meta, Amazon, Nvidia…).",
    "hero.cta1":      "Xem khoá học",
    "hero.cta2":      "Gặp giảng viên →",

    // ============== STATS ==============
    "stats.years":          "Năm đồng hành",
    "stats.years.since":    "từ 26·04·2023",
    "stats.students":       "Học viên đã đào tạo",
    "stats.offers":         "Offers được ghi nhận",
    "stats.youtube":        "YouTube subscribers",
    "stats.substack":       "Substack subscribers",
    "stats.caption.mentors": "mentors từ Big Tech",
    "stats.caption.giangvien": "giảng viên",
    "stats.caption.courses":   "khoá học chuyên sâu",

    // ============== COMPANIES MARQUEE ==============
    "companies.label": "Học viên EngineerPro đã nhận offer tại",

    // ============== PILLARS ==============
    "pillars.head":     "3 điều cốt lõi của EngineerPro",
    "pillars.intro":    "Kết tinh từ kinh nghiệm thực chiến của mentor tại các công ty công nghệ hàng đầu.",
    "pillar1.title":    "Thăng tiến sự nghiệp",
    "pillar1.body":     "Mentor giúp rút ngắn quãng đường phát triển sự nghiệp bằng lời khuyên & kinh nghiệm thực chiến tại nhiều công ty lớn.",
    "pillar2.title":    "Cải tiến không ngừng",
    "pillar2.body":     "Lộ trình rõ ràng từ người chưa kinh nghiệm đến Senior Mid Level — tự tin ứng tuyển công ty công nghệ hàng đầu.",
    "pillar3.title":    "Cộng đồng Alumni",
    "pillar3.body":     "Tham gia cộng đồng Việt Nam và toàn thế giới để cùng ôn luyện, trao đổi và tiến bộ cùng nhau.",

    // ============== FORMAT (home section) ==============
    "format.head":       "Hình thức học",
    "format.intro":      "Học trực tiếp, hỏi trực tiếp, hỗ trợ trực tiếp — không có video thu sẵn.",
    "format.illu.alt":   "Minh hoạ hình thức học EngineerPro: Zoom live + Discord 24/7, lớp 15-20 học viên",
    "format.zoom.title":  "Lớp live trên Zoom",
    "format.zoom.body":   "100% buổi học diễn ra trực tiếp trên Zoom cùng mentor đang làm tại Big Tech. Học viên hỏi đáp realtime, được sửa code và mock interview trên lớp.",
    "format.zoom.b1":     "Mentor live, không video thu sẵn",
    "format.zoom.b2":     "Slide, code, và bài tập gửi sau mỗi buổi",
    "format.zoom.b3":     "Record lại buổi học cho học viên xem lại",
    "format.discord.title": "Cộng đồng Discord hỗ trợ 24/7",
    "format.discord.body":  "Mỗi học viên được thêm vào server Discord riêng — kênh hỏi đáp, chia sẻ resource, tìm partner mock interview, và networking với alumni đang làm tại Big Tech.",
    "format.discord.b1":  "Mỗi lớp giới hạn 15–20 học viên",
    "format.discord.b2":  "Hỏi-đáp với mentor & alumni mọi lúc",
    "format.discord.b3":  "Channel riêng theo từng khoá / topic",
    "format.tip.html":    "<strong>Tip:</strong> sau khi đăng ký, học viên sẽ nhận lịch học qua email & invite link Discord trong vòng 24 giờ.",

    // ============== COURSES ==============
    "courses.head":  "Khoá học",
    "courses.intro": "khoá đào tạo chuyên sâu — từ DSA, System Design, Backend (Go / Java), đến Behaviour Interview và Machine Coding.",
    "courses.filter.all": "Tất cả",
    "courses.empty": "Không tìm thấy khoá nào khớp với tag này.",
    "courses.card.viewMore": "Xem chi tiết →",
    "course.back":   "← Quay lại danh sách khoá học",
    "course.cta":    "Nhắn fanpage để tư vấn lộ trình →",
    "course.allCourses": "← Tất cả khoá học",

    // ============== MENTORS ==============
    "mentors.head":  "Giảng viên",
    "mentors.intro.html":
      '<span id="mentorsCount">19</span> mentor đang làm việc tại Google, Amazon, Meta, TikTok, Spotify, Shopee, Acronis, AWS… Bấm vào nút LinkedIn để xem profile.',
    "mentors.cta.linkedin": "LinkedIn",
    "mentors.cta.disabled": "LinkedIn — cập nhật sau",

    // ============== STORIES ==============
    "stories.head":  "Success Stories",
    "stories.intro.html":
      '<span id="storiesCount">94</span> câu chuyện học viên EngineerPro chinh phục offer tại Google, Meta, Amazon, TikTok, Microsoft, Grab, Shopee, NAB, ANZ… Sắp xếp theo Big Tech trước.',
    "stories.foot.html":
      'Đây mới chỉ là một phần — xem thêm trên <a href="https://engineerprovn.substack.com/" target="_blank" rel="noopener">Substack</a> hoặc <a href="https://viblo.asia/u/EngineerPro" target="_blank" rel="noopener">Viblo</a>.',
    "stories.back":  "← Tất cả câu chuyện",
    "stories.cta":   "Nhắn fanpage để được mentor tư vấn →",
    "stories.cta.substack": "Xem bản gốc trên Substack ↗",
    "stories.card.cta": "Đọc bài →",
    "stories.empty": "Không có câu chuyện nào khớp.",
    "toast.success.close": "Đóng",
    "toast.success.badge": "CÂU CHUYỆN THÀNH CÔNG",
    "toast.success.cta": "Xem chi tiết →",

    // ============== PODCAST ==============
    "podcast.head": "Podcast",
    "podcast.intro.html":
      '<span id="podcastCount">12</span> tập gần nhất — bấm vào để nghe trực tiếp trên <a href="https://engineerprovn.substack.com/podcast/archive?sort=new" target="_blank" rel="noopener">Substack</a>.',
    "podcast.card.cta": "Nghe trên Substack →",

    // ============== ROADMAP ==============
    "roadmap.eyebrow": "📍 Lộ trình ôn thi · Big Tech",
    "roadmap.title.html":
      'Từ <span class="grad">fresher</span> đến <span class="grad">Big Tech offer</span><br />trong 3 giai đoạn rõ ràng.',
    "roadmap.extras.title": "Song song với lộ trình chính",
    "roadmap.module.cta": "Bấm vào đây để xem chi tiết khoá học →",
    "roadmap.benefits.head": "Khi là học viên EngineerPro, bạn nhận được gì?",
    "roadmap.cta1":   "Xem khoá học áp dụng →",
    "roadmap.cta2":   "💬 Bấm vào đây để nhắn fanpage tư vấn lộ trình →",

    // ============== BOOK ==============
    "book.eyebrow":   "📚 Sách miễn phí cho cộng đồng · 2026",
    "book.read.en":   "Đọc sách (EN) →",
    "book.read.vi":   "Đọc tiếng Việt",
    "book.why":       "Vì sao nên đọc?",
    "book.why.intro": "Đúc kết từ hàng trăm vòng phỏng vấn ở cả hai phía — ứng viên và interviewer — tại TikTok, Grab và các Big Tech khác.",
    "book.chapters":  "44 chương — sắp xếp theo pattern",
    "book.chapters.intro":
      "Mỗi chương gồm: mục tiêu, khi nào áp dụng, code template, bài tập cuối chương, và 6+ bài LeetCode điển hình có lời giải đầy đủ.",
    "book.final.head": "Sẵn sàng luyện thuật toán theo pattern?",
    "book.final.body.html":
      'Sách <strong>miễn phí 100%</strong> cho cộng đồng. Nếu thấy hữu ích, hãy nhắn fanpage để ủng hộ tác giả — donate từ <strong>20 USD</strong> còn được tặng series 10 video <em>Career & Interview Hack</em> độc quyền.',
    "book.final.cta1": "Mở sách trên GitHub Pages →",
    "book.final.cta2": "Nhắn fanpage để ủng hộ ❤",

    // ============== RESOURCES ==============
    "resources.head":   "Interview Resources",
    "resources.badge":  "FREE",
    "resources.intro":  "Bộ tài nguyên miễn phí — bấm từng nhóm (CV, HR checklist, PIP Big Tech, CS Fundamentals, Golang, Programming Foundation) để xem chi tiết.",
    "resources.searchPh": "Tìm trong Resources… (vd: CV, STAR, Golang)",
    "resources.expand":   "Mở tất cả",
    "resources.collapse": "Thu gọn",
    "resources.empty":    "Không tìm thấy nhóm tài nguyên nào khớp.",
    "resources.expandOne":  "Mở rộng",
    "resources.collapseOne": "Thu gọn",
    "resources.hr.kicker": "✅ CHECKLIST · HR PHONE SCREEN",
    "resources.hr.head": "HR / Recruiter call — đừng fail vì phần “dễ”",
    "resources.hr.sub": "Vòng gọi 20–30 phút trước technical — thường bị đánh giá chủ quan nếu chưa chuẩn bị.",
    "resources.hr.intro": "Nhiều bạn rớt sớm không phải vì coding, mà vì HR/recruiter hỏi self-intro, behaviour, project depth và motivation — và cảm thấy bạn chưa “own” công việc mình làm hoặc chưa thật sự muốn vào công ty. Bấm từng mục để xem tips chi tiết.",
    "resources.hr.searchPh": "Tìm trong checklist… (vd: STAR, motivation, project)",
    "resources.hr.expand":   "Mở tất cả",
    "resources.hr.collapse": "Thu gọn",
    "resources.hr.empty":    "Không tìm thấy mục nào khớp.",
    "resources.hr.item1.title": "Tell me about yourself",
    "resources.hr.item1.why": "Mở đầu ~90 giây – 2 phút — HR quyết định có muốn đẩy bạn sang vòng sau không.",
    "resources.hr.item1.t1": "Present → Past → Future: role hiện tại, highlight có số liệu, vì sao apply vị trí/công ty này.",
    "resources.hr.item1.t2": "Không đọc CV từng dòng; kết bằng hook “That’s why I’m excited about …”.",
    "resources.hr.item1.t3": "Luyện nói to, rõ — tránh monologue quá dài.",
    "resources.hr.item2.title": "Behavioural / situational (STAR)",
    "resources.hr.item2.why": "HR hay hỏi conflict, failure, leadership, deadline — để xem bạn phản ứng thế nào khi làm việc thật.",
    "resources.hr.item2.t1": "Chuẩn bị đủ story behavioural: conflict, mistake, influence without authority, tight deadline, disagreement.",
    "resources.hr.item2.t2": "STAR gọn: Situation → Task → Action (chi tiết I làm gì) → Result (metric nếu có).",
    "resources.hr.item2.t3": "Tránh “we did…” suốt — recruiter cần signal cá nhân, không phải team generic.",
    "resources.hr.item3.title": "Past projects — chứng minh bạn nắm việc mình làm",
    "resources.hr.item3.why": "HR/recruiter thường drill project trên CV để xem có “resume inflation” không.",
    "resources.hr.item3.t1": "Chọn project gần nhất: problem, scope của bạn, trade-offs, outcome, stack — nói được không cần slide.",
    "resources.hr.item3.t2": "Walk-through flow / architecture ở mức high-level; sẵn sàng giải thích quyết định kỹ thuật bạn chịu trách nhiệm.",
    "resources.hr.item3.t3": "Project team → nói rõ phần việc của bạn; đừng claim credit cả team.",
    "resources.hr.item4.title": "Motivation — why company / why role",
    "resources.hr.item4.why": "Thiếu motivation cụ thể = red flag “ứng tượng trúng đâu hay đấy”.",
    "resources.hr.item4.t1": "Research điểm cụ thể: sản phẩm, culture/values, scope level role — không chỉ “công ty lớn”.",
    "resources.hr.item4.t2": "Nối motivation với mục tiêu nghề nghiệp trung hạn của bạn.",
    "resources.hr.item4.t3": "Không diss công ty cũ; compensation chỉ là một phần của câu trả lời.",
    "resources.hr.item5.title": "Logistics & chuyên nghiệp",
    "resources.hr.item5.why": "Vòng HR cũng screen fit thực tế — timeline, package, next steps.",
    "resources.hr.item5.t1": "Biết notice period, salary range mong muốn (hoặc “open depending on package”), work authorization nếu apply abroad.",
    "resources.hr.item5.t2": "Chuẩn bị câu hỏi ngược: process, team structure, timeline các vòng sau.",
    "resources.hr.item5.t3": "Test mic/line; chỗ yên tĩnh; CV + JD mở sẵn trước mặt.",
    "resources.hr.item6.title": "Sau cuộc gọi",
    "resources.hr.item6.why": "Iteration nhỏ giúp vòng sau mạnh hơn — kể cả khi bạn pass HR screen.",
    "resources.hr.item6.t1": "Ghi lại câu hỏi HR đã hỏi → refine story / pitch cho lần sau.",
    "resources.hr.item6.t2": "Thank-you note ngắn trong ngày (optional nhưng tăng impression).",
    "resources.hr.promo.badge": "Khóa học gợi ý",
    "resources.hr.promo.head": "Behaviour Interview Course — luyện đúng phần HR hay hỏi",
    "resources.hr.promo.text": "12 buổi live: self-intro, behavioural phổ biến, leadership principles & STAR bằng tiếng Anh — format nhiều Big Tech dùng từ recruiter screen đến onsite behavioural.",
    "resources.hr.promo.cta": "Xem khóa Behaviour Interview →",
    "resources.hr.promo.consult": "Nhắn fanpage tư vấn lộ trình →",
    "resources.pip.kicker": "⚠️ GUIDE · PIP BIG TECH",
    "resources.pip.head": "How to handle PIP — Axon, Grab, TikTok, Shopee, Nvidia, Google, Amazon…",
    "resources.pip.sub": "Thoát PIP hiếm khi thành công — ưu tiên negotiate mutual severance (vd. N+1, N+2 tháng lương) có lợi cho bạn.",
    "resources.pip.intro": "Performance Improvement Plan (PIP) ở Big Tech thường là bước chuẩn bị cho offboarding, không phải “cơ hội công bằng” để cứu job. EngineerPro khuyên anh em tập trung đàm phán exit package sạch, bảo vệ uy tín và runway tìm việc — thay vì hy vọng turnaround trong timeline ngắn.",
    "resources.pip.searchPh": "Tìm trong guide PIP… (vd: severance, RSU, garden leave)",
    "resources.pip.expand": "Mở tất cả",
    "resources.pip.collapse": "Thu gọn",
    "resources.pip.empty": "Không tìm thấy mục nào khớp.",
    "resources.pip.item1.title": "PIP ở Big Tech thực sự là gì?",
    "resources.pip.item1.why": "Google, Amazon, Meta, TikTok, Shopee, Grab, Nvidia, Axon… đều có khung tương tự: goal đo lường, check-in hàng tuần, quyết định cuối từ manager + HR.",
    "resources.pip.item1.namesIntro": "Cùng bản chất (formal performance coaching, thường dẫn tới exit) — mỗi công ty đặt tên khác nhau:",
    "resources.pip.item1.n1": "Amazon: Focus (giai đoạn 1) → Pivot nếu không pass Focus",
    "resources.pip.item1.n2": "TikTok / ByteDance: Formal Coaching",
    "resources.pip.item1.n3": "Google: Performance Improvement Plan (PIP)",
    "resources.pip.item1.n4": "Meta: Performance Improvement Plan (PIP)",
    "resources.pip.item1.n5": "Microsoft: Performance Improvement Plan",
    "resources.pip.item1.n6": "Nvidia: Performance Improvement Plan (PIP) / performance coaching track",
    "resources.pip.item1.n7": "Apple: Performance Improvement Plan",
    "resources.pip.item1.n8": "Shopee / Grab: Performance Improvement Plan (thường gọi PIP)",
    "resources.pip.item1.n9": "Axon & nhiều US tech khác: PIP hoặc Performance Coaching",
    "resources.pip.item1.t1": "PIP = quy trình tài liệu hoá performance, giảm rủi ro pháp lý cho công ty khi terminate.",
    "resources.pip.item1.t2": "Manager đã có signal “does not meet bar” từ trước — PIP thường là formalize bước cuối, không phải bất ngờ.",
    "resources.pip.item1.t3": "Ở nhiều nơi, pass rate sau PIP rất thấp; đừng lên kế hoạch tài chính dựa trên “mình sẽ pass”.",
    "resources.pip.item2.title": "Vì sao “cơ hội thoát PIP” cực khó",
    "resources.pip.item2.why": "Timeline ngắn (thường vài tuần đến hai chu kỳ review) + bar cao + bias xác nhận — bạn phải overturn perception đã tồn tại.",
    "resources.pip.item2.t1": "Goal PIP thường gắn delivery đã miss — khó chứng minh turnaround trong cửa sổ hẹp.",
    "resources.pip.item2.t2": "Stakeholder ít muốn “bet” lại headcount đã flagged; headcount planning & promo freeze làm PIP pass hiếm hơn.",
    "resources.pip.item2.t3": "Năng lượng tốt nhất: chuẩn bị exit có kiểm soát — không burn bridge, không ký thức gì khi chưa hiểu.",
    "resources.pip.item3.title": "Chiến lược số 1: Mutual separation / severance",
    "resources.pip.item3.why": "Đàm phán package chấm dứt hợp đồng hai bên (mutual agreement) thường tốt hơn bị terminate for cause sau fail PIP.",
    "resources.pip.item3.severanceHead": "N+1, N+2 nghĩa là gì?",
    "resources.pip.item3.severanceN": "N = số năm bạn đã làm việc tại công ty (tenure; HR thường làm tròn theo policy nội bộ).",
    "resources.pip.item3.severanceFormula": "N+1, N+2… = tổng số tháng lương được đền bù khi chấm dứt (severance), thường tính trên base salary — không phải “thêm 1 năm làm việc”.",
    "resources.pip.item3.severanceExample": "Ví dụ: làm 3 năm → N = 3. Package N+1 = 4 tháng lương; N+2 = 5 tháng lương (lump-sum hoặc trả theo kỳ).",
    "resources.pip.item3.severanceNote": "Số tháng thực tế còn tùy level, entity (US/SG/VN) và leverage đàm phán — mỗi công ty có khung riêng.",
    "resources.pip.item3.t1": "Mục tiêu: exit “clean” — employment record không gắn performance termination; có runway và tiền buffer.",
    "resources.pip.item3.t2": "Khung thương lượng: đòi severance theo công thức tháng lương N+1, N+2… (xem giải thích trên), không chỉ mức tối thiểu theo luật.",
    "resources.pip.item3.t3": "Có thể thêm: bonus pro-rate, PTO payout, healthcare bridge, garden leave, hỗ trợ outplacement, reference wording.",
    "resources.pip.item4.title": "Checklist package cần negotiate",
    "resources.pip.item4.why": "HR có playbook — bạn cũng cần checklist riêng; đừng chỉ nhìn vào một dòng “severance months”.",
    "resources.pip.item4.t1": "Cash: base severance (vd. N+1 / N+2 tháng lương, N = năm tenure), signing bonus clawback waiver, unpaid bonus cycle, relocation repayment waiver.",
    "resources.pip.item4.t2": "Equity: unvested RSU/ESOP — accelerated vesting một phần, extended exercise window, hoặc treatment khi mutual leave (tùy grant & policy).",
    "resources.pip.item4.t3": "Benefits & time: COBRA/health subsidy, garden leave paid, unused PTO, non-compete / non-disparagement đối xứng.",
    "resources.pip.item4.t4": "Reputation: reference check wording, title on paper, LinkedIn-friendly departure narrative nội bộ.",
    "resources.pip.item5.title": "Trước khi họp HR / People Partner",
    "resources.pip.item5.why": "Cuộc họp đầu quyết định leverage — chuẩn bị như một negotiation, không như “xin tha”.",
    "resources.pip.item5.t1": "Đọc kỹ PIP letter, handbook, equity plan, offer letter — ghi deadline, metric, ai sign-off.",
    "resources.pip.item5.t2": "Thu thập context: tenure, level, prior reviews, reorg, health/family nếu relevant (không overshare), market comp.",
    "resources.pip.item5.t3": "Chốt BATNA nội bộ: bạn muốn mutual exit với package tối thiểu nào; ai có authority approve (HRBP, comp, legal).",
    "resources.pip.item5.t4": "Mang proposal bằng văn bản sau họp — đừng agree verbal; xin vài ngày review với luật sư/ advisor nếu cần.",
    "resources.pip.item6.title": "Những điều tuyệt đối tránh",
    "resources.pip.item6.why": "Một sai lầm có thể mất hết leverage severance hoặc bị terminate ngay.",
    "resources.pip.item6.t1": "Ký separation agreement ngay trong phòng họp — luôn mang về đọc, tối thiểu 48-72 giờ.",
    "resources.pip.item6.t2": "Emotional outburst, email cc cả org, Slack drama — company sẽ document thêm “conduct”.",
    "resources.pip.item6.t3": "Tự ý nghỉ việc (rage quit) trước khi deal — thường mất severance và equity treatment xấu hơn.",
    "resources.pip.item6.t4": "Đăng chi tiết nội bộ lên mạng xã hội — vi phạm policy + làm negotiation khó hơn.",
    "resources.pip.item7.title": "Sau khi có deal — chuyển sang hunt job",
    "resources.pip.item7.why": "Package tốt chỉ có ý nghĩa nếu bạn dùng runway đó để land offer tiếp theo đúng hướng.",
    "resources.pip.item7.t1": "Update CV + LinkedIn theo framing neutral (“team restructure / mutual separation”) — đồng bộ với reference đã thỏa thuận.",
    "resources.pip.item7.t2": "Ưu tiên mock behavioural + system/DSA nếu target Big Tech — xem Resources HR checklist & khóa Behaviour Interview.",
    "resources.pip.item7.t3": "Network warm intro > cold apply; mentor review story trước onsite.",
    "resources.pip.promo.badge": "Bị PIP — cần tư vấn riêng?",
    "resources.pip.promo.head": "Đặt lịch tư vấn 1-1 qua fanpage",
    "resources.pip.promo.text": "Nếu bạn đang trong PIP và cần hướng negotiate / severance, vui lòng nhắn fanpage EngineerPro để đặt lịch tư vấn. Mỗi công ty (US / SG / VN entity) có policy khác nhau — hỗ trợ chiến lược, script nói chuyện HR, lộ trình sau exit; không thay thế luật sư lao động.",
    "resources.pip.promo.consult": "Nhắn fanpage đặt lịch tư vấn →",
    "resources.cs.kicker": "🧠 CS FUNDAMENTALS · REAL INTERVIEW QUESTIONS",
    "resources.cs.head": "~100 câu hỏi CS Fundamentals từ phỏng vấn thật — crawl LeetCode Discuss",
    "resources.cs.sub": "List câu hỏi thật từ LeetCode Discuss + khóa live CS Fundamental Interview (12 buổi qua Zoom).",
    "resources.cs.intro.html": "Danh sách <strong>free</strong> tổng hợp từ <a href=\"https://leetcode.com/discuss/\" target=\"_blank\" rel=\"noopener\">LeetCode Discuss</a> — câu hỏi non-coding (OS, network, DB…), kèm công ty &amp; vị trí/location được hỏi. Muốn ôn có hệ thống + mock đúng format Big Tech → <a href=\"/courses/computer-science-fundamental-interview/\">khóa CS Fundamental Interview</a> (12 buổi live qua Zoom).",
    "resources.cs.footer.html": "Muốn luyện trả lời + feedback mentor? <a href=\"/courses/computer-science-fundamental-interview/\">Đăng ký khóa CS Fundamental Interview →</a>",
    "resources.cs.searchPh": "Tìm câu hỏi… (vd: TCP, deadlock, ACID, thread)",
    "resources.cs.topicAll": "Tất cả chủ đề",
    "resources.cs.expand": "Mở tất cả",
    "resources.cs.collapse": "Thu gọn",
    "resources.cs.empty": "Không tìm thấy câu hỏi nào khớp.",
    "resources.cs.promo.badge": "Khóa EngineerPro · CS Fundamentals",
    "resources.cs.promo.head": "Computer Science Fundamental Interview — 12 buổi live qua Zoom",
    "resources.cs.promo.text": "List câu hỏi free ở dưới giúp biết Big Tech hay hỏi gì — khóa live qua Zoom giúp bạn trả lời trọn vẹn: OS, networking, DB, concurrency, OOP, browser/HTTP… đúng format technical screen / CS round.",
    "resources.cs.promo.cta": "Xem & đăng ký khóa CS Fundamentals →",
    "resources.cs.promo.consult": "Nhắn fanpage tư vấn lộ trình →",
    "resources.formats.kicker": "📋 CHEATSHEET · INTERVIEW FORMAT",
    "resources.formats.head": "Format phỏng vấn theo công ty — Amazon, Google, Meta, Grab, Axon…",
    "resources.formats.sub": "14 công ty · tổng hợp từ EngineerPro cheatsheet V2 — mang tính tham khảo.",
    "resources.formats.intro": "Mỗi công ty/team/location có thể thay đổi số vòng, thứ tự và độ khó theo thời điểm. Dùng bảng dưới để định hướng ôn tập — không coi là quy trình cố định.",
    "resources.formats.disclaimer.title": "⚠️ Format mang tính chất tham khảo",
    "resources.formats.disclaimer.body": "Process thực tế phụ thuộc team, hiring manager, location và thời điểm tuyển. Một số công ty (Amazon, Nvidia, Shopee, Google, Axon, TikTok…) ghi chú rõ từng team có thể khác nhau.",
    "resources.formats.dsaNote": "Big Tech / rich tech: topic DSA nên ít nhất LeetCode Medium trở lên.",
    "resources.formats.searchPh": "Tìm công ty, level, vòng… (vd: Amazon LP, Google L4, Axon CS)",
    "resources.formats.companyAll": "Tất cả công ty",
    "resources.formats.expand": "Mở tất cả",
    "resources.formats.collapse": "Thu gọn",
    "resources.formats.empty": "Không tìm thấy công ty/level nào khớp.",
    "resources.formats.footer.html": "Muốn mock đúng format từng công ty + feedback mentor? <a href=\"/mock/\">Đặt Mock Interview 1-1 →</a> hoặc xem <a href=\"/courses/\">các khóa live EngineerPro</a>.",
    "resources.formats.reco.title": "Khóa EngineerPro gợi ý",
    "resources.formats.reco.mock": "Mock Interview 1-1",
    "resources.foundation.kicker": "📺 PLAYLIST · YOUTUBE",
    "resources.foundation.cta":    "Mở full playlist ↗",
    "resources.golangTour.kicker": "📺 PLAYLIST · YOUTUBE",
    "resources.golangTour.cta":    "Mở full playlist ↗",
    "resources.cv.kicker": "📄 BỘ TÀI LIỆU VIẾT CV",
    "resources.cv.head":   "Viết CV chuẩn Big Tech",
    "resources.cv.sample.kicker": "★ CV MẪU — ĐÃ PASS GOOGLE",
    "resources.cv.sample.b1": "1 trang, layout sạch, chuẩn ATS",
    "resources.cv.sample.b2": "Format bullet \"X-Y-Z\" — action · context · impact",
    "resources.cv.sample.b3": "Có số liệu cụ thể (latency, scale, savings)",
    "resources.cv.sample.b4": "Skills section gọn, không spam keyword",
    "resources.cv.sample.cta": "Mở full CV trên Drive ↗",
    "resources.cv.overleaf.kicker": "1 · Template LaTeX",
    "resources.cv.overleaf.cta":    "Mở trên Overleaf ↗",
    "resources.cv.review.kicker":   "2 · Playlist Review CV",
    "resources.cv.tool.kicker":     "3 · Video tool nhanh",
    "resources.cv.tool.cta":        "Xem trên YouTube ↗",

    // ============== PARTNERS ==============
    "partners.head":  "Đối tác",
    "partners.intro": "EngineerPro hợp tác cùng các tổ chức / chương trình cùng sứ mệnh đưa kỹ sư Việt vươn ra Big Tech.",
    "partners.soon.html":
      'Bạn là tổ chức quan tâm hợp tác? <a href="https://m.me/EngineerPro.Official" target="_blank" rel="noopener">Nhắn fanpage để trao đổi →</a>',
    "partners.strip.tag":  "ĐỐI TÁC",
    "partners.strip.text.html":
      'Cùng <strong>MentorPro</strong> — chương trình mentor 1-1 cho ai muốn break-in Big Tech',
    "partners.strip.cta":  "Xem chi tiết →",

    // ============== FAQ ==============
    "faq.head":      "Câu hỏi thường gặp",
    "faq.intro.html":
      '<span id="faqCount">6</span> câu hỏi phổ biến nhất — bấm vào từng câu để xem trả lời. Có thể search nhanh ở khung bên dưới.',
    "faq.searchPh":  "Tìm trong FAQ… (vd: tiếng Anh, backend, lộ trình)",
    "faq.expand":    "Mở tất cả",
    "faq.collapse":  "Thu gọn",
    "faq.empty":     "Không tìm thấy câu hỏi nào khớp.",
    "faq.terms.cta": "Xem điều khoản dịch vụ →",

    // ============== TERMS OF SERVICE ==============
    "terms.head":  "Điều khoản dịch vụ",
    "terms.intro": "Cam kết & chính sách của EngineerPro với học viên — vui lòng đọc kỹ trước khi đăng ký khoá học.",
    "terms.body.html":
      '<h3>1. Cam kết cung cấp khóa học</h3>' +
      '<p>Các khóa học mà học viên đăng ký tại <strong>EngineerPro</strong> sẽ được cung cấp đầy đủ và đúng theo cam kết. Chúng tôi có nghĩa vụ đảm bảo chất lượng và tiến độ giảng dạy của khóa học đã được quảng bá.</p>' +
      '<h3>2. Quyền sở hữu tài liệu học tập</h3>' +
      '<p>Tất cả các tài liệu học tập, bao gồm nhưng không giới hạn ở video record và tài liệu, đều thuộc <strong>quyền sở hữu trí tuệ của EngineerPro</strong>. EngineerPro bảo lưu quyền thu hồi hoặc ngừng cung cấp các tài liệu này bất cứ lúc nào. Việc chia sẻ, sao chép hoặc phát tán tài liệu ra ngoài phạm vi lớp học dưới bất kỳ hình thức nào là hành vi bị <strong>nghiêm cấm</strong>. Các tài liệu học tập (bao gồm record) chỉ được cung cấp nhằm hỗ trợ học viên trong trường hợp vắng mặt buổi học.</p>' +
      '<h3>3. Sử dụng tài liệu học tập</h3>' +
      '<p>Học viên cam kết sử dụng tài liệu của EngineerPro <strong>chỉ cho mục đích học tập</strong>. Việc sử dụng tài liệu sai mục đích, bao gồm nhưng không giới hạn ở sao chép, chia sẻ tài liệu ra ngoài phạm vi lớp học, hoặc sử dụng tài liệu cho các mục đích khác mà không có sự cho phép của EngineerPro, sẽ bị coi là vi phạm điều khoản. Trong trường hợp này, EngineerPro bảo lưu quyền thu hồi tài liệu và từ chối cung cấp các dịch vụ cho học viên mà không hoàn lại học phí hoặc các khoản phí đã đóng.</p>' +
      '<h3>4. Các dịch vụ cộng đồng</h3>' +
      '<p>Các dịch vụ cộng đồng của EngineerPro, bao gồm <strong>review CV, hỗ trợ xin việc, chia sẻ tài liệu/record và tham gia Alumni</strong>, là các dịch vụ <strong>miễn phí</strong> và không bao gồm trong học phí đã đóng của học viên. EngineerPro có quyền tạm dừng hoặc ngừng cung cấp các dịch vụ này nếu cảm thấy các hoạt động không còn phù hợp hoặc không đáp ứng được yêu cầu của cộng đồng. Ngoài ra, chúng tôi cũng bảo lưu quyền từ chối cung cấp các dịch vụ này cho học viên trong trường hợp có xung đột lợi ích hoặc khi không còn phù hợp.</p>' +
      '<h3>5. Chính sách bảo lưu khóa học</h3>' +
      '<p>EngineerPro <strong>không hỗ trợ bảo lưu khóa học</strong>. Tuy nhiên, trong một số trường hợp đặc biệt, đội ngũ của chúng tôi sẽ xem xét và có thể chấp thuận bảo lưu khóa học. Quyết định bảo lưu sẽ do EngineerPro đưa ra và chúng tôi có quyền từ chối bảo lưu nếu thấy không hợp lý.</p>' +
      '<h3>6. Chính sách tham gia Alumni và Internal Techtalk</h3>' +
      '<p>EngineerPro Alumni và Internal Techtalk là các nền tảng để các mentor và học viên hỗ trợ lẫn nhau, giúp nhau phát triển sự nghiệp sau khóa học. Tất cả các thành viên trong cộng đồng Alumni có quyền và nghĩa vụ tham gia xây dựng và phát triển cộng đồng này. EngineerPro bảo lưu quyền từ chối cho phép học viên tham gia nếu họ có hành vi <strong>thiếu tính xây dựng hoặc có xung đột lợi ích</strong>.</p>' +
      '<h3>7. Chính sách hoàn tiền và dời cọc / học phí</h3>' +
      '<h4>a. Chính sách hoàn tiền</h4>' +
      '<p>Chúng tôi cung cấp dịch vụ chất lượng và luôn nỗ lực để đáp ứng tốt nhất kỳ vọng của học viên. Chúng tôi hiểu rằng có thể xảy ra những tình huống phát sinh không mong muốn, vì vậy rất mong học viên sẽ đọc kĩ nội dung điều khoản bên dưới:</p>' +
      '<p><strong>Không hoàn tiền trong mọi trường hợp</strong> (ngoại trừ khoá học bị huỷ) — Học viên không thể yêu cầu hoàn lại học phí hoặc cọc đã đóng. Điều này áp dụng cho mọi khóa học ngoại trừ trường hợp khóa học bị hủy bởi EngineerPro.</p>' +
      '<h4>b. Chính sách chuyển cọc / học phí sang khoá học khác</h4>' +
      '<p>Học viên có thể chuyển cọc/học phí đã đóng cho khóa học này sang một khóa học khác với những điều kiện sau:</p>' +
      '<ul>' +
      '<li>Học viên phải yêu cầu chuyển cọc/học phí <strong>ít nhất 5 ngày trước ngày khai giảng</strong> của khóa học đã đăng ký.</li>' +
      '<li>Học viên được yêu cầu chuyển <strong>tối đa 2 lần</strong>.</li>' +
      '<li>Việc chuyển cọc/học phí sang khóa học khác phụ thuộc chỗ trống và chương trình đào tạo sẵn có tại thời điểm yêu cầu.</li>' +
      '<li>Nếu khóa học mới có học phí <strong>cao hơn</strong>, học viên thanh toán phần chênh lệch. Nếu <strong>thấp hơn</strong>, phần chênh lệch không được hoàn lại.</li>' +
      '<li>Phí dời cọc/học phí (nếu có) sẽ được thông báo và yêu cầu thanh toán trước khi hoàn tất việc chuyển đổi.</li>' +
      '</ul>' +
      '<h4>c. Trường hợp không áp dụng chuyển cọc / học phí</h4>' +
      '<ul>' +
      '<li>Học viên tự ý yêu cầu huỷ khóa học hoặc dời cọc/học phí <strong>sau khi khóa học đã bắt đầu</strong>.</li>' +
      '<li>Học viên không tham gia khóa học do lý do cá nhân, không có thông báo trước.</li>' +
      '<li>Học viên không tuân thủ các quy định, điều khoản dịch vụ của EngineerPro.</li>' +
      '<li>Học viên không tham gia đầy đủ các buổi học mà không có lý do chính đáng.</li>' +
      '</ul>' +
      '<h4>d. Quy trình yêu cầu chuyển cọc / học phí</h4>' +
      '<ol>' +
      '<li>Gửi yêu cầu qua <strong>email hoặc fanpage</strong> ít nhất <strong>5 ngày trước ngày khai giảng</strong>.</li>' +
      '<li>Đính kèm lý do cụ thể và các thông tin liên quan để đội ngũ xem xét.</li>' +
      '<li>EngineerPro phản hồi trong vòng <strong>2 ngày</strong> và thông báo kết quả.</li>' +
      '</ol>' +
      '<h4>e. Quyền quyết định cuối cùng</h4>' +
      '<p>EngineerPro bảo lưu quyền quyết định cuối cùng về việc hoàn tiền hoặc chuyển cọc/học phí sang khóa học khác, tùy theo từng trường hợp cụ thể.</p>' +
      '<p class="terms-callout"><strong>Lưu ý quan trọng:</strong> Các yêu cầu hoàn tiền hoặc dời cọc sẽ được xử lý theo từng trường hợp cụ thể và theo chính sách được nêu trên.</p>',

    // ============== CONTACT ==============
    "contact.head":  "Liên hệ",
    "contact.intro": "Hãy liên hệ với chúng tôi để được giải đáp thắc mắc và tư vấn lộ trình.",
    "contact.cta.email":     "Gửi email →",
    "contact.cta.messenger": "Chat ngay →",
    "contact.cta.facebook":  "Theo dõi Fanpage →",
    "contact.cta.zalo":      "Mở Zalo →",
    "contact.cta.spotify":   "Nghe trên Spotify →",
    "contact.cta.youtube":   "Xem video →",
    "contact.cta.substack":  "Đọc & nghe →",
    "contact.cta.viblo":     "Đọc bài viết →",

    // ============== FLOATING CTA ==============
    "cta.fab.messenger": "Đặt lịch tư vấn qua FB Messenger",
    "cta.fab.zalo":      "Đặt lịch tư vấn qua Zalo",

    // ============== FOOTER ==============
    "footer.tag":  "Conquering Big Tech Marvels.",
    "footer.col1": "Học tập",
    "footer.col2": "Cộng đồng",
    "footer.col3": "Hỗ trợ",
    "footer.col4": "Đối tác",
    "footer.link.roadmap":   "Lộ trình ôn thi",
    "footer.link.courses":   "Khoá học",
    "footer.link.book":      "Coding Book",
    "footer.link.resources": "Resources miễn phí",
    "footer.link.format":    "Hình thức học",
    "footer.link.mentors":   "Giảng viên",
    "footer.link.stories":   "Success Stories",
    "footer.link.podcast":   "Podcast",
    "footer.link.faq":       "FAQ",
    "footer.link.terms":     "Điều khoản dịch vụ",
    "footer.link.mock":      "Mock Interview 1-1",
    "footer.link.contact":   "Liên hệ",

    // ============== MOCK INTERVIEW 1-1 ==============
    "mock.head":         "Mock Interview 1-1",
    "mock.intro.html":
      "Buổi mock 1-1 với <strong>interviewer từ team EngineerPro</strong> — luyện đúng style phỏng vấn Big Tech (Google, Meta, TikTok, Amazon, Microsoft, Nvidia, WorldQuant, Axon…). Ngôn ngữ mock <strong>VI hoặc EN</strong> tuỳ học viên chọn khi đăng ký.",
    "mock.sd.kicker":    "🏗 SYSTEM DESIGN",
    "mock.sd.title":     "Mock System Design",
    "mock.sd.body":      "Thiết kế hệ thống realtime với interviewer — clarify requirements, high-level design, deep-dive component, trade-off, scale-up. Feedback theo signal rubric của Big Tech cho từng level (mid / senior / staff).",
    "mock.dsa.kicker":   "💻 DSA / CODING",
    "mock.dsa.title":    "Mock DSA / Coding Interview",
    "mock.dsa.body":     "Coding interview style Big Tech: clarify → brainstorm → code → debug → complexity analysis. Interviewer hỏi đào theo edge case + đánh giá communication + clean code.",
    "mock.beh.kicker":   "🎤 BEHAVIORAL",
    "mock.beh.title":    "Mock Behavioral Interview",
    "mock.beh.body":     "Luyện trả lời câu hỏi behavioral theo framework STAR + Leadership Principles (Amazon, Meta, Google style). Mock bằng tiếng Anh, feedback về story-telling, signal mạnh / yếu, mức độ specific.",
    "mock.beh.note":     "Inbox fanpage để xem video demo (nội bộ — không public).",
    "mock.demo.watch":   "▶ Xem demo trên YouTube ↗",
    "mock.who.title":    "Ai phù hợp?",
    "mock.who.b1":       "SWE đang chuẩn bị onsite Big Tech, muốn rehearse vài tuần trước phỏng vấn thật.",
    "mock.who.b2":       "Học viên sau khoá DSA / System Design / Behavioral của EngineerPro muốn đo trình độ trước khi apply.",
    "mock.who.b3":       "Người chưa từng phỏng vấn Big Tech, muốn trải nghiệm trước một lần để bớt áp lực ngày thật.",
    "mock.session.title": "Mỗi buổi mock 1-1 bạn nhận được",
    "mock.session.b1":   "45–60 phút mock 1-1 trên Zoom (record lại để xem lại).",
    "mock.session.b2":   "Feedback chi tiết theo rubric Big Tech — không phải feedback chung chung.",
    "mock.session.b3":   "Gợi ý cụ thể cách improve cho buổi sau / cho phỏng vấn thật.",
    "mock.session.b4":   "Bonus tips về negotiation, story-telling, follow-up email sau onsite.",
    "mock.bigtech.title": "Mock theo style các Big Tech",
    "mock.bigtech.list": "Google · Meta · TikTok · Amazon · Microsoft · Nvidia · WorldQuant · Axon · Apple · Citadel",
    "mock.bigtech.note": "Interviewer từ team EngineerPro đã đi qua các vòng phỏng vấn thật tại các công ty này — mock đúng format, đúng signal, đúng level.",
    "mock.cta.primary":  "💬 Inbox fanpage để đặt lịch mock 1-1 →",
    "mock.cta.zalo":     "Hoặc đặt qua Zalo 0352 911 223 →",
    "mock.book.title":   "📅 Cách đặt lịch mock 1-1",
    "mock.book.body.html":
      "Để đặt lịch buổi mock, các bạn vui lòng <strong>nhắn qua fanpage EngineerPro</strong>. Team sẽ phản hồi trong vòng 24h để confirm <strong>topic, level, ngôn ngữ (VI / EN) và thời gian</strong> phù hợp.",
    "footer.link.messenger": "Messenger",
    "footer.link.allPartners": "Tất cả đối tác",
    "footer.fanpage.head":   "Fanpage",
  },

  en: {
    "lang.switch.alt": "Switch to Vietnamese",
    "lang.switch.label": "VI",

    "nav.home":       "Home",
    "nav.roadmap":    "Roadmap",
    "nav.courses":    "Courses",
    "nav.book":       "Coding Book",
    "nav.mock":       "Mock 1-1",
    "nav.resources":  "Resources",
    "nav.mentors":    "Mentors",
    "nav.stories":    "Success Stories",
    "nav.podcast":    "Podcast",
    "nav.contact":    "Contact",

    "hero.eyebrow":   "Software Education • Mastering Engineer",
    "hero.since":     "· est. 26·04·2023",
    "hero.title.html":
      'Conquer <span class="grad">Big Tech</span><br />with battle-tested mentors.',
    "hero.sub.html":
      "100% mentors from Google, Amazon, TikTok, Shopee, Uber, Spotify… A clear path from fresher to senior. Live Zoom sessions in <strong>small classes of 15–20 students</strong>, with 24/7 Discord support. Top students get <strong>direct mentor referrals into Big Tech</strong> (Google, Meta, Amazon, Nvidia…).",
    "hero.cta1":      "Browse courses",
    "hero.cta2":      "Meet the mentors →",

    "stats.years":          "Years going",
    "stats.years.since":    "since 26·04·2023",
    "stats.students":       "Students trained",
    "stats.offers":         "Offers recorded",
    "stats.youtube":        "YouTube subscribers",
    "stats.substack":       "Substack subscribers",
    "stats.caption.mentors": "mentors from Big Tech",
    "stats.caption.giangvien": "mentors",
    "stats.caption.courses":   "in-depth courses",

    "companies.label": "EngineerPro students have received offers at",

    "pillars.head":  "3 core values of EngineerPro",
    "pillars.intro": "Distilled from real interview experience at top tech companies.",
    "pillar1.title": "Career growth",
    "pillar1.body":  "Mentors help shorten your career runway with hands-on advice from working at top tech companies.",
    "pillar2.title": "Continuous improvement",
    "pillar2.body":  "A clear path from zero experience to Senior Mid-Level — confidently apply to top tech companies.",
    "pillar3.title": "Alumni community",
    "pillar3.body":  "Join our Vietnam-wide and global alumni community to prep, discuss, and grow together.",

    "format.head":       "Learning format",
    "format.intro":      "Live teaching, live questions, live support — no pre-recorded videos.",
    "format.illu.alt":   "EngineerPro learning format: Zoom live + Discord 24/7, classes of 15-20 students",
    "format.zoom.title":  "Live Zoom sessions",
    "format.zoom.body":   "100% of sessions are live on Zoom with mentors currently at Big Tech. Real-time Q&A, code reviews, and mock interviews in class.",
    "format.zoom.b1":     "Live mentor, never recorded video",
    "format.zoom.b2":     "Slides, code, and homework sent after each session",
    "format.zoom.b3":     "Session recording for review",
    "format.discord.title": "24/7 Discord community",
    "format.discord.body":  "Each student is added to a dedicated Discord server — Q&A channels, resource sharing, mock interview partner matching, and networking with Big Tech alumni.",
    "format.discord.b1":  "Each class limited to 15–20 students",
    "format.discord.b2":  "Always-on Q&A with mentors & alumni",
    "format.discord.b3":  "Dedicated channels per course / topic",
    "format.tip.html":    "<strong>Tip:</strong> after registration, students receive the schedule via email & Discord invite within 24 hours.",

    "courses.head":  "Courses",
    "courses.intro": "in-depth training tracks — from DSA, System Design, Backend (Go / Java), to Behavioural Interview and Machine Coding.",
    "courses.filter.all": "All",
    "courses.empty": "No courses match this tag.",
    "courses.card.viewMore": "Read more →",
    "course.back":   "← Back to all courses",
    "course.cta":    "Message our Fanpage for path consultation →",
    "course.allCourses": "← All courses",

    "mentors.head":  "Mentors",
    "mentors.intro.html":
      '<span id="mentorsCount">19</span> mentors currently at Google, Amazon, Meta, TikTok, Spotify, Shopee, Acronis, AWS… Click LinkedIn to see their profile.',
    "mentors.cta.linkedin": "LinkedIn",
    "mentors.cta.disabled": "LinkedIn — coming soon",

    "stories.head":  "Success Stories",
    "stories.intro.html":
      '<span id="storiesCount">94</span> stories of EngineerPro students landing offers at Google, Meta, Amazon, TikTok, Microsoft, Grab, Shopee, NAB, ANZ… Sorted with Big Tech first.',
    "stories.foot.html":
      'These are only some highlights — find more on <a href="https://engineerprovn.substack.com/" target="_blank" rel="noopener">Substack</a> or <a href="https://viblo.asia/u/EngineerPro" target="_blank" rel="noopener">Viblo</a>.',
    "stories.back":  "← Back to all stories",
    "stories.cta":   "Message our Fanpage for mentor consultation →",
    "stories.cta.substack": "View original on Substack ↗",
    "stories.card.cta": "Read more →",
    "stories.empty": "No stories match.",
    "toast.success.close": "Close",
    "toast.success.badge": "SUCCESS STORY",
    "toast.success.cta": "Read story →",

    "podcast.head": "Podcast",
    "podcast.intro.html":
      '<span id="podcastCount">12</span> latest episodes — click to listen on <a href="https://engineerprovn.substack.com/podcast/archive?sort=new" target="_blank" rel="noopener">Substack</a>.',
    "podcast.card.cta": "Listen on Substack →",

    "roadmap.eyebrow": "📍 Interview roadmap · Big Tech",
    "roadmap.title.html":
      'From <span class="grad">fresher</span> to <span class="grad">Big Tech offer</span><br />in 3 clear stages.',
    "roadmap.extras.title": "Alongside the main path",
    "roadmap.module.cta": "Click here to view course details →",
    "roadmap.benefits.head": "What you get as an EngineerPro student",
    "roadmap.cta1":   "See applicable courses →",
    "roadmap.cta2":   "💬 Click here to message our Fanpage for a personalised plan →",

    "book.eyebrow":   "📚 Free for the community · 2026",
    "book.read.en":   "Read in English →",
    "book.read.vi":   "Read in Vietnamese",
    "book.why":       "Why read it?",
    "book.why.intro": "Distilled from hundreds of interview rounds — on both sides of the table, as candidates and interviewers, at TikTok, Grab, and other Big Tech.",
    "book.chapters":  "44 chapters — organised by pattern",
    "book.chapters.intro":
      "Each chapter includes: goals, when to use, code template, end-of-chapter practice, and 6+ classic LeetCode problems with full solutions.",
    "book.final.head": "Ready to train algorithms by pattern?",
    "book.final.body.html":
      'The book is <strong>100% free</strong> for the community. If you find it useful, message our Fanpage to support — donations from <strong>$20</strong> also unlock the exclusive 10-video <em>Career & Interview Hack</em> series.',
    "book.final.cta1": "Open the book on GitHub Pages →",
    "book.final.cta2": "Message Fanpage to support ❤",

    "resources.head":   "Interview Resources",
    "resources.badge":  "FREE",
    "resources.intro":  "Free resources — click each group (CV kit, HR checklist, PIP Big Tech, CS Fundamentals, Golang, Programming Foundation) to expand.",
    "resources.searchPh": "Search resources… (e.g. CV, STAR, Golang)",
    "resources.expand":   "Expand all",
    "resources.collapse": "Collapse all",
    "resources.empty":    "No resource groups match.",
    "resources.expandOne":  "Expand",
    "resources.collapseOne": "Collapse",
    "resources.hr.kicker": "✅ CHECKLIST · HR PHONE SCREEN",
    "resources.hr.head": "HR / Recruiter call — don't fail the \"easy\" round",
    "resources.hr.sub": "A 20–30 minute call before technical — often judged subjectively if you're under-prepared.",
    "resources.hr.intro": "Many candidates drop out early not because of coding, but because HR/recruiters probe self-intro, behaviour, project depth, and motivation — and sense you don't own your work or aren't genuinely interested in the company. Click each item to expand tips.",
    "resources.hr.searchPh": "Search checklist… (e.g. STAR, motivation, project)",
    "resources.hr.expand":   "Expand all",
    "resources.hr.collapse": "Collapse all",
    "resources.hr.empty":    "No items match.",
    "resources.hr.item1.title": "Tell me about yourself",
    "resources.hr.item1.why": "Opening ~90 seconds – 2 minutes — HR decides whether to push you to the next round.",
    "resources.hr.item1.t1": "Present → Past → Future: current role, quantified highlights, why this role/company.",
    "resources.hr.item1.t2": "Don't read your CV line by line; close with “That's why I'm excited about …”.",
    "resources.hr.item1.t3": "Practice out loud — avoid overly long monologues.",
    "resources.hr.item2.title": "Behavioural / situational (STAR)",
    "resources.hr.item2.why": "HR often asks about conflict, failure, leadership, deadlines — how you behave at work.",
    "resources.hr.item2.t1": "Prepare enough behavioural stories: conflict, mistake, influence without authority, tight deadline, disagreement.",
    "resources.hr.item2.t2": "Tight STAR: Situation → Task → Action (what you did) → Result (metrics if possible).",
    "resources.hr.item2.t3": "Avoid endless “we did…” — recruiters need your personal signal.",
    "resources.hr.item3.title": "Past projects — prove you know your work",
    "resources.hr.item3.why": "HR/recruiters often drill CV projects to catch resume inflation.",
    "resources.hr.item3.t1": "Pick recent projects: problem, your scope, trade-offs, outcome, stack — explain without slides.",
    "resources.hr.item3.t2": "Walk through flow / architecture at a high level; be ready to justify a technical decision you owned.",
    "resources.hr.item3.t3": "Team projects — spell out your slice; don't claim the whole team's credit.",
    "resources.hr.item4.title": "Motivation — why company / why role",
    "resources.hr.item4.why": "Vague motivation reads as “applying everywhere”.",
    "resources.hr.item4.t1": "Research specifics: product, culture/values, role scope — not just “big company”.",
    "resources.hr.item4.t2": "Tie motivation to your medium-term career goal.",
    "resources.hr.item4.t3": "Don't trash your current employer; comp is only part of the answer.",
    "resources.hr.item5.title": "Logistics & professionalism",
    "resources.hr.item5.why": "HR also screens practical fit — timeline, package, next steps.",
    "resources.hr.item5.t1": "Know notice period, desired salary range (or “open depending on package”), work authorization if applying abroad.",
    "resources.hr.item5.t2": "Prepare questions back: process, team structure, timeline of next rounds.",
    "resources.hr.item5.t3": "Test mic/line; quiet space; CV + JD open in front of you.",
    "resources.hr.item6.title": "After the call",
    "resources.hr.item6.why": "Small iterations compound — even if you pass HR screen.",
    "resources.hr.item6.t1": "Note questions HR asked → refine stories / pitch for next time.",
    "resources.hr.item6.t2": "Short thank-you same day (optional but boosts impression).",
    "resources.hr.promo.badge": "Recommended course",
    "resources.hr.promo.head": "Behaviour Interview Course — practice what HR actually asks",
    "resources.hr.promo.text": "12 live sessions: self-intro, common behavioural questions, leadership principles & STAR in English — the format many Big Tech companies use from recruiter screen through onsite behavioural.",
    "resources.hr.promo.cta": "View Behaviour Interview course →",
    "resources.hr.promo.consult": "Message us for path consultation →",
    "resources.pip.kicker": "⚠️ GUIDE · PIP BIG TECH",
    "resources.pip.head": "How to handle PIP — Axon, Grab, TikTok, Shopee, Nvidia, Google, Amazon…",
    "resources.pip.sub": "Escaping PIP rarely works — prioritize negotiating mutual severance (e.g. N+1, N+2 months of pay) in your favor.",
    "resources.pip.intro": "A Performance Improvement Plan (PIP) at Big Tech is usually a step toward offboarding, not a fair shot to save your job. EngineerPro recommends focusing on a clean exit package, protecting your reputation, and runway for your next search — rather than betting on a short-window turnaround.",
    "resources.pip.searchPh": "Search PIP guide… (e.g. severance, RSU, garden leave)",
    "resources.pip.expand": "Expand all",
    "resources.pip.collapse": "Collapse all",
    "resources.pip.empty": "No items match.",
    "resources.pip.item1.title": "What a Big Tech PIP really is",
    "resources.pip.item1.why": "Google, Amazon, Meta, TikTok, Shopee, Grab, Nvidia, Axon… share a similar frame: measurable goals, weekly check-ins, final call from manager + HR.",
    "resources.pip.item1.namesIntro": "Same idea (formal performance coaching, often leading to exit) — different names by company:",
    "resources.pip.item1.n1": "Amazon: Focus (stage 1) → Pivot if you don't pass Focus",
    "resources.pip.item1.n2": "TikTok / ByteDance: Formal Coaching",
    "resources.pip.item1.n3": "Google: Performance Improvement Plan (PIP)",
    "resources.pip.item1.n4": "Meta: Performance Improvement Plan (PIP)",
    "resources.pip.item1.n5": "Microsoft: Performance Improvement Plan",
    "resources.pip.item1.n6": "Nvidia: Performance Improvement Plan (PIP) / performance coaching track",
    "resources.pip.item1.n7": "Apple: Performance Improvement Plan",
    "resources.pip.item1.n8": "Shopee / Grab: Performance Improvement Plan (often called PIP)",
    "resources.pip.item1.n9": "Axon & many other US tech firms: PIP or Performance Coaching",
    "resources.pip.item1.t1": "PIP = documented performance process that reduces legal risk when the company terminates.",
    "resources.pip.item1.t2": "Managers often already had a “does not meet bar” signal — PIP formalizes the last step, not a surprise reset.",
    "resources.pip.item1.t3": "Pass rates after PIP are often very low; don't plan your finances assuming you'll pass.",
    "resources.pip.item2.title": "Why “getting off PIP” is extremely hard",
    "resources.pip.item2.why": "Short timelines (often weeks to two review cycles) + high bar + confirmation bias — you must overturn an existing perception.",
    "resources.pip.item2.t1": "PIP goals usually tie to missed delivery — hard to prove turnaround in a narrow window.",
    "resources.pip.item2.t2": "Stakeholders rarely want to re-bet on flagged headcount; hiring freezes and promo cuts make PIP passes rarer.",
    "resources.pip.item2.t3": "Best use of energy: a controlled exit — don't burn bridges or sign anything you don't understand.",
    "resources.pip.item3.title": "Strategy #1: Mutual separation / severance",
    "resources.pip.item3.why": "Negotiating a mutual separation package is often better than failing PIP and being terminated for cause.",
    "resources.pip.item3.severanceHead": "What do N+1, N+2 mean?",
    "resources.pip.item3.severanceN": "N = years you have worked at the company (tenure; HR often rounds per internal policy).",
    "resources.pip.item3.severanceFormula": "N+1, N+2… = total months of salary paid as severance on exit, usually based on base salary — not “one more year of employment”.",
    "resources.pip.item3.severanceExample": "Example: 3 years at the company → N = 3. An N+1 package = 4 months of pay; N+2 = 5 months (lump sum or paid in installments).",
    "resources.pip.item3.severanceNote": "Actual months depend on level, entity (US/SG/VN), and negotiation leverage — each company has its own framework.",
    "resources.pip.item3.t1": "Goal: a “clean” exit — employment record without performance termination; runway and cash buffer.",
    "resources.pip.item3.t2": "Negotiation frame: ask for severance in months of pay using N+1, N+2… (see above), not statutory minimum only.",
    "resources.pip.item3.t3": "Also ask for: pro-rated bonus, PTO payout, healthcare bridge, garden leave, outplacement, reference wording.",
    "resources.pip.item4.title": "Package checklist to negotiate",
    "resources.pip.item4.why": "HR has a playbook — you need your own checklist; don't stare at one “severance months” line.",
    "resources.pip.item4.t1": "Cash: base severance (e.g. N+1 / N+2 months of pay, N = years of tenure), signing bonus clawback waiver, unpaid bonus cycle, relocation repayment waiver.",
    "resources.pip.item4.t2": "Equity: unvested RSU/ESOP — partial accelerated vesting, extended exercise window, or mutual-leave treatment (grant & policy dependent).",
    "resources.pip.item4.t3": "Benefits & time: COBRA/health subsidy, paid garden leave, unused PTO, balanced non-compete / non-disparagement.",
    "resources.pip.item4.t4": "Reputation: reference check wording, title on paper, internal LinkedIn-friendly departure narrative.",
    "resources.pip.item5.title": "Before the HR / People Partner meeting",
    "resources.pip.item5.why": "The first meeting sets leverage — prepare like a negotiation, not a plea.",
    "resources.pip.item5.t1": "Read the PIP letter, handbook, equity plan, offer letter — note deadlines, metrics, sign-off chain.",
    "resources.pip.item5.t2": "Gather context: tenure, level, prior reviews, reorg, health/family if relevant (don't overshare), market comp.",
    "resources.pip.item5.t3": "Define your BATNA: minimum mutual exit package; who can approve (HRBP, comp, legal).",
    "resources.pip.item5.t4": "Send a written proposal after the meeting — no verbal yes; ask days to review with counsel/advisor if needed.",
    "resources.pip.item6.title": "Absolute don'ts",
    "resources.pip.item6.why": "One mistake can wipe severance leverage or trigger immediate termination.",
    "resources.pip.item6.t1": "Signing the separation agreement in the room — always take it home; at least 48-72 hours to review.",
    "resources.pip.item6.t2": "Emotional outbursts, company-wide email CCs, Slack drama — the company will document “conduct”.",
    "resources.pip.item6.t3": "Rage-quitting before a deal — you often lose severance and get worse equity treatment.",
    "resources.pip.item6.t4": "Posting internal details on social media — policy violation + harder negotiation.",
    "resources.pip.item7.title": "After the deal — switch to job hunt",
    "resources.pip.item7.why": "A good package only matters if you use the runway to land the right next offer.",
    "resources.pip.item7.t1": "Update CV + LinkedIn with neutral framing (“team restructure / mutual separation”) — aligned with agreed references.",
    "resources.pip.item7.t2": "Prioritize behavioural mocks + system/DSA for Big Tech targets — see HR checklist & Behaviour Interview course.",
    "resources.pip.item7.t3": "Warm intros beat cold apply; get mentor review on stories before onsite.",
    "resources.pip.promo.badge": "On a PIP — need private guidance?",
    "resources.pip.promo.head": "Book a 1-1 consult via Fanpage",
    "resources.pip.promo.text": "If you're on a PIP and need help with negotiation / severance, message EngineerPro on Fanpage to schedule a consult. Policies differ by entity (US / SG / VN) — we help with strategy, HR scripts, and post-exit planning; not a substitute for employment counsel.",
    "resources.pip.promo.consult": "Message Fanpage to book a consult →",
    "resources.cs.kicker": "🧠 CS FUNDAMENTALS · REAL INTERVIEW QUESTIONS",
    "resources.cs.head": "~100 real CS Fundamental interview questions — crawled from LeetCode Discuss",
    "resources.cs.sub": "Real questions from LeetCode Discuss + live CS Fundamental Interview course (12 sessions on Zoom).",
    "resources.cs.intro.html": "Free list from <a href=\"https://leetcode.com/discuss/\" target=\"_blank\" rel=\"noopener\">LeetCode Discuss</a> — non-coding questions (OS, networking, DB…) with company &amp; role/location context. For structured prep + Big Tech-style mock → <a href=\"/courses/computer-science-fundamental-interview/\">CS Fundamental Interview course</a> (12 live sessions on Zoom).",
    "resources.cs.footer.html": "Want coached answers + mentor feedback? <a href=\"/courses/computer-science-fundamental-interview/\">Enroll in CS Fundamental Interview →</a>",
    "resources.cs.searchPh": "Search questions… (e.g. TCP, deadlock, ACID, thread)",
    "resources.cs.topicAll": "All topics",
    "resources.cs.expand": "Expand all",
    "resources.cs.collapse": "Collapse all",
    "resources.cs.empty": "No questions match.",
    "resources.cs.promo.badge": "EngineerPro course · CS Fundamentals",
    "resources.cs.promo.head": "Computer Science Fundamental Interview — 12 live Zoom sessions",
    "resources.cs.promo.text": "The free list below shows what Big Tech asks — the live Zoom course teaches you how to answer: OS, networking, DB, concurrency, OOP, browser/HTTP… technical screen / CS round format.",
    "resources.cs.promo.cta": "View & enroll CS Fundamentals →",
    "resources.cs.promo.consult": "Message Fanpage for a roadmap consult →",
    "resources.formats.kicker": "📋 CHEATSHEET · INTERVIEW FORMAT",
    "resources.formats.head": "Interview format by company — Amazon, Google, Meta, Grab, Axon…",
    "resources.formats.sub": "14 companies · from EngineerPro cheatsheet V2 — reference only.",
    "resources.formats.intro": "Each company/team/location may change rounds, order, and difficulty over time. Use this as a prep guide — not a fixed playbook.",
    "resources.formats.disclaimer.title": "⚠️ Reference format only",
    "resources.formats.disclaimer.body": "Actual process depends on team, hiring manager, location, and timing. Some companies (Amazon, Nvidia, Shopee, Google, Axon, TikTok…) note that teams may differ.",
    "resources.formats.dsaNote": "Big Tech / rich tech: aim for at least LeetCode Medium on DSA topics.",
    "resources.formats.searchPh": "Search company, level, round… (e.g. Amazon LP, Google L4, Axon CS)",
    "resources.formats.companyAll": "All companies",
    "resources.formats.expand": "Expand all",
    "resources.formats.collapse": "Collapse all",
    "resources.formats.empty": "No company/level matches.",
    "resources.formats.footer.html": "Want company-specific mock + mentor feedback? <a href=\"/mock/\">Book Mock Interview 1-1 →</a> or browse <a href=\"/courses/\">EngineerPro live courses</a>.",
    "resources.formats.reco.title": "Recommended EngineerPro courses",
    "resources.formats.reco.mock": "Mock Interview 1-1",
    "resources.foundation.kicker": "📺 PLAYLIST · YOUTUBE",
    "resources.foundation.cta":    "Open full playlist ↗",
    "resources.golangTour.kicker": "📺 PLAYLIST · YOUTUBE",
    "resources.golangTour.cta":    "Open full playlist ↗",
    "resources.cv.kicker": "📄 CV WRITING TOOLKIT",
    "resources.cv.head":   "Write a Big Tech-ready CV",
    "resources.cv.sample.kicker": "★ SAMPLE CV — PASSED GOOGLE",
    "resources.cv.sample.b1": "1 page, clean layout, ATS-friendly",
    "resources.cv.sample.b2": "X-Y-Z bullet format — action · context · impact",
    "resources.cv.sample.b3": "Concrete numbers (latency, scale, savings)",
    "resources.cv.sample.b4": "Skills section concise, no keyword spam",
    "resources.cv.sample.cta": "Open full CV on Drive ↗",
    "resources.cv.overleaf.kicker": "1 · LaTeX Template",
    "resources.cv.overleaf.cta":    "Open in Overleaf ↗",
    "resources.cv.review.kicker":   "2 · CV Review Playlist",
    "resources.cv.tool.kicker":     "3 · Quick tool video",
    "resources.cv.tool.cta":        "Watch on YouTube ↗",

    "partners.head":  "Partners",
    "partners.intro": "EngineerPro collaborates with organisations sharing the same mission to bring Vietnamese engineers into Big Tech.",
    "partners.soon.html":
      'Are you an organisation interested in partnering? <a href="https://m.me/EngineerPro.Official" target="_blank" rel="noopener">Message our Fanpage →</a>',
    "partners.strip.tag":  "PARTNER",
    "partners.strip.text.html":
      'Meet <strong>MentorPro</strong> — a 1-on-1 mentoring program for those breaking into Big Tech',
    "partners.strip.cta":  "Read more →",

    "faq.head":      "FAQ",
    "faq.intro.html":
      '<span id="faqCount">6</span> most common questions — click each to expand. Quick search in the box below.',
    "faq.searchPh":  "Search FAQ… (e.g. English, backend, roadmap)",
    "faq.expand":    "Expand all",
    "faq.collapse":  "Collapse all",
    "faq.empty":     "No questions match.",
    "faq.terms.cta": "Read our terms of service →",

    "terms.head":  "Terms of Service",
    "terms.intro": "EngineerPro's commitments & policies for our students — please read carefully before enrolling.",
    "terms.body.html":
      '<h3>1. Course delivery commitment</h3>' +
      '<p>Courses you enroll in with <strong>EngineerPro</strong> will be delivered in full and as advertised. We are responsible for the quality and pace of every course we publish.</p>' +
      '<h3>2. Ownership of learning materials</h3>' +
      '<p>All learning materials, including but not limited to recorded videos and documents, are the <strong>intellectual property of EngineerPro</strong>. EngineerPro reserves the right to revoke or stop providing these materials at any time. Sharing, copying, or distributing materials outside the classroom in any form is <strong>strictly prohibited</strong>. Materials (including recordings) are only provided to support students who miss a session.</p>' +
      '<h3>3. Use of learning materials</h3>' +
      '<p>Students commit to using EngineerPro materials <strong>for study purposes only</strong>. Misuse — including copying, sharing outside the classroom, or repurposing without permission — is considered a breach. In that case, EngineerPro reserves the right to revoke access and refuse further services without refund.</p>' +
      '<h3>4. Community services</h3>' +
      '<p>EngineerPro community services — <strong>CV review, job-search support, material sharing, Alumni access</strong> — are <strong>free of charge</strong> and are not part of the course fee. EngineerPro may pause or stop these services if they no longer fit community needs, and reserves the right to refuse service in case of conflict of interest.</p>' +
      '<h3>5. Course freeze / deferral policy</h3>' +
      '<p>EngineerPro <strong>does not generally support course freezing</strong>. In special cases, the team may review and approve a freeze. The final decision rests with EngineerPro and may be declined if deemed unreasonable.</p>' +
      '<h3>6. Alumni & Internal Tech Talk policy</h3>' +
      '<p>EngineerPro Alumni and Internal Tech Talk are platforms where mentors and students support each other and grow careers after the course. All Alumni members have the right and the duty to help build the community. EngineerPro reserves the right to refuse participation for <strong>unconstructive behavior or conflict of interest</strong>.</p>' +
      '<h3>7. Refunds & deposit / tuition transfer</h3>' +
      '<h4>a. Refund policy</h4>' +
      '<p>We deliver quality and always do our best to meet expectations. We recognize unexpected situations happen, so please read the policy below carefully.</p>' +
      '<p><strong>No refund under any circumstance</strong> (except when the course is cancelled by EngineerPro) — students cannot request a refund of tuition or deposit. This applies to all courses.</p>' +
      '<h4>b. Transferring deposit / tuition to another course</h4>' +
      '<p>Students may transfer paid deposit/tuition to a different course under the following conditions:</p>' +
      '<ul>' +
      '<li>Request must be made <strong>at least 5 days before the start date</strong> of the enrolled course.</li>' +
      '<li>Up to <strong>2 transfer requests</strong> per student.</li>' +
      '<li>Transfers depend on seat availability and curriculum at the time of request.</li>' +
      '<li>If the new course is <strong>more expensive</strong>, the student pays the difference. If <strong>cheaper</strong>, the difference is not refunded.</li>' +
      '<li>Any transfer fee (if applicable) must be paid before the transfer is finalized.</li>' +
      '</ul>' +
      '<h4>c. When transfer is NOT allowed</h4>' +
      '<ul>' +
      '<li>Student unilaterally cancels or requests transfer <strong>after the course has started</strong>.</li>' +
      '<li>Student does not attend due to personal reasons without prior notice.</li>' +
      '<li>Student violates EngineerPro policies / terms of service.</li>' +
      '<li>Student misses sessions without valid reason.</li>' +
      '</ul>' +
      '<h4>d. Transfer request process</h4>' +
      '<ol>' +
      '<li>Submit request via <strong>email or fanpage</strong> at least <strong>5 days before the start date</strong>.</li>' +
      '<li>Include a specific reason and supporting information.</li>' +
      '<li>EngineerPro responds within <strong>2 days</strong> with the decision.</li>' +
      '</ol>' +
      '<h4>e. Final decision</h4>' +
      '<p>EngineerPro reserves the right to the final decision on refunds and transfers, case by case.</p>' +
      '<p class="terms-callout"><strong>Important:</strong> Refund and deferral requests are reviewed case-by-case under the policy above.</p>',

    "contact.head":  "Contact",
    "contact.intro": "Reach out to us for any questions or path consultation.",
    "contact.cta.email":     "Send email →",
    "contact.cta.messenger": "Chat now →",
    "contact.cta.facebook":  "Follow our Fanpage →",
    "contact.cta.zalo":      "Open Zalo →",
    "contact.cta.spotify":   "Listen on Spotify →",
    "contact.cta.youtube":   "Watch videos →",
    "contact.cta.substack":  "Read & listen →",
    "contact.cta.viblo":     "Read articles →",

    "cta.fab.messenger": "Book consultation via FB Messenger",
    "cta.fab.zalo":      "Book consultation via Zalo",

    "footer.tag":  "Conquering Big Tech Marvels.",
    "footer.col1": "Learn",
    "footer.col2": "Community",
    "footer.col3": "Support",
    "footer.col4": "Partners",
    "footer.link.roadmap":   "Interview roadmap",
    "footer.link.courses":   "Courses",
    "footer.link.book":      "Coding Book",
    "footer.link.resources": "Free resources",
    "footer.link.format":    "Learning format",
    "footer.link.mentors":   "Mentors",
    "footer.link.stories":   "Success Stories",
    "footer.link.podcast":   "Podcast",
    "footer.link.faq":       "FAQ",
    "footer.link.terms":     "Terms of Service",
    "footer.link.mock":      "Mock Interview 1-1",
    "footer.link.contact":   "Contact",
    "footer.link.messenger": "Messenger",
    "footer.link.allPartners": "All partners",
    "footer.fanpage.head":   "Fanpage",

    // ============== MOCK INTERVIEW 1-1 ==============
    "mock.head":         "Mock Interview 1-1",
    "mock.intro.html":
      "A 1-1 mock with <strong>interviewers from the EngineerPro team</strong> — practise the actual Big Tech interview style (Google, Meta, TikTok, Amazon, Microsoft, Nvidia, WorldQuant, Axon…). Mock language is <strong>VI or EN</strong> — your choice at booking time.",
    "mock.sd.kicker":    "🏗 SYSTEM DESIGN",
    "mock.sd.title":     "Mock System Design",
    "mock.sd.body":      "Live system-design session with an interviewer — clarify requirements, high-level design, deep-dive a component, trade-offs, scale-up. Feedback against the Big Tech signal rubric for each level (mid / senior / staff).",
    "mock.dsa.kicker":   "💻 DSA / CODING",
    "mock.dsa.title":    "Mock DSA / Coding Interview",
    "mock.dsa.body":     "Big-Tech-style coding interview: clarify → brainstorm → code → debug → complexity analysis. Interviewer drills edge cases and grades communication + clean-code habits.",
    "mock.beh.kicker":   "🎤 BEHAVIORAL",
    "mock.beh.title":    "Mock Behavioral Interview",
    "mock.beh.body":     "Practise behavioural questions using the STAR framework + Leadership Principles (Amazon, Meta, Google style). Mock in English, feedback on story-telling, strong / weak signals, and specificity.",
    "mock.beh.note":     "Message the Fanpage to request the demo video (internal — not public).",
    "mock.demo.watch":   "▶ Watch demo on YouTube ↗",
    "mock.who.title":    "Who is this for?",
    "mock.who.b1":       "SWEs preparing for a Big Tech onsite who want to rehearse a few weeks before the real interview.",
    "mock.who.b2":       "EngineerPro students after the DSA / System Design / Behavioral courses who want to benchmark before applying.",
    "mock.who.b3":       "Anyone who has never interviewed at Big Tech and wants a low-pressure run-through before the real day.",
    "mock.session.title": "What you get from each 1-1 mock",
    "mock.session.b1":   "45–60 minutes 1-1 mock on Zoom (recorded so you can re-watch).",
    "mock.session.b2":   "Detailed feedback against the Big Tech rubric — not generic comments.",
    "mock.session.b3":   "Concrete suggestions for what to improve before the next mock / real interview.",
    "mock.session.b4":   "Bonus tips on negotiation, story-telling, post-onsite follow-up emails.",
    "mock.bigtech.title": "Mock in the style of Big Tech",
    "mock.bigtech.list": "Google · Meta · TikTok · Amazon · Microsoft · Nvidia · WorldQuant · Axon · Apple · Citadel",
    "mock.bigtech.note": "EngineerPro interviewers have actually gone through the interview loops at these companies — mock with the right format, the right signals, the right level.",
    "mock.cta.primary":  "💬 Message our Fanpage to book a 1-1 mock →",
    "mock.cta.zalo":     "Or book via Zalo 0352 911 223 →",
    "mock.book.title":   "📅 How to book your 1-1 mock",
    "mock.book.body.html":
      "To book a mock session, please <strong>message the EngineerPro Fanpage</strong>. The team will reply within 24 hours to confirm <strong>topic, level, language (VI / EN) and a time slot</strong> that works for you.",
  },
};
