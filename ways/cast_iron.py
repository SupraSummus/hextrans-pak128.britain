"""Bake the cast-iron edge rail (pre-wrought-iron era).

`SPEC` mirrors the upstream `cast_iron.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.cast_iron

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
    name='cast_iron_track',
    waytype='track',
    intro_year=1789,
    intro_month=10,
    retire_year=1831,
    retire_month=9,
    topspeed=27,
    max_weight=4,
    wear_capacity=8640000,
    cost=30000,
    maintenance=800,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (62, 54, 42),
    "Wood": (77, 66, 51),
    "Rail": (92, 84, 74),
    "RailTop": (223, 223, 223),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
