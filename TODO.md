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
and the first two ship ports (`boats/dogger`, `boats/secr_queen`)
drop both keys on port; every other boat dat will too, since
water vehicles always gate on the Ship / Large-ship water-class
indices (5, 6).  Concrete next move: model the field as
`dict[int, int]` (or similar), add `way_constraint_prohibitive`
back, and teach `emit_vehicle` to walk dict items.  Triggered.

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

**Dogger calibration drift — facing-orientation mismatch.**
`boats/dogger` lands at IoU 0.117-0.927 — NW alone is healthy
(0.927), the other seven facings drift to 0.12-0.46.  The one-
facing-fits / others-don't pattern is the signature of the
upstream model not honouring the contributing-graphics "long-axis
Y, centred on origin" contract that the `vehicles` alignment
assumes (see CLAUDE.md → "Upstream blend calibration contract").
`boats/secr_queen` on the same alignment lands worst-IoU 0.938
across all 8 facings, so the alignment itself isn't broken — it's
per-blend.  Concrete next move: load `boats/dogger.blend` in
Blender, check the model's bbox vs origin and which axis the hull
runs along; if the authoring is off, either fix the blend
upstream (out of repo scope) or add per-asset
`model_rotation`/`model_translation` bake-meta on `Vehicle` (the
buildings pipeline already has `model_translation` for multi-tile
placement — extend the pattern).  Trigger: next sailing-vessel
port (they may share the issue).

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


**BI-faithful slot composition replaces, heuristic multiplies.**
`pak.blend_slots` reads per-slot MTex.r/g/b + Tex ColorBand from the
.blend binary; `Slot.color` / `Slot.color_band` ride through to
`render._build_slot_output`, which emits the BI-faithful colour for
procedural slots (constant MTex-r/g/b, or band mapped through noise
intensity).  No ported Britain building blend carries an active
`TEX_COLORBAND` flag, so the band path is forward infrastructure
rather than load-bearing for today's catalog.

What's actually load-bearing: a slot[0] IMAGE under MIX fac=1.0
**replaces** the material's diffuse with the image pixels in BI's
real math.  The `Material(image=..., size=...)` single-slot heuristic
in `_build_image_material` instead **multiplies** `image x diffuse`
-- BI-incorrect, but visually closer to upstream because
`flemish-bond-improved x (0.61, 0.33, 0.27)` lands near the
upstream Brick photo where BI's replace renders too bright.  The
pilot ships in the heuristic path because of this; slot form on
this blend regressed the metric.

