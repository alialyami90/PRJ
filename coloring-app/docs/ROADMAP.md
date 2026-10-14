# Roadmap

## M1 — Playable prototype (1 region, 2 scenes)
- [ ] XcodeGen project builds on iPad simulator (CI: `.github/workflows/coloring-app.yml`)
- [ ] Region/scene gallery
- [x] Fill mode working on the region-map engine (renderer, colour tray, outline-tolerant taps)
- [ ] Freestyle brush with undo
- [x] Save/restore a coloring document

## M2 — Full modes + content pipeline
- [ ] Paint-by-Number overlay and correctness check
- [ ] `Scripts/sync_scenes.py` + `validate_content.py` in use
- [ ] Arabic localization, RTL check
- [x] 9 regions × 8 scenes with real art imported (see docs/CONTENT_PLAN.md, docs/ART_REVIEW.md)
- [ ] Fix the pages flagged in docs/ART_REVIEW.md, then mark scenes `approved`

## M3 — Ads + App Store
- [ ] AdService with a child-directed AdMob implementation (see docs/MONETIZATION.md)
- [ ] Parental gate
- [ ] Privacy nutrition label, Kids Category selection, age band 6–8
- [ ] Screenshots (iPad 13", iPad 11", iPhone 6.7") and App Store listing in en + ar
- [ ] TestFlight with a handful of families

## M4 — Measure
- [ ] Compare eCPM/fill across networks
- [ ] Decide on "Remove ads" IAP
