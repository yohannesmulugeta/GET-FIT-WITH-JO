# Get Fit with JO — gallery and booking review branch

This is a **draft implementation** intended to be reviewed before merging into `main`.

## Added
1. Four-card responsive training photo gallery.
2. Reference transformation image and empty JO client-results card.
3. Six FAQs using accessible native `<details>` elements.
4. Clear three-step coaching enquiry guidance above the existing email/WhatsApp form.
5. Responsive design polish in the original navy/orange/teal identity.

## Temporary third-party photographs: NOT CLEARED FOR PRODUCTION
The new photo cards load five Coach Miki Addis photographs directly from `https://coachmikiaddis.com/images/` **as external references** (no images have been generated, downloaded, or copied into the repository). All carry persistent attribution and explicitly say they do not show JO or his clients. This is a **design preview only**. Do not merge or deploy the branch until Joseph supplies owned photographs or obtains appropriate reuse permission. Referencing external photos does not grant any license and hotlinking may stop working.

| New slot | Temporary source | Final JO replacement |
| --- | --- | --- |
| `gallery-01` | `gallery-1.jpg` | Joseph coaching a private client |
| `gallery-02` | `gallery-2.jpg` | JO technique or gym photograph |
| `gallery-03` | `gallery-6.jpg` | JO group/community training |
| `gallery-04` | `gallery-5.jpg` | JO stretching or training session |
| `transformation-example` | `transformation-1.jpg` | Approved JO client before/after photos |
| `transformation-01` | No photo | Additional approved JO client story |

**Replacement:** locate `data-image-slot="gallery-01"` etc. in `index.html`, replace the nearby external `<img src>` with local optimized files under `assets/`, update widths, heights and alt text, remove reference badges and temporary disclaimer once everything is verified. The asset whitelist in `build_site.py` copies locally referenced files automatically. Do not reuse source content or client outcome claims.

## Required checks before release
- Confirm client photo ownership, explicit consent, original before-and-after context, and accuracy.
- Confirm Joseph's current service rates, schedules, coaching locations, payment methods and contact details.
- Activate and test the FormSubmit email destination with Joseph (see `ENQUIRY_FORM_SETUP.md`).
- Run `python test_site.py`, `node --check script.js`, and `python build_site.py`; visually review small Android widths, desktop and keyboard navigation.
- Check slow mobile connections in Ethiopia after using locally optimized replacement photos.

**Existing hero photography, program text, training videos, About page, contact methods and main-branch deployment remain intact.**
