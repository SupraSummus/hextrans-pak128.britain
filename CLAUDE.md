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
`tools/threed/hex_synth.py`.  Each baker is a single
`grounds/<asset>.py` that emits sibling `<asset>.{png,dat}`; the
filename matches the engine `Name=` field (`light_texture`,
`shore_trans`, …) so grepping from engine source lands on the
right baker.  Ported from `hextrans-pak128/landscape/grounds/`; see
TODO.md for the gaps (texture-climate, way_ground, fence).

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

The vanilla (Simutrans-Standard) pak128.Britain lives on
SourceForge SVN at
`https://sourceforge.net/p/simutrans/code/HEAD/tree/pak128.Britain/`.
This is the pre-fork ancestor of the extended pak we carry, and
was explored as a potential second source.  It is **not used**:
its `.dat` files are vanilla-schema (no `axle_load=`, `comfort=`,
`livery_*=`, etc.) and could serve as a diff reference for the
extended→vanilla key-drop pass, but the engine's
`descriptor/writer/*_writer.cc` is the authoritative key list and
the diff isn't worth wiring up an SVN fetcher for.  Its `sound/`
ships only ~13 generic UI/climate wavs; the ~191 per-vehicle
wavs our `.dat`s reference are extended-fork curation and only
exist in the github upstream above.  No `.blend` files — those
have always lived in `Pak128.Britain-blends`.  Recorded here so
the next agent doesn't redo the exploration.

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
  `hextrans-pak128/tools/threed/hex_synth.py::HexGeom` and
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

**Camera scale.**  Upstream's
`render_SimutransRender_pak128Britain-65.py` uses a fixed ortho
camera with `ortho_scale = 24` rendering to 128 × 128 px.  That
ratio (the hex `fit_kind` in `tools/threed/render.py` builds
`2R / 24`) is the single pakset-wide scale
constant — it corresponds to the artist-side 15 m ruler (46 m for
aircraft, log-scaled for large ships) used to calibrate geometry in
Blender.  Width and height for land vehicles are authored at 1.25×
the length scale by convention; bakers do not undo this.

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
buildings).  Only `SQUARE_VIEWPOINT` in `tools/threed/viewpoints.py`
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

**Calibration validation loop.**  `tools/threed/diff_upstream.py`
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

`tools/threed/check.py` is the driver: it imports a bake script,
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
  `copy` Makefile target via `tools/threed/fetch_wavs.py` (scans
  ported `.dat`s for `sound=*.wav` references, pulls each through
  `fetch_pak`, stages into `$(PAKDIR)/sound/`).  See "Asset sourcing
  without cloning" below; the hex pak doesn't ship them in git.
- `.tab~`/`.dat~`/`.bak` — editor backups.

Kept in git: `.dat` (gameplay catalog), `.tab` (config),
`.nut` (scripts), authored text.

Before committing any new bulk-content type, ask: can the
runtime fetch it from a pinned upstream SHA over HTTP instead?
If yes, don't commit it.

To re-run the size analysis (e.g. before a future strip pass),
against an *unshallowed* clone:

```
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' \
  | awk '$1=="blob" { n=split($3,a,"."); ext=tolower(a[n]); s[ext]+=$2 }
         END { for (k in s) printf "%-10s %12d\n", k, s[k] }' \
  | sort -k2 -rn
```

The rewrite was destructive: clone hashes changed, outstanding
branches needed rebasing.  Done.  Further filter-repo passes are
possible but expect the same coordination cost.

If the proxied HTTP push hits a 413 (Payload Too Large), split
the push into chunks by walking commit history
(`git push origin <intermediate-sha>:refs/heads/<branch>` for a
handful of mid-history commits, then push the tip).

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
  the pak by `tools/threed/fetch_wavs.py` in the Makefile `copy`
  step), and the boot-screen / demo deliverables (`symbol.BigLogo.pak`,
  `demo.sve`).
- A `tools/<area>/fetch_*.py` script resolves `<path within
  upstream repo>` against that SHA, fetches the individual blob
  over HTTP, caches under a `.gitignore`d `.cache/` dir.
- Consumers (per-asset `bake.py`, the runtime sound loader, the
  calibration diff) call the fetcher rather than reading files
  directly.

