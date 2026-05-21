"""gwr-hall-modified."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/gwr-hall-modified-br-revised.blend'
_UPSTREAM_DAT = 'trains/gwr-hall-modified.dat'

SPECS = [
    Vehicle(
        name='GWR-Modified-Hall',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1944,
        intro_month=1,
        retire_year=1950,
        retire_month=9,
        speed=137,
        length=7,
        weight=77,
        axle_load=19,
        power=376,
        tractive_effort=121,
        payload=0,
        cost=9895000,
        runningcost=270,
        fixed_cost=32246,
        upgrade_price=81400,
        increase_maintenance_after_years=9,
        years_before_maintenance_max_reached=18,
        smoke='Steam',
        sound='keithpeter-gwr-hall.wav',
        constraint_next=['GWR-Modified-Hall-Tender'],
        liverytype=['GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='GWR-Modified-Hall-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1944,
        intro_month=1,
        retire_year=1950,
        retire_month=9,
        speed=137,
        length=4,
        weight=48.1,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=9,
        years_before_maintenance_max_reached=18,
        constraint_prev=['GWR-Modified-Hall'],
        liverytype=['GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
