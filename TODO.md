# TODO.md

Open work for the hex port of the Britain pakset.  Rules: see
`CLAUDE.md` → "TODO.md rules".

## Starting spine

A small spine that gets the engine to draw something Britain-ish
under hex.  Order is rough — later items have soft triggers on
earlier ones.

**Port a distinct-sprite multi-object vehicle.**  Shared-sprite
multi-object is exercised by `air/dragon_rapide.py` (`SPECS = [
PASSENGER, MAIL]` → one combined dat sharing one atlas).
Distinct-sprite (loco + tender, EMU set, carriage family — N
separate `<basename>.{dat,png}` triples driven by per-output
`bake_vehicle` calls in one script) is still on paper.  Concrete
next move: port `gwr-king` (loco + tender) — open the upstream
blends, see whether loco and tender ship as one .blend with
collections or two separate .blends, then write the bake script
calling `bake_vehicle` twice with distinct `basename` (and likely
distinct `blend`) per output.  Drops the 6 livery refs (extended-
only).  Will also force the reemit hook (see next entry).

**Expand build scope as categories bake.**  `make all` compiles
`grounds/`, `air/`, `trains/`, `trams/`, `ways/` today — the
categories with at least one ported asset (`.dat`/`.png`/`.py`
triple).
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

**Distinct-sprite reemit hook.**  `pak/reemit_dats.py` now handles
`SPEC` (single) and `SPECS: list[Vehicle]` (shared-sprite multi-
object, one combined dat).  Distinct-sprite multi-object scripts
(one script emitting N `<basename>.{dat,png}` triples — designed
but not yet exercised) still don't fit: the worst case is a
script with `SPEC` plus an additional tender output that gets
silently missed.  Concrete next move when the first distinct-
sprite bake unit lands (`gwr-king` is the canonical candidate):
add a per-script `reemit_dats(out_dir)` hook convention and have
`_reemit` prefer it over `SPEC` / `SPECS` introspection.  Trigger:
distinct-sprite multi-object port.

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
translucent glass), gate it behind a Viewpoint flag.  Soft
trigger — `check.py` isn't CI-gated, so the failure sits in
local-run output until somebody wires `--all` into the lint
workflow.

**Engine facing count cutover.**  Vehicles currently bake under
the engine's 4-or-8-direction convention with hex-heading
remapping.  Once the engine ports to a native 6-direction layout
(see `hextrans/TODO.md` → "ribi cutover" and the related
roadsign / runway entries), every directional asset baked under
the old convention needs a rebake.  Concrete next move when
that engine port lands: bump `blends.lock` (if helpful) and run
the full CI rebake; otherwise no work needed until then.  Soft
trigger.

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


