"""Exercise editable video lists and the production asset copy path."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

from video_gallery import load_videos, render_videos, sync_gallery, START, END

ROOT = Path(__file__).resolve().parent


class VideoGalleryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'assets/videos').mkdir(parents=True)
        for name in ('new clip.mp4', 'cover.webp', 'captions.vtt'):
            (self.root / 'assets/videos' / name).write_bytes(b'test fixture')
        self.entries = [{
            'id': 'new-clip', 'src': 'assets/videos/new clip.mp4',
            'poster': 'assets/videos/cover.webp', 'captions': 'assets/videos/captions.vtt',
            'title': 'Strength & control <practice>', 'category': 'TRAINING',
            'format': 'landscape'
        }]
        (self.root / 'index.html').write_text(
            '<html><style id="site-css"></style><div class="video-grid">'
            + START + END + '</div></html>', encoding='utf-8')
        self.save()

    def save(self):
        (self.root / 'videos.json').write_text(json.dumps(self.entries), encoding='utf-8')

    def test_replace_add_reorder_and_hide(self):
        self.entries.append(dict(self.entries[0], id='second', title='Second'))
        self.entries.reverse()
        self.save()
        sync_gallery(self.root)
        page = (self.root / 'index.html').read_text(encoding='utf-8')
        self.assertLess(page.index('data-video-id="second"'), page.index('data-video-id="new-clip"'))
        self.entries[0]['enabled'] = False
        self.save()
        self.assertEqual(len(sync_gallery(self.root)), 1)
        self.entries = []
        self.save()
        sync_gallery(self.root)
        self.assertIn('More training videos coming soon.', (self.root / 'index.html').read_text())

    def test_missing_file_is_reported(self):
        self.entries[0]['src'] = 'assets/videos/missing.mp4'
        self.save()
        with self.assertRaisesRegex(ValueError, 'missing or empty'):
            load_videos(self.root)

    def test_unsafe_paths_and_duplicate_ids_are_rejected(self):
        for value in ('../clip.mp4', 'assets/../clip.mp4', 'javascript:clip.mp4', '//example.com/clip.mp4', 'assets/%2e%2e/clip.mp4'):
            self.entries[0]['src'] = value
            self.save()
            with self.assertRaises(ValueError, msg=value):
                load_videos(self.root)
        self.entries[0]['src'] = 'assets/videos/new clip.mp4'
        self.entries.append(dict(self.entries[0]))
        self.save()
        with self.assertRaisesRegex(ValueError, 'unique'):
            load_videos(self.root)

    def test_rendering_preserves_controls_captions_and_escapes_copy(self):
        html = render_videos(load_videos(self.root))
        self.assertIn('Strength &amp; control &lt;practice&gt;', html)
        self.assertIn('preload="none" playsinline controls', html)
        self.assertIn('kind="captions"', html)
        self.assertIn('data-video-format="landscape"', html)
        self.assertNotIn('autoplay', html)

    def test_build_copies_nested_media_and_excludes_unused_files(self):
        for name in ('build_site.py', 'video_gallery.py', 'styles.css', 'script.js', 'motion.js', 'robots.txt', 'sitemap.xml'):
            shutil.copy2(ROOT / name, self.root / name)
        (self.root / 'about.html').write_text('<html><style id="site-css"></style></html>')
        (self.root / 'assets/videos/unused.mp4').write_bytes(b'unused fixture')
        result = subprocess.run([sys.executable, str(self.root / 'build_site.py')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ('new clip.mp4', 'cover.webp', 'captions.vtt'):
            self.assertEqual((self.root / 'dist/assets/videos' / name).read_bytes(), b'test fixture')
        self.assertFalse((self.root / 'dist/assets/videos/unused.mp4').exists())
        self.assertIn('new clip.mp4', (self.root / 'dist/index.html').read_text(encoding='utf-8'))

    def test_https_video_without_cover_is_allowed(self):
        entry = self.entries[0]
        entry['src'] = 'https://example.com/clip.mp4'
        entry.pop('poster')
        entry.pop('captions')
        self.save()
        self.assertEqual(len(load_videos(self.root)), 1)
        self.assertNotIn('data-poster', render_videos(load_videos(self.root)))


if __name__ == '__main__':
    unittest.main()
