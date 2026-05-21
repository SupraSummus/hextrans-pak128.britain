"""gwr-bulldog-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.gwr.org.uk/no440s.html
SPEC = Vehicle(
    name='gwr-bulldog-superheated',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1910,
    intro_month=9,
    retire_year=1926,
    retire_month=12,
    speed=127,
    length=5,
    weight=52.6,
    axle_load=18,
    power=325,
    tractive_effort=94,
    payload=0,
    cost=9273600,
    runningcost=115,
    fixed_cost=31728,
    upgrade_price=2156655,
    increase_maintenance_after_years=36,
    years_before_maintenance_max_reached=20,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-churchward-tender'],
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gwr-bulldog.blend',
    upstream_dat='trains/gwr-bulldog-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
