# TODO.md

Open work for the hex port of the Britain pakset.  Rules: see
`CLAUDE.md` → "TODO.md rules".

## Starting spine

A small spine that gets the engine to draw something Britain-ish
under hex.  Order is rough — later items have soft triggers on
earlier ones.

**Hex-camera `blend_render.py`.**  The square-dimetric spike at
`tools/threed/blend_render.py` proves the `blender -b -P` +
`fetch_blend.py` pipeline against the upstream `-65` script.  The
hex camera is a separate harness whose math mirrors
`hextrans-pak128/tools/threed/render.py::HexCamera` (anchored to
`HexGeom`, no yaw, orthographic, z-lift via `PIXELS_PER_UNIT`).
Concrete next move: write `tools/threed/hex_render.py` driven off
the same `fetch_blend.py`, factoring shared scene-prep out of the
square spike at the same time.  Trigger: first asset bake.

**Bake one asset end-to-end.**  Pick a single passenger carriage
(no depth-clip slicing, no multi-tile geometry).  Lands the
per-asset template — `bake.py` shape, dat schema delta, what
`out/` debug looks like — plus shakes out every silent-failure
landmine from `CLAUDE.md` → "Engine facts" (scale, sun, anchor y).
Trigger: `hex_render.py` exists.

**Ground tiles + one rail way.**  Once the carriage bakes,
porting `hextrans-pak128/landscape/grounds/` and `…/rail_060_*`
gives the carriage somewhere to sit.  At that point the spine is
visible in-engine.

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
