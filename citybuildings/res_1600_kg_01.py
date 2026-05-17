"""RES_KG_1600_00_01 city building."""

from __future__ import annotations

from pak.bake import bake_building_main
from pak.dat import Building
from pak.materials import Lighting, Material

# `color=` overrides converged by `pak.tune_materials` against the
# blurred-all-pixel dRGB metric (`pak.diff.drgb_intersection` at
# sigma=3) under the current LIGHTING; converged value 6.9.  The
# metric averages over all 128*128 pixels including the magic-pink
# background that matches between ours and upstream, so the absolute
# number is suppressed -- per-silhouette-pixel error is ~5x higher.
# Use as a relative optimisation target, not a "we're 6.9 RGB off
# everywhere" claim.  Only `color=`-bearing materials are tuned;
# image-only materials stay at the heuristic `image x blend_diffuse`
# path (which lands closer to upstream by accident, see TODO
# "BI-faithful slot composition replaces, heuristic multiplies").
MATERIALS = {
    "Brick":          Material(image="flemish-bond-improved", size=(0.5, 0.5, 0.5)),
    "Hedge":          Material(image="scratched_bricks_9271", size=(4.0, 4.0, 1.0)),
    "MainColour1":    Material(noise=True, color=(0.956, 1.0, 0.994)),
    "Pavement":       Material(image="concrete-paving-small", size=(2.105, 1.89, 1.0), ofs=(0.0, 0.02, 0.0)),
    "Roof":           Material(image="flemish-bond-impr.001", size=(3.0, 1.0, 2.0), color=(0.357, 0.107, 0.019)),
    "RoofSide":       Material(image="flemish-bond-impr.001", size=(3.0, 1.0, 2.0), color=(0.45, 0.22, 0.18)),
    "Shop3":          Material(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
    "WindowFrame":    Material(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
    "WindowSurround": Material(noise=True, color=(0.18, 0.18, 0.18)),
    "Interior":       Material(noise=True, color=(0.283, 0.328, 0.362)),
}

# Pilot-specific world + sun tune.  Hand-grid-searched against the
# blurred-all-pixel dRGB metric; ambient at 0.55 lifts EEVEE's dark-
# diffuse floor to match upstream's BI ambient term, sun elev 45deg
# better aligns the side-wall shading.  sun_energy scale 2.0/0.028
# is the existing global default kept explicit so the asset's
# lighting recipe is self-contained.
LIGHTING = Lighting(
    world_ambient=(0.55, 0.55, 0.55),
    sun_energy_scale=2.0 / 0.028,
    sun_elev_deg=45.0,
    sun_az_offset_deg=-90.0,
)

# Seeded by `python3 -m pak.extract_materials
# citybuildings/1600-detatched-house-2f-snow.blend` — the upstream
# winter sibling.  Same material names as summer; Roof / Brick drop
# their flemish-bond textures in favour of CLOUDS, picking up the
# snow blend's grey diffuse via flat colour + noise.
MATERIALS_WINTER = {
    # Brick / Brick.003 stay at the .blend's authored dark red-brown
    # diffuse — these are the half-timbered wall's timber frames, not
    # snow surfaces.  Brick.002 (plaster) and Roof get `color=` overrides
    # sampled from the upstream winter atlas (mean RGB inside the
    # silhouette per region): plaster → near-white, roof tile dusted
    # with snow → warm brown-pink.  BI's default CLOUDS slot at fac=1.0
    # paints `mix(diffuse, white, noise)`; we don't have the .blend's
    # Tex datablock so the renderer can't infer the snow tint, hence
    # the per-asset override.
    "Brick":          Material(noise=True),
    "Brick.002":      Material(noise=True, color=(0.78, 0.78, 0.77)),
    "Brick.003":      Material(noise=True),
    # Hedge / Pavement: image+color tint came out brown because the
    # underlying image (dark brick / grey concrete) multiplied by a
    # near-white tint still reads dark.  BI composites image + CLOUDS
    # additively (lerp toward white), which we don't model.  Trade-off:
    # noise+white gives the right snow tint but flattens the bush vs
    # lawn silhouettes upstream gets from the image structure under
    # the snow overlay.  Snow tint wins on dRGB; bush detail lost.
    "Hedge":          Material(noise=True, color=(0.82, 0.82, 0.80)),
    "MainColour1":    Material(noise=True),
    "Pavement":       Material(noise=True, color=(0.85, 0.85, 0.83)),
    "Roof":           Material(noise=True, color=(0.60, 0.50, 0.46)),
    "RoofSide":       Material(image="flemish-bond-impr", size=(3.0, 1.0, 2.0)),
    "Shop3":          Material(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
    "WindowFrame":    Material(image="scratched_bricks_", size=(4.0, 4.0, 1.0)),
    "WindowSurround": Material(noise=True),
}

# Artisan's cottage, perhaps: large, double-fronted.
# Population: estimate 12 per house (including servants) x 5 (low
# density, large gardens) yields 75, / 16 hours * 6.4 hours = 30;
# half when meters/tile is taken into account → 15.
SPEC = Building(
    name="RES_KG_1600_00_01",
    type="res",
    copyright="Kieron",
    level=1,
    chance=50,
    intro_year=1600,
    retire_year=1850,
    needs_ground=1,
    population_and_visitor_demand_capacity=15,
    employment_capacity=0,
    mail_demand=1,
    class_proportion=[0, 40, 100, 75, 0],
    seasons=2,
)
BLEND = "citybuildings/1600-detatched-house-2f.blend"
BLEND_WINTER = "citybuildings/1600-detatched-house-2f-snow.blend"
UPSTREAM_STEM = "citybuildings/images/res/1600-detatched-house-2f.png"


if __name__ == "__main__":
    bake_building_main(
        SPEC, BLEND, __file__,
        materials=MATERIALS,
        blend_winter=BLEND_WINTER, materials_winter=MATERIALS_WINTER,
        lighting=LIGHTING,
    )
