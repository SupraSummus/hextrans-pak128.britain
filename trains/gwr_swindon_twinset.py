"""gwr-swindon-twinset."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.greatwestern.org.uk/aec3.htm
_BLEND = 'trains/Railcars/gwr-swindon-twinset-br-revised.blend'
_UPSTREAM_DAT = 'trains/gwr-swindon-twinset.dat'

SPECS = [
    Vehicle(
        name='GWR-Swindon-TwinsetFront',
        waytype='track',
        copyright='Kieron',
        freight='Passagiere',
        engine_type='diesel',
        intro_year=1941,
        intro_month=11,
        retire_year=1951,
        retire_month=12,
        speed=112,
        length=11,
        weight=37.7,
        axles=4,
        power=154,
        gear=50,
        tractive_effort=28,
        payload=62,
        min_loading_time=25,
        max_loading_time=90,
        overcrowded_capacity=33,
        catering_level=2,
        cost=2184000,
        runningcost=161,
        fixed_cost=8275,
        bidirectional=0,
        can_lead_from_rear=1,
        smoke='Diesel',
        sound='laurie-gwr-railcar.wav',
        constraint_prev=['none'],
        constraint_next=['GWR-Swindon-TwinsetRear'],
        payload_by_class=[0, 62],
        comfort_by_class=[0, 115],
        liverytype=['GWR-shirtbutton', 'BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='GWR-Swindon-TwinsetRear',
        waytype='track',
        copyright='Kieron',
        freight='Passagiere',
        engine_type='diesel',
        intro_year=1941,
        intro_month=11,
        retire_year=1951,
        retire_month=12,
        speed=112,
        length=11,
        weight=37.7,
        axles=4,
        power=154,
        gear=50,
        tractive_effort=28,
        payload=42,
        min_loading_time=25,
        max_loading_time=90,
        overcrowded_capacity=23,
        cost=2184000,
        runningcost=161,
        fixed_cost=8275,
        bidirectional=0,
        can_lead_from_rear=1,
        smoke='Diesel',
        sound='laurie-gwr-railcar.wav',
        constraint_prev=['GWR-Swindon-TwinsetFront'],
        constraint_next=['none'],
        payload_by_class=[0, 42],
        comfort_by_class=[0, 115],
        liverytype=['GWR-shirtbutton', 'BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
