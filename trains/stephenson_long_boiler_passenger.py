"""stephenson-long-boiler-passenger."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Ahrons p. 58
_BLEND = 'trains/Locomotives/stephenson-long-boiler-passenger-mr-green.blend'
_UPSTREAM_DAT = 'trains/stephenson-long-boiler-passenger.dat'

SPECS = [
    Vehicle(
        name='stephenson-long-boiler-passenger',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1845,
        intro_month=11,
        retire_year=1849,
        retire_month=10,
        speed=81,
        length=4,
        weight=21.7,
        axles=3,
        power=76,
        tractive_effort=16,
        brake_force=0,
        rolling_resistance=19,
        payload=0,
        cost=15400000,
        runningcost=126,
        fixed_cost=45389,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['stephenson-long-boiler-passenger-tender'],
        liverytype=['MR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='stephenson-long-boiler-passenger-tender',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1845,
        intro_month=11,
        retire_year=1849,
        retire_month=10,
        speed=81,
        length=3,
        weight=14,
        brake_force=3,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['stephenson-long-boiler-passenger'],
        liverytype=['MR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
