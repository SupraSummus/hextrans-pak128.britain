"""gnr-k3."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.lner.info/locos/K/k3k5.php
# NOTE: All locomotives grouped into the LNER are given their LNER class numbers in Pak328.Britain-Ex
_BLEND = 'trains/Locomotives/gnr-k3-tender-lner.blend'
_UPSTREAM_DAT = 'trains/gnr-k3.dat'

SPECS = [
    Vehicle(
        name='gnr-k3',
        waytype='track',
        copyright='Kieron&jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1920,
        intro_month=1,
        retire_year=1937,
        retire_month=4,
        speed=123,
        length=6,
        weight=72.8,
        axle_load=20,
        power=364,
        tractive_effort=104,
        payload=0,
        cost=7715158,
        runningcost=166,
        fixed_cost=27004,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['gnr-k3-tender'],
        liverytype=['GNR-Standard', 'LNER-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gnr-k3-tender',
        waytype='track',
        copyright='Kieron/jamespetts',
        freight='None',
        intro_year=1920,
        intro_month=1,
        retire_year=1937,
        retire_month=4,
        speed=123,
        length=4,
        weight=43.8,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['gnr-k3'],
        liverytype=['GNR-Standard', 'LNER-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
