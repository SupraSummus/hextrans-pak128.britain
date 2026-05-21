"""gwr-517-rebuilt."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.gwr.org.uk/no4-coup-tanks.html
# This is the version as rebuilt in circa 1883
_BLEND = 'trains/Locomotives/gwr-517-rebuilt-ww1-austerity.blend'
_UPSTREAM_DAT = 'trains/gwr-517-rebuilt.dat'

SPECS = [
    Vehicle(
        name='gwr-517-rebuilt',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1883,
        intro_month=7,
        retire_year=1930,
        retire_month=10,
        speed=90,
        length=5,
        weight=35.8,
        axle_load=13,
        power=174,
        tractive_effort=66,
        payload=0,
        cost=6900000,
        runningcost=154,
        fixed_cost=29500,
        upgrade_price=1650000,
        increase_maintenance_after_years=38,
        years_before_maintenance_max_reached=20,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='konakaboom-gwr-pannier.wav',
        liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'WW2-Austerity', 'BR-Early'],
        upgrade=['gwr-517-rebuilt-auto-fitted', 'gwr-3571'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gwr-517-rebuilt-auto-fitted',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1905,
        intro_month=2,
        retire_year=1930,
        retire_month=10,
        speed=90,
        length=5,
        weight=36,
        axle_load=13,
        power=174,
        tractive_effort=66,
        payload=0,
        cost=6600000,
        runningcost=154,
        fixed_cost=17833,
        upgrade_price=94000,
        increase_maintenance_after_years=38,
        years_before_maintenance_max_reached=20,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Steam',
        sound='konakaboom-gwr-pannier.wav',
        liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
