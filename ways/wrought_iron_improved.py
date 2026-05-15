"""Bake the improved wrought-iron rail.

`SPEC` mirrors the upstream `wrought_iron_improved.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.wrought_iron_improved
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='wrought_iron_improved_track',
    waytype='track',
    intro_year=1855,
    intro_month=3,
    retire_year=1875,
    retire_month=9,
    topspeed=130,
    max_weight=14,
    wear_capacity=576000000,
    cost=46500,
    maintenance=610,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (43, 34, 32),
    "Wood": (72, 70, 62),
    "Rail": (84, 86, 75),
    "RailTop": (136, 131, 126),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
