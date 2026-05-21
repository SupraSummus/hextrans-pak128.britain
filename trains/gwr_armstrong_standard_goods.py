"""gwr-armstrong-standard-goods."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_388_class
# Boiler details here: http://www.gwr.org.uk/no-boilers.html
# https://www.rmweb.co.uk/community/uploads/monthly_01_2019/post-17793-0-45927500-1547424343.jpg
SPEC = Vehicle(
    name='gwr-armstrong-standard-goods',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1866,
    intro_month=11,
    retire_year=1883,
    retire_month=7,
    speed=85,
    length=4,
    weight=30.2,
    axle_load=11,
    power=192,
    tractive_effort=59,
    brake_force=0,
    payload=0,
    cost=14001450,
    runningcost=211,
    fixed_cost=28050,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined'],
    blend='trains/Locomotives/gwr-armstrong-goods-churchward.blend',
    upstream_dat='trains/gwr-armstrong-standard-goods.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
