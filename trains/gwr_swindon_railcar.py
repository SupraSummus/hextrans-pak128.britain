"""gwr-swindon-railcar."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='gwr-swindon-railcar',
    waytype='track',
    copyright='Kieron/JamesPetts',
    freight='Passagiere',
    engine_type='diesel',
    intro_year=1940,
    intro_month=6,
    retire_year=1951,
    retire_month=12,
    speed=112,
    length=11,
    weight=33.1,
    axles=4,
    power=154,
    gear=50,
    tractive_effort=28,
    payload=62,
    min_loading_time=25,
    max_loading_time=90,
    overcrowded_capacity=33,
    cost=2176000,
    runningcost=161,
    fixed_cost=8270,
    bidirectional=0,
    can_lead_from_rear=1,
    smoke='Diesel',
    sound='laurie-gwr-railcar.wav',
    payload_by_class=[0, 62],
    comfort_by_class=[0, 115],
    liverytype=['GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early', 'BR-Revised'],
    blend='trains/Railcars/gwr-swindon-railcar-br-revised.blend',
    upstream_dat='trains/gwr-swindon-railcar.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
