"""Bookshop 1750 — single-era port.

Upstream `bookshop.dat` packs five eras off four distinct atlases;
only Bookshop1750 renders from `industries/bookshop.blend`.  The
victorian / deco / 1950s eras (bookshop-victorian, bookshop-deco,
1950shops) are out of scope until those blends or atlases port.

No `bookshop-snow.blend` exists upstream; `seasons=1` drops the
upstream's winter slots until a snow blend lands.
"""

from pak.bake import bake_main
from pak.dat import Factory
from pak.materials import Lighting, Material

_BLEND = "industries/bookshop.blend"
_UPSTREAM_DAT = "industry/bookshop.dat"

_CLIMATES = "rocky,tundra,temperate,mediterran,desert,arctic,tropic"

# AUTO-TUNED: pak.tune_industries
MATERIALS = {
    'Brick': Material(image='flemish-bond-improved', size=(0.5, 0.5, 0.5), color=(0.491, 0.442, 0.301)),
    'Hedge': Material(image='scratched_bricks_9271', size=(4.0, 4.0, 1.0), color=(0.229, 0.578, 0.316)),
    'Material.001': Material(image='grey_roof_slate.jpg', texco='ORCO', size=(20.0, 20.0, 20.0), color=(0.81, 0.859, 0.825)),
    'Pavement': Material(image='concrete-paving-small', size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0), color=(0.774, 0.776, 0.714)),
    'Roof': Material(image='flemish-bond-improved', size=(3.0, 1.0, 2.0), color=(1.0, 1.0, 1.0)),
    'Shop2': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(0.58, 1.656, 2.5)),
    'Shop2.001': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
    'Shop3': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
    'Stone Wall': Material(image='stonewall-texture.jpg', color=(1.518, 1.401, 1.351)),
    'WindowFrame': Material(image='scratched_bricks_.001', size=(4.0, 4.0, 1.0), color=(1.0, 1.0, 1.0)),
}

LIGHTING = Lighting(world_ambient=(0.45, 0.45, 0.45), sun_energy_scale=71.428571, sun_elev_deg=45.0, sun_az_offset_deg=-90.0)
# END AUTO-TUNED

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
    materials=MATERIALS,
    lighting=LIGHTING,
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
