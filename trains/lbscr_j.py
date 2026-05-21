"""lbscr-j."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LBSCR-J',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1910,
    intro_month=12,
    retire_year=1917,
    retire_month=6,
    speed=130,
    length=8,
    weight=86,
    axle_load=17,
    power=398,
    tractive_effort=84,
    payload=0,
    cost=7143100,
    runningcost=152,
    fixed_cost=45953,
    increase_maintenance_after_years=25,
    years_before_maintenance_max_reached=21,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['LBSCR-Marsh', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity'],
    blend='trains/Locomotives/lbscr-J-malachite.blend',
    upstream_dat='trains/lbscr-j.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
