"""gwr-grange."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/gwr-grange-br-revised.blend'
_UPSTREAM_DAT = 'trains/gwr-grange.dat'

SPECS = [
    Vehicle(
        name='gwr-grange',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1936,
        intro_month=8,
        retire_year=1950,
        retire_month=3,
        speed=126,
        length=7,
        weight=75.2,
        axle_load=19,
        power=411,
        tractive_effort=128,
        payload=0,
        cost=9121000,
        runningcost=235,
        fixed_cost=31600,
        increase_maintenance_after_years=15,
        years_before_maintenance_max_reached=13,
        smoke='Steam',
        sound='keithpeter-gwr-hall.wav',
        constraint_next=['gwr-grange-tender'],
        liverytype=['GWR-chocolate-cream-lined', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gwr-grange-tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1936,
        intro_month=8,
        retire_year=1950,
        retire_month=3,
        speed=137,
        length=4,
        weight=47,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=15,
        years_before_maintenance_max_reached=13,
        constraint_prev=['gwr-grange'],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
