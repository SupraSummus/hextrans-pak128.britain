"""gwr-gloucester-railcar."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='GWR-Gloucester-Railcar',
    waytype='track',
    copyright='Kieron',
    freight='Passagiere',
    engine_type='diesel',
    intro_year=1935,
    intro_month=7,
    retire_year=1941,
    retire_month=1,
    speed=130,
    length=12,
    weight=30,
    axles=4,
    power=195,
    gear=50,
    tractive_effort=30,
    payload=63,
    min_loading_time=20,
    max_loading_time=90,
    overcrowded_capacity=37,
    cost=2772000,
    runningcost=196,
    fixed_cost=12888,
    increase_maintenance_after_years=22,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke='Diesel',
    sound='laurie-gwr-railcar.wav',
    constraint_prev=['none'],
    constraint_next=['none'],
    payload_by_class=[0, 63],
    comfort_by_class=[0, 83],
    liverytype=['GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
    blend='trains/Railcars/gwr-gloucester-railcar-br.blend',
    upstream_dat='trains/gwr-gloucester-railcar.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
