"""Butchery 1840 + 1910 — shared-sprite upgrade pair.

Upstream `butchery.dat` packs four eras; Butchery1820 renders off
the unported `1750-shops.*` atlas and Butchery1945 off the
unported `1950shops.*` atlas (out of scope).  The two middle eras
share the `butchery.*` atlas off `industries/butchery.blend`.
"""

from pak.bake import bake_factory_main
from pak.dat import Factory

_BLEND = "industries/butchery.blend"
_BLEND_WINTER = "industries/butchery-snow.blend"
_UPSTREAM_DAT = "industry/butchery.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

SPECS = [
    Factory(
        name="Butchery1840",
        copyright="James",
        seasons=2,
        level=4,
        intro_year=1840, intro_month=12,
        retire_year=1910, retire_month=10,
        climates=_CLIMATES,
        population_and_visitor_demand_capacity=200,
        employment_capacity=80,
        mail_demand=11,
        class_proportion=[12, 29, 29, 18, 12],
        class_proportion_jobs=[38, 42, 20, 0, 0],
        upgrade=["Butchery1910"],
        location="city",
        productivity=2,
        range=3,
        distributionweight=30,
        mapcolor=132,
        electricity_amount=1,
        electricity_boost=320,
        passenger_boost=800,
        mail_boost=200,
        inputgood=["meat"],
        inputcapacity=[16],
        inputfactor=[100],
        blend=_BLEND,
        blend_winter=_BLEND_WINTER,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Factory(
        name="Butchery1910",
        copyright="James",
        seasons=2,
        level=5,
        intro_year=1910, intro_month=12,
        retire_year=1945, retire_month=10,
        climates=_CLIMATES,
        population_and_visitor_demand_capacity=300,
        employment_capacity=120,
        mail_demand=16,
        class_proportion=[15, 28, 28, 17, 12],
        class_proportion_jobs=[35, 43, 22, 0, 0],
        location="city",
        productivity=3,
        range=7,
        distributionweight=27,
        mapcolor=132,
        electricity_amount=1,
        electricity_boost=500,
        passenger_boost=800,
        mail_boost=200,
        inputgood=["meat"],
        inputcapacity=[32],
        inputfactor=[100],
        blend=_BLEND,
        blend_winter=_BLEND_WINTER,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_factory_main(SPECS, __file__)
