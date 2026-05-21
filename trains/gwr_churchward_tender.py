"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gwr-churchward-tender',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    intro_year=1908,
    intro_month=12,
    retire_year=1946,
    retire_month=11,
    speed=160,
    length=4,
    weight=40.6,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=36,
    years_before_maintenance_max_reached=20,
    constraint_prev=['gwr-bulldog-superheated', 'gwr-city-superheated', 'gwr-duke-superheated', 'gwr-badminton-superheated', 'gwr-4300', 'gwr-aberdare-superheated'],
    liverytype=['GWR-standard-green', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gwr-churchward-tender.blend',
    upstream_dat='trains/gwr-churchward-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
