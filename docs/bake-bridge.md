# Bridge-bake architecture

Companion to `CLAUDE.md` (engine facts, calibration contract,
bake-unit conventions).

Bridges (`Obj=bridge`) port via a `Bridge` SPEC with inline
`blend=` per piece (image / start / ramp / pillar) and a
`bake_main(SPEC, __file__)` call.  Per-piece renders go
through `bridge_hex_viewpoint(piece)`; `pak.bake._stitch_bridge_atlas`
composes them into a multi-row atlas next to the dat.

**Atlas layout.**  Four rows, one per piece kind, in the order
`HEX_BRIDGE_PIECE_ORDER = ("image", "start", "ramp", "pillar")`.
`pak.dat.HEX_BRIDGE_PIECE_LABELS` is the single source of truth
for per-row labels — drift between bake, emit, and viewpoint
would render the wrong sprite per axis/direction with no
runtime error.

* **image** (row 0) — axial span connecting two opposite hex
  edges, 3 cells: `n_s`, `ne_sw`, `nw_se`.  Cols 3-5 transparent.
* **start** (row 1) — abutment at one of the 6 hex edges, 6 cells:
  `n, ne, se, s, sw, nw` (cw from N, matching
  `pak.way.SLOPE_HEX_ENTRIES` order).
* **ramp** (row 2) — same 6 labels as start.
* **pillar** (row 3) — same 3 axial labels as image.

`emit_bridge` keys dat refs as `BackImage[<label>]=./<basename>.0.<col>`
etc., row + col straight from the layout above.

**Hex engine schema is unverified.**  The dat key tokens
(`BackImage[n_s]`, `BackStart[ne]`, …) and the 3-axis / 6-dir
shape are translated from upstream's square `[NS]`/`[EW]` and
`[N]`/`[S]`/`[E]`/`[W]` conventions.  Hex `bridge_writer.cc` is
the authoritative source — `hextrans-pak128/infrastructure/
rail_bridges/rail_060_bridge/` is the worked-example pakset to
calibrate against once the Britain pak first builds a bridge
`.pak` artifact.

**Variants and seasons.**  Upstream emits four families per
piece (variant 1 / variant 2 × season 0 / season 1; variant
interleaves under `pillar_asymmetric`, season switches at snow
climates).  Production bake currently ships variant 1 + season 0
only — variant 2 keys (`BackImage2` etc.) and `[1]` snow cells
are documented as deferred in TODO.md.

**Depth-clipped Back/Front not yet wired.**  Today the Front
layer points at the same atlas cell as Back, so the bridge
silhouette is opaque and a vehicle traversing the deck vanishes
behind the bridge image.  The fix is the tunnel approach
(per-facing camera `clip_start`/`clip_end` at the tile-centre Y
plane, atlas doubled vertically).  See TODO.md.
