"""br-419."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='BR-419[MLV]',
    waytype='track',
    copyright='Kieron',
    freight='Post',
    engine_type='electric',
    intro_year=1959,
    intro_month=1,
    retire_year=1996,
    retire_month=7,
    speed=145,
    length=11,
    weight=45,
    axles=4,
    power=373,
    gear=80,
    tractive_effort=40,
    payload=600,
    cost=1500000,
    runningcost=75,
    fixed_cost=11042,
    bidirectional=1,
    can_lead_from_rear=1,
    sound='x24tohayes-epb.wav',
    constraint_prev=['BR-410[CEP]Rear', 'BR-414[HAP]Rear', 'BR-419[MLV]', 'BR-499[TLV]', 'BR-423-DTCL-Rear', 'BR-421[CIG]Rear', 'BR-4EPB(rear)', 'BR-2EPB(rear)', 'none'],
    liverytype=['BR-Revised', 'BR-Blue', 'BR-Large-Logo', 'Jaffa-Cake', 'NSE-Standard', 'SWT-orange-stripe'],
    way_constraint_permissive=[0],
    blend='trains/Railcars/br-419-nse.blend',
    upstream_dat='trains/br-419.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
