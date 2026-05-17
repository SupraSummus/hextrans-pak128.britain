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
  `https://github.com/jamespetts/Pak128.Britain-blends`
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
   deck heights via `…/render.py::engine_z_per_step`.
2. **Sun direction.**  The upstream
   `render_SimutransRender_pak128Britain-65.py` rotates the sun
   with the camera (correct for square 8-view).  Hex pins one
   world sun direction (south + 60° elevation — match
   `render.py::SUN_DIR`) and rotates the model under it, so
   shading stays consistent across facings.
3. **Image pixel orientation.**  `bpy.types.Image.pixels` is
   bottom-up (origin at bottom-left).  PIL and
   `hextrans-pak128/tools/threed/bespoke.py::bake_atlas` work
   top-down.  `render.py` flips on load and again on save so
   the in-memory atlas representation matches upstream's
   convention (and bbox printouts read row-from-top).  Forget the
   flip and the atlas comes out vertically mirrored — silently
   rendered, silently saved, only caught by eye.
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
the cell instead of overflowing it.  `pak/render.py::_strip_scene`
reads the camera's ortho_scale before stripping it; `_compute_fit`
then builds the per-asset scale `2R / blend_ortho_scale` (defaults
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

**Z = 0 is the renderer's hex-frame floor, not an upstream
invariant.**  The .blend's native z = 0 is wherever the artist left
it; visible geometry routinely dips below (e.g. 4wheel-1850 has
`z_min ≈ −1.54`).  The hex renderer pins the lowest visible vertex
to z = 0 by computing `z_floor = min(zs)` and translating by
`−z_floor`.  Don't read the upstream z origin; let the bbox drive
the shift.

**XY centring is per-asset, not per-frame.**  Artists place the
asset anywhere inside the camera view; upstream compensates with
per-facing camera offset (`"vehicles"` alignment vs `"bases"` /
`"normal"`).  Hex bakers re-centre under their fixed camera using
the bounding-box midpoint; this is the only piece of fit math that
reads the model, and it reads only position, never scale.

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
  * **Colour** — mean abs(RGB-delta) restricted to the silhouette
    intersection.  Colour-only; pixels missing from one or the other
    don't bleed in.

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

`pak/check.py` is the driver: it imports a bake script,
reads `BLEND` and `UPSTREAM_STEM` (declared next to `SPEC`), and
runs the diff with no extra path-passing.  `--all` sweeps every
bake script under `trains/` for a fleet-wide summary; scripts
without `UPSTREAM_STEM` are skipped with a notice (fill in when
the upstream sprite stem is known).

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
  4wheel-stanhope.dat     # unported upstream (seeder input)
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
inline as a typed `Vehicle` instance and a blend reference, then
calls `bake_main` from `pak/bake.py`.  The full
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
)
BLEND = "trains/Carriages/4wheel-1850.blend"

if __name__ == "__main__":
    bake_main(SPEC, BLEND, __file__)
```

`bake_main` derives out-dir + basename from `__file__` and calls
the underlying `bake_vehicle` (fetch-blend / run-render /
emit-dat).  Both accept either a `Vehicle` or a `list[Vehicle]` —
shared-sprite multi-object scripts pass `SPECS` to the same entry
point and the dat-emit step writes one combined dat.  Distinct-
sprite multi-object bake units skip the convenience and call
`bake_vehicle` directly per output, with distinct `basename` (and
typically distinct `blend`) per call.

**Ways follow the same shape.**  A way bake script holds a typed
`Way` (covers the hex-engine `Obj=way` schema + the few extended
keys upstream Britain dats carry: `wear_capacity`, `axle_load`)
plus a `BLEND` and a `bake_way_main(SPEC, BLEND, __file__)` call:

```python
from pak.bake import bake_way_main
from pak.dat import Way

SPEC = Way(
    name="cssr", waytype="track",
    intro_year=1968, intro_month=3,
    topspeed=160, max_weight=22,
    wear_capacity=4128000000,
    cost=140000, maintenance=375,
)
BLEND = "ways/ns-cssr.blend"

