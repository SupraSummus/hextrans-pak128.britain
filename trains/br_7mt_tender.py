"""BR Standard Class 7MT Britannia tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name="BR-7MT-Tender",
    waytype="track",
    copyright="Kieron",
    freight="None",
    intro_year=1951, intro_month=1,
    retire_year=1960, retire_month=12,
    speed=160,
    length=4,
    weight=49,
    axles=3,
    power=0,
    rolling_resistance=13,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=7,
    years_before_maintenance_max_reached=13,
    constraint_prev=[
        "BR-7MT", "BR-8P",
        "SR-MerchantNavyRebuilt_4-6-2",
        "SR-WestCountryRebuilt_4-6-2",
    ],
    blend="trains/Locomotives/br-7mt-tender.blend",
    upstream_dat="trains/br-7mt-tender.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
