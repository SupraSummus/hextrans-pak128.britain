"""gnr-a-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Ahrons pp. 171-2
SPEC = Vehicle(
    name='gnr-a-class',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1867,
    intro_month=3,
    retire_year=1885,
    retire_month=7,
    speed=100,
    length=4,
    weight=32.8,
    axle_load=13,
    power=170,
    tractive_effort=56,
    brake_force=0,
    rolling_resistance=19,
    payload=0,
    cost=12423000,
    runningcost=206,
    fixed_cost=34353,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['gnr-sturrock-tender'],
    liverytype=['GNR-early', 'GNR-Standard'],
    blend='trains/Locomotives/gnr-a-class-dark.blend',
    upstream_dat='trains/gnr-a-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