if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__)
```

`bake_way_main` shells out to `pak/bake_way.py` under `blender -b
-P` (the way bake is Blender-only — see `pak.bake_way`'s docstring)
and then calls `emit_way` to write the dat alongside the rendered
atlas.  `emit_way` keys the dat's per-ribi image refs against
`pak/bake_way.py`'s popcount-then-ribi hex atlas layout (`image[-
][0]` at row 0 col 0, then 63 ribi labels left-to-right, 8 cells
per row — see `_HEX_WAY_LABELS` in `pak/dat.py`).  Per-blend strip
extras (e.g. extra debug meshes) thread through `bake_way_main(...,
strip="Sphere,Ruler")`; the rail strand atom in `ns-cssr.blend`
only needs the default `Sphere` strip.

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
no underscore.  `pak/__init__.py` and `trains/__init__.py`
make the repo a proper package tree so bake scripts can
`from pak.dat import …` without a `sys.path` hack.  Run as a module from the repo root:

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
PR" review.  Cumulative atlas weight gets measured after the
first batch lands (`TODO.md` → "Atlas commit vs.
CI-artefact-only").  Debug renders, per-facing PNGs, diff
visualisations go to a `.gitignore`d `out/` and regenerate on
demand.

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
docstring naming the asset, the SPEC, the blend reference, the
`if __name__` invocation.  The docstring is not a place for
"`SPEC` mirrors upstream `<X>.dat`; `BLEND` is shared with every
rail grade; `MATERIALS` is the per-variant recolour — see
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

Single-row is the default.  `render.py --cols-per-row N` exists for
atlases that grow tall enough to be awkward (way ribi tables,
multi-state machinery); not relevant for 8-facing vehicles.

## Bake tooling

Lives at `pak/` in this repo, not in the blends repo
(blends are upstream-owned and stay reusable; our hex-rendering
opinions don't belong there).

Present:

- `pak/_fetch.py` — shared `Source`-driven HTTP fetch + `.cache/`
  resolver + lock-file parser/emitter + validate-or-record.
- `pak/fetch_blend.py` / `pak/fetch_pak.py` — thin per-source
  wrappers over `_fetch`.  `Source` carries the GitHub slug, lock
  filename and `.cache/` subdir; each wrapper re-exports `fetch`
  for its source.
  Used by `diff_upstream.py` today and by future runtime `.wav`
  fetching (see `TODO.md`).
- `pak/render.py` — `blender -b -P` harness that takes a
  `Viewpoint` and renders one atlas (plus optional per-facing PNGs).
  Strips the blend's Camera / Sphere / Lamp objects on entry and
  installs its own from the Viewpoint — the .blend is treated as
  pure model data.  Same code path serves the upstream square
  reference and this project's hex projection; the only difference
  is which `Viewpoint` gets passed in.  Applies the upstream blend
  calibration contract (see above) and emits a single-row atlas PNG.
- `pak/viewpoints.py` — `SQUARE_VIEWPOINT` (reproduces
  the upstream `render_SimutransRender_pak128Britain-65.py`
  "vehicles" alignment verbatim) and `HEX_VIEWPOINT` (camera looking
  +Y at origin, ortho_scale=2R, hex shear baked into mesh via
  `extrinsic`, model rotated per facing).  Same facing labels in
  both so .dat keys port without relabelling.
- `pak/diff_upstream.py` — drives `render.py --viewpoint
  square --keep-per-facing`, fetches the matching upstream PNG via
  `fetch_pak.py`, and reports the contour and colour metrics from
  "Calibration validation loop" above (silhouette IoU + XOR pixel
  count, and intersection-restricted mean abs(RGB-delta)).  Returns
  non-zero if any facing is below 0.90 IoU.
- `pak/check.py` — convenience driver around
  `diff_upstream.py` / `diff_buildings.py`.  Takes a bake-script
  path (or `--all`), imports it, reads `BLEND` and `UPSTREAM_STEM`
  from the module, dispatches by `SPEC` type (Vehicle vs Building)
  to the matching diff harness, prints metrics.  Vehicle SPECs go
  through the worst-IoU + sum-XOR-pixel summary; Building SPECs
  produce the N×N permutation matrix described below.
- `pak/diff_buildings.py` — square-projection diff harness for
  ported buildings.  Renders the blend through
  `building_square_viewpoint` (upstream's normal-alignment cardinal
  cameras, blend's authored ortho_scale) and slices the upstream
  atlas PNG into per-layout cells.  Reports an N_layouts ×
  N_layouts IoU matrix `M[our_L][upstream_C]` plus the best-
  matching permutation -- when ours ≠ identity, our layout
  rotation convention permutes vs upstream's dat-declared mapping,
  which is the diagnostic for landmine (a) in "Building-bake
  architecture" above.  Handles upstream's RGB + magic-pink
  transparency (vs our renders' proper RGBA) via
  `_silhouette_mask`.  Single-tile (`dims = 1×1`, heights=1) only;
  multi-tile per-cell diffs need a square tile lattice -- deferred.
- `pak/square_synth.py` — `SquareGeom`, a sibling to
  `HexGeom` implementing pak128.Britain's square-dimetric tile
  layout (4 corners, base-3 slope encoding, 128×128 cells with the
  flat lozenge spanning `y = 64..127`).  Same `Geom` interface as
  `HexGeom` — `corner_count`, `corner_world_xy`, `corner_projected_xy`,
  `all_chords`, `corner_labels`, `full_path`, plus
  `decode_corner_heights` / `iter_valid_slopes` / `slope_is_valid`
  — so the generic partition / region / fill / outline helpers in
  `hex.py` work against either projection without isinstance
  branches.  Exists for `diff_grounds.py`'s test harness (see
  below); not on the hex production path.
- `pak/diff_grounds.py` — square-projection diff harness
  for the parametric ground bakers.  Re-runs `grounds/<asset>.py`
  through `SquareGeom`, fetches the matching upstream PNG +
  `Image[N]=...` dat via `fetch_pak`, parses the slope→cell map
  (multi-object dat support; scope by `Name=`), and reports
  per-cell silhouette IoU + per-region brightness ratio.  The
  asset's `min_iou` in the `ASSETS` table is the calibrated
  regression floor (slightly under the current measured min, so
  drift below trips CI without flagging today's baseline).  Today
  only `light_texture` is wired in — mean IoU 0.97, min 0.90 vs
  upstream's authored cell atlas; mean ratio ≈ 1.1× reflects the
  hex-engine lightmap multiplier scale vs pak128-standard's, not a
  generation bug.  The point of the harness is to exercise slope
  decode + partition + Lambert + fill + atlas layout end-to-end
  against authored ground truth; extend `ASSETS` per baker (see
  TODO.md → "Square-bake diff harness coverage").
- `pak/dat.py` — Simutrans `.dat` parse / port / emit.
  Exposes `Vehicle` (typed dataclass covering both hex-engine
  and Extended schema; list fields may carry
  `metadata["dat_key"]` to remap field-name → dat-key, e.g.
  `payload_by_class` → `payload[N]`), `parse(path)` (splits
  multi-object dats into `list[list[(k, v)]]`), `port_vehicle`
  (one-time seeder: upstream object entries → fully-populated
  `Vehicle`), `seed_python(vehicle)` (paste-ready non-default-only
  source repr for a new bake script), and
  `emit_vehicles(list_of_vehicle, out_dir, basename)` (writes
  one combined dat where every block points at the same atlas;
  pass a one-element list for the single-vehicle case).  The
  freight-image subsystem (`freightimage[<dir>]`,
  `freightimage[N][<dir>]`, `freightimagetype[N]`) is the one
  area `Vehicle` doesn't model yet — see `TODO.md`.
- `pak/bake.py` — per-asset bake driver.
  `bake_vehicle(spec, blend=..., basename=..., out_dir=...)`
  fetches the blend, runs the hex renderer, writes the atlas
  PNG, and emits the dat.  `spec` may be a single `Vehicle` or a
  `list[Vehicle]` (shared-sprite multi-object — emit_vehicles
  writes one combined dat).  `bake_building` accepts an optional
  `materials=MATERIALS` dict (see `pak.materials`) routed to
  `pak/render.py --materials`.  Bake scripts shrink to imports +
  SPEC (or SPECS) + a single `bake_main(...)` call.
- `pak/blend_slots.py` — minimal pre-2.5 .blend parser; reads
  BI's Material+MTex struct array (image refs, texco, size, ofs,
  per-material rgb+alpha) directly from the binary.  Britain's
  blends are all saved by Blender 2.42/2.48 so the legacy struct
  layout survives even though 2.80+ dropped the
  `material.texture_slots` API.  CLI: `python3 -m pak.blend_slots
  <blend>` dumps every material's slot table.
- `pak/materials.py` — `Material` dataclass (image / texco /
  size / ofs / noise) carried in each `citybuildings/<asset>.py`
  as `MATERIALS = {...}`.  `to_jsonable` / `from_jsonable`
  serialise for subprocess transit; `seed_python` emits paste-
  ready source.  See "Texture rebinding" above.
- `pak/extract_materials.py` — one-shot seeder.
  `python3 -m pak.extract_materials <blend>` prints the
  `MATERIALS = {...}` block to paste next to SPEC; collapses each
  material to its first IMAGE slot or fallback CLOUDS/NOISE slot.
- `pak/bake_units.py` — `discover()` returns every
  per-asset bake script (`.py` with `.dat` + `.png` siblings outside
  `pak/`, `tests/`, `grounds/`, `simutranslator/`), `import_script
  (path)` imports it by its repo-relative dotted name, and
  `specs_of(mod)` normalises a script's `SPECS` (multi-object
  shared sprite) or `SPEC` (single) attribute into a list — one
  definition of what counts as a ported asset, shared by
  `reemit_dats`, `fetch_wavs`, `check`, and `tests/test_ported_dats`.
- `pak/reemit_dats.py` — catalog-wide driver that
  imports every `discover()`-ed bake script and re-emits its dat
  from `SPECS` (multi-block via `emit_vehicles`) or `SPEC` (single
  via the right per-type emitter).  No Blender, no render.  Wired
  into CI as the `reemit-dats` lint job to catch dat drift on
  every push.  Raises on a bake script with neither — distinct-
  sprite multi-object units (one script emitting multiple
  `<basename>.{dat,png}` triples) still need a per-script reemit
  hook (see `TODO.md` → "Multi-object reemit hook").
- `pak/fetch_wavs.py` — catalog-wide driver that walks
  `bake_units.discover()`, reads `sound` off every `SPEC` /
  `SPECS` Vehicle, and pulls each unique wav from the upstream
  pak via `fetch_pak`.  Invoked by
  the Makefile `copy` step to stage sounds into `$(PAKDIR)/sound/`
  on every build.
- `tests/test_dat.py` — `unittest`-based smoke tests for parse,
  emit, port, seed_python, and the schema-enforcement-at-
  construction property.  Run via
  `python3 -m unittest tests.test_dat` (or
  `python3 -m pytest tests/`).
- `tests/test_square.py` — geometry assertions for
  `SquareGeom`: slope encoding (base-3 weights, `Image[N]` corner
  mapping), validity filter (normalised + adjacency ≤ 2, 65 slopes
  total), screen layout pinned to upstream's `texture-lightmap.png`
  cells, partition output for known slope shapes, and the shared
  `Geom`-interface attribute surface that the generic helpers
  consume.  The pinned values come from upstream and don't move,
  so a future projection refactor has to re-justify itself against
  the same ground truth as the diff harness.

The Britain blends already carry the `sp_*` material-name
convention for player-colour masks; port that pass over from the
upstream render script when the first asset bake needs masks.

Atlas composition is implemented inline in `render.py` rather
than imported from `hextrans-pak128/tools/threed/bespoke.py::bake_atlas`
because `bespoke` uses PIL and Blender's bundled Python on Ubuntu
ships only `numpy` (see "Running the bake in a fresh sandbox"
below).  The API surface mirrors `bake_atlas` (label/cell entries,
`cols_per_row`, per-cell bbox printout) — port across if/when the
two converge into a shared package.

When the bake tooling stabilises it's a candidate for extraction
into a shared `simutrans-threed` Python package consumed by both
this pakset and `hextrans-pak128`.  Don't extract before the
second consumer has bent the API at least once.

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
buildings, townhalls, HQs, stops, extensions) port via the same
shape as vehicles: a typed `Building` SPEC in a per-asset bake
script, a `BLEND` path, and `bake_building_main(SPEC, BLEND,
__file__)` at the bottom.  The rendering side multiplies out into
per-cell renders driven by the SPEC's footprint.

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
plus a sibling `BLEND_WINTER` + `MATERIALS_WINTER` pair in the
bake script.  The upstream `-snow.blend` convention is JP's
own: each blend-sourced building that has winter art ships an
adjacent `<name>-snow.blend` with the same geometry but
reshuffled materials (Roof texture dropped for procedural snow
noise, brick desaturated, ground textured for snow, etc.); the
upstream render script has no season logic, just feeds the snow
blend through the same pipeline.  We mirror this:
`bake_building` runs two `blender -b -P render.py` subprocesses
when `seasons >= 2`, one per blend, and `_stitch_seasons`
vertically concatenates the per-season PNGs (summer on top).
Seed `MATERIALS_WINTER` via `python3 -m pak.extract_materials
<winter-blend>`.

A landmine specific to the `-snow.blend` siblings: many ship
with their geometry collection saved at `hide_render=True` (JP
toggles visibility interactively before rendering, and the saved
state carries the off-toggle).  `pak.render._bake_world_into_meshes`
falls back to lifting `collection.hide_render` on every collection
holding a non-hidden mesh when the per-collection filter yields
zero meshes — Blender's renderer respects the collection flag
regardless of our vertex transforms.

**Per-cell rendering.**  `viewpoints.building_hex_viewpoint
(layouts, dims_x, dims_y)` returns a Viewpoint with one Facing
per cell.  The Facing's `model_rot_z_deg = (360°/layouts) * l`
rotates the model into the layout's orientation — `layouts=8`
spaces facings at 45° (the same set `HEX_VIEWPOINT` uses for
vehicles), `layouts=4` lands face-on at each cardinal.  Its
`model_translation` is `-hex_tile_world_offset(qx=x, ry=y)`,
the negative of the cell's world centre computed from the hex
tile lattice (`HEX_KOORD_Q_WORLD` heads SE, `HEX_KOORD_R_WORLD`
heads S; pinned to `display/hex_proj.h::hex_screen_dx/dy` at
`ortho_scale = 2R`, `W = 128`).  The standard hex camera looking
+Y at world origin then renders just that cell's content per
pass.  No image-space slicing — each cell is its own 128 × 128
EEVEE render (vs vehicles' Cycles; see "Lighting calibration"
below).

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
* **Multi-tile centring.**  `fit_kind="hex"` centres on the
  model's XY bounding box, which is right for single-tile
  assets.  For a multi-tile blend whose authored frame puts tile
  (0,0) at world origin (or the footprint centre at origin, or
  somewhere else entirely — unknown upstream convention), the
  per-cell translations may need to compose with a per-asset
  offset.  Surfaces as "every cell renders the same part of the
  model".  Fix: a `fit_kind="hex_building"` variant in
  `render.py::_compute_fit` that anchors on a known footprint
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

A fourth landmine the calibration diff exposed:

* **Per-blend ortho_scale must reach the diff camera.**  Vehicles
  are all authored at ortho_scale=24 (the contributing-graphics
  convention) so `SQUARE_VIEWPOINT`'s hardcoded 24 happens to
  match.  Buildings author at 12 (twice the per-cell zoom).  With
  a hardcoded camera ortho_scale, the diff renders the building
  at half-size in the cell (IoU drops to 0.26).
  `Viewpoint.ortho_scale=None` means "use the blend's authored
  value"; `_install_camera_and_sun` falls back to `blend_ortho`
  (returned by `_strip_scene`).  `building_square_viewpoint` uses
  this so the diff renders at the upstream blend's per-pixel
  scale.  `building_hex_viewpoint` and the hex production bake
  intentionally don't -- they target the pak's intra-tile coord
  system, with `_compute_fit("hex")` doing the
  `INTRA_TILE_PER_BLEND_UNIT = 2R / blend_ortho` scale conversion.

The dat side (Building dataclass, `emit_building`, `port_building`,
`bake_building`) is in tree and tested round-trip against
upstream `attractions/nelson-column.dat` (2×2×1, `type=mon`).
The render side ships end-to-end via `citybuildings/
res_1600_kg_01.py` (1×1×8, `type=res`); the four landmines above
are exercised on a single-tile near-symmetric residential, so
multi-tile centring and layout-rotation-sign disambiguation still
wait on a multi-tile asymmetric port.

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
Sun energy enters via `_strip_scene`: each Britain blend ships
its own SUN lamp at the BI-authored `energy=0.028`, which
`render.py::BlendAuthored` captures before stripping the lamp.
Building viewpoints declare `sun_energy=None,
sun_energy_scale=_BI_TO_EEVEE_SUN_SCALE` (= 2.0/0.028 ≈ 71.4)
so `_install_camera_and_sun` resolves to `authored × scale ≈ 2.0`
under EEVEE.  Vehicles/ways pin `sun_energy=0.028` directly under
Cycles where the upstream PNG is the calibration target.

The remaining EEVEE-substitution magic numbers — sun direction
(elev=30°, az=-90° defaults) and world ambient (0.30 grey in
`pak.render`) — are calibrated to `res_1600_kg_01` only; see
TODO → "Building lighting is calibrated to one asset" for the
trigger to revisit.  Authored `world.color` (Britain blends ship
(0.906, 1.0, 1.0)) is *not* extracted: that value was BI's
background sky, not its ambient term, and modern EEVEE's
`world.color` IS the ambient term — so the authored value is the
wrong thing to plug in here.

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
  (`python3 -m pak.extract_materials <blend>`).  Collapses each
  material to its first IMAGE slot or fallback procedural slot
  and emits paste-ready Python source for the bake script's
  `MATERIALS = {...}` dict.
* **`pak/materials.py`** defines the `Material` dataclass --
  per-material `image / texco / size / ofs` or `noise=True`.
  `to_jsonable` / `from_jsonable` serialise across the subprocess
  command line.
* Each `citybuildings/<asset>.py` carries `MATERIALS = {...}`
  inline next to `SPEC`, passed through
  `bake_building_main(..., materials=MATERIALS)`.  Once seeded,
  the dict is the authoritative representation -- hand-edits are
  welcome (JP's authoring quirks like a Roof material pointing
  at the BrownTile-duplicate image rather than its sibling
  `Brick` live as in-place comments).
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
    diffuse colour.  BI's CLOUDS substitute.
  * Materials omitted from MATERIALS render flat-diffuse via
    Blender's `use_nodes=False` auto-conversion.

External texture filepaths in the .blend (`//../../../textures/...`)
are remapped via `_reload_external_textures` to the blends-repo
cache before binding.  Image data blocks whose filepath 404s
(e.g. Pavement's typo'd `concrete-paving-smalll.jpg` path) warn
and fall back to flat diffuse rather than failing the bake -- see
TODO → "Pavement texture file missing from upstream blends repo".

