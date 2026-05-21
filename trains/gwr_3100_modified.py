"""gwr-3100-modified."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# *Collett* 3100 class.
SPEC = Vehicle(
    name='GWR-Prairie-Tank-Modified',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1938,
    intro_month=2,
    retire_year=1951,
    retire_month=6,
    speed=95,
    length=7,
    weight=82.2,
    axle_load=20,
    power=360,
    tractive_effort=139,
    payload=0,
    cost=5312569,
    runningcost=178,
    fixed_cost=27471,
    upgrade_price=400000,
    increase_maintenance_after_years=11,
    years_before_maintenance_max_reached=11,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    liverytype=['GWR-shirtbutton', 'GWR-hawksworth', 'WW2-Austerity', 'BR-Early', 'BR-Revised'],
    blend='trains/Locomotives/gwr-3100-modified-black.blend',
    upstream_dat='trains/gwr-3100-modified.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
