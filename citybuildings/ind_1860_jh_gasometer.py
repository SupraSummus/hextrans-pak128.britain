"""IND_JH_1860_00_10 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building
from pak.materials import Material

MATERIALS = {
    "MainColour1.001": Material(noise=True),
    "Material.001":    Material(noise=True),
    "Material.002":    Material(noise=True),
    "Material.003":    Material(noise=True),
}

# Gasometer.  Rotationally symmetric — keep upstream's single layout.
SPEC = Building(
    name="IND_JH_1860_00_10",
    type="ind",
    copyright="James",
    layouts=1,
    level=5,
    chance=200,
    intro_year=1860,
    retire_year=1950,
    needs_ground=1,
    population_and_visitor_demand_capacity=0,
    employment_capacity=3,
    mail_demand=0,
    class_proportion_jobs=[50, 50, 0, 0, 0],
)
BLEND = "citybuildings/1860-gasometer.blend"
UPSTREAM_STEM = "citybuildings/images/ind/1860-gasometer.png"


if __name__ == "__main__":
    bake_building_main(SPEC, BLEND, __file__, materials=MATERIALS)
