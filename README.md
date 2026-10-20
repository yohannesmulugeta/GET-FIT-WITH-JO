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
- The original three training video posters were reduced **103.9 KB → 50.4 KB** in the October 2026 performance pass; the current two posters are also deferred until their cards approach the viewport.
- Training clips use `preload="none"` and aren't downloaded until played.
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

### Verified final Lighthouse result

| Category | Mobile | Desktop |
|---|---:|---:|
| Performance | **98** | **100** |
| Accessibility | **100** | **100** |
| Best practices | **100** | **100** |
| SEO | **100** | **100** |
| FCP | 1.3 s | 0.2 s |
| LCP | 1.5 s | 0.3 s |
| Speed Index | 2.5 s | 0.2 s |
| TBT | 160 ms | 0 ms |
| CLS | 0 | 0 |

Measured by Lighthouse in GitHub Actions run #38462279373. Run-to-run variation and real-world network differences remain.

**Deployment compatibility:** Both the source `index.html` and published build include the same CSS inline because GitHub Pages has run both branch-based and Actions-based deployment jobs. When changing `styles.css`, synchronize the `<style id="site-css">` block in `index.html` before publishing. `build_site.py` keeps the published copy synchronized.

## Image and fact integrity

- `joseph-*-fast.webp` files are **AI-assisted illustrative visual concepts** based on supplied Joseph photos. They are **not** documentary evidence of Joseph coaching any particular person at any location. Joseph must approve the likeness and usage before promotion.
- `original-*.jpg` and `original-*.mp4` are preserved unaltered in the GitHub repository. The two featured clips are edits of newer supplied MOV files; the full MOV files are not checked in.
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

## Restored coaching content (2026-10-14)
The original sport-science statement, biography and family sports history, all seven services, six target audiences, package formats, client-progress example, social discovery and a dedicated About page have been restored.
No archival photos or videos or brand colors were replaced. Confirm the 14-year versus four-year experience wording, pricing, testimonial publication permissions and official social handles with Joseph before advertising.
See CONTENT_RESTORATION.md for the full provenance and confirmation list.

## October 2026 approved portrait refresh

The 4 new AI-assisted Joseph reference portraits were prepared for the website as 10 responsive, optimized WebP images. Hero, avatar, About, lifestyle, strength, program-card, philosophy, and share-preview slots have been updated using existing asset paths. The generated images are creative portraits, not documentation of real training sessions or clients. Brand styling, original video footage, client content, and WhatsApp/email enquiry features were preserved.

## October 2026 training footage refresh

The two featured clips are 12-second edits from supplied `IMG_1544.MOV` (5–17 seconds) and `IMG_1573.MOV` (18–30 seconds). They were converted from HDR HEVC to SDR H.264 MP4 at 720 × 1280 and 30 fps, with audio removed. Matching WebP posters are used in the training cards, and the floor-training poster also replaces the former low-resolution Results still. The About section links directly to the footage.

The five older `original-mp4-*.mp4` files and their posters remain in the source archive but are no longer referenced or included in the published build. New videos retain `preload="none"`; playback and layout were checked in a browser at desktop and mobile widths.

## October 2026 — Services and consultation update

- Primary navigation uses **Services** and **Book Consultation**, not Contact.
- Training videos and four gallery cards are grouped under one Gallery section. Duplicated package, process, and generic journey sections have been removed; seven services and the factual client account remain.
- Consultation preferences (date, time period, service, training format, and goals) are sent to the existing FormSubmit email endpoint or included in a WhatsApp message. These are *requests*, not confirmed bookings.
- CBE, Abyssinia, and telebirr cards contain local logos and click-to-copy functionality. **The bank numbers are demonstration values and must not receive payments.** The telebirr contact number requires receiving-wallet confirmation.
- Supplied Facebook and TikTok accounts are linked. Instagram and LinkedIn currently go to the platform homepages.
- The header and mobile bar expose tap-to-call/WhatsApp links. For logos, payment accuracy and privacy notes, see `PAYMENT_AND_BOOKING_NOTES.md`.
