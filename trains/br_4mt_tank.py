"""BR Standard Class 4MT 2-6-4 tank locomotive."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name="BR-4MT-Tank",
    waytype="track",
    copyright="Kieron",
    freight="None",
    engine_type="steam",
    intro_year=1951, intro_month=7,
    retire_year=1957, retire_month=11,
    speed=126,
    # Extrapolated
    power=312,
    tractive_effort=111,
    weight=86,
    axle_load=18,
    rolling_resistance=13,
    payload=0,
    cost=4435000,
    runningcost=328,
    fixed_cost=27696,
    increase_maintenance_after_years=8,
    years_before_maintenance_max_reached=11,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke="Steam",
    sound="lwalker-br-4mt-tank.wav",
    blend="trains/Locomotives/br-4mt-tank.blend",
    upstream_dat="trains/br-4mt-tank.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
