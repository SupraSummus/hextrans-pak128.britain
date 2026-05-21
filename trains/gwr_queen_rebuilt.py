"""gwr-queen-rebuilt."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_Queen_Class
# See also Ahrons p. 186
SPEC = Vehicle(
    name='gwr-queen-rebuilt',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1884,
    intro_month=10,
    retire_year=1895,
    retire_month=11,
    speed=135,
    length=4,
    weight=35.1,
    axle_load=15,
    power=238,
    tractive_effort=45,
    brake_force=19,
    payload=0,
    cost=19150560,
    runningcost=252,
    fixed_cost=39200,
    upgrade_price=3830112,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity'],
    blend='trains/Locomotives/gwr-queen.blend',
    upstream_dat='trains/gwr-queen-rebuilt.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
