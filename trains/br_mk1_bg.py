"""br-mk1-bg."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Mk1-BG',
    waytype='track',
    copyright='Kieron/James',
    freight='Post',
    intro_year=1951,
    intro_month=2,
    retire_year=2003,
    retire_month=6,
    speed=177,
    length=11,
    weight=45,
    axles=4,
    payload=500,
    min_loading_time=25,
    max_loading_time=120,
    cost=583000,
    runningcost=0,
    fixed_cost=694,
    increase_maintenance_after_years=22,
    bidirectional=1,
    can_lead_from_rear=0,
    liverytype=['BR-Early', 'BR-Revised', 'BR-Blue', 'IC-Executive', 'NSE-Standard', 'Regional-Railways-Standard', 'Scotrail-original', 'RM-Early', 'RM-Revised', 'RES'],
    upgrade=['BR-499[TLV]'],
    blend='trains/Carriages/br-mk1-bg-rm-new.blend',
    upstream_dat='trains/br-mk1-bg.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
