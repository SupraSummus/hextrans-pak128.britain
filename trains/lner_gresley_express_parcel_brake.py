"""lner-gresley-express-parcel-brake."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='LNER-Gresley-Express-Parcel-Brake',
    waytype='track',
    copyright='Kieron',
    freight='Post',
    intro_year=1923,
    intro_month=5,
    retire_year=1951,
    retire_month=2,
    speed=160,
    length=10,
    weight=31,
    axles=4,
    payload=400,
    min_loading_time=25,
    max_loading_time=180,
    cost=760000,
    runningcost=0,
    fixed_cost=5117,
    increase_maintenance_after_years=15,
    years_before_maintenance_max_reached=30,
    bidirectional=1,
    can_lead_from_rear=0,
    liverytype=['LNER-Standard', 'BR-Early', 'BR-Revised'],
    blend='trains/Carriages/lner-gresley-express-parcel-brake-cc.blend',
    upstream_dat='trains/lner-gresley-express-parcel-brake.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
