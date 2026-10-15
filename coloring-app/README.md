# Saudi Colors

A coloring book for kids (iPad first, iPhone too) built around the cities and cultures of Saudi Arabia: 9 regions, 8 scenes each, with Fill, Freestyle and Paint-by-Number modes. Ad-supported.

- `CLAUDE.md` — how the code is organised and how to build/test.
- `docs/CONTENT_PLAN.md` — the 72 scenes.
- `docs/MONETIZATION.md` — ads and App Store Kids Category constraints.
- `docs/ROADMAP.md` — milestones to a first App Store release.
- `docs/TESTFLIGHT.md` — how builds reach TestFlight, and the one-time App Store Connect setup.

Quick start: `brew install xcodegen && xcodegen generate && open SaudiColoring.xcodeproj`.

## Screenshots

Taken on an iPad simulator by `.github/workflows/screenshots.yml` (the `Screenshots` scheme, with demo progress). It runs on demand (Actions > App screenshots > Run workflow, on the branch you want) and pushes fresh PNGs to the branch `screenshots/<that branch>`.

| | |
|---|---|
| ![Home](docs/screenshots/01-home.png) | ![Najran pages](docs/screenshots/02-gallery.png) |
| ![Fill](docs/screenshots/03-fill.png) | ![Paint](docs/screenshots/04-paint.png) |
| ![Numbers](docs/screenshots/05-numbers.png) | ![You did it!](docs/screenshots/06-finished.png) |
| ![Ask a grown-up](docs/screenshots/07-parental-gate.png) | |
