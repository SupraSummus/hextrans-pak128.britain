"""br-4mt-4-6-0."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/br-4mt-4-6-0.blend'
_UPSTREAM_DAT = 'trains/br-4mt-4-6-0.dat'

SPECS = [
    Vehicle(
        name='BR-4MT-4-6-0',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1951,
        intro_month=5,
        retire_year=1957,
        retire_month=5,
        speed=131,
        length=6,
        weight=69,
        axle_load=18,
        power=368,
        tractive_effort=114,
        rolling_resistance=13,
        payload=0,
        cost=4621000,
        runningcost=316,
        fixed_cost=27851,
        increase_maintenance_after_years=8,
        years_before_maintenance_max_reached=11,
        bidirectional=0,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['BR-4MT-Tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='BR-4MT-Tender',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        intro_year=1951,
        intro_month=4,
        retire_year=1957,
        retire_month=11,
        speed=135,
        length=4,
        weight=43,
        axle_load=17,
        power=0,
        rolling_resistance=13,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=8,
        years_before_maintenance_max_reached=11,
        constraint_prev=['BR-4MT-4-6-0', 'BR-4MT-2-6-0', 'BR-5MT'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