**Building lighting needs re-calibration against the new MATERIALS
baseline.**  The previous EEVEE-substitution knobs
(`_BI_TO_EEVEE_SUN_SCALE` ≈ 71.4, sun direction elev=30°/az_offset=-90°,
world ambient 0.30 grey) were grid-searched against a hand-coded
material-binding path (now retired -- see "Building material binding
now reads BI MTex slot data" above).  Under the new slot-driven
binding the fleet-mean dRGB shifted slightly (res_1600 from 26.6 to
30.6; fleet mean from ~30.7 to ~32.2 excl gasometer) because the
old hand-tuned `_TEX_TILE` frequencies were themselves part of the
lighting fit.  Per-asset preferences still disagree (res_kg_1920's
opposing-ambient need is structural, not fixed by material data).
Concrete next move: re-run the 12-point grid (elev=0, az ∈
{-90,-45,+45,+90}, amb ∈ {0.15,0.30,0.50}) on the 6-asset fleet
under the new MATERIALS path; if no global beats the current
baseline, move sun + ambient into a per-asset `LIGHTING` dict on
`Building` SPEC (mirroring how ways carry per-recolour
`MATERIALS`), defaulting to today's fleet values; calibrate
townhouse and detached houses independently.

**Pavement texture file missing from upstream blends repo.**
Multiple Britain blends reference a `concrete-paving-small` Image
data block whose filepath points to `//../../../concrete-paving-
smalll.jpg` (note the triple-l typo) -- a path that 404s against
`blends.lock`'s SHA-pinned upstream.  `_resolve_image` returns
None for these and `_bind_textures_via_nodes` warns + falls back
to flat diffuse, so the bake completes but Pavement / Tiles etc.
on res_1600, the townhouse, both detached houses, and the
gasometer renders without their authored texture.  Concrete next
move: grep the blends repo for any remaining `concrete-paving-*`
asset, work out whether the typo is fixable upstream or whether
the file was lost in a directory rename.  Until then, every
Britain blend referencing this image lands at higher dRGB than it
should (interior shading shows the diffuse colour with no surface
detail).

**Gasometer renders see-through under EEVEE.**  Symptom:
ind_1860_jh_gasometer sits at IoU 0.80 / dRGB 65 vs the fleet's
~0.92 / ~30, with the silhouette XOR red+blue across the upper
half of the tank.  `pak/blend_slots.py` reads `Material->alpha`
authoritatively from the .blend binary; on the gasometer only the
small `Transparent` material (on a 4-vert decorative plane) has
alpha < 1, while every outer-tank material (`Material.001..003`,
`MainColour1.001`) is alpha=1.  So the translucent appearance
upstream isn't from per-material alpha at all -- likely a BI
ZTRANSP / raytrace-transparency / use_transparency flag the
.blend stores in a field `pak.blend_slots` doesn't currently
extract.  Concrete next move: extend `blend_slots.extract` to
read `Material.mode` (BI's flag bitfield; `MA_ZTRANSP=1<<6`,
`MA_RAYTRANSP=1<<9`); audit the gasometer materials for which
flags are set; route those through a (future) renderer integration
that uses node-graph alpha -- a fresh-eyes test confirmed
`use_nodes=False` + `blend_method='BLEND'` + `diffuse_color[3]<1`
is a no-op under EEVEE 4.0, so any alpha integration has to build
a real Principled BSDF graph with the Alpha socket wired.

**Pixel-perfect building match needs UVs (or new materials).**
The ~30 dRGB floor on `res_1600_kg_01` is set by BI's lost UVs --
slot data via `pak.blend_slots` recovers per-axis size/ofs/texco
but not per-vertex UV coords.  Three ways to close it if it
becomes a goal: (1) re-author every Britain blend with proper
UVs + node-based image textures (~500 blends, content work);
(2) sidecar Blender 2.79b with BI in the bake sandbox (breaks
cross-renderer determinism); (3) ship new hex-native materials
authored from scratch (artistic divergence from upstream).
Today's `_bind_textures_via_nodes` gets the per-region mean
right via slot-driven `blend_world_pos` (GLOB) or `Generated`
(ORCO) coords + the slot's authored `size`, and per-asset
material color via `MixRGB(MULTIPLY, diffuse_color)` -- the
remaining gap is per-vertex UV detail.  No concrete next move
unless one of the three is chosen.

**Multi-tile vehicle overflow.**  `HEX_VIEWPOINT`'s `fit_kind="hex"`
applies a single pakset-wide scale (`2R / upstream_ortho_scale = 2R/24`)
under the calibration contract documented in CLAUDE.md, so a long loco
at its real upstream size renders larger than one cell.  The vehicle
atlas is one row of W×W cells; a mainline loco needs to be sliced
across multiple cells with a known per-cell offset, matching the
engine's multi-tile vehicle convention.  The per-cell-translation
scaffolding now exists for buildings
(`viewpoints.building_hex_viewpoint`, `Facing.model_translation`,
`pak.dat.iter_building_cells`); a vehicle version follows the same
pattern but the multi-cell convention for `vehicle_writer.cc` is a
different schema than `building_writer.cc`'s `[layout][y][x]` grid.
Concrete next move when the first mainline-loco-length asset is
ported: read the engine's multi-tile-vehicle convention out of
`vehicle_writer.cc` (it's a per-image-slot offset list, not a
footprint), add a `vehicle_hex_viewpoint(n_cells)` factory beside
the building one, and wire the resulting cell layout into the dat.
Soft trigger.

**Per-blend layout-to-cardinal authoring isn't uniform upstream.**
Square-projection diff across the six new asymmetric ports lands
at best-perm IoU ~0.93 (pipeline renders correctly) but the
permutation differs per blend: 1890/1920 detached houses + 1970
office land on `[2,3,0,1]` (matches upstream when read through
upstream's own `[2,1,0,3]` L→col mapping), while 1870 pub +
1870 townhouse land on `[1,2,3,0]` — i.e. our L0 == upstream's
L1, one cardinal off.  Survey of 47 upstream dats: 68 entries use
L→col `(2,1,0,3)`, 19 use identity `(0,1,2,3)`, 27 use degenerate
`(0,0,0,0)` (one-layout dats), plus three smaller outliers — no
single global convention to flip a sign against.  The L assignment
in upstream's `BackImage[L]=...0.col` lines records *which
direction the artist drew the blend's "front" facing*, not a
pipeline-side rotation.  Under the hex 6-layout policy with
uniform `simrand` placement the per-L mismatch is gameplay-
invisible, but artistically inconsistent across the pak.  Concrete
next moves if uniformity matters: (a) per-script `LAYOUT_OFFSET`
override on the cardinal-zero angle, calibrated by inspection; or
(b) accept the upstream's per-blend orientation as authored.
Closes the original "rotation sign" probe.

**Building square-projection diff: multi-tile + heights coverage.**
`building_square_viewpoint` errors on `dims_x*dims_y > 1` or
`heights > 1`; only layout permutation diffing works today.  Adding
multi-tile diff needs a square tile lattice mirroring
`HEX_KOORD_Q_WORLD` / `HEX_KOORD_R_WORLD` — pak128's
square-dimetric tile spans 128 px on screen, so the world-space
inter-tile offset is `(±SQUARE_TILE_HALF, ±SQUARE_TILE_HALF)`
along the screen diagonal.  Trigger: first 2x1+ building port.
Heights coverage triggers on the first port with rendered
silhouette overflowing one cell vertically.

**Multi-tile centring** — `fit_kind="hex"` centres on the model's
XY bbox, which may not match upstream's per-tile-anchor convention
for multi-tile blends; first 2x1+ building port surfaces this.

**Multi-tile building bake.**  `res_1600_kg_01` is 1×1×4 — the
multi-tile axis (`dims_x>1` or `dims_y>1`) of `building_hex_viewpoint`
is unit-tested via `iter_building_cells` but unverified end-to-end.
Concrete next move: pick a 1×2 or 2×1 upstream building with a
matching blend (`town-house`, `terrace-row-house-2f`, or similar
in `citybuildings/`), port it, observe whether the two cells'
content correctly stitches at the shared tile edge in-engine.

**Building schema gaps.**  `pak.dat.Building` covers attractions,
monuments, city buildings (res/com/ind), townhalls, HQs, stops,
extensions — the dat shapes around the engine's `obj=building`
type field.  Two known gaps: (a) **Factory schema** —
`Obj=factory` (industries like brewery, bakery, fishing-ground)
carries `Productivity`, `Range`, `InputGood[N]`, `OutputGood[N]`,
`distributionweight`, `passenger_boost`, smoke fields etc., much
fatter than Building; add a `Factory` dataclass once the first
industry ports.  (b) **Animation phase** — `emit_building`
hardcodes phase=0.  Animated assets (phase > 0) need their own
axis in `iter_building_cells` and the viewpoint factory.
Concrete next move when the first port needs it: extend the cell
iterator to yield `(s, l, y, x, h, p)` and the viewpoint to
multiply facings accordingly.  Seasons (the `s` axis) and
height-stacking (the `h` axis) are already plumbed end-to-end and
tested — same axis-multiplication pattern.

**Climate texture not yet hex-native.**  `climate_texture` is
vendored from upstream pak128.Britain verbatim (see
`grounds/climate_texture.{png,dat}`) as biome-art-without-tile-
geometry — replace with a Britain-flavoured hex-native palette when
in-game appearance warrants.

**way_ground is v1 only.**  Reuses `light_texture`'s per-region
Lambert pass without per-axis differentiation (no chord-band
flattening, no ballast-edge shading).  Concrete next move when
in-game readability surfaces a gap: give the chord band under the
way its own brightness term (lift the chord midpoints, render the
way's running surface as a distinct face).

**fence bake is parametric posts+rails, not from the blend.**
`grounds/fence.blend` ships in the upstream blends repo — a full
3D fence model with white pickets, wire mesh and corner poles
across four quadrants (`pak/diff_fence.py` proves it: rendering
the blend through the upstream cardinal-S camera matches
fence-4 at IoU 0.896, the cardinal-E camera matches fence-3 at
0.862, and the OR composite matches fence-5 at 0.844).  Our
`grounds/fence.py` ignores all of that and traces brown polylines
parametrically.  Concrete next move when fidelity matters:
rewrite `grounds/fence.py` as a Blender-driven bake mirroring the
way/building bakers — hex-camera render of the same blend at one
facing per back-wall.  The blend's 4 fence quadrants map naturally
onto the 3 hex back-edges (NW, N, NE) via per-facing model
rotation, same pattern as `building_hex_viewpoint`.  Then drop
the polyline path entirely.

**Fence wall-2 cases render IMG_EMPTY.**  Engine `FENCE_IMAGE_COUNT = 3`
in `grund.h` caps the per-set sprite count at 3, so `fence_offset`
values 4..7 (any combo involving the rightmost back-wall, wall 2)
either index past the artificial set (rendering the wrong sprite)
or fall off the end (IMG_EMPTY).  Matches upstream Britain's shape —
their fences.dat also ships 6 entries — but is genuinely under-
specified for the 3-back-edge hex.  Concrete next move when it
bites in-game: bump `FENCE_IMAGE_COUNT` to 7 in `grund.h`, extend
`grounds/fence.py`'s `_WALL_MASKS` to cover all seven non-zero
masks × {natural, artificial}, and rebake.  Engine-side change,
not just a pak edit.

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

**Tile-chord flush across adjacent hex tiles.**  `bake_way.py`
assumes the atom + cap-bisect geometry gives flush rail joins at
shared tile edges, but nothing in the composition pipeline pins
the cap plane to the tile-edge midpoint where the neighbour
tile's strand starts.  Concrete next move once the square diff
converges: render two adjacent hex tiles + check edge alignment
pixel-by-pixel.  If rails don't meet flush, a small tile-overlap
fraction is needed (strand longer than chord by a cap-mitre-
worth).

**No procedural ground / wide ballast under the strand.**
`ns-cssr.blend` ships a `Plane.005` mesh carrying a `Transparent`
material — diffuse 0.8 grey, no `concrete-paving-small` texture
wired up — meant to be the wide ground under the rail strand.
Cycles renders it as opaque mid-grey, contaminating ~50 % of the
bake's lit pixels; `pak/bake_way.py::_STRIP_MATERIALS` now drops
any mesh carrying the `Transparent` material so the strand stands
on its own.  Downstream, our cells show only the strand atom's
extent (400 lit px in the NS cell), while upstream's `image[NS]`
shows full ballast across the cell (2372 lit px in the chord cell)
— roughly 5x our coverage.  Concrete next move when in-game ground
continuity matters: either author the missing `concrete-paving-
small` texture into a node tree and re-enable the plane, or render
a procedural ballast region around the strand (Lambert pass like
`pak/lightmap.py`, masked to the strand-adjacent strip).  Soft
trigger.

**Cast-iron / fishbelly geometry mismatch.**  `ways/cast_iron.py`,
`fishbelly.py`, `fishbelly_heavy.py` render through `ns-cssr.blend`
(crushed-stone ballast + sleepers) tinted by their per-variant
`MATERIALS` dict — but real cast-iron rail (1789-1830s) and early
wrought-iron fishbelly were iron strips fastened to stone setts,
no ballast, no transverse wooden sleepers.  The blend-share is a
category error for the pre-ballast era.  Each affected per-rail
.py carries a "Geometry caveat" docstring flagging this.  Concrete
next move when in-game readability of early-era track matters:
author a `ways/cast_iron.blend` strand atom (iron strip on stone
setts), repoint the three early-era .pys at it, drop their
`MATERIALS` (the new blend authors its own colours).  Until then,
the dats are correct (intro dates, costs, wear); only visual
fidelity for the 1789-1845 window suffers.

**Rail-grade variant bake + recalibration.**  20 `ns-cssr.blend`
rail-grade scripts (cast_iron through cssri); six have committed
Workbench-FLAT-calibrated PNGs (cast_iron, wrought_iron_light,
wrought_iron, wssr-early, wssri, cssr — continuous track from
1834 onward bar a 1832-1833 micro-gap and a one-year 1887 gap).
The remaining 14 scripts hold Cycles-era `MATERIALS` values
sampled under the previous Cycles bake; under Workbench FLAT they
would render at the literal sampled colour with no shading
attenuation, which is darker than upstream's authored atlas for
the same reason cssr's old values were.  Concrete next move per
script: fetch upstream's `ways/images/<name>.png` through
`pak.fetch_pak`, K-means k=4 with magic-pink masked, paste the
luminance-ordered centroids into `MATERIALS`, bake.  Same pattern
as cssr (see CLAUDE.md → "Per-way material recolour").

**Waggonway and plateway have no upstream blend.**  `ways/waggonway.dat`
(10 kph, wooden) and `ways/plateway.dat` (12 kph, iron-plated
wooden) reference per-direction atlases (`waggonway-wood_<dir>.png`)
not present in the blends repo's `ways/` directory and visibly
distinct from `ns-cssr.blend`'s rail-on-ballast cross-section.
They're not in the 19 ported rail grades.  Concrete next move when
the first-era rail look matters in-game: either author a
`ways/waggonway.blend` (single wooden rail, no ballast) and a
`ways/plateway.blend` (wooden with iron plate on top), or render
them parametrically without a blend.  Soft trigger.

**Bake hex icon + cursor sprites for ways.**  Option (a) is in
today (`emit_way` stubs `cursor=./<basename>.0.0` and
`icon=./<basename>.1.6` for every way) so `way_builder_t::weg_search`
picks the way up as a buildable default and the engine doesn't fatal
with "No road found at all".  Toolbar icons render the no-way and
straight-through-tile ribi cells instead of dedicated artwork —
visually crude but functional.  Concrete next move when the visual
matters: extend `pak/bake_way.py` with a dedicated icon/cursor
render mode that appends two cells to the atlas (e.g. at (8,0) and
(8,1)) at a canonical camera angle, then drop the `emit_way` stubs
and have `port_way` keep upstream's refs.

**Road-blend generalization.**  `bake_way.py` was tuned against
the rail strand atom in `ns-cssr.blend` (one straight cross-section
authored along +Y, composed onto every hex ribi chord).  Upstream
Britain does not ship an analogous straight-atom road blend —
per-material the blends repo carries `<mat>/{slope1, slope2,
standard-city-base}.blend`, and the snow-shape family
`road_snow/{ew-snow, n, ne, nw-diagonal-snow, sew, 3, 3h, -}.blend`
pre-renders individual ribi shapes rather than composing one.
`ways/tarmac_road.py` currently points `BLEND` at
`ways/tarmac/standard-city-base.blend` as the closest analog, but
this is unverified — the blend may be a four-way junction, a
multi-tile city panel, or carry materials the bake pipeline doesn't
expect.  Concrete next move: open one of the
`<mat>/standard-city-base.blend` blends in Blender, characterise
its geometry (single strand? junction? extent in tile units?) and
either (a) point `ways/tarmac_road.py` at it with whatever scale /
strip extras `bake_way_main` needs, or (b) add a road-specific
composition mode to `bake_way.py` that consumes the per-shape
`road_snow/*.blend` family directly.  Trigger: first time the road
bake runs and produces nonsense, or the first user who needs
in-game roads.

**Hex re-bake of GUI sprites.**  The engine's
`skinverwaltung_t::successfully_loaded` fatals on a missing
Construction / GeneralTools / Logo / freight-icon skin obj at load,
so the Makefile stages upstream `gui/gui{64,128}/*.png` next to
their dats and runs makeobj on the staged copy
(`$(GUI_STAGED)`).  GUI elements don't carry the world-projection
burden world tiles do — 64/128 px bitmaps render fine under hex —
so the verbatim-upstream shortcut is sustainable until somebody
wants a hex-distinctive UI look.  Concrete next move when that
matters: per-skin re-bake pass (most are cursor / icon strips,
similar machinery to the ways icon/cursor TODO above), then drop
`pak.fetch_gui_images` and ship committed sibling PNGs.  Soft
trigger.

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

**Atlas commit vs. CI-artefact-only.**  Default is commit (per
`CLAUDE.md` → "Per-asset directory layout") but reversible.
Switching to CI-artefact-only saves repo bytes at the cost of
"see the change in the PR".  Concrete next move: measure committed
atlas size after the first ~10 asset bakes; if the cumulative is
under 10 MB this question retires.  Trigger: ten assets baked.

After the spine: expand by asset family (rail vehicles, road
vehicles, buildings, industries).  Per-family progress is
recorded by deleting that family's entry from this file when it's
done, not by adding "completed" notes.
