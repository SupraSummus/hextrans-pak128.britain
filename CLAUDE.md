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

The two **silent-failure landmines** to pin for the blend
pipeline:

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

The intended pattern for each, once implemented (neither
fetcher nor lock file exists yet — see `TODO.md`):

- A `*.lock` file at the repo root holds one upstream commit SHA
  (`blends.lock`, `wavs.lock`).
- A `tools/<area>/fetch_*.py` script resolves `<path within
  upstream repo>` against that SHA, fetches the individual blob
  over HTTP, caches under a `.gitignore`d `.cache/` dir.
- Consumers (per-asset `bake.py`, the runtime sound loader)
  call the fetcher rather than reading files directly.

Net once landed: a session touching one asset downloads one
blend (or one wav), not the tree.  Upstream repo size becomes
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

## Bake tooling

Lives at `tools/threed/` in this repo, not in the blends repo
(blends are upstream-owned and stay reusable; our hex-rendering
opinions don't belong there).

Start by copying `hextrans-pak128/tools/threed/` and adding:

- `fetch_blend.py` — HTTP fetch + `.cache/` resolver.
- `blend_render.py` — `blender -b` harness whose camera math
  mirrors `hextrans-pak128/tools/threed/render.py::HexCamera`
  (anchored to `HexGeom`, no yaw, orthographic, z-lift via
  `PIXELS_PER_UNIT`).  Facing count read from the engine's
  current `get_dirs()` convention, not hard-coded.

The Britain blends already carry the `sp_*` material-name
convention for player-colour masks; port that pass over from the
upstream render script.

When the bake tooling stabilises it's a candidate for extraction
into a shared `simutrans-threed` Python package consumed by both
this pakset and `hextrans-pak128`.  Don't extract before the
second consumer has bent the API at least once.

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
