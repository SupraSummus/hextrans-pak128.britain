"""gwr-gloucester-parcel-railcar."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='GWR-Gloucester-Parcel-Railcar',
    waytype='track',
    copyright='Kieron',
    freight='Post',
    engine_type='diesel',
    intro_year=1935,
    intro_month=7,
    retire_year=1941,
    retire_month=1,
    speed=130,
    length=12,
    weight=29,
    axles=4,
    power=195,
    gear=50,
    tractive_effort=30,
    payload=500,
    min_loading_time=35,
    max_loading_time=120,
    cost=3200000,
    runningcost=196,
    fixed_cost=13333,
    increase_maintenance_after_years=22,
    bidirectional=1,
    can_lead_from_rear=1,
    smoke='Diesel',
    sound='laurie-gwr-railcar.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    liverytype=['GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
    blend='trains/Railcars/gwr-gloucester-parcel-railcar-br.blend',
    upstream_dat='trains/gwr-gloucester-parcel-railcar.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
