"""stagecoach-rail."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See "A short history of the railway carriage", R. W. Kidner, p. 82
# This is intended for horse haulage only.
# https://ebid.s3.amazonaws.com/upload_big/3/0/0/uo_1465540541-6780-23.jpg
SPEC = Vehicle(
    name='stagecoach-rail',
    waytype='track',
    copyright='JamesPetts',
    freight='Passagiere',
    intro_year=1826,
    intro_month=3,
    retire_year=1850,
    retire_month=1,
    speed=20,
    length=3,
    weight=1.6,
    axle_load=1,
    axles=2,
    brake_force=1,
    rolling_resistance=19,
    payload=6,
    min_loading_time=300,
    max_loading_time=600,
    overcrowded_capacity=0,
    cost=101000,
    runningcost=0,
    fixed_cost=4842,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['rail-horse-friesian-single', 'rail-horse-cleveland-bay-single', 'rail-horse-yorkshire-coach-single', 'rail-horse-shire-single', 'rail-horse-irish-draught-single', 'rail-horse-clydesdale-single'],
    constraint_next=['none'],
    payload_by_class=[0, 0, 6, 4],
    comfort_by_class=[0, 0, 18, 53],
    blend='trains/Carriages/stagecoach-rail.blend',
    upstream_dat='trains/stagecoach-rail.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
