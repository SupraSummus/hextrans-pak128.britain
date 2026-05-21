"""gwr-bow-ended-non-corridor."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See "Great Western Coaches from 1890" by Michael Harris at p. 78 for details.
# 5 aside in the thirds and 4 aside in the firsts
_BLEND = 'trains/Carriages/gwr-bow-ended-non-corridor-60ft-br.blend'
_UPSTREAM_DAT = 'trains/gwr-bow-ended-non-corridor.dat'

SPECS = [
    Vehicle(
        name='gwr-bow-ended-non-corridor-composite',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1925,
        intro_month=1,
        retire_year=1937,
        retire_month=6,
        speed=160,
        length=10,
        weight=30.6,
        axles=4,
        payload=50,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=25,
        cost=450300,
        runningcost=0,
        fixed_cost=723,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-front', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-front', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-front', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-front', 'gwr-toplight-non-corridor-composite', 'gwr-toplight-brake-third-front', 'gwr-clerestory-suburban-third', 'gwr-clerestory-suburban-second', 'gwr-clerestory-suburban-first', 'gwr-clerestory-suburban-brake-third-front'],
        constraint_next=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-rear', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-rear', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-rear', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-rear', 'gwr-toplight-non-corridor-composite', 'gwr-toplight-brake-third-rear', 'gwr-clerestory-suburban-third', 'gwr-clerestory-suburban-second', 'gwr-clerestory-suburban-first', 'gwr-clerestory-suburban-brake-third-rear'],
        payload_by_class=[0, 50, 0, 32],
        comfort_by_class=[0, 72, 72, 84],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gwr-bow-ended-non-corridor-brake-third-front',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1925,
        intro_month=1,
        retire_year=1937,
        retire_month=6,
        speed=160,
        length=10,
        weight=30.0,
        axles=4,
        payload=60,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=30,
        cost=450200,
        runningcost=0,
        fixed_cost=723,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-rear', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-rear', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-rear', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-rear', 'gwr-toplight-non-corridor-composite', 'gwr-toplight-brake-third-rear', 'gwr-clerestory-suburban-third', 'gwr-clerestory-suburban-second', 'gwr-clerestory-suburban-first', 'gwr-clerestory-suburban-brake-third-rear', 'none'],
        payload_by_class=[0, 60, 0, 0],
        comfort_by_class=[0, 72, 72, 84],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gwr-bow-ended-non-corridor-brake-third-rear',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1925,
        intro_month=1,
        retire_year=1937,
        retire_month=6,
        speed=160,
        length=10,
        weight=30.0,
        axles=4,
        payload=60,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=30,
        cost=450200,
        runningcost=0,
        fixed_cost=5652,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-front', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-front', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-front', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-front', 'gwr-toplight-non-corridor-composite', 'gwr-toplight-brake-third-front', 'gwr-clerestory-suburban-third', 'gwr-clerestory-suburban-second', 'gwr-clerestory-suburban-first', 'gwr-clerestory-suburban-brake-third-front'],
        payload_by_class=[0, 60, 0, 0],
        comfort_by_class=[0, 72, 72, 84],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
