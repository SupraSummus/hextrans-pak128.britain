"""lnwr-precedent."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lnwr-precedent.blend'
_UPSTREAM_DAT = 'trains/lnwr-precedent.dat'

SPECS = [
    Vehicle(
        name='LNWR-Precedent',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1874,
        intro_month=12,
        retire_year=1887,
        retire_month=9,
        speed=130,
        length=4,
        weight=33,
        axle_load=12,
        power=232,
        tractive_effort=44,
        brake_force=0,
        payload=0,
        cost=13531500,
        runningcost=206,
        fixed_cost=35276,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LNWR-Precedent-Tender'],
        upgrade=['LNWR-Jumbo'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LNWR-Precedent-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1874,
        intro_month=3,
        retire_year=1887,
        retire_month=9,
        speed=130,
        length=3,
        weight=23,
        axles=3,
        brake_force=8,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['LNWR-Precedent', 'LNWR-precursor-webb'],
        upgrade=['LNWR-Jumbo-Tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
