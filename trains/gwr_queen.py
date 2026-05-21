"""gwr-queen."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_Queen_Class
# See also Ahrons p. 186
SPEC = Vehicle(
    name='gwr-queen',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1873,
    intro_month=10,
    retire_year=1878,
    retire_month=12,
    speed=132,
    length=4,
    weight=34.0,
    axle_load=14,
    power=220,
    tractive_effort=45,
    brake_force=0,
    payload=0,
    cost=19150560,
    runningcost=250,
    fixed_cost=39359,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity'],
    upgrade=['gwr-queen-rebuilt'],
    blend='trains/Locomotives/gwr-queen-churchward-ww1-austerity.blend',
    upstream_dat='trains/gwr-queen.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
