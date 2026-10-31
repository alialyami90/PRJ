---
version: 1
slug: "saudicoloring-features"
primary_target: "SaudiColoring/Features"
related_targets: ["SaudiColoring/Features/Home","SaudiColoring/Features/RegionGallery","SaudiColoring/Features/Canvas"]
---

# App shell: home, region gallery, canvas chrome, celebration

Scope: every child-facing screen of Saudi Colors (iPad first, iPhone too). Mode: Operate. A child picks a region, picks a page, colours it. Grown-up screens (parental gate) stay quiet and neutral.

Constraints: native SwiftUI controls and navigation (NavigationSplitView, stack push, sheet); 60pt targets; icon plus label; RTL-safe; Dynamic Type for adult-read text; Reduce Motion honoured. Accessibility labels used by the screenshot UI test must keep their words (region names, scene titles, Fill / Paint / Numbers, You did it!, Get more colours, Ask a grown-up).

Open decisions: user has two choice cards open (per-region looks vs unified; Rihla vs Al-Qatt vs standard). Building the recommended options meanwhile. Arabic app name undecided.

## Direction contract

THESIS: Rihla, a journey across the Kingdom. The app is a trip with nine stops, and every stop is dressed in its own region's design language. Refuses the category default of a grey settings-style list of thumbnails with one accent.

OWN-WORLD: Shell rail in deep palm green with a dashed date-gold caravan route. Each region owns a palette (ground, tint, accent, ink) and one ornament band from its own tradition: Najdi shurfa triangles (Riyadh), rawashin lattice (Jeddah), khoos palm plait (Al-Ahsa), Al-Qatt stripes and triangles (Asir), Nabataean crow-steps (AlUla), Hisma arches (Tabuk), sea scallops (Jazan), Sadu weave (Hail), Najrani basket diamonds (Najran). SF Rounded heavy for display, system text styles elsewhere.

STORY: The child sees where they are on the journey and how many pages each stop has finished, enters a region that looks like that place, colours, and stamps the stop when a page is done.

FIRST VIEWPORT: iPad landscape. Leading: green rail, route line running down through nine stops (coloured stop dot, cover, name, Arabic name, eight progress diamonds). Trailing: selected region's header band in its ground colour, large name and Arabic name, progress diamonds, ornament band along its bottom edge; under it a grid of page cards on the region tint, finished ones carrying the region's stamp.

FORM: Rihla route, position 4 on the ordered list (1 Al-Qatt room, 2 regional doorways, 3 Sadu loom, 4 Rihla route, 5 souq stalls, 6 khoos plait, 7 Gergean lanterns). Seed key 10e3fbea (degraded roll, no challengers). Signature move: the route with stops that fill as pages are finished; the region stamp pressing onto a finished page.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
