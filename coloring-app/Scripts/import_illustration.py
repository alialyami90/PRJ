#!/usr/bin/env python3
"""Turn an illustrator's line art + flat colour PNGs into the scene asset contract.

    python3 Scripts/import_illustration.py Content/Regions/<region>/<scene> [...]

Reads <scene>/art/line.png (black lines on white) and <scene>/art/color.png (the same
lines with every shape filled one flat colour), both 2048x1536, and writes next to them:

- regions.png   every closed white area of the line art as one region, a unique RGB each;
                0xFFFFFF (paper: stays white, never coloured) for light shapes too small to tap and
                for eye highlights, 0x000000 for the lines and for dark shapes too small or filled black
                in color.png
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
MERGE_PX = 30          # a shape too small to tap joins a region of its own colour this close (a bit of leaf),
DARK_SMALL = 100       # ...or else is solid ink when darker than this (hair, shoes), paper white when lighter
                       # (teeth, the shine in an eye)
SAME_COLOUR = 12       # colours closer than this (sum of RGB differences) are one paint (export drift)
MIXED_SHARE = 0.15     # a second colour this big inside one region means a gap in the lines,
MIXED_PX = 4 * MIN_REGION_PX  # ...as does any second colour this many px (a gap into a huge sky)
PAPER = 0xFFFFFF       # regions.png id of white the child cannot colour (same value in RegionMap.swift)
SOLID_INK = 7          # ink at least 2x this thick is a solid black area (pupil, hair, mouth), not a line
HIGHLIGHT_GAP = 4      # a white gap up to 2x this wide running along solid black is a highlight
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
    """White gaps narrower than 2 * HIGHLIGHT_GAP px that run along solid black: the shine on a pupil,
    a strand of hair. The line art often leaves them open to the face, so they would take its colour."""
    solid = grow(shrink(ink, SOLID_INK), SOLID_INK + 6)  # within 6 px of black at least 15 px thick
    narrow = shrink(grow(ink, HIGHLIGHT_GAP), HIGHLIGHT_GAP)  # gaps closed by thickening the lines
    return solid & narrow & ~ink


def hexcolour(c):
    return "#%06X" % c


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

    burn, paper, small, keep = [], [], [], []
    for lab in range(1, n + 1):
        col = best[lab][0]
        r, g, b = col >> 16, col >> 8 & 0xFF, col & 0xFF
        if max(r, g, b) < DARK_FILL:
            burn.append(lab)
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

    # Shapes too small to tap: join the region of the same paint they sit next to, so they colour with it;
    # failing that, solid ink if dark and paper if light.
    by_label = np.argsort(flat, kind="stable")
    starts = np.searchsorted(flat[by_label], np.arange(n + 2))
    unmerged = 0
    for lab in small:
        px = by_label[starts[lab]:starts[lab + 1]]
        ys, xs = px // W, px % W
        y0, y1 = max(ys.min() - MERGE_PX, 0), min(ys.max() + MERGE_PX + 1, H)
        x0, x1 = max(xs.min() - MERGE_PX, 0), min(xs.max() + MERGE_PX + 1, W)
        window = labels[y0:y1, x0:x1]
        near = grow(window == lab, MERGE_PX)
        paint = paint_of(best[lab][0])
        cands, hits = np.unique(window[near], return_counts=True)
        same = [(h, c) for c, h in zip(cands.tolist(), hits.tolist()) if region_id[c] and colour_of[c] == paint]
        if same:
            target = max(same)[1]
            region_id[lab], colour_of[lab] = region_id[target], colour_of[target]
            continue
        col = best[lab][0]
        luma = 0.299 * (col >> 16) + 0.587 * (col >> 8 & 0xFF) + 0.114 * (col & 0xFF)
        (burn if luma < DARK_SMALL else paper).append(lab)
        unmerged += areas[lab] >= 50
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
