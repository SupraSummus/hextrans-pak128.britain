"""wagon-brake-br."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://rail.wikia.com/wiki/British_Railways_Standard_Brake_Van
SPEC = Vehicle(
    name='BrakeBR',
    waytype='track',
    copyright='James',
    freight='Bucher',
    intro_year=1950,
    intro_month=4,
    retire_year=1984,
    retire_month=2,
    speed=120,
    length=3,
    weight=20.5,
    brake_force=7,
    rolling_resistance=18,
    payload=0,
    cost=150000,
    runningcost=0,
    fixed_cost=4720,
    bidirectional=1,
    blend='trains/Wagons/brake-br.blend',
    upstream_dat='trains/wagon-brake-br.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
