# TODO.md

Open work for the hex port of the Britain pakset.  Rules: see
`CLAUDE.md` → "TODO.md rules".

## Starting spine

A small spine that gets the engine to draw something Britain-ish
under hex.  Order is rough — later items have soft triggers on
earlier ones.

**Port a multi-object vehicle.**  Five single-object ports
exist now (1850s-first, open-third, br-cl15, br-9f,
blackpool-brush), so the seeder workflow + the `bake_main`
single-vehicle convenience are validated.  The multi-object
path — one bake script emitting N dat+png pairs — is still
on-paper-only.  Concrete next move: pick a multi-object
upstream like `gwr-king` (loco + tender) and run a bake script
that calls `bake_vehicle` twice with distinct `basename` (and
typically distinct `blend`) per output.  Will surface how blends
map to objects (one blend per object? one blend with multiple
collections? unknown until we look at one) and whether
`bake_main` should sprout a multi-spec variant.

**Expand build scope as categories bake.**  `make all` compiles
`grounds/`, `air/`, `trains/`, `trams/` today — the categories
with at least one ported asset (`.dat`/`.png`/`.py` triple).
Other Makefile `DIRS*` lines stay commented out as scope
statement; per-dir, the `ported_dats` filter feeds only the
`.dat` files with a sibling `.png` to makeobj, so re-enabling a
dir doesn't drag in its unported upstream `.dat` files (e.g.
`trains/` has 866 unported dats against 4 ported, and the build
ignores the 866 without touching them).  Concrete next move when
a new category's first asset is ported: uncomment its
`DIRS128 += <dir>` (and matching `TR_DIRS += <dir>`) line, push,
watch CI go green.

**Vehicle render rebake in CI.**  The `reemit-dats` lint job
re-emits every vehicle bake unit's `.dat` from its `SPEC` and
asserts byte-identical, but the *render* side (atlas PNG) isn't
wired — vehicle bakes need Blender + `libegl1` + a per-asset
blend fetch (~minutes of Cycles per asset).  Concrete next move
when the bake catalog grows past the ~5-asset spike: a
`rebake-vehicles` job gated on diff-detected `bake.py` or
`blends.lock` changes (path filter on the workflow trigger),
installing Blender once and only rebaking the touched assets.
`CLAUDE.md` → "CI" notes this gap.  Trigger: when drift in
committed vehicle atlases is first observed (or when ~10
vehicles are baked, whichever comes first).

**Multi-object reemit hook.**  `pak/reemit_dats.py`
introspects each bake script's `SPEC: Vehicle` attribute and
re-emits one `.dat` per script.  Multi-object bake units (one
script emits N dat+png pairs — designed but not yet exercised,
see "Bake units and per-asset layout" in `CLAUDE.md`) have no
single `SPEC` and won't fit this shape; the worst case is a
script with `SPEC` *plus* an additional tender output that gets
silently missed.  Concrete next move when the first multi-object
bake unit lands: replace the `SPEC` introspection with a
per-script `reemit_dats(out_dir)` hook (or a `SPECS` list +
basename map convention), and update the existing single-object
scripts to expose the hook.  Trigger: first multi-object port.

**Freight-image subsystem unmodelled.**  Hex `vehicle_writer.cc`
reads `freightimage[<dir>]` (single-freight visual variant),
`freightimage[N][<dir>]` (multi-freight, per good), and
`freightimagetype[N]` (good-name → image-index map).  `Vehicle`
doesn't have fields for these, and `emit_vehicle` doesn't bake
freight atlas variants.  Doesn't matter for passenger carriages
(no visual variation by load) but absolutely matters for coal
trucks / tankers / container flats.  Concrete next move when the
first freight wagon ports: add fields + extend the bake script's
atlas pass to render per-freight variants, with a naming
convention like `<basename>.png` (empty) plus
`<basename>_<good>.png` per loaded variant.  Soft trigger.

