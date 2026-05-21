"""gnr-k1."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.lner.info/locos/K/k1k2.php
# NOTE: All locomotives grouped into the LNER are given their LNER class numbers in Pak128.Britain-Ex
_BLEND = 'trains/Locomotives/gnr-k1-br.blend'
_UPSTREAM_DAT = 'trains/gnr-k1.dat'

SPECS = [
    Vehicle(
        name='gnr-k1',
        waytype='track',
        copyright='Kieron&jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1912,
        intro_month=10,
        retire_year=1921,
        retire_month=6,
        speed=120,
        length=6,
        weight=62.9,
        axle_load=18,
        power=364,
        tractive_effort=104,
        payload=0,
        cost=7013780,
        runningcost=141,
        fixed_cost=25851,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['gnr-k1-tender'],
        liverytype=['GNR-Standard', 'LNER-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gnr-k1-tender',
        waytype='track',
        copyright='Kieron/jamespetts',
        freight='None',
        intro_year=1912,
        intro_month=10,
        retire_year=1921,
        retire_month=6,
        speed=120,
        length=4,
        weight=43.8,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['gnr-k1'],
        liverytype=['GNR-Standard', 'LNER-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
