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
check('Video posters are deferred',len(p.videos)==3 and all(v.get('data-poster') and not v.get('poster') for v in p.videos))
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

for name,ok,details in tests:
    print(('PASS' if ok else 'FAIL')+'  '+name+((': '+details) if details and not ok else ''))
print(f'\n{sum(ok for _,ok,_ in tests)}/{len(tests)} source checks passed')
sys.exit(0 if all(ok for _,ok,_ in tests) else 1)
