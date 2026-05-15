"""Bake the wrought-iron rail, intermediate weight.

`SPEC` mirrors the upstream `wrought_iron_intermediate.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.wrought_iron_intermediate
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='wrought_iron_intermediate_track',
    waytype='track',
    intro_year=1837,
    intro_month=8,
    retire_year=1867,
    retire_month=12,
    topspeed=100,
    max_weight=9,
    wear_capacity=231840000,
    cost=36000,
    maintenance=725,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (49, 46, 44),
    "Wood": (69, 66, 61),
    "Rail": (82, 81, 70),
    "RailTop": (124, 109, 98),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