## Way-bake architecture

Ways (rails, roads, trams) port via a different shape than vehicles
or grounds: an upstream rail-shape blend like `ways/ns-cssr.blend`
is treated as the **elementary geometric atom**, and the bake
**composes** that atom into 63 hex ribi cells (+ slope variants)
by cloning, clipping, and transforming it onto each ribi's path.
No parametric cross-section painter; no separate "draw the ballast,
draw the ties, draw the rails" code.  The blend already has the
cross-section authored as separable Rail / Sleeper / Ground meshes
— the composition step just lays them along the right path.

Two layers, kept honestly split:

- **Path geometry** (`pak/way.py`, `pak/way_topology.py`).  Pure
  data — ribi vocabulary (the `ribi_key` engine contract), slope
  slot labels, and the per-ribi `StraightPath` list `for_edges_paths`
  emits (stub for 1 edge, chord / V-bend for 2 edges, junction =
  pairwise paths for 3+ edges).  No painting, no rasterizer, no
  Blender.  Tested in `tests/test_way.py`.

- **Bake driver** (`pak/bake_way.py`, runs only inside
  `blender -b -P`).  Opens the blend, strips authored cameras /
  lights and the `Sphere` sun-direction visualizer (matching the
  vehicle harness in `pak/render.py`), bakes `matrix_world` into
  mesh vertex data, then walks `HEX_ENTRIES` (popcount-then-ribi).
  For each ribi: clones the atom meshes per
  `pak.way_topology.for_edges_paths(edges)` segment, rotates +
  translates the clone onto the segment's chord, bisects against
  the segment's cap planes (`pak.way_topology.cap_plane`) + the
  six hex-outline planes (`pak.way.hex_clip_planes()`), applies
  the hex projection shear, and renders one PNG.  Per-cell PNGs
  go to a temp dir (or `--cell-dir` for debugging); the stitched
  atlas (8 cols, popcount-major) lands at `<out>/<name>.png`.

  Bisect convention: every cap- and outline-plane normal points
  **inward** (toward the chord midpoint, or toward the hex centre
  for outline planes), and `bmesh.ops.bisect_plane` runs with
  `clear_inner=True` so the kept half is the +normal side.  Two
  places this contract lives — the plane builders in `pak.way` /
  `pak.way_topology`, and the bisect call in `_bisect_mesh` —
  must agree, or every clone gets deleted instead of clipped.
  `tests/test_way.py` pins the +normal-side-keep convention so a
  future refactor that inverts one side trips the test instead of
  silently emptying the atlas.

  Naming pitfall worth pinning: in `ns-cssr.blend` the mesh named
  `Plane` is **not** an upstream ruler — it's the 2048-poly ballast
  pile (material `Ballast`, z up to 0.28).  Stripping by name
  generically (e.g. "anything called Plane") loses the ballast
  silhouette.  Default-strip is `{Sphere}` only; per-blend extras
  go via `--strip`.

  Atom scale and composition:

  * **Hex** scales the blend by `INTRA_TILE_PER_BLEND_UNIT` (=
    `2R/UPSTREAM_ORTHO_SCALE` = `1/12` at current constants, the
    same blend → intra-tile conversion `fit_kind="hex"` uses for
    vehicles) — so a hex rail's gauge, sleeper width and
    ballast extent land at the right **intra-tile** size.  Two
    coord systems not to conflate:

      * **Tile coords** are integers (adjacent tile is `(x+1, y)`
        in either projection — no projection difference here).
      * **Intra-tile coords** are continuous within one tile.
        Our pakset fixes tile edge = 1 intra-tile unit in both
        projections (`HEX_TILE_RADIUS` = the square tile side),
        so a way of width `WAY_WIDTH = 0.4` crosses every tile
        edge at the same fractional width in both projections,
        and a way spanning a tile boundary has the same
        complete-way-width at the crossing.

    Blend coords are upstream's authoring frame, a third ruler;
    `INTRA_TILE_PER_BLEND_UNIT` is the only conversion between
    them.  Pixel sizes between projections differ (hex at
    `ortho_scale = 2R` renders 1 intra-tile unit at 64 px;
    upstream-square at `ortho_scale = 24` renders 1 blend unit
    at 5.33 px) and that's by design — what's preserved is
    intra-tile size, not pixel size.

  * **Multi-atom-per-chord tiling** applies to **both
    projections** — the blend's 8.78-unit strand is shorter than
    every load-bearing chord in either system: hex at `1/12`
    scale gives a `0.73`-unit atom against a `√3 ≈ 1.73` chord,
    and square at native gives an 8.78-unit atom against a
    24-unit NS chord (= `2 * SQUARE_TILE_HALF` in blend coords).
    Upstream's NS cell visibly has 9+ sleepers — more than one
    9-sleeper atom holds — so upstream itself tiles atoms along
    the chord; our pipeline mirrors that.
    `pak.way_topology.atom_offsets_along_path` returns
    `ceil(chord_len / atom_y_extent)` chord-offset slots centred
    on the chord midpoint; the bake driver places one atom per
    slot, and the cap bisect trims the outer pair's overrun.
    The blend's symmetric sleeper layout (9 ties centred on Y=0)
    makes consecutive atoms' end-sleepers meet flush within
    sub-millimetre intra-tile units, so the rail reads continuous
    across the tiled atoms without explicit seam handling.

  * **Square** keeps native blend scale (`atom_scale=None`) and
    skips the blend → intra-tile conversion entirely.
    `SQUARE_PROJECTION` exists only as the upstream-coord
    **calibration view** for the open square diff harness
    (mirror of `SQUARE_VIEWPOINT` with `fit_kind="none"`), so its
    pixels are directly comparable to pak128.Britain's published
    cells.  Its `SQUARE_TILE_HALF = UPSTREAM_ORTHO_SCALE / 2` is
    in blend coords, **not** our intra-tile system — comparing it
    against `HEX_TILE_RADIUS = 1` would be a category error.

