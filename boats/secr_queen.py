"""SECR The Queen — 1903 steam passenger ferry.

https://en.wikipedia.org/wiki/TSS_The_Queen
"""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name="SECRQueen",
    waytype="water",
    copyright="James",
    freight="Passagiere",
    engine_type="steam",
    intro_year=1903, intro_month=4,
    retire_year=1925, retire_month=1,
    speed=40,
    length=10,
    weight=800,
    power=4250,
    payload=450,
    # 40-60 minutes
    min_loading_time=2400,
    max_loading_time=3600,
    catering_level=4,
    cost=67500000,
    runningcost=259,
    fixed_cost=228125,
    smoke="Steam",
    sound="ship-horn_a.wav",
    range=260,
    constraint_prev=["none"],
    constraint_next=["SECRQueenAddMail"],
    payload_by_class=[0, 450, 0, 125],
    comfort_by_class=[0, 95, 0, 165],
    blend="boats/secr-queen.blend",
    upstream_stem="boats/images/secr-queen",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
