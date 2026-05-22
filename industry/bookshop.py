"""Bookshop 1750 — single-era port.

Upstream `bookshop.dat` packs five eras off four distinct atlases;
only Bookshop1750 renders from `industries/bookshop.blend`.  The
victorian / deco / 1950s eras (bookshop-victorian, bookshop-deco,
1950shops) are out of scope until those blends or atlases port.

No `bookshop-snow.blend` exists upstream; `seasons=1` drops the
upstream's winter slots until a snow blend lands.
"""

from pak.bake import bake_factory_main
from pak.dat import Factory

_BLEND = "industries/bookshop.blend"
_UPSTREAM_DAT = "industry/bookshop.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

SPEC = Factory(
    name="Bookshop1750",
    copyright="James",
    seasons=1,
    intro_year=1750, intro_month=1,
    retire_year=1860, retire_month=1,
    needs_ground=1,
    climates=_CLIMATES,
    population_and_visitor_demand_capacity=75,
    employment_capacity=22,
    mail_demand=8,
    class_proportion=[0, 10, 30, 30, 30],
    class_proportion_jobs=[40, 45, 15, 0, 0],
    location="city",
    productivity=4,
    range=3,
    distributionweight=2,
    mapcolor=7,
    inputgood=["Bucher"],
    inputcapacity=[17],
    inputfactor=[100],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
)


if __name__ == "__main__":
    bake_factory_main(SPEC, __file__)
