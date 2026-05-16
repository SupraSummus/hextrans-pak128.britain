"""Heavier wrought-iron fishbelly rail."""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


# As used on the original Liverpool & Manchester Railway.  35 lb/yard.
# Rainhill suggests a 27 km/h limit, but higher speeds on the LMR
# (laid with this track initially until 1835) are recorded in many
# sources e.g. Ahrons p. 65.
# https://books.google.co.uk/books?id=WBI1AAAAMAAJ&pg=PA275
# http://myweb.tiscali.co.uk/gansg/2-track/02track1.htm
# https://lancashireminingmuseum.org/2017/05/02/fishbelly-rails-on-stone-sleepers-original-track-on-the-liverpool-manchester-bolton-leigh-railway-of-1830/
# https://en.wikipedia.org/wiki/Wagonway#Metal_rails_introduced
# http://www.rainhilltrials.com/index.cfm/page/article/id/46/listid/27/title/The%20Liverpool%20and%20Manchester%201830%20Onwards
SPEC = Way(
    name='wrought_iron_fishbelly_heavy_track',
    waytype='track',
    intro_year=1827,
    intro_month=8,
    retire_year=1845,
    retire_month=2,
    topspeed=80,
    max_weight=6,
    wear_capacity=28800000,
    cost=31700,
    maintenance=765,
)
BLEND = "ways/ns-cssr.blend"
MATERIALS = {
    "Ballast": (101, 95, 79),
    "Wood": (111, 106, 91),
    "Rail": (121, 118, 108),
    "RailTop": (138, 134, 127),
}


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
