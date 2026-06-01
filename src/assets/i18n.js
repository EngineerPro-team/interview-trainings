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

    "podcast.head": "Podcast",
    "podcast.intro.html":
      '<span id="podcastCount">12</span> latest episodes — click to listen on <a href="https://engineerprovn.substack.com/podcast/archive?sort=new" target="_blank" rel="noopener">Substack</a>.',
    "podcast.card.cta": "Listen on Substack →",

    "roadmap.eyebrow": "📍 Interview roadmap · Big Tech",
    "roadmap.title.html":
      'From <span class="grad">fresher</span> to <span class="grad">Big Tech offer</span><br />in 3 clear stages.',
    "roadmap.extras.title": "Alongside the main path",
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
    "footer.link.contact":   "Contact",
    "footer.link.messenger": "Messenger",
    "footer.link.allPartners": "All partners",
    "footer.fanpage.head":   "Fanpage",
  },
};