Present:  `fetch_blend.py` (blends repo) and `fetch_pak.py` (pak
repo) both implement the pattern; `fetch_wavs.py` is a thin
batch helper over `fetch_pak` that scans ported dats for
`sound=*.wav` references and pulls each one.  A session touching
one asset downloads one blend, not the tree; upstream repo size is
irrelevant to the day-to-day.

If the upstream HTTP endpoint requires auth or routing, the
fetcher is the single place to handle it.  Keep auth concerns
out of per-asset `bake.py`s and out of the runtime loader.

## Bake units and per-asset layout

A "bake unit" is one bake script.  It owns a `SPEC` (or `SPECS`)
of pure gameplay data and a list of blends to render; running it
emits the corresponding `.dat` + `.png` outputs as siblings.  The
script is the **single source of truth** — no upstream `.dat` is
read at bake time.

The bake-unit shape (single-vehicle demonstrated;
multi-vehicle pattern designed but not yet exercised):

```
trains/
  __init__.py                    # makes the dir an importable package
  _4wheel_1850s_first.py         # bake unit; 1 SPEC -> 1 dat + 1 png
  _4wheel_1850s_first.dat        # generated
  _4wheel_1850s_first.png        # generated
  _gwr_king.py                   # (illustrative) 2 SPECs (loco + tender)
  _gwr_king.dat                  # generated
  _gwr_king.png
  _gwr_king_tender.dat
  _gwr_king_tender.png
  4wheel-stanhope.dat            # unported upstream (seeder input)
  …
```

Today only `_4wheel_1850s_first` is ported.  The multi-vehicle
pattern (one script emitting multiple dat+png pairs) is
intentionally supported by the parser and emitter but not yet
demonstrated end-to-end; the first multi-object port will validate
how blends map to objects in real upstream blend files.

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
calls `bake_main` from `tools/threed/bake.py`.  The full
single-vehicle bake script:

```python
from tools.threed.bake import bake_main
from tools.threed.dat import Vehicle

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
emit-dat).  Multi-object bake units skip the convenience and
call `bake_vehicle` directly per output, with distinct `basename`
(and typically distinct `blend`) per call.

`Vehicle` fields cover both hex-engine (keys
`descriptor/writer/vehicle_writer.cc` reads) and
Simutrans-Extended schema (`bidirectional`, `comfort`, `axles`,
`tractive_effort`, `liverytype`, …).  `emit_vehicle` writes every
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
the engine's default.  Multi-object bake scripts hold a list of
`Vehicle`s and call `emit_vehicle` once per output.

**Importable bake scripts.**  Asset names that start with a
digit (`4wheel_…`) aren't valid Python identifiers — a leading
`_` keeps the script importable
(`from trains import _4wheel_1850s_first`); generated artefacts
share the prefix so the triple moves and greps together.
Letter-leading names (`br_cl15`, `blackpool_brush`) go plain —
no underscore.  `tools/__init__.py`, `tools/threed/__init__.py`,
and `trains/__init__.py` (each empty) make the repo a proper
package tree so bake scripts can `from tools.threed.dat import …`
without a `sys.path` hack.  Run as a module from the repo root:

    python3 -m trains._4wheel_1850s_first

Catalog-wide tooling imports the bake scripts as modules and
reads `SPEC` as a Python value without baking — see
`tools/threed/reemit_dats.py` for the worked example (used by
the `reemit-dats` CI job; see "CI" below).  `Name=` inside the
dat is its own namespace — the pak's internal identity, hyphens
kept upstream-compatible, what makeobj keys on (verified in
`root_writer.cc`).

**Seeding a new asset.**  When porting fresh from upstream:

```python
from tools.threed.dat import parse, port_vehicle, seed_python
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

### Atlas layout

Each per-asset PNG is a single row of N facing renders, sliced by
makeobj into 128×128 sprites (cell width = pak tile width).
makeobj's image-ref parser (`descriptor/writer/image_writer.cc`)
reads `<file>.X.Y` as **row=X, col=Y**, so a single-row atlas
addresses its cells as `.0.<col>`.  Getting the order wrong gives
`invalid image number` when col exceeds the atlas width in cells,
or silently transposed rendering when both indices fit.

