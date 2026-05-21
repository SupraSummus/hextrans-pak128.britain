"""gwr-collett-autocoach."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.cs.rhrp.org.uk/se/CarriageInfo.asp?Ref=55
_BLEND = 'trains/Carriages/gwr-collett-autotrailer-br.blend'
_UPSTREAM_DAT = 'trains/gwr-collett-autocoach.dat'

SPECS = [
    Vehicle(
        name='gwr-collett-autotrailer',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1929,
        intro_month=8,
        retire_year=1950,
        retire_month=4,
        speed=100,
        length=11,
        weight=30.5,
        axles=4,
        payload=72,
        min_loading_time=20,
        max_loading_time=95,
        overcrowded_capacity=36,
        cost=810000,
        runningcost=0,
        fixed_cost=951,
        bidirectional=1,
        can_lead_from_rear=1,
        constraint_prev=['none'],
        constraint_next=['gwr-517-rebuilt-auto-fitted', 'GWR-1400Tank', 'gwr-6400', 'gwr-railmotor', 'gwr-2021-rebuilt'],
        payload_by_class=[0, 72],
        comfort_by_class=[0, 70],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gwr-collett-autotrailer-rear',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1929,
        intro_month=8,
        retire_year=1950,
        retire_month=4,
        speed=100,
        length=11,
        weight=30.5,
        axles=4,
        payload=72,
        min_loading_time=20,
        max_loading_time=95,
        overcrowded_capacity=36,
        cost=810000,
        runningcost=0,
        fixed_cost=951,
        bidirectional=1,
        can_lead_from_rear=1,
        constraint_prev=['gwr-517-rebuilt-auto-fitted', 'GWR-1400Tank', 'gwr-6400', 'gwr-railmotor', 'gwr-2021-rebuilt'],
        constraint_next=['none'],
        payload_by_class=[0, 72],
        comfort_by_class=[0, 75],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
