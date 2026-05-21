"""br-mk1-tpo."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Mk1-TPO',
    waytype='track',
    copyright='Kieron/James',
    freight='Post',
    intro_year=1959,
    intro_month=1,
    retire_year=2003,
    retire_month=6,
    speed=175,
    length=11,
    weight=45,
    axles=4,
    payload=450,
    min_loading_time=30,
    max_loading_time=360,
    catering_level=1,
    cost=1500000,
    runningcost=0,
    fixed_cost=24625,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_next=['BR-Mk1-POS', 'BR-Mk1-TPO', 'BR-Mk1-BG'],
    liverytype=['BR-Revised', 'RM-Early', 'RM-Revised', 'RES', 'BR-Blue'],
    blend='trains/Carriages/br-mk1-tpo-res.blend',
    upstream_dat='trains/br-mk1-tpo.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
