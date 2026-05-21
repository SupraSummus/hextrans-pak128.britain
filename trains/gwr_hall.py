"""gwr-hall."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/gwr-hall-modified-br-revised.blend'
_UPSTREAM_DAT = 'trains/gwr-hall.dat'

SPECS = [
    Vehicle(
        name='GWR-Hall',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1928,
        intro_month=1,
        retire_year=1944,
        retire_month=2,
        speed=137,
        length=7,
        weight=76.2,
        axle_load=19,
        power=410,
        tractive_effort=121,
        payload=0,
        cost=9121000,
        runningcost=235,
        fixed_cost=31601,
        upgrade_price=1894200,
        increase_maintenance_after_years=16,
        years_before_maintenance_max_reached=13,
        smoke='Steam',
        sound='keithpeter-gwr-hall.wav',
        constraint_next=['GWR-Hall-Tender'],
        liverytype=['GWR-chocolate-cream-lined', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
        upgrade=['GWR-Modified-Hall'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='GWR-Hall-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1928,
        intro_month=1,
        retire_year=1944,
        retire_month=2,
        speed=137,
        length=4,
        weight=47,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=16,
        years_before_maintenance_max_reached=13,
        constraint_prev=['GWR-Hall'],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
