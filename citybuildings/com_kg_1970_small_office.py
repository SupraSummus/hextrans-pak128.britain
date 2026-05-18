"""COM_KG_1970_00_08 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building
from pak.materials import Material

MATERIALS = {
    "FeltRoof":    Material(noise=True),
    "Pavement":    Material(image="concrete-paving-small", size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0)),
    "WindowFrame": Material(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
}

# Two-storey office block.
SPEC = Building(
    name="COM_KG_1970_00_08",
    type="com",
    copyright="Kieron",
    level=8,
    chance=70,
    intro_year=1970,
    retire_year=1990,
    needs_ground=1,
    population_and_visitor_demand_capacity=5,
    employment_capacity=38,
    mail_demand=3,
    class_proportion=[0, 1, 69, 25, 5],
    class_proportion_jobs=[2, 8, 80, 8, 2],
    blend="citybuildings/70-small-office.blend",
    upstream_dat="citybuildings/com-70.dat",
    materials=MATERIALS,
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
