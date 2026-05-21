"""gwr-69."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://en.wikipedia.org/wiki/Daniel_Gooch_standard_gauge_locomotives#69_Class
# See also Ahrons p. 113
SPEC = Vehicle(
    name='gwr-69',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    engine_type='steam',
    intro_year=1855,
    intro_month=5,
    retire_year=1862,
    retire_month=8,
    speed=112,
    length=4,
    weight=21.1,
    axle_load=13,
    power=156,
    tractive_effort=26,
    brake_force=0,
    payload=0,
    cost=11500000,
    runningcost=208,
    fixed_cost=32500,
    smoke='Steam',
    sound='nick-parry-gwr-city-class.wav',
    constraint_next=['gwr-armstrong-tender'],
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green'],
    blend='trains/Locomotives/gwr-69-dark-green.blend',
    upstream_dat='trains/gwr-69.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
