"""wilberforce."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Ahrons p. 26
_BLEND = 'trains/Locomotives/wilberforce.blend'
_UPSTREAM_DAT = 'trains/wilberforce.dat'

SPECS = [
    Vehicle(
        name='wilberforce',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1831,
        intro_month=6,
        retire_year=1839,
        retire_month=2,
        speed=40,
        length=3,
        weight=11.9,
        axles=3,
        power=30,
        tractive_effort=9,
        brake_force=0,
        rolling_resistance=20,
        payload=0,
        cost=3900000,
        runningcost=36,
        fixed_cost=21417,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['wilberforce-tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='wilberforce-tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1831,
        intro_month=6,
        retire_year=1839,
        retire_month=2,
        speed=40,
        length=2,
        weight=1,
        brake_force=1,
        rolling_resistance=19,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['wilberforce'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