**Per-way material recolour** (per-way `MATERIALS` dicts).
Upstream ships ~20 rail-grade dats (cast_iron through cssri) that
render from one underlying geometry — within-family silhouette IoU
is 1.000, cross-family ≥ 0.96.  The visual differentiation is
material recolour: four blend slots (`Rail`, `RailTop`, `Wood`,
`Ballast`) shift hue and value per variant.  We mirror that:
each `ways/<way>.py` declares its own `MATERIALS = {…}` inline
(colocated with the SPEC, no central catalog), passes it through
`bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)`,
`pak/bake.py::bake_way` serialises to JSON on the `--materials`
arg, and `pak/bake_way.py` parses it back with `json.loads` and
applies via `mat.diffuse_color` before render.  tarmac and tgv use
their own blends with their own slot sets (`Dirt` / `MainColour1`
for tarmac, the rail family plus `Tarmac` for tgv); the schema
generalises naturally.  Old-style (`use_nodes=False`) materials
render via the diffuse colour directly under both Cycles auto-
conversion and Workbench `MATERIAL` color mode; node-graph
materials would need a different override path.

Under Workbench `light = "FLAT"`, rendered pixel == material's
`diffuse_color` directly -- no shading attenuation.  `MATERIALS`
values are K-means centroids over the upstream PNG's lit pixels
(magic pink keyed out at `(231, 255, 255)`), luminance-ranked
into Ballast / Wood / Rail / RailTop (k=4 for rail-family, k=2
for tarmac).  The sampler isn't committed -- it's a one-off
inline numpy + Pillow script, ~20 lines.  Adding a new variant
is re-implement-as-needed: fetch upstream's PNG via
`pak.fetch_pak`, mask `(231, 255, 255)`, k-means cluster, paste
into a new `ways/<name>.py`.  Every committed-PNG way is
calibrated this way; the unbaked rail-grade scripts still hold
Cycles-era MATERIALS that will need re-sampling when they're
actually baked.

