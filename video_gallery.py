"""Editable video gallery rendered as static HTML; no browser dependencies."""
from html import escape
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
import json
import re

ROOT = Path(__file__).resolve().parent
START = '<!-- VIDEO_GALLERY_START -->'
END = '<!-- VIDEO_GALLERY_END -->'
FORMATS = {'portrait', 'landscape', 'square'}


def local_media(value):
    """Return an assets-relative path, or None for an HTTPS media URL."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Media paths must be nonempty strings')
    url = urlsplit(value)
    if url.scheme == 'https' and url.netloc and not url.username and not url.password:
        return None
    media = PurePosixPath(value)
    if (url.scheme or url.netloc or url.query or url.fragment or '\\' in value
            or any(ord(c) < 32 for c in value) or '%' in value
            or media.parts[:1] != ('assets',) or '..' in media.parts):
        raise ValueError('Use a path inside assets/ or a complete HTTPS URL: ' + value)
    return Path(*media.parts)


def load_videos(root=ROOT):
    entries = json.loads((root / 'videos.json').read_text(encoding='utf-8'))
    if not isinstance(entries, list):
        raise ValueError('videos.json must contain a list')
    active, ids = [], set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Each video must be an object')
        video_id = entry.get('id', '')
        if not isinstance(video_id, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', video_id) or video_id in ids:
            raise ValueError('Each video needs a unique lowercase id with letters, numbers or hyphens')
        ids.add(video_id)
        if not isinstance(entry.get('enabled', True), bool):
            raise ValueError('enabled must be true or false')
        if not entry.get('enabled', True):
            continue
        for key in ('title', 'category'):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                raise ValueError(video_id + ': missing ' + key)
        if entry.get('format', 'portrait') not in FORMATS:
            raise ValueError(video_id + ': format must be portrait, landscape or square')
        if entry.get('duration') and (not isinstance(entry['duration'], str) or not re.fullmatch(r'\d+:[0-5]\d', entry['duration'])):
            raise ValueError(video_id + ': duration must use m:ss')
        if entry.get('summary') and not isinstance(entry['summary'], str):
            raise ValueError(video_id + ': summary must be text')
        if urlsplit(entry.get('src', '')).path.lower().split('.')[-1] not in ('mp4', 'webm'):
            raise ValueError(video_id + ': use an MP4 or WebM video')
        for key in ('src', 'poster', 'captions'):
            value = entry.get(key)
            if key != 'src' and not value:
                continue
            asset = local_media(value)
            if asset is not None:
                resolved = (root / asset).resolve()
                if not resolved.is_relative_to((root / 'assets').resolve()):
                    raise ValueError(video_id + ': media must stay inside assets/')
                if not resolved.is_file() or not resolved.stat().st_size:
                    raise ValueError(video_id + ': missing or empty ' + value)
        active.append(entry)
    return active


def render_videos(entries):
    cards = []
    for entry in entries:
        attr = lambda value: escape(str(value), quote=True)
        video_format = entry.get('format', 'portrait')
        poster = ' data-poster="' + attr(entry['poster']) + '"' if entry.get('poster') else ''
        mime = 'video/webm' if urlsplit(entry['src']).path.lower().endswith('.webm') else 'video/mp4'
        track = ''
        if entry.get('captions'):
            track = ('<track kind="captions" src="' + attr(entry['captions'])
                     + '" srclang="' + attr(entry.get('captionLanguage', 'en'))
                     + '" label="' + attr(entry.get('captionLabel', 'English')) + '">')
        duration = '<span class="video-duration">' + attr(entry['duration']) + '</span>' if entry.get('duration') else ''
        summary = '<p class="video-summary">' + attr(entry['summary']) + '</p>' if entry.get('summary') else ''
        hint = ('<p class="video-watch-note">Press Play to watch with sound.</p>'
                '<a class="video-consultation" href="#consultation">Book Consultation</a>') if video_format == 'landscape' else ''
        cards.append(
            '<article class="video-card" data-video-id="' + attr(entry['id'])
            + '" data-video-format="' + video_format + '"><div class="video-stage">'
            + '<video preload="none" playsinline controls' + poster + ' aria-label="'
            + attr(entry.get('description') or entry['title']) + '"><source src="'
            + attr(entry['src']) + '" type="' + mime + '">' + track
            + 'Your browser does not support video playback. <a href="' + attr(entry['src'])
            + '">Open video</a>.</video><span class="video-length">'
            + 'WITH SOUND</span>' + duration + '</div><div class="video-info"><span class="video-category">'
            + attr(entry['category']) + '</span><h3>' + attr(entry['title'])
            + '</h3>' + summary + hint + '</div></article>'
        )
    return '\n'.join(cards) if cards else '<p class="video-empty">More training videos coming soon.</p>'


def sync_gallery(root=ROOT):
    entries = load_videos(root)
    page = root / 'index.html'
    source = page.read_text(encoding='utf-8')
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError('Expected one marked video gallery in index.html')
    before, remaining = source.split(START, 1)
    _, after = remaining.split(END, 1)
    output = before + START + '\n' + render_videos(entries) + '\n' + END + after
    if output != source:
        page.write_text(output, encoding='utf-8')
    return entries


if __name__ == '__main__':
    print('Prepared', len(sync_gallery()), 'video cards from videos.json')
