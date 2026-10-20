"""Build fast and complete static pages for GitHub Pages.
CSS is inlined into both source pages; only media referenced in the published pages ships.
Original client media remains in the repo as a backup but unused originals are excluded from deployment.
"""
from pathlib import Path
import re
import shutil
import sys
ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
style=(ROOT/'styles.css').read_text(encoding='utf-8')
inline='<style id="site-css">\n'+style+'\n</style>'
if DIST.exists():shutil.rmtree(DIST)
DIST.mkdir()
allpages=[]
for name in ('index.html','about.html'):
    source=(ROOT/name).read_text(encoding='utf-8')
    if '<style id="site-css">' in source:
        output=re.sub(r'<style id="site-css">.*?</style>',lambda _:inline,source,count=1,flags=re.DOTALL)
    elif '<link rel="stylesheet" href="styles.css">' in source:
        output=source.replace('<link rel="stylesheet" href="styles.css">',inline)
    else:sys.exit('Expected main CSS for '+name)
    (DIST/name).write_text(output,encoding='utf-8')
    allpages.append(output)
for name in ('script.js','motion.js','robots.txt','sitemap.xml'):
    shutil.copy2(ROOT/name,DIST/name)
(DIST/'assets').mkdir()
names=set()
for page in allpages:
    names.update(re.findall(r'assets/([A-Za-z0-9._-]+)',page))
for name in sorted(names):
    asset=ROOT/'assets'/name
    if not asset.is_file():sys.exit('Missing asset '+str(asset))
    shutil.copy2(asset,DIST/'assets'/name)
print('Published',len(allpages),'pages and',len(names),'used media files; inlined CSS',len(style.encode()),'bytes.')
print('Dist bytes:',sum(p.stat().st_size for p in DIST.rglob('*') if p.is_file()))
