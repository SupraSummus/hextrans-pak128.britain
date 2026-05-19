"""Hunslet Port class narrow-gauge 0-4-0 saddle tank (1883)."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# https://www.quarryhunslet.mste.co.uk/public/Gwynedd.php
# https://www.quarryhunslet.mste.co.uk/public/Lillian.php
# https://en.wikipedia.org/wiki/Penrhyn_Port_Class
SPEC = Vehicle(
    name="hunslet-port",
    waytype="narrowgauge_track",
    copyright="James/jamespetts",
    freight="None",
    engine_type="steam",
    intro_year=1883, intro_month=1,
    retire_year=1892, retire_month=10,
    speed=35,
    length=3,
    # Extrapolated
    power=14,
    # Calculated
    tractive_effort=10,
    rolling_resistance=20,
    payload=0,
    # http://orion.math.iastate.edu/jdhsmith/term/slgbpqr.htm
    weight=8,
    axles=2,
    cost=1604510,
    runningcost=12,
    fixed_cost=17292,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke="Steam",
    sound="laurie-barclay-0-4-0.wav",
    blend="narrowgauge/hunslet-port.blend",
    upstream_dat="narrowgauge/hunslet-port.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
