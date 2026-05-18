"""stonehenge attraction."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building
from pak.materials import Material, Slot

MATERIALS = {
    "Pavement": Material(slots=[
        Slot(image="concrete-paving-small", size=(2.11, 1.89, 1.0), ofs=(0.0, 0.02, 0.0)),
    ]),
    "Stone": Material(slots=[
        Slot(procedural="MUSGRAVE", color=(0.5, 0.4932, 0.45)),
        Slot(procedural="CLOUDS", texco="ORCO", color=(0.6862, 0.6861, 0.6861)),
    ]),
}

# Upstream carries seasons=2 (winter atlas slots).  JamesHood doesn't
# ship a `-snow.blend` for stonehenge so the winter pass is dropped;
# summer atlas only.  Second multi-tile building port (2x2x4, after
# mechanical-signalbox-large's 2x1x4) -- exercises the dims_x ==
# dims_y centroid / 4-rotation cycle path that the rectangular
# signalbox didn't hit (see TODO.md -> multi-tile calibration
# diff / rotation formula entries).
SPEC = Building(
    name="Stonehenge",
    type="cur",
    dims_x=2,
    dims_y=2,
    layouts=4,
    intro_year=1700,
    intro_month=1,
    needs_ground=1,
    regions=0,
    build_time=0,
    population_and_visitor_demand_capacity=130,
    employment_capacity=3,
    mail_demand=0,
    chance=5,
    class_proportion=[10, 20, 25, 25, 20],
    class_proportion_jobs=[30, 35, 30, 5, 0],
    blend="attractions/stonehenge.blend",
    upstream_dat="attractions/stonehenge.dat",
    blend_source="jh",
    materials=MATERIALS,
    # Blend ortho=72 was authored to fit the whole composition
    # (stones + surrounding landscape planes spanning ~42 world
    # units), not the per-tile rate (72 / max(dims)=2 = 36 per
    # tile, vs the standard 24).  Pin per-tile=24 to render at
    # the standard rate -- 72 / (24 * 2) = 1.5 divisor.
    blend_ortho_per_tile=24.0,
    # `pak.diag_centroid_align` reports per-layout residuals that
    # don't reduce to a single model translation: tried pinning the
    # mean and only one layout aligns; others get worse.  Leave None
    # -- the residual is per-layout shape mismatch from procedural
    # Stone material's MUSGRAVE/CLOUDS noise rotating with the model
    # (every layout renders a different noise phase in world coords
    # while upstream BI samples differently).  Worst stitched IoU
    # ~0.49 is the floor.
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
