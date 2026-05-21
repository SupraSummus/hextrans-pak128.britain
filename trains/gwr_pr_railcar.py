"""gwr-pr-railcar."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='GWR-ParkRoyal-Railcar',
    waytype='track',
    copyright='Kieron',
    freight='Passagiere',
    engine_type='diesel',
    intro_year=1933,
    intro_month=12,
    retire_year=1937,
    retire_month=4,
    speed=100,
    length=12,
    weight=24,
    axles=4,
    power=195,
    gear=50,
    tractive_effort=32,
    payload=69,
    min_loading_time=20,
    max_loading_time=90,
    overcrowded_capacity=41,
    cost=4032000,
    runningcost=196,
    fixed_cost=14200,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='laurie-gwr-railcar.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 69],
    comfort_by_class=[0, 82],
    liverytype=['GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
    blend='trains/Railcars/gwr-pr-railcar-br.blend',
    upstream_dat='trains/gwr-pr-railcar.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
