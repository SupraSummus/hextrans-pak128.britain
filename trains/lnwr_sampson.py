"""lnwr-sampson."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Data based on the LNWR Newton class,
# adjusted for 6'0 driving wheels.
# Dates from: http://www.lnwrs.org.uk/Glossary/locoClasss.php
_BLEND = 'trains/Locomotives/lnwr-sampson-green.blend'
_UPSTREAM_DAT = 'trains/lnwr-sampson.dat'

SPECS = [
    Vehicle(
        name='LNWR-Sampson',
        waytype='track',
        copyright='James/jamespetts',
        freight='None',
        engine_type='steam',
        intro_year=1863,
        intro_month=4,
        retire_year=1879,
        retire_month=7,
        speed=110,
        length=5,
        weight=28,
        axle_load=12,
        power=174,
        tractive_effort=39,
        brake_force=0,
        rolling_resistance=19,
        payload=0,
        cost=17600000,
        runningcost=211,
        fixed_cost=38667,
        smoke='Steam',
        sound='lwalker-br-4mt-tank.wav',
        constraint_next=['LNWR-Sampson-Tender'],
        liverytype=['LNWR-Early', 'LNWR-Black'],
        upgrade=['LNWR-Waterloo'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LNWR-Sampson-Tender',
        waytype='track',
        copyright='James',
        freight='None',
        engine_type='steam',
        intro_year=1863,
        intro_month=4,
        retire_year=1879,
        retire_month=7,
        speed=110,
        length=3,
        weight=23,
        brake_force=8,
        rolling_resistance=19,
        payload=0,
        cost=0,
        runningcost=0,
        fixed_cost=0,
        constraint_prev=['LNWR-Sampson'],
        liverytype=['LNWR-Early', 'LNWR-Black'],
        upgrade=['LNWR-Waterloo-Tender'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
