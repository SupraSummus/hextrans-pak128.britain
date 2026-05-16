"""4wheel-1850s-first passenger carriage."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle


SPEC = Vehicle(
    name="4-wheel-1850s-first",
    waytype="track",
    copyright="James/jamespetts",
    freight="Passagiere",
    intro_year=1850, intro_month=9,
    retire_year=1859, retire_month=10,
    speed=135,
    length=3,
    weight=8.1,
    axles=2,
    brake_force=0,
    rolling_resistance=19,
    payload=18,
    min_loading_time=17,
    max_loading_time=47,
    overcrowded_capacity=12,
    cost=167000,
    runningcost=0,
    fixed_cost=139,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=["any"],
    constraint_next=["any"],
    payload_by_class=[0, 0, 0, 18],
    comfort_by_class=[0, 38, 41, 69],
    liverytype=[
        "LNWR-Early", "MR-Early", "MR-Standard", "GNR-early",
        "LSWR-Indian-red", "GWR-early", "GWR-two-tone",
    ],
)
BLEND = "trains/Carriages/4wheel-1850.blend"
UPSTREAM_STEM = "trains/carriages/4wheel-1850-first-lnwr"


if __name__ == "__main__":
    bake_main(SPEC, BLEND, __file__)
