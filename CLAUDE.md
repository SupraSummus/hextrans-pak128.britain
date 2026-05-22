# CLAUDE.md

Notes for AI agents (and humans) working on the hex port of the
Britain pakset.  Companion to `TODO.md` (running registry of open
work) and to the engine repo `SupraSummus/hextrans`.

## Where this repo came from, and where it's going

Forked from `jamespetts/simutrans-pak128.britain`
(simutrans-extended-flavoured, square-dimetric).  The destination
is a pakset that runs on the hex-grid `SupraSummus/hextrans`
engine, using 3D source blends from
`jamespetts/Pak128.Britain-blends` re-rendered through a hex
camera.

The migration is two simultaneous strands:

**`.dat` schema port.**  Drop extended-only keys (`axle_load=`,
`comfort=`, `livery_*=`, …) as each asset is touched.  Sprite
references get repointed onto hex headings (current engine state)
or re-rendered at native hex angles (once the engine lands its
6-direction cutover — see "Vehicle facing count" below).  The
vehicle catalog, intro dates, prices, accept-lists — the actual
gameplay content that makes this "Britain" — survives intact.

**Sprite re-bake from 3D source.**  Every existing `.png` here is
unusable under hex (different tile geometry, projection, anchor
y).  We re-render from `jamespetts/Pak128.Britain-blends` through
the hex camera defined in
`hextrans/src/simutrans/display/hex_proj.h` and mirrored in
`hextrans-pak128/tools/threed/`.  Per-asset baked PNG + new `.dat`
ship together; until both arrive the asset is stubbed, not
half-ported.

**Parametric ground synth.**  A separate pipeline covers the
engine-driven ground families (per-slope lightmap, marker, borders,
cliff faces, water, climate / shore alpha masks, sidewalk).  These
have no upstream art content — geometry, region partition and
Lambert shading are functions of engine constants in
`hextrans/src/simutrans/descriptor/synth_geometry.h` + mirrored in
`pak/hex_synth.py`.  Each baker is a single
`grounds/<asset>.py` that emits sibling `<asset>.{png,dat}`; the
filename matches the engine `Name=` field (`light_texture`,
`shore_trans`, …) so grepping from engine source lands on the
right baker.  Ported from `hextrans-pak128/landscape/grounds/`;
`climate_texture` is still vendored upstream verbatim and the
`fence` / `way_ground` bakers are v1 only — see TODO.md.

One ground asset (`Outside`, the void cell shown beyond the map
edge) ships under `pak1file/128/` instead, mirroring upstream's
layout — see `pak1file/readme.txt`, which records that the loader
historically required a standalone `ground.Outside.pak`.  Makeobj
emits per-object paks when fed a directory output (the `OUTSIDE`
Makefile target) rather than a bundled `<dir>.pak` filename.  The
bake script sits as a sibling of its `.dat`/`.png` outputs as
elsewhere, but runs through PYTHONPATH rather than `python3 -m`
because the `128` subdir isn't a legal Python module name.

The pak is unplayable until a critical mass of ground + ways +
vehicles is baked, and that's fine — the engine isn't shipping
either.  `TODO.md` tracks which assets have crossed the line.

## Cross-repo provenance

- **Upstream pak (`.dat` catalog, `.wav` sounds, sprite
  references):**
  `https://github.com/jamespetts/simutrans-pak128.britain`
- **Upstream blends (`.blend` source for sprite re-bake):**
  `https://github.com/jamespetts/Pak128.Britain-blends` is the
  primary source.  A second repo,
  `https://github.com/JamesHood/pak128.Britain-blend-files`, fills
  two of jamespetts' gaps — it is the only blend source for
  top-level `attractions/` and `depots/` — and adds substantially
  more `stations/` blends (~75 vs ~13).  `citybuildings/` and
  `industries/` paths are near-identical between the two; `boats`
  / `trams` / `trees` overlap heavily on shared paths; `trains` is
  organised completely differently (no shared paths).  Neither
  repo holds an OldBrickSchool / hospital / stone-attractions
  blend — those upstream PNGs predate the .blend pipeline.
  `pak/fetch_blend.py` currently only knows jamespetts; wire the
  second `Source` when the first attraction or depot ports.
- **Hex engine:**  `SupraSummus/hextrans`.
- **Worked-example hex pakset (procedural):**
  `SupraSummus/hextrans-pak128`.

Neither upstream pak nor blends repo is cloned in agent
sessions.  See "Asset sourcing without cloning" below.

The vanilla (Simutrans-Standard) pak128.Britain on SourceForge SVN
(`https://sourceforge.net/p/simutrans/code/HEAD/tree/pak128.Britain/`)
is the pre-fork ancestor and **not used**: vanilla-schema dats,
~13 generic wavs vs. our 191 extended-fork ones, no blends.  The
engine's `descriptor/writer/*_writer.cc` is the authoritative
key list, so the dat diff isn't worth an SVN fetcher.

That said, vanilla is still the cleaner reference when Extended
has *deprecated* a key that vanilla and hex both still honour.
The 2022 `pier_system` migration (PJMack, simutrans-extended PR
#528, landed 2022-04-15) replaced per-bridge `backPillar*=` art
with a universal `Obj=pier` + `Obj=deck` ground; a 2022-02-13 pak
commit `#`-prefixed those keys in ~10 bridge dats ahead of the
engine PR.  Vanilla and hex `bridge_writer.cc` both still read
`backPillar[<axis>][<season>]` and the same row of the upstream
sprite atlas holds real pillar art (`plate-girder.4.{2,3,4,5}` and
peers).  Treat the upstream `#backPillar*=` lines as
Extended-deprecation noise and un-`#` them; vanilla SourceForge
SVN is the cleaner ground truth for "which cells should ship".
Similar Extended-only deprecations are worth checking against
vanilla SVN before assuming "the cell isn't shipped".

## Engine facts (look up, don't fit)

Hex projection, camera, sun direction, sheet layout, slope
encoding, vehicle facing count — these are engine and upstream-pak
facts, not free parameters.  Look them up before tweaking.
Fitting against a single reference gives a result that's right
by accident and breaks on the next asset.

Recurring lookup categories:

- **Tile-to-screen mapping:**
  `hextrans/src/simutrans/display/viewport.cc`,
  `…/display/hex_proj.h`.  Lattice, anchor y, per-row x-step.
- **Compass directions:**
  `hextrans/src/simutrans/dataobj/koord.cc::neighbours[]` (edge
  order SE, S, SW, NW, N, NE).
- **Slope encoding:**
  `hextrans/src/simutrans/dataobj/ribi.h` — `slope_t` and the
  hex `slope_type(ribi)` direction-to-slope map.
- **Hex camera + lighting:**
  `hextrans-pak128/tools/threed/hex.py::HexGeom` and
  `…/render.py::HexCamera, world_to_screen_hex, SUN_DIR`.
  These mirror `display/hex_proj.h` and `display/synth_geometry.h`
  on the engine side — same constants, same orientation.
- **Per-asset-class `.dat` keys:**
  `hextrans/src/simutrans/descriptor/writer/*_writer.cc`.  Tells
  you which keys the hex engine actually reads (and therefore
  which extended-only keys to drop on port).
- **Vehicle facing count:**
  `hextrans/src/simutrans/descriptor/vehicle_desc.h::get_dirs()`
  returns 4 or 8 today.  The hex port has not migrated vehicle
  direction count; it repoints existing 8 sprites onto hex
  headings (pak N = hex NE, E = SE, S = SW, W = NW — see
  `hextrans/TODO.md` → "ribi cutover" for the current mapping).
  Hex-native 6-direction sprites are a planned engine port, not
  a present capability.  The bake's facing count is determined
  by `get_dirs()` at port time, not chosen freely.
- **Pak128 art conventions:**
  `hextrans-pak128/devdocs/128painting.txt` (dither, taper, sun
  height, ballast bands, mask colours) and the upstream blends
  repo's `render_SimutransRender_pak128Britain-65.py` (camera /
  sun setup the existing blends were authored for, `sp_*`
  material-name mask convention).
