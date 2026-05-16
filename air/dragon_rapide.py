"""De Havilland DH.89 Dragon Rapide passenger biplane."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle


# https://en.wikipedia.org/wiki/De_Havilland_Dragon_Rapide
# http://www.aviacaocomercial.net/english/frotavarig.htm
SPEC = Vehicle(
    name="dragon-rapide",
    waytype="air",
    # CC-BY-SA.
    copyright="Emmanuel Baranger",
    freight="Passagiere",
    engine_type="petrol",
    intro_year=1934, intro_month=4,
    retire_year=1939, retire_month=12,
    speed=214,
    weight=1.6,
    # https://en.wikipedia.org/wiki/De_Havilland_Dragon_Rapide#Specifications_(Dragon_Rapide)
    power=300,
    tractive_effort=4,
    payload=8,
    min_loading_time=1600,
    max_loading_time=1600,
    catering_level=0,
    cost=2000000,
    runningcost=15,
    fixed_cost=51389,
    sound="andysvideo-vickers-vimy.wav",
    minimum_runway_length=265,
    range=895,
    constraint_prev=["none"],
    constraint_next=["none"],
    payload_by_class=[0, 0, 0, 0, 8],
    comfort_by_class=[0, 0, 0, 0, 68],
)
BLEND = "air/dragon-rapide.blend"
UPSTREAM_STEM = "air/images/dragon-rapide"


if __name__ == "__main__":
    bake_main(SPEC, BLEND, __file__)
