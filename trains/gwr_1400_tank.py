"""gwr-1400-tank."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='GWR-1400Tank',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1930,
    intro_month=5,
    retire_year=1950,
    retire_month=12,
    speed=87,
    length=5,
    weight=42,
    axle_load=14,
    power=187,
    tractive_effort=62,
    way_wear_factor=66150,
    payload=0,
    cost=1372000,
    runningcost=99,
    fixed_cost=17143,
    increase_maintenance_after_years=13,
    years_before_maintenance_max_reached=10,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    blend='trains/Locomotives/gwr-1400-tank-br-green.blend',
    upstream_dat='trains/gwr-1400-tank.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
