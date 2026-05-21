"""gwr-5100."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gwr-5100',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1912,
    intro_month=5,
    retire_year=1929,
    retire_month=12,
    speed=105,
    length=7,
    weight=77.4,
    axle_load=18,
    power=317,
    tractive_effort=108,
    payload=0,
    cost=4562910,
    runningcost=100,
    fixed_cost=43456,
    upgrade_price=691200,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    liverytype=['GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    upgrade=['GWR-Prairie-Tank-Modified', 'gwr-5101'],
    blend='trains/Locomotives/gwr-5100-ww1-austerity.blend',
    upstream_dat='trains/gwr-5100.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
