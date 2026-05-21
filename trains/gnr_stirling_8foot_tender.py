"""gnr-stirling-8foot-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='GNR-Stirling8Foot-Tender',
    waytype='track',
    copyright='Kieron',
    freight='None',
    intro_year=1870,
    intro_month=3,
    retire_year=1908,
    retire_month=9,
    speed=150,
    length=4,
    weight=29,
    axles=3,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    increase_maintenance_after_years=27,
    years_before_maintenance_max_reached=31,
    constraint_prev=['GNR-Stirling8Foot', 'gnr-g1', 'gnr-g2', 'gnr-g3', 'gnr-q', 'gnr-h2-class', 'gnr-h2-class'],
    liverytype=['GNR-Standard', 'LNER-Standard'],
    blend='trains/Locomotives/gnr-stirling-7ft-single-dark.blend',
    upstream_dat='trains/gnr-stirling-8foot-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
