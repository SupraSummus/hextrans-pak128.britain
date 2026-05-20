"""BR Standard Class 2MT 2-6-2 tank — base and push-pull variants.

Upstream ships both in one dat sharing the same EmptyImage refs
(same loco, push-pull is an in-place upgrade).
"""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = "trains/Locomotives/br-2mt-tank.blend"
_UPSTREAM_DAT = "trains/br-2mt-tank.dat"

# http://en.wikipedia.org/wiki/BR_Standard_Class_2_2-6-2T
BASE = Vehicle(
    name="BR-2MT-Tank",
    waytype="track",
    copyright="Kieron",
    freight="None",
    engine_type="steam",
    intro_year=1953, intro_month=8,
    retire_year=1957, retire_month=6,
    speed=100,
    length=7,
    # Extrapolated
    power=234,
    tractive_effort=82,
    weight=67,
    axle_load=14,
    rolling_resistance=13,
    payload=0,
    cost=3205000,
    runningcost=188,
    fixed_cost=18671,
    increase_maintenance_after_years=6,
    years_before_maintenance_max_reached=12,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke="Steam",
    sound="lwalker-br-4mt-tank.wav",
    upgrade=["BR-2MT-Tank-Push-Pull"],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
)

PUSH_PULL = Vehicle(
    name="BR-2MT-Tank-Push-Pull",
    waytype="track",
    copyright="Kieron",
    freight="None",
    engine_type="steam",
    intro_year=1953, intro_month=7,
    retire_year=1957, retire_month=6,
    speed=100,
    length=7,
    # Extrapolated
    power=234,
    tractive_effort=82,
    weight=67,
    axle_load=14,
    rolling_resistance=13,
    payload=0,
    cost=3275000,
    runningcost=180,
    fixed_cost=26729,
    upgrade_price=95000,
    increase_maintenance_after_years=6,
    years_before_maintenance_max_reached=12,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke="Steam",
    sound="lwalker-br-4mt-tank.wav",
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
)

SPECS = [BASE, PUSH_PULL]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
