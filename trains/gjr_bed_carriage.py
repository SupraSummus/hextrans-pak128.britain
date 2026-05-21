"""gjr-bed-carriage."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Hamilton Ellis pp. 22-3
# http://gerald-massey.org.uk/Railway/c13_operational.htm
SPEC = Vehicle(
    name='gjr-bed-carriage',
    waytype='track',
    copyright='James/jamespetts',
    freight='Passagiere',
    intro_year=1838,
    intro_month=2,
    retire_year=1842,
    retire_month=2,
    speed=125,
    length=3,
    weight=2.8,
    axles=2,
    brake_force=0,
    rolling_resistance=19,
    payload=10,
    min_loading_time=35,
    max_loading_time=120,
    overcrowded_capacity=0,
    cost=200000,
    runningcost=0,
    fixed_cost=167,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_next=['railway-mail-locker'],
    payload_by_class=[0, 0, 0, 0, 10],
    comfort_by_class=[0, 0, 0, 0, 70],
    liverytype=['LMR-Standard'],
    blend='trains/Carriages/gjr-bed-carriage.blend',
    upstream_dat='trains/gjr-bed-carriage.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
