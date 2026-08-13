#!/usr/bin/env python3
"""Build the self-contained Gumroad custom landing pages for the two e-books.

Each Gumroad product page can carry its own landing page, and a landing page
REPLACES the whole product page (native price and "I want this!" button
included), so every generated file has to ship its own buy elements.

Both books get the same design system and layout; only the copy, the hero
visual and which book is the lead swap over. Output:

    landing.html                 -> product "Forty-Seconds-Ten-Real-CVs-That-Passed-Big-Tech"
    landing-cafe-talk.html       -> product "cafe-talk-the-interview-and-career-playbook"

Run: python3 scripts/gumroad_landing/build.py
"""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

STORE = "https://engineerprovn.gumroad.com"

# Cover art served from Gumroad's own file host. Other image hosts are blocked
# inside the sandboxed landing page, so these two URLs are the only art we can use.
COVER_FORTY = "https://public-files.gumroad.com/0crfr93vbfu6wwshh93d84mqku45"
COVER_CAFE = "https://public-files.gumroad.com/kito51ojyindwee0h337iiu00tdo"

# The "EngineerProAug" offer code takes $5 off and auto-applies at checkout, so
# data-gumroad-field="price" already resolves to the discounted figure. The list
# price is shown struck through next to it. Retire the code -> set OFFER to None
# and rerun this script.
OFFER = {"amount": "$5", "code": "EngineerProAug"}

SLUG_FORTY = "Forty-Seconds-Ten-Real-CVs-That-Passed-Big-Tech"
SLUG_CAFE = "cafe-talk-the-interview-and-career-playbook"


# --------------------------------------------------------------------------- #
# Hero visuals
# --------------------------------------------------------------------------- #

INSIDE_ART_FORTY = """        <div class="scan" aria-hidden="true">
          <div class="scan__stack">
            <div class="scan__sheet">
              <div class="cvline cvline--head"></div>
              <div class="cvline cvline--sub"></div>
              <p class="cvsec">Experience</p>
              <div class="cvline cvline--w90"></div>
              <div class="cvline cvline--w80"></div>
              <div class="cvline cvline--w65"></div>
              <p class="cvsec">Projects</p>
              <div class="cvline cvline--w80"></div>
              <div class="cvline cvline--w90"></div>
              <p class="cvsec">Skills</p>
              <div class="cvline cvline--w40"></div>
            </div>
            <p class="scan__timer">00:40 — người lạ đọc CV của bạn</p>
          </div>
        </div>
        <p class="inside-art__cap">
          Không ai đọc CV theo thứ tự bạn viết. Chương đầu tiên vẽ lại đường đi thật của mắt
          người đọc, và ba hệ quả của nó lên bố cục.
        </p>"""


def _row(name, value, fill, mark, miss=False):
    cls = " row--miss" if miss else ""
    return f"""              <div class="row{cls}">
                <div class="row__top">
                  <span class="row__name">{name}</span>
                  <span class="row__val">{value}</span>
                </div>
                <div class="row__bar" aria-hidden="true">
                  <div class="row__fill" style="width:{fill}%"></div>
                  <div class="row__mark" style="left:{mark}%"></div>
                </div>
              </div>"""


INSIDE_ART_CAFE = """        <div class="card">
          <div class="card__stack">
            <div class="card__sheet">
              <p class="card__title">Phiếu đánh giá · vòng onsite</p>
              <p class="card__lvl">Ứng viên đề xuất level L5</p>
{rows}
              <p class="card__rule">
                Nguyên tắc <b>làm tròn xuống</b>: mỗi mục có ngưỡng tối thiểu riêng cho từng level.
                Chỉ cần một mục rơi xuống dưới ngưỡng là cả buổi bị kéo theo.
              </p>
            </div>
            <p class="card__verdict">Kết quả: L4</p>
          </div>
        </div>
        <p class="inside-art__cap">
          Bốn vòng đều đạt vẫn có thể rớt level. Chương về phiếu đánh giá giải thích vì sao,
          và mục nào thường là mục kéo cả buổi xuống.
        </p>""".replace(
    "{rows}",
    "\n".join(
        [
            _row("Thuật toán", "đạt", 84, 68),
            _row("Thiết kế hệ thống", "đạt", 76, 68),
            _row("Kiến thức nền", "đạt", 72, 68),
            _row("Giao tiếp", "dưới ngưỡng", 52, 68, miss=True),
        ]
    ),
)


# --------------------------------------------------------------------------- #
# Per-book content
# --------------------------------------------------------------------------- #