**Sparse way_constraint indexing.**  Upstream uses sparse,
category-indexed flag lists like `way_constraint_permissive[1]=1`
and `way_constraint_prohibitive[0]=0` — the index is the
constraint category, the value is the per-category flag.
`Vehicle.way_constraint_permissive` is currently a dense `list[str]`
which can only emit `[0]=, [1]=, …` densely, and there's no
`way_constraint_prohibitive` field at all.  `blackpool_brush`
drops both keys on port (see its comment).  Concrete next move
when the second tram/road vehicle that uses these ports: model
the field as `dict[int, int]` (or similar), add
`way_constraint_prohibitive` back, and teach `emit_vehicle` to
walk dict items.  Soft trigger.

**Hex viewpoint output validation.**  `render.py` with
`HEX_VIEWPOINT` is believed-correct on paper and shares its
pipeline with the square viewpoint (which passes the upstream IoU
diff at 0.93+), but the hex projection itself has no quantitative
reference -- the upstream pak only ships square-dimetric PNGs.
4wheel-1850s-first's atlas visually confirms shading and facing
layout look right (W/E read as carriage side views; wheels sit at
tile centre), but that's eyeball-verification.  Concrete next
move: pixel-compare a `HEX_VIEWPOINT` output of a procedural
reference cube against the same cube through
`hextrans-pak128/tools/threed/render.py::HexCamera`; they should
agree to within renderer noise.  Trigger: any second-asset bake.

**Ground bake gaps: way_ground, fence.**  Eight parametric ground
families port from pak128 live under `grounds/*.py` now
(light_texture, back_wall → slopes + basement, marker, borders,
water, sidewalk, shore_trans, slope_trans); `climate_texture` is
vendored from upstream pak128.Britain verbatim (see
`grounds/climate_texture.{png,dat}`) as biome-art-without-tile-
geometry — replace with a Britain-flavoured hex-native palette when
in-game appearance warrants.  Two pieces still missing.  `way_ground` is
the per-`(axis, slope)` ground lightmap for tiles carrying a way — a
parametric per-slope shading bake, not a way render.  Concrete next
move: port pak128's `landscape/grounds/way_ground/` directly into
`grounds/way_ground.py`, expressing the three faces via
`pak.hex_synth.fill_polygon` in the engine's screen-space Lambert
frame (the same path the existing `grounds/light_texture.py` /
`grounds/borders.py` bakers use).  Don't re-port a Model / Camera
mini-rasterizer for this — the engine-space Lambert frame is
sufficient.  `grounds/fences.dat`
(`Obj=ground Name=Fence`) is the boundary fence at climate
transitions; the upstream stub references photographic
`images/fence-*.png` stripped from history, same un-ported state as
the train / building dats waiting on per-asset bakes.  Concrete next
move: write `grounds/fence.py` as a small procedural baker (low-side
hex edges under a simple wood-rail palette), keyed by slope,
mirroring the marker / borders shape; delete the upstream stub once
the baker emits a real `fence.{png,dat}`.

**Lightmap multiplier scale mismatch.**  The square-bake diff
against upstream `grounds/images/texture-lightmap.png` shows a
consistent ≈ 1.1–1.4× brightness ratio across slopes — our flat
cell renders grey 132, upstream's renders grey 188.  The Lambert
*shape* is right (cell IoUs sit at 0.90–0.99 even on the worst
multi-region slopes); only the absolute scale differs.  That's
`pak/lightmap.py::brightness_to_grey_rgb`'s
`create_textured_tile` convention — `gray5 = brightness/16` lands
flat at gray8 ≈ 132 for the hex engine's multiplier path, but
pak128-standard's `create_textured_tile` uses a different scale.
Concrete next move when the hex engine's lightmap path is
validated in-engine (i.e. we can see the actual rendered ground
under climate-texture multiplication): if the result reads too
dark, parameterise `brightness_to_grey_rgb` by a per-projection
multiplier scale and bump it for the hex engine to match
upstream's apparent brightness.  Soft trigger.

