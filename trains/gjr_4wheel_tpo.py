"""gjr-4wheel-tpo."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See Hamilton Ellis p. 42
# https://www.flickr.com/photos/benrevell/16392817652/in/photostream/lightbox/
SPEC = Vehicle(
    name='LMR-4Wheel-TPO',
    waytype='track',
    copyright='James/jamespetts',
    freight='Post',
    intro_year=1838,
    intro_month=10,
    retire_year=1850,
    retire_month=9,
    speed=125,
    length=3,
    weight=4,
    axles=2,
    brake_force=0,
    rolling_resistance=19,
    payload=180,
    min_loading_time=35,
    max_loading_time=120,
    catering_level=1,
    cost=184000,
    runningcost=0,
    fixed_cost=24077,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['any'],
    constraint_next=['any'],
    liverytype=['LMR-Standard'],
    blend='trains/Carriages/4wheel-tpo.blend',
    upstream_dat='trains/gjr-4wheel-tpo.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
