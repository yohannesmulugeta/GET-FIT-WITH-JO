# Replace Shorts or add videos

1. Put your MP4 videos and cover images in `assets/videos/`.
2. Edit `videos.json`. Change an existing entry to replace a Short, or duplicate an entry to add another video. Entries appear in the order listed.
3. Run `python video_gallery.py` to refresh the source preview, or `python build_site.py` to prepare the complete site in `dist/`.
4. Preview with `python -m http.server 8000`, then open `http://localhost:8000/#training`.

Example entry (add the actual files before enabling it):

```json
{
  "id": "my-new-short",
  "src": "assets/videos/my-new-short.mp4",
  "poster": "assets/videos/my-new-short.webp",
  "title": "Train with JO.",
  "category": "TRAINING",
  "description": "Describe what happens in this clip",
  "format": "portrait"
}
```

- Use `portrait` for 9:16 Shorts, `landscape` for 16:9 videos, or `square` for 1:1 clips. Videos fit inside the frame without cropping.
- Optional `duration` uses `m:ss` (for example `0:43`); `summary` adds a short description to a featured video.
- Use a unique `id` for each clip. Titles and categories are editable. Remove an entry to remove the card, or set `"enabled": false` to hide it.
- `poster` is optional. A matching cover image gives visitors something to see before pressing Play.
- MP4 with H.264 video and AAC audio is recommended for broad browser support. Export portrait Shorts at 720 × 1280 or 1080 × 1920 and compress them before adding them. Large original MOV files should be converted first.
- Videos start only when visitors press Play. Sound is available when present in the uploaded video; playing one clip pauses the others.
- Optional subtitles: add `"captions": "assets/videos/my-new-short.vtt"`, `"captionLanguage": "en"`, and `"captionLabel": "English"` to an entry. Supply a real WebVTT file.
- A complete HTTPS MP4/WebM URL also works for hosted clips. YouTube/Shorts page links are not direct video files.
- The build includes the configured local clips, posters and captions automatically and fails clearly if an enabled local file is missing.

## Current local checkout

Source retrieved from `yohannesmulugeta/GET-FIT-WITH-JO`, main commit `49619a63179c7fad2fa5485986554592699464dd` on 25 November 2026.

Direct Git/network access was blocked. The GitHub connection supplied 48 files, including images and archived small clips, but did not return the two video files larger than 1 MB. The two original cards initially used their existing GitHub Pages URLs. They have now been replaced by local compressed Josi footage: 11 enabled videos and four disabled alternate edits in `videos.json`. The gallery no longer depends on the remote video URLs. See `VIDEO_UPDATE.md` for compression results and validation. This is a source snapshot, not a complete Git clone with history.

The live site and remote GitHub repository have not been changed. The updated source and `dist/` production build are ready locally.
