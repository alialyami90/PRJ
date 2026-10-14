# Content

Source of truth for scene art. One folder per region, one per scene. A scene folder holds either the illustrator's `art/line.png` + `art/color.png` (final art, imported with `Scripts/import_illustration.py`) or a placeholder `scene.py` sketch (built with `Scripts/scene_kit.py` and the region's `_figures.py`), plus the files they generate:

- `outline.png` (imported art) or `outline.svg` (sketches) — black line art, 2048×1536 artboard (4:3, landscape, iPad-friendly).
- `regions.png` — same size; every fillable area a unique flat RGB colour, outline pixels pure black `#000000`, no anti-aliasing.
- `palette.json` — paint-by-number key (see `CLAUDE.md` → Scene asset contract).
- `preview.png` — 1024×768 coloured-in preview for review.

Rebuild with `python3 Scripts/build_scenes.py` (all), `python3 Scripts/import_illustration.py Content/Regions/<region>/<scene>` (one imported scene) or `python3 Content/Regions/<region>/<scene>/scene.py` (one sketch). Keep the illustrator's layered source files (.ai/.psd/.procreate) outside the repo.

Illustrator file rules (from the brief): pure black lines on white, outer lines about 14 px and inner 7 to 9 px, every shape closed, no colorable shape under about 40×40 px, 25 to 90 shapes, at most 18 flat colours, no gradients.

Each region folder also holds `cover.png` (1024×768 colour cover, shown in the app's region list).

Update `status` in `region.json` as a scene progresses; `Scripts/sync_scenes.py` ships `vectorized` and `approved` scenes into the app (`--approved-only` for a release build).

Art direction: bold outlines, friendly faces, no small details a 4-year-old's finger can't hit. Avoid text inside the drawing (it would need translating).
