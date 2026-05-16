"""Bake the inter-urban tarmac road.

First road port — exercises the way renderer on a non-rail blend.
Unlike rails, upstream Britain doesn't ship a single straight-atom
road blend; per-material the blends repo carries
`<material>/{slope1, slope2, standard-city-base}.blend`, plus the
per-shape `road_snow/{ew-snow, n, ne, ...}.blend` family used to
pre-render snow variants.  `standard-city-base.blend` is the closest
analog to the rail strand atom; the bake runs without errors against
it but the silhouette has not been QAed against expectation (the
blend may carry only a small base mesh — the bake's Cycles memory
footprint was an order of magnitude smaller than `ns-cssr.blend`).
See TODO.md -> "Road-blend generalization" for next moves.

Run from the repo root:

    python3 -m ways.tarmac_road
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


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
