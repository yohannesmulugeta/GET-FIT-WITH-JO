# Get Fit with JO — Coaching enquiry form setup

## What has been built

- **Email:** AJAX submission from the homepage form to `https://formsubmit.co/ajax/josi1983ab@gmail.com` via FormSubmit.co. The ordinary HTML form POSTs to `https://formsubmit.co/josi1983ab@gmail.com` if JavaScript is unavailable.
- **WhatsApp:** an alternative link to `+251 986 890 425`, with the visitor's entered information included in the pre-filled message. The visitor presses **Send** inside WhatsApp themselves. No WhatsApp API or monthly subscription is required.
- The About page links directly to the form on the homepage: `index.html#enquiry`.
- Users choose among all seven coaching categories, including adaptive, children’s, and community wellness coaching. The form asks for name, a contact method, service, training location, goals and consent. It does **not** ask for health records.
- Spam protection includes FormSubmit's built-in protections and a hidden honeypot. Its AJAX endpoint does not need a backend or a token embedded in GitHub Pages.

## IMPORTANT: one-time email activation (required)

FormSubmit.co requires confirmation of the receiving email address on first use. **Deploying this code does not itself activate the destination mailbox or prove that any email was delivered.**

1. Make sure Joseph agrees that `josi1983ab@gmail.com` is his correct receiving address (currently listed on the website).
2. Submit **one clearly labelled setup test** from the live enquiry form using non-personal test data.
3. Joseph checks that inbox, including Spam/Promotions, for FormSubmit's activation/confirmation message, and clicks its confirmation link.
4. After activation, submit a second test. Verify the complete enquiry reaches Joseph's inbox and that the Reply-To address allows a reply.
5. Test WhatsApp: fill the form, choose WhatsApp, verify that the message opens for `+251986890425`, and **do not press Send** unless you want to deliver the test message.

If FormSubmit returns an error, the webpage leaves entered values in place and offers WhatsApp as an alternative. FormSubmit states that it retains submissions for up to 30 days; see https://formsubmit.co/documentation and https://formsubmit.co/privacy.pdf. Do not collect private medical information in general enquiries.

## Maintenance and testing

- Edit the receiving email in **both** `action` and `data-email-endpoint` in `index.html` if Joseph requests a new address. A new destination requires email activation again.
- Edit the number in the `enquiry-whatsapp-button` fallback link and in `script.js` if it changes.
- Keep `styles.css` synchronized with inline `<style id="site-css">` in both HTML pages, as required by the source tests and Pages setup.
- Run `python3 test_site.py`, `node --check script.js`, and `python3 build_site.py` from the repository root.
- The email success status means the third-party form service acknowledged the submission, not independently confirmed delivery to an unactivated mailbox.
