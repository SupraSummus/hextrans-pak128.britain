"""gwr-armstrong-tender."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# This is intended to represent the Armstrong 1,800 gallon
# tender. See: http://www.gwr.org.uk/no-tenders.html
SPEC = Vehicle(
    name='gwr-armstrong-tender',
    waytype='track',
    copyright='James/JamesPetts',
    freight='None',
    intro_year=1855,
    intro_month=2,
    retire_year=1895,
    retire_month=11,
    speed=150,
    length=3,
    weight=28.7,
    axles=3,
    power=0,
    brake_force=4,
    payload=0,
    cost=0,
    runningcost=0,
    fixed_cost=0,
    constraint_prev=['gwr-2201', 'gwr-157', 'gwr-3232', 'gwr-queen', 'gwr-queen-rebuilt', 'gwr-806', 'gwr-717', 'gwr-481', 'gwr-sir-daniel', 'gwr-sharp', 'gwr-69', 'gwr-chancellor', 'gwr-57', 'gwr-79', 'gwr-131', 'gwr-322', 'gwr-armstrong-standard-goods', 'gwr-armstrong-coal-goods'],
    liverytype=['GWR-early', 'GWR-dark-green', 'GWR-standard-green', 'GWR-overall-brown', 'WW1-Austerity', 'GWR-chocolate-cream-lined'],
    blend='trains/Locomotives/gwr-armstrong-tender-ww1-austerity.blend',
    upstream_dat='trains/gwr-armstrong-tender.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