- **Existing hex worked examples:**
  `hextrans-pak128/infrastructure/rail_tracks/rail_060_tracks/`
  (single-layer; one `scene.py` emits both square and hex via
  `bake_pakset`).
  `…/rail_bridges/rail_060_bridge/` (multi-layer; back/front
  depth-clip slicing for bridges).

The **silent-failure landmines** to pin for the blend pipeline:

1. **Blender world scale.**  Upstream blends are authored for the
   square-dimetric 128-px tile.  Under hex the tile is the same
   world size but the projection differs.  A mis-scaled model
   renders without complaint at the wrong on-screen size.
   Back-solve from a known anchor — corners at radius
   `HEX_TILE_RADIUS` from `hextrans-pak128/tools/threed/way.py`,
   deck heights from the engine's per-step world-z lift
   (`hex_height_raster_scale_y` over `PIXELS_PER_UNIT`).
2. **Sun direction.**  The upstream
   `render_SimutransRender_pak128Britain-65.py` rotates the sun
   with the camera (correct for square 8-view).  Hex pins one
   world sun direction (south + 60° elevation — match
   `render.py::SUN_DIR`) and rotates the model under it, so
   shading stays consistent across facings.
3. **Image pixel orientation.**  `bpy.types.Image.pixels` is
   bottom-up (origin at bottom-left).  PIL and
   `hextrans-pak128/tools/threed/bespoke.py::bake_atlas` work
   top-down.  Atlas composition (`pak.compose`) goes through PIL
   only -- read PNG, slice/paste in numpy, save PNG -- so the trap
   doesn't bite the current pipeline.  Reach for `bpy.data.images.
   load` / `.pixels` and you immediately need to flip on both ends
   for the in-memory representation to agree with PIL's, and an
   asymmetric flip ships a vertically mirrored atlas silently.
   The fix is "don't IO through bpy"; the workflow lives in
   compose.
4. **`matrix_basis` drops shear.**  Assigning a 4×4 to
   `obj.matrix_basis` (or routing it via a parent Empty's basis)
   decomposes the matrix into translation/rotation/scale and
   silently discards anything outside that — including the hex
   projection's y/z shear.  The stored basis ends up a TRS
   approximation of the intended matrix, off by ~10 % in the
   off-diagonal terms, and the rendered silhouette tilts in a way
   that looks like a rotation bug.  `render.py` bakes the
   per-facing `shear @ rot @ fit` matrix into mesh vertex data
   directly via `bpy.types.Mesh.transform()`, which accepts
   arbitrary 4×4 exactly.
5. **Edit-mode meshes render their BMesh buffer, not
   `obj.data`.**  Upstream blends occasionally ship with one mesh
   stuck in edit mode (e.g. 4wheel-1850's body `Cube.009`).
   Blender keeps the render geometry for that mesh in a separate
   BMesh edit buffer; `obj.data.vertices` writes are invisible to
   the renderer until the obj leaves edit mode, and
   `obj.evaluated_get(deps).data` reports zero verts even though
   the mesh visibly renders.  `render.py` forces every mesh
   into OBJECT mode at the start of the bake.  When the rendered
   silhouette of one specific object refuses to track your
   projection, check `obj.data.is_editmode` first.

## Don't bake the answer

The asset source — `bake.py`, scene config, camera params — must
not read the upstream pak's PNGs.  The `.blend` is the model; the
upstream sprite is reference, not input.  Pakset materials
(climate textures) may be reused as material *inputs* into the
hex renderer, never as the rendered output.

The temptation under visual-supervision iteration is real:
fitting to the reference pixel-by-pixel produces a result that's
right by accident on the trained view and wrong on the others.
The diff loop's job is regression check + progress quantifier,
not steering signal.  Treat low diff as necessary but not
sufficient.

## Structural anchors

Fixed points to back-solve other parameters from.  These don't
move:

- **World z = 0 is ground.**  Vehicle wheels, building footings,
  pillar bases all touch z = 0.
- **Hex tile extent in world coords.**  Corners at radius
  `HEX_TILE_RADIUS`; one world unit = one entry-edge length.
- **One world sun**, south + 60° elevation; model rotates, sun
  doesn't.
- **Cell anchor y = `geom.mid_y`** for ground-level assets;
  bridges drop below to absorb the `,0,N` `.dat` shift the square
  pak handled with a draw-time offset.

When a render doesn't match expectations, the first move is
back-solve from these, not tweak the camera.

## Upstream blend calibration contract

The pak128.Britain blends are not bespoke per-asset — they share a
standardised world frame defined in the "Contributing graphics to
pak128.Britain" sticky on the Simutrans forum (jamespetts' April
2017 update, msg 162208).  Per-asset bakes inherit the contract;
none of the values below should be guessed from a single model's
bounding box.

**Camera scale.**  The contributing-graphics spec says
`ortho_scale = 24` rendering to 128 × 128 px — the 15 m ruler
(46 m for aircraft, log-scaled for large ships) the artist
calibrates Blender's units against.  In practice, each `.blend`
ships its own Camera object with the artist's chosen
ortho_scale: vehicle blends sit at 24, but several building
blends (e.g. `citybuildings/1600-detatched-house-2f.blend`) are
authored at 12 — half the per-cell zoom, building roughly fills
the cell instead of overflowing it.  `pak/render.py::strip_scene`
reads the camera's ortho_scale before stripping it; the per-
viewpoint `fit_matrix` callable then builds the scale `2R /
blend_ortho_scale` (defaults
to `2R / UPSTREAM_ORTHO_SCALE = 1/12` when the blend has no
camera).  Each blend renders at the per-pixel scale its author
intended.  Width and height for land vehicles are authored at
1.25× the length scale by convention; bakers do not undo this.

**Long axis along Y.**  All upstream Britain blends with a
longitudinal axis (carriages, locos, road vehicles, ships, planes)
are authored so `span_y > span_x`.  Auto-detecting "which is the
long axis" by bounding-box comparison and rotating to a different
canonical inverts every such asset's facings (the standard
configuration was the failing case in the original `render.py`
auto-fit) — trust the contract instead.

**Artist-authored XYZ is the placement contract.**  The hex
`fit_matrix` (built by `_hex_fit()` in `pak.viewpoints`) is
scale-only: convert blend coords to intra-tile coords by
`2*HEX_TILE_RADIUS/blend_ortho` and stop.  No
XY recentre, no z-floor drop.  Britain blends are authored against
the contributing-graphics spec (long-axis Y, centre near origin,
footings at z=0 for buildings); the scale-only fit honours that
authoring and surfaces drift on assets that don't.  Positional
anchoring goes through the per-tile `model_translation` axis (used
by multi-tile buildings), not the fit matrix.

**`blend_model_offset_xyz` applies pre-rotation, model-local.** The
renderer translates the mesh by `-offset` BEFORE the per-facing Z
rotation (see `render.py::render_facings`, the
`M_target @ Matrix.Translation((-mx,-my,-mz))` line).  Multi-tile
layouts rotate the model (`(2·step·L) % 360` in
`building_square_viewpoint`), so the screen displacement caused by
a fixed model-local XY *rotates with each layout*.  Tools that want
to invert from per-layout screen shifts back to a single
`blend_model_offset_xyz` must bake the per-layout rotation into the
design matrix; tools that don't will fail on every multi-tile asset
with real XY drift.

`pak.diag_centroid_align` is that tool: per-layout silhouette-IoU
sweep recovers `(dx_L, dy_L)`, then a single model-local
`(mx, my, mz)` is fit jointly by least squares with R² ≥ 90 % as
the pin threshold.  R² well below 90 % means the per-layout shifts
are inconsistent with any model-local offset — the most common
explanation is screen-constant drift that needs a post-rotation
world-frame mechanism (see `TODO.md` → "Multi-tile XY offset gap"),
but high non-translational mismatch (mesh clipping against
stitched cell boundaries, MUSGRAVE/CLOUDS noise floor) drives R² down
the same way.  `pak/_experiment_ground_truth.py` is the
perturbation harness that validates the tool's forward model
against the real renderer; run it after any change to the design
matrix or per-layout rotation convention.

**Alignment mode is asset-class-dependent.**  Trains, trams, water
craft and aircraft use upstream's **`vehicles` alignment** camera
positions (`op_list "2"`); road vehicles, buildings, signals and
stops use **`normal alignment`** (`op_list "1"`, or `"0"` for 4-view
buildings).  Only `SQUARE_VIEWPOINT` in `pak/viewpoints.py`
hard-codes one alignment (currently "vehicles", chosen to match the
asset class of the first ported asset); other alignments aren't
modelled yet.  The hex viewpoint is single and fixed.

**Old blends ship with broken scene settings.**  Many .blend files
predate the RGBA + `film_transparent = True` convention and still
have `Output = RGB` and a solid world background.  `render.py`
strips the blend's Camera / Sphere / Lamp objects on entry and
installs its own, then forces `film_transparent = True` and
`image_settings.color_mode = "RGBA"` regardless of what the .blend
saved.  Trusting the .blend's state gives black/cyan backgrounds
with no other diagnostic.

**Hex vs. square facing-to-screen shift.**  The square pak renders
a world rotated 45° in screen space, so its `_S.png` shows the
**world-SE** facing of the model; hex `_S.png` shows the world-S
facing.  Expect a one-position rotation when comparing hex vs.
square renders of the same asset (e.g. end-on appears at SE / NW
in square, at S / N in hex).  This is a coordinate-system
difference, not a calibration bug.

**Calibration validation loop.**  `pak/diff_upstream.py`
runs `render.py --viewpoint square` against an upstream blend, fetches the
corresponding pakset PNG via `fetch_pak.py` (pinned by `pak.lock`),
and reports two independent per-facing metrics:

  * **Contour** — silhouette IoU plus the absolute XOR pixel count.
    Geometry-only; ignores RGB entirely.
  * **Colour** — mean abs(RGB-delta) over the whole image after
    compositing both renders onto MAGIC_PINK and Gaussian-blurring
    σ=3.  Common-background composite collapses the "ours-zero vs
    upstream-pink" gap; the blur folds texture-phase / sub-pixel-AA
    mismatch into the macro colour signal.  Reported as
    `dRGB (blurred all-pixel)` -- note that 80% of pixels are
    background-on-background and contribute zero, so the absolute
    number is suppressed relative to per-silhouette-pixel error;
    use as a relative optimisation target.

A calibrated asset's bboxes match upstream within ±1 px on every
facing — bbox match is the geometry-only check.  Calibrated assets
*typically* land at IoU >= 0.93 (XOR pixel count single-digit per
facing, just the AA edge ring of a sub-pixel offset).  The
diagnostic flow when IoU is under 0.90:

  * Bboxes drift > ±1 px → real contour drift; the blend's frame is
    what's wrong, fix the blend or the alignment mode.
  * Bboxes match but IoU still low → material-handling discrepancy,
    not geometry (e.g. cockpit glass with alpha-blend rendering
    semi-transparent in Cycles where upstream's older pipeline
    rendered opaque — see `TODO.md` -> aircraft alpha-blend entry).
    The contour metric reflects this honestly; the calibration
    isn't broken.
  * Bbox + IoU healthy but colour delta high → livery material swap
    (see `TODO.md` -> `sp_*` mask pass), not a calibration problem.
The bottom row of `grid.png` colours the silhouette XOR (red =
ours-only, blue = upstream-only) so contour drift is visible at a
glance.  This is the only step that touches upstream PNGs — see
"Don't bake the answer" above; comparison is regression check, not
steering signal.

The ≥ 0.93 bar above is the **vision-supervised calibration**
target, reached by iterating material/lighting/blend-frame
adjustments with eyes on `grid.png`.  Unsupervised batch porting
runs a **soft-acceptance** variant: ship at IoU ≥ 0.5 with a
note, queue the 0.5-0.93 band for a later polish pass.  See
`docs/porting.md` for the batch workflow + empirical IoU
distribution; the n=595 train trial shipped 62 % at ≥ 0.90 and
median 0.92, so the soft-acceptance pool is the wrong-livery
tail, not the bulk of ports.  `pak.check` exits non-zero below
the 0.90 strict floor regardless of mode — batch tooling parses
stdout for the actual IoU and ignores the exit code.

`pak/check.py` is the driver: it imports a bake script,
reads `SPEC.blend` and `SPEC.upstream_dat`, and runs the diff
with no extra path-passing.  `--all` sweeps every bake script
under `trains/` for a fleet-wide summary; scripts whose SPEC
lacks `upstream_dat` are skipped with a notice (fill it in
when the upstream dat path is known).  The image paths the
diff fetches are derived from `upstream_dat`'s `*Image[…]=`
refs (via `pak/upstream.py::image_stem`), so the SPEC carries
the dat as the source-of-truth identity rather than mirroring
image-stem conventions that vary per asset class.

## What to carry from upstream, tiered

The Britain pak has decades of accumulated `.dat` content.  Per
asset, choose the tier:

*Verbatim.*  Intro dates, retire dates, base costs, capacities,
accept-lists, names.  These are the value of the Britain pak and
translate without modification.

*Translate cleanly.*  Sprite references migrate to the engine's
current direction layout (see "Vehicle facing count" above).
Extended-only gameplay keys get dropped or mapped to vanilla
equivalents where one exists.  Don't preserve dead keys.

*Drop.*  Extended-only features without a vanilla analogue
(detailed comfort model, livery system, reverse-formation rolling
stock, axle load).  Note the loss in the commit message; don't
carry a `# was: comfort=…` ghost in the file.

