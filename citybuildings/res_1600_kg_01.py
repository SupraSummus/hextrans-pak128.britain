"""Bake the RES_KG_1600_00_01 city building.

Single-tile residential (`type=res`) with four layout rotations.
First multi-rotation building bake — exercises the layouts axis
of the `Building` schema, the `building_hex_viewpoint` factory,
and `bake_building` end-to-end.  Still single-tile (1x1
footprint), so the multi-tile centring landmine called out in
CLAUDE.md → "Building-bake architecture" stays out of scope
until a 2x1+ building ports.

Run from the repo root:

    python3 -m citybuildings.res_1600_kg_01

Seeded by `port_building` against upstream `citybuildings/
res-1600.dat` (single-object dat); upstream removed once the
SPEC verifiably round-trips, per CLAUDE.md → "Upstream dats get
deleted once ported".
"""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building


# Artisan's cottage, perhaps: large, double-fronted.
# Population derivation (preserved from upstream res-1600.dat):
#   Estimate 12 per house (including servants) x 5 (low density,
#   large gardens) yields 75, / 16 hours * 6.4 hours = 30.
#   Half when meters/tile taken into account → 15.
SPEC = Building(
    name="RES_KG_1600_00_01",
    type="res",
    copyright="Kieron",
    layouts=4,
    # heights=1 is correct for this asset: the hex projection +
    # shear render this 2-storey detached as a ~54 px-tall
    # silhouette that fits one cell, even though the blend's z
    # extent is 2.64 intra-tile.  Height-stacking exists for cases
    # where the rendered silhouette overflows one cell vertically.
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
# For `python3 -m pak.check`: full upstream PNG path within the pak repo
# (not a stem, unlike vehicles -- buildings render to a single atlas
# rather than a per-facing collection).  Diffed per-layout via
# `diff_buildings`.
UPSTREAM_STEM = "citybuildings/images/res/1600-detatched-house-2f.png"


if __name__ == "__main__":
    bake_building_main(SPEC, BLEND, __file__)
