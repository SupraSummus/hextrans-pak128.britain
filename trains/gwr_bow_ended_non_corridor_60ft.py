"""gwr-bow-ended-non-corridor-60ft."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See "Great Western Coaches from 1890" by Michael Harris at p. 89 for details,
# although few are given.
# 5 aside in the thirds and 4 aside in the firsts
_BLEND = 'trains/Carriages/gwr-bow-ended-non-corridor-60ft-br.blend'
_UPSTREAM_DAT = 'trains/gwr-bow-ended-non-corridor-60ft.dat'

SPECS = [
    Vehicle(
        name='gwr-bow-ended-non-corridor-60ft-third',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1933,
        intro_month=3,
        retire_year=1939,
        retire_month=2,
        speed=160,
        length=10,
        weight=31.1,
        axles=4,
        payload=100,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=50,
        cost=504336,
        runningcost=0,
        fixed_cost=726,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-front', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-front', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-front', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-front'],
        constraint_next=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-rear', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-rear', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-rear', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-rear'],
        payload_by_class=[0, 100, 0, 0],
        comfort_by_class=[0, 72, 72, 84],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gwr-bow-ended-non-corridor-60ft-brake-composite-front',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1933,
        intro_month=3,
        retire_year=1939,
        retire_month=2,
        speed=160,
        length=10,
        weight=30.9,
        axles=4,
        payload=50,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=25,
        cost=503200,
        runningcost=0,
        fixed_cost=726,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-rear', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-rear', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-rear', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-rear', 'none'],
        payload_by_class=[0, 50, 0, 8],
        comfort_by_class=[0, 72, 72, 84],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gwr-bow-ended-non-corridor-60ft-brake-composite-rear',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1933,
        intro_month=3,
        retire_year=1939,
        retire_month=2,
        speed=160,
        length=10,
        weight=30.9,
        axles=4,
        payload=50,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=25,
        cost=503200,
        runningcost=0,
        fixed_cost=726,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['gwr-hawksworth-non-corridor-third', 'gwr-hawksworth-non-corridor-composite', 'gwr-hawksworth-non-corridor-brake-front', 'gwr-non-cor-1930s-third', 'gwr-non-cor-1930s-first', 'gwr-non-cor-1930s-brake-front', 'gwr-bow-ended-non-corridor-composite', 'gwr-bow-ended-non-corridor-brake-third-front', 'gwr-bow-ended-non-corridor-60ft-third', 'gwr-bow-ended-non-corridor-60ft-brake-composite-front'],
        payload_by_class=[0, 50, 0, 8],
        comfort_by_class=[0, 72, 72, 84],
        liverytype=['GWR-chocolate-cream-lined', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