Concrete next moves to close the gap honestly: (a) switch building
viewpoint to Cycles (handles world emission as ambient natively,
may rebalance slot composition); or (b) audit BI's actual slot
math (mapto's `MA_ADDCOL` flag, MTex `stencil`) for a path that
multiplies image against diffuse.  Pixel-identical via BI 2.79b
sidecar is open but on hold (legacy-renderer dependency we'd
rather not carry -- see "Pixel-perfect building match needs UVs"
for the framing).

**Per-material dRGB attribution surfaced two systematic gaps.**
`pak.diag_per_material --all` (added this session) aggregates by
material name across the catalog and reveals the dominant
contributors are (1) dark-diffuse surfaces — Interior, Tiles,
FeltRoof, Stone — uniformly rendering ~50 RGB below upstream, and
(2) multi-image-slot surfaces — Hedge, Veg-Green*, Veg2 — rendering
2× too dark.  (1) needs ambient lighting that EEVEE doesn't deliver
without baked light probes; we tried world emission + irradiance
probe + light_cache_bake in headless mode and the probe adds AO-like
darkening that cancels the world contribution, net zero.  Concrete
next move: either switch building viewpoint to Cycles (handles world
emission as ambient natively, no probes) and re-tune sun energy
scale, or investigate adding an explicit additive emission floor at
the BSDF level (mimicking BI's additive WORLD_AMB term).  (2) is
the multi-slot colour-band gap above — same fix, different
manifestation.

**Lighting overrides exist; only the pilot uses them.**  Per-asset
`lighting=Lighting(world_ambient, sun_energy_scale, sun_elev_deg,
sun_az_offset_deg)` lives on the SPEC alongside `materials=`,
threaded through bake / diff / render via `--lighting` JSON.
`res_1600_kg_01` carries one (ambient 0.55, elev 45°); the other
six ported buildings still rely on the global EEVEE-substitute
defaults (ambient 0.30, elev 30°).  Per-asset preferences diverge
(res_kg_1920's opposing-ambient need is structural, not fixed by
material data) so the global is unlikely to beat per-asset tuning
across the fleet.  Concrete next move: run `pak.tune_materials` on
each ported building, accept whichever per-asset `lighting=` +
`materials=` it converges to.  Light cost (~2-5 min per asset);
does not require any infrastructure beyond what landed.

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

**`grounds/shore_trans.py` baker isn't byte-stable across
numpy/PIL builds.**  Pure-numpy parametric baker, no Cycles, yet
shore_trans landed at a different SHA on this sandbox CPU than
on CI -- 319 pixels (0.0081%) flip red↔blue at rows 1121-1122,
diagnosed via `pak.diag_png_drift`.  The other 7 parametric
ground bakers (`light_texture`, `back_wall`, `marker`, `borders`,
`water`, `way_ground`, `fence`) are stable.  Likely a floating-
point order-of-operations difference in a numpy reduction the
shore_trans baker happens to hit on a tie.  Concrete next move
when CI flakes again on shore_trans: bisect which numpy operation
in the baker reorders, replace with an order-stable form (e.g.
explicit accumulator + Python loop, or `np.add.reduceat` with a
pinned axis).  Bites silently otherwise; the only signal is the
CI rebake step's `git diff --exit-code` failing.

**EEVEE townhouse atlas isn't byte-stable across consecutive
runs.**  `citybuildings/res_kg_1870_townhouse.png` re-bakes to a
different SHA on consecutive `python3.12 -m citybuildings.res_kg_
1870_townhouse` invocations on the same machine with no code
change; every other EEVEE building (`com_kg_1870_pub`,
`com_kg_1970_small_office`, `ind_1860_jh_gasometer`, `res_1600_
kg_01`, `res_kg_1890_detatched`, `res_kg_1920_detatched`) is
byte-stable, so something specific to this blend triggers EEVEE
TAA jitter that the standard determinism pins
(`use_gtao=False`, fixed thread count, etc) don't cover.  Cycles
vehicles and Workbench ways are stable too.  Concrete next move:
diff a `--keep-per-facing` dump across two runs to see if all
facings drift uniformly or just one; if just one, the
non-determinism is per-facing render order, not global, and
points at the per-facing mesh-rewrite path
(`_apply_facing` + `_bake_world_into_meshes`).  Until pinned,
`rebake` CI will flake whenever the townhouse re-bakes.

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

**Multi-tile vehicle overflow.**  `HEX_VIEWPOINT`'s `fit_matrix`
(`_hex_fit()`) applies a single pakset-wide scale
(`2R / upstream_ortho_scale = 2R/24`)
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

**Multi-tile building port — production-side slicing landed; in-
engine validation and material/ortho conventions are the open
gaps.**  `signalboxes/mechanical_signalbox_large.py` is the first
2×1×4 port.  `building_hex_viewpoint` renders multi-tile via
image-space slicing: one Facing per `(layout, height)` on a wide
canvas covering the full footprint at the hex screen lattice,
model untranslated (artist XYZ contract preserved); each Facing
carries `slices` listing per-cell W×W crops at
`hex_tile_screen_offset(qx, ry)`.  Single-tile path is unchanged.
`Viewpoint.canvas_width/canvas_height` + `Facing.slices` in
`pak/render.py` do the underlying render-once-crop-many; the bake
driver routes through automatically based on `dims`.
`building_hex_viewpoint`'s `fit_matrix = _hex_fit(divisor=
max(dims))` divides authored blend ortho so the artist's
`ortho = dims · per-tile-ortho` convention renders at the per-
tile size the engine paints at.  All 8 atlas cells populate,
building straddles the hex tile boundaries.

**Open: in-engine eyeball.**  The hex atlas has never been seen
under hextrans -- structural correctness is verified by bbox
inspection + by `tests/test_viewpoints.py::TestBuildingHexMultiTile`,
but whether adjacent cells actually tile coherently at hex tile
seams in-game is unknown.  Concrete next move: load a built pak
into hextrans (when build infrastructure can stage a multi-tile
building); if seams misalign, the slice-centre formula in
`hex_tile_screen_offset` is the place to look.

**Open: per-asset `blend_ortho_per_tile` override is opt-in, no
sniffer.**  `Building.blend_ortho_per_tile` lets a SPEC pin the
multi-tile per-tile ortho target when the blend's authored ortho
isn't `max(dims)·24` -- stonehenge ships ortho=72 over a 2x2
footprint, so SPEC declares per_tile=24 which the factory bakes
into `fit_matrix = _fixed_hex_scale(2R/(per_tile · max_dims))`,
constant against the blend's authored ortho.  The default
fallback (`_hex_fit(divisor=max(dims))`) is still implicit-
assumption-based -- equivalent to "honour the artist's authored
per-tile rate".  Concrete next move when the third multi-tile
building ports: if a pattern emerges (e.g. every attraction at
`dims·36`, every signalbox at `dims·24`), document the per-class
convention; otherwise treat per-asset override as the steady state.

**Open: multi-tile calibration diff residual.**
`diff_buildings.run_multitile` anchors the stitch on
`_STITCH_CANVAS_ANCHOR = (256, 288)` -- where the camera projects
world (0,0,0) per the cardinal-camera math (pitch=60° looks at
(-4.2, 4.2, 0) not origin; uniform by cardinal symmetry).
`Building.blend_model_offset_xyz` lets a SPEC pin where the model
sits in world (renderer pre-translates by -offset before fit/
rotation/render) for assets where the artist authored off-centre;
`pak.diag_centroid_align` is the porter-aimed sweep that suggests
a candidate offset.  The diff scores raw IoU at the structural
anchor -- no auto-sweep -- so misalignment surfaces as IoU
residual rather than being silently absorbed.

Worst raw stitched IoU: signalbox **0.69** (was 0.55 -- pinned
`blend_model_offset_xyz=(0,0,+2.14)` per `diag_centroid_align`'s
pure-Z candidate), stonehenge **0.52** (was 0.49 -- corner-plane
strip).  Signalbox's pure-Z case worked cleanly because Z is
rotation-invariant; stonehenge's residual is XY drift that the
current pre-rotation `blend_model_offset_xyz` can't express on a
multi-tile asset (see "Multi-tile XY offset gap" below).
Stonehenge's MUSGRAVE/CLOUDS noise floor exists too but is a
distinct, smaller residual stacked on top of the positional drift.

Stonehenge sits at IoU 0.52, signalbox at 0.69 -- both still below
`FAIL_IOU=0.88`.  Either lower the floor, add per-asset
relaxation (`FAIL_IOU` override on SPEC), or mark these as
known-fail and exclude from the gate.  No decision yet -- the
diff still emits useful per-layout numbers and the visual grid
for human inspection.

**Open: multi-tile XY offset gap.**  `blend_model_offset_xyz`
applies pre-rotation (model-local) per `render.py::render_atlas`,
so on multi-tile buildings whose layouts rotate the model an XY
offset rotates with each layout -- it lands correctly for L0/L2 in
a 0°/180°/0°/180° cycle but flips for L1/L3.  Z is rotation-
invariant and works (signalbox just exercised this).  Stonehenge
has a clean XY drift the diag identifies (mean (-0.27, +0.27),
clustered within ±1 px across layouts) that can't be pinned today.
Concrete next move when an asset really needs it: add a second
field on `Building`, e.g. `blend_world_offset_xyz`, that augments
every facing's `model_translation` (the existing post-rotation
world-frame slot multi-tile cell positioning already uses).  Cheap
to plumb: one CLI arg through `render.py`, one tuple add at the
build-facings step.  Hold off until stonehenge isn't the only
customer.

**Open: hex vs square building viewpoints disagree on footprint
centring.**  `building_hex_viewpoint` shifts slice positions by
`hex_tile_screen_offset(max(dims)-1, max(dims)-1) / 2` (constant per
asset, max-dim-corner-midpoint).  `diff_buildings` -- via
`pak.dat.building_footprint_centroid` -- uses the per-layout (y, x)
centroid that varies between even and odd L on rectangular footprints
because of the engine's dims swap in `building_writer.cc`.  For a 2x1
building these differ by half a tile on the odd layouts.  Only the
diff side is calibrated (matches upstream); the hex side hasn't been
visually validated under hextrans yet so the discrepancy hasn't
bitten.  Concrete next move when the first multi-tile hex bake hits
the engine: if seam alignment is off on odd layouts, port the
`building_footprint_centroid` rule into `building_hex_viewpoint`'s
slice centring (replace `max(dims)/2` with the per-L centroid via
`hex_tile_screen_offset(centroid_x, centroid_y)`).  Either side
calling into the same SPEC-level helper avoids future drift.

**Open: 4-layout rotation formula is signalbox-pinned, not proven.**
The `model_rot_z = (2·step·l) % 360` formula in
`building_square_viewpoint` was chosen on visual evidence from
mechanical-signalbox-large (it produces the face arrangement matching
upstream's stitched cells).  Stonehenge (second multi-tile port) is
rotationally near-symmetric so doesn't discriminate between this
and alternative rotation patterns -- the face-arrangement test
needs a third port with clear asymmetry (e.g. a 2x2 building with
distinguishable front/back).  Concrete next move when such an asset
ports: re-test both this formula and `180° for L in (1, 2)`; if
the latter wins, the formula isn't universal.

**Open: winter-pass for signalboxes + attractions.**  `seasons=2`
requires a `-snow.blend` sibling; jamespetts blends doesn't ship
one for any signalbox, and JamesHood blends ships `-snow` for
some attractions (`citychurch-snow`, `cricket-ground-sm-snow`,
`fountain-snow`, …) but not for stonehenge.  mechanical-signalbox-
large and stonehenge ports drop `seasons=2` and ship summer-only.
Concrete next move when winter coverage is wanted: either paint
snow procedurally (a `materials_winter` recipe swapping
Roof/Pavement/Stone diffuse for snow tones, like
`citybuildings/res_1600_kg_01.py`'s winter pass does), or accept
the per-season divergence from upstream.

**Open: heights coverage.**  The slicing canvas computes vertical
headroom from hex koord offsets alone; `heights>1` will need
extra vertical room in the canvas plus per-height slice rows.
Untested end-to-end -- first multi-height port (no asset yet
needs it) will surface what's missing.

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

**Hex bridge: bake pipeline shipped, in-engine schema unverified.**
`pak.dat.Bridge` + `emit_bridge`, `pak.bake.bake_bridge_main`, the
per-piece `bridge_hex_viewpoint`, and `ways/plate_girder.py`
exercise the bake side end-to-end (3-row × 6-col atlas: image axes
/ start dirs / ramp dirs).  What's *not* validated: the emitted
dat actually loading in-engine.  Three gaps visible in the current
output:

* **Hex bridge schema is a guess.**  Dat key tokens
  (`BackImage[n_s]`, `BackStart[ne]`, …) and the 3-axis / 6-dir
  layout are translated from upstream's square `[NS]`/`[EW]` and
  `[N]`/`[S]`/`[E]`/`[W]` keys; hex `bridge_writer.cc` (presumed
  to exist on the engine side -- `hextrans-pak128/infrastructure/
  rail_bridges/rail_060_bridge/` is the worked-example pakset)
  is the authoritative source.  Concrete next move when the
  Britain pak first builds a `.pak` artifact for bridges: feed
  `ways/plate_girder.{dat,png}` through makeobj, then load in-
  engine and read engine logs for unknown-key warnings; if the
  tokens drift, fix `HEX_BRIDGE_PIECE_LABELS` in `pak.dat` (one
  source of truth -- bake and emit both read it).

* **Depth-clipped Back/Front.**  The Front layer points at the
  same atlas cell as Back, so the bridge silhouette is fully
  opaque -- a vehicle traversing the deck vanishes behind the
  bridge image instead of passing between Back and Front planes.
  Concrete next move: split each piece render into Back / Front
  passes (compositor Z-mask or per-render clip plane
  perpendicular to camera Y at the cell midline), grow the atlas
  to 6 rows (Back/Front × 3 pieces), have `emit_bridge` key Front
  at row+1.

* **Variant 2 + season 1 cells.**  Upstream emits four families
  (variant 1 / variant 2 × season 0 / season 1; variant
  interleaves under `pillar_asymmetric`, season switches at snow
  climates).  We emit only variant 1 + season 0.  Concrete next
  move when asymmetric pillars matter: render a second piece set
  from a variant-pillar blend (none in JH yet -- see the variant
  0 entry below) and emit `*2` keys.  Snow follows the building
  pattern (recolour materials for winter).

PlateGirderConcrete (the 1949+ successor in the same upstream dat
file) is unported -- separate visual family, no JH blend source
under `ways/plate_girder/`; lands when a `concrete.{blend}` set
appears or someone authors one.

**Plate-girder variant 0 (`BackImage` / `Start` / `Ramp` without
trailing `2`) lacks a JH source.**  JH's `end.blend` and
`slope.blend` ship the steeper-slope abutment that geometrically
matches upstream's variant 2 cells (`BackImage2` / `Start2` /
`Ramp2`); per-facing IoU 0.66-0.91 vs 0.52-0.65 against variant 0.
The variant 0 cells in upstream show a gentler-slope abutment
(visually obvious in `pak.diff_bridge_overview`'s output grid).
`straight-end.blend` (a shared blob across the four viaduct families
in JH) was the obvious candidate but IoU 0.48-0.51 against Start v0
and 0.30 against Ramp v0 — not it.  Concrete next move when v0
fidelity matters: probe two-blend compositions (load `straight.blend`
+ `end.blend` into one scene with `end` positioned at the abutment
end and re-render through `bridge_square`) and check whether the
gentler-slope silhouette emerges; if not, an authored blend the JH
repo doesn't carry is the only path.

**N/E facing asymmetry on plate-girder end/slope.**  S/W facings
land at IoU 0.81-0.91 against variant 2 Start/Ramp cells while N/E
sit at 0.66-0.76 — uniform 15-25 point gap.  Probed a 180 deg model
rotation on the N / E facings only; those views collapse onto S/W
views (the bridge-end abutment is approximately 4-fold symmetric
about Z), so 180 deg is the wrong rotation.  Other model rotations
(90 deg, 270 deg), Y-axis mirroring, and multi-blend compositions
haven't been probed.  Concrete next move when uniformity matters:
run `pak.diff_bridge --match` with the model rotated 90 / 180 / 270
deg and after a Y-mirror, look for a cleaner permutation, lock it
in if one appears.  If no rotation closes the gap, the asymmetry is
JH-vs-upstream geometric drift the probe cannot heal — accept as
ceiling and move on.

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
called out in `docs/bake-way.md` becomes the
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
as cssr (see `docs/bake-way.md` → "Per-way material recolour").

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

**Tree per-season leaf-colour calibration.**  `trees/oak.py`
ships `seasons=1` (summer only); upstream's `tree.dat` ports
`seasons=5` (autumn / winter / spring / winter-snow added).
`tree_square_viewpoint` diff against upstream's summer cells
lands at IoU 0.95-0.98 on ages 1-3, so the calibration is solid
for one season -- expanding to five needs per-season material
recolour applied before each render pass.  Concrete next move:
sample K-means leaf-colour centroids from upstream's `oak-
{autumn,winter,spring,winter-snow}-{0..3}_S.png` (magic-pink
keyed at upstream's transparent colour, same sampling shape
`ways/<rail>.py` calibrates against — see CLAUDE.md →
"Per-way material recolour"), thread the per-season MATERIALS
dict through `bake_tree` as N subprocess renders that stitch
like the building snow path, bump the SPEC to `seasons=5`.
Trigger: when seasonal trees matter in-game (or when porting
Beech, which is also `seasons=5`).

**Tree age-0 silhouette is too wide vs upstream.**  Ours: 32 px
wide × 30 px tall.  Upstream: 22 px wide × 29 px tall.  Bbox
height tracks but width is 50 % over.  Ages 1-3 match upstream
within ±1 px on every edge, so it's not a calibration drift in
the rendering pipeline -- linear scale-by-`_TREE_AGE_SCALES`
overshoots at the smallest age, suggesting upstream rendered
age-0 from a different (thinner) model variant, not the same
model uniformly scaled.  The oak blend ships duplicate mesh
trios (`Mesh`+`Mesh.035`, `Mesh.001`+`Mesh.034`, `Mesh.002`+
`Mesh.033`) and 20 collections most of which carry the same
geometry under different `hide_render` flags -- candidate for
where the age variants hid.  Concrete next move: visually
inspect the unrendered collections (`Collection 2`, `4`...`20`)
and the two rotated mesh trios via a quick collection-include
probe in the bake driver to see if any of them carry a thinner
small-tree silhouette upstream uses for age 0.  Soft trigger;
the rendered atlas reads fine without it.

**Tree blends missing for Pine + NorwaySpruce.**  Upstream
`trees/tree.dat` ships four species (NorwaySpruce, EnglishOak,
Beech, Pine).  `Pak128.Britain-blends` only carries `trees/oak.
blend` and `trees/beech.blend` -- Pine is credited to "The Mav"
(BlendSwap 77005, public domain) and Norway Spruce isn't in JP's
blends repo either.  Concrete next move when porting those
species matters: fetch the BlendSwap originals, add the fetch URL
to `blends.lock` (or vendor under `trees/<species>.blend` if
licence-and-size permit), then write the bake scripts.  Triggered
by anyone wanting the full upstream tree set in-game.

**Tree `Name=` collision between `trees/oak.dat` and
`trees/tree.dat`.**  Upstream's combined `trees/tree.dat` carries
`Name=EnglishOak`; our ported `trees/oak.dat` does too.  Today
both coexist because `trees/` isn't in the Makefile `DIRS128`
list, so makeobj never sees either.  Concrete next move when
enabling `trees/` in DIRS128: port the other three species so
all four bake scripts exist, then `git rm trees/tree.dat` and
add `trees` to DIRS128.  Trigger: enabling trees in the build.

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

**Rewrite README.md.**  Current text is upstream's 2009 readme
preserved verbatim with a disclaimer header — describes the
vanilla Simutrans pakset, not the hex port.  Concrete next move:
short README covering what this repo is (hex port targeting
`SupraSummus/hextrans`), upstream provenance (pakset + blends),
build path (`Makefile` copy + makeobj), and pointers to
`CLAUDE.md` / `TODO.md` for porting status.  Trigger: when the
pak boots far enough to claim "runs, with N categories of
objects" — i.e. there's something concrete to ship behind.

After the spine: expand by asset family (rail vehicles, road
vehicles, buildings, industries).  Per-family progress is
recorded by deleting that family's entry from this file when it's
done, not by adding "completed" notes.
