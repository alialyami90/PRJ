---
name: Saudi Colors
description: A coloring book of the Kingdom, framed as one journey (Rihla) across nine Saudi regions.
colors:
  palm-green: "#11563F"
  rail-green: "#0B3A2C"
  rail-selected: "#17604A"
  date-gold: "#E2A63B"
  date-gold-dark: "#E8B04B"
  sage-ground: "#EDF2EC"
  sage-ground-dark: "#0F1A15"
  palm-ink: "#13261E"
  palm-ink-dark: "#EDF2EC"
  palm-ink-wash: "#13261E14"
  on-gold: "#1E1513"
  sadu-red: "#9E2B25"
  sadu-wool: "#F3EADF"
  sadu-black: "#1E1513"
  sadu-gold: "#D9A13A"
  white: "#FFFFFF"
typography:
  display:
    fontFamily: "SF Pro Rounded, system-ui, sans-serif"
    fontSize: "50px"
    fontWeight: 800
    lineHeight: 1
  display-arabic:
    fontFamily: "SF Pro Rounded, system-ui, sans-serif"
    fontSize: "41px"
    fontWeight: 700
    lineHeight: 1
  celebration:
    fontFamily: "SF Pro Rounded, system-ui, sans-serif"
    fontSize: "46px"
    fontWeight: 800
    lineHeight: 1
  headline:
    fontFamily: "SF Pro Rounded, system-ui, sans-serif"
    fontSize: "22px"
    fontWeight: 700
  title:
    fontFamily: "SF Pro Rounded, system-ui, sans-serif"
    fontSize: "20px"
    fontWeight: 800
  title-mode:
    fontFamily: "SF Pro Rounded, system-ui, sans-serif"
    fontSize: "20px"
    fontWeight: 700
  card-title:
    fontFamily: "SF Pro Rounded, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 600
  body-strong:
    fontFamily: "SF Pro Text, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 600
  label:
    fontFamily: "SF Pro Text, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 600
rounded:
  cover: "14px"
  page: "16px"
  card: "18px"
  rail-row: "22px"
  dialog: "34px"
  full: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  row: "14px"
  lg: "22px"
  gutter: "28px"
  grid-row: "32px"
  xl: "36px"
  target: "60px"
components:
  journey-rail:
    backgroundColor: "{colors.rail-green}"
    textColor: "{colors.white}"
    width: "350px"
  rail-stop-row-selected:
    backgroundColor: "{colors.rail-selected}"
    textColor: "{colors.white}"
    rounded: "{rounded.rail-row}"
    padding: "13px 14px 13px 0"
  route-stop:
    backgroundColor: "{colors.date-gold}"
    textColor: "{colors.on-gold}"
    rounded: "{rounded.full}"
    size: "24px"
  route-stop-selected:
    backgroundColor: "{colors.date-gold}"
    textColor: "{colors.on-gold}"
    rounded: "{rounded.full}"
    size: "30px"
  region-cover:
    rounded: "{rounded.cover}"
    width: "100px"
    height: "75px"
  header-band:
    backgroundColor: "{colors.palm-green}"
    textColor: "{colors.white}"
    typography: "{typography.display}"
    padding: "8px 28px 22px"
  sadu-band:
    backgroundColor: "{colors.sadu-red}"
    height: "30px"
  sadu-band-tray:
    backgroundColor: "{colors.sadu-red}"
    height: "12px"
  scene-card:
    backgroundColor: "{colors.white}"
    textColor: "{colors.palm-ink}"
    typography: "{typography.card-title}"
    rounded: "{rounded.card}"
  finished-seal:
    backgroundColor: "{colors.palm-green}"
    textColor: "{colors.palm-green}"
    rounded: "{rounded.full}"
    size: "60px"
  finished-seal-celebration:
    backgroundColor: "{colors.palm-green}"
    rounded: "{rounded.full}"
    size: "118px"
  mode-switch:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.full}"
    padding: "5px"
    width: "720px"
  mode-switch-segment:
    textColor: "{colors.palm-ink}"
    typography: "{typography.title-mode}"
    rounded: "{rounded.full}"
    height: "56px"
  mode-switch-segment-selected:
    backgroundColor: "{colors.palm-green}"
    textColor: "{colors.white}"
    typography: "{typography.title-mode}"
    rounded: "{rounded.full}"
    height: "56px"
  color-swatch:
    rounded: "{rounded.full}"
    size: "{spacing.target}"
  brush-size-option-selected:
    backgroundColor: "{colors.sage-ground}"
    rounded: "{rounded.page}"
    size: "{spacing.target}"
  celebration-card:
    backgroundColor: "{colors.sage-ground}"
    textColor: "{colors.palm-ink}"
    rounded: "{rounded.dialog}"
    width: "760px"
  button-green:
    backgroundColor: "{colors.palm-green}"
    textColor: "{colors.white}"
    typography: "{typography.headline}"
    rounded: "{rounded.full}"
    height: "64px"
  button-quiet:
    backgroundColor: "{colors.palm-ink-wash}"
    textColor: "{colors.palm-ink}"
    typography: "{typography.headline}"
    rounded: "{rounded.full}"
    height: "64px"
  hint-bubble:
    backgroundColor: "{colors.palm-green}"
    textColor: "{colors.white}"
    typography: "{typography.headline}"
    rounded: "{rounded.full}"
    padding: "12px 22px"