When in doubt, lean *Translate cleanly*: the goal is a pak that
runs on the hex engine, not a literal port of every quirk.

## Repo size strategy

Upstream Britain pak history was ~1.3 GB unshallowed (~700 MB
packed shallow).  A one-shot `git filter-repo` pass cut it to
~19 MB packed by dropping blob types the hex pak doesn't carry
in git.

The principle behind the strip set: discriminate
**regeneratable migration burden** from **shipped content** —
only the first is safe to strip.  Being heavy in history is not
in itself a reason to remove a blob; the question is whether
the pak still ships it (and if it does, whether the runtime can
fetch it on demand from upstream instead of carrying it in
git).

The applied strip set:

- `.png`/`.jpg`/`.jpeg`/`.xcf` (plus uppercase variants) —
  sprite art, re-baked from the blends repo through the hex
  camera.
- `.blend`/`.blend1`/`.blend2` — stray blends; canonical home
  is the blends repo.
- `.pdf`/`.ods`/`.xls`/`.xlsx`/`.doc` — JP's research material,
  originals stay reachable upstream.
- `.suo`/`.vcxproj`/`.vcproj` — IDE detritus.
- `.pak` — compiled `makeobj` output; regenerates from `.dat`.
- `.wav` — sound effects.  Fetched at pak-build time by the
  `copy` Makefile target via `pak/fetch_wavs.py` (scans
  ported `.dat`s for `sound=*.wav` references, pulls each through
  `fetch_pak`, stages into `$(PAKDIR)/sound/`).  See "Asset sourcing
  without cloning" below; the hex pak doesn't ship them in git.
- `.tab~`/`.dat~`/`.bak` — editor backups.

Kept in git: `.dat` (gameplay catalog), `.tab` (config),
`.nut` (scripts), authored text.

Before committing any new bulk-content type, ask: can the
runtime fetch it from a pinned upstream SHA over HTTP instead?
If yes, don't commit it.

The rewrite was destructive: clone hashes changed, outstanding
branches needed rebasing.  Done.  Further filter-repo passes are
possible but expect the same coordination cost.

## Asset sourcing without cloning

Two upstream repos are **URL-addressable, SHA-pinned,
read-only** sources rather than checked-out trees:

1. **`jamespetts/Pak128.Britain-blends`** — ~5.4 GB packed /
   ~18 GB working tree.  Source for sprite re-bake.  No git
   LFS (and we're not adding it; CCW doesn't support LFS).
2. **`jamespetts/simutrans-pak128.britain`** — the upstream
   pakset itself, the repo this one was forked from.  Source
   for `.wav` sound effects after they were stripped from this
   repo's history.

