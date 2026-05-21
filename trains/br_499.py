"""br-499."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# These were through-wired Mk. I BGs with their gangways plated up:
# http://www.therailwaycentre.com/Recognition%20Tech%20Data%20EMU/EMU_419_499.html
# No photographs availlable except for this MSTS model/render (the TLVs are at the rear):
# http://farm4.staticflickr.com/3247/2448504052_87077169f9_o.jpg
SPEC = Vehicle(
    name='BR-499[TLV]',
    waytype='track',
    copyright='Kieron/jamespetts',
    freight='Post',
    intro_year=1968,
    intro_month=7,
    retire_year=1975,
    retire_month=12,
    speed=145,
    length=11,
    weight=32,
    axles=4,
    rolling_resistance=13,
    payload=600,
    min_loading_time=25,
    max_loading_time=120,
    cost=600000,
    runningcost=0,
    fixed_cost=714,
    upgrade_price=83000,
    bidirectional=1,
    can_lead_from_rear=0,
    constraint_prev=['BR-410[CEP]Rear', 'BR-414[HAP]Rear', 'BR-419[MLV]', 'BR-499[TLV]', 'BR-423-DTCL-Rear', 'BR-421[CIG]Rear', 'BR-4EPB(rear)', 'BR-2EPB(rear)'],
    constraint_next=['BR-410[CEP]Front', 'BR-414[HAP]Front', 'BR-419[MLV]', 'BR-499[TLV]', 'BR-423-DTCL-Front', 'BR-421[CIG]Front', 'BR-4EPB(front)', 'none'],
    liverytype=['BR-Blue'],
    blend='trains/Railcars/br-499-b.blend',
    upstream_dat='trains/br-499.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
