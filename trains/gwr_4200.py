"""gwr-4200."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gwr-4200',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1910,
    intro_month=4,
    retire_year=1923,
    retire_month=7,
    speed=90,
    length=7,
    weight=82.9,
    axle_load=19,
    power=336,
    tractive_effort=139,
    payload=0,
    cost=5940000,
    runningcost=120,
    fixed_cost=43650,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    liverytype=['GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
    upgrade=['gwr-5205'],
    blend='trains/Locomotives/gwr-4200-collett.blend',
    upstream_dat='trains/gwr-4200.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
