"""gwr-bulldog."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.gwr.org.uk/no440s.html
SPEC = Vehicle(
    name='GWR-Bulldog',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1898,
    intro_month=10,
    retire_year=1906,
    retire_month=8,
    speed=127,
    length=5,
    weight=52.6,
    axle_load=18,
    power=282,
    tractive_effort=90,
    payload=0,
    cost=9273600,
    runningcost=120,
    fixed_cost=31728,
    increase_maintenance_after_years=36,
    years_before_maintenance_max_reached=20,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['GWR-dean-tender'],
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'WW2-Austerity', 'BR-Early'],
    upgrade=['gwr-bulldog-superheated', 'gwr-city-superheated'],
    blend='trains/Locomotives/gwr-bulldog-collett-unlined.blend',
    upstream_dat='trains/gwr-bulldog.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
