"""gwr-717."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_56_Class
SPEC = Vehicle(
    name='gwr-717',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1871,
    intro_month=4,
    retire_year=1881,
    retire_month=7,
    speed=112,
    length=4,
    weight=39.8,
    axle_load=15,
    power=193,
    tractive_effort=52,
    brake_force=0,
    payload=0,
    cost=9933229,
    runningcost=255,
    fixed_cost=32709,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity'],
    blend='trains/Locomotives/gwr-717-dark-green-early.blend',
    upstream_dat='trains/gwr-717.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
