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
and reports per-facing silhouette IoU and mean abs(RGB-delta).
Calibrated assets land at IoU ≥ 0.93 across all 8 facings (the
residual is colour, not geometry — livery material swap, see the
`sp_*` follow-up in `TODO.md`).  Worst IoU under 0.90 means real
drift: the blend's frame is what's wrong, not the hex bake; fix
the blend (or the alignment mode) before extending hex coverage.
This is the only step that touches upstream PNGs — see "Don't
bake the answer" above; comparison is regression check, not
steering signal.

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
- `.wav` — sound effects.  Fetched on demand from the upstream
  pak repo at runtime, parallel to blend fetching (see "Asset
  sourcing without cloning" below); the hex pak doesn't ship
  them in git.
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
  upstream repo, not per file-type — `pak.lock` covers both pakset
  PNGs (used by `diff_upstream.py`) and `.wav` sound effects (when
  runtime sound fetching lands).
- A `tools/<area>/fetch_*.py` script resolves `<path within
  upstream repo>` against that SHA, fetches the individual blob
  over HTTP, caches under a `.gitignore`d `.cache/` dir.
- Consumers (per-asset `bake.py`, the runtime sound loader, the
  calibration diff) call the fetcher rather than reading files
  directly.

Present:  `fetch_blend.py` (blends repo) and `fetch_pak.py` (pak
repo) both implement the pattern.  A session touching one asset
downloads one blend, not the tree; upstream repo size is
irrelevant to the day-to-day.

If the upstream HTTP endpoint requires auth or routing, the
fetcher is the single place to handle it.  Keep auth concerns
out of per-asset `bake.py`s and out of the runtime loader.

## Per-asset directory layout

Mirroring `hextrans-pak128` (model-and-deliverable co-located,
one dir per atomic asset):

```
vehicles/trains/br_class_350/
  bake.py                  # fetch_blend + render + atlas
  br_class_350.png         # committed baked atlas
  br_class_350.dat         # committed hex-flavour dat
  refs/                    # (optional) square ref for cross-check
  notes.md                 # (optional) anything not fit for commit msg
```

The `.blend` is not in this repo.  `bake.py` references it by
its path inside the upstream blends repo (e.g.
`Trains/Railcars/br-350-lnr.blend`) plus the global `blends.lock`
SHA.

Atlas PNGs are committed for the reviewer-friendly "see the
change in the PR" property; their cumulative weight gets measured
after the first batch lands (`TODO.md` → "Atlas commit vs.
CI-artefact-only").  Only the final atlas + dat are committed.  Debug renders, per-facing PNGs,
diff visualisations go to a `.gitignore`d `out/` and regenerate
on demand.

### Atlas layout

Each per-asset PNG is a single row of N facing renders, sliced by
makeobj into 128×128 sprites (cell width = pak tile width).  Cell
`(col, row)` is addressed from the .dat as `<file>.<col>.<row>`.

Column order is the `facings` list in `HEX_VIEWPOINT`
(`tools/threed/viewpoints.py`): `S, SW, W, NW, N, NE, E, SE` for the
default 8-view bake.  Per-asset .dat keys (`EmptyImage[S]=…0.0`,
`EmptyImage[SW]=…1.0`, …) must match this order or the engine
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
  `fetch_pak.py`, and reports per-facing silhouette IoU + mean
  abs(RGB-delta) against the upstream sprite.  Returns non-zero if
  any facing is below 0.90 IoU — see "Calibration validation loop"
  above.

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

## CI rebake check

Match `hextrans-pak128`'s convention: every push reruns the bake
for changed assets (detected by changes to `bake.py` or the
relevant `blends.lock` entry), asserts the committed PNG is
byte-identical.  Stops silent drift between source `.blend` and
committed atlas.

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
