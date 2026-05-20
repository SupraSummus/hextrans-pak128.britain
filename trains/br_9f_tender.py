"""BR Standard Class 9F tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name="BR-9F-Tender",
    waytype="track",
    copyright="Kieron",
    freight="None",
    intro_year=1954, intro_month=6,
    retire_year=1960, retire_month=2,
    speed=105,
    length=4,
    weight=56,
    axles=3,
    power=0,
    rolling_resistance=13,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=4,
    years_before_maintenance_max_reached=12,
    constraint_prev=["BR-9F"],
    blend="trains/Locomotives/br-9f-tender.blend",
    upstream_dat="trains/br-9f-tender.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
