"""RES_KG_1920_00_02 city building."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Building
from pak.materials import Material

MATERIALS = {
    "Brick":     Material(image="scratched_bricks_", size=(1.0, 0.8, 0.2), ofs=(0.5, 0.0, 0.0)),
    "Frame":     Material(image="scratched_bricks_9271", size=(4.0, 4.0, 1.0)),
    "Pavement":  Material(image="concrete-paving-small", size=(2.11, 1.89, 1.0), ofs=(0.0, 0.02, 0.0)),
    "Rendering": Material(image="scratched_bricks_9271", size=(4.0, 4.0, 1.0)),
    "Tiles":     Material(image="concrete-paving-small", size=(12.0, 12.0, 12.0)),
}

# Detached house with sizeable garden.
SPEC = Building(
    name="RES_KG_1920_00_02",
    type="res",
    copyright="Kieron",
    level=2,
    chance=65,
    intro_year=1920,
    retire_year=1940,
    needs_ground=1,
    population_and_visitor_demand_capacity=11,
    mail_demand=4,
    class_proportion=[0, 5, 40, 50, 5],
    blend="citybuildings/1920-detatched-house-2f.blend",
    upstream_dat="citybuildings/res-1920.dat",
    materials=MATERIALS,
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
