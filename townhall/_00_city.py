"""Smallest classical townhall (population threshold 0)."""

from __future__ import annotations

from pak.bake import bake_2d_building_main
from pak.dat import Building, Symmetry

SPEC = Building(
    name="00_CITY",
    type="tow",
    dims_x=2,
    dims_y=2,
    symmetry=Symmetry.CONTINUOUS,
    seasons=2,
    intro_year=1750,
    intro_month=1,
    needs_ground=1,
    noconstruction=1,
    build_time=0,
    population_and_visitor_demand_capacity=25,
    employment_capacity=20,
    mail_demand=20,
    class_proportion=[3, 7, 25, 30, 30],
    class_proportion_jobs=[5, 10, 45, 25, 15],
    upstream_dat="townhall/townhalls.dat",
)


if __name__ == "__main__":
    bake_2d_building_main(SPEC, __file__)
