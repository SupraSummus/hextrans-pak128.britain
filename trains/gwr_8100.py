"""gwr-8100."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_5100_Class#8100_class
SPEC = Vehicle(
    name='gwr-8100',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1938,
    intro_month=11,
    retire_year=1949,
    retire_month=8,
    speed=95,
    length=7,
    weight=79.7,
    axle_load=17,
    power=323,
    tractive_effort=125,
    payload=0,
    cost=5900756,
    runningcost=109,
    fixed_cost=51278,
    upgrade_price=1123954,
    increase_maintenance_after_years=12,
    years_before_maintenance_max_reached=15,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    blend='trains/Locomotives/gwr-8100-black.blend',
    upstream_dat='trains/gwr-8100.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
