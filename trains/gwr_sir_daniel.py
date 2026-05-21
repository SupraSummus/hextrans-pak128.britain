"""gwr-sir-daniel."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_378_Class
# https://hughevelynprints.com/wp-content/uploads/2018/08/RA-03-GWR-No.-378.jpg
# See also Ahrons p. 167
SPEC = Vehicle(
    name='gwr-sir-daniel',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1866,
    intro_month=9,
    retire_year=1873,
    retire_month=12,
    speed=125,
    length=4,
    weight=30.1,
    axle_load=13,
    power=195,
    tractive_effort=43,
    brake_force=0,
    payload=0,
    cost=15561450,
    runningcost=220,
    fixed_cost=29955,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown'],
    blend='trains/Locomotives/gwr-sir-daniel-churchward.blend',
    upstream_dat='trains/gwr-sir-daniel.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
