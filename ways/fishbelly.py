"""Bake the wrought-iron fishbelly rail.

`SPEC` mirrors the upstream `wrought_iron_fishbelly.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.fishbelly

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
    name='wrought_iron_fishbelly_track',
    waytype='track',
    intro_year=1820,
    intro_month=4,
    retire_year=1835,
    retire_month=9,
    topspeed=75,
    max_weight=5,
    wear_capacity=20160000,
    cost=30000,
    maintenance=755,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (83, 76, 59),
    "Wood": (97, 89, 69),
    "Rail": (111, 106, 92),
    "RailTop": (138, 133, 120),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
