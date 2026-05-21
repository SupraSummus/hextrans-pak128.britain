"""br-mk1-sub-brake."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Carriages/br-mk1-sub-brake-crimson.blend'
_UPSTREAM_DAT = 'trains/br-mk1-sub-brake.dat'

SPECS = [
    Vehicle(
        name='BR-Mk1-Sub-Brake-rear',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        intro_year=1952,
        intro_month=10,
        retire_year=1969,
        retire_month=3,
        speed=140,
        length=10,
        weight=29.4,
        axles=4,
        payload=72,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=36,
        cost=431000,
        runningcost=0,
        fixed_cost=5313,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['BR-Mk1-Sub-Brake-front', 'BR-Mk1-Sub', 'LMS-non-cor-lav', 'LMS-non-cor-non-lav', 'LMS-non-cor-brake-front', 'LMS-non-cor-brake-lav-front', 'MR-50ft-arc-lav-d1060', 'MR-54ft-eliptical-cor-d1047', 'MR-54ft-eliptical-non-lav-brake-front-d1246', 'BR-Mk1-Sub-cl'],
        payload_by_class=[0, 72],
        comfort_by_class=[0, 76],
        liverytype=['BR-Early', 'BR-Revised', 'BR-Blue'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='BR-Mk1-Sub-Brake-front',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        intro_year=1952,
        intro_month=10,
        retire_year=1969,
        retire_month=3,
        speed=140,
        length=10,
        weight=29.4,
        axles=4,
        payload=72,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=36,
        cost=431000,
        runningcost=0,
        fixed_cost=5313,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['BR-Mk1-Sub-Brake-rear', 'BR-Mk1-Sub', 'LMS-non-cor-lav', 'LMS-non-cor-non-lav', 'LMS-non-cor-brake-rear', 'LMS-non-cor-brake-lav-rear', 'MR-50ft-arc-lav-d1060', 'MR-54ft-eliptical-cor-d1047', 'MR-54ft-eliptical-non-lav-brake-rear-d1246', 'BR-Mk1-Sub-cl', 'none'],
        payload_by_class=[0, 72],
        comfort_by_class=[0, 76],
        liverytype=['BR-Early', 'BR-Revised', 'BR-Blue'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
