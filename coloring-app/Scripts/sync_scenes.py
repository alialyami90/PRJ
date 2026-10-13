#!/usr/bin/env python3
"""Copy approved scene assets from Content/Regions into the app bundle.

Only scenes with status "approved" are copied, into
SaudiColoring/Resources/Scenes/<region>/<scene>/. Also writes
Resources/Scenes/catalog.json, which the app reads at launch.
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Content" / "Regions"
DST = ROOT / "SaudiColoring" / "Resources" / "Scenes"

catalog = []
for rdir in sorted(p for p in SRC.iterdir() if p.is_dir()):
    data = json.loads((rdir / "region.json").read_text(encoding="utf-8"))
    shipped = []
    for s in data["scenes"]:
        if s.get("status") != "approved":
            continue
        out = DST / data["id"] / s["id"]
        out.mkdir(parents=True, exist_ok=True)
        for rel in s["assets"].values():
            shutil.copy2(rdir / rel, out / Path(rel).name)
        shipped.append({k: s[k] for k in ("id", "title", "titleAr", "difficulty")})
    if shipped:
        catalog.append({"id": data["id"], "name": data["name"], "nameAr": data["nameAr"],
                        "order": data["order"], "scenes": shipped})

DST.mkdir(parents=True, exist_ok=True)
(DST / "catalog.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"synced {sum(len(r['scenes']) for r in catalog)} approved scenes across {len(catalog)} regions")
