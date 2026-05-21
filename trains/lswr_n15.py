"""lswr-n15."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/lswr-n15-tender-holly-green.blend'
_UPSTREAM_DAT = 'trains/lswr-n15.dat'

SPECS = [
    Vehicle(
        name='LSWR-N15',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1918,
        intro_month=8,
        retire_year=1922,
        retire_month=4,
        speed=142,
        length=6,
        weight=82,
        axle_load=19,
        power=420,
        tractive_effort=106,
        payload=0,
        cost=11486200,
        runningcost=241,
        fixed_cost=49572,
        increase_maintenance_after_years=25,
        years_before_maintenance_max_reached=14,
        smoke='Steam',
        sound='konakaboom-black-five.wav',
        constraint_next=['LSWR-N15-Tender'],
        liverytype=['LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        upgrade=['SR-N15'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LSWR-N15-Tender',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        intro_year=1918,
        intro_month=8,
        retire_year=1922,
        retire_month=4,
        speed=142,
        length=4,
        weight=57,
        axles=4,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=25,
        years_before_maintenance_max_reached=14,
        constraint_prev=['LSWR-N15'],
        liverytype=['LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
