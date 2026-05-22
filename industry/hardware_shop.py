"""HardwareShop 1850 — single-era port.

Upstream `hardware-shop.dat` packs four eras off four distinct
atlases; only HardwareShop1850 renders from
`industries/hardware-shop.blend`.  The earlier `hardware-shop-early`
and later `hardware-shop-deco` / 1950s atlases stay unported.
"""

from pak.bake import bake_factory_main
from pak.dat import Factory

_BLEND = "industries/hardware-shop.blend"
_BLEND_WINTER = "industries/hardware-shop-snow.blend"
_UPSTREAM_DAT = "industry/hardware-shop.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

SPEC = Factory(
    name="HardwareShop1850",
    copyright="James",
    seasons=2,
    level=5,
    intro_year=1850, intro_month=2,
    retire_year=1920, retire_month=12,
    climates=_CLIMATES,
    population_and_visitor_demand_capacity=60,
    employment_capacity=22,
    mail_demand=5,
    class_proportion=[10, 15, 20, 27, 28],
    class_proportion_jobs=[40, 45, 14, 1, 0],
    location="City",
    productivity=6,
    range=9,
    distributionweight=18,
    mapcolor=153,
    electricity_amount=1,
    electricity_boost=320,
    passenger_boost=800,
    mail_boost=200,
    inputgood=["hardware"],
    inputcapacity=[96],
    inputfactor=[100],
    blend=_BLEND,
    blend_winter=_BLEND_WINTER,
    upstream_dat=_UPSTREAM_DAT,
)


if __name__ == "__main__":
    bake_factory_main(SPEC, __file__)
