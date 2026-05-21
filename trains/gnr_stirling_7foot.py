"""gnr-stirling-7foot."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Ahrons p. 168
SPEC = Vehicle(
    name='GNR-Stirling7Foot',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1868,
    intro_month=3,
    retire_year=1873,
    retire_month=7,
    speed=130,
    length=4,
    weight=34,
    axle_load=15,
    power=170,
    tractive_effort=39,
    brake_force=0,
    rolling_resistance=21,
    payload=0,
    cost=19125375,
    runningcost=212,
    fixed_cost=39938,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['gnr-sturrock-tender'],
    liverytype=['GNR-early', 'GNR-Standard'],
    blend='trains/Locomotives/gnr-stirling-7ft-single-dark.blend',
    upstream_dat='trains/gnr-stirling-7foot.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
