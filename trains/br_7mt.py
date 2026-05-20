"""BR Standard Class 7MT Britannia Pacific."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# For possible calibration data see http://www.traintesting.com/bulletin_5.htm
# Max. speed given as 73mph with a train of 993t (gross, equivalent given testing vehicles)
# On the level
# NOTE: The source itself suggests drawbar horsepower at approx. 2,000,
# which is equivalent to 1491Kw, compared to the 847kW suggested
# by in-game tests. However, even this is out of line with other
# locomotives, so extrapolated.
# http://en.wikipedia.org/wiki/BR_Standard_Class_7
SPEC = Vehicle(
    name="BR-7MT",
    waytype="track",
    copyright="Kieron",
    freight="None",
    engine_type="steam",
    intro_year=1951, intro_month=1,
    retire_year=1957, retire_month=9,
    speed=160,
    weight=94,
    axle_load=20,
    power=639,
    tractive_effort=143,
    rolling_resistance=13,
    way_wear_factor=147839,
    payload=0,
    cost=9849000,
    runningcost=516,
    fixed_cost=48208,
    increase_maintenance_after_years=7,
    years_before_maintenance_max_reached=13,
    smoke="Steam",
    sound="konakaboom-black-five.wav",
    constraint_next=["BR-7MT-Tender"],
    blend="trains/Locomotives/br-7mt.blend",
    upstream_dat="trains/br-7mt.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
