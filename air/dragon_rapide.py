"""Bake the de Havilland DH.89 Dragon Rapide passenger biplane.

First aircraft port — confirms upstream's `vehicles`-alignment
camera + 128px tile size also works for air assets straight out
of the box (no new viewpoint or scale tweaks beyond what
trains/road vehicles already use; see CLAUDE.md -> "Upstream
blend calibration contract", "Alignment mode" paragraph).

The upstream dat ships a paired mail variant
(`dragon-rapide-mail`); not yet ported — would be the first
multi-object bake unit.  See `_4wheel_1850s_first.py` for the
single-object pattern this script follows.
"""

from __future__ import annotations

from tools.threed.bake import bake_main
from tools.threed.dat import Vehicle


SPEC = Vehicle(
    name="dragon-rapide",
    waytype="air",
    copyright="Emmanuel Baranger",
    freight="Passagiere",
    engine_type="petrol",
    intro_year=1934, intro_month=4,
    retire_year=1939, retire_month=12,
    speed=214,
    weight=1.6,
    power=300,
    tractive_effort=4,
    payload=8,
    min_loading_time=1600,
    max_loading_time=1600,
    catering_level=0,
    cost=2000000,
    runningcost=15,
    fixed_cost=51389,
    sound="andysvideo-vickers-vimy.wav",
    minimum_runway_length=265,
    range=895,
    constraint_prev=["none"],
    constraint_next=["none"],
    payload_by_class=[0, 0, 0, 0, 8],
    comfort_by_class=[0, 0, 0, 0, 68],
)
BLEND = "air/dragon-rapide.blend"
UPSTREAM_STEM = "air/images/dragon-rapide"


if __name__ == "__main__":
    bake_main(SPEC, BLEND, __file__)
