#!/usr/bin/env python3
"""Turn an illustrator's line art + flat colour PNGs into the scene asset contract.

    python3 Scripts/import_illustration.py Content/Regions/<region>/<scene> [...]

Reads <scene>/art/line.png (black lines on white) and <scene>/art/color.png (the same
lines with every shape filled one flat colour), both 2048x1536, and writes next to them:

- regions.png   every closed white area of the line art as one region, a unique RGB each
- palette.json  each region's colour = the most common colour inside it in color.png
- outline.png   the line art, with the shapes too small to tap burned in black
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
SAME_COLOUR = 12       # colours closer than this (sum of RGB differences) are one paint (export drift)
MIXED_SHARE = 0.15     # a second colour this big inside one region means a gap in the lines,
MIXED_PX = 4 * MIN_REGION_PX  # ...as does any second colour this many px (a gap into a huge sky)


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

    burn, keep = [], []
    for lab in range(1, n + 1):
        col = best[lab][0]
        r, g, b = col >> 16, col >> 8 & 0xFF, col & 0xFF
        if areas[lab] < MIN_REGION_PX or max(r, g, b) < DARK_FILL:
            burn.append(lab)
            continue
        keep.append(lab)
        mixed = second.get(lab, 0)
        if mixed >= MIXED_PX or (mixed >= MIN_REGION_PX and mixed >= MIXED_SHARE * areas[lab]):
            y, x = first_px[lab]
            problems.append(f"gap? region from ({x},{y}) holds two colours")
    small = sum(1 for lab in burn if areas[lab] < MIN_REGION_PX and areas[lab] >= 50)
    if small:
        problems.append(f"{small} shape(s) under {MIN_REGION_PX}px drawn as solid ink")

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
        assert rid and rid not in used
        used.add(rid)
        region_id[lab] = rid
        colour_of[lab] = paint_of(best[lab][0])
    order = [col for _, col in paints]
    palette = [{"regionId": int(region_id[lab]), "number": order.index(int(colour_of[lab])) + 1,
                "color": hexcolour(int(colour_of[lab]))} for lab in keep]

    if len(keep) > MAX_REGIONS:
        problems.append(f"{len(keep)} regions (max {MAX_REGIONS})")
    if len(order) > MAX_COLOURS:
        problems.append(f"{len(order)} distinct colours (max {MAX_COLOURS})")
    black = int((region_id[labels] == 0).sum())
    if black > W * H * 0.2:
        problems.append(f"{100 * black // (W * H)}% of the canvas is outline (very heavy lines?)")

    ids = region_id[labels]
    regions = np.stack([ids >> 16, ids >> 8 & 0xFF, ids & 0xFF], axis=-1).astype(np.uint8)
    Image.fromarray(regions, "RGB").save(scene_dir / "regions.png", optimize=True)
    outline = np.where(~ink & (ids == 0), 0, line).astype(np.uint8)  # keep the artist's anti-aliasing
    Image.fromarray(outline, "L").save(scene_dir / "outline.png", optimize=True)
    col = colour_of[labels]
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
