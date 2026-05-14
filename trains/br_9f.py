"""Bake the BR Standard Class 9F steam locomotive.

The 9F's published power figures (>800 kW) imply >12 % thermal
efficiency, which is unrealistic; values here extrapolate on a
7 % thermal-efficiency basis instead.  See
http://www.traintesting.com/bulletin_13.htm for context.

The way_wear_factor reflects the reduced hammer blow from the
better-balanced motion.

Reference: https://en.wikipedia.org/wiki/BR_Standard_Class_9F

See `_4wheel_1850s_first.py` for the bake-unit pattern.
"""

from __future__ import annotations

from tools.threed.bake import bake_main
from tools.threed.dat import Vehicle


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
    power=601,
    tractive_effort=176,
    rolling_resistance=13,
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
)
BLEND = "trains/Locomotives/br-9f.blend"


if __name__ == "__main__":
    bake_main(SPEC, BLEND, __file__)
