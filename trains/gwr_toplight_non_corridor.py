"""gwr-toplight-non-corridor."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See "Great Western Coaches from 1890" by Michael Harris at p. 69 for details.
# 5 aside in the thirds and 4 aside in the firsts
# https://www.warwickshirerailways.com/gwr/gwrms1730.htm
# Not clear whether any toplight non-corridor carriages had any second class compartments: probably not.
_BLEND = 'trains/Carriages/gwr-toplight-non-corridor-collett.blend'
_UPSTREAM_DAT = 'trains/gwr-toplight-non-corridor.dat'

SPECS = [
    Vehicle(
        name='gwr-toplight-non-corridor-composite',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1908,
        intro_month=2,
        retire_year=1925,
        retire_month=5,
        speed=160,
        length=10,
        weight=27.0,
        axles=4,
        payload=50,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=25,
        cost=450200,
        runningcost=0,
        fixed_cost=725,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-front', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-front', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-front', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-front', 'gwr-toplight-non-corridor-composite', 'gwr-toplight-brake-third-front', 'gwr-clerestory-suburban-third', 'gwr-clerestory-suburban-second', 'gwr-clerestory-suburban-first', 'gwr-clerestory-suburban-brake-third-front'],
        constraint_next=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-rear', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-rear', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-rear', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-rear', 'gwr-toplight-non-corridor-composite', 'gwr-toplight-brake-third-rear', 'gwr-clerestory-suburban-third', 'gwr-clerestory-suburban-second', 'gwr-clerestory-suburban-first', 'gwr-clerestory-suburban-brake-third-rear'],
        payload_by_class=[0, 50, 0, 32],
        comfort_by_class=[0, 72, 72, 84],
        liverytype=['GWR-two-tone', 'GWR-overall-brown', 'GWR-lake', 'ww1-austerity', 'GWR-chocolate-cream-lined', 'GWR-chocolate-cream-plain', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gwr-toplight-brake-third-front',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1908,
        intro_month=2,
        retire_year=1925,
        retire_month=5,
        speed=160,
        length=10,
        weight=26.4,
        axles=4,
        payload=50,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=25,
        cost=450000,
        runningcost=0,
        fixed_cost=725,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-rear', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-rear', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-rear', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-rear', 'gwr-toplight-non-corridor-composite', 'gwr-toplight-brake-third-rear', 'gwr-clerestory-suburban-third', 'gwr-clerestory-suburban-second', 'gwr-clerestory-suburban-first', 'gwr-clerestory-suburban-brake-third-rear', 'none'],
        payload_by_class=[0, 50, 0, 0],
        comfort_by_class=[0, 72, 72, 84],
        liverytype=['GWR-two-tone', 'GWR-overall-brown', 'GWR-lake', 'ww1-austerity', 'GWR-chocolate-cream-lined', 'GWR-chocolate-cream-plain', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gwr-toplight-brake-third-rear',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1908,
        intro_month=2,
        retire_year=1925,
        retire_month=5,
        speed=160,
        length=10,
        weight=26.4,
        axles=4,
        payload=50,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=25,
        cost=450000,
        runningcost=0,
        fixed_cost=5652,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-front', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-front', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-front', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-front', 'gwr-toplight-non-corridor-composite', 'gwr-toplight-brake-third-front', 'gwr-clerestory-suburban-third', 'gwr-clerestory-suburban-second', 'gwr-clerestory-suburban-first', 'gwr-clerestory-suburban-brake-third-front'],
        payload_by_class=[0, 50, 0, 0],
        comfort_by_class=[0, 72, 72, 84],
        liverytype=['GWR-two-tone', 'GWR-overall-brown', 'GWR-lake', 'ww1-austerity', 'GWR-chocolate-cream-lined', 'GWR-chocolate-cream-plain', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
