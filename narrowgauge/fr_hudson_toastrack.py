"""autoport stub — see docs/porting.md."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='FR-hudson-toastrack',
    waytype='narrowgauge_track',
    copyright='jamespetts',
    freight='Passagiere',
    intro_year=1915,
    intro_month=4,
    retire_year=1947,
    retire_month=1,
    speed=60,
    length=4,
    weight=4.8,
    rolling_resistance=19,
    payload=32,
    min_loading_time=15,
    max_loading_time=55,
    cost=220000,
    runningcost=0,
    fixed_cost=4096,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_next=['any'],
    payload_by_class=[0, 32],
    comfort_by_class=[0, 23],
    liverytype=['FR-Royal-Purple-Cream', 'FR-Col-Stephens', 'FR-Green-Cream', 'FR-Cherry-Red', 'FR-Red-Cream'],
    blend='narrowgauge/fr-hudson-toastrack-grey.blend',
    upstream_dat='narrowgauge/fr-hudson-toastrack.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
