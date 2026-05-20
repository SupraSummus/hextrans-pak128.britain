# Way-bake architecture

Companion to `CLAUDE.md` (engine facts, calibration contract,
bake-unit conventions).

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
    same blend → intra-tile conversion `_hex_fit()` uses for
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

**Per-way material recolour** (per-way `materials=` dicts).
Upstream ships ~20 rail-grade dats (cast_iron through cssri) that
render from one underlying geometry — within-family silhouette IoU
is 1.000, cross-family ≥ 0.96.  The visual differentiation is
material recolour: four blend slots (`Rail`, `RailTop`, `Wood`,
`Ballast`) shift hue and value per variant.  We mirror that:
each `ways/<way>.py` declares its own `materials={…}` inline on
the SPEC (no central catalog), `bake_way_main(SPEC, __file__)`
threads it through `pak/bake.py::bake_way`, which serialises to
JSON on the `--materials` arg, and `pak/bake_way.py` parses it
back with `json.loads` and applies via `mat.diffuse_color` before
render.  tarmac and tgv use their own blends with their own slot
sets (`Dirt` / `MainColour1` for tarmac, the rail family plus
`Tarmac` for tgv); the schema generalises naturally.  Old-style
(`use_nodes=False`) materials render via the diffuse colour
directly under both Cycles auto-conversion and Workbench
`MATERIAL` color mode; node-graph materials would need a different
override path.

Under Workbench `light = "FLAT"`, rendered pixel == material's
`diffuse_color` directly -- no shading attenuation.  `materials=`
values are K-means centroids over the upstream PNG's lit pixels
(magic pink keyed out at `(231, 255, 255)`), luminance-ranked
into Ballast / Wood / Rail / RailTop (k=4 for rail-family, k=2
for tarmac).  The sampler isn't committed -- it's a one-off
inline numpy + Pillow script, ~20 lines.  Adding a new variant
is re-implement-as-needed: fetch upstream's PNG via
`pak.fetch_pak`, mask `(231, 255, 255)`, k-means cluster, paste
into a new `ways/<name>.py`.  Every committed-PNG way is
calibrated this way; the unbaked rail-grade scripts still hold
Cycles-era materials that will need re-sampling when they're
actually baked.

The Transparent ground plane in `ns-cssr.blend` (Plane.005,
material `Transparent`) is dropped via `_STRIP_MATERIALS` in the
bake driver — diffuse 0.8 grey with no texture wired up, it
otherwise contaminates ~50 % of the lit pixels with fake bright
grey that upstream's atlases don't show.

No `CrossSection` class and no numpy rasterizer: the blend is the
cross-section, and the blend-as-atom pipeline subsumes the
parametric painter the pak128 sibling carries.

**Full-cell mode** (`Way.full_cell = True`) is the parallel path
for blends authored as 1-to-1 full cells rather than short atoms.
JH's `ways/<family>/{straight,DIAGONAL,3-way,4-way,pillar,end,
slope}.blend` families ship the entire elevated viaduct cell
(deck + arches + ballast + rails) as a single mesh group sized
to fill the cell -- the chord-composition pipeline would
replicate the asset for popcount>2 junctions (two crossing
decks for NSEW), so full-cell mode skips composition entirely
and aliases one render as every cell.  `full_cell_rotations`
maps ribi label to world-Z rotation in degrees so an EW-authored
blend can also cover NS via `{"NS": 90}`; the bake driver
groups cells by rotation and only re-renders when the rotation
changes.  Per-ribi blend dispatch (different blend per ribi
label) is the open follow-up; see TODO.md.

`Way.blend_source` ("jp" jamespetts, "jh" JamesHood) selects the
fetcher.  JH carries the elevated-viaduct families jamespetts
doesn't ship; `Way.inherit_camera = True` installs the blend's
authored camera (SW-looking-NE, ortho_scale=12) instead of
SQUARE_VIEWPOINT['S'].

`pak/diff_way.py` runs a per-ribi silhouette IoU + dRGB diff via
`--projection square --cell-dir`, parses upstream's
`image[<ribi>][0]=...row.col,...` refs to slice the upstream
atlas into per-ribi cells, and emits a `grid.png` (ours /
upstream / silhouette-XOR).  `pak/check.py` dispatches Way SPECs
through it.

Topology duplication between `way_topology.py` (hex) and
`way_proj.py` (square path helpers — `_square_between_edges`,
`_square_bend`, `_square_curve`, `_square_stub`,
`square_for_edges_paths`) is **deliberate, deferred**.
Consolidating through a shared `tile`-geom parameter (`corners`,
`edges`, `opposite_edge`, `edge_midpoint`, `edge_unit_dir`,
`shared_corner`, `edge_unit_normal`) is the natural next refactor,
but the right shape will fall out of what the diff harness needs to
swap — premature to do it before then.  Shared invariants
(`cap_plane`, `path_chord_*`, the +normal-keep bisect convention)
are already in `way_topology.py` and projection-agnostic;
`tests/test_way.py::_ProjectionInvariants` runs property-based
checks against both projections so a future asymmetry trips the
test instead of silently miscomposing an atlas.
