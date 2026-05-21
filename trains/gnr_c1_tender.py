"""gnr-c1-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='GNR-C1-Tender',
    waytype='track',
    copyright='Kieron',
    freight='None',
    intro_year=1896,
    intro_month=1,
    retire_year=1924,
    retire_month=4,
    speed=150,
    length=4,
    weight=43.8,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=28,
    years_before_maintenance_max_reached=25,
    constraint_prev=['GNR-C1', 'GNR-Klondyke', 'GNR-C1-superheated', 'gnr-d1', 'gnr-d2', 'gnr-1321', 'gnr-e1'],
    liverytype=['GNR-Standard', 'LNER-Standard'],
    blend='trains/Locomotives/gnr-c1-tender-lner.blend',
    upstream_dat='trains/gnr-c1-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
