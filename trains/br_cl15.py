"""Bake the BR Class 15 diesel locomotive.

See `_4wheel_1850s_first.py` for the bake-unit pattern.
"""

from __future__ import annotations

from tools.threed.bake import bake_main
from tools.threed.dat import Vehicle


SPEC = Vehicle(
    name="BR-Class15",
    waytype="track",
    copyright="Junna/Cake",
    freight="None",
    engine_type="diesel",
    intro_year=1957, intro_month=5,
    retire_year=1961, retire_month=8,
    speed=97,
    length=8,
    weight=70,
    axles=4,
    power=597,
    gear=50,
    tractive_effort=167,
    rolling_resistance=13,
    payload=0,
    cost=4500000,
    runningcost=598,
    fixed_cost=14688,
    increase_maintenance_after_years=20,
    bidirectional=1,
    can_lead_from_rear=0,
    smoke="Diesel-heavy",
    sound="androo4519-class-17.wav",
    # Blue star multi-working group.
    constraint_prev=[
        "BR-Class15", "BR-Class17", "BR-Class20", "BR-Class24",
        "BR-Class25", "BR-Class26", "BR-Class27", "BR-Class31-1",
        "BR-Class37", "BR-Class40", "BR-Class45", "none",
    ],
    liverytype=["BR-Early", "BR-Blue"],
)
BLEND = "trains/Locomotives/br-cl15.blend"


if __name__ == "__main__":
    bake_main(SPEC, BLEND, __file__)
