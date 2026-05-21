"""ner-tyne-petrol-electric-railcar."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.lner.info/locos/IC/ner_petrolelectric.php
# https://en.wikipedia.org/wiki/1903_Petrol_Electric_Autocar
# https://electricautocar.co.uk/
SPEC = Vehicle(
    name='ner-tyne-petrol-electric-railcar',
    waytype='track',
    copyright='Junna/Cake/JamesPetts',
    freight='Passagiere',
    engine_type='petrol',
    intro_year=1903,
    intro_month=5,
    retire_year=1933,
    retire_month=12,
    speed=70,
    length=10,
    weight=36.3,
    axles=4,
    power=63,
    gear=50,
    tractive_effort=18,
    payload=52,
    min_loading_time=15,
    max_loading_time=80,
    overcrowded_capacity=40,
    cost=471000,
    runningcost=65,
    fixed_cost=7200,
    bidirectional=0,
    can_lead_from_rear=1,
    constraint_prev=['none'],
    payload_by_class=[0, 52],
    comfort_by_class=[0, 69],
    liverytype=['NER-standard', 'LNER-Standard'],
    blend='trains/Railcars/ner-tyne-petrol-electric-railcar-lner.blend',
    upstream_dat='trains/ner-tyne-petrol-electric-railcar.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
