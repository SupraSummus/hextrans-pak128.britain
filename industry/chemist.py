"""Chemist 1860 + 1955 — shared-sprite upgrade pair.

Upstream `chemist.dat` packs three eras under one upgrade chain; the
first two render off `industries/chemist.blend` and the third
(Chemist1975) repoints at the unported `1950shops.*` atlas — out of
scope for this bake unit.  The two-era SPECS share one atlas via the
shared-sprite multi-object pattern (mirrors `air/dragon_rapide.py`).

`upgrade=` lists drop `Chemist1975` to avoid a dangling reference;
re-add when the 1950shops bake unit lands and restores that era.
"""

from pak.bake import bake_main
from pak.dat import Factory
from pak.materials import Lighting, Material

_BLEND = "industries/chemist.blend"
_BLEND_WINTER = "industries/chemist-snow.blend"
_UPSTREAM_DAT = "industry/chemist.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

# AUTO-TUNED: pak.tune_industries
MATERIALS = {
    'Brick': Material(image='flemish-bond-improved', size=(0.5, 0.5, 0.5), color=(0.619, 0.53, 0.345)),
    'BrickCapping': Material(image='flemish-bond-improved', texco='ORCO', size=(2.0, 2.0, 2.0), color=(1.0, 1.0, 1.0)),
    'Pavement': Material(image='concrete-paving-small', size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0), color=(0.78, 0.754, 0.694)),
    'Roof': Material(image='flemish-bond-improved', size=(3.0, 1.0, 2.0), color=(0.215, 0.155, 0.1)),
    'RoofSide': Material(image='flemish-bond-improved', size=(3.0, 1.0, 2.0), color=(1.0, 1.0, 1.0)),
    'Shop1': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(0.863, 0.537, 1.135)),
    'Shop2': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
    'Shop3': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
    'WindowFrame': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
}

LIGHTING = Lighting(world_ambient=(0.45, 0.45, 0.45), sun_energy_scale=71.428571, sun_elev_deg=45.0, sun_az_offset_deg=-90.0)
# END AUTO-TUNED

SPECS = [
    Factory(
        name="Chemist1860",
        copyright="James",
        seasons=2,
        level=15,
        intro_year=1860, intro_month=11,
        retire_year=1955, retire_month=10,
        climates=_CLIMATES,
        population_and_visitor_demand_capacity=80,
        employment_capacity=20,
        mail_demand=6,
        class_proportion=[15, 20, 35, 15, 15],
        class_proportion_jobs=[20, 30, 70, 0, 0],
        upgrade=["Chemist1955"],
        location="City",
        productivity=2,
        range=1,
        distributionweight=18,
        mapcolor=215,
        electricity_amount=1,
        electricity_boost=320,
        passenger_boost=600,
        mail_boost=400,
        inputgood=["pharmaceuticals"],
        inputcapacity=[16],
        inputfactor=[100],
        blend=_BLEND,
        blend_winter=_BLEND_WINTER,
        upstream_dat=_UPSTREAM_DAT,
        materials=MATERIALS,
        lighting=LIGHTING,
    ),
    Factory(
        name="Chemist1955",
        copyright="Kieron & WLindley",
        seasons=2,
        level=18,
        intro_year=1955, intro_month=7,
        retire_year=1975, retire_month=12,
        climates=_CLIMATES,
        population_and_visitor_demand_capacity=120,
        employment_capacity=25,
        mail_demand=8,
        class_proportion=[20, 20, 30, 15, 15],
        class_proportion_jobs=[0, 40, 75, 5, 0],
        upgrade=[],
        location="City",
        productivity=3,
        range=2,
        distributionweight=21,
        mapcolor=215,
        electricity_amount=1,
        electricity_boost=1000,
        passenger_boost=600,
        mail_boost=400,
        inputgood=["pharmaceuticals"],
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
    bake_main(SPECS, __file__)
