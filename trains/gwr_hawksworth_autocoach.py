"""gwr-hawksworth-autocoach."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://www.cs.rhrp.org.uk/se/CarriageInfo.asp?Ref=55
_BLEND = 'trains/Carriages/gwr-hawksworth-autocoach-br-revised.blend'
_UPSTREAM_DAT = 'trains/gwr-hawksworth-autocoach.dat'

SPECS = [
    Vehicle(
        name='gwr-hawksworth-autocoach',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1950,
        intro_month=3,
        retire_year=1954,
        retire_month=10,
        speed=100,
        length=11,
        weight=30.5,
        axles=4,
        payload=72,
        min_loading_time=20,
        max_loading_time=95,
        overcrowded_capacity=36,
        cost=820000,
        runningcost=0,
        fixed_cost=950,
        bidirectional=1,
        can_lead_from_rear=1,
        constraint_prev=['none'],
        constraint_next=['gwr-517-rebuilt-auto-fitted', 'GWR-1400Tank', 'gwr-6400', 'gwr-railmotor', 'gwr-2021-rebuilt'],
        payload_by_class=[0, 72],
        comfort_by_class=[0, 75],
        liverytype=['BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gwr-hawksworth-autocoach-rear',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1950,
        intro_month=3,
        retire_year=1954,
        retire_month=10,
        speed=100,
        length=11,
        weight=30.5,
        axles=4,
        payload=72,
        min_loading_time=20,
        max_loading_time=95,
        overcrowded_capacity=36,
        cost=820000,
        runningcost=0,
        fixed_cost=950,
        bidirectional=1,
        can_lead_from_rear=1,
        constraint_prev=['gwr-517-rebuilt-auto-fitted', 'GWR-1400Tank', 'gwr-6400', 'gwr-railmotor', 'gwr-2021-rebuilt'],
        constraint_next=['none'],
        payload_by_class=[0, 72],
        comfort_by_class=[0, 75],
        liverytype=['BR-Early', 'BR-Revised'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
