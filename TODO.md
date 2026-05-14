# TODO.md

Open work for the hex port of the Britain pakset.  Rules: see
`CLAUDE.md` → "TODO.md rules".

## Starting spine

A small spine that gets the engine to draw something Britain-ish
under hex.  Order is rough — later items have soft triggers on
earlier ones.

**`.dat` validation gap.**  `vehicles/trains/4wheel_1850s_first/`
ships a `.dat` whose vanilla-vs-extended key triage was guessed,
not looked up.  CLAUDE.md → "Engine facts — look up, don't fit"
is the rule we broke.  Authoritative key list is
`hextrans/src/simutrans/descriptor/writer/vehicle_writer.cc`; no
makeobj binary is in this tree to fail-fast on bad keys.
Concrete next move: clone the engine, read `vehicle_writer.cc`,
revise the dat, and ideally build makeobj to actually compile
the asset.  Trigger: any push toward second-asset bake.

**hex_render.py output validation.**  hex_render.py is
believed-correct on paper but never compared against an engine
reference render.  4wheel-1850s-first's atlas now visually
confirms shading and facing layout look right (W/E read as
narrow end-on carriage faces, geometrically correct), but
that's eyeball-verification, not a quantitative check against
the engine's own projection.  Concrete next move: pixel-compare
a hex_render output of a procedural reference cube against the
same cube through `hextrans-pak128/tools/threed/render.py::HexCamera`;
they should agree to within renderer noise.  Trigger: any
second-asset bake.

**Ground tiles + one rail way.**  Port
`hextrans-pak128/landscape/grounds/` and `…/rail_060_*` so the
carriage has somewhere to sit.  At that point the spine is
visible in-engine.

**Directory layout migration.**  This repo holds the upstream
flat layout (`trains/*.dat` referencing PNGs in sibling
subfolders) AND the per-asset layout introduced this session
(`vehicles/trains/4wheel_1850s_first/{bake.py, *.png, *.dat}`).
Rule under construction: ported assets live under the per-asset
layout; the flat `trains/` etc. are read-only reference until
their assets get ported.  Concrete next move: write the rule
into CLAUDE.md once the second per-asset bake confirms the
layout holds up.  Soft trigger.

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
history; the engine still expects to load them.  Concrete next
move when audio first matters in-engine: write `wavs.lock`
pinned to a known-good upstream `simutrans-pak128.britain` SHA
(the SHA whose `sound/` we want), write
`tools/sound/fetch_wav.py` mirroring `fetch_blend.py`, and
decide whether the engine's sound loader calls the fetcher
directly or a pre-launch step warms `.cache/`.  Soft trigger.

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
hex_render.py renders the native materials only; the mask render
is a second pass that swaps those materials for the engine's
mask palette and emits a parallel `_mask.png` set the dat
references via `EmptyImage[FRONT-...]` etc.  Concrete next move:
port the material-swap code from the upstream `-65` script into
a `--mask` mode on hex_render.py.  Trigger: first asset that
gameplay-actually-needs livery support (probably a BR-era loco).

**Per-asset fit overrides.**  hex_render.py's auto-fit is
heuristic — picks the longer of (span_x, span_y) as the
longitudinal axis, scales to 80% of tile diameter, grounds at
min z.  Wrong on assets where span_y > span_x but the artist
intended X-native (the heuristic flips them).  Also can't
handle multi-tile assets (the carriage IS one tile; a long loco
might want to overflow).  Concrete next move when the first
asset trips this: add `tools/threed/fit.toml` or a `bake.py`
kwarg, fall back to auto-fit when unspecified.  Soft trigger.
