"""Bake the improved steel rail on wooden sleepers, light section.

`SPEC` mirrors the upstream `wssri-light.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.wooden_sleeper_steel_rail_improved_light
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='wssri_light',
    waytype='track',
    intro_year=1894,
    intro_month=11,
    retire_year=1974,
    retire_month=6,
    topspeed=90,
    max_weight=17,
    wear_capacity=1492114286,
    cost=45000,
    maintenance=360,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (53, 43, 40),
    "Wood": (89, 78, 73),
    "Rail": (106, 95, 89),
    "RailTop": (167, 158, 146),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
