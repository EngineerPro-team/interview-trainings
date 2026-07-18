(function () {
  "use strict";

  // ===================== BASE PATH =====================
  // GitHub Pages serves project repos at /<repo>/. build_pages.py injects
  // window.EP_BASE_PATH; everything else defaults to "" (root deploy).
  const BASE_PATH = (typeof window !== "undefined" && window.EP_BASE_PATH) || "";
  const SD_URL_SLUG = "system-design-material";

  function stripBasePath(p) {
    if (!BASE_PATH) return p || "";
    if (p === BASE_PATH) return "/";
    if (p && p.indexOf(BASE_PATH + "/") === 0) return p.slice(BASE_PATH.length);
    return p || "";
  }

  // Rewrite every relative `src="assets/..."` (or "src='assets/...'") inside a
  // string of HTML to use asset(...). Needed when we inject crawled HTML
  // bodies that embed images via relative paths — without rewriting, the
  // browser resolves them against the page URL (so /courses/foo/assets/...
  // returns 404) AND BASE_PATH wouldn't be honoured on project Pages.
  function rewriteAssetUrls(html) {
    if (!html || typeof html !== "string") return html;
    return html.replace(
      /(\b(?:src|href)=)(["'])(assets\/[^"']+)(\2)/gi,
      (_full, attr, q, path, _q2) => attr + q + asset(path) + q
    );
  }

  // Resolve any asset path so it works at both root (/) and project-Pages
  // subpath (/interview-trainings/). Pass through absolute URLs, root-relative
  // paths, and data: URIs unchanged.
  function asset(p) {
    if (!p) return p;
    if (typeof p !== "string") return p;
    if (/^(?:https?:|data:|blob:|\/\/)/i.test(p)) return p;          // absolute / data
    if (p.charAt(0) === "/") {                                       // root-relative
      // Already includes BASE_PATH? leave as-is. Otherwise prepend it.
      if (BASE_PATH && p.indexOf(BASE_PATH + "/") !== 0 && p !== BASE_PATH) {
        return BASE_PATH + p;
      }
      return p;
    }
    // bare "assets/..." — prefix with BASE_PATH (or "" if root deploy)
    return BASE_PATH + "/" + p;
  }

  // If we got here via 404.html (e.g. user opened a non-prerendered URL),
  // 404.html stashed the original path in sessionStorage. Restore it before
  // the router runs so the SPA still ends up at the right route.
  try {
    const stash = sessionStorage.getItem("ep_redirect");
    if (stash && stash !== location.pathname + location.search + location.hash) {
      sessionStorage.removeItem("ep_redirect");
      history.replaceState(null, "", stash);
    }
  } catch (e) { /* sessionStorage disabled */ }

  // ===================== i18n =====================
  // Lang priority: ?lang= query param → localStorage → navigator.language → 'vi'.
  // The query param is honoured so that hreflang alternate URLs ("?lang=en") are
  // deterministic for crawlers and direct visitors.
  function detectLang() {
    try {
      const qp = new URLSearchParams(location.search).get("lang");
      if (qp === "vi" || qp === "en") {
        try { localStorage.setItem("epLang", qp); } catch (e) {}
        return qp;
      }
    } catch (e) { /* URLSearchParams disabled */ }
    try {
      const saved = localStorage.getItem("epLang");
      if (saved === "vi" || saved === "en") return saved;
    } catch (e) { /* localStorage disabled */ }
    const nav = (navigator.language || navigator.userLanguage || "").toLowerCase();
    return nav.startsWith("vi") ? "vi" : "en";
  }

  let currentLang = detectLang();
  const I18N = window.I18N || { vi: {}, en: {} };

  // Translate a single key. Falls back through: requested → vi → key itself.
  function t(key) {
    const dict = I18N[currentLang] || {};
    const fallback = I18N.vi || {};
    return dict[key] != null ? dict[key] : (fallback[key] != null ? fallback[key] : key);
  }

  function applyI18n(root = document) {
    root.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      el.textContent = t(key);
    });
    root.querySelectorAll("[data-i18n-html]").forEach((el) => {
      const key = el.getAttribute("data-i18n-html");
      el.innerHTML = t(key);
    });
    root.querySelectorAll("[data-i18n-attr]").forEach((el) => {
      // data-i18n-attr="placeholder|some.key" — may chain "attr|key,attr|key"
      const spec = el.getAttribute("data-i18n-attr") || "";
      spec.split(",").forEach((pair) => {
        const [attr, key] = pair.split("|").map((s) => s.trim());
        if (attr && key) el.setAttribute(attr, t(key));
      });
    });
    // Swap any <img data-src-vi="..." data-src-en="..."> based on currentLang
    document.querySelectorAll("img[data-src-vi][data-src-en]").forEach((img) => {
      const raw = currentLang === "en"
        ? img.getAttribute("data-src-en")
        : img.getAttribute("data-src-vi");
      const next = asset(raw);
      if (next && img.getAttribute("src") !== next) img.setAttribute("src", next);
    });
    // Refresh dynamic count spans (their innerHTML was just clobbered by data-i18n-html).
    refreshLiveCounts();
    document.documentElement.lang = currentLang === "en" ? "en" : "vi";
  }

  // Minimal allowlist sanitizer for HTML coming from our own crawlers.
  // Threat model: defence-in-depth only — all upstream sources are owned by us
  // (EngineerPro blog, our Google Docs, our Substack), but if any source ever
  // ships a <script> or javascript: URL we don't want it executing on the page.
  // Strips: <script>, <style>, on* event handlers, javascript:/data: hrefs.
  // Allows iframes only for known embed hosts (YouTube, Vimeo, Google Drive,
  // Facebook page plugin).
  const IFRAME_HOST_ALLOWLIST = [
    "www.youtube.com", "youtube.com",
    "www.youtube-nocookie.com", "youtube-nocookie.com",
    "player.vimeo.com",
    "drive.google.com", "docs.google.com",
    "www.facebook.com",
  ];
  function sanitizeHtml(html) {
    if (!html || typeof html !== "string") return "";
    const doc = new DOMParser().parseFromString(`<div>${html}</div>`, "text/html");
    const root = doc.body.firstElementChild;
    if (!root) return "";
    const walker = doc.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
    const toRemove = [];
    let n = walker.currentNode;
    while ((n = walker.nextNode())) {
      const tag = n.tagName.toLowerCase();
      if (tag === "script" || tag === "style" || tag === "object" || tag === "embed") {
        toRemove.push(n);
        continue;
      }
      // Drop event-handler attributes + javascript: / data: URLs in href/src
      for (const attr of [...n.attributes]) {
        const name = attr.name.toLowerCase();
        const value = (attr.value || "").trim();
        if (name.startsWith("on")) { n.removeAttribute(attr.name); continue; }
        if ((name === "href" || name === "src" || name === "xlink:href") &&
            /^\s*(javascript|data|vbscript):/i.test(value)) {
          n.removeAttribute(attr.name);
        }
      }
      if (tag === "iframe") {
        let host = "";
        try { host = new URL(n.getAttribute("src") || "", location.href).host; }
        catch (_) { host = ""; }
        if (!IFRAME_HOST_ALLOWLIST.includes(host)) toRemove.push(n);
      }
    }
    toRemove.forEach((el) => el.remove());
    return root.innerHTML;
  }

  // Counts that change with data: stories, courses, mentors, podcasts, faq.
  // Single source of truth so the i18n templates can keep a placeholder number
  // and we don't end up with stale "50" everywhere.
  function refreshLiveCounts() {
    const set = (id, n) => {
      const el = document.getElementById(id);
      if (el && n != null) el.textContent = String(n);
    };
    if (typeof stories !== "undefined") set("storiesCount", stories.length);
    if (typeof courses !== "undefined") set("coursesCount", courses.length);
    if (typeof podcasts !== "undefined") set("podcastCount", podcasts.length);
    if (typeof window.FAQS !== "undefined") set("faqCount", (window.FAQS || []).length);
    if (data && data.mentors) set("mentorsCount", data.mentors.length);
  }

  function setLang(lang) {
    if (lang !== "vi" && lang !== "en") return;
    currentLang = lang;
    try { localStorage.setItem("epLang", lang); } catch (e) { /* ignore */ }
    applyI18n();
    // Re-render dynamic content (cards, lists) so labels translate too
    if (typeof window.__rerenderAll === "function") window.__rerenderAll();
    updateLangSwitchUI();
  }

  function updateLangSwitchUI() {
    const btn = document.getElementById("langSwitch");
    if (!btn) return;
    const flag = btn.querySelector(".lang-switch__flag");
    const label = btn.querySelector(".lang-switch__label");
    // Show the OTHER language as the switch target
    if (currentLang === "vi") {
      if (flag) flag.textContent = "🇬🇧";
      if (label) label.textContent = "EN";
    } else {
      if (flag) flag.textContent = "🇻🇳";
      if (label) label.textContent = "VI";
    }
  }

  // ===================== TINY HASH ROUTER =====================
  //  #home, #courses, #book, #resources, #mentors, #stories, #podcast, #partners, #faq, #contact
  //  (#home-roadmap and #home-format are anchor scrolls into the home page)
  const TOP_ROUTES = [
    "home", "courses", "lich-khai-giang", "book", "system-design", "mock", "resources",
    "mentors", "stories", "podcast", "partners", "faq", "terms", "contact",
  ];

  // Route resolution: prefer pathname (real URL like /courses/foo/) if it matches
  // one of our routes, then fall back to hash (#course/foo). This lets the SPA
  // serve prerendered URLs cleanly while keeping the legacy hash router alive
  // for backwards-compatible links.
  // Clean path shortcuts that resolve to a section anchor on the home page
  // (e.g. /roadmap → / + scroll to #home-roadmap).
  const HOME_ANCHORS = {
    "roadmap": "home-roadmap",
    "format":  "home-format",
  };
  // Reverse map: anchor id -> clean URL alias, so clicking an in-page home
  // anchor (e.g. #home-roadmap) reflects a shareable path (/roadmap/).
  const HOME_ANCHOR_PATHS = Object.fromEntries(
    Object.entries(HOME_ANCHORS).map(([alias, anchorId]) => [anchorId, alias]),
  );
  // Deep-link sub-sections of the Resources tab: clicking
  // /resources/golang-tour lands on /resources/ and scrolls straight to
  // that resource block.
  const RESOURCES_ANCHORS = {
    "hr-screen":     "resHrScreen",
    "pip-big-tech":  "resPipBigTech",
    "pip":           "resPipBigTech", // back-compat alias
    "cs-fundamental":"resCsFundamental",
    "cs-fundamentals":"resCsFundamental",
    "interview-formats": "resInterviewFormats",
    "interview-format":  "resInterviewFormats",
    "formats":           "resInterviewFormats",
    "foundation":    "resFoundation",
    "golang-tour":   "resGolangTour",
    "cv-kit":        "resCV",
    "cv":            "resCV",         // back-compat alias
  };

  function parseHash() {
    let path = stripBasePath((location.pathname || "/").replace(/\/index\.html$/, ""));
    let m;
    if ((m = path.match(/^\/courses\/([^/]+)\/?$/))) return { route: "course", slug: m[1] };
    if ((m = path.match(/^\/stories\/([^/]+)\/?$/))) return { route: "story", slug: m[1] };
    if ((m = path.match(new RegExp(`^/${SD_URL_SLUG}/([^/]+)/?$`)))) {
      return { route: "sd-chapter", slug: m[1] };
    }
    // Legacy URL → same route; bootRoute() will replaceState to the new path.
    if ((m = path.match(/^\/system-design\/([^/]+)\/?$/))) {
      return { route: "sd-chapter", slug: m[1], legacySdUrl: true };
    }
    if (/^\/system-design\/?$/.test(path)) {
      return { route: "system-design", slug: null, legacySdUrl: true };
    }
    // Deep-link to a specific company inside the Interview Formats block, e.g.
    // /resources/interview-formats/axon → open the panel + jump to Axon.
    if ((m = path.match(/^\/resources\/(interview-formats|interview-format|formats)\/([\w-]+)\/?$/))) {
      return { route: "resources", slug: null, scrollTo: "resInterviewFormats", formatCompany: m[2].toLowerCase() };
    }
    if ((m = path.match(/^\/resources\/([\w-]+)\/?$/)) && RESOURCES_ANCHORS[m[1]]) {
      return { route: "resources", slug: null, scrollTo: RESOURCES_ANCHORS[m[1]] };
    }
    if ((m = path.match(new RegExp(`^/(courses|lich-khai-giang|book|${SD_URL_SLUG}|mock|resources|mentors|stories|podcast|partners|faq|terms|contact)/?$`)))) {
      const route = m[1] === SD_URL_SLUG ? "system-design" : m[1];
      return { route, slug: null };
    }
    if ((m = path.match(/^\/(roadmap|format)\/?$/))) {
      return { route: "home", slug: null, scrollTo: HOME_ANCHORS[m[1]] };
    }
    // Hash fallback (legacy or anchor-only navigation)
    const raw = (location.hash || "").replace(/^#/, "").trim();
    if (!raw) return { route: "home", slug: null };
    const [head, ...rest] = raw.split("/");
    if (head === "course" && rest.length) return { route: "course", slug: rest.join("/") };
    if (head === "story" && rest.length) return { route: "story", slug: rest.join("/") };
    if (head === "sd-chapter" && rest.length) return { route: "sd-chapter", slug: rest.join("/") };
    if (TOP_ROUTES.includes(head)) return { route: head, slug: null };
    if (HOME_ANCHORS[head]) return { route: "home", slug: null, scrollTo: HOME_ANCHORS[head] };
    return { route: "home", slug: null };
  }

  // Build the canonical /path/ for a given {route, slug}, prefixed by the
  // deploy subpath when running under a project-Pages URL.
  function pathFor(route, slug) {
    let p;
    if (route === "home" || !route) p = "/";
    else if (route === "course" && slug) p = `/courses/${slug}/`;
    else if (route === "story"  && slug) p = `/stories/${slug}/`;
    else if (route === "system-design") p = `/${SD_URL_SLUG}/`;
    else if (route === "sd-chapter" && slug) p = `/${SD_URL_SLUG}/${slug}/`;
    else p = `/${route}/`;
    return BASE_PATH ? BASE_PATH + (p === "/" ? "/" : p) : p;
  }

  function showRoute({ route, slug, scrollTo, legacySdUrl, formatCompany }) {
    if (legacySdUrl) {
      history.replaceState(null, "", pathFor(route, slug));
    }
    // Remove the prerender-time style that forces one route visible — once
    // JS hydrates we let `.route[hidden]` CSS do the work as usual.
    const preStyle = document.getElementById("prerenderShowRoute");
    if (preStyle) preStyle.remove();
    document.querySelectorAll(".route").forEach((s) => {
      s.hidden = s.dataset.route !== route;
    });
    document.querySelectorAll(".nav__links a").forEach((a) => {
      const active =
        a.dataset.route === route ||
        (route === "course" && a.dataset.route === "courses") ||
        (route === "story" && a.dataset.route === "stories") ||
        (route === "sd-chapter" && a.dataset.route === "system-design");
      a.classList.toggle("is-active", active);
    });

    updateSeoForRoute(route, slug);

    if (route === "course") {
      renderCourseDetail(slug);
    }
    if (route === "story") {
      renderStoryDetail(slug);
    }
    if (route === "sd-chapter") {
      renderSdChapter(slug);
    }
    if (scrollTo) {
      // Deep links like /roadmap or /format land on the home page and need
      // to scroll past the hero to the requested section. Wait a frame so
      // the route swap + i18n hydration finishes before measuring.
      requestAnimationFrame(() => {
        const el = document.getElementById(scrollTo);
        if (!el) return;
        const panel = el.classList.contains("resource-panel")
          ? el
          : el.closest("details.resource-panel");
        if (panel && !panel.open) panel.open = true;
        if (el.matches("details.faq-item") && !el.open) el.open = true;
        if (typeof syncResourceExpandLabels === "function") syncResourceExpandLabels();
        el.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    } else {
      window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
    }

    // Deep link /resources/interview-formats/<company>: select that company in
    // the filter (which expands it), then scroll to its card.
    if (formatCompany) {
      // Keep the "All companies" filter — just expand + scroll to the target
      // company within the full list (don't narrow the dropdown to one).
      const focusCompany = (tries = 0) => {
        const list = document.getElementById("interviewFormatsList");
        const card = list?.querySelector(
          `details.interview-formats__company[data-company-id="${formatCompany}"]`,
        );
        // List may not be hydrated yet on a cold deep-link load — retry.
        if (!card && tries < 20) {
          if (typeof initInterviewFormats === "function") initInterviewFormats();
          return requestAnimationFrame(() => focusCompany(tries + 1));
        }
        if (!card) return;
        card.open = true;
        if (typeof syncResourceExpandLabels === "function") syncResourceExpandLabels();
        requestAnimationFrame(() => card.scrollIntoView({ behavior: "smooth", block: "start" }));
      };
      requestAnimationFrame(() => focusCompany());
    }

    // SPA route changes go through pushState, so GA's auto page_view (which
    // fires once on initial document load) won't see them. Manually emit a
    // page_view event with the new path so Analytics → Pages report stays
    // accurate. We send `page_location` so GA picks up the absolute URL +
    // any query/hash; `page_title` reflects the route-specific document.title
    // that updateSeoForRoute() just wrote.
    try {
      if (typeof window.gtag === "function") {
        window.gtag("event", "page_view", {
          page_location: location.href,
          page_path:     location.pathname + location.search,
          page_title:    document.title,
        });
      }
    } catch (_) { /* analytics is non-critical, never block routing on it */ }
  }

  // SEO: keep <title>, <meta name="description">, <link rel="canonical">,
  // og:title, og:description, og:url, twitter:* in sync with the current route.
  function updateSeoForRoute(route, slug) {
    const en = currentLang === "en";
    const SUFFIX = en ? "EngineerPro — Big Tech Interview Prep" : "EngineerPro — Luyện phỏng vấn Big Tech";
    let title, desc;

    if (route === "course") {
      const c = (window.COURSES || []).find((x) => x.slug === slug);
      const en_c = (window.COURSES_EN || {})[slug] || {};
      const cTitle = (en && en_c.title) ? en_c.title : (c && c.title);
      const cBlurb = (en && en_c.blurb) ? en_c.blurb : (c && c.blurb);
      title = cTitle ? `${cTitle} · ${SUFFIX}` : SUFFIX;
      desc = (cBlurb || "").slice(0, 160);
    } else if (route === "story") {
      const s = (window.STORIES || []).find((x) => x.slug === slug);
      if (s) {
        const sTitle = en
          ? (s.originalTitleEn || s.titleEn || s.originalTitle || s.title)
          : (s.originalTitle || s.title);
        const sLead = en ? (s.leadEn || s.lead) : (s.lead || s.leadEn);
        title = sTitle ? `${sTitle} · ${SUFFIX}` : SUFFIX;
        desc = (sLead || "").replace(/<[^>]+>/g, "").slice(0, 160);
      } else {
        title = SUFFIX;
        desc = "";
      }
    } else if (route === "sd-chapter") {
      const ch = (window.SYSTEM_DESIGN && window.SYSTEM_DESIGN.chapters || [])
        .find((x) => x.slug === slug);
      const chTitle = ch ? (en && ch.titleEn ? ch.titleEn : ch.title) : "";
      const chN = ch ? ch.n : "";
      title = chTitle ? `${chTitle} · ${SUFFIX}` : SUFFIX;
      if (chTitle && chN) {
        desc = en
          ? `Ch. ${chN}: ${chTitle} — original System Design Interview case study (VI & EN) by EngineerPro.`
          : `Chương ${chN}: ${chTitle} — case study System Design Interview gốc (VI & EN) biên soạn bởi EngineerPro.`;
      } else {
        desc = "";
      }
    } else {
      const label = labelFor(route);
      title = route === "home"
        ? (en
            ? "EngineerPro — Conquering Big Tech with battle-tested mentors"
            : "EngineerPro — Chinh phục Big Tech cùng mentor thực chiến")
        : `${label} · ${SUFFIX}`;
      // Counts derived from live data so descriptions can never drift.
      const nCourses  = (typeof courses  !== "undefined") ? courses.length  : 10;
      const nMentors  = (data && data.mentors) ? data.mentors.length : 19;
      const nStories  = (typeof stories  !== "undefined") ? stories.length  : 94;
      const ROUTE_DESC = {
        home:      en ? "100% mentors from Google, Amazon, TikTok, Shopee, Spotify, Uber. A clear roadmap to land Big Tech offers." : "100% mentors đến từ Google, Amazon, TikTok, Shopee, Spotify, Uber. Lộ trình rõ ràng để chinh phục offer Big Tech.",
        courses:   en ? `${nCourses} in-depth courses — DSA, System Design, Backend (Go/Java), Behavioural Interview, Machine Coding.` : `${nCourses} khoá đào tạo chuyên sâu — DSA, System Design, Backend (Go/Java), Behavioural Interview, Machine Coding.`,
        "lich-khai-giang": en ? "EngineerPro course launch schedule — DSA, System Design, CS Fundamentals, Backend Go, Redis crash course. Online classes, GMT+7." : "Lịch khai giảng các lớp mới tại EngineerPro — DSA, System Design, CS Fundamentals, Backend Go, Crash Course Redis. Lớp online, giờ GMT+7.",
        book:      en ? "Coding DSA Interview at Big Tech — 288 problems, 44 patterns, full solutions. Free for the community." : "Coding DSA Interview at Big Tech — 288 bài, 44 patterns, lời giải đầy đủ. Miễn phí cho cộng đồng.",
        "system-design": en ? "21 original System Design Interview case studies — read chapter by chapter (VI & EN). Original content by EngineerPro." : "21 case study System Design Interview gốc — đọc từng chương (VI & EN). Nội dung gốc bởi EngineerPro.",
        resources: en ? "Free interview resources from EngineerPro — HR phone screen checklist, programming foundation videos, Big Tech CV templates and review playlist." : "Tài nguyên phỏng vấn miễn phí từ EngineerPro — checklist HR phone screen, video lập trình nền tảng, template CV Big Tech và playlist review CV.",
        mentors:   en ? `${nMentors} mentors currently at Google, Amazon, Meta, TikTok, Spotify, Shopee, Acronis, AWS…` : `${nMentors} mentor đang làm tại Google, Amazon, Meta, TikTok, Spotify, Shopee, Acronis, AWS…`,
        stories:   en ? `${nStories}+ EngineerPro students landed offers at Google, Meta, Amazon, TikTok, Microsoft, Grab, Shopee, NAB, ANZ…` : `${nStories}+ học viên EngineerPro chinh phục offer tại Google, Meta, Amazon, TikTok, Microsoft, Grab, Shopee, NAB, ANZ…`,
        podcast:   en ? "EngineerPro podcast on Substack & Spotify — tech career and interview tips from Big Tech mentors." : "Podcast EngineerPro trên Substack & Spotify — tips sự nghiệp & phỏng vấn từ mentor Big Tech.",
        partners:  en ? "EngineerPro partners — organisations sharing the mission of bringing Vietnamese engineers into Big Tech." : "Đối tác EngineerPro — các tổ chức cùng sứ mệnh đưa kỹ sư Việt vươn ra Big Tech.",
        faq:       en ? "Frequently asked questions about EngineerPro courses, mentors, schedule, and admissions." : "Câu hỏi thường gặp về khoá học, mentor, lịch học và thủ tục đăng ký tại EngineerPro.",
        contact:   en ? "Reach EngineerPro on Messenger, Facebook, Zalo, Spotify, YouTube, Substack, Viblo." : "Liên hệ EngineerPro qua Messenger, Facebook, Zalo, Spotify, YouTube, Substack, Viblo.",
      };
      desc = ROUTE_DESC[route] || ROUTE_DESC.home;
    }
    document.title = title;

    setMeta('name', 'description', desc);
    setMeta('property', 'og:title', title);
    setMeta('property', 'og:description', desc);
    setMeta('name', 'twitter:title', title);
    setMeta('name', 'twitter:description', desc);

    // Canonical URL + og:url track the actual /path/ (no hash)
    const canon = location.origin + pathFor(route, slug);
    setLink('canonical', canon);
    setMeta('property', 'og:url', canon);
    setMeta('name', 'twitter:url', canon);
  }

  function setMeta(keyAttr, keyValue, content) {
    if (!content) return;
    let el = document.querySelector(`meta[${keyAttr}="${keyValue}"]`);
    if (!el) {
      el = document.createElement("meta");
      el.setAttribute(keyAttr, keyValue);
      document.head.appendChild(el);
    }
    el.setAttribute("content", content);
  }
  function setLink(rel, href) {
    let el = document.querySelector(`link[rel="${rel}"]`);
    if (!el) {
      el = document.createElement("link");
      el.setAttribute("rel", rel);
      document.head.appendChild(el);
    }
    el.setAttribute("href", href);
  }

  function labelFor(name, slug) {
    if (name === "course") {
      const c = (window.COURSES || []).find((x) => x.slug === slug);
      return c ? c.title : t("nav.courses");
    }
    if (name === "story") {
      const s = (window.STORIES || []).find((x) => x.slug === slug);
      return s ? (s.originalTitle || s.title) : t("nav.stories");
    }
    if (name === "sd-chapter") {
      const en = currentLang === "en";
      const ch = (window.SYSTEM_DESIGN && window.SYSTEM_DESIGN.chapters || [])
        .find((x) => x.slug === slug);
      if (!ch) return t("nav.systemDesign");
      return en && ch.titleEn ? ch.titleEn : ch.title;
    }
    return (
      {
        courses:   t("nav.courses"),
        "lich-khai-giang": t("nav.schedule"),
        book:      t("nav.book"),
        "system-design": t("nav.systemDesign"),
        resources: t("nav.resources"),
        mentors:   t("nav.mentors"),
        stories:   t("nav.stories"),
        podcast:   t("nav.podcast"),
        partners:  t("partners.head"),
        faq:       t("faq.head"),
        contact:   t("nav.contact"),
      }[name] || ""
    );
  }

  window.addEventListener("hashchange", () => {
    showRoute(parseHash());
    closeMobileNav();
  });
  // Back/forward through pushState'd path URLs also drives the SPA.
  window.addEventListener("popstate", () => {
    showRoute(parseHash());
    closeMobileNav();
  });

  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[data-route], a[data-href], a[href]");
    if (!a) return;
    // Skip modifier/middle clicks + new-tab + external links + downloads
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    if (a.getAttribute("target") === "_blank") return;
    if (a.hasAttribute("download")) return;

    const dataHref = a.getAttribute("data-href");
    const dataRoute = a.dataset.route;
    const rawHref = a.getAttribute("href") || "";

    // Anchor-style on home page (#home-format etc.) — route home + scroll.
    // Use pathFor() so the URL stays under BASE_PATH on project Pages deploys
    // (e.g. /interview-trainings/ instead of jumping to the origin root).
    const anchor = dataHref || (rawHref.startsWith("#home-") ? rawHref : null);
    if (anchor && anchor.startsWith("#home-")) {
      e.preventDefault();
      const anchorId = anchor.slice(1);
      // Reflect a clean, shareable URL for anchors that have one (/roadmap/,
      // /format/); otherwise stay on the home path.
      const alias = HOME_ANCHOR_PATHS[anchorId];
      const url = alias
        ? (BASE_PATH ? `${BASE_PATH}/${alias}/` : `/${alias}/`)
        : pathFor("home", null);
      history.pushState(null, "", url);
      showRoute({ route: "home", slug: null });
      requestAnimationFrame(() => {
        const target = document.getElementById(anchorId);
        if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
      });
      closeMobileNav();
      return;
    }

    // Compute the {route, slug} this link wants to navigate to.
    let target = null;
    if (dataRoute) {
      target = { route: dataRoute, slug: null };
    } else if (dataHref && dataHref.startsWith("#")) {
      const raw = dataHref.replace(/^#/, "");
      const [head, ...rest] = raw.split("/");
      if (head === "course" && rest.length) target = { route: "course", slug: rest.join("/") };
      else if (head === "story" && rest.length) target = { route: "story", slug: rest.join("/") };
      else if (head === "sd-chapter" && rest.length) target = { route: "sd-chapter", slug: rest.join("/") };
      else target = { route: head, slug: null };
    } else if (rawHref.startsWith("/") && !rawHref.startsWith("//")) {
      // Real path-based link e.g. /courses/foo/ — let parseHash classify it.
      try {
        const u = new URL(rawHref, location.origin);
        if (u.origin !== location.origin) return; // external — let browser handle
        // Temporarily simulate the target path through parseHash logic by
        // pushing state first, then parsing.
        e.preventDefault();
        history.pushState(null, "", u.pathname + u.search + u.hash);
        showRoute(parseHash());
        closeMobileNav();
        return;
      } catch (_) { /* fall through */ }
    }

    if (!target) return; // not one of ours; browser default
    e.preventDefault();

    const path = pathFor(target.route, target.slug);
    if (location.pathname !== path || location.hash !== "") {
      // Clear hash when navigating to a path-based route
      history.pushState(null, "", path);
    }
    showRoute(target);
    closeMobileNav();
  });

  // ===================== MOBILE NAV =====================
  const navLinks = document.getElementById("navLinks");
  const navToggle = document.getElementById("navToggle");
  function closeMobileNav() {
    navLinks?.classList.remove("is-open");
    navToggle?.classList.remove("is-open");
  }
  navToggle?.addEventListener("click", () => {
    navLinks.classList.toggle("is-open");
    navToggle.classList.toggle("is-open");
  });

  // ===================== HELPERS =====================
  const data = window.SITE_DATA || { mentors: [] };
  const courses = Array.isArray(window.COURSES) ? window.COURSES : [];
  const podcasts = Array.isArray(window.PODCASTS) ? window.PODCASTS : [];
  const faqs = Array.isArray(window.FAQS) ? window.FAQS : [];
  const resources = window.RESOURCES || null;
  const stories = Array.isArray(window.STORIES) ? window.STORIES : [];

  function el(tag, attrs = {}, children = []) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") node.className = v;
      else if (k === "html") node.innerHTML = v;
      else if (k.startsWith("on") && typeof v === "function")
        node.addEventListener(k.slice(2).toLowerCase(), v);
      else if (v !== false && v != null) node.setAttribute(k, v);
    }
    (Array.isArray(children) ? children : [children]).forEach((c) => {
      if (c == null || c === false) return;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function colorFor(name) {
    const palette = [
      ["#ff7a18", "#ff3b2d"],
      ["#0b1d3a", "#3a5fb8"],
      ["#16a34a", "#0e7c39"],
      ["#7c3aed", "#a855f7"],
      ["#0ea5e9", "#1e40af"],
      ["#db2777", "#7e22ce"],
      ["#f59e0b", "#b45309"],
      ["#0d9488", "#115e59"],
    ];
    let h = 0;
    for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0;
    return palette[h % palette.length];
  }

  function initials(name) {
    const parts = name.trim().split(/\s+/);
    return ((parts[0]?.[0] || "") + (parts[parts.length - 1]?.[0] || "")).toUpperCase();
  }

  function bookAuthorAvatar(author, size = 96) {
    if (author.photo) {
      return el("span", { class: "book-author-card__avatar book-author-card__avatar--photo" }, [
        el("img", {
          src: asset(author.photo),
          alt: author.name,
          loading: "lazy",
          width: String(size),
          height: String(size),
        }),
      ]);
    }
    const [c1, c2] = colorFor(author.name);
    const avatar = el("span", { class: "book-author-card__avatar" }, initials(author.name));
    avatar.style.background = `linear-gradient(135deg, ${c1}, ${c2})`;
    return avatar;
  }

  function bookAuthorCard(author) {
    const en = currentLang === "en";
    const role = en && author.roleEn ? author.roleEn : author.role;
    const actions = [
      el("a", {
        class: "book-author-card__btn book-author-card__btn--linkedin",
        href: author.linkedin,
        target: "_blank",
        rel: "noopener",
      }, [
        el("span", { class: "book-author-card__btn-icon", "aria-hidden": "true" }, "in"),
        t("book.author.linkedin"),
      ]),
    ];
    if (author.portfolio) {
      actions.push(
        el("a", {
          class: "book-author-card__btn book-author-card__btn--portfolio",
          href: author.portfolio,
          target: "_blank",
          rel: "noopener",
        }, [
          el("span", { class: "book-author-card__btn-icon", "aria-hidden": "true" }, "🌐"),
          t("book.author.portfolio"),
        ])
      );
    }
    return el("article", { class: "book-author-card" }, [
      bookAuthorAvatar(author),
      el("div", { class: "book-author-card__body" }, [
        el("h3", { class: "book-author-card__name" }, author.name),
        el("p", { class: "book-author-card__role" }, role),
        el("p", { class: "book-author-card__org" }, [
          `${t("book.author.cofounder")} `,
          el("strong", {}, "EngineerPro"),
        ]),
        el("div", { class: "book-author-card__actions" }, actions),
      ]),
    ]);
  }

  // ===================== COURSE LISTING =====================
  function deriveBadge(c) {
    const t = c.title.toLowerCase();
    if (t.includes("premium")) return "Premium";
    if (t.includes("level 2")) return "Advanced";
    if (t.includes("level 1") || t.includes("big tech")) return "Bestseller";
    if (t.includes("introduction") || t.includes("front end")) return "Foundation";
    if (t.includes("behaviour") || t.includes("english") || t.includes("tiếng anh")) return "English";
    if (t.includes("machine coding") || t.includes("low-level")) return "Mới";
    if (t.includes("dsa")) return "Career";
    if (t.includes("system design")) return "Architecture";
    if (t.includes("backend")) return "Backend";
    return "Course";
  }

  // Tag taxonomy — each entry maps a display label to keyword patterns.
  // `where: "all"` (default) matches against title+blurb. `where: "title"` only
  // matches the title — used for language tags where cross-referencing blurbs
  // would create false positives (e.g. the Golang course mentions Java).
  const TAG_RULES = [
    { tag: "DSA",                       patterns: ["dsa", "data structure", "algorithm", "thuật toán", "leetcode"] },
    { tag: "System Design Interview",   patterns: ["system design"] },
    { tag: "Coding Interview",          patterns: ["coding interview", "coding-interview", "machine coding"] },
    { tag: "Behavior Interview",        patterns: ["behaviour", "behavior", "leadership principles"] },
    { tag: "CS Fundamental",            patterns: ["fundamental", "computer science"] },
    { tag: "Low Level Design",          patterns: ["low-level", "low level design", "lld", "machine coding"] },
    { tag: "Backend",                   patterns: ["backend"], where: "title" },
    { tag: "Golang",                    patterns: ["golang"], where: "title" },
    { tag: "Java",                      patterns: ["java"], where: "title" },
    { tag: "Big Tech",                  patterns: ["big tech"] },
    { tag: "Crash Course",              patterns: ["crash course", "crash-course", "pet project", "build kafka", "build redis", "build mini database", "from scratch"] },
    { tag: "Build CV",                  patterns: ["build cv", "viết cv", "review cv", "làm cv", "cv writing", "cv mạnh"] },
    { tag: "Mentor Talk",               patterns: ["mini series", "tech tea", "sharing tips"] },
    { tag: "Career",                    patterns: ["career", "sự nghiệp", "bứt phá"] },
  ];

  function deriveTags(c) {
    const title = (c.title || "").toLowerCase();
    const blurb = (c.blurb || "").toLowerCase();
    const out = [];
    TAG_RULES.forEach((r) => {
      const hay = r.where === "title" ? title : title + " " + blurb;
      if (r.patterns.some((p) => hay.includes(p))) out.push(r.tag);
    });
    return out;
  }

  let activeTag = null; // null = show all

  function renderTagBar() {
    const wrap = document.getElementById("courseTags");
    if (!wrap) return;

    // Count courses per tag
    const counts = new Map();
    courses.forEach((c) => deriveTags(c).forEach((t) => counts.set(t, (counts.get(t) || 0) + 1)));
    // Only keep tags with ≥ 1 course; preserve TAG_RULES order
    const tags = TAG_RULES.map((r) => r.tag).filter((t) => counts.get(t));

    wrap.innerHTML = "";
    const allBtn = el("button", {
      class: "tag-chip" + (activeTag === null ? " is-active" : ""),
      type: "button",
      onClick: () => { activeTag = null; renderTagBar(); renderCourses(); },
    }, `${t("courses.filter.all")} · ${courses.length}`);
    wrap.appendChild(allBtn);

    tags.forEach((t) => {
      const chip = el("button", {
        class: "tag-chip" + (activeTag === t ? " is-active" : ""),
        type: "button",
        onClick: () => { activeTag = activeTag === t ? null : t; renderTagBar(); renderCourses(); },
      }, `${t} · ${counts.get(t)}`);
      wrap.appendChild(chip);
    });
  }

  function renderCourses() {
    const wrap = document.getElementById("coursesGrid");
    if (!wrap) return;
    wrap.innerHTML = "";

    const filtered = activeTag
      ? courses.filter((c) => deriveTags(c).includes(activeTag))
      : courses;

    // Most-enrolled courses first; courses without an enrolment figure
    // (e.g. machine coding, mini-series) fall to the bottom. Stable sort
    // keeps the original order within the same popularity tier.
    const enrollOf = (c) => COURSE_ENROLLED[c.slug] || 0;
    const ordered = filtered.slice().sort((a, b) => enrollOf(b) - enrollOf(a));

    const count = document.getElementById("coursesCount");
    if (count) count.textContent = courses.length;

    const empty = document.getElementById("coursesEmpty");
    if (empty) empty.hidden = filtered.length !== 0;

    const en = currentLang === "en";
    const enMap = (typeof window !== "undefined" && window.COURSES_EN) || {};

    ordered.forEach((c) => {
      const badge = deriveBadge(c);
      const tags = deriveTags(c);
      const tx = enMap[c.slug] || {};
      const cardTitle = en && tx.title ? tx.title : c.title;
      const cardBlurb = en && tx.blurb ? tx.blurb : c.blurb;
      const filterTitle = en ? `Filter by ${"%t%"}` : `Lọc theo ${"%t%"}`;
      const cover = c.cover
        ? el("img", { class: "card--course__cover", src: asset(c.cover), alt: cardTitle, loading: "lazy" })
        : el("div", { class: "card--course__cover card--course__cover--placeholder" }, "EP");

      const tagRow = el(
        "div",
        { class: "card--course__tags" },
        tags.slice(0, 4).map((tg) =>
          el(
            "button",
            {
              class: "tag-pill",
              type: "button",
              title: filterTitle.replace("%t%", tg),
              onClick: (e) => {
                e.preventDefault();
                e.stopPropagation();
                activeTag = activeTag === tg ? null : tg;
                renderTagBar();
                renderCourses();
                window.scrollTo({ top: 0, behavior: "smooth" });
              },
            },
            tg
          )
        )
      );

      const enrolled = COURSE_ENROLLED[c.slug];
      const enrollPill = enrolled
        ? el("span", { class: "enroll-pill enroll-pill--card", title: en ? "Students enrolled" : "Học viên đã đăng ký" }, [
            el("span", { class: "enroll-pill__spark", "aria-hidden": "true" }, "✨"),
            el("strong", {}, `${enrolled.toLocaleString("en-US")}+`),
            el("span", { class: "enroll-pill__label" }, en ? " students" : " học viên"),
          ])
        : null;

      const card = el("article", { class: "card card--course" }, [
        el(
          "a",
          { class: "card--course__media", href: `${BASE_PATH}/courses/${c.slug}/`, "data-href": `#course/${c.slug}` },
          enrollPill ? [cover, enrollPill] : cover
        ),
        el("div", { class: "card--course__body" }, [
          el("span", { class: "badge" }, badge),
          el(
            "h3",
            {},
            el("a", { href: `${BASE_PATH}/courses/${c.slug}/`, "data-href": `#course/${c.slug}`, class: "card--course__title" }, cardTitle)
          ),
          el("p", {}, cardBlurb),
          tags.length ? tagRow : null,
          el(
            "a",
            { class: "card__link", href: `${BASE_PATH}/courses/${c.slug}/`, "data-href": `#course/${c.slug}` },
            t("courses.card.viewMore")
          ),
        ]),
      ]);
      wrap.appendChild(card);
    });
  }

  // ===================== COURSE DETAIL =====================
  function renderCourseDetail(slug) {
    const wrap = document.getElementById("courseArticle");
    if (!wrap) return;
    const c = courses.find((x) => x.slug === slug);
    if (!c) {
      const notFound = currentLang === "en"
        ? '<h1>Course not found</h1><p>Invalid slug. <a data-href="#courses">Back to all courses</a>.</p>'
        : '<h1>Không tìm thấy khoá học</h1><p>Slug không hợp lệ. <a data-href="#courses">Về danh sách</a>.</p>';
      wrap.innerHTML = notFound;
      return;
    }

    const en = currentLang === "en";
    const enMap = (typeof window !== "undefined" && window.COURSES_EN) || {};
    const tx = enMap[c.slug] || {};
    const title = en && tx.title ? tx.title : c.title;
    const blurb = en && tx.blurb ? tx.blurb : c.blurb;

    // Body priority:
    //   EN mode  → c.htmlEn (machine-translated full body); fall back to c.html with a banner.
    //   VI mode  → c.html (original Vietnamese).
    const body = (en && c.htmlEn) ? c.htmlEn : c.html;
    const langNote = (en && !c.htmlEn)
      ? '<p class="lang-note">📌 The original course body below is in Vietnamese. Use your browser\'s auto-translate for the full read.</p>'
      : "";

    const cover = c.cover
      ? `<img class="article__cover" src="${escapeAttr(asset(c.cover))}" alt="${escapeAttr(title)}" />`
      : "";

    const enrolled = COURSE_ENROLLED[c.slug];
    const statHtml = enrolled
      ? `<div class="course-stat"><span class="course-stat__icon" aria-hidden="true">👥</span>
          <span><strong>${enrolled.toLocaleString("en-US")}+</strong> ${escapeText(en ? "students enrolled" : "học viên đã đăng ký")}</span>
        </div>`
      : "";

    wrap.innerHTML = `
      <header class="article__head">
        ${statHtml}
        <span class="badge">${escapeText(deriveBadge(c))}</span>
        <h1>${escapeText(title)}</h1>
        <p class="article__lede">${escapeText(blurb)}</p>
      </header>
      ${cover}
      ${langNote}
      <div class="article__body">${buttonifyContactLinks(rewriteAssetUrls(sanitizeHtml(body)))}</div>
      ${buildCourseReviews(c.slug)}
      <div class="article__cta">
        <a class="btn btn--primary" href="https://m.me/EngineerPro.Official" target="_blank" rel="noopener">
          ${escapeText(t("course.cta"))}
        </a>
        <a class="back-link" href="#courses" data-href="#courses">${escapeText(t("course.allCourses"))}</a>
      </div>
    `;
  }

  // Approximate cumulative enrolments per course (across cohorts), shown as a
  // trust badge at the top of each course page. DSA aggregates levels 1–3.
  const COURSE_ENROLLED = {
    "khoa-hoc-dsa": 750,
    "khoa-hoc-system-design-interview-big-tech": 400,
    "system-design-interview-level-2": 150,
    "khoa-hoc-backend-golang": 500,
    "backend-golang-level-2": 70,
    "khoa-hoc-backend-java": 200,
    "computer-science-fundamental-interview": 150,
    "crash-course-build-world-class-pet-project": 200,
    "behaviour-interview-course": 120,
    "mini-series-sharing-tips-for-tech-career": 40,
    "cracking-machine-coding-low-level-design-round": 20,
  };

  // Curated positive student reviews shown under each course (data in
  // window.COURSE_REVIEWS, extracted from post-course surveys).
  function buildCourseReviews(slug) {
    const all = (typeof window !== "undefined" && window.COURSE_REVIEWS) || {};
    const list = all[slug] || [];
    if (!list.length) return "";
    const en = currentLang === "en";
    const heading = en ? "What students say" : "Học viên nói gì về khoá học";
    const sub = en
      ? `${list.length} reviews from post-course student surveys`
      : `${list.length} cảm nhận từ khảo sát học viên sau khoá học`;
    const helpLabel = en ? "Mentor" : "Giảng viên";
    const items = list.map((r) => {
      const chip = r.three
        ? `<span class="course-review__chip">${escapeText(r.three)}</span>`
        : "";
      const help = r.help
        ? `<p class="course-review__help"><span class="course-review__help-label">${escapeText(helpLabel)}:</span> ${escapeText(r.help)}</p>`
        : "";
      const cohort = r.cohort
        ? ` <span class="course-review__cohort">${escapeText(r.cohort)}</span>`
        : "";
      return `
        <figure class="course-review">
          ${chip}
          <blockquote class="course-review__text">${escapeText(r.text)}</blockquote>
          ${help}
          <figcaption class="course-review__author">— ${escapeText(r.name)}${cohort}</figcaption>
        </figure>`;
    }).join("");
    return `
      <section class="course-reviews">
        <h2 class="course-reviews__title">${escapeText(heading)}</h2>
        <p class="course-reviews__sub muted">${escapeText(sub)}</p>
        <div class="course-reviews__grid">${items}</div>
      </section>`;
  }

  function normaliseHeading(s) {
    return String(s || "")
      .replace(/[\s\u00A0]+/g, " ")
      .replace(/[“”"’'`–—\-:;,.!?()]+/g, "")
      .trim()
      .toLowerCase();
  }

  function stripDuplicateHeading(html, title) {
    if (!html || !title) return html;
    const t = normaliseHeading(title);
    if (!t) return html;
    return html.replace(/^\s*<h([12])[^>]*>([\s\S]*?)<\/h\1>\s*/i, (full, _lvl, inner) => {
      const innerText = inner.replace(/<[^>]+>/g, "");
      const n = normaliseHeading(innerText);
      // strip if the body's first heading matches or is a substring of the page title
      if (!n) return "";
      if (n === t || t.includes(n) || n.includes(t)) return "";
      return full;
    });
  }

  function escapeText(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }
  function escapeAttr(s) {
    return escapeText(s).replace(/"/g, "&quot;");
  }

  // ===================== MENTORS =====================
  function renderMentors() {
    const wrap = document.getElementById("mentorsGrid");
    if (!wrap) return;
    wrap.innerHTML = "";
    const count = document.getElementById("mentorsCount");
    if (count) count.textContent = data.mentors.length;

    data.mentors.forEach((m) => {
      let avatar;
      if (m.photo) {
        avatar = el("img", {
          class: "avatar avatar--photo",
          src: asset(m.photo),
          alt: m.name,
          loading: "lazy",
        });
      } else {
        const [c1, c2] = colorFor(m.name);
        avatar = el("div", { class: "avatar" }, initials(m.name));
        avatar.style.background = `linear-gradient(135deg, ${c1}, ${c2})`;
      }

      const en = currentLang === "en";
      const updatingLabel = en ? "Coming soon" : "Đang cập nhật";
      const company = (m.current.company === "Đang cập nhật") ? updatingLabel : m.current.company;
      const current = el("div", { class: "mentor__line mentor__line--current" }, [
        el("span", { class: "mentor__role" }, m.current.role),
        el("span", { class: "mentor__sep" }, "@"),
        el("span", { class: "mentor__company" }, company),
      ]);

      // Wrap the role lines in a single .mentor__body cell so the card's
      // 4-row grid (avatar / name / body 1fr / cta) keeps the LinkedIn CTA
      // pinned to the same y across all cards in a row.
      const bodyChildren = [current];
      if (m.previous) {
        bodyChildren.push(
          el("div", { class: "mentor__line mentor__line--ex" }, [
            el("span", { class: "mentor__ex" }, "ex-"),
            el("span", {}, `${m.previous.role} @ ${m.previous.company}`),
          ])
        );
      }
      const body = el("div", { class: "mentor__body" }, bodyChildren);

      const children = [
        avatar,
        el("h3", {}, m.name),
        body,
      ];

      if (m.linkedin) {
        children.push(
          el(
            "a",
            { class: "mentor__cta", href: m.linkedin, target: "_blank", rel: "noopener" },
            [
              el("span", { class: "mentor__cta-icon" }, "in"),
              " " + t("mentors.cta.linkedin"),
            ]
          )
        );
      } else {
        children.push(
          el("span", { class: "mentor__cta mentor__cta--disabled" }, t("mentors.cta.disabled"))
        );
      }

      wrap.appendChild(el("article", { class: "card card--mentor" }, children));
    });
  }

  // ===================== PODCASTS =====================
  function renderPodcasts() {
    const wrap = document.getElementById("podcastGrid");
    if (!wrap) return;
    wrap.innerHTML = "";
    const count = document.getElementById("podcastCount");
    if (count) count.textContent = podcasts.length;

    podcasts.forEach((p) => {
      const metaRow = el("div", { class: "row" }, [
        p.series && el("span", { class: "series" }, p.series),
        p.date && el("span", {}, p.date),
        p.duration && el("span", { class: "duration" }, p.duration),
      ]);

      const card = el(
        "a",
        {
          class: "card card--podcast",
          href: p.url,
          target: "_blank",
          rel: "noopener",
          title: p.title,
        },
        [
          el("div", { class: "play" }, "▶"),
          el("div", { class: "meta" }, [
            el("h3", {}, p.title),
            metaRow,
            p.blurb && el("p", { class: "podcast__blurb" }, p.blurb),
            el("span", { class: "podcast__cta" }, t("podcast.card.cta")),
          ]),
        ]
      );
      wrap.appendChild(card);
    });
  }

  // ===================== BOOK =====================
  function renderBook() {
    const book = data.book;
    if (!book) return;

    const titleEl = document.getElementById("bookTitle");
    if (titleEl) titleEl.textContent = book.title;

    const subEl = document.getElementById("bookSubtitle");
    if (subEl) subEl.textContent = book.subtitle;

    const authorsEl = document.getElementById("bookAuthors");
    if (authorsEl) {
      authorsEl.innerHTML = "";
      book.authors.forEach((a) => authorsEl.appendChild(bookAuthorCard(a)));
    }

    [["bookReadEn", book.urlEn], ["bookReadEn2", book.urlEn], ["bookReadVi", book.urlVi]].forEach(
      ([id, href]) => {
        const link = document.getElementById(id);
        if (link) link.href = href;
      }
    );

    const statsEl = document.getElementById("bookStats");
    if (statsEl) {
      statsEl.innerHTML = "";
      book.stats.forEach((s) =>
        statsEl.appendChild(
          el("div", { class: "stat" }, [
            el("div", { class: "stat__num" }, s.num),
            el("div", { class: "stat__label" }, s.label),
          ])
        )
      );
    }

    const hiEl = document.getElementById("bookHighlights");
    if (hiEl) {
      hiEl.innerHTML = "";
      const icons = ["🐍", "🧩", "⚠️", "🌐", "🎓"];
      const highlights = (currentLang === "en" && book.highlightsEn) ? book.highlightsEn : book.highlights;
      highlights.forEach((text, i) => {
        hiEl.appendChild(
          el("article", { class: "card card--pillar" }, [
            el("div", { class: "card__icon" }, icons[i] || "✓"),
            el("h3", {}, text.split(" — ")[0] || text),
            el("p", {}, text),
          ])
        );
      });
    }

    const chEl = document.getElementById("bookChapters");
    if (chEl) {
      chEl.innerHTML = "";
      // group by .group
      const groups = new Map();
      book.chapters.forEach((c) => {
        if (!groups.has(c.group)) groups.set(c.group, []);
        groups.get(c.group).push(c);
      });
      groups.forEach((items, name) => {
        const grp = el("div", { class: "book-group" }, [
          el("h3", { class: "book-group__name" }, name),
          el("div", { class: "book-group__items" }, items.map((c) =>
            el("a", {
              class: "book-chapter",
              href: `${book.urlEn}#${c.anchor || `chapter-${c.n}`}`,
              target: "_blank",
              rel: "noopener",
              title: `Chapter ${c.n} — ${c.title}`,
            }, [
              el("span", { class: "book-chapter__n" }, String(c.n)),
              el("span", { class: "book-chapter__title" }, c.title),
            ])
          )),
        ]);
        chEl.appendChild(grp);
      });
    }
  }

  // ===================== SYSTEM DESIGN =====================
  const sdChapterCache = new Map();
  let sdChapterRequest = 0;

  function sdLang() {
    return currentLang === "en" ? "en" : "vi";
  }

  function getSdChapter(slug) {
    return (window.SYSTEM_DESIGN && window.SYSTEM_DESIGN.chapters || [])
      .find((x) => x.slug === slug);
  }

  async function loadSdChapterBody(slug, lang) {
    const key = `${lang}:${slug}`;
    if (sdChapterCache.has(key)) return sdChapterCache.get(key);
    const url = asset(`assets/content/system-design/${lang}/${slug}.html`);
    const res = await fetch(url);
    if (!res.ok) throw new Error(`chapter ${slug} (${lang}) not found`);
    const html = await res.text();
    sdChapterCache.set(key, html);
    return html;
  }

  function sdChapterFooterHtml() {
    const sd = window.SYSTEM_DESIGN || {};
    const en = currentLang === "en";
    const credit = en && sd.creditEn ? sd.creditEn : (sd.credit || "");
    const refNote = t("sd.chapter.refNote");
    const course1 = pathFor("course", "khoa-hoc-system-design-interview-big-tech");
    const course2 = pathFor("course", "system-design-interview-level-2");
    return `
      <footer class="sd-chapter-foot">
        ${credit ? `<p class="muted sd-chapter-credit">${escapeText(credit)}</p>` : ""}
        ${refNote ? `<p class="muted sd-chapter-ref">${escapeText(refNote)}</p>` : ""}
        <div class="sd-chapter-promo">
          <p class="sd-chapter-promo__lead">${escapeText(t("sd.chapter.promo.lead"))}</p>
          <div class="sd-chapter-promo__cta">
            <a class="btn btn--ghost" href="${escapeText(course1)}" data-href="#course/khoa-hoc-system-design-interview-big-tech">${escapeText(t("sd.cta.l1"))}</a>
            <a class="btn btn--ghost" href="${escapeText(course2)}" data-href="#course/system-design-interview-level-2">${escapeText(t("sd.cta.l2"))}</a>
            <a class="btn btn--primary" href="https://m.me/EngineerPro.Official" target="_blank" rel="noopener">${escapeText(t("sd.chapter.promo.fanpage"))}</a>
          </div>
        </div>
      </footer>
    `;
  }

  function renderSystemDesign() {
    const sd = window.SYSTEM_DESIGN;
    if (!sd) return;
    const en = currentLang === "en";

    const titleEl = document.getElementById("sdTitle");
    if (titleEl) titleEl.textContent = en && sd.titleEn ? sd.titleEn : sd.title;

    const introEl = document.getElementById("sdIntro");
    if (introEl) introEl.textContent = en && sd.introEn ? sd.introEn : sd.intro;

    const creditEl = document.getElementById("sdCredit");
    if (creditEl) {
      creditEl.textContent = en && sd.creditEn ? sd.creditEn : (sd.credit || "");
    }

    const attrEl = document.getElementById("sdAttribution");
    if (attrEl) {
      attrEl.textContent = en && sd.attributionEn ? sd.attributionEn : sd.attribution;
    }

    const authorsEl = document.getElementById("sdAuthors");
    if (authorsEl) {
      authorsEl.innerHTML = "";
      (sd.authors || []).forEach((a) => authorsEl.appendChild(bookAuthorCard(a)));
    }

    const chEl = document.getElementById("sdChapters");
    if (!chEl) return;
    chEl.innerHTML = "";

    const itemsWrap = el("div", { class: "book-group__items" });
    (sd.chapters || []).forEach((c) => {
      const title = en && c.titleEn ? c.titleEn : c.title;
      const href = `${BASE_PATH}/${SD_URL_SLUG}/${c.slug}/`;
      const attrs = {
        class: "book-chapter" + (c.available ? "" : " book-chapter--soon"),
        href: c.available ? href : "#",
        title: `${c.n}. ${title}`,
      };
      if (c.available) {
        attrs["data-href"] = `#sd-chapter/${c.slug}`;
      } else {
        attrs["aria-disabled"] = "true";
      }
      const children = [
        el("span", { class: "book-chapter__n" }, String(c.n)),
        el("span", { class: "book-chapter__title" }, title),
      ];
      if (!c.available) {
        children.push(el("span", { class: "sd-soon-badge" }, t("sd.chapter.badgeSoon")));
      }
      itemsWrap.appendChild(el("a", attrs, children));
    });
    chEl.appendChild(itemsWrap);
  }

  // Lazy-load the vendored Mermaid bundle (only on chapters that use diagrams).
  let mermaidLoadingPromise = null;
  const mermaidSrc = new WeakMap(); // node -> original diagram definition (for re-theming)

  function mermaidTheme() {
    return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "neutral";
  }
  function initMermaid() {
    try {
      window.mermaid.initialize({
        startOnLoad: false,
        securityLevel: "strict",
        theme: mermaidTheme(),
        flowchart: { useMaxWidth: true, htmlLabels: true },
        sequence: { useMaxWidth: true },
      });
    } catch (e) { /* ignore init errors */ }
  }
  function ensureMermaid() {
    if (window.mermaid) return Promise.resolve(window.mermaid);
    if (mermaidLoadingPromise) return mermaidLoadingPromise;
    mermaidLoadingPromise = new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = asset("assets/vendor/mermaid.min.js");
      s.async = true;
      s.onload = () => { initMermaid(); resolve(window.mermaid); };
      s.onerror = reject;
      document.head.appendChild(s);
    });
    return mermaidLoadingPromise;
  }

  // Render any <pre class="mermaid"> diagrams inside a freshly-injected container.
  async function renderMermaidIn(container) {
    if (!container) return;
    const nodes = [...container.querySelectorAll("pre.mermaid, .mermaid")];
    if (!nodes.length) return;
    // Stash each diagram's source so we can re-render it on a theme switch.
    nodes.forEach((n) => { if (!mermaidSrc.has(n)) mermaidSrc.set(n, n.textContent); });
    try {
      const m = await ensureMermaid();
      const pending = nodes.filter((n) => n.getAttribute("data-processed") !== "true");
      if (pending.length) await m.run({ nodes: pending });
    } catch (e) { /* leave diagram source visible if rendering fails */ }
  }

  // Re-render on-page diagrams when the colour theme changes (light <-> dark).
  async function rethemeMermaid() {
    if (!window.mermaid) return; // nothing rendered yet
    const nodes = [...document.querySelectorAll("pre.mermaid, .mermaid")]
      .filter((n) => mermaidSrc.has(n));
    if (!nodes.length) return;
    nodes.forEach((n) => {
      n.innerHTML = "";
      n.textContent = mermaidSrc.get(n);
      n.removeAttribute("data-processed");
    });
    initMermaid();
    try { await window.mermaid.run({ nodes }); } catch (e) { /* ignore */ }
  }

  function renderSdChapter(slug) {
    const wrap = document.getElementById("sdChapterArticle");
    if (!wrap) return;
    const ch = getSdChapter(slug);
    const en = currentLang === "en";
    const title = ch ? (en && ch.titleEn ? ch.titleEn : ch.title) : "";

    if (!ch) {
      wrap.innerHTML = en
        ? "<h1>Chapter not found</h1><p><a data-href=\"#system-design\" href=\"" + pathFor("system-design") + "\">Back to list</a></p>"
        : "<h1>Không tìm thấy chương</h1><p><a data-href=\"#system-design\" href=\"" + pathFor("system-design") + "\">Về danh sách</a></p>";
      return;
    }

    if (!ch.available) {
      wrap.innerHTML = `
        <header class="article__head">
          <span class="badge">${escapeText(t("sd.chapter.badgeSoon"))}</span>
          <h1>${escapeText(title)}</h1>
        </header>
        <div class="article__body"><p>${t("sd.chapter.comingSoon")}</p></div>
      `;
      return;
    }

    const reqId = ++sdChapterRequest;
    wrap.innerHTML = `
      <header class="article__head">
        <span class="badge">Ch. ${escapeText(String(ch.n))}</span>
        <h1>${escapeText(title)}</h1>
      </header>
      <div class="article__body"><p class="muted">${escapeText(t("sd.chapter.loading"))}</p></div>
    `;

    loadSdChapterBody(slug, sdLang())
      .then((html) => {
        if (reqId !== sdChapterRequest) return;
        const body = buttonifyContactLinks(rewriteAssetUrls(sanitizeHtml(html)));
        wrap.innerHTML = `
          <header class="article__head">
            <span class="badge">Ch. ${escapeText(String(ch.n))}</span>
            <h1>${escapeText(title)}</h1>
          </header>
          <div class="article__body">${body}</div>
          ${sdChapterFooterHtml()}
        `;
        renderMermaidIn(wrap);
      })
      .catch(() => {
        if (reqId !== sdChapterRequest) return;
        wrap.innerHTML = `
          <header class="article__head">
            <h1>${escapeText(title)}</h1>
          </header>
          <div class="article__body"><p>${t("sd.chapter.error")}</p></div>
        `;
      });
  }

  // ===================== FAQ =====================
  // Promote bare Facebook / Messenger / Zalo URLs inside FAQ answers to
  // styled CTA buttons. Detects by hostname; ignores already-styled links
  // (anything with a class= attribute).
  function buttonifyContactLinks(html) {
    if (!html) return html;
    const HOSTS = {
      "facebook.com":  { label: { vi: "Mở Fanpage trên Facebook →", en: "Open the Fanpage on Facebook →" }, cls: "btn btn--primary faq-cta faq-cta--fb" },
      "fb.com":        { label: { vi: "Mở Fanpage trên Facebook →", en: "Open the Fanpage on Facebook →" }, cls: "btn btn--primary faq-cta faq-cta--fb" },
      "m.me":          { label: { vi: "Chat trên Messenger →",      en: "Chat on Messenger →" },           cls: "btn btn--primary faq-cta faq-cta--msg" },
      "messenger.com": { label: { vi: "Chat trên Messenger →",      en: "Chat on Messenger →" },           cls: "btn btn--primary faq-cta faq-cta--msg" },
      "zalo.me":       { label: { vi: "Mở Zalo →",                  en: "Open Zalo →" },                   cls: "btn btn--primary faq-cta faq-cta--zalo" },
    };
    const lang = (typeof currentLang !== "undefined" && currentLang === "en") ? "en" : "vi";
    return html.replace(
      /<a\s+([^>]*?)href="([^"]+)"([^>]*)>([\s\S]*?)<\/a>/gi,
      (full, pre, href, post, _inner) => {
        // skip already-styled links (anything with class=)
        if (/\bclass=/.test(pre + post)) return full;
        let host;
        try { host = new URL(href, location.href).host.replace(/^www\./, ""); }
        catch (_) { return full; }
        const cfg = Object.entries(HOSTS).find(([h]) => host === h || host.endsWith("." + h) || host === "www." + h);
        if (!cfg) return full;
        const [, { label, cls }] = cfg;
        const text = label[lang] || label.vi;
        return `<a class="${cls}" href="${href}" target="_blank" rel="noopener">${text}</a>`;
      }
    );
  }

  // FAQ enrichment: spot YouTube URLs inside the html and append a responsive
  // 16:9 iframe right after the matching <a>, so readers can watch the linked
  // video inline without leaving the page. Idempotent — skip if an embed for
  // the same video id is already present.
  function embedYouTubeLinks(html) {
    if (!html) return html;
    const VID_RE = /(?:youtube\.com\/(?:watch\?(?:[^"']*?[?&])?v=|embed\/|v\/)|youtu\.be\/)([A-Za-z0-9_-]{11})/g;
    return html.replace(
      /<a\s+([^>]*?)href="([^"]+)"([^>]*)>([\s\S]*?)<\/a>/gi,
      (full, pre, href, post, inner) => {
        VID_RE.lastIndex = 0;
        const m = VID_RE.exec(href);
        if (!m) return full;
        const vid = m[1];
        // already embedded?
        if (html.includes(`youtube.com/embed/${vid}`)) return full;
        // Use youtube-nocookie + lite cosmetic params (cleaner player,
        // no "Watch on YouTube" overlay, less crowded thumbnail).
        // loading="lazy" defers off-screen FAQ videos until scrolled to.
        const src =
          `https://www.youtube-nocookie.com/embed/${vid}` +
          `?rel=0&modestbranding=1&playsinline=1`;
        const embed =
          `<div class="embed-16x9" style="margin:0.5rem 0 0.75rem;">` +
          `<iframe src="${src}" ` +
          `title="YouTube video" loading="lazy" frameborder="0" allowfullscreen ` +
          `allow="accelerometer; encrypted-media; picture-in-picture"></iframe>` +
          `</div>`;
        return full + embed;
      }
    );
  }

  function renderFAQ() {
    const wrap = document.getElementById("faqList");
    if (!wrap) return;
    const count = document.getElementById("faqCount");
    if (count) count.textContent = faqs.length;

    wrap.innerHTML = "";
    faqs.forEach((f, i) => {
      const q    = currentLang === "en" ? (f.questionEn || f.question) : f.question;
      const html = currentLang === "en" ? (f.htmlEn     || f.html)     : f.html;
      const enriched = embedYouTubeLinks(buttonifyContactLinks(rewriteAssetUrls(sanitizeHtml(html))));
      const item = el(
        "details",
        {
          class: "faq-item",
          "data-q": (q + " " + (f.plain || "")).toLowerCase(),
        },
        [
          el(
            "summary",
            { class: "faq-item__q" },
            [
              el("span", { class: "faq-item__n" }, String(i + 1)),
              el("span", { class: "faq-item__qtext" }, q),
              el("span", { class: "faq-item__chevron", "aria-hidden": "true" }, "›"),
            ]
          ),
          el("div", { class: "faq-item__a", html: enriched }),
        ]
      );
      wrap.appendChild(item);
    });

    // Search
    const search = document.getElementById("faqSearch");
    const empty = document.getElementById("faqEmpty");
    const apply = () => {
      const q = (search?.value || "").trim().toLowerCase();
      let visible = 0;
      wrap.querySelectorAll(".faq-item").forEach((it) => {
        const match = !q || it.dataset.q.includes(q);
        it.hidden = !match;
        if (match) visible++;
      });
      if (empty) empty.hidden = visible !== 0;
    };
    if (search) search.addEventListener("input", apply);

    // Expand / collapse all
    document.getElementById("faqExpandAll")?.addEventListener("click", () => {
      wrap.querySelectorAll(".faq-item").forEach((it) => (it.open = true));
    });
    document.getElementById("faqCollapseAll")?.addEventListener("click", () => {
      wrap.querySelectorAll(".faq-item").forEach((it) => (it.open = false));
    });
  }

  function syncResourceExpandLabels() {
    const expand = t("resources.expandOne");
    const collapse = t("resources.collapseOne");
    document.querySelectorAll("details.faq-item .faq-item__action").forEach((label) => {
      const item = label.closest("details");
      if (item) label.textContent = item.open ? collapse : expand;
    });
  }

  function initResourcesPanels() {
    const list = document.getElementById("resourcesPanels");
    if (!list) return;

    const search = document.getElementById("resourcesSearch");
    const empty = document.getElementById("resourcesEmpty");

    const apply = () => {
      const q = (search?.value || "").trim().toLowerCase();
      let visible = 0;
      list.querySelectorAll(":scope > details.resource-panel").forEach((it) => {
        const show = !q || it.textContent.toLowerCase().includes(q);
        it.hidden = !show;
        if (show) {
          visible++;
          if (q) it.open = true;
        }
      });
      if (empty) empty.hidden = visible !== 0;
      if (typeof syncResourceExpandLabels === "function") syncResourceExpandLabels();
    };
    if (search) search.addEventListener("input", apply);

    list.querySelectorAll(":scope > details.resource-panel").forEach((it) => {
      it.addEventListener("toggle", syncResourceExpandLabels);
    });
    syncResourceExpandLabels();

    document.getElementById("resourcesExpandAll")?.addEventListener("click", () => {
      list.querySelectorAll(":scope > details.resource-panel:not([hidden])").forEach((it) => {
        it.open = true;
      });
      document.querySelectorAll("#hrChecklist .faq-item, #pipChecklist .faq-item, #csFundamentalList .faq-item").forEach((it) => {
        it.open = true;
      });
      syncResourceExpandLabels();
    });
    document.getElementById("resourcesCollapseAll")?.addEventListener("click", () => {
      list.querySelectorAll(":scope > details.resource-panel").forEach((it) => {
        it.open = false;
      });
      document.querySelectorAll("#hrChecklist .faq-item, #pipChecklist .faq-item, #csFundamentalList .faq-item").forEach((it) => {
        it.open = false;
      });
      syncResourceExpandLabels();
    });
  }

  function initHrChecklist() {
    const list = document.getElementById("hrChecklist");
    if (!list) return;

    const search = document.getElementById("hrSearch");
    const empty = document.getElementById("hrEmpty");

    const apply = () => {
      const q = (search?.value || "").trim().toLowerCase();
      let visible = 0;
      list.querySelectorAll(":scope > .faq-item").forEach((it) => {
        const show = !q || it.textContent.toLowerCase().includes(q);
        it.hidden = !show;
        if (show) {
          visible++;
          if (q) it.open = true;
        }
      });
      if (empty) empty.hidden = visible !== 0;
      if (typeof syncResourceExpandLabels === "function") syncResourceExpandLabels();
    };
    if (search) search.addEventListener("input", apply);

    list.querySelectorAll(":scope > .faq-item").forEach((it) => {
      it.addEventListener("toggle", syncResourceExpandLabels);
    });
    syncResourceExpandLabels();

    document.getElementById("hrExpandAll")?.addEventListener("click", () => {
      const hrPanel = document.getElementById("resHrScreen");
      if (hrPanel && !hrPanel.open) hrPanel.open = true;
      list.querySelectorAll(":scope > .faq-item:not([hidden])").forEach((it) => {
        it.open = true;
      });
      syncResourceExpandLabels();
    });
    document.getElementById("hrCollapseAll")?.addEventListener("click", () => {
      list.querySelectorAll(":scope > .faq-item").forEach((it) => {
        it.open = false;
      });
      syncResourceExpandLabels();
    });
  }

  function formatCsSourceLabel(item, lang) {
    if (item.sourceLabel) return item.sourceLabel;

    const company = (item.company || "Big Tech").split(",")[0].trim();
    const outcomeNoise = /^(reject(ed)?|offer|selected|pending|failed|passed|waiting|pass\/fail)$/i;
    const yoeNoise = /^\d+(\.\d+)?\s*yoe$/i;
    const dateNoise = /\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{4}\b/i;
    const metaTitleNoise =
      /\b(journey|my journey|prep journey|experience journey|interview experience|chances|expectations|overview|story|guide|how i|lessons from|worst interview)\b/i;
    const roleHint =
      /\b(SDE-?\d*|SSE|E\d+|L\d+|L60|MTS-?\d*|SWE\s*\d*|Staff|Senior|Software Engineer|Data Engineer|Cloud Support|Human Engineering|Product Engineer|Analyst|Intern|Infra|Level\s*\d+[A-Z]?|AA Round|Bar Raiser|phone screen)\b/i;
    const locationRe =
      /\b(bangalore|bengaluru|hyderabad|chennai|mumbai|pune|delhi|india|usa|us|singapore|london|seattle|cupertino|germany|switzerland|mountain view|san francisco|blr|nyc|new york|vietnam|vn|sg)\b/i;
    const companyRe = new RegExp(`\\b${company.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`, "i");

    const parts = (item.sourceTitle || "")
      .split("|")
      .map((s) => s.replace(/\[.*?\]/g, "").trim())
      .filter(Boolean)
      .filter((s) => !outcomeNoise.test(s))
      .filter((s) => !yoeNoise.test(s))
      .filter((s) => !metaTitleNoise.test(s) || roleHint.test(s));

    const roles = [];
    const locations = [];

    for (const part of parts) {
      if (companyRe.test(part) && part.length <= company.length + 12) continue;
      if (/^(aws|amazon|google|meta|microsoft|apple|uber|linkedin|oracle|bytedance|dropbox)$/i.test(part)) {
        continue;
      }
      if (locationRe.test(part) && !roleHint.test(part)) {
        locations.push(part.trim());
        continue;
      }
      const cleaned = part
        .replace(/\b(interview experience|phone screen|tech screen|technical phone screen|onsite|full interview experience)\b/gi, "")
        .replace(companyRe, "")
        .replace(/\s{2,}/g, " ")
        .trim();
      if (!cleaned || cleaned.length <= 2 || companyRe.test(cleaned)) continue;
      if (metaTitleNoise.test(cleaned) && !roleHint.test(cleaned)) continue;
      if (dateNoise.test(cleaned) && !roleHint.test(cleaned)) continue;
      if (/^[\w\s-]+:\s/.test(cleaned) && !roleHint.test(cleaned)) continue;
      if (!roleHint.test(cleaned) && (cleaned.length > 48 || /\d{4}/.test(cleaned))) continue;
      roles.push(cleaned);
    }

    const roleStr = [...new Set(roles)].slice(0, 2).join(" · ");
    const locStr = [...new Set(locations)].slice(0, 2).join(" · ");

    if (lang === "en") {
      let s = `Source: ${company} interview`;
      if (roleStr) s += ` — ${roleStr}`;
      if (locStr) s += ` · ${locStr}`;
      return `${s}.`;
    }
    let s = `Nguồn: Phỏng vấn ${company}`;
    if (roleStr) s += `, vị trí ${roleStr}`;
    if (locStr) s += ` · ${locStr}`;
    return `${s}.`;
  }

  function initCsFundamentalList() {
    const list = document.getElementById("csFundamentalList");
    if (!list) return;

    const data = window.CS_FUNDAMENTAL_QUESTIONS || [];
    const search = document.getElementById("csFundamentalSearch");
    const topicSel = document.getElementById("csFundamentalTopic");
    const empty = document.getElementById("csFundamentalEmpty");
    const meta = document.getElementById("csFundamentalMeta");
    const lang = document.documentElement.lang || "vi";

    const topics = [...new Set(data.map((q) => q.topic).filter(Boolean))].sort();
    if (topicSel && topicSel.options.length <= 1) {
      topics.forEach((t) => {
        const opt = document.createElement("option");
        opt.value = t;
        opt.textContent = t;
        topicSel.appendChild(opt);
      });
    }

    const render = () => {
      list.innerHTML = "";
      const q = (search?.value || "").trim().toLowerCase();
      const topic = topicSel?.value || "";
      let visible = 0;

      data.forEach((item, idx) => {
        const hay = `${item.question} ${item.company} ${item.topic} ${item.sourceTitle} ${formatCsSourceLabel(item, lang)}`.toLowerCase();
        const show = (!q || hay.includes(q)) && (!topic || item.topic === topic);
        if (!show) return;
        visible++;

        const details = document.createElement("details");
        details.className = "faq-item cs-fundamental__item";

        const summary = document.createElement("summary");
        summary.className = "faq-item__q";

        const num = document.createElement("span");
        num.className = "faq-item__n";
        num.textContent = String(idx + 1);

        const qtext = document.createElement("span");
        qtext.className = "faq-item__qtext";
        qtext.textContent = item.question;

        const action = document.createElement("span");
        action.className = "faq-item__action";
        action.setAttribute("data-i18n", "resources.expandOne");

        const chevron = document.createElement("span");
        chevron.className = "faq-item__chevron";
        chevron.setAttribute("aria-hidden", "true");
        chevron.textContent = "›";

        summary.append(num, qtext, action, chevron);

        const body = document.createElement("div");
        body.className = "faq-item__a cs-fundamental__detail";

        const badges = document.createElement("p");
        badges.className = "cs-fundamental__badges";
        badges.innerHTML =
          `<span class="cs-fundamental__badge cs-fundamental__badge--company">${escapeText(item.company)}</span>` +
          `<span class="cs-fundamental__badge cs-fundamental__badge--topic">${escapeText(item.topic)}</span>`;

        const source = document.createElement("p");
        source.className = "muted cs-fundamental__source";
        source.textContent = formatCsSourceLabel(item, lang);

        body.append(badges, source);
        details.append(summary, body);
        list.appendChild(details);

        if (q || topic) details.open = true;
      });

      if (empty) empty.hidden = visible !== 0;
      if (meta) {
        const total = data.length;
        meta.textContent =
          lang === "en"
            ? `${visible} of ${total} questions shown · crawled from LeetCode Discuss`
            : `Hiển thị ${visible}/${total} câu · crawl từ LeetCode Discuss`;
      }
      if (typeof syncResourceExpandLabels === "function") syncResourceExpandLabels();
    };

    render();
    search?.addEventListener("input", render);
    topicSel?.addEventListener("change", render);

    list.addEventListener("toggle", (ev) => {
      if (ev.target.matches(".faq-item")) syncResourceExpandLabels();
    }, true);

    document.getElementById("csFundamentalExpandAll")?.addEventListener("click", () => {
      const panel = document.getElementById("resCsFundamental");
      if (panel && !panel.open) panel.open = true;
      list.querySelectorAll(":scope > .faq-item:not([hidden])").forEach((it) => {
        it.open = true;
      });
      syncResourceExpandLabels();
    });
    document.getElementById("csFundamentalCollapseAll")?.addEventListener("click", () => {
      list.querySelectorAll(":scope > .faq-item").forEach((it) => {
        it.open = false;
      });
      syncResourceExpandLabels();
    });
  }

  function initInterviewFormats() {
    const data = window.INTERVIEW_FORMATS || [];
    const list = document.getElementById("interviewFormatsList");
    if (!list || !data.length) return;

    const search = document.getElementById("interviewFormatsSearch");
    const companySel = document.getElementById("interviewFormatsCompany");
    const empty = document.getElementById("interviewFormatsEmpty");
    const meta = document.getElementById("interviewFormatsMeta");

    if (companySel && companySel.options.length <= 1) {
      data.forEach((co) => {
        const opt = document.createElement("option");
        opt.value = co.id;
        opt.textContent = co.company;
        companySel.appendChild(opt);
      });
    }

    function appendBullets(parent, bullets) {
      if (!bullets?.length) return;
      const ul = document.createElement("ul");
      bullets.forEach((b) => {
        const li = document.createElement("li");
        li.textContent = b;
        ul.appendChild(li);
      });
      parent.appendChild(ul);
    }

    function appendBlocks(parent, blocks) {
      if (!blocks?.length) return;
      blocks.forEach((block) => {
        const wrap = document.createElement("div");
        wrap.className = "interview-formats__block";
        const head = document.createElement("p");
        head.className = "interview-formats__block-head";
        head.textContent = `${block.icon ? block.icon + " " : ""}${block.title}`;
        wrap.appendChild(head);
        appendBullets(wrap, block.bullets);
        parent.appendChild(wrap);
      });
    }

    function buildProfileBody(profile) {
      const body = document.createElement("div");
      body.className = "faq-item__a interview-formats__profile-body";
      (profile.sections || []).forEach((sec) => {
        const secEl = document.createElement("div");
        secEl.className = "interview-formats__section";
        const h = document.createElement("h5");
        h.className = "interview-formats__section-title";
        h.textContent = sec.title;
        secEl.appendChild(h);
        appendBullets(secEl, sec.bullets);
        appendBlocks(secEl, sec.blocks);
        body.appendChild(secEl);
      });
      return body;
    }

    function courseTitleForSlug(slug, lang) {
      const c = (window.COURSES || []).find((x) => x.slug === slug);
      if (!c) return slug;
      const enMap = window.COURSES_EN || {};
      const en = enMap[slug];
      if (lang === "en" && en?.title) return en.title;
      return c.title;
    }

    function buildRecommendations(co, langNow) {
      if (!co.recommendations?.length) return null;
      const dict = window.I18N?.[langNow] || window.I18N?.vi || {};
      const box = document.createElement("div");
      box.className = "interview-formats__reco";
      const title = document.createElement("p");
      title.className = "interview-formats__reco-title";
      title.textContent = `${dict["resources.formats.reco.title"] || "Khóa EngineerPro gợi ý"} — ${co.company}`;
      box.appendChild(title);
      const ul = document.createElement("ul");
      ul.className = "interview-formats__reco-list";
      co.recommendations.forEach((rec) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        if (rec.slug === "mock") {
          a.href = pathFor("mock");
          a.textContent = dict["resources.formats.reco.mock"] || "Mock Interview 1-1";
        } else {
          a.href = pathFor("course", rec.slug);
          a.textContent = courseTitleForSlug(rec.slug, langNow);
        }
        li.appendChild(a);
        if (rec.note) {
          const note = document.createElement("span");
          note.className = "interview-formats__reco-note muted";
          note.textContent = ` — ${rec.note}`;
          li.appendChild(note);
        }
        ul.appendChild(li);
      });
      box.appendChild(ul);
      return box;
    }

    function buildCompanyBody(co, langNow) {
      const body = document.createElement("div");
      body.className = "faq-item__a interview-formats__company-body";

      if (co.note) {
        const note = document.createElement("p");
        note.className = "interview-formats__company-note muted";
        note.textContent = co.note;
        body.appendChild(note);
      }
      if (co.tag) {
        const tag = document.createElement("p");
        tag.className = "interview-formats__tag";
        tag.textContent = co.tag;
        body.appendChild(tag);
      }

      const profiles = document.createElement("div");
      profiles.className = "interview-formats__profiles";
      (co.profiles || []).forEach((profile, pIdx) => {
        const det = document.createElement("details");
        det.className = "faq-item interview-formats__profile";
        const sum = document.createElement("summary");
        sum.className = "faq-item__q";
        const num = document.createElement("span");
        num.className = "faq-item__n";
        num.textContent = String(pIdx + 1);
        const qtext = document.createElement("span");
        qtext.className = "faq-item__qtext";
        qtext.textContent = profile.title;
        const action = document.createElement("span");
        action.className = "faq-item__action";
        action.setAttribute("data-i18n", "resources.expandOne");
        const chevron = document.createElement("span");
        chevron.className = "faq-item__chevron";
        chevron.setAttribute("aria-hidden", "true");
        chevron.textContent = "›";
        sum.append(num, qtext, action, chevron);
        det.append(sum, buildProfileBody(profile));
        profiles.appendChild(det);
      });
      body.appendChild(profiles);

      if (co.tips) {
        const tips = document.createElement("div");
        tips.className = "interview-formats__tips";
        const th = document.createElement("p");
        th.className = "interview-formats__tips-title";
        th.textContent = co.tips.title;
        tips.appendChild(th);
        appendBullets(tips, co.tips.bullets);
        body.appendChild(tips);
      }

      const reco = buildRecommendations(co, langNow);
      if (reco) body.appendChild(reco);
      return body;
    }

    // Return the language-appropriate view of a company. English content lives
    // in an optional `co.en` overlay; missing fields fall back to Vietnamese.
    const viewOf = (co, lang) => (lang === "en" && co.en ? { ...co, ...co.en } : co);

    const render = () => {
      const langNow = document.documentElement.lang || "vi";
      list.innerHTML = "";
      const q = (search?.value || "").trim().toLowerCase();
      const companyId = companySel?.value || "";
      let visible = 0;

      data.forEach((co) => {
        // Search across both languages (co already includes the en overlay).
        const hay = JSON.stringify(co).toLowerCase();
        const show = (!companyId || co.id === companyId) && (!q || hay.includes(q));
        if (!show) return;
        visible++;

        const view = viewOf(co, langNow);
        const details = document.createElement("details");
        details.className = "faq-item interview-formats__company";
        details.dataset.companyId = co.id;

        const summary = document.createElement("summary");
        summary.className = "faq-item__q";
        const num = document.createElement("span");
        num.className = "faq-item__n";
        num.textContent = String(visible);
        const qtext = document.createElement("span");
        qtext.className = "faq-item__qtext";
        qtext.textContent = (view.company || co.company) + (view.tag ? ` · ${view.tag}` : "");
        const action = document.createElement("span");
        action.className = "faq-item__action";
        action.setAttribute("data-i18n", "resources.expandOne");
        const chevron = document.createElement("span");
        chevron.className = "faq-item__chevron";
        chevron.setAttribute("aria-hidden", "true");
        chevron.textContent = "›";
        summary.append(num, qtext, action, chevron);
        details.append(summary, buildCompanyBody(view, langNow));
        list.appendChild(details);
        if (q || companyId) details.open = true;
      });

      if (empty) empty.hidden = visible !== 0;
      if (meta) {
        const total = data.length;
        meta.textContent =
          langNow === "en"
            ? `${visible} of ${total} companies shown · EngineerPro cheatsheet V2`
            : `Hiển thị ${visible}/${total} công ty · EngineerPro cheatsheet V2`;
      }
      if (typeof syncResourceExpandLabels === "function") syncResourceExpandLabels();
    };

    list.__formatsRender = render;
    render();

    if (list.dataset.formatsBound) return;
    list.dataset.formatsBound = "1";

    search?.addEventListener("input", render);
    companySel?.addEventListener("change", render);

    const formatsBase = () => ((typeof BASE_PATH !== "undefined" && BASE_PATH) || "");
    // Reflect the opened company in the address bar so it is shareable, e.g.
    // opening Amazon → /resources/interview-formats/amazon (no history spam).
    const reflectCompanyUrl = () => {
      // Only when the Resources route is the active view (avoid rewriting the
      // URL when a re-render fires toggles while another route is shown).
      const sec = list.closest(".route");
      if (sec && sec.hidden) return;
      // Don't fight the URL while the user is searching/filtering.
      if ((search?.value || "").trim()) return;
      const open = list.querySelector(":scope > details.interview-formats__company[open]");
      const target = open?.dataset.companyId
        ? `${formatsBase()}/resources/interview-formats/${open.dataset.companyId}/`
        : `${formatsBase()}/resources/interview-formats/`;
      if (location.pathname !== target) {
        try { history.replaceState(null, "", target); } catch (_) {}
      }
    };

    list.addEventListener("toggle", (ev) => {
      if (ev.target.matches(".faq-item")) syncResourceExpandLabels();
      if (ev.target.matches(".interview-formats__company")) reflectCompanyUrl();
    }, true);

    document.getElementById("interviewFormatsExpandAll")?.addEventListener("click", () => {
      const panel = document.getElementById("resInterviewFormats");
      if (panel && !panel.open) panel.open = true;
      list.querySelectorAll(":scope > .faq-item").forEach((it) => {
        it.open = true;
        it.querySelectorAll(".interview-formats__profile").forEach((p) => {
          p.open = true;
        });
      });
      syncResourceExpandLabels();
    });
    document.getElementById("interviewFormatsCollapseAll")?.addEventListener("click", () => {
      list.querySelectorAll(":scope > .faq-item").forEach((it) => {
        it.open = false;
        it.querySelectorAll(".interview-formats__profile").forEach((p) => {
          p.open = false;
        });
      });
      syncResourceExpandLabels();
    });
  }

  function initPipChecklist() {
    const list = document.getElementById("pipChecklist");
    if (!list) return;

    const search = document.getElementById("pipSearch");
    const empty = document.getElementById("pipEmpty");

    const apply = () => {
      const q = (search?.value || "").trim().toLowerCase();
      let visible = 0;
      list.querySelectorAll(":scope > .faq-item").forEach((it) => {
        const show = !q || it.textContent.toLowerCase().includes(q);
        it.hidden = !show;
        if (show) {
          visible++;
          if (q) it.open = true;
        }
      });
      if (empty) empty.hidden = visible !== 0;
      if (typeof syncResourceExpandLabels === "function") syncResourceExpandLabels();
    };
    if (search) search.addEventListener("input", apply);

    list.querySelectorAll(":scope > .faq-item").forEach((it) => {
      it.addEventListener("toggle", syncResourceExpandLabels);
    });
    syncResourceExpandLabels();

    document.getElementById("pipExpandAll")?.addEventListener("click", () => {
      const pipPanel = document.getElementById("resPipBigTech");
      if (pipPanel && !pipPanel.open) pipPanel.open = true;
      list.querySelectorAll(":scope > .faq-item:not([hidden])").forEach((it) => {
        it.open = true;
      });
      syncResourceExpandLabels();
    });
    document.getElementById("pipCollapseAll")?.addEventListener("click", () => {
      list.querySelectorAll(":scope > .faq-item").forEach((it) => {
        it.open = false;
      });
      syncResourceExpandLabels();
    });
  }

  function initSuccessToast() {
    const root = document.getElementById("successToast");
    if (!root) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const textEl = document.getElementById("successToastText");
    const linkEl = document.getElementById("successToastLink");
    const closeBtn = root.querySelector(".success-toast__close");

    const TOAST_INTERVAL_MS = 10000;
    const TOAST_VISIBLE_MS = 4500;

    const TEMPLATES_VI = [
      "{name} vừa đỗ {company} cùng EngineerPro",
      "{name} đã nhận offer tại {company} sau lộ trình EngineerPro",
      "Chúc mừng {name} — đỗ {company} rồi!",
    ];
    const TEMPLATES_EN = [
      "{name} just landed {company} with EngineerPro",
      "{name} got an offer at {company} after EngineerPro training",
      "Congrats {name} — offer at {company}!",
    ];

    function formatCompanies(companies) {
      if (!companies?.length) return currentLang === "en" ? "Big Tech" : "Big Tech";
      if (companies.length === 1) return companies[0];
      return companies.slice(0, 2).join(" & ");
    }

    function isMentorSharingStory(s) {
      const blob = [
        s.rawTitle,
        s.originalTitle,
        s.originalTitleEn,
        s.title,
        s.titleEn,
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return /mentor|giảng viên|giang vien|instructor|lecturer/.test(blob);
    }

    function buildPool() {
      return stories.filter((s) => {
        if (s.anonymous || s.isArticle || isMentorSharingStory(s)) return false;
        if (!s.companies?.length) return false;
        const name = (s.name || "").trim();
        if (!name || /^Học viên EngineerPro$/i.test(name)) return false;
        return true;
      });
    }

    let pool = buildPool();
    if (pool.length < 3) return;

    let queue = [];
    let lastSlug = "";
    let showTimer = null;
    let cycleTimer = null;
    let pausedUntil = 0;

    function shuffle(arr) {
      for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
      }
      return arr;
    }

    function refillQueue() {
      queue = shuffle(pool.slice());
    }
    refillQueue();

    function pickNext() {
      if (!queue.length) refillQueue();
      let s = queue.pop();
      if (s.slug === lastSlug && queue.length) {
        queue.unshift(s);
        s = queue.pop();
      }
      lastSlug = s.slug;
      return s;
    }

    function renderMessage(s) {
      const templates = currentLang === "en" ? TEMPLATES_EN : TEMPLATES_VI;
      const tpl = templates[Math.floor(Math.random() * templates.length)];
      const name = (s.name || "").trim();
      const company = formatCompanies(s.companies);
      return tpl.replace("{name}", name).replace("{company}", company);
    }

    function hideToast() {
      root.classList.remove("success-toast--visible");
      window.setTimeout(() => {
        if (!root.classList.contains("success-toast--visible")) root.hidden = true;
      }, 320);
    }

    function showToast() {
      if (Date.now() < pausedUntil) {
        scheduleNext();
        return;
      }
      pool = buildPool();
      if (pool.length < 1) return;

      const s = pickNext();
      if (textEl) textEl.textContent = renderMessage(s);
      if (linkEl) linkEl.href = pathFor("story", s.slug);
      root.hidden = false;
      requestAnimationFrame(() => root.classList.add("success-toast--visible"));

      clearTimeout(showTimer);
      showTimer = window.setTimeout(() => {
        hideToast();
        scheduleNext();
      }, TOAST_VISIBLE_MS);
    }

    function scheduleNext() {
      clearTimeout(cycleTimer);
      cycleTimer = window.setTimeout(showToast, TOAST_INTERVAL_MS);
    }

    closeBtn?.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      hideToast();
      clearTimeout(showTimer);
      pausedUntil = Date.now() + 90000;
      scheduleNext();
    });

    window.__refreshSuccessToast = function () {
      pool = buildPool();
      if (!root.classList.contains("success-toast--visible") || !textEl) return;
      const s = stories.find((x) => x.slug === lastSlug);
      if (s) textEl.textContent = renderMessage(s);
    };

    window.setTimeout(showToast, TOAST_INTERVAL_MS);
  }

  // ===================== ROADMAP =====================
  function renderRoadmap() {
    const r = data.roadmap;
    if (!r) return;

    const en = currentLang === "en";
    const phaseLabel = en ? "STAGE" : "GIAI ĐOẠN";
    const goalLabel = en ? "Goal: " : "Mục tiêu: ";

    const intro = document.getElementById("roadmapIntro");
    if (intro) intro.textContent = (en && r.introEn) ? r.introEn : r.intro;

    const tl = document.getElementById("roadmapTimeline");
    if (tl) {
      tl.innerHTML = "";
      r.stages.forEach((s) => {
        const sTitle = (en && s.titleEn) ? s.titleEn : s.title;
        const sSub = (en && s.subtitleEn) ? s.subtitleEn : s.subtitle;
        const sGoal = (en && s.goalEn) ? s.goalEn : s.goal;
        const stage = el("article", { class: "stage" }, [
          el("div", { class: "stage__rail" }, [
            el("div", { class: "stage__n" }, String(s.n).padStart(2, "0")),
          ]),
          el("div", { class: "stage__body" }, [
            el("header", { class: "stage__head" }, [
              el("span", { class: "stage__icon" }, s.icon),
              el("div", { class: "stage__title-wrap" }, [
                el("h2", { class: "stage__title" }, [
                  el("span", { class: "stage__phase" }, `${phaseLabel} ${s.n}`),
                  el("span", {}, sTitle),
                ]),
                el("p", { class: "stage__subtitle" }, sSub),
              ]),
            ]),
            el("p", { class: "stage__goal" }, [goalLabel, el("span", {}, sGoal)]),
            el(
              "div",
              { class: "stage__modules" },
              s.modules.map((m) => {
                const mTitle = (en && m.titleEn) ? m.titleEn : m.title;
                const mBlurb = (en && m.blurbEn) ? m.blurbEn : m.blurb;
                // Inject an explicit "Bấm vào đây để xem chi tiết khoá học"
                // mini-button when the module has a real course backing it,
                // so visitors don't have to guess that the title is clickable.
                const ctaNode = m.courseSlug
                  ? el("a", {
                      class: "module__cta",
                      href: pathFor("course", m.courseSlug),
                    }, t("roadmap.module.cta"))
                  : null;
                return el("article", { class: "module" }, [
                  el("header", { class: "module__head" }, [
                    el("h3", {}, mTitle),
                    mBlurb ? el("p", { class: "module__blurb" }, mBlurb) : null,
                    ctaNode,
                  ]),
                  el(
                    "div",
                    { class: "module__topics" },
                    m.topics.map((t) =>
                      el("span", { class: "topic-pill" }, [
                        el("span", { class: "topic-pill__check" }, "✓"),
                        el("span", {}, t),
                      ])
                    )
                  ),
                ]);
              })
            ),
          ]),
        ]);
        stage.style.setProperty("--stage-accent", s.accent || "var(--orange)");
        tl.appendChild(stage);
      });
    }

    const extras = document.getElementById("roadmapExtras");
    if (extras && r.extras) {
      const exTitleEl = document.getElementById("roadmapExtrasTitle");
      if (exTitleEl) exTitleEl.textContent = (en && r.extras.titleEn) ? r.extras.titleEn : r.extras.title;
      extras.innerHTML = "";
      // Items can be either a plain string (legacy) or an object
      // { courseSlug, linkLabel, text, textEn } where the linkLabel becomes
      // a hyperlink to /courses/<slug>/ and `text` is the trailing copy.
      const items = r.extras.items || [];
      items.forEach((it) => {
        if (typeof it === "string") {
          extras.appendChild(el("li", {}, it));
          return;
        }
        const trailing = (en && it.textEn) ? it.textEn : (it.text || "");
        const linkText = it.linkLabel || it.courseSlug || "";
        const nameNode = el("strong", { class: "roadmap-extras__name" }, linkText);
        const ctaNode = it.courseSlug
          ? el("a", {
              class: "module__cta",
              href: pathFor("course", it.courseSlug),
            }, t("roadmap.module.cta"))
          : null;
        const li = el("li", {}, [nameNode, trailing]);
        if (ctaNode) li.appendChild(ctaNode);
        extras.appendChild(li);
      });
    }

    const ben = document.getElementById("roadmapBenefits");
    if (ben) {
      ben.innerHTML = "";
      const benefits = (en && r.benefitsEn) ? r.benefitsEn : r.benefits;
      benefits.forEach((t) =>
        ben.appendChild(
          el("li", {}, [el("span", { class: "roadmap-benefits__check" }, "🔥"), el("span", {}, t)])
        )
      );
    }
  }

  // ===================== SUCCESS STORIES =====================
  function renderStoryDetail(slug) {
    const wrap = document.getElementById("storyArticle");
    if (!wrap) return;
    const s = stories.find((x) => x.slug === slug);
    if (!s) {
      wrap.innerHTML =
        '<h1>Không tìm thấy bài viết</h1>' +
        '<p>Quay lại <a data-href="#stories">danh sách Success Stories</a>.</p>';
      return;
    }

    // Anonymous stories must never leak the student's real name. The data
    // layer already neutralises s.name to "Học viên EngineerPro" but we
    // localise it here so EN visitors see English copy too.
    const cleanName = s.anonymous
      ? (currentLang === "en" ? "EngineerPro student" : "Học viên EngineerPro")
      : ((s.name || "").trim() || (s.companies?.[0] ? `EP · ${s.companies[0]}` : "EngineerPro"));
    const nm = cleanName.replace(/^(anh|chị|bạn|em|cô)\s+/i, "");
    const [c1, c2] = colorFor(cleanName);
    const cos = (s.companies || []).map((c) => `<span class="story-card__co">${c}</span>`).join("");
    const badges = [];
    // "Big Tech" tier-1 badge removed per request — the company chips already convey it.
    if (s.premium) badges.push('<span class="story-card__badge story-card__badge--prem">Premium</span>');
    if (s.anonymous) {
      badges.push(`<span class="story-card__badge story-card__badge--anon">${currentLang === "en" ? "Anonymous" : "Ẩn danh"}</span>`);
    }

    // Only show "View original on Substack" when we have a specific article URL —
    // not the generic substack homepage / archive page (would be useless).
    function isSpecificSubstackUrl(u) {
      if (!u || !u.includes("substack")) return false;
      try {
        const url = new URL(u);
        // Must be /p/<slug> (post page); skip "/", "/podcast/...", "/archive", etc.
        return /^\/p\/[\w-]+/.test(url.pathname);
      } catch (_) { return false; }
    }
    const extUrl = s.matchedSubstackUrl || s.externalUrl;
    // For anonymous stories, never link to the original Substack post — it
    // reveals the student's real name. Show only our name-free write-up.
    const extLink = (!s.anonymous && isSpecificSubstackUrl(extUrl))
      ? `<a class="btn btn--ghost" href="${extUrl}" target="_blank" rel="noopener">${escapeText(t("stories.cta.substack"))}</a>`
      : "";

    const dispTitle = currentLang === "en"
      ? (s.originalTitleEn || s.titleEn || s.originalTitle || s.title)
      : (s.originalTitle || s.title);

    // Body priority:
    //   VI mode → originalHtml (full crawled article, Vietnamese)
    //   EN mode → originalHtmlEn (machine-translated full article)
    //             → fall back to bodyEn (our concise summary)
    //             → fall back to the Vietnamese original (with a banner)
    let dispBody;
    let langBanner = "";
    if (currentLang === "en") {
      if (s.originalHtmlEn) {
        dispBody = s.originalHtmlEn;
      } else if (s.bodyEn) {
        dispBody = s.bodyEn;
      } else if (s.originalHtml) {
        dispBody = s.originalHtml;
        langBanner =
          '<p class="lang-note">📌 The original article is in Vietnamese — use your browser\'s auto-translate for the full read.</p>';
      } else {
        dispBody = s.body || "";
      }
    } else {
      dispBody = s.originalHtml || s.body || s.bodyEn || "";
    }

    // Strip a duplicate leading <h1>/<h2> if it just repeats the page title.
    dispBody = rewriteAssetUrls(sanitizeHtml(stripDuplicateHeading(dispBody, dispTitle)));

    const cover = s.cover
      ? `<img class="story-detail__cover" src="${escapeAttr(asset(s.cover))}" alt="${escapeAttr(dispTitle || cleanName)}" />`
      : "";

    wrap.innerHTML = `
      <header class="story-detail__head">
        <div class="story-detail__chips">
          ${badges.join("")}
          ${cos}
        </div>
        <h1>${escapeText(dispTitle)}</h1>
        <p class="story-detail__byline">${escapeText(cleanName)}</p>
      </header>
      ${cover}
      ${langBanner}
      <div class="story-detail__body">${dispBody}</div>
      <div class="article__cta">
        <a class="btn btn--primary" href="https://m.me/EngineerPro.Official" target="_blank" rel="noopener">
          ${escapeText(t("stories.cta"))}
        </a>
        ${extLink}
        <a class="back-link" data-href="#stories">${escapeText(t("stories.back"))}</a>
      </div>
    `;
  }

  let storiesFilter = null;
  let storiesPage = 1;
  let storiesShowAllTags = false;
  const STORIES_PER_PAGE = 8;
  const STORIES_INITIAL_TAGS = 10;

  function renderStories() {
    const grid = document.getElementById("storiesGrid");
    if (!grid) return;
    const count = document.getElementById("storiesCount");
    if (count) count.textContent = stories.length;

    // Render filter chips (count per company across all stories)
    const filterWrap = document.getElementById("storiesFilter");
    function buildFilter() {
      if (!filterWrap) return;
      filterWrap.innerHTML = "";
      const counts = new Map();
      stories.forEach((s) =>
        (s.companies || []).forEach((c) => counts.set(c, (counts.get(c) || 0) + 1))
      );
      // Big-tech first, then by count desc
      const TIER1 = new Set(["Google","Meta","Amazon","Microsoft","TikTok","Uber","Apple","Tesla","Nvidia","Spotify","Citadel"]);
      const sorted = [...counts.entries()].sort((a, b) => {
        const ta = TIER1.has(a[0]) ? 0 : 1;
        const tb = TIER1.has(b[0]) ? 0 : 1;
        if (ta !== tb) return ta - tb;
        return b[1] - a[1];
      });

      filterWrap.appendChild(
        el(
          "button",
          {
            class: "tag-chip" + (storiesFilter === null ? " is-active" : ""),
            type: "button",
            onClick: () => { storiesFilter = null; storiesPage = 1; buildFilter(); paint(); },
          },
          `${t("courses.filter.all")} · ${stories.length}`
        )
      );

      // If the currently-selected filter would be hidden by the collapse limit,
      // include it explicitly so the user still sees what's active.
      const visible = storiesShowAllTags ? sorted : sorted.slice(0, STORIES_INITIAL_TAGS);
      if (storiesFilter && !visible.find(([c]) => c === storiesFilter)) {
        const hit = sorted.find(([c]) => c === storiesFilter);
        if (hit) visible.push(hit);
      }
      visible.forEach(([co, n]) => {
        filterWrap.appendChild(
          el(
            "button",
            {
              class: "tag-chip" + (storiesFilter === co ? " is-active" : ""),
              type: "button",
              onClick: () => {
                storiesFilter = storiesFilter === co ? null : co;
                storiesPage = 1;
                buildFilter();
                paint();
              },
            },
            `${co} · ${n}`
          )
        );
      });
      // Toggle button if there are more than the initial cap
      if (sorted.length > STORIES_INITIAL_TAGS) {
        const remaining = sorted.length - STORIES_INITIAL_TAGS;
        const label = storiesShowAllTags
          ? (currentLang === "en" ? "Show less" : "Thu gọn")
          : (currentLang === "en" ? `+ ${remaining} more` : `+ ${remaining} tag khác`);
        filterWrap.appendChild(
          el(
            "button",
            {
              class: "tag-chip tag-chip--toggle",
              type: "button",
              onClick: () => { storiesShowAllTags = !storiesShowAllTags; buildFilter(); },
            },
            label
          )
        );
      }
    }
    if (filterWrap && !filterWrap.children.length) {
      buildFilter();
    }

    function refreshChips() {
      const wrap = document.getElementById("storiesFilter");
      if (!wrap) return;
      const allLabel = t("courses.filter.all");
      [...wrap.children].forEach((btn) => {
        const label = btn.textContent.split(" · ")[0];
        const active = (label === allLabel && storiesFilter === null) || label === storiesFilter;
        btn.classList.toggle("is-active", active);
      });
    }

    function paint() {
      grid.innerHTML = "";
      const list = storiesFilter
        ? stories.filter((s) => (s.companies || []).includes(storiesFilter))
        : stories;

      const totalPages = Math.max(1, Math.ceil(list.length / STORIES_PER_PAGE));
      if (storiesPage > totalPages) storiesPage = totalPages;
      const start = (storiesPage - 1) * STORIES_PER_PAGE;
      const slice = list.slice(start, start + STORIES_PER_PAGE);

      slice.forEach((s) => grid.appendChild(makeCard(s)));
      renderPagination(list.length, totalPages);

      const empty = document.getElementById("storiesEmpty");
      if (empty) empty.hidden = list.length !== 0;
    }

    function renderPagination(totalItems, totalPages) {
      let pager = document.getElementById("storiesPager");
      if (!pager) {
        pager = document.createElement("nav");
        pager.id = "storiesPager";
        pager.className = "pager";
        pager.setAttribute("aria-label", "Stories pagination");
        grid.parentNode.insertBefore(pager, grid.nextSibling);
      }
      pager.innerHTML = "";
      if (totalPages <= 1) {
        pager.hidden = true;
        return;
      }
      pager.hidden = false;

      const labelPrev = currentLang === "en" ? "← Prev" : "← Trước";
      const labelNext = currentLang === "en" ? "Next →" : "Sau →";
      const labelOf   = currentLang === "en"
        ? `Showing ${(storiesPage - 1) * STORIES_PER_PAGE + 1}–${Math.min(
            storiesPage * STORIES_PER_PAGE, totalItems
          )} of ${totalItems}`
        : `Hiển thị ${(storiesPage - 1) * STORIES_PER_PAGE + 1}–${Math.min(
            storiesPage * STORIES_PER_PAGE, totalItems
          )} / ${totalItems} câu chuyện`;

      function goTo(p) {
        storiesPage = Math.max(1, Math.min(totalPages, p));
        paint();
        // Smooth scroll back to top of the list
        const head = grid.previousElementSibling; // filter chip bar
        (head || grid).scrollIntoView({ behavior: "smooth", block: "start" });
      }

      function pageBtn(label, page, disabled = false, active = false) {
        return el(
          "button",
          {
            class:
              "pager__btn" +
              (active ? " is-active" : "") +
              (disabled ? " is-disabled" : ""),
            type: "button",
            disabled: disabled || undefined,
            onClick: disabled ? null : () => goTo(page),
          },
          String(label)
        );
      }

      pager.appendChild(pageBtn(labelPrev, storiesPage - 1, storiesPage === 1));

      // Show all pages if ≤7, else compact 1 … cur-1 cur cur+1 … last
      const pages = [];
      if (totalPages <= 7) {
        for (let p = 1; p <= totalPages; p++) pages.push(p);
      } else {
        pages.push(1);
        const left = Math.max(2, storiesPage - 1);
        const right = Math.min(totalPages - 1, storiesPage + 1);
        if (left > 2) pages.push("…");
        for (let p = left; p <= right; p++) pages.push(p);
        if (right < totalPages - 1) pages.push("…");
        pages.push(totalPages);
      }
      pages.forEach((p) => {
        if (p === "…") {
          pager.appendChild(el("span", { class: "pager__gap" }, "…"));
        } else {
          pager.appendChild(pageBtn(p, p, false, p === storiesPage));
        }
      });

      pager.appendChild(pageBtn(labelNext, storiesPage + 1, storiesPage === totalPages));
      pager.appendChild(el("span", { class: "pager__info" }, labelOf));
    }

    function makeCard(s) {
      const cleanName = s.anonymous
        ? (currentLang === "en" ? "EngineerPro student" : "Học viên EngineerPro")
        : ((s.name || "").trim() || (s.companies?.[0] ? `EP · ${s.companies[0]}` : "EngineerPro"));
      // Prefer the real article title from the Google Doc; only fall back to
      // the AI-generated title if we never crawled the original.
      const dispTitle = currentLang === "en"
        ? (s.titleEn || s.originalTitle || s.title)
        : (s.originalTitle || s.title);
      const dispLead  = currentLang === "en" ? (s.leadEn  || s.lead)  : s.lead;

      const companyChips = (s.companies || []).map((c) =>
        el("span", { class: "story-card__co" }, c)
      );

      const badges = [];
      // "Big Tech" tier-1 badge removed per request — keep stories sorted by tier server-side instead.
      if (s.premium) badges.push(el("span", { class: "story-card__badge story-card__badge--prem" }, "Premium"));
      if (s.anonymous) {
        badges.push(el(
          "span",
          { class: "story-card__badge story-card__badge--anon" },
          currentLang === "en" ? "Anonymous" : "Ẩn danh"
        ));
      }

      const primaryCo = (s.companies || [])[0] || "EngineerPro";
      const moreCo = (s.companies || []).length > 1 ? `+${(s.companies || []).length - 1}` : "";

      const cover = s.cover
        ? el("div", { class: "story-row__cover" }, [
            el("img", { src: asset(s.cover), alt: dispTitle || cleanName, loading: "lazy" }),
            el(
              "span",
              { class: "story-row__cover-tag" },
              moreCo ? `${primaryCo}  ${moreCo}` : primaryCo
            ),
          ])
        : el("div", { class: "story-row__cover story-row__cover--ph" }, "EP");

      const snippet = (dispLead || "").length > 180
        ? (dispLead || "").slice(0, 178).replace(/\s+\S*$/, "") + "…"
        : (dispLead || "");

      return el(
        "a",
        {
          class: "story-row",
          href: `${BASE_PATH}/stories/${s.slug}/`,
          "data-href": `#story/${s.slug}`,
          title: dispTitle,
        },
        [
          cover,
          el("div", { class: "story-row__body" }, [
            (badges.length || companyChips.length)
              ? el("div", { class: "story-row__top" }, [
                  ...badges,
                  ...companyChips,
                ])
              : null,
            el("h3", { class: "story-row__title" }, dispTitle || cleanName),
            snippet ? el("p", { class: "story-row__snippet" }, snippet) : null,
            el("span", { class: "story-row__cta" }, t("stories.card.cta")),
          ]),
        ]
      );
    }

    paint();
  }

  // ===================== INTERVIEW RESOURCES =====================
  function renderResources() {
    if (!resources) return;
    const en = currentLang === "en";
    const enMap = (typeof window !== "undefined" && window.RESOURCES_EN) || {};
    const viLabels = (typeof window !== "undefined" && window.RESOURCES_VI_LABELS) || {};

    const f = resources.foundation;
    if (f) {
      const fEn = enMap.foundation || {};
      const videoWord = en ? (fEn.videoCountLabel || "videos") : (viLabels.foundation?.videoCountLabel || "video");
      const subtitle = (en && fEn.subtitle) ? fEn.subtitle : f.subtitle;
      const description = (en && fEn.description) ? fEn.description : f.description;

      const t = document.getElementById("resFoundationTitle");
      if (t) t.textContent = `${f.title} — ${f.videos.length} ${videoWord}`;
      const s = document.getElementById("resFoundationSub");
      if (s) s.textContent = subtitle;
      const d = document.getElementById("resFoundationDesc");
      if (d) d.textContent = description;
      const c = document.getElementById("resFoundationCta");
      if (c) c.href = f.url;

      const grid = document.getElementById("resFoundationGrid");
      if (grid) {
        grid.innerHTML = "";
        f.videos.forEach((v, i) => {
          const card = el(
            "a",
            {
              class: "video-card",
              href: v.url,
              target: "_blank",
              rel: "noopener",
              title: v.title,
            },
            [
              el("div", { class: "video-card__thumb" }, [
                el("img", { src: asset(v.thumbnail), alt: v.title, loading: "lazy" }),
                v.duration ? el("span", { class: "video-card__dur" }, v.duration) : null,
                el("span", { class: "video-card__play" }, "▶"),
              ]),
              el("div", { class: "video-card__meta" }, [
                el("span", { class: "video-card__idx" }, `#${String(i + 1).padStart(2, "0")}`),
                el("h4", {}, v.title),
              ]),
            ]
          );
          grid.appendChild(card);
        });
      }
    }

    // Golang Tour — 3 free videos with a senior Shopee SWE
    const gt = resources.golangTour;
    if (gt) {
      const gtEn = enMap.golangTour || {};
      const videoWord = en
        ? (gtEn.videoCountLabel || "videos")
        : (viLabels.golangTour?.videoCountLabel || "video");
      const t = document.getElementById("resGolangTourTitle");
      if (t) t.textContent = `${gt.title} — ${gt.videos.length} ${videoWord}`;
      const s = document.getElementById("resGolangTourSub");
      if (s) s.textContent = (en && gtEn.subtitle) ? gtEn.subtitle : gt.subtitle;
      const d = document.getElementById("resGolangTourDesc");
      if (d) d.textContent = (en && gtEn.description) ? gtEn.description : gt.description;
      const c = document.getElementById("resGolangTourCta");
      if (c) c.href = gt.url;

      const grid = document.getElementById("resGolangTourGrid");
      if (grid) {
        grid.innerHTML = "";
        gt.videos.forEach((v, i) => {
          const card = el(
            "a",
            {
              class: "video-card",
              href: v.url,
              target: "_blank",
              rel: "noopener",
              title: v.title,
            },
            [
              el("div", { class: "video-card__thumb" }, [
                el("img", { src: asset(v.thumbnail), alt: v.title, loading: "lazy" }),
                v.duration ? el("span", { class: "video-card__dur" }, v.duration) : null,
                el("span", { class: "video-card__play" }, "▶"),
              ]),
              el("div", { class: "video-card__meta" }, [
                el("span", { class: "video-card__idx" }, `#${String(i + 1).padStart(2, "0")}`),
                el("h4", {}, v.title),
              ]),
            ]
          );
          grid.appendChild(card);
        });
      }
    }

    const cv = resources.cv;
    if (cv) {
      const cvEn = enMap.cv || {};

      const intro = document.getElementById("resCVIntro");
      if (intro) intro.textContent = (en && cvEn.intro) ? cvEn.intro : cv.intro;

      const sample = cv.sample;
      if (sample) {
        const sEn = cvEn.sample || {};
        const iframe = document.getElementById("cvSampleIframe");
        if (iframe) iframe.src = sample.previewUrl;
        const t = document.getElementById("cvSampleTitle");
        if (t) t.textContent = (en && sEn.title) ? sEn.title : sample.title;
        const s = document.getElementById("cvSampleSub");
        if (s) s.textContent = (en && sEn.subtitle) ? sEn.subtitle : sample.subtitle;
        const v = document.getElementById("cvSampleView");
        if (v) v.href = sample.viewUrl;
      }

      const ol = cv.overleaf;
      if (ol) {
        const oEn = cvEn.overleaf || {};
        const node = document.getElementById("cvOverleaf");
        if (node) node.href = ol.url;
        document.getElementById("cvOverleafTitle").textContent = (en && oEn.title) ? oEn.title : ol.title;
        document.getElementById("cvOverleafSub").textContent = (en && oEn.subtitle) ? oEn.subtitle : ol.subtitle;
      }

      const rv = cv.review;
      if (rv) {
        const rEn = cvEn.review || {};
        const node = document.getElementById("cvReview");
        if (node) node.href = rv.url;
        document.getElementById("cvReviewTitle").textContent = (en && rEn.title) ? rEn.title : rv.title;
        document.getElementById("cvReviewSub").textContent = (en && rEn.subtitle) ? rEn.subtitle : rv.subtitle;
        const cta = document.getElementById("cvReviewCta");
        if (cta) {
          const makeCta = en
            ? (rEn.episodeCta || ((n) => `Watch ${n} episodes ↗`))
            : (viLabels.cv?.review?.episodeCta || ((n) => `Xem ${n} tập ↗`));
          cta.textContent = makeCta(rv.videos.length);
        }
      }

      const tool = cv.tool;
      if (tool) {
        const tEn = cvEn.tool || {};
        const node = document.getElementById("cvTool");
        if (node) node.href = tool.url;
        document.getElementById("cvToolThumb").src = asset(tool.thumbnail);
        document.getElementById("cvToolTitle").textContent = (en && tEn.title) ? tEn.title : tool.title;
        document.getElementById("cvToolAuthor").textContent = `EngineerPro · YouTube`;
      }
    }
  }

  // ===================== PARTNERS =====================
  function renderPartners() {
    const wrap = document.getElementById("partnersGrid");
    if (!wrap || !data.partners) return;
    wrap.innerHTML = "";

    const en = currentLang === "en";
    const lbl = {
      mentorsHeading: en ? "Mentor team" : "Đội ngũ mentor",
      offersHeading: en ? "Mentees received offers at" : "Học viên đã nhận offer tại",
      founded: en ? "Founded" : "Thành lập",
      detail: en ? "View details →" : "Xem chi tiết →",
    };

    data.partners.forEach((p) => {
      const statsArr = (en && p.statsEn) ? p.statsEn : (p.stats || []);
      const mentorsArr = (en && p.mentorsEn) ? p.mentorsEn : (p.mentors || []);
      const tagline = (en && p.taglineEn) ? p.taglineEn : p.tagline;
      const quote = (en && p.quoteEn) ? p.quoteEn : p.quote;
      const description = (en && p.descriptionEn) ? p.descriptionEn : p.description;
      const ctaText = (en && p.ctaEn) ? p.ctaEn : (p.cta || lbl.detail);

      const stats = el(
        "div",
        { class: "partner-page__stats" },
        statsArr.map((s) =>
          el("div", { class: "stat" }, [
            el("div", { class: "stat__num" }, s.num),
            el("div", { class: "stat__label" }, s.label),
          ])
        )
      );

      const mentors = mentorsArr.length
        ? el("div", { class: "partner-page__group" }, [
            el("h4", {}, lbl.mentorsHeading),
            el(
              "ul",
              { class: "partner-page__mentors" },
              mentorsArr.map((m) =>
                el("li", {}, [
                  el("strong", {}, m.name),
                  el("span", {}, ` — ${m.role}`),
                ])
              )
            ),
          ])
        : null;

      const offerCos = (p.offerCompanies || []).length
        ? el("div", { class: "partner-page__group" }, [
            el("h4", {}, lbl.offersHeading),
            el(
              "div",
              { class: "partner-page__chips" },
              p.offerCompanies.map((c) => el("span", { class: "topic-pill" }, c))
            ),
          ])
        : null;

      const card = el("article", { class: "partner-page" }, [
        el("header", { class: "partner-page__head" }, [
          el("img", {
            class: "partner-page__logo",
            src: asset(p.logo),
            alt: `${p.name} logo`,
            loading: "lazy",
          }),
          el("div", { class: "partner-page__title" }, [
            el("h3", {}, p.name),
            el("p", { class: "partner-page__tagline" }, tagline),
            quote
              ? el("p", { class: "partner-page__quote" }, [
                  el("em", {}, `“${quote}”`),
                ])
              : null,
            p.founded
              ? el("p", { class: "partner-page__meta" }, `${lbl.founded} ${p.founded}`)
              : null,
          ]),
        ]),
        stats,
        description ? el("p", { class: "partner-page__desc" }, description) : null,
        mentors,
        offerCos,
        el("div", { class: "partner-page__cta" }, [
          el(
            "a",
            { class: "btn btn--primary", href: p.url, target: "_blank", rel: "noopener" },
            ctaText
          ),
        ]),
      ]);
      wrap.appendChild(card);
    });
  }

  // ===================== INIT =====================
  // Apply initial i18n on static markup, then re-render dynamic content
  applyI18n();
  updateLangSwitchUI();
  document.getElementById("langSwitch")?.addEventListener("click", () => {
    setLang(currentLang === "vi" ? "en" : "vi");
  });

  // ===================== THEME (dark / light) =====================
  function currentTheme() {
    return document.documentElement.getAttribute("data-theme") || "light";
  }
  function updateThemeSwitchUI() {
    const btn = document.getElementById("themeSwitch");
    if (!btn) return;
    const icon = btn.querySelector(".theme-switch__icon");
    const isDark = currentTheme() === "dark";
    if (icon) icon.textContent = isDark ? "☀️" : "🌙";
    btn.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
    btn.setAttribute("title", isDark ? "Switch to light mode" : "Switch to dark mode");
  }
  function setTheme(theme) {
    if (theme !== "dark" && theme !== "light") return;
    document.documentElement.setAttribute("data-theme", theme);
    try { localStorage.setItem("epTheme", theme); } catch (e) { /* ignore */ }
    // Update the meta theme-color so OS chrome (mobile browser UI) matches
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", theme === "dark" ? "#0a1424" : "#0b1d3a");
    updateThemeSwitchUI();
    if (typeof rethemeMermaid === "function") rethemeMermaid();
  }
  updateThemeSwitchUI();
  document.getElementById("themeSwitch")?.addEventListener("click", () => {
    setTheme(currentTheme() === "dark" ? "light" : "dark");
  });
  // Follow OS-level theme changes if the user hasn't explicitly chosen one
  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener?.("change", (e) => {
      let saved = null;
      try { saved = localStorage.getItem("epTheme"); } catch (_) {}
      if (!saved) setTheme(e.matches ? "dark" : "light");
    });
  }

  // Re-render hook called by setLang so dynamic content updates after a switch.
  window.__rerenderAll = function () {
    if (typeof renderTagBar === "function") renderTagBar();
    if (typeof renderCourses === "function") renderCourses();
    if (typeof renderMentors === "function") renderMentors();
    if (typeof renderPodcasts === "function") renderPodcasts();
    if (typeof renderBook === "function") renderBook();
    if (typeof renderSystemDesign === "function") renderSystemDesign();
    if (typeof renderFAQ === "function") renderFAQ();
    if (typeof renderRoadmap === "function") renderRoadmap();
    if (typeof renderPartners === "function") renderPartners();
    if (typeof renderResources === "function") renderResources();
    if (typeof renderStories === "function") renderStories();
    if (typeof initInterviewFormats === "function") {
      const fl = document.getElementById("interviewFormatsList");
      if (fl?.__formatsRender) fl.__formatsRender();
      else initInterviewFormats();
    }
    // Translate any data-i18n elements created by renderers
    applyI18n();
    if (typeof syncResourceExpandLabels === "function") syncResourceExpandLabels();
    if (typeof window.__refreshSuccessToast === "function") window.__refreshSuccessToast();
    // Re-render current detail page if applicable
    const h = parseHash();
    if (h.route === "course") renderCourseDetail(h.slug);
    if (h.route === "story") renderStoryDetail(h.slug);
    if (h.route === "sd-chapter") renderSdChapter(h.slug);
    // Refresh SEO tags (title/description/canonical) for the current route
    if (typeof updateSeoForRoute === "function") updateSeoForRoute(h.route, h.slug);
  };

  document.getElementById("year").textContent = new Date().getFullYear();

  // Anniversary: years since 26 April 2023
  (function setStats() {
    const founded = new Date(2023, 3, 26); // month is 0-indexed → 3 = April
    const now = new Date();
    let years = now.getFullYear() - founded.getFullYear();
    const m = now.getMonth() - founded.getMonth();
    if (m < 0 || (m === 0 && now.getDate() < founded.getDate())) years--;
    const yEl = document.getElementById("statYears");
    if (yEl) yEl.textContent = Math.max(years, 0);
    const mEl = document.getElementById("statMentors");
    if (mEl && data.mentors) mEl.textContent = data.mentors.length;
    const cEl = document.getElementById("statCourses");
    if (cEl) cEl.textContent = courses.length;
  })();

  // Render the auto-scrolling company logo marquee.
  // SVGs and PNG silhouettes are applied as CSS masks so the tile colour
  // flows through (mask-image works on PNG with alpha + SVG alike).
  // We duplicate the entire logo list once so the CSS keyframe can scroll
  // -50% and loop seamlessly.
  (function renderCompanies() {
    const track = document.getElementById("logoMarquee");
    if (!track || !data.companies) return;
    track.innerHTML = "";

    function makeTile(c) {
      const tile = document.createElement("div");
      tile.className = "logo-tile";
      tile.title = c.name;
      tile.setAttribute("aria-label", c.name);
      if (c.logo) {
        const mark = document.createElement("span");
        mark.className = "logo-tile__svg";
        const u = asset(c.logo);
        mark.style.setProperty("-webkit-mask-image", `url(${u})`);
        mark.style.setProperty("mask-image", `url(${u})`);
        tile.appendChild(mark);
      } else {
        const wm = document.createElement("span");
        wm.className = "logo-tile__wordmark";
        wm.textContent = c.wordmark || c.name;
        tile.appendChild(wm);
      }
      return tile;
    }

    // Two passes for seamless loop
    for (let pass = 0; pass < 2; pass++) {
      data.companies.forEach((c) => track.appendChild(makeTile(c)));
    }
  })();

  renderTagBar();
  renderCourses();
  renderMentors();
  renderPodcasts();
  renderBook();
  renderSystemDesign();
  renderFAQ();
  initResourcesPanels();
  initHrChecklist();
  initPipChecklist();
  initCsFundamentalList();
  initInterviewFormats();
  initSuccessToast();
  renderRoadmap();
  renderPartners();
  renderResources();
  renderStories();
  showRoute(parseHash());
})();
