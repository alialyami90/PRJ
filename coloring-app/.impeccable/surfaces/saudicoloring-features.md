---
version: 1
slug: "saudicoloring-features"
primary_target: "SaudiColoring/Features"
related_targets: ["SaudiColoring/Features/Home","SaudiColoring/Features/RegionGallery","SaudiColoring/Features/Canvas"]
---

# App shell: home, region gallery, canvas chrome, celebration

Scope: every child-facing screen of Saudi Colors (iPad first, iPhone too). Mode: Operate. A child picks a region, picks a page, colours it. Grown-up screens (parental gate) stay quiet and neutral.

Constraints: native SwiftUI controls and navigation (NavigationSplitView, stack push, sheet); 60pt targets; icon plus label; RTL-safe; Dynamic Type for adult-read text; Reduce Motion honoured. Accessibility labels used by the screenshot UI test must keep their words (region names, scene titles, Fill / Paint / Numbers, You did it!, Get more colours, Ask a grown-up).

Decisions: owner chose one unified Saudi look for every region (no per-region palettes or ornaments). Open: Rihla route vs Al-Qatt room vs standard iOS; building Rihla meanwhile. Arabic app name undecided.

## Direction contract

THESIS: Rihla, a journey across the Kingdom. The app is a trip with nine stops along one caravan route, in one Saudi design language. Refuses the category default of a grey settings-style list of thumbnails with one accent.

OWN-WORLD: Palm green shell (rail a step darker than the headers), date-gold dotted caravan route and gold stops, sage-white ground behind the pages. One ornament: an Al-Sadu woven band (red ground, black teeth, cream and gold diamonds) along the bottom of every header, the top of the colour tray, and the celebration card. Finished pages get a green seal with a gold stitched ring. SF Rounded heavy for display, system text styles elsewhere.

STORY: The child sees where they are on the journey and how many pages each stop has finished, enters a region, colours, and a seal stamps the page when it is done.

FIRST VIEWPORT: iPad landscape. Leading: deep green rail, dotted gold route running down through nine gold stops (cover with a Sadu strip, name, area and Arabic name, eight progress diamonds). Trailing: green header band with the region's large name and Arabic name, progress diamonds, Sadu band along its bottom edge; under it a grid of page cards on the sage ground, finished ones carrying the seal.

FORM: Rihla route, position 4 on the ordered list (1 Al-Qatt room, 2 regional doorways, 3 Sadu loom, 4 Rihla route, 5 souq stalls, 6 khoos plait, 7 Gergean lanterns). Seed key 10e3fbea (degraded roll, no challengers). Signature move: the route with stops that fill as pages are finished; the seal pressing onto a finished page.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