The Transparent ground plane in `ns-cssr.blend` (Plane.005,
material `Transparent`) is dropped via `_STRIP_MATERIALS` in the
bake driver — diffuse 0.8 grey with no texture wired up, it
otherwise contaminates ~50 % of the lit pixels with fake bright
grey that upstream's atlases don't show.

Note on what's intentionally **not** here:

- No numpy rasterizer.  An earlier session ported pak128's
  `tools/threed/render.py` (Model/SquareCamera/HexCamera) as a
  parametric-painting fallback, then deleted it after the pivot to
  blend-as-atom — leaving the rasterizer in tree without a caller
  would have rotted.  The pak128 sibling keeps it; we re-port if a
  numpy-only path ever becomes useful here.

- No `CrossSection` class.  The blend is the cross-section; no
  duplicate Python source-of-truth for "what a rail looks like in
  cross-section."

- No square-pak calibration loop for ways yet — but the
  *infrastructure* for one (a `--projection square` mode in
  `pak/bake_way.py`, switching tile geometry, ribi vocabulary,
  camera + sun, ortho_scale, extrinsic, atlas layout) **does** ship,
  via `pak/way_proj.py::Projection`.  The actual diff harness
  (`pak/diff_way.py`) is the open consumer; until it lands we
  validate hex by eye + by adjacency tests (do rails meet flush at
  shared edges?).  See TODO.md → "Way square-projection diff
  harness".

  Topology duplication is **deliberate, deferred**.  The square
  path-dispatch helpers (`_square_between_edges`, `_square_bend`,
  `_square_curve`, `_square_stub`, `square_for_edges_paths`) in
  `pak/way_proj.py` are line-for-line copies of their hex
  counterparts in `pak/way_topology.py`.  Consolidating them through
  a shared `tile`-geom parameter would be the natural next refactor,
  but doing it before the diff harness has bent the API would be
  premature — the right shape will fall out of what the diff harness
  actually needs to swap.  The shared invariants (`cap_plane`,
  `path_chord_*`, the +normal-keep bisect convention) live in
  `pak/way_topology.py` and are projection-agnostic;
  `tests/test_way.py::_ProjectionInvariants` is the mixin that runs
  the property-based checks against both projections' entries lists,
  so an asymmetry (a square ribi whose paths have outward-pointing
  cap normals, say) trips the test instead of silently miscomposing
  an atlas.

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
W whitespace, I import sorting, UP outdated typing); stylistic-only
checks are dropped (E501 line length, E702 intentional `a; b` pairs,
E741 `l` collides with the engine's `(l, y, x)` building-layout loop
convention).  Same philosophy as "Test value rules" below — catch
the bug, skip the noise.  Net real-bug catch on adoption was near-
zero; the value is prophylactic.

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