---

# Design System: Saudi Colors

## Overview

**Creative North Star: "Rihla, one caravan route across the Kingdom"**

Saudi Colors is a trip with nine stops. The whole app speaks one Saudi design language, chosen by the owner for every region alike: a deep palm green shell, a dotted date-gold caravan route with gold stops, and a calm sage-white ground behind the pages. Regions do not get their own palettes or ornaments. Their character lives in their pictures and their names, in English and Arabic; the chrome around them stays the same so that moving from Najd to Jazan feels like travel through one country, not a jump between apps.

The system has exactly one ornament: a strip of Al-Sadu weaving (red ground, black teeth, a chain of cream and gold diamonds), drawn in code so it stays sharp at any size. It sits where a woven edge would sit: along the bottom of every green header, along the top of the colour tray, along the top of the celebration card, and as a thin selvedge on each region cover in the rail. Progress is told without reading: eight diamonds per region, gold stops that earn a star when a region is complete, and a green seal with a gold stitched ring pressed onto each finished page.

This is a native iPadOS / iOS 17+ SwiftUI app, iPad-first in landscape, used by children aged 4 to 9 who often cannot read. Density is low and targets are large (60pt minimum). Every child control pairs an SF Symbol with a short label. Display type is SF Rounded at heavy weight; everything else uses the system text styles so Dynamic Type and Arabic shaping come for free. The illustrated scene is always the hero: chrome frames it, the tray sits on plain paper so paint reads true, and nothing decorative is laid over the artwork. Grown-up surfaces (the parental gate) deliberately stay in the stock system sheet style, quiet and separate from play.

**Key Characteristics:**
- One unified Saudi look for all nine regions; variety comes from the scene art.
- Deep green rail with a dotted gold route and gold stops (the journey).
- Palm green header bands on a sage-white ground.
- One ornament only: the Al-Sadu woven band.
- Green seal with a gold stitched ring for finished pages.
- SF Rounded heavy for display, system text styles elsewhere.
- 60pt minimum child targets, icon plus label, RTL safe, Reduce Motion honoured on the large moves.

## Colors

A two-green shell with one warm gold, set on a pale sage ground, plus the fixed four colours of the Sadu weave.

### Primary
- **Palm Green** (palm-green): the header band behind each region's name, the navigation bar on the gallery and canvas, the selected mode segment, the "Keep coloring" button, the hint bubble, and the body of the finished seal. White text sits on it at 8.65:1. It is the same value in light and dark appearance (see The One Green Bar Rule).
- **Deep Rail Green** (rail-green): the journey rail and its navigation bar, a step darker than the headers so the rail reads as the land the route crosses. Same value in both appearances. Also the app-wide control tint.
- **Selected Stop Green** (rail-selected): the rounded trailing pill behind the selected region row on the rail. White text 7.48:1.

