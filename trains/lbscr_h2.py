"""lbscr-h2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-H2',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1911,
    intro_month=6,
    retire_year=1916,
    retire_month=10,
    speed=150,
    length=6,
    weight=68,
    axle_load=19,
    power=438,
    tractive_effort=92,
    payload=0,
    cost=9070100,
    runningcost=173,
    fixed_cost=47558,
    increase_maintenance_after_years=28,
    years_before_maintenance_max_reached=25,
    smoke='Steam',
    sound='konakaboom-black-five.wav',
    constraint_next=['LBSCR-H1-Tender'],
    liverytype=['LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lbscr-h2-malachite.blend',
    upstream_dat='trains/lbscr-h2.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
