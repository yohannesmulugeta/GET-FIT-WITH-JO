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
if source.count(placeholder) != 1:
    sys.exit('Expected one stylesheet link in the source HTML.')
# HTML already has a high-priority, responsive preload for the LCP image.
# Inline CSS eliminates a blocking stylesheet network round trip.
result = source.replace(placeholder, '<style>\n'+style+'\n</style>')

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