### Secondary
- **Date Gold** (date-gold, dark appearance date-gold-dark): the dotted caravan route, the route stops, and the stitched ring of the seal. Dark ink (on-gold) sits on it at 8.32:1 (9.17:1 in dark). Gold on the rail green is 5.89:1.

### Tertiary
- **Sadu Red** (sadu-red), **Sadu Wool** (sadu-wool), **Sadu Black** (sadu-black), **Sadu Gold** (sadu-gold): the weave's own colours, used only inside the Sadu band and the app icon's band. They do not change with dark mode.

### Neutral
- **Sage Ground** (sage-ground, dark appearance sage-ground-dark): the gallery background behind the page cards, the canvas background around the page, the celebration card body, and the selected brush-size tile.
- **Palm Ink** (palm-ink, dark appearance palm-ink-dark): text and lines on the sage ground: scene titles, unselected mode labels, "You did it!", and the card outline (at 80%). 13.99:1 on sage.
- **Ink Wash** (palm-ink-wash, palm ink at 8%): the quiet "More pictures" button.
- **On Gold** (on-gold): text and the star on gold.
- **White** (white): text on every green, the scene card paper, the seal's inner disc and outer ring, the stop's ring. The colour tray and the mode switch track use the system background (white in light, black in dark) so paint colours read true.
- Secondary text on green uses white at reduced opacity: 72% on the rail (7.35:1), 82% for the area name and 90% for the "done" count on the header (6.43:1 and 7.35:1).

### Named Rules
**The One Saudi Look Rule.** Every region uses the same palette and the same ornament. Never introduce a per-region colour, header tint or pattern; a region's identity comes from its scene art and its names.

**The One Green Bar Rule.** Palm green and rail green carry the same value in light and dark appearance on purpose. Their navigation bars are forced into the dark appearance (`toolbarColorScheme(.dark)`), so a separate dark-mode value would make the bar and the header band below it two different greens. Only the ground, the ink and the gold shift for dark mode.

**The Paper Tray Rule.** Anything the child picks paint from (colour tray, brush sizes) sits on plain system background, never on green or sage, so the swatches look like the paint they will lay down.

## Typography

**Display Font:** SF Pro Rounded (the system rounded design), heavy and bold weights
**Body Font:** SF Pro, through the system text styles (title, title3, headline, subheadline)
**Label/Mono Font:** none

**Character:** A soft, friendly, chunky rounded face for everything a child looks at as a sign (region names, mode names, the celebration), on top of the plain platform styles that carry Dynamic Type and Arabic script without extra work.

### Hierarchy
- **Display** (800, 50pt scaled with largeTitle, minimum scale 0.6, one line): the region's name in the app's language on the header band. The name in the other language (Arabic in an English app, English in an Arabic one) sits trailing at 0.82 of that size, weight 700 (display-arabic), minimum scale 0.5.
- **Celebration** (800, 46pt on iPad, 36pt on iPhone, minimum scale 0.6): "You did it!" on the celebration card.
- **Headline** (700, title2, rounded): celebration buttons.
- **Title** (800, title3, rounded): region names on the rail. The mode switch labels use title3 at 700 (title-mode), minimum scale 0.7.
- **Card title** (600, headline, rounded): scene titles under the cards (two lines reserved) and the "More colors" lock button.
- **Body strong** (600, title3 or headline, standard design): the area name under the header title and the "N of 8 done" count.
- **Label** (600, subheadline): the rail subtitle "Najd · الرياض".

### Named Rules
**The Rounded Is For Children Rule.** SF Rounded is used for text a child reads as a sign or a button. Text that grown-ups read (the parental gate, system dialogs) stays in the standard design.

**The Text Style Rule.** Outside the display sizes, use system text styles (`.title2`, `.title3`, `.headline`, `.subheadline`) with a weight, never fixed point sizes, so Dynamic Type works. The region display size is a `@ScaledMetric` tied to largeTitle.

## Layout

iPad landscape first. The root is a `NavigationSplitView`: the journey rail is the leading sidebar column (minimum 300pt, ideal 350pt, maximum 420pt) and the selected region's gallery is the detail column with its own `NavigationStack`, which pushes the canvas. On iPhone the rail comes first and a region opens over it.

