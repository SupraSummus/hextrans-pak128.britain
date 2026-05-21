"""lswr-watercart-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# NOTE: This version is only for use with passenger and mixed traffic classes due to the livery selections.
SPEC = Vehicle(
    name='lswr-watercart-tender',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    intro_year=1899,
    intro_month=7,
    retire_year=1927,
    retire_month=5,
    speed=147,
    length=4,
    weight=49.8,
    axles=4,
    power=0,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    constraint_prev=['LSWR-T9', 'LSWR-S11', 'LSWR-L11', 'LSWR-L12', 'LSWR-T14', 'LSWR-D15', 'LSWR-T9-superheated', 'LSWR-T14-superheated', 'LSWR-S11-superheated', 'LSWR-L12-superheated', 'LSWR-D15-superheated'],
    liverytype=['LSWR-royal-green', 'LSWR-sage', 'SR-Olive-Green', 'SR-Malachite-Green', 'WW2-Austerity', 'BR-Early'],
    blend='trains/Locomotives/lswr-watercart-tender-royal-green.blend',
    upstream_dat='trains/lswr-watercart-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
