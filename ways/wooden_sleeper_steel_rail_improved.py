"""Bake the improved steel rail on wooden sleepers.

`SPEC` mirrors the upstream `wssri.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.wooden_sleeper_steel_rail_improved
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='wssri',
    waytype='track',
    intro_year=1888,
    intro_month=11,
    retire_year=1990,
    retire_month=7,
    topspeed=155,
    max_weight=19,
    wear_capacity=3088800000,
    cost=75000,
    maintenance=500,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (82, 73, 71),
    "Wood": (113, 106, 104),
    "Rail": (126, 120, 120),
    "RailTop": (178, 174, 168),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
