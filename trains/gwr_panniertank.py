"""GWR 5700 Class pannier tank locomotive."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Retirement date extended to allow building with auto trailers;
# revert (orig 1950/8) when more suitable engines are introduced.
# Weight + axle load: https://en.wikipedia.org/wiki/GWR_5700_Class#Variants
SPEC = Vehicle(
    name='GWR-PannierTank',
    waytype='track',
    copyright='Kieron',
    freight='None',
    engine_type='steam',
    intro_year=1929,
    intro_month=4,
    retire_year=1954,
    retire_month=9,
    speed=95,
    length=5,
    weight=48.3,
    axle_load=17,
    power=236,
    tractive_effort=100,
    payload=0,
    cost=2772000,
    runningcost=128,
    fixed_cost=26310,
    increase_maintenance_after_years=9,
    years_before_maintenance_max_reached=17,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-standard-green', 'GWR-shirtbutton', 'GWR-hawksworth',
                'WW2-Austerity', 'BR-Early', 'LT'],
    blend='trains/Locomotives/gwr-panniertank.blend',
    upstream_dat='trains/gwr-panniertank.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
