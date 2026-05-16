"""Wrought-iron fishbelly rail."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


# As used on the original Stockton & Darlington Railway.  28 lb/yard.
# https://books.google.co.uk/books?id=WBI1AAAAMAAJ&pg=PA275
# http://myweb.tiscali.co.uk/gansg/2-track/02track1.htm
# https://lancashireminingmuseum.org/2017/05/02/fishbelly-rails-on-stone-sleepers-original-track-on-the-liverpool-manchester-bolton-leigh-railway-of-1830/
# https://en.wikipedia.org/wiki/Wagonway#Metal_rails_introduced
SPEC = Way(
    name='wrought_iron_fishbelly_track',
    waytype='track',
    intro_year=1820,
    intro_month=4,
    retire_year=1835,
    retire_month=9,
    topspeed=75,
    max_weight=5,
    wear_capacity=20160000,
    cost=30000,
    maintenance=755,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (83, 76, 59),
    "Wood": (97, 89, 69),
    "Rail": (111, 106, 92),
    "RailTop": (138, 133, 120),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
