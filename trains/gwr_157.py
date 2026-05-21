"""gwr-157."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_157_Class_(Dean)
# See also Ahrons p. 210
SPEC = Vehicle(
    name='gwr-157',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1878,
    intro_month=11,
    retire_year=1889,
    retire_month=3,
    speed=135,
    length=4,
    weight=36.7,
    axle_load=17,
    power=243,
    tractive_effort=46,
    brake_force=19,
    payload=0,
    cost=15941310,
    runningcost=270,
    fixed_cost=39387,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity'],
    blend='trains/Locomotives/gwr-157-ww1-austerity.blend',
    upstream_dat='trains/gwr-157.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
