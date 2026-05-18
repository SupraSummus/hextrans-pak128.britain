"""Dogger — 17th-century North Sea sailing fishing boat."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name="Dogger",
    waytype="water",
    copyright="James",
    freight="FreshFish",
    engine_type="sail",
    intro_year=1650, intro_month=1,
    retire_year=1900,
    speed=12,
    length=7,
    weight=10,
    power=400,
    payload=8,
    # 1-2 hours
    min_loading_time=3600,
    max_loading_time=7200,
    cost=240000,
    runningcost=0,
    fixed_cost=16167,
    constraint_prev=["none"],
    constraint_next=["none"],
    blend="boats/dogger.blend",
    upstream_dat="boats/dogger.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
