"""Large classical townhall."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Building, Symmetry
from pak.sprites import UpstreamRemap

SPEC = Building(
    name="02_CITY",
    type="tow",
    dims_x=2,
    dims_y=2,
    symmetry=Symmetry.CONTINUOUS,
    seasons=2,
    intro_year=1750,
    intro_month=1,
    needs_ground=1,
    noconstruction=1,
    build_time=4000,
    population_and_visitor_demand_capacity=65,
    employment_capacity=85,
    mail_demand=60,
    class_proportion=[3, 7, 25, 30, 30],
    class_proportion_jobs=[5, 10, 45, 25, 15],
    upstream_dat="townhall/townhalls.dat",
    sprites=UpstreamRemap(),
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
