"""Bakery 1840 + 1910 + 1945 — shared-sprite upgrade chain.

Upstream `bakery.dat` packs four eras; Bakery1750 renders off the
unported `1750-shops.*` atlas (out of scope), the other three all
point at the shared `bakery.*` atlas off `industries/bakery.blend`.
"""

from pak.bake import bake_main
from pak.dat import Factory
from pak.materials import Lighting, Material

_BLEND = "industries/bakery.blend"
_BLEND_WINTER = "industries/bakery-snow.blend"
_UPSTREAM_DAT = "industry/bakery.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

# AUTO-TUNED: pak.tune_industries
MATERIALS = {
    'Brick': Material(image='flemish-bond-improved', size=(0.5, 0.5, 0.5), color=(0.622, 0.533, 0.349)),
    'BrickCapping': Material(image='flemish-bond-improved', texco='ORCO', size=(2.0, 2.0, 2.0), color=(1.0, 1.0, 1.0)),
    'Pavement': Material(image='concrete-paving-small', size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0), color=(0.783, 0.749, 0.689)),
    'Roof': Material(image='flemish-bond-improved', size=(3.0, 1.0, 2.0), color=(0.215, 0.156, 0.101)),
    'RoofSide': Material(image='flemish-bond-improved', size=(3.0, 1.0, 2.0), color=(1.0, 1.0, 1.0)),
    'Shop1': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(0.354, 0.948, 0.775)),
    'Shop2': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(0.692, 0.913, 0.953)),
    'Shop2.001': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
    'Shop3': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
    'WindowFrame': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
}

LIGHTING = Lighting(world_ambient=(0.45, 0.45, 0.45), sun_energy_scale=71.428571, sun_elev_deg=45.0, sun_az_offset_deg=-90.0)
# END AUTO-TUNED

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
        materials=MATERIALS,
        lighting=LIGHTING,
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
        materials=MATERIALS,
        lighting=LIGHTING,
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
        materials=MATERIALS,
        lighting=LIGHTING,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
