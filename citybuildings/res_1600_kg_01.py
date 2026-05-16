"""RES_KG_1600_00_01 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building


# Artisan's cottage, perhaps: large, double-fronted.
# Population: estimate 12 per house (including servants) x 5 (low
# density, large gardens) yields 75, / 16 hours * 6.4 hours = 30;
# half when meters/tile is taken into account → 15.
SPEC = Building(
    name="RES_KG_1600_00_01",
    type="res",
    copyright="Kieron",
    layouts=4,
    # heights=1 is correct here: the hex projection + shear render
    # this 2-storey detached as a ~54 px-tall silhouette that fits
    # one cell, even though the blend's z extent is 2.64 intra-tile.
    level=1,
    chance=50,
    intro_year=1600,
    retire_year=1850,
    needs_ground=1,
    population_and_visitor_demand_capacity=15,
    employment_capacity=0,
    mail_demand=1,
    class_proportion=[0, 40, 100, 75, 0],
)
BLEND = "citybuildings/1600-detatched-house-2f.blend"
UPSTREAM_STEM = "citybuildings/images/res/1600-detatched-house-2f.png"


if __name__ == "__main__":
    bake_building_main(SPEC, BLEND, __file__)
