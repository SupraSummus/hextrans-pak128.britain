"""hawthorn-2-2-2."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# This is based on the Great North of England
# Railway's "Richmond": see Ahrons, p. 50.
# See also: http://www.steamindex.com/locotype/nerloco.htm
# Note that the latter is inconsistent with Ahrons in
# some respects.
SPEC = Vehicle(
    name='hawthorn-2-2-2',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1845,
    intro_month=5,
    retire_year=1851,
    retire_month=2,
    speed=96,
    length=3,
    weight=18.3,
    axle_load=8,
    power=66,
    tractive_effort=12,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=32823,
    payload=0,
    cost=12198750,
    runningcost=136,
    fixed_cost=32943,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LMR-Patentee-Tender'],
    blend='trains/Locomotives/hawthorn-2-2-2.blend',
    upstream_dat='trains/hawthorn-2-2-2.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
