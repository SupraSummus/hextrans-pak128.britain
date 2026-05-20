# Building-bake architecture

Companion to `CLAUDE.md` (engine facts, calibration contract,
bake-unit conventions).

Buildings (`Obj=building` — attractions, monuments, city
buildings, townhalls, HQs, stops, extensions) port via the same
shape as vehicles: a typed `Building` SPEC in a per-asset bake
script with inline bake-meta (`blend=`, `upstream_dat=`,
`materials=`, `blend_winter=`, `materials_winter=`, `lighting=`),
and `bake_building_main(SPEC, __file__)` at the bottom.  The
rendering side multiplies out into per-cell renders driven by
the SPEC's footprint.

**Engine schema** (`descriptor/writer/building_writer.cc`).
Image keys are six-bracket
`backimage[layout][y][x][height][phase][season]` (and `frontimage`
likewise; the engine errors on frontimage with `height > 1`).
`dims=X,Y,Z` parses as `(size.x, size.y, layouts)` — Z is the
number of rotation variants, **not** vertical levels.  Engine
default when Z is omitted: `layouts = (size.x == size.y) ? 1
: 2`.  For odd layouts the y/x loop bounds swap:
`h = (l & 1) ? size.x : size.y`.  `pak.dat.layouts_default` and
`pak.dat.iter_building_cells` mirror this.

**Atlas layout.**  `seasons*heights` rows × `layouts*dims_x*dims_y`
cols.  Row formula `s * heights + h` — each season is a
`heights`-row stripe (summer on top, winter under).  Col formula
`l * dims_x*dims_y + y * w + x` — layouts span columns
left-to-right; within a layout block, `w = (l & 1) ? dims_y :
dims_x` per the engine's swap rule.  For the 1x1xN-layout
single-height single-season case (most current ports) the result
is one row × N cols.  The `iter_building_cells` order
(`s, h, l, y, x`) is canonical for both the dat-side emit and the
renderer-side facing list — keep them in sync or the wrong
sprite paints per tile.

**Seasons.**  Buildings opt in to winter via `SPEC.seasons = 2`
plus `blend_winter=` + `materials_winter=` on the same SPEC.
The upstream `-snow.blend` convention is JP's own: each
blend-sourced building that has winter art ships an adjacent
`<name>-snow.blend` with the same geometry but reshuffled
materials (Roof texture dropped for procedural snow noise, brick
desaturated, ground textured for snow, etc.); the upstream
render script has no season logic, just feeds the snow blend
through the same pipeline.  We mirror this: `bake_building` runs
two `blender -b -P render.py` subprocesses when `seasons >= 2`,
one per blend, and `_stitch_seasons` vertically concatenates the
per-season PNGs (summer on top).  Seed `materials_winter` via
`python3 -m pak.extract_materials <winter-blend>`.

A landmine specific to the `-snow.blend` siblings: many ship
with their geometry collection saved at `hide_render=True` (JP
toggles visibility interactively before rendering, and the saved
state carries the off-toggle).  `pak.render._bake_world_into_meshes`
falls back to lifting `collection.hide_render` on every collection
holding a non-hidden mesh when the per-collection filter yields
zero meshes — Blender's renderer respects the collection flag
regardless of our vertex transforms.

