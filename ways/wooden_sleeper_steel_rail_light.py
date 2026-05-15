"""Bake the lightweight steel rail on wooden sleepers.

`SPEC` mirrors the upstream `wssr-light.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.wooden_sleeper_steel_rail_light
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='wssr_light',
    waytype='track',
    intro_year=1876,
    intro_month=2,
    retire_year=1903,
    retire_month=4,
    topspeed=80,
    max_weight=15,
    wear_capacity=1008000000,
    cost=32000,
    maintenance=375,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (51, 43, 40),
    "Wood": (78, 67, 61),
    "Rail": (91, 79, 72),
    "RailTop": (140, 130, 116),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
