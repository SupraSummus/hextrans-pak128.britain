"""lms-stanier-3p."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# Should be a little underpowered, but
# more economical than the Fowler 3P.
# (See Wikipedia article)
_BLEND = 'trains/Locomotives/lms-stanier-3p-br.blend'
_UPSTREAM_DAT = 'trains/lms-stanier-3p.dat'

SPECS = [
    Vehicle(
        name='LMS-Stanier-3P-Tank',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1935,
        intro_month=12,
        retire_year=1946,
        retire_month=1,
        speed=100,
        length=7,
        weight=72,
        axle_load=16,
        power=261,
        tractive_effort=96,
        payload=0,
        cost=3024049,
        runningcost=125,
        fixed_cost=26520,
        increase_maintenance_after_years=12,
        years_before_maintenance_max_reached=13,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Steam',
        liverytype=['LMS-Standard', 'BR-Early'],
        upgrade=['LMS-Stanier-3P-Tank-Push-Pull'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='LMS-Stanier-3P-Tank-Push-Pull',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='None',
        engine_type='steam',
        intro_year=1935,
        intro_month=12,
        retire_year=1946,
        retire_month=1,
        speed=110,
        length=7,
        weight=72,
        axle_load=16,
        power=151,
        tractive_effort=96,
        payload=0,
        cost=3064049,
        runningcost=76,
        fixed_cost=26553,
        upgrade_price=50000,
        increase_maintenance_after_years=12,
        years_before_maintenance_max_reached=13,
        bidirectional=1,
        can_lead_from_rear=0,
        smoke='Steam',
        liverytype=['LMS-Standard', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
