"""China Shop 1750 — single-era port off `industries/1750-china-shop.blend`.

Upstream `1750-china-shop.dat` packs three eras across three
atlases; only ChinaShop1750 renders from the matching blend.
ChinaShop1850 (`victorian-china-shop.*`) and ChinaShop1905
(`deco-china-shop.*`) need their own atlases / blends -- not in
the upstream blends repo.
"""

from pak.bake import bake_factory_main
from pak.dat import Factory

_BLEND = "industries/1750-china-shop.blend"
_BLEND_WINTER = "industries/1750-china-shop-snow.blend"
_UPSTREAM_DAT = "industry/1750-china-shop.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

SPEC = Factory(
    name="ChinaShop1750",
    copyright="James",
    seasons=2,
    level=3,
    intro_year=1750, intro_month=1,
    retire_year=1855, retire_month=9,
    needs_ground=1,
    climates=_CLIMATES,
    population_and_visitor_demand_capacity=75,
    employment_capacity=22,
    mail_demand=8,
    class_proportion=[10, 25, 35, 15, 15],
    class_proportion_jobs=[40, 45, 15, 0, 0],
    location="city",
    productivity=2,
    range=3,
    distributionweight=13,
    mapcolor=29,
    electricity_amount=0,
    electricity_boost=0,
    passenger_boost=800,
    mail_boost=200,
    inputgood=["china"],
    inputcapacity=[32],
    inputfactor=[100],
    blend=_BLEND,
    blend_winter=_BLEND_WINTER,
    upstream_dat=_UPSTREAM_DAT,
)


if __name__ == "__main__":
    bake_factory_main(SPEC, __file__)
