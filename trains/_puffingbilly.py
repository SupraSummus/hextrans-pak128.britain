"""puffingbilly."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='PuffingBilly',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1813,
    intro_month=10,
    retire_year=1815,
    retire_month=8,
    speed=10,
    length=2,
    weight=9.1,
    axles=2,
    power=8,
    tractive_effort=1,
    brake_force=0,
    rolling_resistance=19,
    way_wear_factor=21044,
    payload=0,
    cost=924000,
    runningcost=40,
    fixed_cost=17283,
    increase_maintenance_after_years=42,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['PuffingBilly-Tender'],
    blend='trains/Locomotives/puffingbilly.blend',
    upstream_dat='trains/puffingbilly.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