FORTY = {
    "slug": SLUG_FORTY,
    "css": "hero-forty-seconds.css",
    "lang_title": "Forty Seconds: Ten Real CVs That Passed Big Tech | EngineerPro",
    "name_fallback": "Forty Seconds",
    "price_fallback": "$14.99",
    "list_price": "$19.99",
    # the real book title, never a Vietnamese rendering of it
    "hero_h1": 'Forty Seconds<br /><em>Ten Real CVs That Passed Big Tech</em>',
    "hero_sub": (
        "Vòng đầu tiên không có ai phỏng vấn bạn. Chỉ có một tờ giấy, và một người lạ đọc nó "
        "trong bốn mươi giây. Đây là vòng đánh trượt nhiều người nhất, và gần như không ai được "
        "biết vì sao mình trượt. Cuốn sách mổ xẻ mười CV thật đã qua được vòng đó — trích nguyên "
        "văn tiếng Anh, kèm phân tích vì sao qua và chỗ nào còn rủi ro."
    ),
    "inside_art": INSIDE_ART_FORTY,
    "cover_pill": "10 CV thật · từ intern tới staff",
    "price_note": "Đang giảm $5 — mã <code>EngineerProAug</code> tự động áp ở bước thanh toán, bạn không phải nhập gì. Tải PDF ngay sau khi mua.",
    "chips": [
        "10 CV thật, không phải mẫu",
        "Đã qua vòng loại tại 14 công ty",
        "PDF · Tiếng Việt",
    ],
    # the full list from the product description — naming all fourteen is the proof,
    # a truncated "…" list reads like a claim
    "proof": {
        "label": "Mười CV trong sách đã qua vòng loại tại",
        "items": [
            "Meta", "Google", "Amazon", "Microsoft", "NVIDIA", "Databricks", "Grab",
            "Airwallex", "Uber", "Anthropic", "xAI", "Axon", "Citadel", "WorldQuant",
        ],
    },
    "authors_note": (
        "Cả hai cùng dạy tại EngineerPro và duy trì chương trình review CV miễn phí cho "
        "cộng đồng suốt hơn ba năm qua. Phần lời khuyên trong sách rút ra từ hàng nghìn "
        "CV đã đọc ở đó."
    ),
    # the book this page is hosted on
    "self": {
        "badge": "Bạn đang ở trang này",
        "cover": COVER_FORTY,
        "cover_alt": "Bìa sách Forty Seconds: Ten Real CVs That Passed Big Tech",
        "title_html": '<span data-gumroad-field="name">Forty Seconds: Ten Real CVs That Passed Big Tech</span>',
        "meta": "PDF · 86 trang · 11 chương · Tiếng Việt",
        "blurb": (
            "Mười CV thật của kỹ sư Việt Nam đã qua vòng loại tại Meta, Google, Amazon, NVIDIA, "
            "Databricks, Anthropic, Grab, Citadel… Trích nguyên văn tiếng Anh, kèm phân tích vì "
            "sao qua được và chỗ nào còn rủi ro."
        ),
        "bullets": [
            "Ba người đọc CV của bạn — và ba câu hỏi khác nhau họ đang tìm câu trả lời",
            "Bốn mảnh của một gạch đầu dòng: động từ, quy mô, cách làm, kết quả",
            "Một hồ sơ ba năm kinh nghiệm vẫn qua được vòng senior",
            "Mười hai lỗi khiến hồ sơ bị loại, xếp theo mức thiệt hại",
            "Checklist trước khi bấm nộp + thư viện động từ theo nhóm việc",
        ],
        "price_note": "Một lượt mua = một bản sách cho một người đọc.",
        "cta": "Tôi muốn cuốn này",
    },
    # the other book, cross-sold with a plain link to its own product page
    "other": {
        "badge": "Cuốn còn lại của bộ đôi",
        "cover": COVER_CAFE,
        "cover_alt": "Bìa sách Cafe Talk: The Interview and Career Playbook",
        "title": "Cafe Talk: The Interview and Career Playbook",
        "meta": "PDF · 67 trang · 10 chương · Tiếng Việt",
        "blurb": (
            "Đúc kết từ mười buổi trò chuyện của hai kỹ sư từng ngồi cả hai phía bàn phỏng vấn — "
            "từ phòng phỏng vấn Big Tech tới ba tháng đầu, thăng tiến và những mùa cắt giảm."
        ),
        "bullets": [
            "Bốn vòng phỏng vấn cốt lõi và cách chúng thực sự được chấm",
            "Hơn nửa cuốn nói về những gì xảy ra SAU khi bạn ký hợp đồng",
            "Phần luật lao động Việt Nam dẫn điều khoản cụ thể",
            "Thử việc, thăng tiến, và việc cần làm khi bị cắt giảm",
        ],
        # effective price after the auto-applied EngineerProAug code, so this card
        # matches what the buyer sees on the Cafe Talk page itself
        "price": "$10.99",
        "list_price": "$15.99",
        "price_note": "Có trang sản phẩm riêng trên Gumroad.",
        "url": f"{STORE}/l/{SLUG_CAFE}",
        "cta": "Xem Cafe Talk",
    },
    "inside_eyebrow": "Bên trong Forty Seconds",
    "inside_h2": "Mười một chương, bốn phần",
    "inside_parts": [
        (
            "P1",
            "Vòng đầu tiên hoạt động như thế nào",
            [
                "Ba người đọc CV của bạn, ba câu hỏi khác nhau mà mỗi người đang tìm câu trả lời",
                "Bốn mươi giây và đường đi thật của mắt người đọc — vì sao không ai đọc CV theo thứ tự bạn viết",
                "Bộ khung của một CV qua vòng: bao nhiêu trang, mục nào trước mục nào",
                "Ba tình huống khó: nhảy việc, khoảng trống, bị cắt giảm",
            ],
        ),
        (
            "P2",
            "Viết từng dòng",
            [
                "Bốn mảnh của một gạch đầu dòng, kèm chuỗi câu hỏi “để làm gì” để đào một dòng xuống tới đáy",
                "Con số: bốn nhóm, và tìm chúng ở đâu khi bạn nghĩ mình chẳng có gì để đếm",
                "Cái bẫy ngược: số to quá thì người đọc không tin, và mất nhiều hơn được",
                "Phạm vi: bốn trục người đọc dùng để định cấp bậc cho bạn",
            ],
        ),
        (
            "P3",
            "Mười CV đã qua vòng",
            [
                "Mười hồ sơ thật, xếp từ intern tới staff, trích nguyên văn tiếng Anh trong khối riêng",
                "Mỗi hồ sơ kèm phân tích: vì sao qua được, chi tiết đáng học, và chỗ nào là rủi ro",
                "Một hồ sơ có chức danh mid-level nhưng nội dung nói senior",
                "Một hồ sơ lấy được phỏng vấn ở tám nơi cùng lúc",
            ],
        ),
        (
            "P4",
            "Trước khi bấm nộp + phần gom lại",
            [
                "Sửa CV theo từng công ty trong hai mươi phút",
                "Thứ mà Amazon, Meta, Google và các công ty hạ tầng thực sự đi tìm",
                "Mười hai lỗi khiến hồ sơ bị loại, xếp theo mức độ thiệt hại",
                "Checklist, thư viện động từ, mẫu câu điền sẵn cho mười tình huống hay gặp",
            ],
        ),
    ],
    "inside_note": (
        "Danh tính trong mọi hồ sơ đã được gỡ sạch: tên người, công ty, địa điểm, tên hệ thống nội bộ. "
        "Cấu trúc, giọng văn, động từ và toàn bộ con số thì giữ nguyên từng chữ."
    ),
    "demo_btn": "Xem thử một gạch đầu dòng được mổ xẻ",
    "modal": {
        "title": "Bốn mảnh của một gạch đầu dòng",
        "intro": "Cùng một việc, viết hai cách. Đây là kiểu mổ xẻ bạn sẽ thấy suốt cuốn sách.",
        "body": """    <div class="bullet">
      <p class="bullet__lbl">Trước</p>
      <p class="bullet__txt">Responsible for improving the performance of the payment service.</p>
    </div>

    <div class="bullet">
      <p class="bullet__lbl">Sau</p>
      <p class="bullet__txt">
        <mark>Cut</mark> p99 latency of the <mark>payment API (12k RPS peak)</mark>
        <mark>by batching ledger writes and adding a read-through cache</mark>,
        <mark>from 840 ms to 180 ms</mark>.
      </p>
      <div class="bullet__key">
        <span><b>Động từ:</b> Cut — một hành động, không phải “responsible for”</span>
        <span><b>Đối tượng &amp; quy mô:</b> payment API, 12k RPS — người đọc định được cỡ hệ thống</span>
        <span><b>Cách làm:</b> batching + read-through cache — chứng minh bạn hiểu vì sao nó nhanh lên</span>
        <span><b>Kết quả:</b> 840 ms → 180 ms — con số đủ nhỏ để tin được</span>
      </div>
    </div>""",
    },
    "faq": [
        (
            "Sách viết bằng tiếng Việt hay tiếng Anh?",
            "Phần phân tích và hướng dẫn viết bằng tiếng Việt. Riêng mười CV được trích "
            "<strong>nguyên văn tiếng Anh</strong>, kể cả tên mục và nhãn đã che — vì bạn nộp CV bằng "
            "tiếng Anh, nên thứ đáng học là cách người ta đặt câu, đúng từng chữ.",
        ),
        (
            "Tôi mới đi làm hoặc đang là sinh viên, có dùng được không?",
            "Được. Mười hồ sơ xếp từ intern tới staff, nên bạn tìm được mức gần với mình nhất. Phần "
            "“tìm con số ở đâu khi bạn nghĩ mình chẳng có gì để đếm” viết riêng cho trường hợp hồ sơ "
            "còn mỏng.",
        ),
        (
            "Đây có phải bộ CV mẫu để tải về điền không?",
            "Không. Đây là hồ sơ thật đã gửi đi và đã được gọi phỏng vấn, kèm danh sách công ty mà nó "
            "qua được vòng loại. Phần phân tích chỉ ra cả chỗ dở — mỗi hồ sơ đều có mục rủi ro, kể cả "
            "những hồ sơ đã qua vòng ở nhiều nơi cùng lúc.",
        ),
        (
            "Mua rồi nhận sách thế nào?",
            "Thanh toán qua Gumroad, tải PDF ngay sau đó. Mỗi lượt mua tương ứng một bản sách cho một "
            "người đọc.",
        ),
        (
            "Nên mua cuốn nào trước?",
            "Nếu bạn đang nộp đơn mà chưa được gọi phỏng vấn, bắt đầu với cuốn này — vòng CV rẻ để cải "
            "thiện nhất. Nếu bạn đã qua vòng CV và đang lo các vòng sau, hoặc vừa nhận offer, chọn "
            f'<a href="{STORE}/l/{SLUG_CAFE}">Cafe Talk</a>.',
        ),
    ],
    "final_eyebrow": "Vòng rẻ nhất để cải thiện",
    "final_h2": "Vòng CV không mở hết cánh cửa. Nhưng nó là cánh cửa đầu tiên.",
    "final_p": (
        "Không hứa đường tắt — phía sau vẫn phải trả bằng năng lực thật. Chỉ là bạn không nên "
        "trượt ở bốn mươi giây đầu mà không biết vì sao."
    ),
    "dock_meta": "PDF 86 trang",
}