- **Rail:** each stop row is a 48pt route column (the dotted line plus the stop bead) followed by a 100 by 75pt cover with its Sadu strip, then the name, subtitle and diamonds, with 14pt between cover and text and 13pt vertical padding. The route line is hidden above the first stop and below the last. The rail scrolls to keep the selected stop in view. When the area and the other-language name do not fit on one line, they go on two lines rather than wrapping mid-phrase.
- **Gallery:** the header band spans the width with 28pt side padding; the Sadu band (30pt) hangs below it. The page grid is adaptive with a 240pt minimum column, 28pt column gap, 32pt row gap, 28pt side and top padding and 40pt bottom padding. An ad banner, when available, sits in a 50pt bottom safe-area inset on the bar material, never over the canvas.
- **Canvas:** a vertical stack of the controls (12pt vertical padding), the page filling the remaining space, and the tray (Sadu strip, then a horizontal scroller of swatches). On iPad the controls are the mode switch (max width 640pt) with the page actions beside it; on iPhone the page actions sit under the switch, the switch puts each icon above its word, and in Paint the brush sizes take their own row above the colours.
- **Celebration:** a card anchored to the bottom of the canvas with no scrim, so the finished picture stays in full view above it. On iPad (max 760pt) the 118pt seal sits leading, with the title over two buttons side by side; on iPhone the 84pt seal sits beside the title over two stacked buttons. A 16pt Sadu band runs along its top edge. It slides up from the bottom (a fade with Reduce Motion), and any new paint on the page puts it away like Keep coloring.
- **Spacing rhythm:** 4 / 8 / 12 / 14 / 22 / 28 / 32 / 36pt, with 28pt as the gallery gutter. Every child target is at least 60pt (swatches, brush sizes, the lock button) or 56pt tall inside a 66pt mode track; celebration buttons are 64pt.
- **RTL:** layout uses leading and trailing only; the selected rail row's rounded corners are declared as trailing radii, so the whole shell mirrors for Arabic.

## Elevation & Depth

Mostly flat colour fields (rail, header, ground) with soft, low shadows reserved for the things a child touches or earns: the page, the cards, the stops, the seal and the celebration card. Shadows are tinted with ink or black at low opacity and always fall downward. Depth between the rail, the header and the ground comes from tone (deep green, palm green, sage), not from shadow. The Sadu band and the header band themselves carry no shadow.

### Shadow Vocabulary
- **Page lift** (black 15%, blur radius 12, y 6): the coloring page on the canvas.
- **Card lift** (palm ink 16%, radius 10, y 6): each scene card in the gallery.
- **Segment glow** (palm green 35%, radius 6, y 3): the selected mode capsule.
- **Bead** (black 25%, radius 3, y 2): each route stop.
- **Seal** (black 22%, radius 8% of size, y 4% of size): the finished seal.
- **Dialog** (black 25%, radius 30, y 14): the celebration card.

### Named Rules
**The Earned Lift Rule.** Only touchable or earned objects cast shadows. Bands, rails, trays and the ground stay flat.

## Shapes

Generous continuous-curve (squircle) corners on everything that holds content, and full capsules on everything that is a button or a segmented choice. Corners step up with the size of the object: 14pt region cover, 16pt page and brush tile, 18pt scene card, 22pt selected rail pill (trailing corners only, square against the leading edge as if it grows out of the route), 34pt celebration card. Circles are reserved for meaning: colour swatches, route stops and the seal. Progress is drawn as small diamonds (squares turned 45 degrees), echoing the diamonds in the Sadu weave. Scene cards carry a 2.5pt ink outline at 80% that rhymes with the illustrator's bold black line; covers carry a 1pt white hairline at 25% that becomes 3pt solid white when selected. The Sadu band is the only angular, patterned form: straight edges, triangular teeth, diamond chain.

## Components