The pattern:

- A `*.lock` file at the repo root holds one upstream commit SHA
  per upstream repo (`blends.lock`, `pak.lock`).  One file per
  upstream repo, not per file-type — `pak.lock` covers pakset PNGs
  (used by `diff_upstream.py`), `.wav` sound effects (staged into
  the pak by `pak/fetch_wavs.py` in the Makefile `copy`
  step), and the boot-screen / demo deliverables (`symbol.BigLogo.pak`,
  `demo.sve`).  The same file also carries a per-blob sha256
  manifest — plain text, `commit <sha>` header line followed by
  `<sha256>  <path>` lines sorted by path (sha256sum format, so
  `sha256sum -c` reads it directly if you strip the header).  The
  fetcher validates downloaded bytes against the manifest; defends
  against upstream serving different bytes for the same path on top
  of the commit-SHA pin.  One-line-per-entry shape was chosen so
  inserts and removes show as single-line diffs.
- A `pak/fetch_*.py` script resolves `<path within
  upstream repo>` against that SHA, fetches the individual blob
  over HTTP, caches under a `.gitignore`d `.cache/` dir.  Unknown
  paths are recorded on first fetch (TOFU); CI's
  `git diff --exit-code` surfaces the manifest change so a human
  reviews any new upstream dependency.  Mismatches against an
  already-recorded sha hard-fail with a `SystemExit`.
- Consumers (per-asset `bake.py`, the runtime sound loader, the
  calibration diff) call the fetcher rather than reading files
  directly.

Present:  `pak/_fetch.py` carries the shared parser / emitter /
validate-or-record / network loop; `fetch_blend.py` and
`fetch_pak.py` are ~40-line wrappers that declare a `Source`
(repo slug, lock filename, cache subdir) and re-export `fetch`.
`fetch_wavs.py` is a thin batch helper over `fetch_pak` that
scans ported dats for `sound=*.wav` references and pulls each
one.  A session touching one asset downloads one blend, not the
tree; upstream repo size is irrelevant to the day-to-day.  Adding
a third source is a 10-line `Source` declaration; mixing sources
within one bake script just means calling the relevant wrappers
side by side.

If the upstream HTTP endpoint requires auth or routing, the
fetcher is the single place to handle it.  Keep auth concerns
out of per-asset `bake.py`s and out of the runtime loader.

**Exploring upstream repos.**  Day-to-day porting goes through
`fetch_blend` / `fetch_pak` — one blob over HTTP, not a clone.
When you genuinely need to see what's *there* (compare two
upstream repos, search for a blend that might or might not
exist), clone blob-less:

    git clone --filter=blob:none --no-checkout --depth 1 <url> <dst>
    git -C <dst> ls-tree -r --name-only HEAD

A full blends-repo clone is multi-GB (jamespetts unpacks to
~18 GB working tree); the blob-less form is a few hundred KB
of tree objects.  Drop the clone under `/tmp/` so it doesn't
end up in the working repo.

## Bake units and per-asset layout

A "bake unit" is one bake script.  It owns a `SPEC` (or `SPECS`)
of pure gameplay data and a list of blends to render; running it
emits the corresponding `.dat` + `.png` outputs as siblings.  The
script is the **single source of truth** — no upstream `.dat` is
read at bake time.

Two bake-unit shapes:

```
air/
  dragon_rapide.py        # SPECS = [PASSENGER, MAIL] -> one combined dat
  dragon_rapide.dat       # generated; two obj=vehicle blocks separated by ----
  dragon_rapide.png       # generated; shared atlas for both blocks
trains/
  __init__.py             # makes the dir an importable package
  _4wheel_1850s_first.py  # SPEC = Vehicle(...)  -> 1 dat + 1 png
  _4wheel_1850s_first.dat # generated
  _4wheel_1850s_first.png # generated
  _gwr_king.py            # (illustrative) 2 distinct-sprite outputs
  _gwr_king.dat           # generated  } loco
  _gwr_king.png           # generated  }
  _gwr_king_tender.dat    # generated  } tender
  _gwr_king_tender.png    # generated  }
  ac-railbus.dat          # unported upstream (seeder input)
  …
```

**Shared-sprite multi-object (`SPECS`).**  When upstream packs two
vehicles into one dat that share the same image refs — e.g.
`dragon-rapide` + `dragon-rapide-mail`, same plane in different
gameplay roles — the bake unit declares `SPECS: list[Vehicle]` and
`emit_vehicles` writes one combined dat where every block points
at the shared `<basename>.0.<col>` atlas.  One render, two
gameplay objects.

**Distinct-sprite multi-object (illustrative `_gwr_king`).**  Loco
and tender are visually different objects; each gets its own
`<basename>.{dat,png}` triple driven by a per-output `bake_vehicle`
call inside the same script.  Designed but not yet exercised
end-to-end — `pak/reemit_dats.py` still introspects only `SPEC` /
`SPECS` and will need a per-script reemit hook for this case (see
TODO.md → "Multi-object reemit hook" — and "Bake script shape"
below).

All three files in a bake-unit triple share the same basename.
A leading `_` is required only when the asset name starts with a
digit (Python identifier rules — see "Importable bake scripts"
below); letter-leading assets like `br_cl15` go plain.  The
underscore (when present) isn't asset identity — `Name=` inside
the dat carries that — it's the filesystem cost of making the
script importable, kept consistent across the triple so the
files move and grep together.

The file/dir structure is **decoupled from vehicle identity** —
one script may emit 1, 2, or 11 outputs (~40 % of `trains/`
upstream is multi-object, packing locos+tenders, EMU sets, or
whole carriage families into one source dat).  The unit boundary
matches whatever's atomic to bake; output basenames are the bake
script's choice per-object, not derived from the script's name.

**Bake script shape.**  A bake script holds its gameplay data
*and* its bake-pipeline metadata (blend path, upstream PNG stem,
per-material recipe, EEVEE lighting tune) inline on a typed SPEC
dataclass, then calls `bake_main` from `pak/bake.py`.  The dat
emitters skip the bake-meta fields (`pak.dat._bake_meta` marker);
`pak/bake.py` and `pak/check.py` read them off SPEC.  The full
single-vehicle bake script:

```python
from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name="4-wheel-1850s-first",
    waytype="track",
    speed=135,
    length=3, weight=8.1,
    payload=18,
    cost=167000, runningcost=0, fixed_cost=139,
    constraint_prev=["any"],
    constraint_next=["any"],
    # … 20-or-so more fields for a complete port
    blend="trains/Carriages/4wheel-1850.blend",
    upstream_dat="trains/4wheel-1850s-first.dat",
)

if __name__ == "__main__":
    bake_main(SPEC, __file__)
```

`bake_main` derives out-dir + basename from `__file__` and calls
the underlying `bake_vehicle` (fetch-blend / run-render /
emit-dat).  Both accept either a `Vehicle` or a `list[Vehicle]` —
shared-sprite multi-object scripts pass `SPECS` to the same entry
point and the dat-emit step writes one combined dat.  Both
Vehicles in such a list carry the same `blend=` / `upstream_dat=`
values; the convention is a local `_BLEND = "..."` /
`_UPSTREAM_DAT = "..."` at module top referenced from each
Vehicle, so a divergence is caught by `_shared_blend`'s assert.
Distinct-sprite multi-object bake units skip the convenience and
call `bake_vehicle` directly per output, with distinct `basename`
per call.

**Ways follow the same shape.**  A way bake script holds a typed
`Way` (covers the hex-engine `Obj=way` schema + the few extended
keys upstream Britain dats carry: `wear_capacity`, `axle_load`)
plus `blend=` / `materials=` / `strip=` bake-meta on the same
SPEC and a `bake_way_main(SPEC, __file__)` call:

