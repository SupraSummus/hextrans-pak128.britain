"""COM_KG_1870_00_06 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building
from pak.materials import Material

MATERIALS = {
    "Brick":     Material(image="concrete-paving-s", size=(1.2, 1.2, 1.2), ofs=(0.5, 0.5, 0.0)),
    "Frame":     Material(image="concrete-paving-s", size=(4.0, 4.0, 1.0)),
    "Pavement":  Material(image="concrete-paving-s", size=(2.11, 1.89, 1.0), ofs=(0.0, 0.02, 0.0)),
    "RightDoor": Material(image="concrete-paving-s", size=(4.0, 4.0, 1.0)),
    "Tiles":     Material(image="concrete-paving-s", texco="ORCO", size=(1.5, 1.5, 1.5)),
    "Veg2":      Material(image="concrete-paving-s", size=(4.0, 4.0, 1.0)),
}

# Public house.
SPEC = Building(
    name="COM_KG_1870_00_06",
    type="com",
    copyright="Kieron",
    level=6,
    chance=50,
    intro_year=1870,
    retire_year=1910,
    needs_ground=1,
    population_and_visitor_demand_capacity=96,
    employment_capacity=17,
    mail_demand=10,
    class_proportion=[0, 5, 45, 50, 0],
    class_proportion_jobs=[70, 20, 8, 2, 0],
    blend="citybuildings/1870-pub.blend",
    upstream_stem="citybuildings/images/com/1870-pub.png",
    materials=MATERIALS,
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
