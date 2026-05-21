"""br-mk1-rmb."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-Mk1-RMB',
    waytype='track',
    copyright='Kieron/James',
    freight='Passagiere',
    intro_year=1957,
    intro_month=1,
    retire_year=1975,
    retire_month=3,
    speed=160,
    length=11,
    weight=34,
    axles=4,
    payload=48,
    min_loading_time=25,
    max_loading_time=120,
    overcrowded_capacity=23,
    catering_level=3,
    cost=724000,
    runningcost=0,
    fixed_cost=862,
    upgrade_price=14480,
    increase_maintenance_after_years=22,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['BR-Mk1-GUV', 'BR-Mk1-SK', 'BR-Mk1-TSO', 'BR-Mk1-BSK-front', 'BR-Mk1-BSO-front', 'BR-Mk1-BG', 'BR-Mk1-RB', 'BR-Mk1-RMB', 'BR-Mk2a-RMB', 'BR-Mk2a-BSO', 'BR-Mk2a-TSO', 'BR-Mk2a-SO', 'BR-Mk2-TSO', 'BR-Mk2-RFB', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Buffet', 'BR-Mk1-BFK-front', 'BR-Mk1-CK', 'BR-Mk1-FK', 'BR-Mk1-FO', 'BR-Mk2a-FK', 'BR-Mk2a-BFK', 'BR-Mk2-FO', 'BR-Mk1-FK', 'BR-Mk2-PFP', 'BR-Mk2-PFK', 'BR-Mk2-PFB', 'BR-Mk1-PFK', 'BR-Mk1-PSP', 'BR-Mk1-PFP', 'pullman-1951-kitchen-first'],
    constraint_next=['BR-Mk1-GUV', 'BR-Mk1-SK', 'BR-Mk1-TSO', 'BR-Mk1-BSK-rear', 'BR-Mk1-BSO-rear', 'BR-Mk1-BG', 'BR-Mk1-RB', 'BR-Mk1-RMB', 'BR-Mk2a-RMB', 'BR-Mk2a-BSO', 'BR-Mk2a-TSO', 'BR-Mk2a-SO', 'BR-Mk2-TSO', 'BR-Mk2-RFB', 'LNER-Gresley-Express-Dining', 'LNER-Gresley-Express-Buffet', 'BR-Mk1-BFK-rear', 'BR-Mk1-CK', 'BR-Mk1-FK', 'BR-Mk1-FO', 'BR-Mk2a-FK', 'BR-Mk2a-BFK', 'BR-Mk2-FO', 'BR-Mk1-FK', 'BR-Mk2-PFP', 'BR-Mk2-PFK', 'BR-Mk2-PFB', 'BR-Mk1-PFK', 'BR-Mk1-PSP', 'BR-Mk1-PFP', 'pullman-1951-kitchen-first'],
    payload_by_class=[0, 48, 0, 0],
    comfort_by_class=[0, 137, 0, 155],
    liverytype=['BR-Early', 'BR-Revised', 'BR-Blue', 'IC-Executive', 'NSE-Standard', 'Regional-Railways-Standard'],
    upgrade=['BR-430[REP]Buffet', 'BR-491[TC]Buffet'],
    blend='trains/Carriages/br-mk1-rmb-jaffa.blend',
    upstream_dat='trains/br-mk1-rmb.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
