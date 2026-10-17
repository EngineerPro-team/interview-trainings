(function () {
  "use strict";

  const LANGS = [
    { id: "cpp", label: "C++" },
    { id: "java", label: "Java" },
    { id: "python", label: "Python3" },
  ];
  const LANG_KEY = "dsaHwLang";

  const KW = {
    cpp: new Set([
      "class","struct","public","private","protected","return","if","else","for",
      "while","do","break","continue","const","auto","new","delete","nullptr",
      "true","false","this","virtual","override","using","namespace","template",
      "typename","static","inline","operator","sizeof","typedef","enum","friend",
    ]),
    java: new Set([
      "class","interface","public","private","protected","return","if","else","for",
      "while","do","break","continue","new","this","static","final","void","boolean",
      "int","long","double","char","import","package","extends","implements","try",
      "catch","throw","throws","null","true","false","super","abstract","synchronized",
    ]),
    python: new Set([
      "class","def","return","if","elif","else","for","while","in","not","and","or",
      "None","True","False","from","import","as","with","yield","lambda","pass",
      "break","continue","try","except","finally","raise","is","global","nonlocal",
    ]),
  };
  const TYPES = new Set([
    "int","long","double","float","char","bool","void","string","vector","unordered_map",
    "unordered_set","map","set","queue","deque","stack","pair","optional","string",
    "List","ArrayList","HashMap","HashSet","Map","Set","String","Integer","Boolean",
    "TreeNode","TrieNode","Node","Solution","Optional","Dict","Tuple",
  ]);

  function loadLang() {
    try {
      const v = localStorage.getItem(LANG_KEY);
      if (LANGS.some((l) => l.id === v)) return v;
    } catch (_) { /* ignore */ }
    return "python";
  }

  function saveLang(id) {
    try { localStorage.setItem(LANG_KEY, id); } catch (_) { /* ignore */ }
  }

  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function highlight(src, lang) {
    const keys = KW[lang] || KW.python;
    const out = [];
    let i = 0;
    const n = src.length;
    while (i < n) {
      const two = src.slice(i, i + 2);
      if (lang === "python" && src[i] === "#") {
        const j = src.indexOf("\n", i);
        const end = j === -1 ? n : j;
        out.push('<span class="com">' + esc(src.slice(i, end)) + "</span>");
        i = end;
        continue;
      }
      if (two === "//") {
        const j = src.indexOf("\n", i);
        const end = j === -1 ? n : j;
        out.push('<span class="com">' + esc(src.slice(i, end)) + "</span>");
        i = end;
        continue;
      }
      if (two === "/*") {
        const j = src.indexOf("*/", i + 2);
        const end = j === -1 ? n : j + 2;
        out.push('<span class="com">' + esc(src.slice(i, end)) + "</span>");
        i = end;
        continue;
      }
      if (src[i] === '"' || src[i] === "'") {
        const q = src[i];
        let j = i + 1;
        while (j < n) {
          if (src[j] === "\\") { j += 2; continue; }
          if (src[j] === q) { j += 1; break; }
          j += 1;
        }
        out.push('<span class="str">' + esc(src.slice(i, j)) + "</span>");
        i = j;
        continue;
      }
      if (/[0-9]/.test(src[i])) {
        let j = i + 1;
        while (j < n && /[0-9xXa-fA-F.]/.test(src[j])) j += 1;
        out.push('<span class="num">' + esc(src.slice(i, j)) + "</span>");
        i = j;
        continue;
      }
      if (/[A-Za-z_]/.test(src[i])) {
        let j = i + 1;
        while (j < n && /[A-Za-z0-9_]/.test(src[j])) j += 1;
        const w = src.slice(i, j);
        let cls = "";
        if (keys.has(w)) cls = "kw";
        else if (TYPES.has(w)) cls = "typ";
        else if (src[j] === "(") cls = "fn";
        out.push(cls ? '<span class="' + cls + '">' + esc(w) + "</span>" : esc(w));
        i = j;
        continue;
      }
      out.push(esc(src[i]));
      i += 1;
    }
    return out.join("");
  }

  function renderEditor(code, lang) {
    const lines = code.replace(/\n$/, "").split("\n");
    const ln = lines.map((_, k) => String(k + 1)).join("\n");
    const html = highlight(lines.join("\n"), lang);
    return (
      '<pre class="editor" data-lang="' + lang + '">' +
        "<code>" +
          '<span class="ln">' + ln + "</span>" +
          '<span class="src">' + html + "</span>" +
        "</code>" +
      "</pre>"
    );
  }

  function renderCodebox(codes, active) {
    const tabs = LANGS.map((l) => (
      '<button type="button" class="tab' + (l.id === active ? " is-active" : "") +
      '" data-lang="' + l.id + '">' + l.label + "</button>"
    )).join("");
    const editors = LANGS.map((l) => renderEditor(codes[l.id] || "", l.id)).join("");
    return (
      '<div class="codebox">' +
        '<div class="codebox__tabs">' + tabs +
          '<div class="codebox__tools"><button type="button" class="copy">Copy</button></div>' +
        "</div>" +
        editors +
      "</div>"
    );
  }

  function setLang(root, lang) {
    root.querySelectorAll(".tab").forEach((t) => {
      t.classList.toggle("is-active", t.dataset.lang === lang);
    });
    root.querySelectorAll(".editor").forEach((ed) => {
      ed.classList.toggle("is-active", ed.dataset.lang === lang);
    });
  }

  function renderProblem(p, lang) {
    const diff = p.difficulty || "";
    return (
      '<article class="problem" id="' + p.id + '">' +
        '<div class="problem__top">' +
          '<h2 class="problem__title">' + esc(p.lc ? p.lc + ". " : "") + esc(p.title) + "</h2>" +
          (diff ? '<span class="badge badge--' + esc(diff) + '">' + esc(diff) + "</span>" : "") +
          (p.url ? '<a class="lc" href="' + esc(p.url) + '" target="_blank" rel="noopener">' + (String(p.url).indexOf("codeforces") !== -1 ? "Mở Codeforces ↗" : "Mở đề ↗") + "</a>" : "") +
        "</div>" +
        (p.statement || "") +
        "<h3>Cách giải</h3>" +
        (p.approach || "") +
        '<div class="complexity">' +
          "<div><strong>Time</strong>" + esc(p.time) + "</div>" +
          "<div><strong>Space</strong>" + esc(p.space) + "</div>" +
        "</div>" +
        "<h3>Code</h3>" +
        renderCodebox(p.codes, lang) +
      "</article>"
    );
  }

  function selectCourse(raw) {
    const id = window.DSA_COURSE;
    if (!raw) return raw;
    if (!id) return raw;
    const course = (raw.courses || []).find((c) => c.id === id);
    if (!course) return { notice: raw.notice, courses: [] };
    return {
      notice: course.notice || raw.notice,
      courses: [course],
    };
  }

  function renderAll(data, lang) {
    const toc = [];
    const body = [];
    toc.push("<h2>Mục lục</h2>");
    const single = (data.courses || []).length === 1;
    data.courses.forEach((course) => {
      if (!single) toc.push('<div class="toc__course">' + esc(course.title) + "</div>");
      body.push('<section class="topic" id="' + course.id + '">');
      course.topics.forEach((topic) => {
        toc.push('<a class="toc__topic" href="#' + topic.id + '">' + esc(topic.title) + "</a>");
        body.push(
          '<h2 class="topic__head" id="' + topic.id + '">' + esc(topic.title) + "</h2>" +
          (topic.lead ? '<p class="topic__lead">' + topic.lead + "</p>" : "")
        );
        topic.problems.forEach((p) => {
          toc.push('<a href="#' + p.id + '">' + esc(p.title) + "</a>");
          body.push(renderProblem(p, lang));
        });
      });
      body.push("</section>");
    });
    return { toc: toc.join(""), body: body.join("") };
  }

  function boot() {
    const data = selectCourse(window.DSA_HW);
    if (!data) return;
    const lang = loadLang();
    const { toc, body } = renderAll(data, lang);
    document.getElementById("toc").innerHTML = toc;
    const notice = document.getElementById("notice");
    if (notice && data.notice) notice.innerHTML = data.notice;
    document.getElementById("content").insertAdjacentHTML("beforeend", body);
    setLang(document, lang);

    document.addEventListener("click", (e) => {
      const tab = e.target.closest(".tab");
      if (tab) {
        const next = tab.dataset.lang;
        saveLang(next);
        document.querySelectorAll(".codebox").forEach((box) => setLang(box, next));
        return;
      }
      const copy = e.target.closest(".copy");
      if (copy) {
        const box = copy.closest(".codebox");
        const ed = box.querySelector(".editor.is-active .src");
        const text = ed ? ed.textContent : "";
        navigator.clipboard.writeText(text).then(() => {
          copy.textContent = "Copied!";
          setTimeout(() => { copy.textContent = "Copy"; }, 1200);
        });
      }
    });

    const themeBtn = document.getElementById("themeBtn");
    themeBtn?.addEventListener("click", () => {
      const cur = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", cur);
      try { localStorage.setItem("epTheme", cur); } catch (_) { /* ignore */ }
    });
  }

  boot();
})();
