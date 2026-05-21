"""lnwr-waterloo."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Extrapolated from the "Jumbo" class based on 6'0 drivers
# instead of 6'9 drivers.
_BLEND = 'trains/Locomotives/lnwr-waterloo-lms.blend'
_UPSTREAM_DAT = 'trains/lnwr-waterloo.dat'

SPECS = [
    Vehicle(
        name='LNWR-Waterloo',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1889,
        intro_month=2,
        retire_year=1896,
        retire_month=12,
        speed=130,
        length=5,
        weight=41,
        axle_load=12,
        power=216,
        tractive_effort=55,
        payload=0,
        cost=10020000,
        runningcost=147,
        fixed_cost=32350,
        upgrade_price=1045500,
        increase_maintenance_after_years=35,
        years_before_maintenance_max_reached=25,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LNWR-Waterloo-Tender'],
        liverytype=['LNWR-Black', 'LMS-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LNWR-Waterloo-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1889,
        intro_month=2,
        retire_year=1896,
        retire_month=12,
        speed=130,
        length=3,
        weight=25,
        axles=3,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        increase_maintenance_after_years=35,
        years_before_maintenance_max_reached=25,
        constraint_prev=['LNWR-Waterloo'],
        liverytype=['LNWR-Black', 'LMS-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
