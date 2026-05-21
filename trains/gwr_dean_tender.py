"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='GWR-dean-tender',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    intro_year=1883,
    intro_month=12,
    retire_year=1930,
    retire_month=9,
    speed=160,
    length=4,
    weight=34.5,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=36,
    years_before_maintenance_max_reached=20,
    constraint_prev=['GWR-Bulldog', 'GWR-City', 'gwr-duke', 'gwr-duke-superheated', 'gwr-badminton', 'gwr-badminton-superheated', 'gwr-aberdare', 'gwr-achillies', 'gwr-barnum', 'gwr-2201', 'gwr-3232', 'gwr-river', 'gwr-stella', 'gwr-dean-goods'],
    liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
    upgrade=['gwr-churchward-tender'],
    blend='trains/Locomotives/gwr-dean-tender.blend',
    upstream_dat='trains/gwr-dean-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
