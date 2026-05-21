"""gwr-5101."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_5101_Class
SPEC = Vehicle(
    name='gwr-5101',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1929,
    intro_month=10,
    retire_year=1949,
    retire_month=8,
    speed=105,
    length=7,
    weight=79.7,
    axle_load=17,
    power=317,
    tractive_effort=108,
    payload=0,
    cost=4836685,
    runningcost=105,
    fixed_cost=43456,
    upgrade_price=691200,
    increase_maintenance_after_years=12,
    years_before_maintenance_max_reached=15,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    blend='trains/Locomotives/gwr-5101-black.blend',
    upstream_dat='trains/gwr-5101.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
