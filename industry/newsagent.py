"""Newsagent 1860 — single-era port off `industries/1860-newsagent.blend`.

Upstream `newsagent.dat` packs four eras: 1860 renders off the
shared `newsagent.*` atlas (matching `1860-newsagent.blend`),
1920 off `newsagent-deco.*` (no upstream blend), and 1950 /
1970 off the unported `1950shops.*` atlas.  Only the 1860 era
ports here; the rest stay unported until those blends or
atlases land.

No `1860-newsagent-snow.blend` ships winter art in the matched
upstream — `seasons=1` drops the upstream's winter slots.
"""

from pak.bake import bake_factory_main
from pak.dat import Factory

_BLEND = "industries/1860-newsagent.blend"
_UPSTREAM_DAT = "industry/newsagent.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

SPEC = Factory(
    name="Newsagent1860",
    copyright="James",
    seasons=1,
    level=5,
    intro_year=1860, intro_month=1,
    retire_year=1920, retire_month=1,
    needs_ground=1,
    climates=_CLIMATES,
    population_and_visitor_demand_capacity=225,
    employment_capacity=33,
    mail_demand=10,
    class_proportion=[15, 20, 20, 27, 18],
    class_proportion_jobs=[40, 45, 14, 1, 0],
    location="city",
    productivity=1,
    range=2,
    distributionweight=24,
    mapcolor=5,
    electricity_amount=1,
    electricity_boost=500,
    passenger_boost=500,
    mail_boost=500,
    inputgood=["newspaper"],
    inputcapacity=[5],
    inputfactor=[100],
    blend=_BLEND,
    upstream_dat=_UPSTREAM_DAT,
)


if __name__ == "__main__":
    bake_factory_main(SPEC, __file__)
