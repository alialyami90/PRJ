# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Saudi Colors" — a kids' coloring book app for iPad (primary) and iPhone, native SwiftUI, iOS/iPadOS 17+. Content is 9 Saudi regions/cultures × 8 scenes each (72 scenes). Every scene is a full scene (place + people/animals + activity), never an isolated object. Three coloring modes on every scene: **Fill** (tap a region), **Freestyle** (finger/Pencil brush), **Paint by Number** (numbered regions with a suggested palette). Monetised with ads.

The Xcode project is generated, not committed: `project.yml` (XcodeGen) is the source of truth for targets and settings.

## Commands

```bash
brew install xcodegen                 # once
xcodegen generate                     # produces SaudiColoring.xcodeproj (git-ignored)
open SaudiColoring.xcodeproj

# Build / test from the CLI (iPad simulator is the default destination)
xcodebuild -project SaudiColoring.xcodeproj -scheme SaudiColoring \
  -destination 'platform=iOS Simulator,name=iPad Pro 13-inch (M4)' build
xcodebuild -project SaudiColoring.xcodeproj -scheme SaudiColoring \
  -destination 'platform=iOS Simulator,name=iPad Pro 13-inch (M4)' test

# Single test class / method
xcodebuild ... test -only-testing:SaudiColoringTests/FloodFillTests
xcodebuild ... test -only-testing:SaudiColoringTests/FloodFillTests/testFillStopsAtOutline

# Content checks (no Xcode needed)
python3 Scripts/validate_content.py   # 9 regions, every region.json has 8 scenes, asset paths exist for non-todo scenes
python3 Scripts/sync_scenes.py        # copies vectorized + approved scenes from Content/ into Resources/Scenes/ (needs Pillow)
python3 Scripts/sync_scenes.py --approved-only  # release builds: approved scenes only
python3 Scripts/build_scenes.py [region...]  # rebuilds every scene's art: illustrator art/ if present, else its scene.py sketch (needs Pillow + numpy)
python3 Scripts/import_illustration.py Content/Regions/<r>/<s>  # imports one scene's illustrator art/line.png + art/color.png
python3 Scripts/make_sample_scene.py  # regenerates the placeholder scene (Resources/SampleScene/) and placeholder AppIcon (needs Pillow)
swiftlint                             # if installed; config in .swiftlint.yml
```

Re-run `xcodegen generate` after adding or moving Swift files or resources; Xcode will not pick them up otherwise.

## Architecture

```
SaudiColoring/
  App/          entry point, root navigation, DI container (AppEnvironment)
  Models/       Region, Scene, Palette, ColoringDocument (pure value types, Codable)
  Engine/       the coloring engine — no SwiftUI here
  Features/     one folder per screen; each has a View + ViewModel (@Observable)
  Services/     Ads, Persistence, Analytics behind protocols; concrete impls injected by App/
  Resources/    Scenes/<region>/<scene>/, Assets, Localization (en + ar), Fonts, Sounds
Content/        source-of-truth scene art + region.json manifests (not shipped as-is)
docs/           content plan, monetization, App Store notes
Scripts/        content validation / sync
Tests/          unit tests; the Engine is the main thing worth testing
```

### Scene asset contract

Each scene ships three files, produced from the master art in `Content/`:

- `outline.png` (imported illustrator art) or `outline.svg` (placeholder sketches) — the black line art shown on top of everything.
- `regions.png` — an index map the same size as the outline where every fillable region is a unique flat colour (`regionId` = RGB packed to Int). The engine never flood-fills the rendered image; it looks up the region id at the touch point in this map. That makes Fill and Paint-by-Number O(1) per tap and leak-proof.
- `palette.json` — `[{ "regionId": 0xRRGGBB, "number": 3, "color": "#F4A62A" }]`, the paint-by-number answer key. Fill mode uses it only as a suggested palette.

Final scene art comes from an illustrator (brief: the "Saudi Colors Illustration Brief" doc). Per scene they deliver `art/line.png` (black lines on white) and `art/color.png` (same lines, every closed shape one flat colour), both 2048×1536, into `Content/Regions/<region>/<scene>/art/`. `Scripts/import_illustration.py` labels every closed white area of the line art as a region, takes its colour from the majority colour in `color.png` (ignoring the anti-aliased pixels next to lines), burns shapes under 1200 px and near-black fills into the outline, and writes `regions.png`, `palette.json`, `outline.png` (the line art, anti-aliasing kept) and `preview.png`. It warns, rather than fails, on gaps in the lines (a region holding two clearly different colours), more than 90 regions or more than 18 colours, so the page can go back to the illustrator. Edit the art, never the generated files.

