// English versions of resource subtitles / descriptions / titles.
// Keys mirror the structure of window.RESOURCES in resources-data.js.
window.RESOURCES_EN = {
  foundation: {
    subtitle: "16 programming foundation videos (C++ · Java · Golang · Python)",
    description:
      "Free 16-video series produced by EngineerPro — covering Introduction, Conditionals, Loops, Functions, Arrays, Strings, Classes, Recursion, Sorting, Linked Lists, HashMap/HashSet, Trees, and Graphs. Every video is delivered in 4 popular languages: C++, Java, Golang, Python.",
    videoCountLabel: "videos",
  },
  cv: {
    intro:
      "4 references to help you write a Big Tech-ready CV — a sample CV that passed Google, a LaTeX template, real CV-review videos, and a quick CV-generation tool.",
    sample: {
      title: "Sample CV — passed Google interview",
      subtitle: "Real CV from an EngineerPro student · reference for format & phrasing",
    },
    overleaf: {
      title: "Overleaf — Software Engineer Resume Template",
      subtitle: "Dedicated LaTeX template for SWE — clean, ATS-friendly",
    },
    review: {
      title: "CV Review",
      subtitle: "Big Tech mentors reviewing real student CVs",
      description:
        "50+ episode series where EngineerPro mentors review students' CVs — pointing out common mistakes, how to phrase impact, and how to lay things out. Watch to avoid pitfalls and write a Big Tech-ready CV.",
      episodeCta: (n) => `Watch ${n} episodes ↗`,
    },
    tool: {
      title: "How to write a CV with a professional tool",
    },
  },
};

// VI counterpart of just the dynamic labels (so the renderer doesn't sprinkle
// VI strings in the code).
window.RESOURCES_VI_LABELS = {
  foundation: { videoCountLabel: "video" },
  cv: { review: { episodeCta: (n) => `Xem ${n} tập ↗` } },
};
