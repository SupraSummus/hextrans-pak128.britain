"""lner-a3."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Apparently the A1, A3 and A4 have the same tender.
# Therefore graphics re-used until corridor-tender becomes necessary for range
SPEC = Vehicle(
    name='LNER-A3',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1927,
    intro_month=10,
    retire_year=1935,
    retire_month=4,
    speed=160,
    length=8,
    weight=97,
    axle_load=22,
    power=655,
    tractive_effort=146,
    way_wear_factor=133375,
    payload=0,
    cost=11818000,
    runningcost=393,
    fixed_cost=64621,
    upgrade_price=2929500,
    increase_maintenance_after_years=23,
    years_before_maintenance_max_reached=11,
    smoke='Steam',
    sound='the-mart-ban-lner-a4.wav',
    constraint_next=['LNER-A1-Tender'],
    liverytype=['LNER-Standard', 'WW2-Austerity', 'BR-Early', 'BR-Green'],
    blend='trains/Locomotives/lner-a3-brgreen.blend',
    upstream_dat='trains/lner-a3.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
