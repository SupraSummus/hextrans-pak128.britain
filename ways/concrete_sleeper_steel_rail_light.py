"""Bake the lightweight steel rail on concrete sleepers.

`SPEC` mirrors the upstream `cssr-light.dat` gameplay data; `BLEND` is
shared with every rail grade (the upstream `ns-cssr.blend`
strand-atom), and `MATERIALS` is the per-variant recolour applied
to the four blend slots — see CLAUDE.md -> "Rail-grade material
recolour".  Run from the repo root:

    python3 -m ways.concrete_sleeper_steel_rail_light
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name='cssr_light',
    waytype='track',
    intro_year=1968,
    intro_month=8,
    topspeed=120,
    max_weight=20,
    wear_capacity=2397600000,
    cost=105000,
    maintenance=200,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (61, 61, 61),
    "Wood": (95, 95, 95),
    "Rail": (112, 112, 112),
    "RailTop": (168, 168, 168),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
