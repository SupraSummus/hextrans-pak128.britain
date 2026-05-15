"""Bake the improved steel rail on wooden sleepers, heavy.

`SPEC` mirrors the upstream `wssri-heavy.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.wooden_sleeper_steel_rail_improved_heavy
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='wssri_heavy',
    waytype='track',
    intro_year=1925,
    intro_month=8,
    retire_year=1968,
    retire_month=6,
    topspeed=160,
    max_weight=22,
    wear_capacity=4050000000,
    cost=135000,
    maintenance=650,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (91, 84, 82),
    "Wood": (119, 115, 113),
    "Rail": (132, 129, 129),
    "RailTop": (181, 178, 174),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