Until a scene's art arrives it shows a placeholder sketch: its `scene.py` lists shapes in painter's order using `Scripts/scene_kit.py` (plus that region's own `_figures.py`) and writes `outline.svg`, `regions.png`, `palette.json` and `preview.png`. A scene with `art/` ignores its `scene.py`. `Scripts/build_scenes.py` rebuilds both kinds.

`Content/Regions/<region>/region.json` lists the 8 scenes, their titles (en/ar), an `era` (`traditional` | `modern`), a `character` (`type`: person in the region's own dress, or a local animal; plus a `description`), and production `status` (`todo` → `sketched` → `vectorized` → `approved`). A scene is `vectorized` once its real art is imported and `approved` once the owner has checked it in the app (see `docs/ART_REVIEW.md`). `Scripts/sync_scenes.py` copies `vectorized` and `approved` scenes into `Resources/Scenes/` (`--approved-only` for a release build): `regions.png`, `palette.json`, a 512×384 line-art `thumb.png` for the gallery, and each region's `cover.png`. The synced files are committed so any checkout builds with the real pages; CI fails if they drift from `Content/`.

### Engine (`Engine/`)

- `RegionMap` — loads `regions.png` into a `[UInt32]` buffer; `regionId(at:)`.
- `ColoringState` — `[regionId: Color]` for fill/PBN plus a `[Stroke]` list for freestyle, with an undo stack. Everything the user does is a `ColoringAction`; views never mutate state directly.
- `CanvasRenderer` — composites: fill layer (regions coloured via the map) → freestyle stroke layer → outline on top. The outline is drawn from the map's `0x000000` pixels, so `outline.svg` is not needed at runtime yet. Used by both the live canvas and the thumbnail/share export.
- `SceneAssets` — loads `regions.png` + `palette.json` for a scene from `Scenes/<region>/<scene>/` in the bundle, falling back to `SampleScene/` (generated placeholder art) so every scene is playable before its art is approved. Both folders are folder references in `project.yml`; anything else under `SaudiColoring/` is flattened into the bundle root.
- `CanvasGeometry` — aspect-fit mapping between screen points and image pixels. `RegionMap.regionId(near:radius:)` lets a tap that lands on an outline fill the nearest region.
- Modes are strategies over the same `ColoringState`: `FillTool`, `BrushTool`, `PaintByNumberTool`. PBN is Fill plus the overlay of numbers and a "correct colour" check.

Keep the engine free of SwiftUI/UIKit view types so it stays unit-testable; it may use CoreGraphics.

### Persistence

One `ColoringDocument` per (scene, user) saved as JSON in Application Support plus a cached PNG thumbnail. No accounts, no backend, nothing leaves the device except ad SDK traffic.

### Ads & the Kids Category (read before touching `Services/Ads`)

This app is for kids, so on the App Store it must go in the **Kids Category** and comply with App Review guideline 1.3 and 5.1.4: no behavioural/targeted ads, no third-party analytics or ad SDKs that collect identifying data, no IDFA, and a parental gate before anything that leaves the app (links, purchases, settings that affect ads). In practice that means contextual-only ads from a COPPA-compliant network (e.g. Google AdMob with `tagForChildDirectedTreatment` + `maxAdContentRating = G`, or a kids-specialist network like SuperAwesome/Kidoz), and the `AdService` protocol must stay swappable so the network can be changed without touching Features. Never show interstitials mid-stroke; ad slots are the home/gallery banner and an optional rewarded "unlock a new palette" after a scene is finished. Ad revenue reporting the user wants to measure comes from the network's dashboard, not in-app.

### Localization

Arabic is a first-class language: all strings go through `Localizable.xcstrings`, layout must be RTL-safe (use leading/trailing, never left/right), and region/scene names carry `nameAr`/`titleAr` in the manifests.

CI (`.github/workflows/coloring-app.yml`) runs the content checks on Linux and `xcodebuild test` on a macOS runner's iPad simulator for every PR that touches `coloring-app/`.

## Conventions

- iPad first: design layouts for regular width (sidebar + canvas), then adapt to compact. Test on iPad simulators before iPhone.
- Touch targets ≥ 60pt in kid-facing UI; no text-only buttons for children (icon + label).
- No em-dashes in user-facing copy; keep strings short, simple, and friendly for ages 4–9.
