"""vulcan."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Ahrons, p. 24 and
# http://www.steamlocomotive.com/locobase.php?country=Great_Britain&wheel=0-6-0&railroad=ls
# http://enuii.com/vulcan_foundry/photographs/Drawings/no%2010%20leicester%20&%20swannington%20%27Vulcan%27%201835.jpg
SPEC = Vehicle(
    name='vulcan',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1834,
    intro_month=2,
    retire_year=1848,
    retire_month=8,
    speed=44,
    length=4,
    weight=17.2,
    axle_load=6,
    power=54,
    tractive_effort=11,
    brake_force=0,
    rolling_resistance=19,
    payload=0,
    cost=6790000,
    runningcost=122,
    fixed_cost=25431,
    smoke='Steam',
    sound='lwalker-br-4mt-tank.wav',
    constraint_next=['LMR-Planet-Tender'],
    blend='trains/Locomotives/vulcan.blend',
    upstream_dat='trains/vulcan.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
