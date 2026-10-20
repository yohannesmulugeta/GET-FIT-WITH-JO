# Get Fit with JO — Training gallery and coaching journey

The website gallery uses existing JO media: two actual training video stills and two illustrative JO portraits already in the repository. The coaching journey uses two branded visual frames and intentionally makes no unsupported claims about specific clients or transformations.

## Reusable slots
| Section slot | Current source | Intended photography |
| --- | --- | --- |
| `gallery-01` | `assets/training-row-2026-poster.webp` | Strength training |
| `gallery-02` | `assets/training-floor-2026-poster.webp` | Movement technique |
| `gallery-03` | `assets/joseph-strength-fast.webp` | Strength or coaching portrait |
| `gallery-04` | `assets/joseph-outdoor-fast.webp` | Fitness and lifestyle |
| `progress-start`, `progress-forward` | CSS brand illustrations | Consented photos with verified context |

To change gallery imagery, edit the local image `src` and corresponding `alt`, `width`, and `height` attributes in `index.html`. Use optimized local WebP under `assets/`. The published build includes locally referenced files automatically. For client result pictures, obtain explicit permission before publication and avoid inventing outcomes.

Core brand palette, existing homepage portraits, programs, two training videos, FAQ and enquiry flows remain unchanged. Check the FormSubmit email activation with Joseph before relying on it.

Run `python3 test_site.py`, `node --check script.js`, and `python3 build_site.py` before deployment.