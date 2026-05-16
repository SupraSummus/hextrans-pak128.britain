"""Inter-urban tarmac road."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


# 0.5 msa.
SPEC = Way(
    name="tarmac_road",
    waytype="road",
    intro_year=1896,
    intro_month=6,
    topspeed=64,
    max_weight=4,
    wear_capacity=32500000,
    cost=40000,
    maintenance=400,
)
BLEND = "ways/tarmac/standard-city-base.blend"
MATERIALS = {
    "Dirt": (64, 64, 64),
    "MainColour1": (80, 80, 80),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