**Square-bake diff harness coverage.**  `pak/diff_grounds.py`
runs a parametric ground baker through `pak.square_synth.SquareGeom` and
pixel-diffs against the upstream pak128.Britain authored cell atlas,
exercising slope decode + region partition + Lambert + polygon fill +
atlas layout end-to-end.  Only `light_texture` is wired into the
`ASSETS` table today (mean IoU 0.97 vs `grounds/images/texture-lightmap.png`,
min 0.90 on the most-sloped triple-region cells); the other procedural
bakers — `slopes`/`basement` (`back_wall.py`), `sidewalk`, `marker`,
`borders`, `water` — have upstream square counterparts under
`grounds/images/` (e.g. `ground-slope-walls-128.png`,
`ground-newfoundation-128.png`, `ls-water-128.png`) and would each
benefit from an `ASSETS` entry.  Concrete next move per baker: identify
the upstream PNG + dat object name, add the entry, run the diff, fix
any < 0.90 IoU regressions surfaced (likely 1-pixel rasterisation
offsets at corner ramps, or palette-multiplier scale mismatches that
the harness reports as `ratio ≠ 1.0`).

**Way square-projection diff harness.**  Mirror of
`pak/diff_grounds.py` for ways: per-ribi pixel diff (silhouette IoU
+ intersection-restricted mean abs(RGB-delta)) of our square bake
against upstream pak128.Britain's authored cells.  The
**infrastructure** is in place — `pak/bake_way.py --projection
square` walks the 15 square ribis through the same composition
pipeline hex uses (clone → place on chord → bisect at caps +
4 tile-outline planes → render), driven by `pak.way_proj.
SQUARE_PROJECTION` (`SQUARE_VIEWPOINT["S"]` camera + ortho_scale=24
+ NSEW edges at world ±12 + canonical NSEW-ordered ribi labels).
The **diff** itself doesn't exist yet.  Concrete next move: add
`pak/diff_way.py` that drives the bake with `--projection square
--cell-dir <tmp>`, reads upstream's atlas via `fetch_pak`
(`ways/images/concrete_sleeper_steel_rail.png` for cssr; cell
layout 6 cols × 5 rows of 128-px cells, per-ribi `Image[NS] = .1.0`
mapping in the upstream `.dat`), per-cell shifts our render's bbox
onto the upstream's bbox to absorb the alignment offset (upstream
uses "vehicles"-alignment camera positions calibrated for
ground-clearance, not centred on origin), and reports per-ribi
IoU + colour delta.  Failure modes the diff is expected to surface:
`SQUARE_TILE_HALF = 12.0` is currently a guess; the alignment
shift is currently un-modelled; the V-bend approximation of
upstream's 90°-curve corner cells will read poorly until corners
are special-cased (or the topology layer learns about arcs).  The
diff is the right tool to drive each of those calibrations.

Once the diff lands and forces a real second consumer of the
`Projection` accessors, the topology-duplication consolidation
called out in CLAUDE.md → "Way-bake architecture" becomes the
natural follow-up: collapse `_square_*` helpers in `pak/way_proj.py`
back into `pak/way_topology.py` parametrised on a `tile`-geom arg.

**Way camera + tile-chord validation.**  `bake_way.py` copies
`HEX_VIEWPOINT`'s camera + sun + `hex_proj_shear()` extrinsic
(tuned for vehicle bakes with `fit_kind="hex"`), and assumes the
atom's scale gives flush rail joins between adjacent tiles.  Both
are unverified.  Concrete next move once the square diff
converges: render two adjacent hex tiles + check edge alignment
pixel-by-pixel; if rails don't meet flush across the shared edge
midpoint, a small tile-overlap fraction is needed (strand longer
than chord by a cap-mitre-worth).  The procedural-cube-vs-engine
probe described in the original "validate the hex camera setup"
entry remains the way to pin the camera independently of the
rail.

  * **Ground-plane material.**  The blend's `Transparent` material
    is non-noded and renders as flat grey; the
    `concrete-paving-small` image is meant to drive it as a ballast
    texture.  Either re-attach the image via a node tree at bake
    time or replace the ground plane with a procedural ballast.

  * **Cycles non-determinism.**  Re-running `bake_way.py` produces
    a byte-different PNG each time (Cycles sampling).  Pinning the
    Cycles seed + sample count + denoiser is needed before the
    bake can land in CI as a `git diff --exit-code` check.

  * **Per-blend strip lists belong in a per-asset bake script.**
    `bake_way.py` default-strips `Sphere` only; other Britain way
    blends may carry their own noise meshes (e.g. ruler / silhouette
    debug objects).  Move the strip declaration into a future
    `ways/<asset>.py` Blender-driver wrapper once the asset count
    grows past 1.  Don't extrapolate the default strip-list from
    one blend.

