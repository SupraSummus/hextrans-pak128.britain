"""gwr-saint."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/gwr-saint-collett-br-green.blend'
_UPSTREAM_DAT = 'trains/gwr-saint.dat'

SPECS = [
    Vehicle(
        name='GWR-Saint',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1902,
        intro_month=3,
        retire_year=1911,
        retire_month=2,
        speed=150,
        length=6,
        weight=69,
        axle_load=18,
        power=377,
        tractive_effort=91,
        payload=0,
        cost=9601000,
        runningcost=161,
        fixed_cost=48001,
        smoke='Steam',
        sound='keithpeter-gwr-hall.wav',
        constraint_next=['GWR-Saint-Tender'],
        liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
        upgrade=['GWR-Hall', 'gwr-saint-superheated'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='GWR-Saint-Tender',
        waytype='track',
        copyright='Kieron',
        freight='None',
        intro_year=1902,
        intro_month=3,
        retire_year=1928,
        retire_month=1,
        speed=150,
        length=4,
        weight=40.6,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=27,
        years_before_maintenance_max_reached=10,
        constraint_prev=['GWR-Saint', 'gwr-saint-superheated'],
        liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
        upgrade=['GWR-Hall-Tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
