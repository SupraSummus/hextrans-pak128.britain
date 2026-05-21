"""sdr-1001."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SDR-1001',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1852,
    intro_month=9,
    retire_year=1875,
    retire_month=7,
    speed=48,
    length=4,
    weight=32,
    axles=3,
    power=103,
    tractive_effort=66,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=66421,
    payload=0,
    cost=7096320,
    runningcost=138,
    fixed_cost=29914,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['SDR-1001-Tender'],
    blend='trains/Locomotives/sdr-1001-tender.blend',
    upstream_dat='trains/sdr-1001.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