### Buttons
Big, rounded and unmistakable: every child button is an SF Symbol plus a short label on a full capsule.
- **Shape:** full capsule ({rounded.full}).
- **Green (Keep coloring):** palm green fill, white text, 64pt.
- **Quiet (More pictures):** ink wash fill, palm ink text, 64pt.
- **Press:** scales to 0.96 with a 0.15s ease out. Gallery cards press to 0.96 with a bouncy 0.25s spring; rail rows press to 0.97.
- **Page actions:** Undo, Redo and Start again as 76 by 60pt buttons, icon above a bold caption word, on a white rounded rectangle (18pt corners) with a hairline ink outline. At 40% opacity and disabled when there is nothing to do. Start again confirms with a system destructive dialog.

### Chips (if used)
- **Mode switch:** a white system-background capsule track (5pt padding, 1pt ink hairline at 12%) holding Fill and Paint with their symbols. The selected segment is a palm green capsule with white text that slides between options (matched geometry, 0.3s spring); with Reduce Motion it jumps without animation.
- **More colors (locked):** headline rounded label with a lock symbol on a capsule of primary at 8% with a 1.5pt primary outline at 20%, 60pt minimum.

### Cards / Containers
- **Scene card:** white paper at 4:3, 18pt continuous corners, 2.5pt palm ink outline at 80%, card lift shadow; title below in rounded headline, two lines reserved. A finished page wears the seal (60pt) on its top trailing corner, turned -12 degrees and hanging off the edge.
- **Celebration card:** sage ground, 34pt corners, dialog shadow, at the foot of the canvas (see Layout). Exactly two choices, Keep coloring and More pictures; nothing on it sells or unlocks anything, and More pictures goes straight back to the gallery with no ad.
- **Header band:** palm green, white text, the region's name in both languages on one line, then the progress diamonds (18pt) and "N of 8 done"; the 30pt Sadu band hangs from its bottom edge.

### Inputs / Fields
- **Colour swatch:** a 60pt circle of the paint with a 2pt black hairline at 25%. Selected: grows to 1.1 and gains a 5pt primary ring 8pt outside the circle. Order: the scene's suggested colours, a divider, the 13-crayon box, a divider, then the bonus colours or the lock button.
- **Number swatch:** the same 60pt circle with its number in title2 bold, digits dark on light paint and light on dark (luminance threshold 150). A finished number shows a checkmark and fades to 50% unless selected.
- **Brush size:** three 60pt tiles showing a dot of the current colour at 12, 22 and 36pt; the selected tile fills sage ground with a 2.5pt palm green outline and 16pt corners.

### Navigation
- **Journey rail:** deep rail green column under a dark navigation bar titled "Saudi Colors". Each region is a stop on a 4pt dotted gold route (round caps, dash 1 on 10). The stretch between two regions that both have finished pages is drawn as a solid 5pt gold line, road already travelled. A stop is a hollow rail-green bead with a white ring until a page is finished; then it fills with a gold wedge in proportion to the pages finished, like a clock face, behind a gold ring, and turns solid gold with a star when all eight are done. The selected row gets the rail-selected trailing pill, a bigger stop (32pt instead of 26pt) with an outer white ring, and a solid white cover outline. Region name in rounded title heavy, subtitle "area · name in the other language" at 72% white ("Najd · الرياض" in English, "نجد · Riyadh" in Arabic), then eight 14pt diamonds whose empty outlines are 60% white (above 3:1 on the rail).
- **Gallery and canvas bars:** palm green, forced dark appearance; the gallery bar shows no title because the header band below carries the name.

### Al-Sadu Band (signature)
A horizontally repeating strip drawn with `Canvas`: sadu red ground, cream selvedge lines on both edges (9% of height, minimum 1.5pt), black teeth pointing in from each edge (tooth width 22% of height), and a centre chain of diamonds alternating wool and gold, each with a black eye. Height sets the scale: 10pt on rail covers, 12pt on the tray, 30pt under headers, 16pt on the celebration card. Hidden from VoiceOver. Its colours never change with appearance.

### Route Stop and Progress Diamonds (signature)
A stop is a date gold bead with a 3pt white ring and the bead shadow; once every page in the region is finished it carries a star in on-gold. Progress diamonds are one per page, filled for each finished page and outlined when not; white on green surfaces (empty at 35% on the rail, 45% on the header). VoiceOver reads "N of 8 pictures finished".

