"""br-cl43."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Locomotives/br-cl43-front-swallow.blend'
_UPSTREAM_DAT = 'trains/br-cl43.dat'

SPECS = [
    Vehicle(
        name='BR-Class43',
        waytype='track',
        copyright='Kieron/Rollmaterial',
        freight='Post',
        engine_type='diesel',
        intro_year=1976,
        intro_month=3,
        retire_year=1987,
        retire_month=9,
        speed=200,
        length=10,
        weight=70,
        axles=4,
        power=1678,
        gear=50,
        tractive_effort=80,
        brake_force=55,
        rolling_resistance=13,
        payload=150,
        min_loading_time=20,
        max_loading_time=50,
        cost=9331000,
        runningcost=840,
        fixed_cost=12480,
        bidirectional=0,
        can_lead_from_rear=1,
        smoke='Diesel',
        sound='sans-pareil-hst-valenta.wav',
        constraint_prev=['none'],
        constraint_next=['BR-Mk3-TSO', 'BR-Mk3-TRB', 'BR-Mk3-TRFB', 'BR-Mk3-FO', 'BR-Mk3-TRFB-pullman'],
        liverytype=['BR-Blue', 'IC-Executive', 'IC-Swallow', 'GWT', 'FGW-Green', 'Firstgroup-Mauve', 'Firstgroup-Neon', 'GNER', 'National-Express', 'GC-Original', 'GC-Daylight', 'VTEC', 'Virgin-original'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='BR-Class43Rear',
        waytype='track',
        copyright='Kieron/Rollmaterial',
        freight='Post',
        engine_type='diesel',
        intro_year=1976,
        intro_month=3,
        retire_year=1987,
        retire_month=9,
        speed=200,
        length=10,
        weight=70,
        axles=4,
        power=1678,
        gear=50,
        tractive_effort=80,
        brake_force=55,
        rolling_resistance=13,
        payload=150,
        min_loading_time=20,
        max_loading_time=50,
        cost=9331000,
        runningcost=840,
        fixed_cost=12480,
        bidirectional=0,
        can_lead_from_rear=1,
        smoke='Diesel',
        sound='x84asrd84boxy-hst-valenta.wav',
        constraint_prev=['BR-Mk3-TSO', 'BR-Mk3-TRB', 'BR-Mk3-TRFB', 'BR-Mk3-FO', 'BR-Mk3-TRFB-pullman'],
        constraint_next=['none'],
        liverytype=['BR-Blue', 'IC-Executive', 'IC-Swallow', 'GWT', 'FGW-Green', 'Firstgroup-Mauve', 'Firstgroup-Neon', 'GNER', 'National-Express', 'GC-Original', 'GC-Daylight', 'VTEC', 'Virgin-original'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
