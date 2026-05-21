"""gnr-h-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Ahrons p. 169
# https://www.gnrsociety.com/locomotive-class/280-series/
# These were later classified as E3
SPEC = Vehicle(
    name='gnr-h-class',
    waytype='track',
    copyright='James/jamespetts',
    freight='None',
    engine_type='steam',
    intro_year=1867,
    intro_month=10,
    retire_year=1885,
    retire_month=5,
    speed=120,
    length=4,
    weight=35.0,
    axle_load=13,
    power=170,
    tractive_effort=48,
    brake_force=0,
    rolling_resistance=19,
    payload=0,
    cost=17184000,
    runningcost=206,
    fixed_cost=38320,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['gnr-sturrock-tender'],
    liverytype=['GNR-early', 'GNR-Standard', 'LNER-Standard'],
    blend='trains/Locomotives/gnr-h-class-dark.blend',
    upstream_dat='trains/gnr-h-class.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
