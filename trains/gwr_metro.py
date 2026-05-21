"""gwr-metro."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_455_Class
SPEC = Vehicle(
    name='gwr-metro',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1868,
    intro_month=10,
    retire_year=1899,
    retire_month=4,
    speed=95,
    length=5,
    weight=37.3,
    axle_load=13,
    power=189,
    tractive_effort=50,
    payload=0,
    cost=8250000,
    runningcost=270,
    fixed_cost=33500,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth'],
    blend='trains/Locomotives/gwr-metro-ww1-austerity.blend',
    upstream_dat='trains/gwr-metro.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
