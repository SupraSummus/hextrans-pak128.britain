"""gwr-1600."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_1600_Class
SPEC = Vehicle(
    name='gwr-1600',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1949,
    intro_month=1,
    retire_year=1955,
    retire_month=7,
    speed=85,
    length=5,
    weight=42.3,
    axles=3,
    power=196,
    tractive_effort=82,
    payload=0,
    cost=255000,
    runningcost=105,
    fixed_cost=19000,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-hawksworth', 'BR-Early'],
    blend='trains/Locomotives/gwr-1600-br.blend',
    upstream_dat='trains/gwr-1600.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
