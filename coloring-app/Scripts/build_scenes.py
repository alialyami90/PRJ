#!/usr/bin/env python3
"""Build every Content/Regions/<region>/<scene>/scene.py (or only the regions given as args).

Each build writes outline.svg, regions.png, palette.json and preview.png next to its
scene.py. Exits non-zero if any scene fails to build. Needs Pillow.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Content" / "Regions"
only = set(sys.argv[1:])
failed = []
for scene in sorted(ROOT.glob("*/*/scene.py")):
    if only and scene.parent.parent.name not in only:
        continue
    # One process per scene: every region has its own _figures module of the same name.
    r = subprocess.run([sys.executable, "-B", str(scene)], capture_output=True, text=True)
    print(r.stdout, end="")
    if r.returncode:  # report and keep going so one bad scene doesn't hide the rest
        failed.append(f"{scene.parent.parent.name}/{scene.parent.name}: {r.stderr.strip().splitlines()[-1]}")
if failed:
    print("FAILED:\n  " + "\n  ".join(failed))
    sys.exit(1)
