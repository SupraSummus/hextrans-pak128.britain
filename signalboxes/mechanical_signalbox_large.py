"""mechanical-signalbox-large signalbox."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building
from pak.materials import Material, Slot

MATERIALS = {
    "Brick": Material(slots=[
        Slot(image="scratched_bricks_.005", size=(5.0, 4.0, 1.0), ofs=(0.5, 0.0, 0.0)),
    ]),
    "Brick.001": Material(slots=[
        Slot(image="scratched_bricks_9271342.JPG", texco="ORCO", size=(4.0, 2.0, 2.0)),
    ]),
    "Brick.004": Material(slots=[
        Slot(image="scratched_bricks_", size=(1.0, 0.8, 0.2), ofs=(0.5, 0.0, 0.0)),
    ]),
    "Dirty brick": Material(slots=[
        Slot(image="scratched_bricks_.005", size=(2.2, 1.7, 0.5), ofs=(0.5, 0.0, 0.0)),
    ]),
    "Door": Material(slots=[
        Slot(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
        Slot(image="scratched_bricks_", texco="ORCO"),
    ]),
    "Door frame": Material(slots=[
        Slot(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
        Slot(image="scratched_bricks_", texco="ORCO"),
    ]),
    "Frame": Material(slots=[
        Slot(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
        Slot(image="scratched_bricks_", texco="ORCO"),
    ]),
    "Pavement": Material(slots=[
        Slot(image="concrete-paving-small", size=(2.11, 1.89, 1.0), ofs=(0.0, 0.02, 0.0)),
    ]),
    "Roof": Material(slots=[
        Slot(image="grey_roof_slate.jpg", texco="ORCO", size=(6.0, 6.0, 4.0)),
    ]),
    "Roof.001": Material(slots=[
        Slot(image="grey_roof_slate.jpg.001", texco="ORCO", size=(6.0, 4.0, 4.0)),
        Slot(procedural="CLOUDS", texco="ORCO", fac=0.7, color=(0.7, 0.7, 0.7)),
    ]),
}

# Upstream carries seasons=2 (winter atlas slots), signal_groups=2,3
# and radius=4000 — Extended-only signal-network keys without a
# Building-dataclass field today.  No `-snow.blend` sibling exists
# upstream so the winter pass is dropped; the signal_groups / radius
# pair are dropped too (the hex engine isn't Extended-aware).  First
# multi-tile building port (2x1x4) — exercises the dims_x>1 axis
# `iter_building_cells` was unit-tested against but never rendered.
SPEC = Building(
    name="mechanical-signalbox-large",
    type="signalbox",
    copyright="JamesPetts",
    dims_x=2,
    layouts=4,
    level=1,
    intro_year=1860,
    intro_month=4,
    retire_year=1971,
    retire_month=8,
    needs_ground=1,
    allow_underground=0,
    population_and_visitor_demand_capacity=0,
    employment_capacity=2,
    mail_demand=2,
    capacity=20,
    maintenance=10000,
    cost=1000000,
    class_proportion=[0, 4, 66, 30, 0],
    class_proportion_jobs=[0, 10, 90, 0, 0],
    blend="signals/mechanical-signalbox-large.blend",
    upstream_stem="signalboxes/images/mechanical-signalbox-large.png",
    materials=MATERIALS,
)


if __name__ == "__main__":
    bake_building_main(SPEC, __file__)
