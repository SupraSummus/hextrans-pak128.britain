"""br-cl50."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Class50',
    waytype='track',
    copyright='Kieron/JamesPetts/Rollmaterial',
    freight='None',
    engine_type='diesel',
    intro_year=1967,
    intro_month=10,
    retire_year=1973,
    retire_month=5,
    speed=160,
    length=12,
    weight=117.0,
    axles=6,
    power=2010,
    gear=50,
    tractive_effort=216,
    rolling_resistance=13,
    payload=0,
    cost=7221000,
    runningcost=1006,
    fixed_cost=15015,
    increase_maintenance_after_years=20,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='video47-class-50.wav',
    constraint_prev=['BR-Class50', 'none'],
    liverytype=['BR-Blue', 'BR-Large-Logo', 'NSE-Standard', 'NSE-Revised'],
    blend='trains/Locomotives/br-cl50-nse-standard.blend',
    upstream_dat='trains/br-cl50.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
