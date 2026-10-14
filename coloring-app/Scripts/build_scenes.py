#!/usr/bin/env python3
"""Build every scene under Content/Regions (or only the regions given as args).

A scene with illustrator art (art/line.png + art/color.png) is imported with
import_illustration.py; otherwise its placeholder scene.py sketch is built. Either way
regions.png, palette.json, preview.png and an outline land in the scene folder.
Exits non-zero if any scene fails to build. Needs Pillow (and numpy for imported art).
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Content" / "Regions"
IMPORT = Path(__file__).resolve().parent / "import_illustration.py"
only = set(sys.argv[1:])
failed = []
for scene_dir in sorted(d for d in ROOT.glob("*/*") if d.is_dir()):
    if only and scene_dir.parent.name not in only:
        continue
    if (scene_dir / "art" / "line.png").exists():
        cmd = [sys.executable, "-B", str(IMPORT), str(scene_dir)]
    elif (scene_dir / "scene.py").exists():
        # One process per scene: every region has its own _figures module of the same name.
        cmd = [sys.executable, "-B", str(scene_dir / "scene.py")]
    else:
        continue
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout, end="")
    if r.returncode:  # report and keep going so one bad scene doesn't hide the rest
        failed.append(f"{scene_dir.parent.name}/{scene_dir.name}: {r.stderr.strip().splitlines()[-1]}")
if failed:
    print("FAILED:\n  " + "\n  ".join(failed))
    sys.exit(1)