### Finished Seal (signature)
A palm green disc, a dashed gold stitched ring inset 9%, a white inner disc inset 22% holding a black-weight star in palm green, and a white outer ring. On the celebration it drops in from 1.9 scale at -30 degrees to 1.0 at -10 degrees with a 0.45s bouncy spring after 0.15s and a success haptic; with Reduce Motion it fades in over 0.2s without the scale drop.

### Finishing Hint
When a child pauses for 5 seconds with at least 70% of the page coloured but not yet finished, the 8 biggest shapes that are still mostly white glow date gold over the page: a soft pulse (opacity 0 to 0.7, twice, 2.4s, ease in and out), repeated up to three times 8 seconds apart. Any touch that changes the page clears it and starts the wait again. With Reduce Motion it is one calm fade in and out instead of a pulse. It is drawn only inside those shapes, never over the line art or the colour already laid down, so the picture stays the hero.

A page is finished when at most 10% of its colourable area is still white and no single white patch is larger than 1.5% of it (`Engine/PageProgress.swift`). Fill and Paint use the same rule; brush paint counts pixel by pixel. The seal, once earned, stays: Undo, Redo and Start again never remove it, and "You did it!" plays at most once per visit.

### App Icon
Generated by `Scripts/make_app_icon.py`: a date palm on a white page disc, half coloured and half still line art, on palm green, over a full-width Sadu band using the same proportions as `SaduBand`. Opaque and square; iOS rounds the corners.

### Parental Gate
Intentionally the stock system look: a large-detent sheet, standard design type, a sum of a two-digit and a one-digit number (12 to 19 times 3 to 9) answered on a bordered system number pad with Delete and a prominent OK, the typed answer in a quaternary field, a shake on a wrong answer (none with Reduce Motion), a new sum after each miss, and the sheet closing itself after three misses. A "Not now" button closes it. The pad always reads left to right. It is grown-up territory and stays visually apart from the Rihla world.

## Do's and Don'ts

### Do:
- **Do** use palm green for every header band and its navigation bar, and rail green for the rail, with the same values in light and dark appearance.
- **Do** put the Al-Sadu band only at a woven edge: header bottoms (30pt), the tray top (12pt), the celebration card (16pt) and rail covers (10pt).
- **Do** show progress with shapes a pre-reader can count: eight diamonds per region, a starred gold stop, and the green seal on finished pages.
- **Do** pair every child control with an SF Symbol and a short label, and keep child targets at 60pt or more.
- **Do** use SF Rounded heavy for display and child-facing labels, and system text styles with a weight everywhere else.
- **Do** keep paint pickers on plain system background so colours read true.
- **Do** use leading and trailing (never left and right) and check every screen in Arabic RTL.
- **Do** gate the large motion (mode slide, seal drop) on Reduce Motion.

### Don't:
- **Don't** give a region its own palette, header colour or ornament; the variety lives in the pages.
- **Don't** add a second ornament or scatter Sadu pattern as a background texture.
- **Don't** lay chrome, gradients or decoration over the scene art; the child's picture is the hero.
- **Don't** give the green bars a separate dark-mode value; the bar and the header below it would split into two greens.
- **Don't** recolour the Sadu band for dark mode or for a region; its colours are the weave's own.
- **Don't** style the parental gate in the Rihla look; grown-up screens stay in the system sheet style.
- **Don't** use text-only buttons in child-facing UI.
- **Don't** use em-dashes in any user-facing copy.

### Open items (build state, not system rules)
These are visible in the build today. They are recorded so future work closes them, not so they spread.
- Small springs are not gated on Reduce Motion: the swatch select scale, the route stop size change, and the press scales on cards and buttons. The two large moves (mode slide, seal drop) are gated.
- Dark appearance: palm green on the dark sage ground is about 2.1:1. It matters only where green is a line or icon on the ground (the selected brush tile outline, the placeholder icon for a missing thumbnail).
- The parental gate is the stock system sheet on purpose; its person icon and number pad take the app tint (rail green) from the environment.
