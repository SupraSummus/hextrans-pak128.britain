"""RES_KG_1870_00_06 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building
from pak.materials import Material

MATERIALS = {
    "FeltRoof":     Material(noise=True),
    "Fence":        Material(image="scratched_bricks_9271", size=(4.0, 4.0, 1.0)),
    "Frame":        Material(image="scratched_bricks_9271", size=(4.0, 4.0, 1.0)),
    "Interior.001": Material(noise=True),
    "MainColour1":  Material(noise=True),
    "Pavement":     Material(image="concrete-paving-small", size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0)),
    "Stone":        Material(image="concrete-paving-s", size=(1.2, 1.2, 1.2), ofs=(0.5, 0.5, 0.0)),
    "Stone.001":    Material(noise=True),
    "Tiles":        Material(image="concrete-paving-small", size=(3.0, 3.0, 3.0)),
    "WindowFrame":  Material(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
}

# Middling semi-detached houses.
SPEC = Building(
    name="RES_KG_1870_00_06",
    type="res",
    copyright="Kieron",
    level=6,
    chance=70,
    intro_year=1870,
    retire_year=1890,
    needs_ground=1,
    population_and_visitor_demand_capacity=38,
    class_proportion=[0, 20, 65, 15, 0],
)
BLEND = "citybuildings/1870-townhouse-3f.blend"
UPSTREAM_STEM = "citybuildings/images/res/1870-townhouse-3f.png"


if __name__ == "__main__":
    bake_building_main(SPEC, BLEND, __file__, materials=MATERIALS)
