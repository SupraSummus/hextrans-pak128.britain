"""gwr-4300."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_4300_Class
SPEC = Vehicle(
    name='gwr-4300',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1911,
    intro_month=6,
    retire_year=1932,
    retire_month=11,
    speed=120,
    length=5,
    weight=63.0,
    axle_load=17,
    power=326,
    tractive_effort=114,
    payload=0,
    cost=5843826,
    runningcost=110,
    fixed_cost=43552,
    bidirectional=0,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-churchward-tender'],
    liverytype=['GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    blend='trains/Locomotives/gwr-4300-collett.blend',
    upstream_dat='trains/gwr-4300.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
