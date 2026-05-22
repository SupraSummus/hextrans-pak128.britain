"""Greengrocers 1840 + 1910 — shared-sprite upgrade pair.

Upstream `greengrocers.dat` packs four eras; Greengrocers1820 renders
off the unported `1750-shops.*` atlas and Greengrocers1945 off the
unported `1950shops.*` atlas (out of scope).  The two middle eras
share the `greengrocers.*` atlas off `industries/greengrocers.blend`.
"""

from pak.bake import bake_factory_main
from pak.dat import Factory

_BLEND = "industries/greengrocers.blend"
_BLEND_WINTER = "industries/greengrocers-snow.blend"
_UPSTREAM_DAT = "industry/greengrocers.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

SPECS = [
    Factory(
        name="Greengrocers1840",
        copyright="James",
        seasons=2,
        level=6,
        intro_year=1840, intro_month=12,
        retire_year=1910, retire_month=10,
        climates=_CLIMATES,
        population_and_visitor_demand_capacity=320,
        employment_capacity=45,
        mail_demand=12,
        class_proportion=[25, 25, 25, 15, 10],
        class_proportion_jobs=[38, 42, 20, 0, 0],
        upgrade=["Greengrocers1910"],
        location="city",
        max_distance_to_supplier=150,
        productivity=2,
        range=3,
        distributionweight=36,
        mapcolor=206,
        electricity_amount=1,
        electricity_boost=250,
        passenger_boost=800,
        mail_boost=200,
        inputgood=["fruit", "vegetables"],
        inputcapacity=[14, 11],
        inputfactor=[100, 75],
        blend=_BLEND,
        blend_winter=_BLEND_WINTER,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Factory(
        name="Greengrocers1910",
        copyright="James",
        seasons=2,
        level=6,
        intro_year=1910, intro_month=12,
        retire_year=1945, retire_month=10,
        climates=_CLIMATES,
        population_and_visitor_demand_capacity=480,
        employment_capacity=67,
        mail_demand=18,
        class_proportion=[23, 23, 23, 17, 15],
        class_proportion_jobs=[35, 43, 22, 0, 0],
        location="city",
        productivity=4,
        range=7,
        distributionweight=30,
        mapcolor=206,
        electricity_amount=1,
        electricity_boost=320,
        passenger_boost=800,
        mail_boost=200,
        inputgood=["fruit", "vegetables"],
        inputcapacity=[32, 21],
        inputfactor=[100, 67],
        blend=_BLEND,
        blend_winter=_BLEND_WINTER,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_factory_main(SPECS, __file__)
