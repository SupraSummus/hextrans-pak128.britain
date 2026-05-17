"""BR Standard Class 9F steam locomotive."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/BR_Standard_Class_9F
SPEC = Vehicle(
    name="BR-9F",
    waytype="track",
    copyright="Kieron",
    freight="None",
    engine_type="steam",
    intro_year=1954, intro_month=6,
    retire_year=1960, retire_month=2,
    speed=110,
    weight=85,
    axle_load=16,
    # Published power figures of >800 kW imply >12 % thermal
    # efficiency, which is unrealistic; extrapolated on a 7 %
    # thermal-efficiency basis instead.
    # http://www.traintesting.com/bulletin_13.htm
    power=601,
    tractive_effort=176,
    rolling_resistance=13,
    # Reflects the reduced hammer blow from the better-balanced motion.
    way_wear_factor=122188,
    payload=0,
    cost=7948000,
    runningcost=445,
    fixed_cost=56558,
    increase_maintenance_after_years=4,
    years_before_maintenance_max_reached=12,
    smoke="Steam",
    sound="the-mart-ban-br-9f.wav",
    constraint_next=["BR-9F-Tender"],
    blend="trains/Locomotives/br-9f.blend",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
