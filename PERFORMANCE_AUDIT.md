# Get Fit with JO — Performance audit

Date: 2026-10-13. Site: https://yohannesmulugeta.github.io/GET-FIT-WITH-JO/

## Before optimization: verified live Google Lighthouse

| Area | Mobile | Desktop |
|---|---:|---:|
| Performance score | 85 | 98 |
| Accessibility score | 95 | 95 |
| Best practices score | 100 | 100 |
| SEO score | 100 | 100 |
| First Contentful Paint | 2.7 s | 0.8 s |
| Largest Contentful Paint | 3.3 s | 0.9 s |
| Speed Index | 4.5 s | 0.8 s |
| Total Blocking Time | 20 ms | 0 ms |
| Cumulative Layout Shift | 0 | 0.003 |

Source: GitHub Actions `Website quality and Lighthouse audit` run #38460642150, based on actual deployed website. Lighthouse identified render-blocking resources and right-sizing of images as major mobile opportunities (estimates: ~1,473 ms and ~280 ms respectively). The diagnostics report opportunities, not guaranteed time savings.

## Fixes implemented

1. Eliminate Google Fonts network requests and reliance on third-party resources at initial render.
2. Inline the ~22 KB stylesheet in the production HTML, avoiding one stylesheet round trip; keep the CSS separate in editable source.
3. Replace a large coach avatar with a visually equivalent 196 px WebP.
4. Deliver separate desktop and mobile hero pictures, crop carefully around the subject, and preload only the matching variant.
5. Resize/recompress all prominent pictures without changing the brand palette or illustrations.
6. Defer poster images until videos are near the viewport. Videos retain `preload=none`.
7. Use intrinsic dimensions on all images, keep lazy image loading, and prefer stable system fonts to minimize layout shifts.
8. Publish only referenced images and original training clips. Keep original source media in GitHub.
9. Enhance accessible button contrast, mobile touch targets, semantic labels and SEO canonical metadata.

### Measured image transfer changes

| Resource | Before | After |
|---|---:|---:|
| Hero image (mobile) | 89,326 B | 16,824 B |
| Hero image (desktop) | 89,326 B | 32,068 B |
| Avatar | 103,828 B | 3,062 B |
| Seven prominent images, desktop variants | 772,626 B | 147,640 B |
| Three video poster images | 103,930 B | 50,362 B |

All original customer photographs and MP4 videos remain unchanged in the source repository.

## Testing coverage and limits

`test_site.py` passes 18 static checks: assets, navigation anchors, HTML image attributes, accessible mobile menu controls, protected external links, canonical/SEO files, responsive CSS breakpoint coverage, safe video loading, and preserved colors. `node --check script.js` and CSS parser validation also passed. GitHub Actions runs real Lighthouse for both desktop and mobile against the deployed site.

**These numbers are file sizes, not reported network/interaction measurements.** Live post-deployment Lighthouse scores are recorded in GitHub Actions audit logs and artifacts once the new deployment is complete. Physical iOS/Android devices, real Ethiopia mobile carriers, and keyboard/screen-reader end-to-end behavior should also be reviewed independently before treating the site as fully validated.
