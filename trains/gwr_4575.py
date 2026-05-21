"""gwr-4575."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/GWR_4575_Class
SPEC = Vehicle(
    name='gwr-4575',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1927,
    intro_month=3,
    retire_year=1950,
    retire_month=2,
    speed=97,
    length=6,
    weight=62.0,
    axle_load=16,
    power=257,
    tractive_effort=94,
    payload=0,
    cost=3869348,
    runningcost=92,
    fixed_cost=39115,
    increase_maintenance_after_years=12,
    years_before_maintenance_max_reached=15,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    blend='trains/Locomotives/gwr-4575-black.blend',
    upstream_dat='trains/gwr-4575.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
