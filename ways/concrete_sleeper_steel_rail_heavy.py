"""Bake the heavy steel rail on concrete sleepers.

`SPEC` mirrors the upstream `cssr-heavy.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.concrete_sleeper_steel_rail_heavy
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='cssr_heavy',
    waytype='track',
    intro_year=1992,
    intro_month=2,
    topspeed=145,
    max_weight=26,
    wear_capacity=4200000000,
    cost=110000,
    maintenance=300,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (95, 95, 95),
    "Wood": (125, 120, 120),
    "Rail": (137, 130, 130),
    "RailTop": (174, 174, 174),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