```python
from pak.bake import bake_way_main
from pak.dat import Way

SPEC = Way(
    name="cssr", waytype="track",
    intro_year=1968, intro_month=3,
    topspeed=160, max_weight=22,
    wear_capacity=4128000000,
    cost=140000, maintenance=375,
    blend="ways/ns-cssr.blend",
    materials={
        "Ballast": (100, 100, 100),
        "Wood": (134, 134, 134),
        "Rail": (192, 192, 192),
        "RailTop": (255, 255, 255),
    },
)

if __name__ == "__main__":
    bake_way_main(SPEC, __file__)
```

`bake_way_main` shells out to `pak/bake_way.py` under `blender -b
-P` (the way bake is Blender-only — see `pak.bake_way`'s docstring)
and then calls `emit_way` to write the dat alongside the rendered
atlas.  `emit_way` keys the dat's per-ribi image refs against
`pak/bake_way.py`'s popcount-then-ribi hex atlas layout (`image[-
][0]` at row 0 col 0, then 63 ribi labels left-to-right, 8 cells
per row — see `_HEX_WAY_LABELS` in `pak/dat.py`).  Per-blend strip
extras (e.g. extra debug meshes) ride on the SPEC's `strip=`
field (default `"Sphere"` — the upstream sun-direction
visualizer); the rail strand atom in `ns-cssr.blend` only needs
the default `Sphere` strip.

Slope sprites (`imageup[<slope_key>][N]`), seasons, the `front`
layer and `cursor` / `icon` are not yet baked, so `emit_way` omits
those keys — revisit when the slope-cell pass lands.

`Vehicle` fields cover both hex-engine (keys
`descriptor/writer/vehicle_writer.cc` reads) and
Simutrans-Extended schema (`bidirectional`, `comfort`, `axles`,
`tractive_effort`, `liverytype`, …).  `emit_vehicles` writes every
set field; the hex engine silently ignores keys it doesn't
recognise, so extended-only keys are harmless from its
perspective and shipping the full schema makes the dat
round-trip-capable with an Extended-aware tool.

Field-name = dat-key by default.  A few list fields override via
`metadata["dat_key"]`: `payload_by_class` emits as `payload[N]`
(matching upstream's class-indexed convention while leaving the
scalar `payload` hex-engine field free for the engine to read),
and `constraint_prev`/`constraint_next` emit as
`Constraint[Prev][N]`/`Constraint[Next][N]` to mirror upstream's
nested-bracket capitalisation.

Construction catches typos (`TypeError: unexpected keyword`).
Unset fields (`None` for scalars, `[]` for lists) are skipped on
emit, matching upstream's convention of omitting keys that take
the engine's default.  Shared-sprite multi-object bake scripts
pass a list of `Vehicle`s in a single `emit_vehicles` call;
distinct-sprite scripts call it once per output.

**Importable bake scripts.**  Asset names that start with a
digit (`4wheel_…`) aren't valid Python identifiers — a leading
`_` keeps the script importable
(`from trains import _4wheel_1850s_first`); generated artefacts
share the prefix so the triple moves and greps together.
Letter-leading names (`br_cl15`, `blackpool_brush`) go plain —
no underscore — **unless** the upstream dat stem has no hyphens
to translate (`vulcan.dat`), in which case the ported `.py`'s
sibling `.dat` would overwrite the upstream before `git rm` can
remove it.  Single-token letter-led names get the `_` prefix
too (`vulcan.dat` → `_vulcan.py`).  `pak/__init__.py` and
`trains/__init__.py` make the repo a proper package tree so
bake scripts can `from pak.dat import …` without a `sys.path`
hack.  Run as a module from the repo root:

    python3 -m trains._4wheel_1850s_first

Catalog-wide tooling imports the bake scripts as modules and
reads `SPEC` as a Python value without baking — see
`pak/reemit_dats.py` for the worked example (used by
the `reemit-dats` CI job; see "CI" below).  `Name=` inside the
dat is its own namespace — the pak's internal identity, hyphens
kept upstream-compatible, what makeobj keys on (verified in
`root_writer.cc`).

**Seeding a new asset.**  When porting fresh from upstream:

```python
from pak.dat import parse, port_vehicle, seed_python
for obj in parse(Path("trains/<asset>.dat")):
    print(seed_python(port_vehicle(obj)))   # paste into new bake script
```

`port_vehicle` is a one-time seeder, not called at bake time.
It returns a `Vehicle` populated from every field the dataclass
knows — including extended-only — so seeded SPECs preserve full
upstream fidelity.  `seed_python` renders only the non-default
fields (default dataclass `__repr__` would include every `=None`,
which gets unreadable fast at ~45 fields).  Indexed `payload[N]`
populates both scalar `payload` (max, what the hex engine reads)
and `payload_by_class` (the upstream class breakdown).

**Generated artefacts are committed** for "see the change in the
PR" review.  Debug renders, per-facing PNGs, diff visualisations
go to a `.gitignore`d `out/` and regenerate on demand.

**Upstream dats get deleted once ported.**  An upstream `.dat`
is the seeder input for `port_vehicle`; once a bake script's
SPEC is shown to match the upstream (run `port_vehicle` on the
upstream, diff against SPEC field-by-field — the verification
loop the 4wheel-1850s-first port followed), the upstream file
is `git rm`d.  This avoids the `Name=` collision that makeobj
would hit recursing over both upstream and ported dats, and
keeps `trains/` showing exactly two states per asset:
unported-flat or ported-triple, never both.

**Preserve upstream dat comments.**  Upstream `.dat` files
carry inline `#` comments that the seeder discards — provenance
notes (`# Artisan's cottage, perhaps`), derivation chains for
the surrounding numeric fields (`# 12 per house x 5 = 75, /16
hours * 6.4 = 30, half when meters/tile → 15`), authorial
context.  These explain *why* a value is what it is, which the
SPEC's bare number can't.  Carry them across to the bake script
as Python comments next to the relevant SPEC field (or above
SPEC when they describe the asset as a whole), before `git rm`-ing
the upstream.  Verbatim text is fine; trim only to fit the
80-col width.  Once the upstream is deleted, git history is the
only other place the comments survive, so the bake script is
the durable home.

**Asset scripts carry asset content, not infrastructure docs.**
Per-asset bake scripts are small (~30–60 lines): a one-line
docstring naming the asset, the SPEC (with its bake-meta fields),
and the `if __name__` invocation.  The docstring is not a place
for "`SPEC` mirrors upstream `<X>.dat`; `blend=` is shared with
every rail grade; `materials=` is the per-variant recolour — see
CLAUDE.md → 'Rail-grade material recolour'" template paragraphs,
"Run from the repo root: `python3 -m <module>`" invocation hints,
"First X port — exercises the Y axis of the Z schema" port-event
narration, or "See `<other-asset>.py` for the bake-unit pattern"
cross-references.  Shared infrastructure (the bake-unit shape,
the rail-recolour pattern, alignment modes, projection contracts)
lives in this file once; the port event is in `git log`; the
invocation rule is one `python3 -m` away from any module path.
Repeating any of it per-asset rots the moment the conventions
shift — and N copies of "see CLAUDE.md → …" add nothing past the
first.

