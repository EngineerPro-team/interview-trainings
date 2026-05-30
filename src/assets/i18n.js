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
      "100% giảng viên đến từ Google, Amazon, TikTok, Shopee, Uber, Spotify… Lộ trình rõ ràng từ fresher đến senior. Học live trên Zoom trong <strong>lớp nhỏ 15–20 học viên</strong>, hỗ trợ 24/7 trên Discord.",
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
      '<span id="mentorsCount">18</span> mentor đang làm việc tại Google, Amazon, Meta, TikTok, Spotify, Shopee, Acronis, AWS… Bấm vào nút LinkedIn để xem profile.',
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

    // ============== PODCAST ==============
    "podcast.head": "Podcast",
    "podcast.intro.html":
      '<span id="podcastCount">12</span> tập gần nhất — bấm vào để nghe trực tiếp trên <a href="https://engineerprovn.substack.com/podcast/archive?sort=new" target="_blank" rel="noopener">Substack</a>.',
    "podcast.card.cta": "Nghe trên Substack →",

    // ============== ROADMAP ==============
    "roadmap.eyebrow": "📍 Lộ trình ôn thi · Big Tech",
    "roadmap.title.html":
      'Từ <span class="grad">fresher</span> đến <span class="grad">Big Tech offer</span><br />trong 3 giai đoạn rõ ràng.',
    "roadmap.source":  "Đọc bản gốc trên Substack ↗",
    "roadmap.extras.title": "Song song với lộ trình chính",
    "roadmap.benefits.head": "Khi là học viên EngineerPro, bạn nhận được gì?",
    "roadmap.cta1":   "Xem khoá học áp dụng →",
    "roadmap.cta2":   "Nhắn fanpage tư vấn lộ trình cá nhân",

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
    "resources.intro":  "Bộ tài nguyên miễn phí team EngineerPro share cho cộng đồng — video nền tảng lập trình, template CV chuẩn Big Tech, và playlist review CV thực tế.",
    "resources.foundation.kicker": "📺 PLAYLIST · YOUTUBE",
    "resources.foundation.cta":    "Mở full playlist ↗",
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
      '<span id="faqCount">8</span> câu hỏi phổ biến nhất — bấm vào từng câu để xem trả lời. Có thể search nhanh ở khung bên dưới.',
    "faq.searchPh":  "Tìm trong FAQ… (vd: tiếng Anh, backend, lộ trình)",
    "faq.expand":    "Mở tất cả",
    "faq.collapse":  "Thu gọn",
    "faq.empty":     "Không tìm thấy câu hỏi nào khớp.",

    // ============== CONTACT ==============
    "contact.head":  "Liên hệ",
    "contact.intro": "Hãy liên hệ với chúng tôi để được giải đáp thắc mắc và tư vấn lộ trình.",
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
    "footer.link.contact":   "Liên hệ",
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
      "100% mentors from Google, Amazon, TikTok, Shopee, Uber, Spotify… A clear path from fresher to senior. Live Zoom sessions in <strong>small classes of 15–20 students</strong>, with 24/7 Discord support.",
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
      '<span id="mentorsCount">18</span> mentors currently at Google, Amazon, Meta, TikTok, Spotify, Shopee, Acronis, AWS… Click LinkedIn to see their profile.',
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

    "podcast.head": "Podcast",
    "podcast.intro.html":
      '<span id="podcastCount">12</span> latest episodes — click to listen on <a href="https://engineerprovn.substack.com/podcast/archive?sort=new" target="_blank" rel="noopener">Substack</a>.',
    "podcast.card.cta": "Listen on Substack →",

    "roadmap.eyebrow": "📍 Interview roadmap · Big Tech",
    "roadmap.title.html":
      'From <span class="grad">fresher</span> to <span class="grad">Big Tech offer</span><br />in 3 clear stages.',
    "roadmap.source":  "Read the original on Substack ↗",
    "roadmap.extras.title": "Alongside the main path",
    "roadmap.benefits.head": "What you get as an EngineerPro student",
    "roadmap.cta1":   "See applicable courses →",
    "roadmap.cta2":   "Message Fanpage for a personalised plan",

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
    "resources.intro":  "Free resources the EngineerPro team shares with the community — programming foundation videos, Big Tech CV templates, and a real CV review playlist.",
    "resources.foundation.kicker": "📺 PLAYLIST · YOUTUBE",
    "resources.foundation.cta":    "Open full playlist ↗",
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
      '<span id="faqCount">8</span> most common questions — click each to expand. Quick search in the box below.',
    "faq.searchPh":  "Search FAQ… (e.g. English, backend, roadmap)",
    "faq.expand":    "Expand all",
    "faq.collapse":  "Collapse all",
    "faq.empty":     "No questions match.",

    "contact.head":  "Contact",
    "contact.intro": "Reach out to us for any questions or path consultation.",
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
    "footer.link.contact":   "Contact",
    "footer.link.messenger": "Messenger",
    "footer.link.allPartners": "All partners",
    "footer.fanpage.head":   "Fanpage",
  },
};
