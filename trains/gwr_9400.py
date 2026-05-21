"""gwr-9400."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gwr-9400',
    waytype='track',
    copyright='JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1947,
    intro_month=2,
    retire_year=1956,
    retire_month=12,
    speed=95,
    length=6,
    weight=56.2,
    axle_load=19,
    power=274,
    tractive_effort=100,
    payload=0,
    cost=3187800,
    runningcost=130,
    fixed_cost=23679,
    increase_maintenance_after_years=6,
    years_before_maintenance_max_reached=15,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-hawksworth', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/gwr-9400-austerity-br.blend',
    upstream_dat='trains/gwr-9400.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
