"""Bakery 1840 + 1910 + 1945 — shared-sprite upgrade chain.

Upstream `bakery.dat` packs four eras; Bakery1750 renders off the
unported `1750-shops.*` atlas (out of scope), the other three all
point at the shared `bakery.*` atlas off `industries/bakery.blend`.
"""

from pak.bake import bake_factory_main
from pak.dat import Factory

_BLEND = "industries/bakery.blend"
_BLEND_WINTER = "industries/bakery-snow.blend"
_UPSTREAM_DAT = "industry/bakery.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

SPECS = [
    Factory(
        name="Bakery1840",
        copyright="Archon",
        seasons=2,
        level=4,
        intro_year=1840, intro_month=12,
        retire_year=1910, retire_month=10,
        climates=_CLIMATES,
        population_and_visitor_demand_capacity=320,
        employment_capacity=90,
        mail_demand=12,
        class_proportion=[25, 25, 25, 15, 10],
        class_proportion_jobs=[45, 40, 15, 0, 0],
        location="city",
        productivity=2,
        range=5,
        distributionweight=30,
        mapcolor=180,
        electricity_amount=1,
        electricity_boost=500,
        passenger_boost=800,
        mail_boost=200,
        inputgood=["flour"],
        inputcapacity=[24],
        inputfactor=[100],
        blend=_BLEND,
        blend_winter=_BLEND_WINTER,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Factory(
        name="Bakery1910",
        copyright="James",
        seasons=2,
        level=5,
        intro_year=1910, intro_month=12,
        retire_year=1945, retire_month=10,
        climates=_CLIMATES,
        population_and_visitor_demand_capacity=480,
        employment_capacity=135,
        mail_demand=18,
        class_proportion=[23, 23, 23, 17, 15],
        class_proportion_jobs=[44, 38, 17, 0, 0],
        location="city",
        productivity=3,
        range=7,
        distributionweight=27,
        mapcolor=180,
        electricity_amount=1,
        electricity_boost=775,
        passenger_boost=800,
        mail_boost=200,
        inputgood=["flour"],
        inputcapacity=[32],
        inputfactor=[100],
        blend=_BLEND,
        blend_winter=_BLEND_WINTER,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Factory(
        name="Bakery1945",
        copyright="Kieron & WLindley",
        seasons=2,
        level=5,
        intro_year=1945, intro_month=12,
        retire_year=1975, retire_month=10,
        climates=_CLIMATES,
        population_and_visitor_demand_capacity=640,
        employment_capacity=180,
        mail_demand=24,
        class_proportion=[20, 20, 20, 20, 20],
        class_proportion_jobs=[25, 35, 40, 0, 0],
        location="city",
        productivity=4,
        range=10,
        distributionweight=24,
        mapcolor=180,
        electricity_amount=2,
        electricity_boost=1125,
        passenger_boost=800,
        mail_boost=200,
        inputgood=["flour"],
        inputcapacity=[48],
        inputfactor=[100],
        blend=_BLEND,
        blend_winter=_BLEND_WINTER,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_factory_main(SPECS, __file__)
