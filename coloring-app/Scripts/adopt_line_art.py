#!/usr/bin/env python3
"""Swap a scene's line art for a redrawn version that has no colour file, keeping the scene's colours.

    python3 Scripts/adopt_line_art.py <new_line.png> Content/Regions/<region>/<scene>
    python3 Scripts/import_illustration.py Content/Regions/<region>/<scene>

The redraws trace the same composition as the scene's current art, so each closed shape of the new
line art takes the most common colour that the current art/color.png has under it (ignoring the old
lines). A frame drawn around the page is cropped off, so its line becomes the page edge, and the
result is scaled to 2048x1536. Writes art/line.png and art/color.png; check the preview after the
import, since a shape the redraw moved can pick up a neighbour's colour. Needs Pillow + numpy.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from import_illustration import DARK_FILL, INK_LEVEL, grow, label  # noqa: E402
from scene_kit import H, W  # noqa: E402

FRAME_SEARCH = 32  # a frame line this close to the page edge is cropped off
FRAME_FILL = 0.8   # share of a row or column that must be ink to count as the frame


def crop_frame(line):
    """Crop to the middle of a frame line drawn around the page, if there is one."""
    ink = np.asarray(line) < INK_LEVEL
    h, w = ink.shape

    def inset(profile):
        hits = np.flatnonzero(profile[:FRAME_SEARCH] > FRAME_FILL)
        return 0 if hits.size == 0 else (hits[0] + hits[-1]) // 2

    left, right = inset(ink.mean(0)), inset(ink.mean(0)[::-1])
    top, bottom = inset(ink.mean(1)), inset(ink.mean(1)[::-1])
    return line.crop((left, top, w - right, h - bottom))


def adopt(new_line, scene_dir):
    art = Path(scene_dir) / "art"
    old_rgb = np.asarray(Image.open(art / "color.png").convert("RGB")).astype(np.int64)
    old_line = np.asarray(Image.open(art / "line.png").convert("L"))
    old = (old_rgb[..., 0] << 16 | old_rgb[..., 1] << 8 | old_rgb[..., 2]).ravel()
    usable = (~grow(old_line < INK_LEVEL, 2) & (old_rgb.max(axis=2) >= DARK_FILL)).ravel()

    line = crop_frame(Image.open(new_line).convert("L")).resize((W, H), Image.LANCZOS)
    ink = np.asarray(line) < INK_LEVEL
    ink[:4, :] = ink[-4:, :] = True
    ink[:, :4] = ink[:, -4:] = True
    labels, n = label(~ink)
    flat = labels.ravel()

    colour = np.zeros(n + 1, np.int64)
    counted = np.zeros(n + 1, np.int64)
    m = (flat > 0) & usable
    pairs, counts = np.unique(flat[m].astype(np.int64) << 24 | old[m], return_counts=True)
    for lab, col, cnt in zip((pairs >> 24).tolist(), (pairs & 0xFFFFFF).tolist(), counts.tolist()):
        if cnt > counted[lab]:
            colour[lab], counted[lab] = col, cnt
    for lab in np.flatnonzero(counted[1:] == 0) + 1:  # only old lines under it: take what is there
        vals, cnts = np.unique(old[flat == lab], return_counts=True)
        colour[lab] = vals[cnts.argmax()]

    c = np.where(ink, 0, colour[labels])
    line.save(art / "line.png", optimize=True)
    rgb = np.stack([c >> 16, c >> 8 & 0xFF, c & 0xFF], axis=-1).astype(np.uint8)
    Image.fromarray(rgb, "RGB").save(art / "color.png", optimize=True)
    print(f"{Path(scene_dir).parent.name}/{Path(scene_dir).name}: {n} shapes coloured from the old art")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    adopt(sys.argv[1], sys.argv[2])
