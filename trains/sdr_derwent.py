"""sdr-derwent."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SDR-Derwent',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1845,
    intro_month=5,
    retire_year=1849,
    retire_month=10,
    speed=46,
    length=4,
    weight=22,
    axles=3,
    power=70,
    tractive_effort=18,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=45629,
    payload=0,
    cost=5280000,
    runningcost=126,
    fixed_cost=31333,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['SDR-Derwent-Tender'],
    blend='trains/Locomotives/derwent.blend',
    upstream_dat='trains/sdr-derwent.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