CAFE = {
    "slug": SLUG_CAFE,
    "css": "hero-cafe-talk.css",
    "lang_title": "Cafe Talk: The Interview and Career Playbook | EngineerPro",
    "name_fallback": "Cafe Talk",
    "price_fallback": "$10.99",
    "list_price": "$15.99",
    "hero_h1": 'Cafe Talk<br /><em>The Interview and Career Playbook</em>',
    "hero_sub": (
        "Từ phòng phỏng vấn Big Tech tới ba tháng đầu, thăng tiến và những mùa cắt giảm. Đúc kết "
        "từ mười buổi trò chuyện của hai kỹ sư đã ngồi cả ghế ứng viên lẫn ghế người phỏng vấn "
        "tại Amazon, NVIDIA, TikTok và Grab."
    ),
    "inside_art": INSIDE_ART_CAFE,
    "cover_pill": "10 chương · hơn nửa sách là sau khi bạn ký",
    "price_note": "Đang giảm $5 — mã <code>EngineerProAug</code> tự động áp ở bước thanh toán, bạn không phải nhập gì. Tải PDF ngay sau khi mua.",
    "chips": [
        "Viết từ cả hai phía của chiếc bàn",
        "Có phần luật lao động Việt Nam",
        "PDF · Tiếng Việt",
    ],
    "proof": {
        "label": "Đúc kết từ ghế ứng viên và ghế người phỏng vấn tại",
        "items": ["Amazon", "NVIDIA", "TikTok", "Grab"],
    },
    "authors_note": (
        "Cả hai cùng dạy tại EngineerPro, nơi các khoá học tập trung vào đúng bốn vòng "
        "phỏng vấn cốt lõi của Big Tech: thuật toán, thiết kế hệ thống, behavioral và "
        "kiến thức nền."
    ),
    "self": {
        "badge": "Bạn đang ở trang này",
        "cover": COVER_CAFE,
        "cover_alt": "Bìa sách Cafe Talk: The Interview and Career Playbook",
        "title_html": '<span data-gumroad-field="name">Cafe Talk: The Interview and Career Playbook</span>',
        "meta": "PDF · 67 trang · 10 chương · Tiếng Việt",
        "blurb": (
            "Hai tác giả đã chấm điểm ứng viên và cũng đã bị chấm điểm. Chỗ nào hai người không đồng "
            "ý với nhau thì được giữ nguyên thay vì làm mượt đi."
        ),
        "bullets": [
            "Vì sao người giỏi vẫn trượt: ba lỗi và bốn red flag người phỏng vấn ghi lại",
            "Nguyên tắc làm tròn xuống — một mục dưới ngưỡng kéo cả buổi xuống theo",
            "Bốn thứ phải chốt trong tuần đầu tiên đi làm",
            "Thử việc theo luật Việt Nam: trần 60 ngày, lương tối thiểu 85%",
            "Cắt giảm nhân sự: trợ cấp thực nhận và hạn nộp bảo hiểm thất nghiệp",
        ],
        "price_note": "Một lượt mua = một bản sách cho một người đọc.",
        "cta": "Tôi muốn cuốn này",
    },
    "other": {
        "badge": "Cuốn còn lại của bộ đôi",
        "cover": COVER_FORTY,
        "cover_alt": "Bìa sách Forty Seconds: Ten Real CVs That Passed Big Tech",
        "title": "Forty Seconds: Ten Real CVs That Passed Big Tech",
        "meta": "PDF · 86 trang · 11 chương · Tiếng Việt",
        "blurb": (
            "Mười CV thật của kỹ sư Việt Nam đã qua vòng loại tại Meta, Google, Amazon, NVIDIA, "
            "Databricks, Anthropic, Grab, Citadel… trích nguyên văn tiếng Anh kèm phân tích."
        ),
        "bullets": [
            "Bốn mươi giây và đường đi thật của mắt người đọc CV",
            "Bốn mảnh của một gạch đầu dòng: động từ, quy mô, cách làm, kết quả",
            "Mười hai lỗi khiến hồ sơ bị loại, xếp theo mức thiệt hại",
            "Checklist trước khi bấm nộp + thư viện động từ",
        ],
        # effective price after the auto-applied EngineerProAug code
        "price": "$14.99",
        "list_price": "$19.99",
        "price_note": "Có trang sản phẩm riêng trên Gumroad.",
        "url": f"{STORE}/l/{SLUG_FORTY}",
        "cta": "Xem Forty Seconds",
    },
    "inside_eyebrow": "Bên trong Cafe Talk",
    "inside_h2": "Mười chương, ba phần cộng một phần gom lại",
    "inside_parts": [
        (
            "P1",
            "Bước vào phòng phỏng vấn",
            [
                "Vì sao người giỏi vẫn trượt: ba lỗi và bốn red flag người phỏng vấn ghi lại mà không ai nói cho bạn biết",
                "Vòng thuật toán: hai trường phái luyện tập, tám bước xử lý một bài, và vì sao cày số lượng là vòng lặp không có lối ra",
                "Thiết kế hệ thống: người ta chấm cách bạn đặt câu hỏi và phân tích đánh đổi, không chấm đáp án",
                "Kiến thức nền: cơ sở dữ liệu, hệ điều hành, mạng, lý thuyết DSA — kèm những câu bẫy hay gặp",
            ],
        ),
        (
            "P2",
            "Thứ quyết định điểm số",
            [
                "Vòng behavioral: cách kể chuyện quyết định bạn được xếp vào level nào",
                "Nguyên tắc làm tròn xuống: mỗi mục trong phiếu đánh giá có ngưỡng tối thiểu riêng cho từng level",
                "Giao tiếp: rõ ràng thắng thông minh — phép thử cho mọi câu hỏi làm rõ",
                "Vì sao im lặng là lỗi đắt nhất trong phòng phỏng vấn",
            ],
        ),
        (
            "P3",
            "Sau khi đã vào được công ty mong muốn",
            [
                "Ba tháng đầu: bốn thứ phải chốt trong tuần đầu tiên, và vì sao được sếp tin quan trọng hơn được sếp quý",
                "Thử việc theo luật Việt Nam: trần 60 ngày, lương tối thiểu 85%, chỉ một lần cho một vị trí",
                "Quan hệ trong ngành: cho trước nhận sau, và một ranh giới bảo mật không được vượt qua",
                "Thăng tiến: hai con đường, và cái trần vô hình nằm ở phạm vi công việc chứ không nằm ở chức danh của sếp",
                "Cắt giảm nhân sự: trợ cấp mất việc thực nhận, hạn nộp bảo hiểm thất nghiệp, và vì sao người đang làm ở nước ngoài phải tra visa trước khi sửa CV",
            ],
        ),
        (
            "P4",
            "Gom lại những gì đã nói",
            [
                "Sáu sợi chỉ nối mười chương",
                "Một danh sách việc cần làm gom từ cả cuốn sách",
            ],
        ),
    ],
    "inside_note": (
        "Không hứa đường tắt. Cuốn sách nói thẳng rằng mẹo không thay thế được nền tảng — phần lớn "
        "nội dung là để bạn không mất điểm ở những chỗ đáng ra không nên mất."
    ),
    "demo_btn": "Xem ba con số trong phần thử việc",
    "modal": {
        "title": "Thử việc theo luật Việt Nam",
        "intro": (
            "Phần luật lao động trong sách dẫn điều khoản cụ thể, không nói chung chung. Ba con số "
            "dưới đây là ví dụ — rất ít người đi làm biết đủ cả ba."
        ),
        "body": """    <div class="bullet">
      <p class="bullet__lbl">Ba con số</p>
      <div class="bullet__key">
        <span><b>Trần 60 ngày:</b> thời gian thử việc không được vượt mức luật định cho vị trí của bạn</span>
        <span><b>85%:</b> mức lương tối thiểu trong thời gian thử việc, tính trên lương của công việc đó</span>
        <span><b>Một lần:</b> một người chỉ thử việc một lần cho một vị trí — không có chuyện gia hạn thêm vòng nữa</span>
      </div>
    </div>

    <div class="bullet">
      <p class="bullet__lbl">Trong sách còn có</p>
      <p class="bullet__txt">
        Trợ cấp mất việc <mark>thực nhận</mark> là bao nhiêu, <mark>hạn nộp</mark> bảo hiểm thất nghiệp,
        quyền lợi khi bị cắt giảm, và vì sao người đang làm ở nước ngoài phải
        <mark>tra visa trước khi sửa CV</mark>.
      </p>
    </div>""",
    },
    "faq": [
        (
            "Sách này dành cho ai?",
            "Cho người đang chuẩn bị phỏng vấn Big Tech, và cho người vừa vào làm. Nếu bạn chỉ cần "
            "luyện đề thì đây không phải sách bài tập — đây là cách người phỏng vấn chấm bạn, và "
            "những gì xảy ra sau khi bạn ký.",
        ),
        (
            "Đã đi làm vài năm rồi thì còn cần không?",
            "Phần ba viết cho đúng giai đoạn đó: thăng tiến, cái trần vô hình nằm ở phạm vi công việc, "
            "quan hệ trong ngành, và việc cần làm trong tuần đầu tiên của một mùa cắt giảm.",
        ),
        (
            "Phần luật lao động có áp dụng cho tôi không?",
            "Phần này viết theo luật lao động Việt Nam và dẫn điều khoản cụ thể — thử việc, trợ cấp mất "
            "việc, quyền lợi khi bị cắt giảm. Nếu bạn đang làm ở nước ngoài, sách nói riêng về chuyện "
            "tra visa trước khi bắt đầu tìm việc lại.",
        ),
        (
            "Mua rồi nhận sách thế nào?",
            "Thanh toán qua Gumroad, tải PDF ngay sau đó. Mỗi lượt mua tương ứng một bản sách cho một "
            "người đọc.",
        ),
        (
            "Nên mua cuốn nào trước?",
            "Nếu bạn nộp đơn mà chưa được gọi phỏng vấn, vấn đề nằm ở vòng CV — chọn "
            f'<a href="{STORE}/l/{SLUG_FORTY}">Forty Seconds</a>. Nếu bạn đã được gọi phỏng vấn, hoặc '
            "vừa nhận offer và muốn biết đường đi phía sau, bắt đầu với cuốn này.",
        ),
    ],
    "final_eyebrow": "Phần ít ai viết ra",
    "final_h2": "Nhận offer không phải vạch đích. Đó là ngày đầu tiên của phần khó hơn.",
    "final_p": (
        "Hai tác giả không phải lúc nào cũng đồng ý với nhau, và những chỗ đó được giữ nguyên. "
        "Không hứa đường tắt — chỉ là bạn đi mà biết đường."
    ),
    "dock_meta": "PDF 67 trang",
}


