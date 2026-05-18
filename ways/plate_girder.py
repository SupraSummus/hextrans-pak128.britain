"""Plate-girder bridge — render the JH straight / end / slope blends
through the hex `bridge_hex` viewpoint into a sibling
`plate_girder/` directory.

Pre-port scaffold.  Not following the SPEC + `bake_<asset>_main(SPEC,
__file__)` pattern other ported assets use because the supporting
infrastructure (a `Bridge` dataclass in `pak.dat`, a `bake_bridge_main`
in `pak.bake`, `Obj=bridge` dat emission with the
`BackImage`/`FrontImage`/`Start`/`Ramp` per-direction-per-variant key
layout) hasn't landed yet.  When it does, this script gains a real
SPEC and the body collapses to a single `bake_bridge_main` call —
the gameplay data the SPEC would carry is preserved as a comment
below to keep the port-in-progress visible.

Eventual SPEC (kept inline so a future port doesn't have to re-read
`ways/plate-girder.dat`):

    SPEC = Bridge(
        name="PlateGirder",
        waytype="track",
        intro_year=1890, intro_month=9,
        retire_year=1949, retire_month=1,
        topspeed=160, cost=2760000, maintenance=100,
        max_weight=400, max_length=4,
        pillar_distance=2, pillar_asymmetric=1,
        blends_dir="ways/plate_girder",
        blends=("straight", "end", "slope"),
    )

Run from the repo root:

    python3 -m ways.plate_girder
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pak import REPO_ROOT
from pak.fetch_jh_blend import fetch as fetch_jh

# The three JH blends we have coverage for — see
# `pak.diff_bridge_overview` CASES for which upstream cells each
# matches.
_BLENDS: tuple[str, ...] = ("straight", "end", "slope")

# Sibling output directory holding one single-row 8-facing atlas per
# blend (`plate_girder/<stem>.png`).
_OUT_DIR = Path(__file__).resolve().parent / "plate_girder"


def main() -> int:
    _OUT_DIR.mkdir(exist_ok=True)
    for stem in _BLENDS:
        blend = fetch_jh(f"ways/plate_girder/{stem}.blend")
        subprocess.run([
            "blender", "-b", str(blend),
            "-P", str(REPO_ROOT / "pak" / "render.py"), "--",
            "--out", str(_OUT_DIR), "--name", stem,
            "--viewpoint", "bridge_hex",
        ], check=True, stdout=subprocess.DEVNULL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
