#!/usr/bin/env python3
"""Validate Content/Regions/*/region.json manifests.

Checks: exactly 8 regions, 8 scenes per region, unique ids, a short title in English and
Arabic for every scene (at most 4 and 5 words), and that every scene whose status is not
"todo" has its asset files on disk.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Content" / "Regions"
STATUSES = {"todo", "sketched", "vectorized", "approved"}
ERAS = {"traditional", "modern"}
CHARACTER_TYPES = {"person", "animal"}

errors = []
regions = sorted(p for p in ROOT.iterdir() if p.is_dir())
if len(regions) != 8:
    errors.append(f"expected 8 regions, found {len(regions)}")

seen_scene_ids = set()
for rdir in regions:
    manifest = rdir / "region.json"
    if not manifest.exists():
        errors.append(f"{rdir.name}: missing region.json")
        continue
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if data.get("id") != rdir.name:
        errors.append(f"{rdir.name}: id mismatch ({data.get('id')})")
    scenes = data.get("scenes", [])
    if len(scenes) != 8:
        errors.append(f"{rdir.name}: expected 8 scenes, found {len(scenes)}")
    for s in scenes:
        sid = s.get("id")
        if sid in seen_scene_ids:
            errors.append(f"{rdir.name}/{sid}: duplicate scene id")
        seen_scene_ids.add(sid)
        title, title_ar = s.get("title", ""), s.get("titleAr", "")
        if not title or len(title.split()) > 4:
            errors.append(f"{rdir.name}/{sid}: title must be 1 to 4 words ({title!r})")
        if not title_ar or len(title_ar.split()) > 5:
            errors.append(f"{rdir.name}/{sid}: titleAr must be 1 to 5 words ({title_ar!r})")
        if s.get("status") not in STATUSES:
            errors.append(f"{rdir.name}/{sid}: bad status {s.get('status')!r}")
        if s.get("era") not in ERAS:
            errors.append(f"{rdir.name}/{sid}: era must be traditional or modern")
        ch = s.get("character") or {}
        if ch.get("type") not in CHARACTER_TYPES or not ch.get("description"):
            errors.append(f"{rdir.name}/{sid}: character needs type (person/animal) and description")
        if s.get("status", "todo") != "todo":
            for key, rel in s.get("assets", {}).items():
                if not (rdir / rel).exists():
                    errors.append(f"{rdir.name}/{sid}: missing {key} asset {rel}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(regions)} regions, {len(seen_scene_ids)} scenes")
