"""Build fast, dependency-free GitHub Pages output.

Inlines the small CSS file into the document to eliminate a render-blocking
request, then copies ONLY the assets referenced by the published site.
The original client photos/videos stay in the repository for future edits.
"""
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
source = (ROOT / 'index.html').read_text(encoding='utf-8')
style = (ROOT / 'styles.css').read_text(encoding='utf-8')
placeholder = '<link rel="stylesheet" href="styles.css">'
inline_css = '<style id="site-css">\n' + style + '\n</style>'
# Source HTML also keeps CSS inlined so both legacy branch-based Pages and
# Actions-based Pages deploy the same non-blocking design. Rebuild is idempotent.
if source.count(placeholder) == 1:
    result = source.replace(placeholder, inline_css)
elif '<style id="site-css">' in source:
    result = re.sub(r'<style id="site-css">.*?</style>', lambda _: inline_css, source, count=1, flags=re.DOTALL)
else:
    sys.exit('Expected the site CSS link or inlined site-css marker.')

if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()
(DIST / 'index.html').write_text(result,encoding='utf-8')
for name in ['script.js','robots.txt','sitemap.xml']:
    shutil.copy2(ROOT / name, DIST / name)
(DIST / 'assets').mkdir()
asset_names = set(re.findall(r'assets/([A-Za-z0-9._-]+)',result))
for name in sorted(asset_names):
    source_asset = ROOT / 'assets' / name
    if not source_asset.is_file():
        sys.exit('Missing asset '+str(source_asset))
    shutil.copy2(source_asset, DIST / 'assets' / name)

print('Deployment output:',DIST)
print('Inline CSS:',len(style.encode('utf-8')),'bytes; zero external font/CSS requests')
print('Assets:',len(asset_names),'\n'+'\n'.join('  '+n for n in sorted(asset_names)))
print('Published folder total:',sum(p.stat().st_size for p in DIST.rglob('*') if p.is_file()),'bytes')
