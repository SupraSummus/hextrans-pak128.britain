"""sr-cc."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='SR-CC',
    waytype='track',
    copyright='Kieron/JamesPetts',
    engine_type='electric',
    intro_year=1941,
    intro_month=12,
    retire_year=1958,
    retire_month=6,
    speed=120,
    length=9,
    weight=101,
    axles=6,
    power=1100,
    gear=80,
    tractive_effort=178,
    payload=0,
    cost=3459100,
    runningcost=220,
    fixed_cost=12402,
    increase_maintenance_after_years=18,
    bidirectional=1,
    can_lead_from_rear=0,
    sound='x24tohayes-epb.wav',
    constraint_prev=['none'],
    liverytype=['SR-Malachite-Green', 'BR-Early', 'BR-Revised', 'BR-Blue'],
    way_constraint_permissive=[0],
    blend='trains/Locomotives/sr-cc-br-black.blend',
    upstream_dat='trains/sr-cc.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
