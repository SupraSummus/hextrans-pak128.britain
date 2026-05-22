"""Fishmongers 1840 + 1910 — shared-sprite upgrade pair.

Upstream `fishmongers.dat` packs four eras; Fishmongers1820 renders
off the unported `1750-shops.*` atlas and Fishmongers1945 off the
unported `1950shops.*` atlas (out of scope).  The two middle eras
share the `fishmongers.*` atlas off `industries/fishmongers.blend`.
"""

from pak.bake import bake_factory_main
from pak.dat import Factory

_BLEND = "industries/fishmongers.blend"
_BLEND_WINTER = "industries/fishmonger-snow.blend"
_UPSTREAM_DAT = "industry/fishmongers.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

SPECS = [
    Factory(
        name="Fishmongers1840",
        copyright="Archon",
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
        upgrade=["Fishmongers1910"],
        location="City",
        productivity=5,
        range=8,
        distributionweight=27,
        mapcolor=150,
        electricity_amount=1,
        electricity_boost=250,
        passenger_boost=800,
        mail_boost=200,
        inputgood=["fish"],
        inputcapacity=[30],
        inputfactor=[100],
        blend=_BLEND,
        blend_winter=_BLEND_WINTER,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Factory(
        name="Fishmongers1910",
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
        location="City",
        productivity=10,
        range=15,
        distributionweight=21,
        mapcolor=150,
        electricity_amount=1,
        electricity_boost=500,
        passenger_boost=800,
        mail_boost=200,
        inputgood=["fish"],
        inputcapacity=[60],
        inputfactor=[100],
        blend=_BLEND,
        blend_winter=_BLEND_WINTER,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_factory_main(SPECS, __file__)
