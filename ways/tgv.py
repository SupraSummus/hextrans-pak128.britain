"""Bake the TGV (high-speed rail) track.

UK HS1 / French TGV-style permanent way — solid concrete base,
no ballast.  The bake reuses `pak/bake_way.py`'s composition
pipeline against `ways/tgv.blend` as a second-rail generalization
test of the renderer (CLAUDE.md -> "Per-blend strip lists belong
in a per-asset bake script").

Run from the repo root:

    python3 -m ways.tgv
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name="tgv",
    waytype="track",
    intro_year=1981,
    intro_month=9,
    topspeed=320,
    max_weight=21,
    wear_capacity=4200000000,
    cost=250000,
    maintenance=950,
)
BLEND = "ways/tgv.blend"


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__)
