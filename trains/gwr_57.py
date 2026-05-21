"""gwr-57."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/Daniel_Gooch_standard_gauge_locomotives#57_Class
# Little data available, so assume a goods version of the 69 class with 5ft0 wheels
SPEC = Vehicle(
    name='gwr-57',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1855,
    intro_month=2,
    retire_year=1862,
    retire_month=9,
    speed=75,
    length=4,
    weight=21.1,
    axle_load=12,
    power=156,
    tractive_effort=44,
    brake_force=0,
    payload=0,
    cost=11500000,
    runningcost=208,
    fixed_cost=32500,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown'],
    blend='trains/Locomotives/gwr-57-churchward.blend',
    upstream_dat='trains/gwr-57.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
