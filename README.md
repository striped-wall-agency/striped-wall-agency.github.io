# Striped Wall

Static English-language studio website for GitHub Pages. No deployment build step or dependencies.

- `index.html` — homepage and Selected Work.
- `work/subdesk/index.html` — Subdesk concept case study.
- `assets/css/home.css` and `subdesk.css` — source design rules, in their original cascade order.
- `assets/css/base.css` — shared accessibility, navigation and responsive rules.
- `assets/js/navigation.js` — progressive enhancement for the compact navigation. Without JavaScript, navigation remains visible.
- `scripts/check_site.py` — local structure and link checks using Python's standard library.
- `scripts/inline_styles.py` — embed CSS sources in both pages to eliminate render-blocking stylesheet requests.
- `CNAME` — custom domain; retain when updating the site.

Preview from the repository root with `python3 -m http.server 8000`, then visit `http://localhost:8000`. Check with `python3 scripts/check_site.py` and `git diff --check`.

After editing files in `assets/css/`, run `python3 scripts/inline_styles.py` and commit both the CSS sources and updated HTML. The checker rejects stale embedded styles. Google Fonts loads asynchronously with system font fallbacks and a `noscript` stylesheet for visitors without JavaScript.

To add a case, create `work/<name>/index.html`, use relative paths (`../../assets/` and `../../index.html#work`), and replace its homepage placeholder with a real link. Add the page to the checker and the stylesheet script's `PAGES` mapping, preserve the semantic navigation and disclosures, and review desktop and mobile layouts. Existing Subflow and Paycontrol cards intentionally have no case links.

Subdesk uses fictional data stored in the browser's IndexedDB. It has no real payment provider, money movement or server authentication. Case visuals are illustrative HTML/CSS recreations, not captured screenshots or working controls. Historical demo checks described in the source case do not constitute verification of the live demo by this website change.
