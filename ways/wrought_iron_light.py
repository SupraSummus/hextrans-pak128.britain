"""Bake the 55lb/yard wrought-iron rail.

`SPEC` mirrors the upstream `wrought_iron_light.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.wrought_iron_light
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='wrought_iron_light_track',
    waytype='track',
    intro_year=1834,
    intro_month=6,
    retire_year=1852,
    retire_month=7,
    topspeed=85,
    max_weight=7,
    wear_capacity=142560000,
    cost=32000,
    maintenance=750,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (45, 40, 39),
    "Wood": (64, 60, 54),
    "Rail": (77, 77, 61),
    "RailTop": (122, 100, 84),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
