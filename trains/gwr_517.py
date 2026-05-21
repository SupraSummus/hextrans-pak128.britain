"""gwr-517."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gwr-517',
    waytype='track',
    copyright='James',
    freight='None',
    engine_type='steam',
    intro_year=1868,
    intro_month=12,
    retire_year=1883,
    retire_month=6,
    speed=90,
    length=5,
    weight=34.8,
    axle_load=12,
    power=154,
    tractive_effort=56,
    brake_force=12,
    rolling_resistance=19,
    payload=0,
    cost=6600000,
    runningcost=155,
    fixed_cost=29500,
    upgrade_price=1650000,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Steam',
    sound='konakaboom-gwr-pannier.wav',
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green'],
    upgrade=['gwr-517-rebuilt', 'gwr-3571'],
    blend='trains/Locomotives/gwr-517-rebuilt-ww1-austerity.blend',
    upstream_dat='trains/gwr-517.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
