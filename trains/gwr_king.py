"""gwr-king."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/gwr-king-austerity.blend'
_UPSTREAM_DAT = 'trains/gwr-king.dat'

SPECS = [
    Vehicle(
        name='GWR-King',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1927,
        intro_month=8,
        retire_year=1942,
        retire_month=6,
        speed=155,
        length=7,
        weight=90.4,
        axle_load=22,
        power=622,
        tractive_effort=177,
        way_wear_factor=118650,
        payload=0,
        cost=11404800,
        runningcost=358,
        fixed_cost=63760,
        increase_maintenance_after_years=20,
        years_before_maintenance_max_reached=7,
        smoke='Steam',
        sound='keithpeter-gwr-hall.wav',
        constraint_next=['GWR-King-Tender'],
        liverytype=['GWR-chocolate-cream-plain', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Green'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='GWR-King-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1927,
        intro_month=8,
        retire_year=1942,
        retire_month=6,
        speed=155,
        length=4,
        weight=47,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=25,
        years_before_maintenance_max_reached=7,
        constraint_prev=['GWR-King'],
        liverytype=['GWR-chocolate-cream-plain', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Green'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
