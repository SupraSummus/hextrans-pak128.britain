"""tayleur-2-2-2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# There are a great many very similar 2-2-2s of the late 1830s:
# see Ahrons p. 35 onwards. This is the Tayleur version.
# The intention of having both this and the Stephenson version
# is that this represents the slightly later developments, with
# slightly larger dimensions.
SPEC = Vehicle(
    name='tayleur-2-2-2',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1840,
    intro_month=11,
    retire_year=1848,
    retire_month=8,
    speed=85,
    length=3,
    weight=16.2,
    axle_load=7,
    power=47,
    tractive_effort=8,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=29015,
    payload=0,
    cost=8385500,
    runningcost=86,
    fixed_cost=27647,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LMR-Patentee-Tender'],
    blend='trains/Locomotives/tayleur-2-2-2.blend',
    upstream_dat='trains/tayleur-2-2-2.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
