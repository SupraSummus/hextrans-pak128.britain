"""br-mk3-tso."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Carriages/br-mk3-co-scr.blend'
_UPSTREAM_DAT = 'trains/br-mk3-tso.dat'

SPECS = [
    Vehicle(
        name='BR-Mk3-TSO',
        waytype='track',
        copyright='Kieron/Rollmaterial',
        freight='Passagiere',
        intro_year=1976,
        intro_month=3,
        retire_year=1989,
        retire_month=11,
        speed=200,
        length=13,
        weight=36.2,
        axles=4,
        brake_force=27,
        rolling_resistance=13,
        payload=72,
        min_loading_time=30,
        max_loading_time=160,
        overcrowded_capacity=20,
        cost=590000,
        runningcost=0,
        fixed_cost=1229,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_prev=['BR-Mk3-TSO', 'BR-Mk3-TRB', 'BR-Mk3-TRFB', 'BR-Mk3-FO', 'BR-Class43', 'BR-Mk3-TRFB-pullman'],
        constraint_next=['BR-Mk3-TSO', 'BR-Mk3-TRB', 'BR-Mk3-TRFB', 'BR-Mk3-FO', 'BR-Class43Rear', 'BR-Mk3-TRFB-pullman'],
        payload_by_class=[0, 72, 0, 0],
        comfort_by_class=[0, 150, 0, 173],
        liverytype=['BR-Blue', 'IC-Executive', 'GWT', 'FGW-Green', 'Firstgroup-Mauve', 'Firstgroup-Neon', 'GNER', 'National-Express', 'GC-Original', 'GC-Daylight', 'VTEC', 'Virgin-original'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='BR-Mk3a-TSO',
        waytype='track',
        copyright='Kieron/Rollmaterial',
        freight='Passagiere',
        intro_year=1975,
        intro_month=4,
        retire_year=1989,
        retire_month=11,
        speed=200,
        length=13,
        weight=36.2,
        axles=4,
        brake_force=27,
        rolling_resistance=13,
        payload=72,
        min_loading_time=30,
        max_loading_time=160,
        overcrowded_capacity=20,
        cost=590000,
        runningcost=0,
        fixed_cost=1229,
        bidirectional=1,
        can_lead_from_rear=0,
        constraint_next=['BR-Mk3a-TSO', 'BR-Mk3-DVT', 'BR-Mk3a-TRB', 'BR-Mk3a-TRFB', 'BR-Mk3a-FO', 'BR-Mk2-DBSO', 'BR-Mk2-RFB', 'BR-Mk2-BFK', 'BR-Mk2-TSOT', 'BR-Mk2-TSO', 'BR-Mk2-FO', 'BR-Mk3a-TRFB-pullman', 'BR-Mk2-PFP', 'BR-Mk2-PFK', 'BR-Mk2-PFB', 'None'],
        payload_by_class=[0, 72, 0, 0],
        comfort_by_class=[0, 150, 0, 173],
        liverytype=['BR-Blue', 'IC-Executive', 'GWT', 'FGW-Green', 'Firstgroup-Mauve', 'Firstgroup-Neon', 'GNER', 'National-Express', 'GC-Original', 'GC-Daylight', 'Chiltern-Mainline', 'Scotrail-original', 'Virgin-original', 'One', 'NXEA', 'Abellio-Greater-Anglia'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
