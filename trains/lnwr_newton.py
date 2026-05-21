"""lnwr-newton."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lnwr-newton-green.blend'
_UPSTREAM_DAT = 'trains/lnwr-newton.dat'

SPECS = [
    Vehicle(
        name='LNWR-Newton',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1866,
        intro_month=5,
        retire_year=1874,
        retire_month=2,
        speed=120,
        length=5,
        weight=29,
        axle_load=9,
        power=163,
        tractive_effort=36,
        brake_force=0,
        rolling_resistance=19,
        payload=0,
        cost=17700000,
        runningcost=198,
        fixed_cost=38750,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LNWR-Newton-Tender'],
        liverytype=['LNWR-Early', 'LNWR-Black'],
        upgrade=['LNWR-Jumbo'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LNWR-Newton-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1866,
        intro_month=5,
        retire_year=1874,
        retire_month=2,
        speed=120,
        length=3,
        weight=23,
        brake_force=8,
        rolling_resistance=19,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['LNWR-Newton'],
        liverytype=['LNWR-Early', 'LNWR-Black'],
        upgrade=['LNWR-Jumbo-Tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
