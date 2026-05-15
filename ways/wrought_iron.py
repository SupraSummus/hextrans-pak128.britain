"""Bake the 60lb/yard wrought-iron rail.

`SPEC` mirrors the upstream `wrought_iron.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.wrought_iron
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='wrought_iron_track',
    waytype='track',
    intro_year=1845,
    intro_month=5,
    retire_year=1872,
    retire_month=6,
    topspeed=110,
    max_weight=10,
    wear_capacity=276480000,
    cost=40000,
    maintenance=700,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (46, 42, 40),
    "Wood": (63, 63, 58),
    "Rail": (72, 79, 68),
    "RailTop": (110, 108, 107),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
