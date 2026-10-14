#!/usr/bin/env python3
"""Copy scene assets from Content/Regions into the app bundle.

    python3 Scripts/sync_scenes.py                  # every scene with real art (vectorized or approved)
    python3 Scripts/sync_scenes.py --approved-only  # release builds: only scenes signed off as approved

Writes SaudiColoring/Resources/Scenes/<region>/<scene>/ with what the app reads at runtime:
regions.png and palette.json (the canvas draws the outline from the map's black pixels), plus
thumb.png, a 512x384 line-art thumbnail for the gallery. Each region also gets cover.png from
Content/Regions/<region>/cover.png. Resources/Scenes/catalog.json lists what was shipped; the app
reads it at launch. Scenes that are not shipped are removed from Resources/. Needs Pillow.
"""
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Content" / "Regions"
DST = ROOT / "SaudiColoring" / "Resources" / "Scenes"
SHIP = {"approved"} if "--approved-only" in sys.argv[1:] else {"vectorized", "approved"}
THUMB = (512, 384)
COVER = (400, 300)


def thumbnail(outline, out):
    im = Image.open(outline).convert("L")
    im.thumbnail(THUMB, Image.LANCZOS)
    # 4-bit grey keeps the anti-aliasing at about half the file size.
    im.point(lambda v: v // 17 * 17).convert("P", palette=Image.ADAPTIVE, colors=16).save(out, optimize=True)


catalog = []
shipped_dirs = set()
for rdir in sorted(p for p in SRC.iterdir() if p.is_dir()):
    data = json.loads((rdir / "region.json").read_text(encoding="utf-8"))
    shipped = []
    for s in data["scenes"]:
        if s.get("status") not in SHIP:
            continue
        out = DST / data["id"] / s["id"]
        out.mkdir(parents=True, exist_ok=True)
        for key in ("regions", "palette"):
            shutil.copyfile(rdir / s["assets"][key], out / Path(s["assets"][key]).name)
        thumbnail(rdir / s["assets"]["outline"], out / "thumb.png")
        shipped_dirs.add(out)
        shipped.append({k: s[k] for k in ("id", "title", "titleAr", "difficulty")})
    if shipped:
        cover = rdir / "cover.png"
        if cover.exists():
            im = Image.open(cover).convert("RGB")
            im.thumbnail(COVER, Image.LANCZOS)
            im.save(DST / data["id"] / "cover.png", optimize=True)
        catalog.append({"id": data["id"], "name": data["name"], "nameAr": data["nameAr"],
                        "order": data["order"], "scenes": shipped})

# Drop scenes that are no longer shipped (e.g. after --approved-only).
if DST.exists():
    for scene_dir in [d for d in DST.glob("*/*") if d.is_dir()]:
        if scene_dir not in shipped_dirs:
            shutil.rmtree(scene_dir)
    shipped_regions = {r["id"] for r in catalog}
    for region_dir in [d for d in DST.iterdir() if d.is_dir()]:
        if region_dir.name not in shipped_regions:
            shutil.rmtree(region_dir)

DST.mkdir(parents=True, exist_ok=True)
(DST / "catalog.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"synced {sum(len(r['scenes']) for r in catalog)} scenes ({' + '.join(sorted(SHIP))}) across {len(catalog)} regions")
