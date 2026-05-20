"""BR Standard Class 8P Duke of Gloucester."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# http://en.wikipedia.org/wiki/BR_Standard_Class_8
SPEC = Vehicle(
    name="BR-8P",
    waytype="track",
    copyright="Kieron/JamesPetts",
    freight="None",
    engine_type="steam",
    intro_year=1954, intro_month=4,
    retire_year=1959, retire_month=3,
    speed=160,
    # Calculated from figures at:
    # https://books.google.co.uk/books?id=GVgiRfFBiTgC&pg=PA437
    power=697,
    tractive_effort=174,
    weight=102.9,
    axle_load=22,
    # Three cylinders
    way_wear_factor=141488,
    rolling_resistance=13,
    payload=0,
    cost=10450000,
    runningcost=525,
    fixed_cost=61771,
    increase_maintenance_after_years=5,
    years_before_maintenance_max_reached=12,
    smoke="Steam",
    sound="konakaboom-black-five.wav",
    constraint_next=["BR-7MT-Tender"],
    blend="trains/Locomotives/br-8p.blend",
    upstream_dat="trains/br-8p.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
