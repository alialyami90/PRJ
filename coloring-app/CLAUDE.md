# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Saudi Colors" — a kids' coloring book app for iPad (primary) and iPhone, native SwiftUI, iOS/iPadOS 17+. Content is 8 Saudi regions/cultures × 8 scenes each (64 scenes). Every scene is a full scene (place + people/animals + activity), never an isolated object. Two coloring modes on every scene: **Fill** (tap a region) and **Freestyle** (finger/Pencil brush, shown as "Paint"). Paint by Number was removed after TestFlight testing (October 2026); do not bring it back without the owner asking. Monetised with ads.

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

# Screenshots of the main screens with demo progress (Debug build launched with -demoContent)
TEST_RUNNER_SCREENSHOTS_DIR=$PWD/docs/screenshots xcodebuild -project SaudiColoring.xcodeproj -scheme Screenshots \
  -destination 'platform=iOS Simulator,name=iPad Pro 13-inch (M4)' test

# Content checks (no Xcode needed)
python3 Scripts/validate_content.py   # 8 regions, every region.json has 8 scenes, asset paths exist for non-todo scenes
python3 Scripts/test_import_illustration.py  # the importer's fill rules on synthetic pages (needs Pillow + numpy)
python3 Scripts/sync_scenes.py        # copies vectorized + approved scenes from Content/ into Resources/Scenes/ (needs Pillow)
python3 Scripts/sync_scenes.py --approved-only  # release builds: approved scenes only
python3 Scripts/build_scenes.py [region...]  # rebuilds every scene's art: illustrator art/ if present, else its scene.py sketch (needs Pillow + numpy)
python3 Scripts/import_illustration.py Content/Regions/<r>/<s>  # imports one scene's illustrator art/line.png + art/color.png
python3 Scripts/adopt_line_art.py <new_line.png> Content/Regions/<r>/<s>  # redrawn line art with no colour file: crops its frame, scales it, colours it from the old art/color.png (then import)
python3 Scripts/paint_shapes.py Content/Regions/<r>/<s>  # line art with no colour file and a new composition: colours every shape from art/paint.json into art/color.png (then import)
python3 Scripts/make_sample_scene.py  # regenerates the placeholder scene (Resources/SampleScene/) (needs Pillow)
python3 Scripts/make_app_icon.py      # draws the app icon: half-coloured palm over a Sadu band (needs Pillow)
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
- `regions.png` — an index map the same size as the outline where every fillable region is a unique flat colour (`regionId` = RGB packed to Int). `0x000000` is outline and `0xFFFFFF` is paper: white that is drawn but never filled (`RegionMap.paper`). The engine never flood-fills the rendered image; it looks up the region id at the touch point in this map. That makes Fill O(1) per tap and leak-proof, as long as `regions.png` is right: a leak on the page is always a fault in the map, never in the engine.
- `palette.json` — `[{ "regionId": 0xRRGGBB, "number": 3, "color": "#F4A62A" }]`, the colour each region is meant to be (`number` ranks the colours by use). Fill uses it only as the suggested row of the colour tray.

