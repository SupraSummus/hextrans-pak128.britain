"""gwr-castle."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/gwr-castle-austerity.blend'
_UPSTREAM_DAT = 'trains/gwr-castle.dat'

SPECS = [
    Vehicle(
        name='GWR-Castle',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1923,
        intro_month=8,
        retire_year=1950,
        retire_month=10,
        speed=155,
        length=6,
        weight=81.1,
        axle_load=20,
        power=458,
        tractive_effort=141,
        way_wear_factor=106444,
        payload=0,
        cost=10975250,
        runningcost=263,
        fixed_cost=49146,
        upgrade_price=2195050,
        increase_maintenance_after_years=8,
        years_before_maintenance_max_reached=9,
        smoke='Steam',
        sound='keithpeter-gwr-hall.wav',
        constraint_next=['GWR-Castle-Tender'],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='GWR-Castle-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        intro_year=1923,
        intro_month=8,
        retire_year=1950,
        retire_month=10,
        speed=155,
        length=4,
        weight=47,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=8,
        years_before_maintenance_max_reached=9,
        constraint_prev=['GWR-Castle'],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