**Per-layout rendering.**  `viewpoints.building_hex_viewpoint
(layouts, dims_x, dims_y)` returns a Viewpoint with one Facing
per `(layout, height)`.  The Facing's `model_rot_z_deg =
(360°/layouts) * l` rotates the model into the layout's
orientation — `layouts=8` spaces facings at 45° (the same set
`HEX_VIEWPOINT` uses for vehicles), `layouts=4` lands face-on
at each cardinal.  Each facing renders the whole footprint into
a canvas sized to the hex screen lattice; per-cell sprites come
from image-space slicing at `hex_tile_screen_offset(qx, ry)`,
not per-cell model translation (artist-authored XYZ contract —
the blend's per-tile anchor placement passes straight through
to pixels).  EEVEE for buildings (vs vehicles' Cycles; see
"Lighting calibration" below).

**Z coefficient.**  `hex_proj_shear`'s z-row coefficient is
`2·sin(60°) = √3` (and `PIXELS_PER_UNIT = W·sin(60°)`), pinned to
upstream square dimetric's `sin(60°)` lift per blend unit.  An
upstream Britain blend authored for dimetric therefore renders at
the same on-screen z extent under hex — no per-asset compensation
in the building viewpoint.  Vehicles and ways inherit the same
shear; rebake any pre-change PNGs to pick up the corrected z
proportions (see TODO.md).

Three landmines the first real building port surfaces:

* **Layout rotation sign.**  `building_hex_viewpoint` uses
  `(360°/layouts) * l` CCW.  The square-projection diff against
  `res_1600_kg_01` lands at mean IoU 0.94 with no clear winner
  between identity and off-diagonal permutation (matrix
  dominated by the building's near-mirror symmetry).  Triggers
  on the first asymmetric building port; see TODO.md → "Building-
  bake layout rotation sign needs asymmetric asset" for the
  concrete probe.
* **Multi-tile centring.**  The standard hex `fit_matrix` is
  scale-only against the model's authored frame, which is right
  for single-tile assets.  For a multi-tile blend whose authored
  frame puts tile (0,0) at world origin (or the footprint centre
  at origin, or somewhere else entirely — unknown upstream
  convention), the per-cell translations may need to compose with
  a per-asset offset.  Surfaces as "every cell renders the same
  part of the model".  Fix: a building-aware `fit_matrix` variant
  in `pak.viewpoints` that anchors on a known footprint
  reference instead.
* **Alignment mode.**  `HEX_VIEWPOINT`'s camera is the
  "vehicles"-alignment Britain blends are authored against;
  upstream's "normal alignment" (`op_list "1"` for stops/
  buildings/road vehicles, `"0"` for 4-view buildings) sits at
  a different camera Z/Y.  The single fixed hex camera the bake
  uses doesn't distinguish; the practical effect is the
  building's ground line lands a few px off.  Diagnose via the
  square-projection diff harness (`pak/diff_buildings.py`), which
  uses the upstream-correct normal-alignment cameras and so its
  residual IoU gap (currently ~6 % for `res_1600_kg_01`) lower-
  bounds the hex render's alignment-mode error.

A fourth, resolved: `Viewpoint.ortho_scale=None` means "use the
blend's authored value", which `building_square_viewpoint` opts
into so the diff renders at the blend's per-pixel scale (vehicles
typically authored at the contributing-graphics convention of 24,
buildings at 12).  Some blends author at a non-standard ortho to
fit surrounding landscape (stonehenge at 72, capturing stones plus
ground planes spanning ~42 world units) -- the SPEC carries
`blend_ortho_per_tile` to override, and both
`building_hex_viewpoint` and `building_square_viewpoint` honour it
to render at the chosen per-tile rate (the square side pins
`camera_ortho = ortho_per_tile * max(dims)` so the 512² stitched
canvas matches upstream's 128-px-per-tile cells stitched onto the
same lattice).  `building_hex_viewpoint` and the hex production
bake otherwise target the pak's intra-tile coord system via
`_compute_fit("hex")`'s `INTRA_TILE_PER_BLEND_UNIT = 2R /
blend_ortho` conversion.

The render side ships end-to-end via `citybuildings/
res_1600_kg_01.py` (1×1×8, `type=res`); the landmines above are
exercised on a single-tile near-symmetric residential, so multi-
tile centring and layout-rotation-sign disambiguation still wait
on a multi-tile asymmetric port.

**Multi-tile pixel ownership.**  A multi-tile sprite carries pixels
from every cell in one wide render, then `Facing.slices` crops one
128² window per tile (positions = `sq_tile_screen_offset(x - xc,
y - yc)` from the per-layout centroid).  A flat crop pulls in
neighbouring tiles' content — upstream pak128.Britain instead
applies a strict per-pixel partition so the engine can paint cells
back-to-front without overdraw.  `sq_tile_pixel_mask` (in
`pak.viewpoints`) builds the clip: every canvas pixel goes to the
tile whose anchor minimises the dimetric L1 distance `|Δx| + 2·|Δy|`
(ties to the closer-to-viewer tile), intersected with the cell-
shape hexagon (apex at top/bottom centre).  Verified zero-pixel
overlap when upstream cells are pasted back onto the canvas.
Bisector lines are diagonals at slope ±2 in the lattice (`sx ±
2·sy = const`), producing the diamond-corner cuts seen in upstream
per-tile sprites.  `building_square_viewpoint` builds one mask per
slice and attaches it via `Slice.alpha_mask`; `pak.compose.
compose_atlas` (parent-side) multiplies the sliced cell's alpha by
the mask.  Hex production
bake still emits `alpha_mask=None` -- the hex-projection ownership
shape is a separate derivation (see TODO.md → "hex-projection
per-tile pixel mask").

**Lighting calibration.**  All upstream PNGs (vehicles, ways,
buildings alike) were rendered in **Blender Internal under Blender
2.79** — confirmed by the contributing-graphics tutorial board 75
topic=17510 (pins Blender 2.79, references BI's OSA-samples
preset 11→16) and the migration thread topic=21677 ("only
openable in Blender <2.80, uses the internal renderer").  BI was
dropped in 2.80 with no upgrade path; everything we render is
therefore a BI substitute.

We pick the substitute per asset class.  Buildings go through
`BLENDER_EEVEE`: Britain's `use_nodes=False` BI materials, with
their flat-Lambert + ambient assumption, render washed-out and
hue-shifted under Cycles' physical BSDF (sun_energy 0.028 lands
as near-zero), but read close enough under EEVEE once ambient
and sun strength are scaled against an upstream PNG.  Vehicles
and ways stay on Cycles — also an empirical substitute, not a
match to upstream's authoring engine (there is no Cycles-rendered
upstream target for any asset class).  Cycles happens to produce
acceptable results on the vehicle/way blends and was the first
substitute tried; switching a flaky-cross-CPU vehicle to
Workbench or EEVEE wouldn't "break upstream calibration" because
no such Cycles-native calibration exists.

`pak.viewpoints.sun_rotation_for_camera(cam_z, elev=30°, az=-90°)`
is the single source of truth for the building sun direction —
used by both the `building_square_viewpoint` (apples-to-apples
diff against upstream's per-cardinal cells, cam_z varies per
facing) and `building_hex_viewpoint` (shipped atlas, cam_z=0).
Sun energy enters via `strip_scene`: each Britain blend ships
its own SUN lamp at the BI-authored `energy=0.028`, which
`render.py::BlendAuthored` captures before stripping the lamp.
Building viewpoints declare `sun_energy=_authored_sun(
_BI_TO_EEVEE_SUN_SCALE)` (= 2.0/0.028 ≈ 71.4) so
`_install_camera_and_sun` resolves to `authored × scale ≈ 2.0`
under EEVEE.  Vehicles/ways pin `sun_energy=_pinned(0.028)`
directly under Cycles where the upstream PNG is the calibration
target.

The remaining EEVEE-substitution magic numbers — sun direction
(elev=30°, az=-90° defaults) and world ambient (0.30 grey in
`pak.render._configure_eevee`) — are the global fallback; per-
asset values land via `lighting=Lighting(world_ambient,
sun_energy_scale, sun_elev_deg, sun_az_offset_deg)` on the SPEC
(see `pak.materials.Lighting`).  The building viewpoint factory
absorbs the Lighting at construction: facing sun rotations get
recomputed against the override, the `sun_energy` callable is
wrapped to apply `Lighting.sun_energy_scale`, and `Viewpoint.
world_ambient` is set from `Lighting.world_ambient` (applied by
`_install_camera_and_sun` after the engine configurer runs).
Today only `res_1600_kg_01` carries one (ambient 0.55, elev 45°);
see TODO → "Lighting overrides exist; only the pilot uses them"
for sweeping the fleet.

Authored `world.color` (Britain blends ship (0.906, 1.0, 1.0))
is *not* extracted: that value was BI's background sky, not its
ambient term, and modern EEVEE's `world.color` IS the ambient
term — so the authored value is the wrong thing to plug in here.

**Per-asset colour solver.**  `pak.tune_materials <bake_script>`
runs an iterative gradient solver on the SPEC's `materials=` dict
against the blurred-all-pixel dRGB metric.  Each step renders the
asset twice (normal + id-map), composites both ours and upstream
onto a common background, blurs σ=3, samples per-material means
from the **blurred** images (σ=0 attribution doesn't track the
σ=3 metric -- neighborhoods average across material boundaries),
proposes `new_color = current_color * (up_mean / our_mean)`
clamped + damped, re-measures.  Only `color=`-bearing materials
get tuned: adding `color=` to an image-only material flips the
heuristic `image x blend_diffuse` path to `image x gain`, a
larger step than the small-gradient iteration assumes.  Opt an
image-only material into solver tuning by giving it an explicit
`color=` starting point in the bake script.

**Texture rebinding.**  Blender 2.80 dropped BI's
`material.texture_slots[i]` API, but the Material+MTex struct
data survives in the .blend binary because Britain's blends are
all saved by 2.42/2.48 (pre-2.5 file format).  The full pipeline:

* **`pak/blend_slots.py`** parses the binary directly to recover
  `tex_type` (IMAGE / CLOUDS / NOISE), `image_name`, `size`,
  `ofs`, `texco` (GLOB / ORCO / UV) per slot, plus per-material
  rgb + alpha.  Not a general .blend parser; targets only what
  building binding needs.
* **`pak/extract_materials.py`** is the one-shot seeder
  (`python3 -m pak.extract_materials <blend>`).  Emits the full BI
  slot stack per material as `Material(slots=[Slot(...), ...])`
  in paste-ready Python source.  The single-slot `image=` /
  `noise=` shorthand forms remain for hand-tuned overrides; the
  slot form is the BI-faithful default.
* **`pak/materials.py`** defines the `Material` and `Slot`
  dataclasses.  Per-material modes (mutually exclusive): a slot
  list (`slots=[Slot(image=..., texco=..., size=..., blend="MIX",
  fac=1.0), ...]`), a single image (`image=..., size=...`), or a
  single noise (`noise=True`).  Optional `color=(r,g,b)` overrides
  the .blend's diffuse as the slot-stack base or noise-band centre.
  `to_jsonable` / `from_jsonable` serialise (slots recursively)
  across the subprocess command line.
* Each `citybuildings/<asset>.py` carries `materials={...}`
  inline on the SPEC.  Once seeded, the dict is the authoritative
  representation -- hand-edits are welcome (JP's authoring
  quirks like a Roof material pointing at the BrownTile-duplicate
  image rather than its sibling `Brick` live as in-place
  comments).
* **`render.py::_bind_textures_via_nodes`** builds the node
  graph per entry, after `_bake_world_into_meshes` runs so the
  GLOB path can read the vertex attribute it populates:
  * `Material(image=..., texco="GLOB")` -> Attribute
    "blend_world_pos" -> Mapping(scale=`size`) -> ImageTexture ->
    Multiply by diffuse colour -> Principled BSDF.  The
    `blend_world_pos` FLOAT_VECTOR vertex attribute is populated
    from the pre-facing-rotation blend-frame coords, so the
    texture stays pinned to the blend frame across per-facing
    model rotation -- BI rendered only-camera-moves and that's
    the behaviour to mirror.
  * `Material(image=..., texco="ORCO")` -> TexCoord.Generated ->
    Mapping(scale=`size`) -> ...  Bbox-normalised per-mesh,
    substitutes BI's object-local projection.
  * `Material(noise=True)` -> Noise -> ColorRamp around the
    diffuse colour.  BI's CLOUDS substitute (single-slot heuristic).
  * `Material(slots=[Slot(...), ...])` -> for each slot, build a
    sub-graph (image: `<coord> -> Mapping -> ImageTexture`;
    procedural: `<coord> -> Mapping -> TexNoise`, with the slot's
    output colour either the parsed Tex ColorBand mapped through
    `ValToRGB` -- when `Tex.flag & TEX_COLORBAND` is set in the
    .blend -- or, much more commonly in the Britain pak, a constant
    `RGB(slot.color)` node carrying the per-slot MTex.r/g/b),
    then chain through `MixRGB(blend_type=slot.blend, fac=slot.fac
    × tex_intensity)` over a running base seeded from the material's
    diffuse (or `color=` override).  Procedural slots' `tex_intensity`
    is the noise.Fac so they partially lerp rather than fully
    replace -- BI-faithful: a CLOUDS slot ships its per-slot RGB
    (e.g. Hedge's `(0.10, 0.06, 0.04)`) and the noise modulates
    influence so low-noise regions show the base while high-noise
    regions lerp toward the slot colour.  `res_1600_kg_01` runs in
    slot form (summer dRGB 37.6); the pilot's L0/L2 vs L1/L3
    asymmetry vs upstream is the open residual -- see TODO ->
    "Multi-slot IMAGE composition shadows the single-slot heuristic".
  * Materials omitted from the SPEC's `materials=` dict render
    flat-diffuse via Blender's `use_nodes=False` auto-conversion.

External texture filepaths in the .blend (`//../../../textures/...`)
are remapped via `_reload_external_textures` to the blends-repo
cache before binding.  Image data blocks whose filepath 404s
(e.g. Pavement's typo'd `concrete-paving-smalll.jpg` path) warn
and fall back to flat diffuse rather than failing the bake -- see
TODO → "Pavement texture file missing from upstream blends repo".

`pak.blend_slots` recovers per-axis size/ofs/texco but not per-
vertex UV coords, so the rebinding gets per-region means right via
GLOB / ORCO substitutes but not per-vertex detail — `res_1600_kg_01`'s
~30 dRGB floor is this gap, not solver under-tuning.  Closing it
would mean re-authoring blends with proper UVs + node materials
(~500 blends), sidecar Blender 2.79b in the bake sandbox (breaks
determinism), or shipping new hex-native materials.  None planned.
