"""lner-steam-railmotor-1924."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.lner.info/locos/Railcar/sentinel.php
# See also Jenkinson pp. 442-3
SPEC = Vehicle(
    name='lner-steam-railmotor-1924',
    waytype='track',
    copyright='JamesPetts',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1924,
    intro_month=4,
    retire_year=1930,
    retire_month=1,
    speed=90,
    length=10,
    weight=17.3,
    axle_load=11,
    power=202,
    tractive_effort=70,
    payload=52,
    min_loading_time=20,
    max_loading_time=105,
    overcrowded_capacity=30,
    cost=1715000,
    runningcost=62,
    fixed_cost=18500,
    bidirectional=1,
    can_lead_from_rear=1,
    smoke='Steam',
    sound='laurie-gwr-railmotor.wav',
    payload_by_class=[0, 52],
    comfort_by_class=[0, 70],
    liverytype=['LNER-Standard', 'BR-Early'],
    blend='trains/Railcars/lner-steam-railmotor-1924-br.blend',
    upstream_dat='trains/lner-steam-railmotor-1924.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
