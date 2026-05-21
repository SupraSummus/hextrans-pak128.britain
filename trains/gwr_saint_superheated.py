"""gwr-saint-superheated."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gwr-saint-superheated',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1910,
    intro_month=9,
    retire_year=1928,
    retire_month=1,
    speed=150,
    length=6,
    weight=69,
    axle_load=18,
    power=445,
    tractive_effort=108,
    payload=0,
    cost=9793020,
    runningcost=155,
    fixed_cost=48961,
    increase_maintenance_after_years=27,
    years_before_maintenance_max_reached=10,
    smoke='Steam',
    sound='keithpeter-gwr-hall.wav',
    constraint_next=['GWR-Saint-Tender'],
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    upgrade=['GWR-Hall'],
    blend='trains/Locomotives/gwr-saint.blend',
    upstream_dat='trains/gwr-saint-superheated.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
