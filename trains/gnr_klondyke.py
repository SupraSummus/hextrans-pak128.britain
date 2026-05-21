"""gnr-klondyke."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='GNR-Klondyke',
    waytype='track',
    copyright='Kieron&jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1898,
    intro_month=2,
    retire_year=1903,
    retire_month=8,
    speed=145,
    length=6,
    weight=61,
    axle_load=16,
    power=314,
    tractive_effort=70,
    payload=0,
    cost=7344700,
    runningcost=210,
    fixed_cost=46121,
    increase_maintenance_after_years=28,
    years_before_maintenance_max_reached=25,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['GNR-C1-Tender'],
    liverytype=['GNR-Standard', 'LNER-Standard'],
    blend='trains/Locomotives/gnr-klondyke-lner.blend',
    upstream_dat='trains/gnr-klondyke.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
