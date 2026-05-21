"""br-mk1-bsk."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Carriages/br-mk1-bsk-nse.blend'
_UPSTREAM_DAT = 'trains/br-mk1-bsk.dat'

SPECS = [
    Vehicle(
        name='BR-Mk1-BSK-front',
        waytype='track',
        copyright='Kieron',
        freight='Passagiere',
        intro_year=1951,
        intro_month=2,
        retire_year=1963,
        retire_month=8,
        speed=160,
        length=11,
        weight=36,
        axles=4,
        payload=24,
        min_loading_time=25,
        max_loading_time=120,
        overcrowded_capacity=22,
        cost=595000,
        runningcost=0,
        fixed_cost=708,
        increase_maintenance_after_years=34,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['BR-Mk1-GUV', 'BR-Mk1-SK', 'BR-Mk1-TSO', 'BR-Mk1-BSK-rear', 'BR-Mk1-BSO-rear', 'BR-Mk1-BG', 'BR-Mk1-RB', 'BR-Mk1-RMB', 'BR-Mk2a-RMB', 'BR-Mk2a-BSO', 'BR-Mk2a-TSO', 'BR-Mk2a-SO', 'BR-Mk2-TSO', 'BR-Mk2-RFB', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Buffet', 'BR-Mk1-BFK-rear', 'BR-Mk1-CK', 'BR-Mk1-FK', 'BR-Mk1-FO', 'BR-Mk2a-FK', 'BR-Mk2a-BFK', 'BR-Mk2-FO', 'BR-Mk1-FK', 'BR-Mk2-PFP', 'BR-Mk2-PFK', 'BR-Mk2-PFB', 'BR-Mk1-PFK', 'BR-Mk1-PSP', 'BR-Mk1-PFP', 'pullman-1951-kitchen-first', 'none'],
        payload_by_class=[0, 24, 0, 0],
        comfort_by_class=[0, 144, 0, 157],
        liverytype=['BR-Early', 'BR-Revised', 'BR-Blue', 'IC-Executive', 'NSE-Standard', 'Regional-Railways-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='BR-Mk1-BSK-rear',
        waytype='track',
        copyright='Kieron',
        freight='Passagiere',
        intro_year=1951,
        intro_month=2,
        retire_year=1963,
        retire_month=8,
        speed=160,
        length=11,
        weight=36,
        axles=4,
        payload=24,
        min_loading_time=25,
        max_loading_time=120,
        overcrowded_capacity=22,
        cost=595000,
        runningcost=0,
        fixed_cost=708,
        increase_maintenance_after_years=34,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['BR-Mk1-GUV', 'BR-Mk1-SK', 'BR-Mk1-TSO', 'BR-Mk1-BSK-front', 'BR-Mk1-BSO-front', 'BR-Mk1-BG', 'BR-Mk1-RB', 'BR-Mk1-RMB', 'BR-Mk2a-RMB', 'BR-Mk2a-BSO', 'BR-Mk2a-TSO', 'BR-Mk2a-SO', 'BR-Mk2-TSO', 'BR-Mk2-RFB', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Buffet', 'BR-Mk1-BFK-front', 'BR-Mk1-CK', 'BR-Mk1-FK', 'BR-Mk1-FO', 'BR-Mk2a-FK', 'BR-Mk2a-BFK', 'BR-Mk2-FO', 'BR-Mk1-FK', 'BR-Mk2-PFP', 'BR-Mk2-PFK', 'BR-Mk2-PFB', 'BR-Mk1-PFK', 'BR-Mk1-PSP', 'BR-Mk1-PFP', 'pullman-1951-kitchen-first'],
        payload_by_class=[0, 24, 0, 0],
        comfort_by_class=[0, 144, 0, 157],
        liverytype=['BR-Early', 'BR-Revised', 'BR-Blue', 'IC-Executive', 'NSE-Standard', 'Regional-Railways-Standard'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
