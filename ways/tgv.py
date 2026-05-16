"""TGV (high-speed rail) track."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name="tgv",
    waytype="track",
    intro_year=1981,
    intro_month=9,
    topspeed=320,
    # Actual French TGV track has a 17 t axle load; HS1 in the UK
    # accommodates at least the Class 92 (21 t).
    # http://www.therailwaycentre.com/Recognition%20Tech%20Data%20EMU/EMU_373.html
    max_weight=21,
    wear_capacity=4200000000,
    cost=250000,
    # Lower than otherwise owing to the hard concrete base in place
    # of ballast.
    maintenance=950,
)
BLEND = "ways/tgv.blend"


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__)
