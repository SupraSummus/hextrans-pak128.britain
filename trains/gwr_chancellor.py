"""gwr-chancellor."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/Daniel_Gooch_standard_gauge_locomotives#%22England%22_or_%22Chancellor%22_Class
# Very little data, so much guessed. Assumed to be 6'6 four coupled versions of the Sharp class
SPEC = Vehicle(
    name='gwr-chancellor',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1862,
    intro_month=2,
    retire_year=1867,
    retire_month=2,
    speed=110,
    length=4,
    weight=21.1,
    axle_load=12,
    power=171,
    tractive_effort=35,
    brake_force=0,
    payload=0,
    cost=17200000,
    runningcost=210,
    fixed_cost=38500,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green'],
    blend='trains/Locomotives/gwr-chancellor-dark-green.blend',
    upstream_dat='trains/gwr-chancellor.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
