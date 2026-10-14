# Content

Source of truth for scene art. One folder per region, one per scene. Each scene folder holds `scene.py` (the drawing, built with `Scripts/scene_kit.py` and the region's `_figures.py`) and the files it generates:

- `outline.svg` — black line art, 2048×1536 artboard (4:3, landscape, iPad-friendly).
- `regions.png` — same size; every fillable area a unique flat RGB colour, outline pixels pure black `#000000`, no anti-aliasing.
- `palette.json` — paint-by-number key (see `CLAUDE.md` → Scene asset contract).
- `preview.png` — 1024×768 coloured-in preview for review.

Rebuild with `python3 Scripts/build_scenes.py` (all) or `python3 Content/Regions/<region>/<scene>/scene.py` (one).

Update `status` in `region.json` as a scene progresses; only `approved` scenes get synced into the app by `Scripts/sync_scenes.py`.

Art direction: bold 6–8px outlines, 20–60 regions per scene, friendly faces, no small details a 4-year-old's finger can't hit. Avoid text inside the drawing (it would need translating).
