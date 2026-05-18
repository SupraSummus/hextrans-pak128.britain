"""RES_KG_1890_00_02 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building
from pak.materials import Material

MATERIALS = {
    "FeltRoof":    Material(noise=True),
    "MainColour1": Material(noise=True),
    "Pavement":    Material(image="concrete-paving-small", size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0)),
    "Stone":       Material(noise=True),
    "Tiles":       Material(image="concrete-paving-small", size=(3.0, 3.0, 3.0)),
}

# Low density townhouses.
SPEC = Building(
    name="RES_KG_1890_00_02",
    type="res",
    copyright="Kieron",
    level=2,
    chance=45,
    intro_year=1890,
    retire_year=1910,
    needs_ground=1,
    population_and_visitor_demand_capacity=18,
    class_proportion=[0, 40, 5, 55, 0],
    blend="citybuildings/1890-detatched-house-3f.blend",
    upstream_dat="citybuildings/res-1890.dat",
    materials=MATERIALS,
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