Final scene art comes from an illustrator (brief: the "Saudi Colors Illustration Brief" doc). Per scene they deliver `art/line.png` (black lines on white) and `art/color.png` (same lines, every closed shape one flat colour), both 2048×1536, into `Content/Regions/<region>/<scene>/art/`. `Scripts/import_illustration.py` labels every closed white area of the line art as a region, takes its colour from the majority colour in `color.png` (ignoring the anti-aliased pixels next to lines), and writes `regions.png`, `palette.json`, `outline.png` (the line art, anti-aliasing kept) and `preview.png`. Two shapes joined only through a crack in the lines (under 12 px) are two regions, each taking the crack's side nearest it (a tower's rungs, a sleeve and its cuff: closed to the eye, so closed to the fill). Shapes under 1200 px but at least 300 px and painted a clear colour are regions of their own, never merged across a line (filling one window used to fill the next); smaller, dark or near-white ones join a same-coloured region within 30 px, else become ink (dark) or paper (light); near-black fills become ink; narrow white gaps cut into solid black (the shine on a pupil, often open to the face) become paper when the solid black makes up most of their walls, so a thin strip of face between an eye's outline and the face's edge stays face (it used to be left white; fixed 1 Nov 2026). Eye whites are found from the lines, not from `color.png`: a shape hugging a pupil (solid, oval black of an eye's size) is paper when the pupil is a good share of its edge, else at least its own region; it never joins the face, whatever colour it was painted. (Carried-over colours painted many eye whites skin, and the small-shape merge then folded them into the face, so filling a face filled the eyes; fixed 31 Oct 2026.) It warns, rather than fails, on gaps in the lines (a region holding two clearly different colours), more than 90 regions or more than 18 colours, so the page can go back to the illustrator. Edit the art, never the generated files. Line art that arrives without a colour file is coloured either by `adopt_line_art.py` (a redraw of the same composition: colours carried over by position) or by `paint_shapes.py` (a new composition: `art/paint.json` lists zones and points with the colour each shape should be, chosen from what the picture shows; `"keep": true` corrects carried-over colours instead of starting blank). Either way `art/color.png` is the committed result the importer reads.

Until a scene's art arrives it shows a placeholder sketch: its `scene.py` lists shapes in painter's order using `Scripts/scene_kit.py` (plus that region's own `_figures.py`) and writes `outline.svg`, `regions.png`, `palette.json` and `preview.png`. A scene with `art/` ignores its `scene.py`. `Scripts/build_scenes.py` rebuilds both kinds.

`Content/Regions/<region>/region.json` lists the 8 scenes, their short titles (`title` and `titleAr`, at most 4 and 5 words, what the child sees on the card and the canvas), a longer `brief` describing the picture for the illustrator, an `era` (`traditional` | `modern`), a `character` (`type`: person in the region's own dress, or a local animal; plus a `description`), and production `status` (`todo` → `sketched` → `vectorized` → `approved`). A scene is `vectorized` once its real art is imported and `approved` once the owner has checked it in the app (see `docs/ART_REVIEW.md`). `Scripts/sync_scenes.py` copies `vectorized` and `approved` scenes into `Resources/Scenes/` (`--approved-only` for a release build): `regions.png`, `palette.json`, a 512×384 line-art `thumb.png` for the gallery, and each region's `cover.png`. The synced files are committed so any checkout builds with the real pages; CI fails if they drift from `Content/`.

### Engine (`Engine/`)

- `RegionMap` — loads `regions.png` into a `[UInt32]` buffer; `regionId(at:)`.
- `ColoringState` — `[regionId: Color]` for fill plus a `[Stroke]` list for freestyle, with an undo stack. Everything the user does is a `ColoringAction`; views never mutate state directly.
- `CanvasRenderer` — composites: fill layer (regions coloured via the map) → freestyle stroke layer → outline on top. The outline is drawn from the map's `0x000000` pixels, so `outline.svg` is not needed at runtime yet. Used by both the live canvas and the thumbnail/share export.
- `SceneAssets` — loads `regions.png` + `palette.json` for a scene from `Scenes/<region>/<scene>/` in the bundle, falling back to `SampleScene/` (generated placeholder art) so every scene is playable before its art is approved. Both folders are folder references in `project.yml`; anything else under `SaudiColoring/` is flattened into the bundle root.
- `CanvasGeometry` — aspect-fit mapping between screen points and image pixels. `RegionMap.regionId(near:radius:)` lets a tap that lands on an outline fill the nearest region.
- `CanvasRenderer.thumbnailPNG(of:)` makes the gallery thumbnail.
- `PageProgress` decides when a page is finished: at most 10% of the colourable area white and no single white patch over 1.5% of it, the same in Fill and Paint (`CanvasRenderer.renderPage` counts brush paint per region). Pages have 60 to 311 shapes, so requiring every sliver kept children from ever finishing. Its `whiteShapes` feed the gold finishing hint (`CanvasRenderer.highlight`). A page's finished mark is earned for good: undo, redo and Start again keep it.
- Modes are strategies over the same `ColoringState`: `FillTool`, `BrushTool`. A saved page whose mode this build does not know (e.g. the old `paintByNumber`) opens in Fill.

The canvas (`Features/Canvas/`) is `CanvasView` (modes, trays, "You did it!") over `PageView`, a `UIScrollView` whose zoomed content view is in image pixels, so touch points need no conversion. Pinch zooms in every mode; one finger pans in Fill and draws in Freestyle, where two fingers pan.

Keep the engine free of SwiftUI/UIKit view types so it stays unit-testable; it may use CoreGraphics.

### Persistence

One `ColoringDocument` per (scene, user) saved as JSON in Application Support plus a cached PNG thumbnail. No accounts, no backend, nothing leaves the device except ad SDK traffic.

### Ads & the Kids Category (read before touching `Services/Ads`)

This app is for kids, so on the App Store it must go in the **Kids Category** and comply with App Review guideline 1.3 and 5.1.4: no behavioural/targeted ads, no third-party analytics or ad SDKs that collect identifying data, no IDFA, and a parental gate before anything that leaves the app (links, purchases, settings that affect ads). In practice that means contextual-only ads from a COPPA-compliant network (e.g. Google AdMob with `tagForChildDirectedTreatment` + `maxAdContentRating = G`, or a kids-specialist network like SuperAwesome/Kidoz), and the `AdService` protocol must stay swappable so the network can be changed without touching Features. Never show interstitials mid-stroke; ad slots are the home/gallery banner, a capped interstitial as a new page opens (never straight after a finish), and an optional rewarded "unlock a new palette" behind the parental gate from the lock in the colour tray. The "You did it!" card sells nothing. Ad revenue reporting the user wants to measure comes from the network's dashboard, not in-app.

### Localization

Arabic is a first-class language: all strings go through `Localizable.xcstrings`, layout must be RTL-safe (use leading/trailing, never left/right), and region/scene names carry `nameAr`/`titleAr` in the manifests. The app picks a region or scene name by `AppLanguage.isArabic` (the first of the app's localizations the device prefers): in Arabic the Arabic name leads and the English one is the smaller second name, and the other way round in English.

CI (`.github/workflows/coloring-app.yml`) runs the content checks on Linux and `xcodebuild test` on a macOS runner's iPad simulator for every PR that touches `coloring-app/`.
`.github/workflows/testflight.yml` archives with Xcode 26 and uploads to TestFlight (cloud signing via an App Store Connect API key in repo secrets) on every push to `main` that touches the app, or on demand; setup in `docs/TESTFLIGHT.md`.

## Conventions

- iPad first: design layouts for regular width (sidebar + canvas), then adapt to compact. Test on iPad simulators before iPhone.
- Touch targets ≥ 60pt in kid-facing UI; no text-only buttons for children (icon + label).
- No em-dashes in user-facing copy; keep strings short, simple, and friendly for ages 4–9.
