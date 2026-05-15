"""Bake the 86lb/yard steel rail on wooden sleepers.

`SPEC` mirrors the upstream `wssr.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.wooden_sleeper_steel_rail
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='wssr',
    waytype='track',
    intro_year=1874,
    intro_month=6,
    retire_year=1895,
    retire_month=3,
    topspeed=145,
    max_weight=17,
    wear_capacity=2323200000,
    cost=55000,
    maintenance=550,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (65, 57, 55),
    "Wood": (94, 88, 86),
    "Rail": (106, 101, 101),
    "RailTop": (155, 151, 146),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
