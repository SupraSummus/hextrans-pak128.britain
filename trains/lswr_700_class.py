"""lswr-700-class."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lswr-700-class-br.blend'
_UPSTREAM_DAT = 'trains/lswr-700-class.dat'

SPECS = [
    Vehicle(
        name='LSWR-700-class',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1897,
        intro_month=10,
        retire_year=1912,
        retire_month=3,
        speed=85,
        length=5,
        weight=43.4,
        axles=3,
        power=252,
        tractive_effort=100,
        payload=0,
        cost=4650000,
        runningcost=169,
        fixed_cost=27875,
        bidirectional=0,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LSWR-700-class-tender'],
        liverytype=['LSWR-royal-green', 'SR-Olive-Green', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LSWR-700-class-tender',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        intro_year=1897,
        intro_month=10,
        retire_year=1912,
        retire_month=3,
        speed=147,
        length=4,
        weight=33,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['LSWR-700-class', 'LSWR-700-class-superheated'],
        liverytype=['LSWR-royal-green', 'SR-Olive-Green', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
