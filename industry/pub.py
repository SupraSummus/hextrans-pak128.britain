"""Pub 1750 + 1840 + 1910 — shared-sprite upgrade chain.

Upstream `pub.dat` packs five eras; Pub1945 / Pub1975 render off
the unported `1950pubs.*` atlas (out of scope).  The three early
eras all point at the shared `pub.*` atlas off `industries/pub.blend`.

No `pub-snow.blend` exists upstream; `seasons=1` drops the
upstream's `pub.1.X` winter row until a snow blend lands.
"""

from pak.bake import bake_factory_main
from pak.dat import Factory
from pak.materials import Lighting, Material

_BLEND = "industries/pub.blend"
_UPSTREAM_DAT = "industry/pub.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

# AUTO-TUNED: pak.tune_industries
MATERIALS = {
    'Brick': Material(image='flemish-bond-improved', size=(0.5, 0.5, 0.5), color=(1.0, 1.0, 1.0)),
    'Hedge': Material(image='scratched_bricks_9271', size=(4.0, 4.0, 1.0), color=(0.469, 0.858, 0.637)),
    'Material.001': Material(image='grey_roof_slate.jpg', texco='ORCO', size=(20.0, 20.0, 20.0), color=(1.342, 1.344, 1.303)),
    'Pavement': Material(image='concrete-paving-small', size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0), color=(0.772, 0.754, 0.714)),
    'Shop2': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
    'Stone Wall': Material(image='stonewall-texture.jpg', color=(1.595, 1.53, 1.499)),
    'WindowFrame': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
}

LIGHTING = Lighting(world_ambient=(0.45, 0.45, 0.45), sun_energy_scale=71.428571, sun_elev_deg=45.0, sun_az_offset_deg=-90.0)
# END AUTO-TUNED

SPECS = [
    Factory(
        name="Pub1750",
        copyright="James",
        seasons=1,
        level=2,
        intro_year=1750, intro_month=1,
        retire_year=1840, retire_month=10,
        needs_ground=1,
        climates=_CLIMATES,
        # 300 customers/day × 3 (size adjustment) = 900/day,
        # / 16 hours * 6.4 hours = 360, / 2 for meters/tile.
        population_and_visitor_demand_capacity=180,
        # Staff of 9 in each of 3 pubs (size adjustment).
        employment_capacity=27,
        mail_demand=7,
        class_proportion=[80, 100, 90, 75, 15],
        class_proportion_jobs=[50, 40, 10, 0, 0],
        upgrade=["Pub1840", "Pub1910"],
        location="city",
        # Each barrel is 36 gallons × 8 pints = 288 pints; 3 pints/customer
        # gives 96 customers/barrel.  360 / 96 = 3.75 barrels/month,
        # × 2/3 for meters/tile.
        productivity=2,
        range=1,
        distributionweight=24,
        mapcolor=62,
        electricity_amount=0,
        electricity_boost=0,
        passenger_boost=750,
        mail_boost=250,
        inputgood=["beer", "cider"],
        inputcapacity=[18, 12],
        inputfactor=[67, 100],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
        materials=MATERIALS,
        lighting=LIGHTING,
    ),
    Factory(
        name="Pub1840",
        copyright="James",
        seasons=1,
        level=4,
        intro_year=1840, intro_month=12,
        retire_year=1910, retire_month=10,
        needs_ground=1,
        climates=_CLIMATES,
        # 500 customers/day × 3 = 1500/day, / 16 × 6.4 = 600, / 2 for tile.
        population_and_visitor_demand_capacity=300,
        # Staff of 10 in each of 3 pubs.
        employment_capacity=30,
        mail_demand=13,
        class_proportion=[95, 100, 90, 65, 15],
        class_proportion_jobs=[50, 40, 10, 0, 0],
        upgrade=["Pub1910"],
        location="city",
        # 600 / 96 customers per barrel = 6.25 barrels/month.
        productivity=6,
        range=3,
        distributionweight=30,
        mapcolor=62,
        electricity_amount=1,
        electricity_boost=200,
        passenger_boost=750,
        mail_boost=250,
        inputgood=["beer", "cider"],
        inputcapacity=[36, 30],
        inputfactor=[80, 100],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
        materials=MATERIALS,
        lighting=LIGHTING,
    ),
    Factory(
        name="Pub1910",
        copyright="James",
        seasons=1,
        level=5,
        intro_year=1910, intro_month=12,
        retire_year=1945, retire_month=10,
        needs_ground=1,
        climates=_CLIMATES,
        population_and_visitor_demand_capacity=360,
        employment_capacity=32,
        mail_demand=16,
        class_proportion=[95, 100, 90, 65, 15],
        class_proportion_jobs=[40, 45, 15, 0, 0],
        location="city",
        productivity=6,
        range=4,
        distributionweight=27,
        mapcolor=62,
        electricity_amount=1,
        electricity_boost=320,
        passenger_boost=750,
        mail_boost=250,
        inputgood=["beer", "cider"],
        inputcapacity=[36, 36],
        inputfactor=[100, 100],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
        materials=MATERIALS,
        lighting=LIGHTING,
    ),
]


if __name__ == "__main__":
    bake_factory_main(SPECS, __file__)
