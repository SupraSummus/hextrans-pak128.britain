"""lner-steam-railmotor-1928."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.lner.info/locos/Railcar/sentinel.php
# Type 89
# See also Jenkinson pp. 442-3
SPEC = Vehicle(
    name='lner-steam-railmotor-1928',
    waytype='track',
    copyright='JamesPetts',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1928,
    intro_month=1,
    retire_year=1937,
    retire_month=3,
    speed=92,
    length=11,
    weight=23.6,
    axle_load=7,
    power=221,
    tractive_effort=74,
    payload=59,
    min_loading_time=20,
    max_loading_time=115,
    overcrowded_capacity=34,
    cost=1789000,
    runningcost=69,
    fixed_cost=18500,
    bidirectional=1,
    can_lead_from_rear=1,
    smoke='Steam',
    sound='laurie-gwr-railmotor.wav',
    payload_by_class=[0, 59],
    comfort_by_class=[0, 70],
    liverytype=['LNER-Standard', 'BR-Early'],
    blend='trains/Railcars/lner-steam-railmotor-1928-br.blend',
    upstream_dat='trains/lner-steam-railmotor-1928.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
