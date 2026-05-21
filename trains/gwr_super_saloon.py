"""gwr-super-saloon."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# See "Great Western Coaches from 1890" by Michael Harris at pp. 84-86 for details
# Normally 2 + 1 seating (could be re-arranged). Very comfortable.
_BLEND = 'trains/Carriages/gwr-super-saloon-br.blend'
_UPSTREAM_DAT = 'trains/gwr-super-saloon.dat'

SPECS = [
    Vehicle(
        name='gwr-super-saloon',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1931,
        intro_month=7,
        retire_year=1951,
        retire_month=12,
        speed=160,
        length=10,
        weight=35.5,
        axles=4,
        payload=36,
        min_loading_time=25,
        max_loading_time=180,
        overcrowded_capacity=0,
        cost=1152112,
        runningcost=0,
        fixed_cost=6533,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['gwr-sunshine-corridor-third', 'gwr-sunshine-corridor-composite-brake-front', 'gwr-sunshine-corridor-first', 'gwr-sunshine-corridor-brake-third-front', 'gwr-sunshine-corridor-full-brake', 'gwr-hawksworth-corridor-third', 'gwr-hawksworth-corridor-composite', 'gwr-hawksworth-corridor-first', 'gwr-hawksworth-corridor-brake-front', 'gwr-hawksworth-corridor-full-brake', 'gwr-sunshine-corridor-restaurant', 'gwr-sunshine-corridor-buffet', 'gwr-super-saloon', 'gwr-super-saloon-kitchen', 'gwr-bow-ended-corridor-third', 'gwr-bow-ended-corridor-composite', 'gwr-bow-ended-corridor-brake-third-front', 'gwr-bow-ended-corridor-restaurant', 'gwr-bow-ended-corridor-buffet', 'gwr-bow-ended-corridor-full-brake', 'gwr-bow-ended-corridor-mail', 'gwr-bow-ended-corridor-tpo', 'gwr-toplight-corridor-third', 'gwr-toplight-corridor-composite', 'gwr-toplight-corridor-composite-second', 'gwr-toplight-corridor-brake-third-front', 'gwr-toplight-corridor-restaurant', 'gwr-toplight-corridor-full-brake', 'gwr-toplight-corridor-mail', 'gwr-toplight-corridor-tpo', 'gwr-clerestory-corridor-second', 'gwr-clerestory-corridor-first', 'gwr-clerestory-corridor-composite', 'gwr-clerestory-brake-third-front', 'gwr-clerestory-corridor-restaurant', 'gwr-clerestory-full-brake', 'gwr-clerestory-mail', 'gwr-clerestory-tpo'],
        constraint_next=['gwr-sunshine-corridor-third', 'gwr-sunshine-corridor-composite-brake-rear', 'gwr-sunshine-corridor-first', 'gwr-sunshine-corridor-brake-third-rear', 'gwr-sunshine-corridor-full-brake', 'gwr-hawksworth-corridor-third', 'gwr-hawksworth-corridor-composite', 'gwr-hawksworth-corridor-first', 'gwr-hawksworth-corridor-brake-rear', 'gwr-hawksworth-corridor-full-brake', 'gwr-sunshine-corridor-restaurant', 'gwr-sunshine-corridor-buffet', 'gwr-super-saloon', 'gwr-super-saloon-kitchen', 'gwr-bow-ended-corridor-third', 'gwr-bow-ended-corridor-composite', 'gwr-bow-ended-corridor-brake-third-rear', 'gwr-bow-ended-corridor-restaurant', 'gwr-bow-ended-corridor-buffet', 'gwr-bow-ended-corridor-full-brake', 'gwr-bow-ended-corridor-mail', 'gwr-bow-ended-corridor-tpo', 'gwr-toplight-corridor-third', 'gwr-toplight-corridor-composite', 'gwr-toplight-corridor-composite-second', 'gwr-toplight-corridor-brake-third-rear', 'gwr-toplight-corridor-restaurant', 'gwr-toplight-corridor-full-brake', 'gwr-toplight-corridor-mail', 'gwr-toplight-corridor-tpo', 'gwr-clerestory-corridor-second', 'gwr-clerestory-corridor-first', 'gwr-clerestory-corridor-composite', 'gwr-clerestory-brake-third-rear', 'gwr-clerestory-corridor-restaurant', 'gwr-clerestory-full-brake', 'gwr-clerestory-mail', 'gwr-clerestory-tpo'],
        payload_by_class=[0, 0, 0, 0, 36],
        comfort_by_class=[0, 0, 0, 0, 170],
        liverytype=['GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='gwr-super-saloon-kitchen',
        waytype='track',
        copyright='JamesPetts',
        freight='Passagiere',
        intro_year=1931,
        intro_month=7,
        retire_year=1951,
        retire_month=12,
        speed=160,
        length=10,
        weight=35.5,
        axles=4,
        payload=24,
        min_loading_time=25,
        max_loading_time=180,
        overcrowded_capacity=0,
        catering_level=5,
        cost=1301887,
        runningcost=0,
        fixed_cost=19599,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['gwr-sunshine-corridor-third', 'gwr-sunshine-corridor-composite-brake-front', 'gwr-sunshine-corridor-first', 'gwr-sunshine-corridor-brake-third-front', 'gwr-sunshine-corridor-full-brake', 'gwr-hawksworth-corridor-third', 'gwr-hawksworth-corridor-composite', 'gwr-hawksworth-corridor-first', 'gwr-hawksworth-corridor-brake-front', 'gwr-hawksworth-corridor-full-brake', 'gwr-sunshine-corridor-restaurant', 'gwr-sunshine-corridor-buffet', 'gwr-super-saloon', 'gwr-super-saloon-kitchen', 'gwr-bow-ended-corridor-third', 'gwr-bow-ended-corridor-composite', 'gwr-bow-ended-corridor-brake-third-front', 'gwr-bow-ended-corridor-restaurant', 'gwr-bow-ended-corridor-buffet', 'gwr-bow-ended-corridor-full-brake', 'gwr-bow-ended-corridor-mail', 'gwr-bow-ended-corridor-tpo', 'gwr-toplight-corridor-third', 'gwr-toplight-corridor-composite', 'gwr-toplight-corridor-composite-second', 'gwr-toplight-corridor-brake-third-front', 'gwr-toplight-corridor-restaurant', 'gwr-toplight-corridor-full-brake', 'gwr-toplight-corridor-mail', 'gwr-toplight-corridor-tpo', 'gwr-clerestory-corridor-second', 'gwr-clerestory-corridor-first', 'gwr-clerestory-corridor-composite', 'gwr-clerestory-brake-third-front', 'gwr-clerestory-corridor-restaurant', 'gwr-clerestory-full-brake', 'gwr-clerestory-mail', 'gwr-clerestory-tpo'],
        constraint_next=['gwr-sunshine-corridor-third', 'gwr-sunshine-corridor-composite-brake-rear', 'gwr-sunshine-corridor-first', 'gwr-sunshine-corridor-brake-third-rear', 'gwr-sunshine-corridor-full-brake', 'gwr-hawksworth-corridor-third', 'gwr-hawksworth-corridor-composite', 'gwr-hawksworth-corridor-first', 'gwr-hawksworth-corridor-brake-rear', 'gwr-hawksworth-corridor-full-brake', 'gwr-sunshine-corridor-restaurant', 'gwr-sunshine-corridor-buffet', 'gwr-super-saloon', 'gwr-super-saloon-kitchen', 'gwr-bow-ended-corridor-third', 'gwr-bow-ended-corridor-composite', 'gwr-bow-ended-corridor-brake-third-rear', 'gwr-bow-ended-corridor-restaurant', 'gwr-bow-ended-corridor-buffet', 'gwr-bow-ended-corridor-full-brake', 'gwr-bow-ended-corridor-mail', 'gwr-bow-ended-corridor-tpo', 'gwr-toplight-corridor-third', 'gwr-toplight-corridor-composite', 'gwr-toplight-corridor-composite-second', 'gwr-toplight-corridor-brake-third-rear', 'gwr-toplight-corridor-restaurant', 'gwr-toplight-corridor-full-brake', 'gwr-toplight-corridor-mail', 'gwr-toplight-corridor-tpo', 'gwr-clerestory-corridor-second', 'gwr-clerestory-corridor-first', 'gwr-clerestory-corridor-composite', 'gwr-clerestory-brake-third-rear', 'gwr-clerestory-corridor-restaurant', 'gwr-clerestory-full-brake', 'gwr-clerestory-mail', 'gwr-clerestory-tpo'],
        payload_by_class=[0, 0, 0, 0, 24],
        comfort_by_class=[0, 0, 0, 0, 170],
        liverytype=['GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
