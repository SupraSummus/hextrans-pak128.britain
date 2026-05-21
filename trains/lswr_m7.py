"""lswr-m7."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LSWR-M7',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1897,
    intro_month=9,
    retire_year=1911,
    retire_month=7,
    speed=100,
    length=6,
    weight=61,
    axle_load=17,
    power=248,
    tractive_effort=87,
    payload=0,
    cost=4528000,
    runningcost=166,
    fixed_cost=27773,
    increase_maintenance_after_years=33,
    years_before_maintenance_max_reached=20,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lswr-m7-royal-green.blend',
    upstream_dat='trains/lswr-m7.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
