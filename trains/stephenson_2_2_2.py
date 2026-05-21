"""stephenson-2-2-2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# There are a great many very similar 2-2-2s of the late 1830s:
# see Ahrons p. 35 onwards. This is the Stephenson version, which
# appears to be a 2-2-2 version of the "Lion". Many different
# railways used this basic design (made by various manufacturers),
# with small detail differences.
SPEC = Vehicle(
    name='stephenson-2-2-2',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1838,
    intro_month=11,
    retire_year=1842,
    retire_month=2,
    speed=85,
    length=3,
    weight=12.5,
    axle_load=5,
    power=45,
    tractive_effort=6,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=22713,
    payload=0,
    cost=7400500,
    runningcost=102,
    fixed_cost=26278,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LMR-Patentee-Tender'],
    blend='trains/Locomotives/stephenson-2-2-2.blend',
    upstream_dat='trains/stephenson-2-2-2.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
