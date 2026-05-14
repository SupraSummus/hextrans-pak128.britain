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

**makeobj smoke-compile.**  No makeobj binary in this tree, so
we've never actually compiled a port to `.pak`.  `Vehicle`'s
field set was derived from `vehicle_writer.cc` by reading source,
not by feeding the emitted dat through makeobj and watching for
errors.  Concrete next move: clone hextrans, build makeobj, run
it against `trains/_4wheel_1850s_first.dat` + the atlas, confirm
it round-trips into a single-vehicle pak.  Will surface any
schema gaps the porter missed — e.g. required-vs-optional
classification mistakes, the unmodelled freight-image subsystem
(see below) tripping a freight wagon, version-mismatch fatals.

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

**Ground tiles + one rail way.**  Port
`hextrans-pak128/landscape/grounds/` and `…/rail_060_*` so the
carriage has somewhere to sit.  At that point the spine is
visible in-engine.

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

**Wire up runtime `.wav` fetching.**  Sounds were stripped from
history; the engine still expects to load them.  `pak.lock` and
`tools/threed/fetch_pak.py` already pin and fetch from the
upstream pak repo (currently for the calibration diff).  Concrete
next move when audio first matters in-engine: decide whether the
engine's sound loader calls `fetch_pak` directly or a pre-launch
step warms `.cache/pak/<sha>/sound/`.  Either way the SHA bump
lives in `pak.lock` so PNG and wav consumers stay in lock-step.
Soft trigger.

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
