"""RES_KG_1600_00_01 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building
from pak.materials import Material

MATERIALS = {
    "Brick":          Material(image="flemish-bond-improved", size=(0.5, 0.5, 0.5)),
    "Hedge":          Material(image="scratched_bricks_9271", size=(4.0, 4.0, 1.0)),
    "MainColour1":    Material(noise=True),
    "Pavement":       Material(image="concrete-paving-small", size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0)),
    "Roof":           Material(image="flemish-bond-impr.001", size=(3.0, 1.0, 2.0)),
    "RoofSide":       Material(image="flemish-bond-impr.001", size=(3.0, 1.0, 2.0)),
    "Shop3":          Material(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
    "WindowFrame":    Material(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
    "WindowSurround": Material(noise=True),
}

# Seeded by `python3 -m pak.extract_materials
# citybuildings/1600-detatched-house-2f-snow.blend` — the upstream
# winter sibling.  Same material names as summer; Roof / Brick drop
# their flemish-bond textures in favour of CLOUDS, picking up the
# snow blend's grey diffuse via flat colour + noise.
MATERIALS_WINTER = {
    "Brick":          Material(noise=True),
    "Brick.002":      Material(noise=True),
    "Brick.003":      Material(noise=True),
    "Hedge":          Material(image="scratched_bricks_9271", size=(4.0, 4.0, 1.0)),
    "MainColour1":    Material(noise=True),
    "Pavement":       Material(image="concrete-paving-small", size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0)),
    "Roof":           Material(noise=True),
    "RoofSide":       Material(image="flemish-bond-impr", size=(3.0, 1.0, 2.0)),
    "Shop3":          Material(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
    "WindowFrame":    Material(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
    "WindowSurround": Material(noise=True),
}

# Artisan's cottage, perhaps: large, double-fronted.
# Population: estimate 12 per house (including servants) x 5 (low
# density, large gardens) yields 75, / 16 hours * 6.4 hours = 30;
# half when meters/tile is taken into account → 15.
SPEC = Building(
    name="RES_KG_1600_00_01",
    type="res",
    copyright="Kieron",
    level=1,
    chance=50,
    intro_year=1600,
    retire_year=1850,
    needs_ground=1,
    population_and_visitor_demand_capacity=15,
    employment_capacity=0,
    mail_demand=1,
    class_proportion=[0, 40, 100, 75, 0],
    seasons=2,
)
BLEND = "citybuildings/1600-detatched-house-2f.blend"
BLEND_WINTER = "citybuildings/1600-detatched-house-2f-snow.blend"
UPSTREAM_STEM = "citybuildings/images/res/1600-detatched-house-2f.png"


if __name__ == "__main__":
    bake_building_main(
        SPEC, BLEND, __file__,
        materials=MATERIALS,
        blend_winter=BLEND_WINTER, materials_winter=MATERIALS_WINTER,
    )