**Bulk-strip remaining unported upstream dats?**  Each upstream
dat is deleted once its bake script's SPEC verifies (CLAUDE.md →
"Bake units" → "Upstream dats get deleted once ported"), but
that's per-asset.  Until the catalog is ported, ~870 unported
flat dats sit in `trains/` alongside the per-asset triples; they
can't compile (their PNG refs target stripped image dirs) and
would `Name=`-collide with the eventual ports.  Concrete next
move when makeobj-on-tree first matters: either let the
incremental per-port deletes drive it, or strip them all up
front and fetch via `pak.lock` when seeding new ports.  Soft
trigger.

After the spine: expand by asset family (rail vehicles, road
vehicles, buildings, industries).  Per-family progress is
recorded by deleting that family's entry from this file when it's
done, not by adding "completed" notes.

## Open design questions

**Atlas commit vs. CI-artefact-only.**  Default is commit (per
`CLAUDE.md` → "Per-asset directory layout") but reversible.
Switching to CI-artefact-only saves repo bytes at the cost of
"see the change in the PR".  Concrete next move: measure committed
atlas size after the first ~10 asset bakes; if the cumulative is
under 10 MB this question retires.  Trigger: ten assets baked.

**Engine facing count cutover.**  Vehicles currently bake under
the engine's 4-or-8-direction convention with hex-heading
remapping.  Once the engine ports to a native 6-direction layout
(see `hextrans/TODO.md` → "ribi cutover" and the related
roadsign / runway entries), every directional asset baked under
the old convention needs a rebake.  Concrete next move when
that engine port lands: bump `blends.lock` (if helpful) and run
the full CI rebake; otherwise no work needed until then.  Soft
trigger.

**Aircraft alpha-blend materials render too transparent.**
`air/dragon_rapide` lands at IoU 0.84-0.92 across facings —
contour-failed by the 0.93 calibration bar.  Bboxes match upstream
within ±1 px on all 8 facings; the XOR is interior holes, 12-51
upstream-only pixels per facing concentrated in the cockpit/glass
region, our alpha 0-16 there (`diff_upstream` diagnostic dump
under S facing, only_up bbox (49,79)-(80,97)).  Almost certainly
the cockpit-window / glass materials carrying alpha-blend that
Cycles renders semi-transparent where upstream's older pipeline
rendered opaque.  Trains weren't affected (4wheel-1850s-first
worst IoU 0.93 on identical render.py).  Concrete next move: try
forcing `mat.blend_method = 'OPAQUE'` (or `'CLIP'`) on every
material in `render.py`'s scene-prep, rerun `check.py --all`,
confirm trains don't regress, then rebake the plane.  If that
breaks something legitimate (e.g. a future asset wants real
translucent glass), gate it behind a Viewpoint flag.  Trigger:
already in the way — diff_upstream fails CI on the dragon-rapide
port until this is resolved.

**`sp_*` player-colour mask pass.**  Upstream blends use a
`sp_*` material naming convention for player-colour masks (see
`render_SimutransRender_pak128Britain-65.py` "Make Masks" path).
render.py renders the native materials only; the mask render
is a second pass that swaps those materials for the engine's
mask palette and emits a parallel `_mask.png` set the dat
references via `EmptyImage[FRONT-...]` etc.  Concrete next move:
port the material-swap code from the upstream `-65` script into
a `--mask` mode on render.py.  Trigger: first asset that
gameplay-actually-needs livery support (probably a BR-era loco).

**Multi-tile asset overflow.**  `HEX_VIEWPOINT`'s `fit_kind="hex"`
applies a single pakset-wide scale (`2R / upstream_ortho_scale = 2R/24`)
under the calibration contract documented in CLAUDE.md, so a long loco
at its real upstream size will render larger than one cell.  The atlas
is currently one row of W×W cells; a mainline loco needs to be
sliced across multiple cells with a known per-cell offset, matching
the engine's multi-tile vehicle convention.  Concrete next move
when the first mainline-loco-length asset is ported: extend
`render.py` to emit multi-cell atlases driven by the model's
post-scale extent, and wire the resulting cell layout into the
`.dat`.  Soft trigger.
