"""Static website smoke tester, no third-party dependencies required.

Run: python test_site.py
This checks source integrity, not browser rendering or Google's PageSpeed score.
"""
from pathlib import Path
from html.parser import HTMLParser
import re
import sys

ROOT = Path(__file__).resolve().parent
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')
CSS = (ROOT / 'styles.css').read_text(encoding='utf-8')
JS = (ROOT / 'script.js').read_text(encoding='utf-8')

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.refs = []
        self.alt_missing = []
        self.img_without_dimensions = []
        self.h1 = 0
        self.links = []
        self.external_links = []
        self.videos = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'img':
            if not a.get('alt'): self.alt_missing.append(a.get('src'))
            if not a.get('width') or not a.get('height'): self.img_without_dimensions.append(a.get('src'))
        if tag == 'a':
            self.links.append(a.get('href',''))
            if a.get('target') == '_blank': self.external_links.append(a)
        if tag == 'video': self.videos.append(a)
        for key in ('src','srcset','data-poster','poster','href'):
            v = a.get(key,'')
            if v.startswith('assets/'):
                self.refs.extend(v.split(',')[0].split())

p = SiteParser(); p.feed(HTML)
tests = []
def check(name, cond, detail=''):
    tests.append((name,bool(cond),detail))

check('Exactly one main H1', p.h1==1)
check('IDs are unique', len(p.ids)==len(set(p.ids)))
check('Local anchor links resolve',all(link[1:] in p.ids for link in p.links if link.startswith('#') and len(link)>1))
check('All linked local assets exist', all((ROOT / ref).is_file() for ref in p.refs), ', '.join(ref for ref in p.refs if not (ROOT / ref).is_file()))
check('All images have descriptions', not p.alt_missing, repr(p.alt_missing))
check('All images reserve layout dimensions', not p.img_without_dimensions,repr(p.img_without_dimensions))
check('Videos avoid preloading', all(v.get('preload')=='none' for v in p.videos))
check('Video posters are deferred',len(p.videos)==2 and all(v.get('data-poster') and not v.get('poster') for v in p.videos))
check('No external CSS/JS blockers', 'fonts.googleapis.com' not in HTML and not re.search(r'<script[^>]+src=["\']https?://',HTML))
check('Hero mobile and desktop candidates', 'joseph-hero-fast.webp' in HTML and 'joseph-hero-mobile-fast.webp' in HTML and 'fetchpriority="high"' in HTML)
check('Responsive breakpoints present', all(f'@media(max-width:{x}px)' in CSS for x in (1120,900,700,510,350)))
check('Responsive site meta', '<meta name="viewport" content="width=device-width, initial-scale=1">' in HTML)
check('Mobile menu is accessible', 'aria-expanded="false"' in HTML and 'aria-controls="site-nav"' in HTML and 'Escape' in JS)
check('External links use safe rel', all('noopener' in a.get('rel','') for a in p.external_links))
check('Canonical and share preview configured', 'rel="canonical"' in HTML and 'property="og:image"' in HTML)
check('Site can index', 'User-agent' in (ROOT/'robots.txt').read_text() and '<urlset' in (ROOT/'sitemap.xml').read_text())
check('Core brand palette preserved', all(x in CSS for x in ['#12213B','#0A1526','#FF6A3D','#17A398','#F5F6F2']))
check('All non-archival image files are under 70 KB', all(x.stat().st_size<70000 for x in (ROOT/'assets').glob('*-fast.webp')))

# Full content restoration guard: preserve the original coaching offer in future redesigns.
ABOUT = (ROOT/'about.html').read_text(encoding='utf-8') if (ROOT/'about.html').exists() else ''
services = ['Private Personal Training','Online Personal Training','Sport Nutrition Coaching','Chronic Disease Support','Adaptive Exercise',"Children's Sport &amp; Fitness",'Corporate &amp; Community Wellness']
check('Dedicated About page exists',bool(ABOUT) and 'My passion for sport' in ABOUT)
check('Original sport science claim restored', 'Training built on 14 years of sport science, not guesswork.' in HTML)
check('Experience and sports qualifications retained', all(x in HTML for x in ['BSc Sport Science','14 years','4 years']))
check('All seven services appear', all(x in HTML for x in services), ', '.join(x for x in services if x not in HTML))
check('Audience section restored', 'id="audiences"' in HTML and HTML.count('class="audience-tile"') == 6)
check('Coaching package options restored', HTML.count('class="package-option"') == 3)
check('Original three-step process preserved', all(x in HTML for x in ['Message me your goals','Get a plan built around you','Train, track, adjust']))
check('Proof-of-work and social sections exist', 'id="results"' in HTML and 'id="social"' in HTML)
check('No invented social profile URLs', all(x not in HTML for x in ['href="https://instagram.com"','href="https://tiktok.com"','href="https://facebook.com"']))
check('Father football history restored', 'Ethiopian Premier League in the 1980s' in ABOUT)
check('About page added to sitemap', 'about.html' in (ROOT/'sitemap.xml').read_text(encoding='utf-8'))
p2 = SiteParser(); p2.feed(ABOUT)
check('Dedicated About has exactly one H1 and unique IDs',p2.h1==1 and len(p2.ids)==len(set(p2.ids)))
check('Dedicated About anchor targets work',all(v[1:] in p2.ids for v in p2.links if v.startswith('#') and len(v)>1))
check('About page images exist and have dimensions', not p2.alt_missing and not p2.img_without_dimensions and all((ROOT / v).is_file() for v in p2.refs))
check('Both pages have identical inline CSS', '<style id="site-css">' in HTML and '<style id="site-css">' in ABOUT and CSS.strip() in HTML and CSS.strip() in ABOUT)
check('All four colors preserved across pages', all(code in CSS for code in ['#12213B','#FF6A3D','#17A398','#F5F6F2']))

