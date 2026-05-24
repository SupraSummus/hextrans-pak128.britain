"""HardwareShop 1850 — single-era port.

Upstream `hardware-shop.dat` packs four eras off four distinct
atlases; only HardwareShop1850 renders from
`industries/hardware-shop.blend`.  The earlier `hardware-shop-early`
and later `hardware-shop-deco` / 1950s atlases stay unported.
"""

from pak.bake import bake_main
from pak.dat import Factory
from pak.materials import Lighting, Material

_BLEND = "industries/hardware-shop.blend"
_BLEND_WINTER = "industries/hardware-shop-snow.blend"
_UPSTREAM_DAT = "industry/hardware-shop.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

# AUTO-TUNED: pak.tune_industries
MATERIALS = {
    'Brick': Material(image='flemish-bond-impr', size=(0.5, 0.5, 0.5), color=(0.623, 0.535, 0.349)),
    'BrickCapping': Material(image='flemish-bond-impr', texco='ORCO', size=(2.0, 2.0, 2.0), color=(1.0, 1.0, 1.0)),
    'Pavement': Material(image='concrete-paving-small', size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0), color=(0.795, 0.761, 0.699)),
    'Roof': Material(image='flemish-bond-impr', size=(3.0, 1.0, 2.0), color=(0.217, 0.159, 0.105)),
    'RoofSide': Material(image='flemish-bond-impr', size=(3.0, 1.0, 2.0), color=(1.0, 1.0, 1.0)),
    'Shop1': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(0.673, 0.716, 1.373)),
    'Shop2': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.052, 1.272, 0.367)),
    'Shop2.001': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
    'Shop3': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
    'WindowFrame': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
}

LIGHTING = Lighting(world_ambient=(0.45, 0.45, 0.45), sun_energy_scale=71.428571, sun_elev_deg=45.0, sun_az_offset_deg=-90.0)
# END AUTO-TUNED

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
    materials=MATERIALS,
    lighting=LIGHTING,
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