Column order is the `facings` list in `HEX_VIEWPOINT`
(`tools/threed/viewpoints.py`): `S, SW, W, NW, N, NE, E, SE` for the
default 8-view bake.  Per-asset .dat keys (`EmptyImage[S]=…0.0`,
`EmptyImage[SW]=…0.1`, …) must match this order or the engine
renders the wrong sprite per facing — there is no run-time
consistency check.

Single-row is the default.  `render.py --cols-per-row N` exists for
atlases that grow tall enough to be awkward (way ribi tables,
multi-state machinery); not relevant for 8-facing vehicles.

## Bake tooling

Lives at `tools/threed/` in this repo, not in the blends repo
(blends are upstream-owned and stay reusable; our hex-rendering
opinions don't belong there).

Present:

- `tools/threed/fetch_blend.py` — HTTP fetch + `.cache/` resolver
  against `jamespetts/Pak128.Britain-blends`, SHA pinned via
  `blends.lock`.
- `tools/threed/fetch_pak.py` — same pattern against
  `jamespetts/simutrans-pak128.britain`, SHA pinned via `pak.lock`.
  Used by `diff_upstream.py` today and by future runtime `.wav`
  fetching (see `TODO.md`).
- `tools/threed/render.py` — `blender -b -P` harness that takes a
  `Viewpoint` and renders one atlas (plus optional per-facing PNGs).
  Strips the blend's Camera / Sphere / Lamp objects on entry and
  installs its own from the Viewpoint — the .blend is treated as
  pure model data.  Same code path serves the upstream square
  reference and this project's hex projection; the only difference
  is which `Viewpoint` gets passed in.  Applies the upstream blend
  calibration contract (see above) and emits a single-row atlas PNG.
- `tools/threed/viewpoints.py` — `SQUARE_VIEWPOINT` (reproduces
  the upstream `render_SimutransRender_pak128Britain-65.py`
  "vehicles" alignment verbatim) and `HEX_VIEWPOINT` (camera looking
  +Y at origin, ortho_scale=2R, hex shear baked into mesh via
  `extrinsic`, model rotated per facing).  Same facing labels in
  both so .dat keys port without relabelling.
- `tools/threed/diff_upstream.py` — drives `render.py --viewpoint
  square --keep-per-facing`, fetches the matching upstream PNG via
  `fetch_pak.py`, and reports the contour and colour metrics from
  "Calibration validation loop" above (silhouette IoU + XOR pixel
  count, and intersection-restricted mean abs(RGB-delta)).  Returns
  non-zero if any facing is below 0.90 IoU.
- `tools/threed/check.py` — convenience driver around
  `diff_upstream.py`.  Takes a bake-script path (or `--all`),
  imports it, reads `BLEND` and `UPSTREAM_STEM` from the module,
  runs the diff, and prints a per-asset worst-IoU + sum-XOR-pixel
  summary.  See "Calibration validation loop" above.
- `tools/threed/square_synth.py` — `SquareGeom`, a sibling to
  `HexGeom` implementing pak128.Britain's square-dimetric tile
  layout (4 corners, base-3 slope encoding, 128×128 cells with the
  flat lozenge spanning `y = 64..127`).  Same `Geom` interface as
  `HexGeom` — `corner_count`, `corner_world_xy`, `corner_projected_xy`,
  `all_chords`, `corner_labels`, `full_path`, plus
  `decode_corner_heights` / `iter_valid_slopes` / `slope_is_valid`
  — so the generic partition / region / fill / outline helpers in
  `hex_synth.py` work against either projection without isinstance
  branches.  Exists for `diff_grounds.py`'s test harness (see
  below); not on the hex production path.
- `tools/threed/diff_grounds.py` — square-projection diff harness
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
- `tools/threed/dat.py` — Simutrans `.dat` parse / port / emit.
  Exposes `Vehicle` (typed dataclass covering both hex-engine
  and Extended schema; list fields may carry
  `metadata["dat_key"]` to remap field-name → dat-key, e.g.
  `payload_by_class` → `payload[N]`), `parse(path)` (splits
  multi-object dats into `list[list[(k, v)]]`), `port_vehicle`
  (one-time seeder: upstream object entries → fully-populated
  `Vehicle`), `seed_python(vehicle)` (paste-ready non-default-only
  source repr for a new bake script), and
  `emit_vehicle(vehicle, out_dir, basename)` (writes the dat
  with every set field plus hex-atlas image refs).  The freight-
  image subsystem (`freightimage[<dir>]`,
  `freightimage[N][<dir>]`, `freightimagetype[N]`) is the one
  area `Vehicle` doesn't model yet — see `TODO.md`.
