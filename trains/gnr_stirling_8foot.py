"""gnr-stirling-8foot."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='GNR-Stirling8Foot',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1870,
    intro_month=3,
    retire_year=1884,
    retire_month=5,
    speed=135,
    length=5,
    weight=40,
    axle_load=15,
    power=203,
    tractive_effort=45,
    brake_force=0,
    payload=0,
    cost=19641600,
    runningcost=246,
    fixed_cost=40368,
    increase_maintenance_after_years=27,
    years_before_maintenance_max_reached=31,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['GNR-Stirling8Foot-Tender'],
    upgrade=['gnr-g2', 'gnr-g3'],
    blend='trains/Locomotives/gnr-stirling-7ft-single-dark.blend',
    upstream_dat='trains/gnr-stirling-8foot.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
