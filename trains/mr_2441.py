"""mr-2441."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://basilicafields.wordpress.com/2010/05/14/midland-locos-pt-4-johnsons-2441-class/
SPEC = Vehicle(
    name='MR-2441',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1899,
    intro_month=2,
    retire_year=1924,
    retire_month=6,
    speed=85,
    length=5,
    weight=49,
    axles=3,
    power=192,
    tractive_effort=93,
    way_wear_factor=77175,
    payload=0,
    cost=1584000,
    runningcost=128,
    fixed_cost=25320,
    increase_maintenance_after_years=30,
    years_before_maintenance_max_reached=20,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['MR-Standard', 'LMS-Standard', 'BR-Early'],
    upgrade=['LMS-3F-Jinty', 'LMS-3F-Jinty-Push-Pull', 'MR-1632'],
    blend='trains/Locomotives/mr-2441-lms.blend',
    upstream_dat='trains/mr-2441.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
