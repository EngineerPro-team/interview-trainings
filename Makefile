# EngineerPro rebuild — static site Makefile
#
#   make github   -> generate docs/ folder (what GitHub Pages serves)
#   make serve    -> serve docs/ locally on http://localhost:8001
#   make dev      -> generate docs + serve in one shot
#   make clean    -> remove docs/

SRC_DIR  := src
DOCS_DIR := docs
PORT     := 8001
# Override with: make PYTHON=python3 crawl
PYTHON   ?= python3.11

.PHONY: github serve dev clean crawl crawl-courses crawl-podcasts crawl-faqs crawl-resources parse-stories crawl-story-images crawl-story-bodies translate-stories fix-translations clean-story-html seo prerender og masks help

help:
	@echo "EngineerPro rebuild — available targets:"
	@echo "  make crawl           Refresh all data files (courses + podcasts + FAQ + resources)"
	@echo "  make crawl-courses   Just the course pages (~10 after EXCLUDED_SLUGS) → src/assets/courses-data.js"
	@echo "  make crawl-podcasts  Just the Substack archive → src/assets/podcasts-data.js"
	@echo "  make crawl-faqs      Just the FAQ page         → src/assets/faqs-data.js"
	@echo "  make crawl-resources Just YouTube playlists    → src/assets/resources-data.js"
	@echo "  make parse-stories   Parse sheet markdown      → src/assets/stories-data.js"
	@echo "  make crawl-story-images  Match + download covers (run after parse-stories)"
	@echo "  make og              Re-generate share card    → src/assets/img/og-share.png"
	@echo "  make masks           Convert raster logos      → src/assets/img/companies/*-mask.png"
	@echo "  make github          Generate $(DOCS_DIR)/ from $(SRC_DIR)/ for GitHub Pages"
	@echo "  make serve           Serve $(DOCS_DIR)/ at http://localhost:$(PORT)"
	@echo "  make dev             Generate + serve"
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

prerender:
	@echo "→ Prerendering route HTML pages under docs/ ..."
	@$(PYTHON) scripts/build_pages.py

masks:
	@echo "→ Converting raster company logos to silhouette masks ..."
	@$(PYTHON) scripts/mask_logos.py

github: seo
	@echo "→ Generating $(DOCS_DIR)/ from $(SRC_DIR)/ ..."
	@rm -rf $(DOCS_DIR)
	@mkdir -p $(DOCS_DIR)
	@cp -R $(SRC_DIR)/. $(DOCS_DIR)/
	@touch $(DOCS_DIR)/.nojekyll
	@echo "→ Prerendering route pages ..."
	@$(PYTHON) scripts/build_pages.py
	@echo "✓ $(DOCS_DIR)/ ready — commit & push, then enable GitHub Pages on /docs."

serve:
	@if [ ! -d "$(DOCS_DIR)" ]; then \
		echo "✗ $(DOCS_DIR)/ not found. Run 'make github' first."; exit 1; \
	fi
	@echo "→ Serving $(DOCS_DIR)/ at http://localhost:$(PORT)  (Ctrl+C to stop)"
	@cd $(DOCS_DIR) && python3 -m http.server $(PORT)

dev: github serve

clean:
	@rm -rf $(DOCS_DIR)
	@echo "✓ Removed $(DOCS_DIR)/"