# --------------------------------------------------------------------------- #
# Shared layout
# --------------------------------------------------------------------------- #

JOURNEY = [
    (
        "01",
        "Vòng CV",
        "Không ai phỏng vấn bạn. Chỉ có một tờ giấy và bốn mươi giây. Đây là vòng đánh trượt nhiều người nhất.",
        "Forty Seconds",
        "",
    ),
    (
        "02",
        "Các vòng phỏng vấn",
        "Thuật toán, system design, behavioral, kiến thức nền — và cách người phỏng vấn thực sự chấm điểm bạn.",
        "Cafe Talk",
        " step__tag--alt",
    ),
    (
        "03",
        "90 ngày đầu",
        "Ký hợp đồng xong mới là lúc khó. Hơn nửa cuốn Cafe Talk nói về giai đoạn này.",
        "Cafe Talk",
        " step__tag--alt",
    ),
    (
        "04",
        "Thăng tiến &amp; rủi ro",
        "Lên level, đàm phán, và phải làm gì khi công ty bước vào mùa cắt giảm — kèm luật lao động Việt Nam.",
        "Cafe Talk",
        " step__tag--alt",
    ),
]

# Gumroad only lets verified buyers rate a product, so the landing page cannot carry a
# public "write a review" button — it points buyers at their library instead.
FAQ_REVIEW = (
    "Đọc xong rồi, viết đánh giá ở đâu?",
    "Gumroad chỉ cho người đã mua chấm điểm, nên nút đánh giá không nằm ở trang này. Mở "
    '<a href="https://app.gumroad.com/library" target="_blank" rel="noopener">thư viện Gumroad</a> '
    "của bạn, chọn cuốn sách rồi chấm sao kèm nhận xét — link tới thư viện cũng có sẵn trong "
    "email biên nhận lúc mua. Điểm và số lượt đánh giá sẽ hiện ngay trên trang này.",
)

