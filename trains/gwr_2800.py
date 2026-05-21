"""gwr-2800."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/gwr-2800-ww1-austerity.blend'
_UPSTREAM_DAT = 'trains/gwr-2800.dat'

SPECS = [
    Vehicle(
        name='GWR-2800',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1903,
        intro_month=6,
        retire_year=1914,
        retire_month=1,
        speed=90,
        length=6,
        weight=76.7,
        axle_load=17,
        power=382,
        tractive_effort=157,
        payload=0,
        cost=4566375,
        runningcost=164,
        fixed_cost=44950,
        smoke='Steam',
        sound='keithpeter-gwr-hall.wav',
        constraint_next=['GWR-2800-Tender'],
        liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'WW2-Austerity', 'BR-Early'],
        upgrade=['gwr-2800-superheated'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='GWR-2800-Tender',
        waytype='track',
        copyright='James/JamesPetts',
        freight='None',
        intro_year=1903,
        intro_month=6,
        retire_year=1938,
        retire_month=7,
        speed=90,
        length=4,
        weight=40.6,
        axles=3,
        power=0,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['GWR-2800', 'gwr-2800-superheated'],
        liverytype=['GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
