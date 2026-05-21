"""mr-1833."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.railpictures.net/viewphoto.php?id=268752&nseq=27
SPEC = Vehicle(
    name='MR-1833',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1875,
    intro_month=5,
    retire_year=1900,
    retire_month=4,
    speed=95,
    length=5,
    weight=44,
    axle_load=15,
    power=200,
    tractive_effort=53,
    payload=0,
    cost=5796000,
    runningcost=210,
    fixed_cost=28830,
    years_before_maintenance_max_reached=25,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    liverytype=['MR-Early', 'MR-Standard'],
    blend='trains/Locomotives/mr-1833-green.blend',
    upstream_dat='trains/mr-1833.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