AUTHORS_PHOTO = (
    "https://public-files.gumroad.com/dlax51rydtohrw6d0sb89ywny9m6"
)

AUTHORS = f"""      <figure class="authors__photo rv">
        <img src="{AUTHORS_PHOTO}" width="1246" height="496"
             alt="Lâm Phạm và Harry Lê Quang Hoà, hai tác giả của bộ sách" />
      </figure>

      <div class="authors">
        <article class="author rv">
          <div class="author__top">
            <div>
              <h3>Lâm Phạm</h3>
              <p class="author__role">Senior Software Engineer @ NVIDIA</p>
            </div>
          </div>
          <p>
            Nhà sáng lập và lead mentor của EngineerPro. Từng làm tại TikTok, Grab, Motional và
            Sea Group. Đã ngồi cả ghế người phỏng vấn lẫn ghế ứng viên, và đã mentor khoảng một
            nghìn năm trăm kỹ sư.
          </p>
          <p style="margin-top:.7rem">
            <a href="https://www.linkedin.com/in/lam0895" target="_blank" rel="noopener">LinkedIn →</a>
          </p>
        </article>

        <article class="author rv">
          <div class="author__top">
            <div>
              <h3>Harry Lê Quang Hoà</h3>
              <p class="author__role">Software Engineer @ Amazon Web Services</p>
            </div>
          </div>
          <p>
            Đồng sáng lập EngineerPro, hiện thuộc team Aurora PostgreSQL tại AWS Canada. Hơn mười
            năm kinh nghiệm ở Singapore và Canada, từng là Tech Lead tại TikTok Singapore và làm
            tại Visa cùng một vài startup.
          </p>
          <p style="margin-top:.7rem">
            <a href="https://www.linkedin.com/in/harry-le-quang-hoa" target="_blank" rel="noopener">LinkedIn →</a>
          </p>
        </article>
      </div>"""

