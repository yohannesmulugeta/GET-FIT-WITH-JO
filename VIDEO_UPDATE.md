# Josi video update — completed locally

15 videos with sound were compressed; 11 distinct videos were added to the local gallery. Four alternate edits remain compressed and are disabled in videos.json. The two silent exports were excluded.

## Compression

- Full-quality inputs: 841.8 MB
- All compressed clips: 132.9 MB
- Reduction: 84.2%
- Active gallery videos: 98.7 MB
- H.264 MP4, 720 × 1280 portrait or 1280 × 720 landscape, 30 fps, AAC stereo audio at 128 kbps.
- Original sound and full durations retained; MP4 metadata placed first for fast startup.
- WebP covers generated from the clips.

## Gallery behavior

The old Shorts presentation has been replaced by a coaching video gallery. A featured landscape film has a separate introduction; portrait videos use clean cards, prominent Play buttons, duration labels and sound indicators. The first four videos are visible, with View all 11 videos expanding the rest. Playing a clip pauses the others; collapsing the gallery pauses hidden clips. Native video controls and all eleven videos remain available without JavaScript. The old video stills in Gallery and Results have also been replaced with frames from the new footage.

## Selection

For four repeated scenes, the more recent export was enabled; alternate edits remain available by changing enabled to true in videos.json. Original files in D:\capcut files and the full-quality collected copies are unchanged.

| Source export | Compressed MB | Gallery |
| --- | ---: | --- |
| 01-josi-website-2.mp4 | 10.19 | Included |
| 02-josi-social-media-7-1.mp4 | 7.77 | Included |
| 03-josi-social-media-9-1.mp4 | 10.50 | Included |
| 04-josi-social-media-1-1.mp4 | 8.33 | Alternate; disabled |
| 05-josi-social-media-1-1-1.mp4 | 8.41 | Included |
| 06-josi-social-media-10-1.mp4 | 7.55 | Included |
| 07-josi-social-media-11-1.mp4 | 10.55 | Alternate; disabled |
| 08-josi-social-media-11-1.mp4 | 9.83 | Included |
| 10-josi-social-media-2-1.mp4 | 6.77 | Included |
| 11-josi-social-media-3-1-1.mp4 | 7.58 | Included |
| 12-josi-social-media-3-1.mp4 | 7.59 | Alternate; disabled |
| 13-josi-social-media-4-1.mp4 | 7.93 | Included |
| 14-josi-social-media-5-1.mp4 | 14.59 | Included |
| 15-josi-social-media-6-1-1.mp4 | 7.62 | Included |
| 16-josi-social-media-6-1.mp4 | 7.68 | Alternate; disabled |

## Verification

- All 15 compressed clips fully decoded with both video and audio; audible signal detected in each.
- Duration matched the corresponding source within 0.15 seconds.
- Fast-start MP4 layout checked in each file.
- 65/65 site checks and 6/6 video/build tests passed; both browser scripts passed syntax checks.
- Production build contains all 11 configured videos and covers, excludes disabled alternates, and serves HTTP 200 locally.
- Browser QA at desktop width 1280 and mobile width 390: featured playback reached readyState 4 and advanced in time, with muted=false. Playing the row clip paused the feature. Expansion displayed 11 cards; collapse restored four and stopped hidden playback. Mobile content fitted the viewport without horizontal overflow; the browser reported no console errors. The temporary viewport override was reset.

## Publication

The local source and dist/ build are ready. GitHub and the live site have not been modified.
