"""Prepare website copies of Josi's exports; originals are never modified.

Run: python compress_josi_videos.py --ffmpeg /path/to/ffmpeg
Requires Pillow for WebP covers. Compression results are recorded for repeatable runs.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import json
import re
import shutil
import subprocess

from PIL import Image

ROOT = Path(__file__).resolve().parent
INBOX = ROOT / 'video-inbox/josi'
OUTPUT = ROOT / 'assets/videos'
REPORT = INBOX / 'compression-report.json'

# Names reflect the visible exercise, without inferring spoken coaching advice.
DETAILS = {
    '01': ('Training with JO', 'COACHING'),
    '02': ('Guided strength training', 'COACHING'),
    '03': ('Kettlebell technique', 'TECHNIQUE'),
    '04': ('Shoulder press coaching', 'STRENGTH'),
    '05': ('Shoulder press coaching', 'STRENGTH'),
    '06': ('A moment with JO', 'MEET JO'),
    '07': ('Floor exercise coaching', 'COACHING'),
    '08': ('Floor exercise coaching', 'COACHING'),
    '10': ('On the gym floor with JO', 'MEET JO'),
    '11': ('Barbell technique with JO', 'TECHNIQUE'),
    '12': ('Barbell technique with JO', 'TECHNIQUE'),
    '13': ('Bench press coaching', 'STRENGTH'),
    '14': ('Barbell curl coaching', 'STRENGTH'),
    '15': ('Bent-over row coaching', 'TECHNIQUE'),
    '16': ('Bent-over row coaching', 'TECHNIQUE'),
}
ALTERNATE_GROUPS = [('04', '05'), ('07', '08'), ('11', '12'), ('15', '16')]


def run(ffmpeg, args):
    result = subprocess.run([ffmpeg, '-hide_banner', '-nostdin', *args],
                            capture_output=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError(result.stderr[-2500:])
    return result.stdout, result.stderr


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ffmpeg', default=shutil.which('ffmpeg'))
    parser.add_argument('--jobs', type=int, default=2)
    args = parser.parse_args()
    if not args.ffmpeg:
        parser.error('Supply --ffmpeg with the path to FFmpeg')
    inventory = json.loads((INBOX / 'inventory.json').read_text(encoding='utf-8'))
    config_path = ROOT / 'videos.json'
    edited = {item['id']: item for item in json.loads(config_path.read_text(encoding='utf-8'))} if config_path.exists() else {}
    selected = [entry for entry in inventory if entry['audible_signal_detected']]
    by_id = {entry['file'][:2]: entry for entry in selected}
    alternates = set()
    for group in ALTERNATE_GROUPS:
        present = [key for key in group if key in by_id]
        latest = max(present, key=lambda key: (INBOX / by_id[key]['file']).stat().st_mtime)
        alternates.update(key for key in present if key != latest)

    encoders, _ = run(args.ffmpeg, ['-encoders'])
    encoder = 'libx264' if 'libx264' in encoders else 'h264_mf'
    OUTPUT.mkdir(parents=True, exist_ok=True)
    previous = {entry['source_file']: entry for entry in json.loads(REPORT.read_text(encoding='utf-8'))} if REPORT.exists() else {}
    settings = {'version': 1, 'encoder': encoder, 'video_kbps': 1800, 'audio_kbps': 128, 'fps': 30}

    def prepare(entry):
        source = INBOX / entry['file']
        stem = Path(entry['file']).stem
        target = OUTPUT / (stem + '.mp4')
        poster = OUTPUT / (stem + '.webp')
        old = previous.get(entry['file'])
        if (old and old.get('settings') == settings and old.get('source_sha256') == entry['sha256']
                and target.is_file() and target.stat().st_size == old['output_bytes'] and poster.is_file()):
            result = old.copy()
        else:
            width, height = entry['resolution']
            dimensions = '1280:720' if width > height else '720:1280'
            partial = OUTPUT / (stem + '.partial.mp4')
            codec_args = ['-preset', 'medium', '-crf', '24', '-maxrate', '2400k', '-bufsize', '4800k'] if encoder == 'libx264' else ['-b:v', '1800k', '-rate_control', 'u_vbr']
            run(args.ffmpeg, ['-v', 'warning', '-y', '-i', str(source),
                '-map', '0:v:0', '-map', '0:a:0', '-map_metadata', '-1', '-map_chapters', '-1',
                '-vf', 'scale=' + dimensions + ',setsar=1', '-r', '30', '-c:v', encoder,
                *codec_args, '-pix_fmt', 'yuv420p', '-g', '60', '-c:a', 'aac', '-b:a', '128k',
                '-ac', '2', '-ar', '44100', '-movflags', '+faststart', str(partial)])
            partial.replace(target)
            # JPEG is an intermediate only; Pillow supplies the WebP encoder.
            still = OUTPUT / (stem + '.poster-temp.jpg')
            run(args.ffmpeg, ['-v', 'error', '-y', '-ss', '3', '-i', str(target), '-frames:v', '1', '-q:v', '2', str(still)])
            with Image.open(still) as image:
                image.thumbnail((960, 768))
                image.save(poster, format='WEBP', quality=82, method=6)
            still.unlink()
            # Decode the complete compressed clip, checking video and audio together.
            _, check = run(args.ffmpeg, ['-v', 'info', '-i', str(target), '-map', '0:v:0', '-map', '0:a:0',
                '-af', 'volumedetect', '-f', 'null', 'NUL' if __import__('os').name == 'nt' else '/dev/null'])
            peak = re.search(r'max_volume: ([-\w.]+) dB', check)
            duration = re.search(r'Duration: (\d+:\d+:\d+\.\d+)', check)
            if not peak or float(peak[1]) <= -60 or 'Audio: aac' not in check or 'Video: h264' not in check:
                raise RuntimeError('Expected audible AAC and H.264 video: ' + target.name)
            data = target.read_bytes()
            if not 0 < data.find(b'moov') < data.find(b'mdat'):
                raise RuntimeError('Fast-start MP4 validation failed: ' + target.name)
            result = {'source_file': entry['file'], 'source_sha256': entry['sha256'],
                'source_bytes': entry['bytes'], 'src': target.relative_to(ROOT).as_posix(),
                'poster': poster.relative_to(ROOT).as_posix(), 'output_bytes': target.stat().st_size,
                'duration': duration[1] if duration else None, 'peak_db': peak[1],
                'decoded_successfully': True, 'fast_start': True, 'audio_preserved': True, 'settings': settings}
        result['enabled'] = entry['file'][:2] not in alternates
        result['format'] = 'landscape' if entry['resolution'][0] > entry['resolution'][1] else 'portrait'
        return result

    results = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        tasks = {pool.submit(prepare, entry): entry for entry in selected}
        for task in as_completed(tasks):
            result = task.result()
            results.append(result)
            results.sort(key=lambda item: item['source_file'])
            REPORT.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
            print(f"Ready {result['source_file']}: {result['output_bytes']/1000000:.1f} MB, sound verified", flush=True)

    videos = []
    for result in results:
        title, category = DETAILS[result['source_file'][:2]]
        item = {'id': Path(result['src']).stem, 'src': result['src'], 'poster': result['poster'],
            'title': title, 'category': category, 'description': title + ' with original audio',
            'format': result['format'], 'enabled': result['enabled']}
        h, m, s = result['duration'].split(':')
        seconds = int(int(h)*3600 + int(m)*60 + float(s) + .5)
        item['duration'] = f'{seconds//60}:{seconds%60:02d}'
        for field in ('title', 'category', 'description', 'summary', 'enabled'):
            if field in edited.get(item['id'], {}):
                item[field] = edited[item['id']][field]
        videos.append(item)
    (ROOT / 'videos.json').write_text(json.dumps(videos, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'compressed': len(results), 'gallery_videos': sum(item['enabled'] for item in results),
        'source_mb': round(sum(item['source_bytes'] for item in results)/1000000, 1),
        'compressed_mb': round(sum(item['output_bytes'] for item in results)/1000000, 1)}, indent=2), flush=True)


if __name__ == '__main__':
    main()
