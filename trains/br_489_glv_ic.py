"""br-489-glv-ic."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-489[GLV]',
    waytype='track',
    copyright='Kieron',
    freight='Post',
    engine_type='electric',
    intro_year=1983,
    intro_month=3,
    retire_year=1990,
    retire_month=11,
    speed=145,
    length=11,
    weight=45,
    axles=4,
    power=370,
    gear=80,
    tractive_effort=45,
    rolling_resistance=13,
    payload=600,
    cost=1500000,
    runningcost=37,
    fixed_cost=10781,
    upgrade_price=600000,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='x24tohayes-epb.wav',
    constraint_prev=['BR-Mk2-TSO', 'BR-Mk2-RFB', 'BR-Mk3a-TSO', 'BR-Mk3a-TRB', 'BR-Mk3a-TRFB', 'BR-Mk2a-RMB', 'BR-Mk2a-TSO', 'BR-Mk2a-SO', 'BR-Mk1-SK', 'BR-Mk1-TSO'],
    constraint_next=['none'],
    liverytype=['IC-Executive', 'IC-Swallow'],
    way_constraint_permissive=[0],
    blend='trains/Railcars/br-489-GLV-ic-e.blend',
    upstream_dat='trains/br-489-glv-ic.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