SCRIPT = r"""<script>
(function () {
  "use strict";

  /* ---------- theme toggle (light / dark) ---------- */
  var root = document.documentElement;
  var btn = document.getElementById("themeBtn");
  var ico = document.getElementById("themeIco");

  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function read(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }

  function systemDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function isDark() {
    var t = root.getAttribute("data-theme");
    return t ? t === "dark" : systemDark();
  }
  function paint() {
    var dark = isDark();
    if (ico) ico.textContent = dark ? "\u2600" : "\u263e";
    if (btn) {
      btn.setAttribute("aria-pressed", dark ? "true" : "false");
      btn.setAttribute("title", dark ? "Chuyển sang giao diện sáng" : "Chuyển sang giao diện tối");
    }
  }
  var saved = read("ep-landing-theme");
  if (saved === "dark" || saved === "light") root.setAttribute("data-theme", saved);
  paint();

  if (btn) {
    btn.addEventListener("click", function () {
      var next = isDark() ? "light" : "dark";
      root.setAttribute("data-theme", next);
      store("ep-landing-theme", next);
      paint();
    });
  }

  /* ---------- scroll reveal ---------- */
  var items = [].slice.call(document.querySelectorAll(".rv"));
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- sticky buy dock: show once the hero CTA scrolls away ---------- */
  var dock = document.getElementById("dock");
  var anchor = document.getElementById("buy");
  if (dock && anchor && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      dock.classList.toggle("is-on", !entries[0].isIntersecting);
    }, { threshold: 0 }).observe(anchor);
  }

  /* ---------- rating row: only reveal it once there is a real rating ---------- */
  var ratingRow = document.getElementById("ratingRow");
  if (ratingRow) {
    var countEl = ratingRow.querySelector('[data-gumroad-field="review-count"]');
    var rateEl = ratingRow.querySelector('[data-gumroad-field="rating"]');
    var count = parseInt(((countEl && countEl.textContent) || "").replace(/[^0-9]/g, ""), 10) || 0;
    if (count > 0) {
      var score = parseFloat(((rateEl && rateEl.textContent) || "").replace(",", ".")) || 0;
      /* floor, never round up: the exact score sits next to the stars anyway,
         so erring low is better than claiming a star that was not earned */
      var full = Math.max(0, Math.min(5, Math.floor(score)));
      ratingRow.querySelector("#ratingStars").textContent =
        "★★★★★".slice(0, full) + "☆☆☆☆☆".slice(0, 5 - full);
      ratingRow.hidden = false;
    }
  }

  /* ---------- demo modal (focus-trapped, Esc to close) ---------- */
  var modal = document.getElementById("demo");
  var open = document.getElementById("demoBtn");
  var close = document.getElementById("demoX");
  var lastFocus = null;

  function focusables() {
    return [].slice.call(
      modal.querySelectorAll('a[href], a[data-gumroad-action], button, input, [tabindex]:not([tabindex="-1"])')
    ).filter(function (el) { return el.offsetParent !== null || el === close; });
  }
  function openModal() {
    lastFocus = document.activeElement;
    modal.classList.add("is-open");
    var f = focusables();
    if (f.length) f[0].focus();
  }
  function closeModal() {
    modal.classList.remove("is-open");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  if (open) open.addEventListener("click", openModal);
  if (close) close.addEventListener("click", closeModal);
  if (modal) {
    modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
  }
  document.addEventListener("keydown", function (e) {
    if (!modal || !modal.classList.contains("is-open")) return;
    if (e.key === "Escape") { closeModal(); return; }
    if (e.key !== "Tab") return;
    var f = focusables();
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  /* ---------- keep anchor-style buy elements keyboard-operable ---------- */
  [].slice.call(document.querySelectorAll('a[data-gumroad-action="buy"]')).forEach(function (el) {
    if (!el.hasAttribute("href")) {
      el.setAttribute("role", "button");
      el.setAttribute("tabindex", "0");
      el.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); el.click(); }
      });
    }
  });
})();
</script>"""


def render(b):
    css = (HERE / "base.css").read_text(encoding="utf-8").rstrip()
    hero_css = (HERE / b["css"]).read_text(encoding="utf-8").rstrip()

    # data-gumroad-field="price" resolves to the price the buyer actually pays, which
    # is $5 under list while the standing "EngineerProAug" offer code auto-applies at
    # checkout. The literal price below is only the pre-interpolation fallback, so it
    # is written as list price and never shown on the live page.
    price_attr = ' data-gumroad-field="price"' if b.get("price_live", True) else ""

    # Struck-through list price + "−$5" badge, so the discounted figure Gumroad
    # renders reads as a discount instead of just looking like the price.
    def was(list_price, indent, cls):
        if not OFFER or not list_price:
            return ""
        pad = " " * indent
        return (
            f'{pad}<span class="sr">Giá gốc</span>\n'
            f'{pad}<s class="{cls}">{list_price}</s>\n'
        )

    def off(cls, indent, label=None):
        if not OFFER:
            return ""
        pad = " " * indent
        return f'{pad}<span class="{cls}">{label or "−" + OFFER["amount"]}</span>\n'

    pr = b["proof"]
    proof_items = "\n".join(f"        <li>{c}</li>" for c in pr["items"])
    proof = (
        '  <section class="proof" aria-label="Các công ty liên quan">\n'
        '    <div class="wrap">\n'
        f'      <p class="proof__label">{pr["label"]}</p>\n'
        '      <ul class="proof__list rv">\n'
        f"{proof_items}\n"
        "      </ul>\n"
        "    </div>\n"
        "  </section>\n"
    )

    dock_was = f'<s>{b["list_price"]}</s> ' if OFFER and b.get("list_price") else ""

    final_deal = ""
    if OFFER and b.get("list_price"):
        final_deal = (
            f'        <p class="final__deal">Giá gốc <s>{b["list_price"]}</s> · '
            f'giảm <b>{OFFER["amount"]}</b> tự động ở bước thanh toán</p>\n'
        )

    was_hero = was(b.get("list_price"), 10, "pricetag__was")
    off_hero = off("pricetag__off", 10, f'Tiết kiệm {OFFER["amount"]}' if OFFER else "")
    was_self = was(b.get("list_price"), 14, "book__was")
    off_self = off("book__off", 14)
    was_other = was(b["other"].get("list_price"), 14, "book__was")
    off_other = off("book__off", 14)

    chips = "\n".join(f'          <span class="chip">{c}</span>' for c in b["chips"])

    journey = "\n".join(
        f"""        <li class="step rv">
          <p class="step__n">{n}</p>
          <h3>{title}</h3>
          <p>{body}</p>
          <span class="step__tag{cls}">{tag}</span>
        </li>"""
        for n, title, body, tag, cls in JOURNEY
    )

    s, o = b["self"], b["other"]
    self_bullets = "\n".join(f"            <li>{x}</li>" for x in s["bullets"])
    other_bullets = "\n".join(f"            <li>{x}</li>" for x in o["bullets"])

    parts = "\n\n".join(
        """        <details class="acc rv">
          <summary><span class="acc__n">{code}</span> {title}</summary>
          <div class="acc__body">
            <ul>
{items}
            </ul>
          </div>
        </details>""".format(
            code=code,
            title=title,
            items="\n".join(f"              <li>{i}</li>" for i in items),
        )
        for code, title, items in b["inside_parts"]
    )

    faq = "\n".join(
        """        <details class="acc rv">
          <summary>{q}</summary>
          <div class="acc__body">{a}</div>
        </details>""".format(q=q, a=a)
        for q, a in b["faq"] + [FAQ_REVIEW]
    )

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{b["lang_title"]}</title>
<style>
{css}

