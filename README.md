# Get Fit with JO — Fast, mobile-first coaching website

Professional single-page website for Joseph Abraham / Get Fit with JO. Hosted using GitHub Pages.

**Live:** https://yohannesmulugeta.github.io/GET-FIT-WITH-JO/

## Local development

```bash
python3 test_site.py
python3 -m http.server 8000
```

Open `http://localhost:8000` for the source preview. To preview the actual optimized deployment, run:

```bash
python3 build_site.py
cd dist
python3 -m http.server 8000
```

`index.html` and `styles.css` remain separately editable. `build_site.py` generates the production `dist/` directory, inlines the small CSS file to remove render-blocking stylesheet requests, and copies only referenced assets. This has **no JavaScript build system or paid dependency**.

## Performance improvements (October 2026)

- Responsive hero images: **16.8 KB mobile**, **32.1 KB desktop**.
- Coach avatar reduced **103.8 KB → 3.1 KB**.
- Seven prominent photos total reduced **772.6 KB → 147.6 KB** (about **81% less**); same visual concepts, reduced pixel count/encoding only.
- Three training video posters reduced **103.9 KB → 50.4 KB**, and are loaded only when their clips approach the viewport.
- Client's three original training clips use `preload="none"` and aren't downloaded until played.
- Render-blocking Google Fonts removed; stable system font stack used.
- CSS inlined only **in production** by the deployment build; source CSS stays modular.
- Images have intrinsic dimensions, lazy loading below the fold, and asynchronous decoding. Responsive hero is preloaded by device width.
- Removed unused media from the published artifact (the original files are safely retained in repository).
- Improved contrast for small UI text by using dark navy/darker teal while preserving the original orange/teal/navy palette.

## Lighthouse testing

`.github/workflows/site-audit.yml` runs Google Lighthouse after every successful GitHub Pages deployment, recording mobile and desktop scores and Core Web Vitals lab metrics. Check the Actions tab and download `website-lighthouse-<run-id>` report artifacts.

The previous version's live Lighthouse baseline (October 13, 2026):

| Metric | Mobile | Desktop |
| --- | ---: | ---: |
| Performance | 85 | 98 |
| Accessibility | 95 | 95 |
| Best practices | 100 | 100 |
| SEO | 100 | 100 |
| FCP | 2.7 s | 0.8 s |
| LCP | 3.3 s | 0.9 s |
| Speed Index | 4.5 s | 0.8 s |
| TBT | 20 ms | 0 ms |
| CLS | 0 | 0.003 |

Lighthouse lab scores vary by run/network; test again after deployment and validate actual Ethiopian mobile connections separately.

## Image and fact integrity

- `joseph-*-fast.webp` files are **AI-assisted illustrative visual concepts** based on supplied Joseph photos. They are **not** documentary evidence of Joseph coaching any particular person at any location. Joseph must approve the likeness and usage before promotion.
- `original-*.jpg` and `original-*.mp4` are preserved unaltered in the GitHub repository, and the three video clips shown are from the supplied original archive.
- Contact information, credentials and coaching services still require Joseph's factual confirmation.
- Medical support claims must not imply medical treatment. The site contains an appropriate note.
- Brand colors remain: dark navy `#0A1526`, navy `#12213B`, orange `#FF6A3D`, teal `#17A398`, off-white `#F5F6F2`.
- No tracking, databases or cookies are used.

## Files

- `index.html` — semantic copy, HTML and SEO metadata
- `styles.css` — mobile-first responsive styling (inlined for production)
- `script.js` — menu, video/poster interactions
- `test_site.py` — repeatable integrity tests
- `build_site.py` — GitHub Pages build step
- `assets/` — optimized images, original photographs/video archive, video posters
- `robots.txt`, `sitemap.xml` — search discovery

## Approval checklist

- [ ] Confirm official biography, services, credentials, WhatsApp, email and phone.
- [ ] Have Joseph explicitly approve the AI-generated visual likeness.
- [ ] Test WhatsApp links using an actual mobile phone.
- [ ] Review the experience on slow Ethiopian mobile data connections.
- [ ] Add verified social accounts later if desired.
