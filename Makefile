# EngineerPro rebuild — static site Makefile
#
#   make github   -> generate docs/ folder (what GitHub Pages serves)
#   make serve    -> serve docs/ locally on http://localhost:8001
#   make dev      -> generate docs + serve in one shot
#   make clean    -> remove docs/

SRC_DIR   := src
DOCS_DIR  := docs
LOCAL_DIR := _local
PORT      := 8001
# Override with: make PYTHON=python3 crawl
PYTHON   ?= python3.11

.PHONY: github local-build serve dev clean crawl crawl-courses crawl-podcasts crawl-faqs crawl-resources crawl-cs-fundamental parse-stories crawl-story-images crawl-story-bodies translate-stories fix-translations clean-story-html seo stats prerender og masks help

help:
	@echo "EngineerPro rebuild — available targets:"
	@echo "  make crawl           Refresh all data files (courses + podcasts + FAQ + resources)"
	@echo "  make crawl-courses   Just the course pages (~10 after EXCLUDED_SLUGS) → src/assets/courses-data.js"
	@echo "  make crawl-podcasts  Just the Substack archive → src/assets/podcasts-data.js"
	@echo "  make crawl-faqs      Just the FAQ page         → src/assets/faqs-data.js"
	@echo "  make crawl-resources Just YouTube playlists    → src/assets/resources-data.js"
	@echo "  make crawl-cs-fundamental LeetCode Discuss CS Q → src/assets/cs-fundamental-questions-data.js"
	@echo "  make parse-stories   Parse sheet markdown      → src/assets/stories-data.js"
	@echo "  make crawl-story-images  Match + download covers (run after parse-stories)"
	@echo "  make og              Re-generate share card    → src/assets/img/og-share.png"
	@echo "  make masks           Convert raster logos      → src/assets/img/companies/*-mask.png"
	@echo "  make github          PROD build of $(DOCS_DIR)/ for GitHub Pages (uses EP_BASE_URL + EP_BASE_PATH)"
	@echo "  make local-build     LOCAL build of $(DOCS_DIR)/ for serving from localhost root (no subpath)"
	@echo "  make serve           Serve $(DOCS_DIR)/ at http://localhost:$(PORT)"
	@echo "  make dev             local-build + serve (the right command for local preview)"
	@echo "  make clean           Remove $(DOCS_DIR)/"

crawl: crawl-courses crawl-podcasts crawl-faqs crawl-resources
	@echo "✓ all crawls done"

crawl-courses:
	@echo "→ Crawling course pages from engineerprogurus.com ..."
	@$(PYTHON) scripts/crawl_courses.py

crawl-podcasts:
	@echo "→ Crawling podcast archive from Substack ..."
	@$(PYTHON) scripts/crawl_podcasts.py

crawl-faqs:
	@echo "→ Crawling FAQ page from engineerprogurus.com ..."
	@$(PYTHON) scripts/crawl_faqs.py
	@echo "→ Adding EN translations to FAQ ..."
	@$(PYTHON) scripts/translate_faqs.py

crawl-resources:
	@echo "→ Crawling free interview resources (YouTube playlists) ..."
	@$(PYTHON) scripts/crawl_resources.py

crawl-cs-fundamental:
	@echo "→ Crawling CS Fundamental questions from LeetCode Discuss ..."
	@$(PYTHON) scripts/crawl_cs_fundamental_discuss.py

parse-stories:
	@echo "→ Parsing Success Stories from Google Sheet markdown ..."
	@$(PYTHON) scripts/parse_stories.py

crawl-story-images:
	@echo "→ Matching + downloading cover images for success stories ..."
	@$(PYTHON) scripts/crawl_story_images.py

crawl-story-bodies:
	@echo "→ Fetching original article HTML from Google Docs linked in sheet ..."
	@$(PYTHON) scripts/crawl_story_bodies.py

translate-stories:
	@echo "→ Translating originalHtml + originalTitle of each story to English ..."
	@$(PYTHON) scripts/translate_stories.py

translate-courses:
	@echo "→ Translating course body HTML to English ..."
	@$(PYTHON) scripts/translate_courses.py

