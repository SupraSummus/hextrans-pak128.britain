"""Butchery 1840 + 1910 — shared-sprite upgrade pair.

Upstream `butchery.dat` packs four eras; Butchery1820 renders off
the unported `1750-shops.*` atlas and Butchery1945 off the
unported `1950shops.*` atlas (out of scope).  The two middle eras
share the `butchery.*` atlas off `industries/butchery.blend`.
"""

from pak.bake import bake_factory_main
from pak.dat import Factory
from pak.materials import Lighting, Material

_BLEND = "industries/butchery.blend"
_BLEND_WINTER = "industries/butchery-snow.blend"
_UPSTREAM_DAT = "industry/butchery.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

# AUTO-TUNED: pak.tune_industries
MATERIALS = {
    'Brick': Material(image='flemish-bond-improved', size=(0.5, 0.5, 0.5), color=(0.622, 0.53, 0.345)),
    'BrickCapping': Material(image='flemish-bond-improved', texco='ORCO', size=(2.0, 2.0, 2.0), color=(1.0, 1.0, 1.0)),
    'Pavement': Material(image='concrete-paving-small', size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0), color=(0.783, 0.752, 0.695)),
    'Roof': Material(image='flemish-bond-improved', size=(3.0, 1.0, 2.0), color=(0.214, 0.156, 0.101)),
    'RoofSide': Material(image='flemish-bond-improved', size=(3.0, 1.0, 2.0), color=(1.0, 1.0, 1.0)),
    'Shop1': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(0.706, 0.834, 0.549)),
    'Shop2': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.209, 0.699, 0.872)),
    'Shop2.001': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
    'Shop3': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
    'WindowFrame': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
}

LIGHTING = Lighting(world_ambient=(0.45, 0.45, 0.45), sun_energy_scale=71.428571, sun_elev_deg=45.0, sun_az_offset_deg=-90.0)
# END AUTO-TUNED

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
        materials=MATERIALS,
        lighting=LIGHTING,
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
        materials=MATERIALS,
        lighting=LIGHTING,
    ),
]


if __name__ == "__main__":
    bake_factory_main(SPECS, __file__)
