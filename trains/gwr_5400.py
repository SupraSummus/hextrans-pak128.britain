"""gwr-5400."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_5400_Class
SPEC = Vehicle(
    name='gwr-5400',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1930,
    intro_month=1,
    retire_year=1945,
    retire_month=3,
    speed=96,
    length=5,
    weight=47.3,
    axles=3,
    power=220,
    tractive_effort=66,
    payload=0,
    cost=275000,
    runningcost=135,
    fixed_cost=20000,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-standard-green', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-austerity', 'BR-Early'],
    blend='trains/Locomotives/gwr-5400-black.blend',
    upstream_dat='trains/gwr-5400.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