{hero_css}
</style>
</head>
<body>
<a class="skip" href="#buy">Bỏ qua tới phần mua sách</a>

<header class="top">
  <div class="wrap top__in">
    <a class="brand" href="{STORE}/">
      <span class="brand__mark" aria-hidden="true">EP</span>
      <span>EngineerPro</span>
    </a>
    <div class="top__spacer"></div>
    <a class="btn btn--ghost btn--sm top__store" href="{STORE}/" target="_blank" rel="noopener">Tất cả sản phẩm</a>
    <a class="btn btn--primary btn--sm" data-gumroad-action="buy">Mua ngay — <span{price_attr}>{b["price_fallback"]}</span></a>
    <button class="iconbtn" id="themeBtn" type="button" aria-pressed="false" title="Đổi giao diện sáng/tối">
      <span aria-hidden="true" id="themeIco">◐</span>
      <span class="sr">Đổi giao diện sáng/tối</span>
    </button>
  </div>
</header>

<main id="main">

  <!-- ======================= HERO ======================= -->
  <section class="hero" aria-labelledby="h-hero">
    <div class="wrap hero__grid">
      <div>
        <p class="eyebrow">Bộ đôi sách · EngineerPro</p>
        <h1 id="h-hero">{b["hero_h1"]}</h1>
        <p class="hero__sub lede">
          {b["hero_sub"]}
        </p>

        <div class="hero__cta">
          <a class="btn btn--primary" data-gumroad-action="buy" id="buy">
            Mua {b["name_fallback"]}
          </a>
          <a class="btn btn--ghost" href="#sach">Xem cả hai cuốn</a>
        </div>

        <div class="pricetag" style="margin-top:1.1rem">
{was_hero}          <span class="sr">Giá sau giảm</span>
          <span class="pricetag__now"{price_attr}>{b["price_fallback"]}</span>
{off_hero}        </div>
        <p class="pricenote">{b["price_note"]}</p>

        <!-- Gumroad interpolates the two fields below. The row stays hidden until a
             script confirms review-count > 0, so an unrated product never shows a
             row of filled stars that it has not earned. -->
        <p class="reviews" id="ratingRow" hidden>
          <span class="stars" id="ratingStars" aria-hidden="true"></span>
          <span><span data-gumroad-field="rating">0</span>/5</span>
          <span aria-hidden="true">·</span>
          <span><span data-gumroad-field="review-count">0</span> lượt đánh giá</span>
        </p>

        <div class="trustrow">
{chips}
        </div>
      </div>

      <div class="cover-hero">
        <div class="cover-hero__frame">
          <!-- no fetchpriority/loading hints here: Gumroad's sanitizer strips them -->
          <img class="cover-hero__img" src="{s["cover"]}" alt="{s["cover_alt"]}"
               width="1005" height="1421" />
          <p class="cover-hero__pill">{b["cover_pill"]}</p>
        </div>
      </div>
    </div>
  </section>

{proof}
  <!-- ======================= AUTHORS ======================= -->
  <section aria-labelledby="h-authors">
    <div class="wrap">
      <div class="sec__head rv">
        <p class="eyebrow">Ai viết</p>
        <h2 id="h-authors">Hai người đã đọc hàng nghìn CV để chọn ứng viên vào vòng trong</h2>
        <p>{b["authors_note"]}</p>
      </div>

