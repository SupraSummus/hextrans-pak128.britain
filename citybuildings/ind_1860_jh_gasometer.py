"""IND_JH_1860_00_10 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building, Symmetry
from pak.materials import Material

MATERIALS = {
    "MainColour1.001": Material(noise=True),
    "Material.001":    Material(noise=True),
    "Material.002":    Material(noise=True),
    "Material.003":    Material(noise=True),
}

# Gasometer — continuously rotationally symmetric.
SPEC = Building(
    name="IND_JH_1860_00_10",
    type="ind",
    copyright="James",
    symmetry=Symmetry.CONTINUOUS,
    level=5,
    chance=200,
    intro_year=1860,
    retire_year=1950,
    needs_ground=1,
    population_and_visitor_demand_capacity=0,
    employment_capacity=3,
    mail_demand=0,
    class_proportion_jobs=[50, 50, 0, 0, 0],
    blend="citybuildings/1860-gasometer.blend",
    upstream_dat="citybuildings/ind-1860.dat",
    materials=MATERIALS,
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