- `tools/threed/bake.py` — per-asset bake driver.
  `bake_vehicle(spec, blend=..., basename=..., out_dir=...)`
  fetches the blend, runs the hex renderer, writes the atlas
  PNG, and emits the dat.  Bake scripts shrink to imports +
  SPEC + a single `bake_vehicle(...)` call.
- `tools/threed/bake_units.py` — `discover()` returns every
  per-asset bake script (`.py` with `.dat` + `.png` siblings outside
  `tools/`, `tests/`, `grounds/`, `simutranslator/`), and
  `import_script(path)` imports it by its repo-relative dotted
  name.  Shared by `reemit_dats`, `fetch_wavs`, and
  `tests/test_ported_dats` so the catalog has one definition of
  what counts as a ported asset.
- `tools/threed/reemit_dats.py` — catalog-wide driver that
  imports every `discover()`-ed bake script and calls
  `emit_vehicle` on its `SPEC`.  No Blender, no render.  Wired
  into CI as the `reemit-dats` lint job to catch SPEC ↔
  committed-`.dat` drift on every push.  Raises on a bake script
  without `SPEC: Vehicle` rather than silently skipping — the
  first multi-object bake unit will need to extend this (see
  `TODO.md` → "Multi-object reemit hook").
- `tools/threed/fetch_wavs.py` — catalog-wide driver that walks
  `bake_units.discover()`, reads each `SPEC.sound`, and pulls the
  named wav from the upstream pak via `fetch_pak`.  Invoked by
  the Makefile `copy` step to stage sounds into `$(PAKDIR)/sound/`
  on every build.
- `tests/test_dat.py` — `unittest`-based smoke tests for parse,
  emit, port, seed_python, and the schema-enforcement-at-
  construction property.  Run via
  `python3 -m unittest tests.test_dat` (or
  `python3 -m pytest tests/`).
- `tests/test_square_synth.py` — geometry assertions for
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

`blender` (4.0.2 on noble) provides the `blender -b -P` harness;
its bundled Python is the system `python3.12`, so `python3-numpy`
lands `numpy` where `render.py`'s `import numpy as np` will
find it.  `python3-pil` (Pillow) is only needed by
`diff_upstream.py` for the side-by-side grid composition, not by
the Blender harnesses themselves.  `libegl1` is the runtime
Blender's GL backend dlopens — without it Cycles aborts with
SIGABRT before the first render even though `--background` would
suggest no display needed.

No GPU required; Cycles falls back to CPU.  ~4 s per facing on
a small carriage.

## CI

Two workflows, matching `hextrans-pak128`'s split:

**Lint** (`.github/workflows/lint.yml`, push + PR).  `rebake-grounds`
re-runs every parametric ground baker via `make bake-grounds` and
asserts `git diff --exit-code -- grounds/` — byte-identical or the
job fails.  Stops silent drift between `grounds/<asset>.py` and the
committed PNG/dat siblings.  `reemit-dats` runs
`python3 -m tools.threed.reemit_dats` (imports every vehicle bake
script, re-runs `emit_vehicle` from its `SPEC` — no Blender, no
render) and asserts `git diff --exit-code -- '*.dat'`; catches dat
drift between a bake script's SPEC and its committed `.dat` sibling
on every push.  `tests` runs the `python3 -m unittest` suite under
`tests/` (needs `numpy` for the `hex_synth` import chain pulled in
by `test_square_synth`).

Vehicle *render* rebake is not wired — vehicles need Blender +
libegl1 + a blend fetch per asset (~minutes per asset of CPU Cycles
render), too heavy for every push.  Selective vehicle rebake
(gated on `bake.py` or `blends.lock` diff) is a future-work entry
in `TODO.md`.

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
the `pak.lock`-pinned upstream pak via `tools/threed/fetch_pak.py`
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
