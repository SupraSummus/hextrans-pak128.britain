"""6wheel-parliamentary passenger carriage."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Hamilton Ellis Plate 6
# This was an ECR vehicle.
# See also p. 19 of the GER Society journal
# special edition (no. 5) summer 1989
SPEC = Vehicle(
    name="6wheel-parliamentary",
    waytype="track",
    copyright="JamesPetts",
    freight="Passagiere",
    intro_year=1845, intro_month=12,
    retire_year=1857, retire_month=6,
    speed=130,
    length=4,
    # Guessed
    weight=5.5,
    axles=3,
    brake_force=0,
    rolling_resistance=19,
    payload=46,
    min_loading_time=17,
    max_loading_time=60,
    overcrowded_capacity=20,
    cost=160000,
    runningcost=0,
    fixed_cost=133,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=["any"],
    constraint_next=["any"],
    payload_by_class=[0, 46],
    comfort_by_class=[0, 26],
    # TODO: Multiple liveries
    liverytype=["MR-Early"],
    blend="trains/Carriages/6wheel-parliamentary.blend",
    upstream_dat="trains/6wheel-parliamentary.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