fix-translations:
	@echo "→ Post-processing common MT artifacts in story translations ..."
	@$(PYTHON) scripts/fix_translations.py

clean-story-html:
	@echo "→ Cleaning story HTML (drop dead bullets, unwrap Google redirects) ..."
	@$(PYTHON) scripts/clean_story_html.py

og:
	@echo "→ Re-generating Open Graph share card ..."
	@$(PYTHON) scripts/make_og_image.py

seo:
	@echo "→ Generating sitemap.xml + robots.txt ..."
	@$(PYTHON) scripts/make_seo.py

stats:
	@echo "→ Auditing stat references across docs + code ..."
	@$(PYTHON) scripts/check_stats.py

prerender:
	@echo "→ Prerendering route HTML pages under docs/ ..."
	@$(PYTHON) scripts/build_pages.py

masks:
	@echo "→ Converting raster company logos to silhouette masks ..."
	@$(PYTHON) scripts/mask_logos.py

github: stats seo
	@echo "→ Generating $(DOCS_DIR)/ from $(SRC_DIR)/ ..."
	@rm -rf $(DOCS_DIR)
	@mkdir -p $(DOCS_DIR)
	@cp -R $(SRC_DIR)/. $(DOCS_DIR)/
	@touch $(DOCS_DIR)/.nojekyll
	@echo "→ Prerendering route pages ..."
	@$(PYTHON) scripts/build_pages.py
	@echo "→ Writing CNAME from EP_BASE_URL ..."
	@$(PYTHON) -c "import os,re; from scripts.site_config import BASE_URL; \
		host = re.sub(r'^https?://', '', BASE_URL).strip('/'); \
		open(os.path.join('$(DOCS_DIR)', 'CNAME'), 'w').write(host + chr(10)) if 'github.io' not in host else None"
	@echo "→ Guarding against localhost URLs in production artifact ..."
	@if grep -rIE "https?://(localhost|127\.0\.0\.1)" $(DOCS_DIR) $(SRC_DIR)/sitemap.xml $(SRC_DIR)/robots.txt 2>/dev/null; then \
		echo "✗ Production artifact contains localhost URLs above. Fix EP_BASE_URL / EP_BASE_PATH before deploying."; \
		exit 1; \
	fi
	@echo "✓ $(DOCS_DIR)/ ready — commit & push, then enable GitHub Pages on /docs."

# Local build into $(LOCAL_DIR)/ with EP_BASE_PATH="" — for local preview ONLY.
# Kept separate from $(DOCS_DIR)/ so the production deploy artefact never gets
# clobbered. $(LOCAL_DIR)/ is in .gitignore.
local-build:
	@echo "→ Building $(LOCAL_DIR)/ for LOCAL serve (no subpath) ..."
	@rm -rf $(LOCAL_DIR)
	@mkdir -p $(LOCAL_DIR)
	@cp -R $(SRC_DIR)/. $(LOCAL_DIR)/
	@touch $(LOCAL_DIR)/.nojekyll
	@EP_BASE_URL=http://localhost:$(PORT) EP_BASE_PATH= EP_OUT=$(LOCAL_DIR) $(PYTHON) scripts/make_seo.py
	@EP_BASE_URL=http://localhost:$(PORT) EP_BASE_PATH= EP_OUT=$(LOCAL_DIR) $(PYTHON) scripts/build_pages.py
	@echo "✓ $(LOCAL_DIR)/ ready for localhost (production docs/ untouched)."

serve:
	@if [ ! -d "$(LOCAL_DIR)" ]; then \
		echo "✗ $(LOCAL_DIR)/ not found. Run 'make local-build' or 'make dev' first."; exit 1; \
	fi
	@echo "→ Serving $(LOCAL_DIR)/ at http://localhost:$(PORT)  (Ctrl+C to stop)"
	@cd $(LOCAL_DIR) && python3 -m http.server $(PORT)

dev: local-build serve

clean:
	@rm -rf $(DOCS_DIR) $(LOCAL_DIR)
	@echo "✓ Removed $(DOCS_DIR)/ and $(LOCAL_DIR)/"