# Dual-channel contact form: validate the actual published structure and safe client flows.
form_options=['Private Personal Training','Online Personal Training','Sport Nutrition Coaching','Chronic Disease Support','Adaptive Exercise',"Children's Sport &amp; Fitness",'Corporate &amp; Community Wellness']
check('Coaching enquiry section exists and is linked', 'id="enquiry"' in HTML and 'id="coach-enquiry-form"' in HTML and 'href="index.html#enquiry"' in ABOUT)
check('Email form has real FormSubmit endpoint', 'action="https://formsubmit.co/josi1983ab@gmail.com"' in HTML and 'target="_blank" method="POST"' in HTML)
check('WhatsApp enquiry uses actual contact', 'id="enquiry-whatsapp-button"' in HTML and 'https://wa.me/251986890425' in HTML)
check('All seven coaching services in form', all(x in HTML[HTML.find('id="coach-enquiry-form"'):] for x in form_options))
check('Form includes required identity, goal and consent', all(x in HTML for x in ['name="name"','name="phone"','name="email"','name="service"','name="message"','id="enquiry-consent"','required']))
check('Spam honeypot, privacy and accessibility included', all(x in HTML for x in ['name="_honey"','role="status"','aria-live="polite"','https://formsubmit.co/privacy.pdf']))
check('Email send uses native FormSubmit POST without blocked AJAX', all(x in JS for x in ["coachingForm.addEventListener('submit'",'validateEnquiry(true)', 'event.preventDefault()', 'secure email submission page']) and 'data-email-endpoint=' not in HTML)
check('WhatsApp prefilled message requires user click and validation', all(x in JS for x in ["whatsappButton.addEventListener('click'",'encodeURIComponent(message)','validateEnquiry(false)','reportValidity()']))
check('Email submit checks phone or email for reply', 'validateEnquiry(true)' in JS and 'fields.email.value.trim()' in JS and 'fields.phone.value.trim()' in JS)
check('Provider confirmation before email delivery is documented', 'must confirm the receiving email address' in JS and 'one-time inbox confirmation' in HTML)


# Review branch: new sections must be present, navigable, and clearly temporary.
check('Gallery, transformations, FAQ and booking are linked correctly', all(('id="'+s+'"') in HTML for s in ('gallery','transformations','faq','booking')) and all(('href="#'+s+'"') in HTML for s in ('gallery','faq')))
check('Preview photos explicitly credited to Coach Miki', HTML.count('REFERENCE PHOTO · COACH MIKI')==4 and 'COACH MIKI EXAMPLE · NOT A JO RESULT' in HTML)
check('No transformation results attributed to JO', 'this is not joseph' in HTML.lower() and 'Replace with a consenting JO client' in HTML)
check('FAQ native disclosure is accessible', 'class="jo-faq-items"' in HTML and HTML.count('<details>')==6 and HTML.count('<summary>')==6)
check('Booking keeps existing email and WhatsApp form', 'id="jo-not-used"' not in HTML and 'id="coach-enquiry-form"' in HTML and 'jo-booking-steps' in HTML)
check('Image sources are external reference URLs, not copied assets', HTML.count('https://coachmikiaddis.com/images/')==5 and 'data-image-slot="gallery-01"' in HTML)

for name,ok,details in tests:
    print(('PASS' if ok else 'FAIL')+'  '+name+((': '+details) if details and not ok else ''))
print(f'\n{sum(ok for _,ok,_ in tests)}/{len(tests)} source checks passed')
sys.exit(0 if all(ok for _,ok,_ in tests) else 1)
