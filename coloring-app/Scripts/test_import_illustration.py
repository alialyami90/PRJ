#!/usr/bin/env python3
"""Tests for import_illustration.py on small synthetic pages.

    python3 Scripts/test_import_illustration.py

Every case is a fill fault seen on a real page: a tap that coloured more than the shape under
the finger, or a shape that could not be coloured at all. Needs Pillow + numpy.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import import_illustration as imp  # noqa: E402
from scene_kit import H, W  # noqa: E402

LINE = 6          # line thickness in the synthetic art, like the illustrator's
SKIN = (245, 191, 137)
SKY = (120, 190, 240)


class Page:
    """A blank page to draw lines and paint shapes on, written as a scene's art/."""

    def __init__(self):
        self.ink = np.zeros((H, W), bool)
        self.colour = np.full((H, W, 3), 255, np.uint8)

    def line(self, x0, y0, x1, y1, thick=LINE):
        """An axis-aligned line, `thick` px wide, inclusive of both ends."""
        self.ink[min(y0, y1):max(y0, y1) + thick, min(x0, x1):max(x0, x1) + thick] = True

    def box(self, x0, y0, x1, y1):
        self.line(x0, y0, x1, y0); self.line(x0, y1, x1, y1)
        self.line(x0, y0, x0, y1); self.line(x1, y0, x1, y1)

    def solid(self, x0, y0, x1, y1):
        self.ink[y0:y1, x0:x1] = True

    def paint(self, x0, y0, x1, y1, rgb):
        self.colour[y0:y1, x0:x1] = rgb

    def write(self, root, region="test", scene="page"):
        scene_dir = Path(root) / region / scene
        (scene_dir / "art").mkdir(parents=True)
        Image.fromarray(np.where(self.ink, 0, 255).astype(np.uint8), "L").save(scene_dir / "art" / "line.png")
        Image.fromarray(self.colour, "RGB").save(scene_dir / "art" / "color.png")
        manifest = {"id": region, "scenes": [{"id": scene, "assets": {"outline": f"{scene}/outline.svg"}}]}
        (scene_dir.parent / "region.json").write_text(json.dumps(manifest))
        return scene_dir


def regions_png(scene_dir):
    rgb = np.asarray(Image.open(scene_dir / "regions.png").convert("RGB")).astype(np.int64)
    return rgb[..., 0] << 16 | rgb[..., 1] << 8 | rgb[..., 2]


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.page = Page()
        # A big sky so the page has one large region and the shapes under test are not the only ones.
        self.page.paint(0, 0, W, H, SKY)

    def tearDown(self):
        self.tmp.cleanup()

    def run_import(self):
        scene_dir = self.page.write(self.tmp.name)
        imp.import_scene(scene_dir)
        return regions_png(scene_dir)

    def test_small_closed_shapes_of_one_colour_stay_separate(self):
        # Two 24x24 cells (576 px: too small to be a full region, big enough to see) side by side,
        # painted the same, separated by a solid line: the rungs of a tower. One tap, one cell.
        p = self.page
        p.box(100, 100, 130, 130)
        p.box(130, 100, 160, 130)
        p.paint(100, 100, 166, 136, SKIN)
        ids = self.run_import()
        left, right = ids[115, 115], ids[115, 145]
        self.assertTrue(imp.is_region(left) and imp.is_region(right))
        self.assertNotEqual(left, right)

    def test_tiny_shape_joins_its_neighbour_of_the_same_colour(self):
        # A 10x10 speck (100 px) beside a big shape of the same paint colours with it: nobody can tap it.
        p = self.page
        p.box(100, 100, 300, 300)
        p.box(300, 100, 316, 116)
        p.paint(100, 100, 322, 306, SKIN)
        ids = self.run_import()
        self.assertEqual(ids[110, 310], ids[200, 200])

    def test_face_strip_beside_an_eye_is_not_a_highlight(self):
        # A face with an eye: an outlined oval, its solid pupil flush against the eye's outline on both
        # sides. Between the eye and the edge of the face runs a strip of face 8 px wide. The shine on
        # the pupil is a 6 px gap cut into it that opens leftwards into the face: a highlight, paper.
        p = self.page
        p.box(100, 100, 500, 500)                   # the face
        p.paint(100, 100, 506, 506, SKIN)
        p.box(300, 200, 400, 300)                   # the eye outline; the strip right of it is x 406..413
        p.line(414, 100, 414, 500)                  # the face edge, 8 px from the eye
        p.solid(306, 220, 400, 290)                 # the pupil, flush against the outline left and right
        p.ink[250:256, 300:360] = False             # the shine, through the outline into the pupil
        ids = self.run_import()
        face = ids[150, 150]
        self.assertTrue(imp.is_region(face))
        self.assertEqual(ids[250, 410], face, "the strip between the eye and the face edge is face")
        self.assertEqual(ids[150, 410], face)
        self.assertEqual(ids[253, 350], imp.PAPER, "the shine on the pupil stays white")
        self.assertEqual(ids[253, 320], imp.PAPER)

    def test_two_cells_joined_through_a_crack_in_the_line_are_two_regions(self):
        # Two 100x100 cells whose dividing line has a 6 px hole: closed to the eye, open to the labeller.
        p = self.page
        p.box(100, 100, 200, 200)
        p.box(200, 100, 300, 200)
        p.ink[150:156, 200:206] = False
        p.paint(100, 100, 306, 206, SKIN)
        ids = self.run_import()
        left, right = ids[120, 150], ids[120, 250]
        self.assertTrue(imp.is_region(left) and imp.is_region(right))
        self.assertNotEqual(left, right)
        self.assertIn(ids[152, 202], (left, right), "the crack itself belongs to one of the cells")

    def test_cells_joined_through_a_wide_opening_stay_one_region(self):
        # The same two cells with a 40 px doorway between them are one shape, as drawn.
        p = self.page
        p.box(100, 100, 200, 200)
        p.box(200, 100, 300, 200)
        p.ink[130:170, 200:206] = False
        p.paint(100, 100, 306, 206, SKIN)
        ids = self.run_import()
        self.assertEqual(ids[120, 150], ids[120, 250])


if __name__ == "__main__":
    unittest.main()
