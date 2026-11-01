#!/usr/bin/env python3
"""Turn an illustrator's line art + flat colour PNGs into the scene asset contract.

    python3 Scripts/import_illustration.py Content/Regions/<region>/<scene> [...]

Reads <scene>/art/line.png (black lines on white) and <scene>/art/color.png (the same
lines with every shape filled one flat colour), both 2048x1536, and writes next to them:

- regions.png   every closed white area of the line art as one region, a unique RGB each (a shape
                closed but for a crack in the lines is closed; a shape big enough to see is never part
                of a neighbour across a line); 0xFFFFFF (paper: stays white, never coloured) for light
                shapes too small to see, for eye whites and for eye highlights, 0x000000 for the lines
                and for dark shapes too small or filled black in color.png
- palette.json  each region's colour = the most common colour inside it in color.png
- outline.png   the line art, with the 0x000000 shapes burned in black
- preview.png   1024x768 coloured preview

It also points the scene's `outline` asset in region.json at outline.png. A scene with
art/ is built from it; its scene.py (the placeholder sketch) is ignored. Needs Pillow + numpy.
Exits non-zero when a file is missing or the wrong size; rule breaks (gaps, tiny shapes,
too many regions or colours) are printed as WARN so the art can go back to the illustrator.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scene_kit import H, MAX_COLOURS, MAX_REGIONS, MIN_REGION_PX, W  # noqa: E402

INK_LEVEL = 128        # line art pixels darker than this are outline
DARK_FILL = 40         # a shape filled (near) black in color.png is drawn as solid ink
MERGE_PX = 30          # a shape too small to see joins a region of its own colour this close (a bit of leaf),
DARK_SMALL = 100       # ...or else is solid ink when darker than this (hair, shoes), paper white when lighter
                       # (teeth, the shine in an eye)
GAP_PX = 6             # a crack in the lines up to 2x this wide still closes a shape: two full-size shapes joined
                       # only through one are two regions (a tower's rungs, a sleeve and its cuff)
SAME_COLOUR = 12       # colours closer than this (sum of RGB differences) are one paint (export drift)
MIXED_SHARE = 0.15     # a second colour this big inside one region means a gap in the lines,
MIXED_PX = 4 * MIN_REGION_PX  # ...as does any second colour this many px (a gap into a huge sky)
PAPER = 0xFFFFFF       # regions.png id of white the child cannot colour (same value in RegionMap.swift)
SOLID_INK = 7          # ink at least 2x this thick is a solid black area (pupil, hair, mouth), not a line
HIGHLIGHT_GAP = 4      # a white gap up to 2x this wide cut into solid black is a highlight...
HIGHLIGHT_WALL = 0.75  # ...when this share of its walls is that solid black (the rest is its mouth, if open)
OWN_PX = 300           # a small shape at least this big and painted a clear colour is a region of its own, never
                       # part of a neighbour across a line (filling one window must not fill the next)
NEAR_WHITE = 235       # ...unless it is painted (near) white: then it stays paper (teeth, eye whites)
PUPIL_CORE = (150, 2500)  # a pupil: solid black whose core (SOLID_INK px in from its edge) is this many px,
PUPIL_FILL = (0.55, 0.88) # ...roughly oval (share of its bounding box; a window or block is ~1, a mouth or hair less)
PUPIL_ASPECT = 3.0        # ...and not long and thin
EYE_MAX_PX = 3 * MIN_REGION_PX  # an eye white is at most this big (a face, sky or wall is far bigger)
EYE_SHARE = 0.12       # a shape with this share of its pixels hugging a pupil may be the white of an eye: it never
                       # joins a neighbour (that is how a face swallowed its eyes), it stays a region of its own
EYE_EDGE = 0.45        # ...and when this share of its edge is the pupil it surely is one: always paper
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def label(free):
    """4-connected components of a bool image. Returns (labels, count); 0 = not free."""
    h, w = free.shape
    padded = np.zeros((h, w + 2), np.int8)
    padded[:, 1:-1] = free
    d = np.diff(padded, axis=1)
    ys, s = np.nonzero(d == 1)
    _, e = np.nonzero(d == -1)  # same row-major order as the starts
    parent = list(range(len(s)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    row_start = np.searchsorted(ys, np.arange(h + 1))
    for y in range(1, h):
        i, i_end = row_start[y - 1], row_start[y]
        j, j_end = row_start[y], row_start[y + 1]
        while i < i_end and j < j_end:
            if s[i] < e[j] and s[j] < e[i]:
                a, b = find(i), find(j)
                if a != b:
                    parent[max(a, b)] = min(a, b)
            if e[i] < e[j]:
                i += 1
            else:
                j += 1
    roots = {}
    labels = np.zeros((h, w), np.int32)
    for k in range(len(s)):
        r = roots.setdefault(find(k), len(roots) + 1)
        labels[ys[k], s[k]:e[k]] = r
    return labels, len(roots)


def shifted(a, dy, dx, fill):
    out = np.full_like(a, fill)
    h, w = a.shape
    out[max(dy, 0):h + min(dy, 0), max(dx, 0):w + min(dx, 0)] = a[max(-dy, 0):h + min(-dy, 0), max(-dx, 0):w + min(-dx, 0)]
    return out


def grow(mask, times):
    for _ in range(times):
        mask = mask | shifted(mask, 1, 0, False) | shifted(mask, -1, 0, False) | shifted(mask, 0, 1, False) | shifted(mask, 0, -1, False)
    return mask


def shrink(mask, times):
    for _ in range(times):
        mask = mask & shifted(mask, 1, 0, True) & shifted(mask, -1, 0, True) & shifted(mask, 0, 1, True) & shifted(mask, 0, -1, True)
    return mask


def highlights(ink):
    """White gaps narrower than 2 * HIGHLIGHT_GAP px cut into solid black: the shine on a pupil, a
    strand of hair. The line art often leaves them open to the face, so they would take its colour.
    Each gap is judged by its walls: a highlight is walled by the solid black itself (HIGHLIGHT_WALL of
    its edge, the rest being its mouth). A strip of face between an eye's outline and the edge of the
    face is as narrow and as close to the pupil, but its walls are lines, and it is face."""
    thick = grow(shrink(ink, SOLID_INK), SOLID_INK + 1)  # black at least 15 px thick, and its soft edge
    narrow = shrink(grow(ink, HIGHLIGHT_GAP), HIGHLIGHT_GAP) & ~ink  # gaps closed by thickening the lines
    gaps, count = label(narrow)
    if not count:
        return narrow
    wall = np.zeros(count + 1, np.int64)
    solid_wall = np.zeros(count + 1, np.int64)
    for dy, dx in DIRS:
        beside = shifted(gaps, dy, dx, 0)  # the gap, if any, on that side of each pixel
        edge = (gaps == 0) & (beside > 0)
        wall += np.bincount(beside[edge], minlength=count + 1)
        solid_wall += np.bincount(beside[edge & thick], minlength=count + 1)
    ok = solid_wall >= HIGHLIGHT_WALL * wall
    ok[0] = False
    return ok[gaps]


def split_at_gaps(labels, n):
    """Splits every shape that is two or more full-size shapes joined only through cracks in the lines
    narrower than 2 * GAP_PX px: a line that stops just short of another closes the shape to the eye,
    so it must close it to the fill too. The crack and the shape's thin parts go with the nearest piece.
    Returns (labels, count)."""
    flat = labels.ravel()
    areas = np.bincount(flat, minlength=n + 1)
    order = np.argsort(flat, kind="stable")
    starts = np.searchsorted(flat[order], np.arange(n + 2))
    w = labels.shape[1]
    for lab in np.nonzero(areas >= 2 * MIN_REGION_PX)[0]:
        if lab == 0:
            continue
        px = order[starts[lab]:starts[lab + 1]]
        ys, xs = px // w, px % w
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        window = labels[y0:y1, x0:x1]
        shape = window == lab
        pieces, count = label(shrink(shape, GAP_PX))
        sizes = np.bincount(pieces.ravel(), minlength=count + 1)
        big = [p for p in range(1, count + 1) if sizes[p] >= MIN_REGION_PX]
        if len(big) < 2:
            continue
        # Grow the pieces back, 1 px at a time, until every pixel of the shape belongs to one of them.
        piece_of = np.where(np.isin(pieces, big), pieces, 0)
        while True:
            left = shape & (piece_of == 0)
            if not left.any():
                break
            ly, lx = np.nonzero(left)
            sy, ey = max(ly.min() - 1, 0), min(ly.max() + 2, piece_of.shape[0])
            sx, ex = max(lx.min() - 1, 0), min(lx.max() + 2, piece_of.shape[1])
            part = piece_of[sy:ey, sx:ex]
            grown = part.copy()
            for dy, dx in DIRS:
                neighbour = shifted(part, dy, dx, 0)
                grown = np.where((grown == 0) & left[sy:ey, sx:ex], neighbour, grown)
            if (grown == part).all():
                break  # cannot happen for a connected shape; never loop forever on one
            piece_of[sy:ey, sx:ex] = grown
        for p in big[1:]:
            n += 1
            window[piece_of == p] = n
    return labels, n


def pupils(ink):
    """Pixels within a few px of a pupil: solid, roughly oval black of an eye's size. Eye whites hug one.
    The colour file (often carried over from older art) cannot be trusted to say which shapes are eye
    whites, so they are found from the lines."""
    core = shrink(ink, SOLID_INK)
    cl, cn = label(core)
    if not cn:
        return np.zeros_like(ink)
    ys, xs = np.nonzero(cl)
    k = cl[ys, xs]
    area = np.bincount(k, minlength=cn + 1)
    y0, y1 = np.full(cn + 1, 1 << 30), np.zeros(cn + 1, np.int64)
    x0, x1 = np.full(cn + 1, 1 << 30), np.zeros(cn + 1, np.int64)
    np.minimum.at(y0, k, ys); np.maximum.at(y1, k, ys)
    np.minimum.at(x0, k, xs); np.maximum.at(x1, k, xs)
    h, w = np.maximum(y1 - y0 + 1, 1), np.maximum(x1 - x0 + 1, 1)
    fill = area / (h * w)
    aspect = np.maximum(h, w) / np.minimum(h, w)
    ok = (area >= PUPIL_CORE[0]) & (area <= PUPIL_CORE[1]) & (fill >= PUPIL_FILL[0]) & (fill <= PUPIL_FILL[1]) & (aspect <= PUPIL_ASPECT)
    ok[0] = False
    return grow(ok[cl], SOLID_INK + 3)


def eye_whites(ink, labels, areas):
    """(sure, maybe): labels of shapes that are the white of an eye or the shine on a pupil, and of shapes
    that may be (a strap beside a black buckle looks much the same to this test)."""
    near = pupils(ink)
    hug = np.bincount(labels[near & ~ink], minlength=len(areas))
    edge = grow(ink, 2) & ~ink
    rim = np.maximum(np.bincount(labels[edge], minlength=len(areas)), 1)
    rim_hug = np.bincount(labels[edge & near], minlength=len(areas))
    maybe = (hug >= EYE_SHARE * areas) & (areas <= EYE_MAX_PX)
    maybe[0] = False
    sure = maybe & (rim_hug >= EYE_EDGE * rim)
    return set(np.nonzero(sure)[0].tolist()), set(np.nonzero(maybe & ~sure)[0].tolist())


def hexcolour(c):
    return "#%06X" % c


def is_region(rid):
    """True for a fillable region id in regions.png: not the outline, not paper."""
    return rid != 0 and rid != PAPER


def import_scene(scene_dir):
    scene_dir = Path(scene_dir).resolve()
    art = scene_dir / "art"
    line_img = Image.open(art / "line.png").convert("L")
    colour_img = Image.open(art / "color.png").convert("RGB")
    for name, im in (("line.png", line_img), ("color.png", colour_img)):
        if im.size != (W, H):
            sys.exit(f"{scene_dir.name}: art/{name} is {im.size[0]}x{im.size[1]}, expected {W}x{H}")

    line = np.asarray(line_img)
    rgb = np.asarray(colour_img).astype(np.int64)
    packed = rgb[..., 0] << 16 | rgb[..., 1] << 8 | rgb[..., 2]
    ink = line < INK_LEVEL
    # Frame so the canvas edge is an outline too.
    ink[:4, :] = ink[-4:, :] = True
    ink[:, :4] = ink[:, -4:] = True

    labels, n = label(~ink)
    labels, n = split_at_gaps(labels, n)
    flat = labels.ravel()
    areas = np.bincount(flat, minlength=n + 1)

    # Most common colour per region. Pixels within 3 px of a line are skipped: that is where
    # the artist's anti-aliasing blends neighbouring colours.
    near_line = ink.copy()
    for _ in range(3):
        grown = near_line.copy()
        grown[1:] |= near_line[:-1]
        grown[:-1] |= near_line[1:]
        grown[:, 1:] |= near_line[:, :-1]
        grown[:, :-1] |= near_line[:, 1:]
        near_line = grown
    core = (flat > 0) & ~near_line.ravel()
    pairs, counts = np.unique(flat[core].astype(np.int64) << 24 | packed.ravel()[core], return_counts=True)
    lab_of, col_of = (pairs >> 24).tolist(), (pairs & 0xFFFFFF).tolist()
    best = {}
    for lab, col, cnt in zip(lab_of, col_of, counts.tolist()):
        if lab not in best or cnt > best[lab][1]:
            best[lab] = (col, cnt)
    for lab in range(1, n + 1):  # a sliver that is all edge: use every pixel it has
        if lab not in best:
            vals, cnts = np.unique(packed.ravel()[flat == lab], return_counts=True)
            best[lab] = (int(vals[cnts.argmax()]), int(cnts.max()))
    # A clearly different second paint inside one region means a gap in the lines.
    second = {}
    for lab, col, cnt in zip(lab_of, col_of, counts.tolist()):
        b = best[lab][0]
        if sum(abs((b >> s & 0xFF) - (col >> s & 0xFF)) for s in (16, 8, 0)) >= 3 * SAME_COLOUR:
            second[lab] = second.get(lab, 0) + cnt

    problems = []
    first_px = {}
    nz = np.flatnonzero(flat)
    uniq, idx = np.unique(flat[nz], return_index=True)
    for lab, i in zip(uniq.tolist(), nz[idx].tolist()):
        first_px[lab] = divmod(i, W)

    # The white of an eye (and the shine on a pupil) stays paper whatever colour.png says, so filling a face
    # never paints the eyes. Without this a small eye white painted like the face joined the face below.
    eyes, maybe_eyes = eye_whites(ink, labels, areas)

    burn, paper, small, keep = [], [], [], []
    for lab in range(1, n + 1):
        col = best[lab][0]
        r, g, b = col >> 16, col >> 8 & 0xFF, col & 0xFF
        if max(r, g, b) < DARK_FILL:
            burn.append(lab)
            continue
        if lab in eyes:
            paper.append(lab)
            continue
        if areas[lab] < MIN_REGION_PX:
            small.append(lab)
            continue
        keep.append(lab)
        mixed = second.get(lab, 0)
        if mixed >= MIXED_PX or (mixed >= MIN_REGION_PX and mixed >= MIXED_SHARE * areas[lab]):
            y, x = first_px[lab]
            problems.append(f"gap? region from ({x},{y}) holds two colours")

    # One paint per group of near-identical colours; the biggest area names the group.
    by_area = {}
    for lab in keep:
        by_area[best[lab][0]] = by_area.get(best[lab][0], 0) + int(areas[lab])
    paints = []
    for col in sorted(by_area, key=by_area.get, reverse=True):
        c = np.array([col >> 16, col >> 8 & 0xFF, col & 0xFF])
        if not any(np.abs(c - p).sum() < SAME_COLOUR for p, _ in paints):
            paints.append((c, col))

    def paint_of(col):
        c = np.array([col >> 16, col >> 8 & 0xFF, col & 0xFF])
        return min(paints, key=lambda p: np.abs(c - p[0]).sum())[1]

    # Regions in reading order (top-left first) so ids are stable across re-imports.
    keep.sort(key=lambda lab: first_px[lab])
    region_id = np.zeros(n + 1, np.int64)
    colour_of = np.zeros(n + 1, np.int64)
    used = set()
    for i, lab in enumerate(keep, 1):
        rid = (i * 0x0F3A71) & 0xFFFFFF
        assert rid and rid != PAPER and rid not in used
        used.add(rid)
        region_id[lab] = rid
        colour_of[lab] = paint_of(best[lab][0])
    order = [col for _, col in paints]

    # Shapes too small to be full regions. Painted a clear colour and at least OWN_PX, a shape is a region of
    # its own: a tower's rungs or a row of windows are the same colour, and filling one must fill only one.
    # Smaller than that, or dark or near-white, it joins the region of the same paint it sits next to, so it
    # colours with it; failing that, it is solid ink if dark and paper if light.
    by_label = np.argsort(flat, kind="stable")
    starts = np.searchsorted(flat[by_label], np.arange(n + 2))
    unmerged = 0
    promoted = []
    for lab in small:
        px = by_label[starts[lab]:starts[lab + 1]]
        ys, xs = px // W, px % W
        y0, y1 = max(ys.min() - MERGE_PX, 0), min(ys.max() + MERGE_PX + 1, H)
        x0, x1 = max(xs.min() - MERGE_PX, 0), min(xs.max() + MERGE_PX + 1, W)
        window = labels[y0:y1, x0:x1]
        near = grow(window == lab, MERGE_PX)
        paint = paint_of(best[lab][0])
        col = best[lab][0]
        luma = 0.299 * (col >> 16) + 0.587 * (col >> 8 & 0xFF) + 0.114 * (col & 0xFF)
        if lab in maybe_eyes and luma >= DARK_SMALL:
            # Perhaps an eye white: never part of the face, even when painted like it.
            (promoted if areas[lab] >= OWN_PX else paper).append(lab)
            continue
        if areas[lab] >= OWN_PX and luma >= DARK_SMALL and min(col >> 16, col >> 8 & 0xFF, col & 0xFF) < NEAR_WHITE:
            promoted.append(lab)  # big enough to see and tap: its own region
            continue
        cands, hits = np.unique(window[near], return_counts=True)
        same = [(h, c) for c, h in zip(cands.tolist(), hits.tolist()) if region_id[c] and colour_of[c] == paint]
        if same:
            target = max(same)[1]
            region_id[lab], colour_of[lab] = region_id[target], colour_of[target]
            continue
        if luma >= DARK_SMALL and min(col >> 16, col >> 8 & 0xFF, col & 0xFF) < NEAR_WHITE and areas[lab] >= OWN_PX:
            promoted.append(lab)  # a small hand, fist or kite bow painted a real colour: keep it, small as it is
            continue
        (burn if luma < DARK_SMALL else paper).append(lab)
        unmerged += areas[lab] >= 50
    for i, lab in enumerate(promoted, len(keep) + 1):
        rid = (i * 0x0F3A71) & 0xFFFFFF
        assert rid and rid != PAPER and rid not in used
        used.add(rid)
        region_id[lab], colour_of[lab] = rid, paint_of(best[lab][0])
    keep += promoted
    if unmerged:
        problems.append(f"{unmerged} shape(s) under {MIN_REGION_PX}px drawn as solid ink or left white")

    palette = [{"regionId": int(region_id[lab]), "number": order.index(int(colour_of[lab])) + 1,
                "color": hexcolour(int(colour_of[lab]))} for lab in keep]

    if len(keep) > MAX_REGIONS:
        problems.append(f"{len(keep)} regions (max {MAX_REGIONS})")
    if len(order) > MAX_COLOURS:
        problems.append(f"{len(order)} distinct colours (max {MAX_COLOURS})")
    black = int((region_id[labels] == 0).sum())  # light small shapes still count here; they become paper below
    if black > W * H * 0.2:
        problems.append(f"{100 * black // (W * H)}% of the canvas is outline (very heavy lines?)")

    region_id[paper] = PAPER
    ids = region_id[labels]
    # Only in light shapes: next to black hair, a dark shape's narrow gaps are more of the same hair.
    rgb_of = np.stack([colour_of >> 16, colour_of >> 8 & 0xFF, colour_of & 0xFF], axis=-1)
    light = rgb_of @ np.array([0.299, 0.587, 0.114]) >= DARK_SMALL
    ids[highlights(ink) & (ids != 0) & light[labels]] = PAPER
    regions = np.stack([ids >> 16, ids >> 8 & 0xFF, ids & 0xFF], axis=-1).astype(np.uint8)
    Image.fromarray(regions, "RGB").save(scene_dir / "regions.png", optimize=True)
    outline = np.where(~ink & (ids == 0), 0, line).astype(np.uint8)  # keep the artist's anti-aliasing
    Image.fromarray(outline, "L").save(scene_dir / "outline.png", optimize=True)
    colour_of[paper] = PAPER
    col = np.where(ids == PAPER, PAPER, colour_of[labels])
    preview = np.stack([col >> 16, col >> 8 & 0xFF, col & 0xFF], axis=-1).astype(np.uint8)
    Image.fromarray(preview, "RGB").resize((1024, 768), Image.LANCZOS).save(scene_dir / "preview.png", optimize=True)
    (scene_dir / "palette.json").write_text(json.dumps(palette, indent=2) + "\n", encoding="utf-8")
    (scene_dir / "outline.svg").unlink(missing_ok=True)  # generated by the old sketch; outline.png replaces it

    manifest = scene_dir.parent / "region.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for s in data["scenes"]:
        if s["id"] == scene_dir.name:
            s["assets"]["outline"] = f"{scene_dir.name}/outline.png"
    manifest.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = f"{scene_dir.parent.name}/{scene_dir.name}: {len(keep)} regions, {len(order)} colours (imported)"
    print(summary + ("  WARN " + "; ".join(problems) if problems else ""))
    return problems


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for arg in sys.argv[1:]:
        import_scene(arg)