What does go in an asset script: the upstream `#` comments
preserved as described above, SPEC-value rationale ("60 lb/yard
fits better — axle loading too low at Ahrons' 55"), genuine
calibration notes that don't generalise.  Domain caveats that
span multiple assets (e.g. cast-iron / fishbelly sprite-vs-era
mismatch, hex z compensation for buildings) belong in TODO.md or
CLAUDE.md once, not in N asset-script docstrings.

### Atlas layout

Each per-asset PNG is a single row of N facing renders, sliced by
makeobj into 128×128 sprites (cell width = pak tile width).
makeobj's image-ref parser (`descriptor/writer/image_writer.cc`)
reads `<file>.X.Y` as **row=X, col=Y**, so a single-row atlas
addresses its cells as `.0.<col>`.  Getting the order wrong gives
`invalid image number` when col exceeds the atlas width in cells,
or silently transposed rendering when both indices fit.

Column order is the `facings` list in `HEX_VIEWPOINT`
(`pak/viewpoints.py`): `S, SW, W, NW, N, NE, E, SE` for the
default 8-view bake.  Per-asset .dat keys (`EmptyImage[S]=…0.0`,
`EmptyImage[SW]=…0.1`, …) must match this order or the engine
renders the wrong sprite per facing — there is no run-time
consistency check.

Single-row is the default.  `compose_atlas(..., cols_per_row=N)`
exists for atlases that grow tall enough to be awkward (way ribi
tables, multi-state machinery); not relevant for 8-facing vehicles.

## Bake tooling

Lives at `pak/` in this repo, not in the blends repo
(blends are upstream-owned and stay reusable; our hex-rendering
opinions don't belong there).

**Fetch.**  `_fetch.py` is the shared HTTP / `.cache/` / lock-file
/ TOFU machinery; `fetch_blend.py` and `fetch_pak.py` are thin
per-`Source` wrappers; `fetch_wavs.py` is a batch helper over
`fetch_pak` driven by `bake_units.discover()`.  See "Asset
sourcing without cloning" above.

**Render.**  `render.py` is the `blender -b -P` harness; takes a
`Viewpoint`, strips the blend's authored Camera / Sphere / Lamp,
installs its own, writes one PNG per Facing.  Same code path
serves square (upstream-calibration) and hex (production)
projections.  `viewpoints.py` carries `SQUARE_VIEWPOINT` /
`HEX_VIEWPOINT` and the building / tree factory variants; facing
labels match across projections so .dat keys port without
relabelling.  `bake_way.py` is the way-bake driver (Workbench
backend, blender-only); see [`docs/bake-way.md`](docs/bake-way.md).

`render.py` has no asset-class knowledge — the parent builds the
`Viewpoint` via the appropriate factory and pickles a `RenderPayload`
to the subprocess (`pak.bake.run_render`).  This requires every field
of `Viewpoint` to round-trip through pickle, including the
`camera_ortho` / `sun_energy` / `fit_matrix` callables — keep those as
`functools.partial` of module-level resolvers (see the helpers at the
top of `viewpoints.py`); a `lambda` or nested-def closure breaks the
pickle silently and the subprocess fails on load.  Pinned by
`tests/test_viewpoints.py::TestViewpointPickleRoundTrip`.

**Compose.**  `compose.py` (pure PIL + numpy, no bpy) runs in the
parent Python after Blender exits: reads the per-facing PNGs,
crops per `Facing.slices` (multi-tile) and applies any
`Slice.alpha_mask`, pastes the cells into the final atlas,
writes `<name>.png` and prints a bbox summary.  Bake drivers
construct the same `Viewpoint` they pass to Blender via CLI and
hand it to `compose_atlas` -- factories are deterministic so the
slice layout the parent expects matches what Blender just
rendered.  Per-piece bridge and per-season building atlases
stitch one layer above, in `pak.bake` (`_stitch_bridge_atlas`,
`_stitch_seasons`).

**Dat schema.**  `dat.py` defines the `Vehicle` / `Way` /
`Building` / `Tree` dataclasses + `parse` / `port_*` seeders +
`emit_*` writers.  Field-name = dat-key by default; list fields
remap via `metadata["dat_key"]`.  The freight-image subsystem
(`freightimage[<dir>]` etc.) is the one area `Vehicle` doesn't
model yet — see TODO.md.

**Upstream image-ref derivation.**  `upstream.py::image_stem(dat,
name=)` fetches an upstream dat, finds the matching object (by
`Name=` for multi-object dats like `citybuildings/com-1870.dat`),
and returns the pak-relative path stem encoded in its first
`*Image[…]=` ref — strips the trailing per-image offset, the
`.<row>.<col>` atlas coords, and any `_<facing>` suffix.  Diff
harnesses append their per-class extension (`_<facing>.png`,
`-<season>-<age>_<facing>.png`, `.png` for buildings).  The dat
is the source-of-truth identity each SPEC carries
(`upstream_dat=`); image refs follow.

**Materials.**  `materials.py` defines `Material` / `Slot` /
`Lighting` carried on each building/way SPEC's `materials=` /
`lighting=` bake-meta fields.  `blend_slots.py` is a minimal
pre-2.5 .blend parser that recovers BI's Material+MTex struct
array (Britain's blends predate the 2.5 file format so the legacy
layout survives even though 2.80+ dropped the
`material.texture_slots` API).  `extract_materials.py` is the
one-shot seeder for paste-ready `materials={...}` blocks.

**Diff (calibration / regression).**  `diff.py` carries the shared
silhouette IoU / dRGB / XOR primitives plus the `cell_metric` +
`compose_grid` helpers every per-class harness composes against;
specialisations live in `diff_upstream` (vehicles), `diff_buildings`
(two calibration metrics over one rendering pipeline -- `run` does
layout-permutation discovery against upstream's strip-atlas, used
for assets where the dat-level L→column mapping isn't fixed;
`run_multitile` parses upstream's `backimage[l][y][x]` keys for a
direct per-cell map, slices our 512² canvas at the tile lattice,
and stitches upstream's per-cell PNGs back onto the same lattice
-- emits `grid_tiles.png` per (L, y, x) cell plus `grid_stitched.
png` per layout, both square-vs-square so the IoU is calibration-
grade), `diff_trees`,
`diff_grounds` (parametric grounds via `SquareGeom`), `diff_fence`.
`MAGIC_PINK` is the canonical transparency key; alpha threshold on
`silhouette_mask` tunes per class (vehicles/trees `>16`,
buildings/fence `>0`; soft-AA story in
`diff_buildings._silhouette_mask` docstring).

**Drivers.**  `bake.py` carries the per-asset entry points
(`bake_vehicle`, `bake_way`, `bake_building`, `bake_tree`) bake
scripts call.  `bake_units.discover()` enumerates every per-asset
script (`.py` with `.dat` + `.png` siblings) and is the shared
definition of "ported asset" consumed by `reemit_dats` (catalog-
wide dat re-emit, the CI lint job), `fetch_wavs`, `check`, and
`tests/test_ported_dats`.  `check.py` dispatches per-bake-script
by `SPEC` type to the right diff harness and prints metrics.

**Tuning.**  `tune_materials.py` is a gradient solver for the
per-asset `materials=` dict against the blurred dRGB metric.
Caveat: adding `color=` to an image-only material flips the
`image x blend_diffuse` heuristic to `image x gain`, breaking the
small-gradient assumption — opt in with an explicit `color=`
starting point.  `diag_per_material.py` attributes dRGB by
material (with `--all` aggregating across the catalog to surface
systematic gaps); its mean-per-px metric is id-map-coverage-
weighted and doesn't match `check.py`'s intersection-mean, so use
for relative ranking only.

**Geometry shared.**  `hex_synth.py` / `square_synth.py` carry
`HexGeom` / `SquareGeom` — partition, region, fill, outline
primitives consumed by the parametric ground bakers and
`diff_grounds`.  Both implement the same `Geom` interface so the
generic helpers in `hex.py` work against either projection without
isinstance branches.  `SquareGeom` is calibration-only (not on the
hex production path).

**Tests.**  `tests/test_dat.py` (parse / emit / port round-trips +
schema-enforcement-at-construction), `tests/test_square.py`
(`SquareGeom` geometry pinned to upstream's
`texture-lightmap.png`), `tests/test_way.py` (path geometry +
bisect convention).  Run via `python3 -m unittest` or `pytest
tests/`.

The Britain blends already carry the `sp_*` material-name
convention for player-colour masks; port that pass over from the
upstream render script when the first asset bake needs masks.

### Running the bake in a fresh sandbox

Ubuntu 24.04 (and the CCW image it derives from) ships nothing
3D-relevant by default.  Minimum install to run a per-asset
`bake.py` end-to-end:

```
apt-get install -y blender python3-numpy python3-pil libegl1
```

This is a normal, expected step — go ahead and run it without
asking when the bake / diff tooling needs it.  Agents have been
hesitant to install system packages in the CCW container; don't
be.  The container is ephemeral, the apt install is reversible
on the next session.

`blender` (4.0.2 on noble) provides the `blender -b -P` harness;
its bundled Python is the system `python3.12`, so `python3-numpy`
lands `numpy` where `render.py`'s `import numpy as np` will
find it.  `python3-pil` (Pillow) is only needed by
`diff_upstream.py` for the side-by-side grid composition, not by
the Blender harnesses themselves.  `libegl1` is the runtime
Blender's GL backend dlopens — without it Cycles aborts with
SIGABRT before the first render even though `--background` would
suggest no display needed.

The CCW base image's `/usr/local/bin/python3` is Python 3.11 and
has its own broken numpy; the apt packages target the system
3.12, so invoke the bake / diff tooling explicitly as
`python3.12 -m …`, not `python3 -m …`, or the import chain blows
up before the bake starts.

No GPU required; Cycles falls back to CPU.  ~4 s per facing on
a small carriage.

## Building-bake architecture

Buildings (`Obj=building` — attractions, monuments, city
buildings, townhalls, HQs, stops, extensions) port via a typed
`Building` SPEC + `bake_building_main(SPEC, __file__)`.  Per-cell
EEVEE renders driven by the footprint
(`backimage[layout][y][x][height][phase][season]`); per-asset
`materials=` + `lighting=` declared on the SPEC.  See
[`docs/bake-building.md`](docs/bake-building.md).

Factories (`Obj=factory` — industries) port via `Factory(Building)`
+ `bake_factory_main`.  Engine `factory_writer.cc` delegates to
`building_writer.cc` for every visual field, so the bake pipeline
(viewpoint, atlas layout, season stitching) carries through
unchanged; only the dat emitter swaps the obj header and walks the
extra factory-only scalars + parallel input/output good lists.
Shared-sprite multi-Obj uses `SPECS: list[Factory]` (e.g. chemist's
1860 + 1955 upgrade pair sharing one render).

## Way-bake architecture

Ways (rails, roads, trams) treat an upstream rail-shape blend
(e.g. `ways/ns-cssr.blend`) as the **elementary geometric atom**
and compose it into 63 hex ribi cells by cloning, clipping and
transforming onto each ribi's path.  Workbench backend (blender-
only).  Path geometry in `pak/way.py` + `pak/way_topology.py`;
bake driver in `pak/bake_way.py`.  Per-way visual differentiation
is `materials=` recolour on the SPEC in `ways/<way>.py`.  See
[`docs/bake-way.md`](docs/bake-way.md).

## Tree-bake architecture

Trees (`Obj=tree`) port via a `Tree` SPEC +
`bake_tree_main(SPEC, __file__)` — a single-facing
billboard expanded over an `ages × seasons` grid.  Five ages
(engine hardcoded) come from one model at four successive scales
plus a `winter-3` fallback for age 4 via `clamp_age_overrides`.
EEVEE backend.  See [`docs/bake-tree.md`](docs/bake-tree.md).

## Tunnel-bake architecture

Tunnels (`Obj=tunnel`) port via a `Tunnel` SPEC +
`bake_tunnel_main(SPEC, __file__)` — 6 hex-edge portal facings
rendered through `tunnel_hex_viewpoint()` into a single-row 6-cell
atlas.  Facing labels are `n, ne, se, s, sw, nw` matching
`hex_keys::edge_names` in the engine writer; `emit_tunnel` ships
lowercase `frontimage[<edge>][0]=` only.

**Two opposite key conventions live in this codebase.**  The hex
engine uses **low-edge** naming -- `frontimage[<edge>]` = portal
whose mouth faces `<edge>` (the direction a train exits) -- so
`_HEX_TUNNEL_MODEL_ROT_DEG`'s rotation table is just
`θ(e) = world_angle_of(e)`.  Upstream pak128.Britain inherits
pak64's **high-edge** naming -- key names the edge the mountain
rises against, mouth points opposite -- so `FrontImage[S]` shows
mouth-points-north.  `tunnel_desc.cc:9-34` documents the engine's
N↔S, E↔W permutation between the two ("pre-port pak64 tunnel
images load at slots with N↔S and E↔W permuted; new hex art needs
to follow the low-edge convention").  Production hex stays
low-edge; `tunnel_square_viewpoint`'s calibration rotation table
goes high-edge so a label-to-label diff against upstream cells
aligns cell-for-cell.

`diff_tunnel` alpha-composites upstream's `BackImage` under
`FrontImage` per facing -- same pattern as
`diff_buildings._stitch_upstream_layout` specialised to the tunnel
case where both layers land on the same 128² cell.  Stone-tunnel
ships Back only for N/W, so S/E rows fall back to Front-only and
carry an XOR contribution from our whole-portal silhouette (worst
IoU ~0.72 on those rows, ~0.81 on Back-present rows;
`FAIL_IOU=0.65`).  Future variants (e.g. brick-face) that ship
Back on all four cardinals will test the apples-to-apples Back+Front
path directly.

## CI

Two workflows, matching `hextrans-pak128`'s split:

**Lint** (`.github/workflows/lint.yml`, push + PR).  `rebake`
re-runs every asset baker — parametric grounds via `make
bake-grounds`, plus a tiny fixed Blender-driven vehicle + way
sample inlined in the workflow — and asserts
`git diff --exit-code`.  Same principle as `reemit-dats`,
different backends; covers render-pipeline drift in
`grounds/<asset>.py` and renderer non-determinism across CI
runners.  See the workflow's "Re-render the Blender-driven
determinism sample" step for the sample's asset list.

Two renderer backends, two determinism strategies.  Ways bake
through Workbench (`pak/bake_way.py::_configure_render`,
`light = "FLAT"`, `color_type = "MATERIAL"`) -- single-pass
rasterizer, no path tracing, no embree, no SIMD-sensitive
reductions; byte-stable across heterogeneous CI runners in
practice.  Vehicles + buildings bake through Cycles
(`pak/render.py::_install_camera_and_sun`) and pin
`threads_mode = "FIXED"; threads = 1`, `use_denoising = False`,
`use_adaptive_sampling = False`, `seed = 0` -- defends every
same-CPU-class non-determinism source we know about, but Intel
vs AMD running the AVX2 kernel still diverge on transcendentals
/ embree (max per-channel delta ~185 on the cssr atlas when we
tried Cycles for ways).  Cycles for vehicles is an empirical
choice that landed acceptable dRGB on the first ported assets,
not a literal match to upstream's authoring engine (which was BI
under 2.79 -- see "Lighting calibration" above).  If a vehicle
flakes cross-CPU in CI, switching it to Workbench or EEVEE would
re-anchor its IoU calibration but not break a Cycles-native
upstream target (no such target exists); cross that bridge when
it bites.

If a flake appears, `pak/diag_png_drift.py` runs as a
post-failure step and reports whether the drift is in the pixel
data or only in the PNG encoding (zlib / chunk layout) -- the
latter would be a libpng / image_settings issue, not the
renderer.  `reemit-dats` runs
`python3 -m pak.reemit_dats` (imports every bake script, re-runs
the matching emitter from `SPEC` / `SPECS` — no Blender, no
render) and asserts `git diff --exit-code -- '*.dat'`; catches dat
drift between bake script and committed `.dat` sibling on every push.  `tests` runs the `python3 -m unittest` suite under
`tests/` (needs `numpy` for the `pak.hex_synth` import chain pulled in
by `test_square_synth`).

`ruff` runs `ruff check .` against `pyproject.toml`'s
`[tool.ruff.lint]`.  Ruleset is scoped to **bug classes the rest of
the system wouldn't catch faster** (F undefined-name / unused-import,
W whitespace, I import sorting, UP outdated typing, B bugbear,
PLE pylint errors, NPY numpy correctness, RUF100 unused noqa,
A builtin shadowing); stylistic-only checks are dropped (E501 line
length, E702 intentional `a; b` pairs, E741 `l` collides with the
engine's `(l, y, x)` building-layout loop convention).  Selection
is explicit per code-group rather than wildcard-with-ignores, so
new ruff releases don't quietly extend either side -- the bar for
adding a group is "found a bug in this codebase or has near-zero
false-positive rate".  Same philosophy as "Test value rules"
below — catch the bug, skip the noise.  Net real-bug catch on
adoption was near-zero; the value is prophylactic.

Full vehicle/way *render* rebake is not wired — the per-asset blend
fetch + Cycles cost (~minutes per asset) makes a full sweep too
heavy for every push.  Selective rebake (gated on `bake.py` or
`blends.lock` diff) is a future-work entry in `TODO.md`; the
Blender-driven half of `rebake` is the always-on canary that's
cheap enough to run unconditionally.

**Build** (`.github/workflows/build.yml`, push + PR + manual).
Clones `SupraSummus/hextrans`, builds `makeobj`, runs
`make MAKEOBJ=./makeobj clean all archives`, publishes
`simupak128.Britain-Ex-nightly.zip` to the `Nightly` GitHub release
on `main` pushes.  Scope is gated in the Makefile (see
`TODO.md` → "Expand build scope as categories bake"): the
top-level `DIRS128` list selects which categories the build
visits, and the per-dir `ported_dats` filter narrows that to
`.dat` files with a sibling `.png` so a partly-ported dir's
upstream-reference dats stay out of makeobj's input list.  No
upstream PNG-fetch indirection: ported assets compile, unported
ones are silently skipped.

The `copy` step fetches `demo.sve` and `symbol.BigLogo.pak` from
the `pak.lock`-pinned upstream pak via `pak/fetch_pak.py`
— both were stripped from history (binary deliverables, no source)
and are filled in at build time rather than committed.

Full rebake on demand for blends-repo SHA bumps.

## Externalize the thinking

Long internal monologue on a hard design call is brittle.  A
private chain of reasoning has no sanity check beyond the agent's
own confidence, and if the session is interrupted or compacted
the work disappears with it.  Default to thinking on the page:
short visible checkpoints describing what's being figured out,
what's been ruled out, what the next probe is.

When the idea is concrete enough to live in the repo, write it
there — a stub `bake.py` with a fatal body and a one-line
comment, a paragraph in `TODO.md`, a half-finished commit on the
working branch.  All durable, all visible, all give the user a
place to redirect before the agent spends an hour chasing the
wrong shape.

This applies hardest to the design questions the port keeps
producing: scale calibration, sun convention, dat-key triage,
multi-tile asset slicing.

## Test value rules

A test earns its keep by catching a class of bug the rest of the
system wouldn't catch faster or more clearly.  Before adding one,
ask:

- Does runtime already fail loudly on this?  If the bake driver
  already raises `RuntimeError: --materials targets unknown blend
  materials: [...]` on a typo'd material name, a test that walks
  every script and matches keys against a hardcoded slot table
  isn't catching a missed case -- it's just trading bake-time
  signal for push-time signal on a bug class that runtime already
  reports clearly.
- Does the test mirror a source of truth that lives elsewhere?
  If the blend file is the authority on what materials exist, a
  test that hardcodes the slot set per blend forces every new
  blend to update the test in lockstep.  Two places to keep in
  sync is worse than one place that fails loud.
- How often does the bug class actually occur?  A test that
  catches RGB-out-of-range and 2-tuples-instead-of-3-tuples earns
  its keep at near-zero cost; a test that forces a slot-table
  update on every new blend port doesn't.

Structural shape checks (a thing is the type / arity / range you
declare) are cheap and worth it.  Cross-checks against an
authoritative source elsewhere in the system are expensive and
usually aren't.  When in doubt, prefer fewer tests with smaller
maintenance surface; lean on runtime errors with clear messages.

## Comment brevity

Defaults from the system prompt: write no comment unless the
WHY is non-obvious; never explain WHAT the code does.  Three
project-specific patterns that show up here and inflate
comment volume:

*Restate-don't-repeat.*  A formula, convention or constant
documented at its definition (e.g. `hex_layouts_default`'s `6
// gcd(6, N)`) shouldn't be restated at every consumer.  Field
comments / call-site comments defer to the definition with a
one-line "see X" rather than re-deriving the math.  Updates
then land in one place.

*Asset scripts carry asset content.*  Pak-side conventions
(layout policy, projection facts, schema-vs-engine
differences) live in `CLAUDE.md` or `TODO.md` once;
per-asset SPEC comments preserve the upstream `#` provenance
notes and SPEC-value rationale that genuinely belong with the
asset.  "Upstream `layouts=4` drops in favour of hex's
6-fold default" is framework narration that decays as soon as
the policy moves; CLAUDE.md is the durable home.

*Cross-references rot.*  "See TODO.md -> X" / "see also
`other_function`" lines are tempting and almost always become
wrong: the named entry resolves, the named function is
renamed.  Leave the breadcrumb only when the link is
structural (a known open bug the reader needs to find);
context-only cross-refs belong in the commit message instead.

## TODO.md rules

`TODO.md` tracks work in flight — porting status, gameplay bugs,
upstream-inherited rough edges, anything else worth tracking
centrally rather than as a scattered code comment.

It is not a changelog.  When an entry is resolved or becomes
outdated, **delete it**.  Do not strike it through, do not leave
a "(done)" note.  Git history is the changelog.

Use paragraphs, not bullet lists.  Paragraphs are easier to
insert and delete; lists encourage atomic-bullet thinking and
accumulate noise.

Every entry must name a concrete next move — what the fix would
actually look like.  "Verify in-game once a pakset is available"
or "eyeball when somebody runs the game" aren't next moves,
they're hopes.  A trigger is useful when one exists ("lands with
the depth-clip slicing — see <other entry>"), but a soft trigger
like "when next refactoring this cluster" is fine — the bar is
that the work is actionable.

A growing `TODO.md` is fine; a stale one is not.

## Doc trim rules

CLAUDE.md and TODO.md bloat over time — investigations get recorded,
verifications get filed, speculation accumulates.  Run a trim pass
when a file's grown hard to skim.

The frame is "does the next person need this to do their job?", not
"is this true?".  Most stale content is technically true.

For TODO.md, the keeper shape is "implemented, but case XYZ probably
breaks because Y" — a specific suspected failure with a fix to try.
"Implemented, go look at the output" without a predicted symptom is
a hope.  Verify any "blocking" or "in the way" trigger claim against
actual workflow state before trusting it.

For CLAUDE.md, one-off operational commands belong in git history.
Investigation records ("we considered X, rejected it") compress to
the one-sentence conclusion.

One theme per pass.  Trimming and restructuring mix badly.  Re-read
your own compressions with fresh eyes — they introduce factual drift
in a way deletions don't.

## Commit message rules

Default to short.  The diff already shows *what* changed; the
message captures only the *why* a reader can't recover from it.
A one-line subject with no body is the right answer for
mechanical fixes and obvious refactors.

Subject: short, present-tense, scope-prefixed (`hex-port:`,
`bake:`, `dat:`).  Keep the prefix consistent across commits in
the same area.  ≤ 72 chars, no metrics.

Body: usually 1–2 short paragraphs, often none.  Cover the
load-bearing reason a reader can't recover from the diff — a
non-obvious trade-off, a porting decision, a dropped
extended-only feature.  Don't:

- Re-explain the surrounding subsystem; link to the file, symbol
  or prior commit.
- Enumerate every dat key dropped or facing rebaked.
- Narrate verification ("re-baked, byte-identical", "atlas
  reproduces").
- Recap the companion engine / blend-repo commit; name it and
  stop.
- Inline durable design context.  That belongs in `CLAUDE.md` /
  `TODO.md`, where it stays current.

If a body is getting long, prefer splitting the commit or moving
the context here.

**Author identity comes from `git log`, not the system prompt.**
Hosted-session environments often inject a label like `jan
<jan@techlabee.ai>` into the harness's user info, but the
authoritative author for this repo is whatever `git log
--format='%an <%ae>' | sort -u` shows.  Use that.  Don't trust
the surrounding metadata; look it up before any `--author=` /
`-c user.name=` operation.

Prefer the GitHub noreply form -- `Real Name
<<id>+<username>@users.noreply.github.com>` -- when `git log` shows
multiple email variants for the same person (real name + private
gmail-style + noreply): the noreply email never leaks a private
address, is what GitHub matches commits against for contributor
attribution, and is what the GitHub web UI uses for new commits by
default.  Look up the numeric id via `mcp__github__search_users`
when it's not already in history.
