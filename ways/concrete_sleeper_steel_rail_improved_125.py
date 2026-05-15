"""Bake the improved steel rail on concrete sleepers (125mph).

`SPEC` mirrors the upstream `cssri-125.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.concrete_sleeper_steel_rail_improved_125
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='cssri-125',
    waytype='track',
    intro_year=1973,
    intro_month=6,
    topspeed=200,
    max_weight=23,
    wear_capacity=4116000000,
    cost=150000,
    maintenance=575,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (106, 106, 106),
    "Wood": (132, 127, 127),
    "Rail": (142, 136, 136),
    "RailTop": (176, 176, 176),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
