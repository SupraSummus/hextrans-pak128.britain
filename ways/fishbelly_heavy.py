"""Bake the heavier wrought-iron fishbelly rail.

`SPEC` mirrors the upstream `wrought_iron_fishbelly_heavy.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.fishbelly_heavy

Geometry caveat: real edge-rail of this era was iron strips on
stone setts — no crushed-stone ballast, no transverse wooden
sleepers.  Rendering through `ns-cssr.blend` gives a tinted
ballasted track that's visually anachronistic; gameplay data is
correct but the sprite isn't.  See TODO.md -> "Cast-iron /
fishbelly geometry mismatch".
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='wrought_iron_fishbelly_heavy_track',
    waytype='track',
    intro_year=1827,
    intro_month=8,
    retire_year=1845,
    retire_month=2,
    topspeed=80,
    max_weight=6,
    wear_capacity=28800000,
    cost=31700,
    maintenance=765,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (101, 95, 79),
    "Wood": (111, 106, 91),
    "Rail": (121, 118, 108),
    "RailTop": (138, 134, 127),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
