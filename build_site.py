"""Build fast and complete static pages for GitHub Pages.
CSS is inlined into both source pages; only media referenced in the published pages ships.
Original client media remains in the repo as a backup but unused originals are excluded from deployment.
"""
from pathlib import Path
from html.parser import HTMLParser
import re
import shutil
import sys
from video_gallery import sync_gallery, local_media
ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
sync_gallery(ROOT)
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
class MediaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets=set()
    def handle_starttag(self, tag, attrs):
        for key,value in attrs:
            if key not in ('src','srcset','href','poster','data-poster') or not value:
                continue
            values=[part.strip().split()[0] for part in value.split(',')] if key=='srcset' else [value]
            for item in values:
                if item.startswith('assets/'):
                    self.assets.add(local_media(item))
media=MediaParser()
for page in allpages:media.feed(page)
names=media.assets
for name in sorted(names):
    asset=(ROOT/name).resolve()
    if not asset.is_relative_to((ROOT/'assets').resolve()) or not asset.is_file():
        sys.exit('Missing or invalid asset '+str(asset))
    target=DIST/name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(asset,target)
print('Published',len(allpages),'pages and',len(names),'used media files; inlined CSS',len(style.encode()),'bytes.')
print('Dist bytes:',sum(p.stat().st_size for p in DIST.rglob('*') if p.is_file()))
