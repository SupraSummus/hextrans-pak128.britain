"""4wheel-open-third early third-class open carriage."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Early third-class open wagon from a time when second class was
# becoming routinely enclosed and third-class passengers first
# started to be conveyed.  Reference photo:
# http://gerald-massey.org.uk/Railway/carriages/Operational/Carriage3.png
SPEC = Vehicle(
    name="4wheel-open-third",
    waytype="track",
    copyright="JamesPetts",
    freight="Passagiere",
    intro_year=1837, intro_month=7,
    retire_year=1845, retire_month=4,
    speed=125,
    length=2,
    weight=1.9,
    axles=2,
    brake_force=0,
    rolling_resistance=19,
    # The payload of the (unillustrated) Birmingham & Derby Junction
    # thirds of 1839 was 40 (Lacy & Dow p. 6).  These are smaller
    # carriages -- capacity assumed lower.
    payload=30,
    min_loading_time=17,
    max_loading_time=47,
    overcrowded_capacity=15,
    cost=60000,
    runningcost=0,
    fixed_cost=125,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=["any"],
    constraint_next=["any"],
    payload_by_class=[0, 30],
    comfort_by_class=[0, 16],
    # TODO: add more liveries (B&DJR, GJR, MCR, MR, LNWR, etc.).
    liverytype=["LMR-Standard"],
)
BLEND = "trains/Carriages/4wheel-open-third.blend"


if __name__ == "__main__":
    bake_main(SPEC, BLEND, __file__)