{AUTHORS}
    </div>
  </section>

  <!-- ======================= JOURNEY ======================= -->
  <section class="band" aria-labelledby="h-journey">
    <div class="wrap">
      <div class="sec__head rv">
        <p class="eyebrow">Hai cuốn, hai nửa hành trình</p>
        <h2 id="h-journey">Vào được cửa là một việc. Trụ được và đi lên là việc khác.</h2>
        <p class="lede">
          Phần lớn tài liệu phỏng vấn dừng lại ở lúc bạn nhận offer. Bộ đôi này đi hết chặng
          đường: từ tờ CV bị đọc trong bốn mươi giây, tới lúc bạn ngồi trong phòng review lương.
        </p>
      </div>

      <ol class="journey">
{journey}
      </ol>
    </div>
  </section>

  <!-- ======================= THE TWO BOOKS ======================= -->
  <section id="sach" aria-labelledby="h-books">
    <div class="wrap">
      <div class="sec__head rv">
        <p class="eyebrow">Nội dung</p>
        <h2 id="h-books">Bạn đang xem bộ đôi</h2>
        <p class="lede">Mua riêng từng cuốn. Cuốn nào cũng đọc độc lập được — nhưng đọc cả hai thì khớp thành một đường thẳng.</p>
      </div>

      <div class="books">
        <!-- the product this page is hosted on -->
        <article class="book book--lead rv">
          <span class="book__badge">{s["badge"]}</span>
          <div class="book__top">
            <div class="book__cover">
              <img src="{s["cover"]}" alt="{s["cover_alt"]}" width="1005" height="1421" />
            </div>
            <div>
              <h3>{s["title_html"]}</h3>
              <p class="book__meta">{s["meta"]}</p>
              <p class="book__blurb">{s["blurb"]}</p>
            </div>
          </div>

          <ul class="book__list">
{self_bullets}
          </ul>

          <p style="margin-top:1rem">
            <button class="btn btn--ghost btn--sm" type="button" id="demoBtn">
              {b["demo_btn"]}
            </button>
          </p>

          <div class="book__foot">
            <div class="book__price">
{was_self}              <b{price_attr}>{b["price_fallback"]}</b>
{off_self}            </div>
            <p class="book__note">{s["price_note"]}</p>
            <a class="btn btn--primary btn--block" data-gumroad-action="buy">{s["cta"]}</a>
          </div>
        </article>

        <!-- the other book: a plain link to its own Gumroad product page -->
        <article class="book rv">
          <span class="book__badge book__badge--alt">{o["badge"]}</span>
          <div class="book__top">
            <div class="book__cover">
              <img src="{o["cover"]}" alt="{o["cover_alt"]}" width="1005" height="1421" />
            </div>
            <div>
              <h3>{o["title"]}</h3>
              <p class="book__meta">{o["meta"]}</p>
              <p class="book__blurb">{o["blurb"]}</p>
            </div>
          </div>

          <ul class="book__list">
{other_bullets}
          </ul>

          <div class="book__foot">
            <div class="book__price">
{was_other}              <b>{o["price"]}</b>
{off_other}            </div>
            <p class="book__note">{o["price_note"]}</p>
            <a class="btn btn--ghost btn--block" href="{o["url"]}">{o["cta"]}</a>
          </div>
        </article>
      </div>

      <div class="store rv">
        <div>
          <p class="store__t">Toàn bộ sản phẩm của EngineerPro</p>
          <p class="store__p">
            Sách, và những thứ ra mắt sau này, đều nằm chung một chỗ trên Gumroad.
          </p>
        </div>
        <a class="btn btn--ghost" href="{STORE}/" target="_blank" rel="noopener">
          Xem cửa hàng EngineerPro →
        </a>
      </div>
    </div>
  </section>

  <!-- ======================= WHAT'S INSIDE ======================= -->
  <section class="band" aria-labelledby="h-inside">
    <div class="wrap">
      <div class="sec__head rv">
        <p class="eyebrow">{b["inside_eyebrow"]}</p>
        <h2 id="h-inside">{b["inside_h2"]}</h2>
      </div>

      <div class="inside-grid">
        <div>
{parts}

          <p class="lede" style="margin-top:1.4rem;font-size:.95rem">
            {b["inside_note"]}
          </p>
        </div>

        <div class="inside-art rv">
{b["inside_art"]}
        </div>
      </div>
    </div>
  </section>

  <!-- ======================= AUTHORS ======================= -->
  <!-- ======================= FAQ ======================= -->
  <section aria-labelledby="h-faq">
    <div class="wrap">
      <div class="sec__head rv">
        <p class="eyebrow">Câu hỏi thường gặp</p>
        <h2 id="h-faq">Trước khi bạn mua</h2>
      </div>
      <div style="max-width:46rem">
{faq}
      </div>
    </div>
  </section>

  <!-- ======================= FINAL CTA ======================= -->
  <section aria-labelledby="h-final">
    <div class="wrap">
      <div class="final rv">
        <p class="eyebrow">{b["final_eyebrow"]}</p>
        <h2 id="h-final">{b["final_h2"]}</h2>
        <p>{b["final_p"]}</p>
        <a class="btn btn--primary" data-gumroad-action="buy">
          Mua {b["name_fallback"]} — <span{price_attr}>{b["price_fallback"]}</span>
        </a>
{final_deal}      </div>
    </div>
  </section>

  <footer>
    <div class="wrap foot__in">
      <span>© EngineerPro</span>
      <a href="{STORE}/">Tất cả sách trên Gumroad</a>
      <a href="https://engineerprogurus.com/ebooks/" target="_blank" rel="noopener">engineerprogurus.com</a>
    </div>
  </footer>
</main>

<!-- ======================= STICKY BUY DOCK (mobile) ======================= -->
<div class="dock" id="dock">
  <div class="dock__txt">
    <p class="dock__t" data-gumroad-field="name">{b["name_fallback"]}</p>
    <p class="dock__p">{dock_was}<span{price_attr}>{b["price_fallback"]}</span> · {b["dock_meta"]}</p>
  </div>
  <a class="btn btn--primary btn--sm" data-gumroad-action="buy">Mua</a>
</div>

<!-- ======================= DEMO MODAL ======================= -->
<div class="modal" id="demo" role="dialog" aria-modal="true" aria-labelledby="demoTitle">
  <div class="modal__box">
    <div class="modal__head">
      <h3 id="demoTitle">{b["modal"]["title"]}</h3>
      <button class="modal__x" type="button" id="demoX" title="Đóng">
        <span aria-hidden="true">✕</span><span class="sr">Đóng</span>
      </button>
    </div>
    <p class="lede" style="margin-top:.6rem;font-size:.93rem">
      {b["modal"]["intro"]}
    </p>

{b["modal"]["body"]}

    <p style="margin-top:1.3rem">
      <a class="btn btn--primary btn--block" data-gumroad-action="buy">
        Mua sách — <span{price_attr}>{b["price_fallback"]}</span>
      </a>
    </p>
  </div>
</div>

{SCRIPT}
</body>
</html>
"""


def main():
    targets = [(FORTY, ROOT / "landing.html"), (CAFE, ROOT / "landing-cafe-talk.html")]
    for book, out in targets:
        html = render(book)
        out.write_text(html, encoding="utf-8")
        # count attributes on real tags only, so the JS querySelector string
        # further down the file is not mistaken for a buy element
        buys = len(re.findall(r'<[a-z]+[^>]*\bdata-gumroad-action="buy"', html))
        fields = len(re.findall(r'<[a-z]+[^>]*\bdata-gumroad-field="', html))
        assert buys >= 1, f"{out.name} has no buy element"
        print(f"{out.name}: {len(html):>6} bytes · {buys} buy elements · {fields} live fields · product {book['slug']}")


if __name__ == "__main__":
    main()
