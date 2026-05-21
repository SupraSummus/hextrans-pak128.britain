"""sdr-locomotion."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SDR-Locomotion',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1825,
    intro_month=9,
    retire_year=1830,
    retire_month=8,
    speed=24,
    length=3,
    weight=8.5,
    axle_load=4,
    power=10,
    tractive_effort=5,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=17638,
    payload=0,
    cost=1663200,
    runningcost=41,
    fixed_cost=18310,
    increase_maintenance_after_years=25,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['SDR-Locomotion-Tender'],
    blend='trains/Locomotives/sdr-locomotion.blend',
    upstream_dat='trains/sdr-locomotion.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
