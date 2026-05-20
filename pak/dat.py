"""Simutrans `.dat` read / port / emit.

A `.dat` file holds one or more objects separated by lines of
dashes (`----------`).  Upstream Britain commonly packs related
vehicles into one file (locomotive + tender, EMU set, carriage
family — ~40 % of `trains/` is multi-object).  The parser
surfaces objects as `list[list[(key, value)]]`; bake scripts
emit one output per object regardless of how upstream grouped
them.

A "bake unit" is one bake script.  It owns one or more `Vehicle`
instances (typed dataclass, fields cover the full upstream
schema) and calls `emit_vehicles` per output.  `Vehicle.__init__`
catches typos at construction; `emit_vehicles` writes the dat
with image refs pointing at the atlas baked alongside.

`Vehicle` fields cover both hex-engine and Simutrans-Extended
schema.  `emit_vehicles` writes all set fields — the hex engine
ignores keys it doesn't recognise, so extended-only keys are
harmless cruft from its perspective, and shipping the full
schema makes the dat round-trip-capable with an Extended-aware
tool if one's ever wanted.  Some Vehicle fields use a custom
dat-key (e.g. `payload_by_class` -> `payload[N]`); those carry
`metadata["dat_key"]` to override the default
field-name-is-dat-key convention.

`Building` is the obj=building counterpart — covers attractions,
monuments, city buildings (res/com/ind), townhalls, HQs, and the
stop/extension overlay objects.  Footprint is `(dims_x, dims_y)`
tiles with `layouts` rotation variants (default per engine rule:
1 if square, 2 if rectangular).  Image refs follow the engine's
`backimage[layout][y][x][height][phase][season]` six-bracket
shape parsed in `descriptor/writer/building_writer.cc`; each
layout's per-tile cells land on one atlas row, with
`size.x*size.y` cells per row (y/x bounds swap on odd layouts
per the engine's `h = (l&1) ? size.x : size.y` rule).  Factories
(`Obj=factory`, with input/output goods + productivity) carry a
fatter schema and are not modelled by `Building` yet.
"""

from __future__ import annotations

import re
from dataclasses import MISSING, dataclass, field, fields, replace
from enum import IntEnum
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pak.way import HEX_ENTRIES

if TYPE_CHECKING:
    from pak.materials import Lighting, Material

_INDEX_RE = re.compile(r"\[([^\]]*)\]")
_TERMINATOR_RE = re.compile(r"^-+\s*$")
# Trailing comment after a value: any whitespace + `#` + rest of line.
# Upstream uses ` # …` (e.g. `way_constraint_prohibitive[6]=6 # Large
# ship`) and tab-prefixed (e.g. `Image[0][1]=basement.0.0\t# wall=…`).
_TRAILING_COMMENT_RE = re.compile(r"\s+#.*$")

# Single-row 8-facing atlas; column i corresponds to facings[i]
# in render.py / viewpoints.py HEX_VIEWPOINT.  Match exactly or
# the engine renders the wrong sprite per direction.  makeobj's
# image-ref parser (image_writer.cc) reads `<file>.X.Y` as
# row=X, col=Y, so a single-row atlas addresses cells as
# `.0.<col>` — see "Atlas layout" in CLAUDE.md.
_HEX_FACINGS: tuple[str, ...] = ("S", "SW", "W", "NW", "N", "NE", "E", "SE")

# Way ribi atlas layout — mirrors `pak/bake_way.py::_stitch_atlas`
# under `HEX_PROJECTION` (`atlas_cols=8`, leading `-` cell, then the
# 63 `HEX_ENTRIES` ribis in popcount-then-ribi order).  Cell index `i`
# in this labels list lands at row `i // 8`, col `i % 8`.  The dat's
# `image[<label>][season]=./<basename>.<row>.<col>` references must
# match this layout or the engine renders the wrong sprite per ribi.
_HEX_WAY_LABELS: tuple[str, ...] = ("-",) + tuple(label for label, _ in HEX_ENTRIES)
_HEX_WAY_ATLAS_COLS: int = 8

# Hex bridge atlas layout.  Single source of truth shared with
# `pak.bake.bake_bridge` (stitches piece renders to match) and
# `pak.viewpoints.bridge_hex_viewpoint` (rotates the model to render
# each label).  Drift across the three modules surfaces in-engine as
# wrong-axis or wrong-direction sprites.
#
# Three piece kinds, one row each:
#
# * `image` (BackImage / FrontImage) is *axial* — a straight span
#   connects two opposite hex edges, so 3 distinct orientations:
#       n_s     N edge <-> S edge
#       ne_sw   NE edge <-> SW edge
#       nw_se   NW edge <-> SE edge
# * `start` (BackStart / FrontStart) — abutment at one of the 6 hex
#   edges; 6 cells in `pak.way.SLOPE_HEX_ENTRIES` order (cw from N).
# * `ramp` (BackRamp / FrontRamp) — ramp at one of the 6 hex edges;
#   same 6 labels as start.
#
# Atlas: row 0 image (cols 0..2; cols 3..5 transparent), row 1 start
# (cols 0..5), row 2 ramp (cols 0..5).  The hex-engine bridge schema
# is unverified -- hex `bridge_writer.cc` is the authoritative key
# source; tokens here are translated from upstream's square
# [NS]/[EW] / [N]/[S]/[E]/[W] keys (see TODO.md -> "Hex bridge cell
# coverage").
HEX_BRIDGE_PIECE_ORDER: tuple[str, ...] = ("image", "start", "ramp")
HEX_BRIDGE_PIECE_LABELS: dict[str, tuple[str, ...]] = {
    "image": ("n_s", "ne_sw", "nw_se"),
    "start": ("n", "ne", "se", "s", "sw", "nw"),
    "ramp":  ("n", "ne", "se", "s", "sw", "nw"),
}
HEX_BRIDGE_ATLAS_COLS: int = max(
    len(labels) for labels in HEX_BRIDGE_PIECE_LABELS.values()
)


def _list_field(*, dat_key: str | None = None) -> Any:
    """Indexed-list field with an optional dat-key override.

    Use `_list_field()` for fields whose dat key matches the
    Python name (`comfort` -> `comfort[N]`).  Pass `dat_key=` to
    remap (`payload_by_class` -> `payload[N]`).
    """
    meta = {"dat_key": dat_key} if dat_key else {}
    return field(default_factory=list, metadata=meta)


def _bake_meta(default: Any = None) -> Any:
    """Bake-pipeline metadata field — declared on the SPEC dataclass but
    skipped by the dat emitters.  The blend path, upstream PNG stem,
    per-material recipe, winter sibling and EEVEE lighting tune all
    live on SPEC so that one named bundle per asset is the source of
    truth, but none of them maps to a hex-engine dat key — they're
    inputs to the bake pipeline, consumed by `pak.bake` and
    `pak.check` rather than emitted into `.dat`.
    """
    return field(default=default, metadata={"bake_meta": True})


@dataclass
class Vehicle:
    """A `obj=vehicle` definition.  Fields cover both hex-engine
    and Simutrans-Extended schema; `emit_vehicles` writes all set
    fields and the hex engine ignores keys it doesn't recognise.

    Order of fields = canonical emit order.  Unset scalars
    (`None`) and empty lists are skipped on emit, matching
    upstream's convention of omitting keys that take the engine's
    default.
    """
    # Required
    name: str
    waytype: str

    # Identity / metadata
    copyright: str | None = None
    freight: str | None = None
    engine_type: str | None = None

    # Lifecycle
    intro_year: int | None = None
    intro_month: int | None = None
    retire_year: int | None = None
    retire_month: int | None = None

    # Physical / performance
    speed: int | None = None
    length: int | None = None
    weight: float | None = None
    axle_load: int | None = None
    axles: int | None = None
    power: int | None = None
    gear: int | None = None
    tractive_effort: int | None = None
    brake_force: int | None = None
    rolling_resistance: int | None = None
    way_wear_factor: int | None = None

    # Capacity / class
    payload: int | None = None
    loading_time: int | None = None
    min_loading_time: int | None = None
    max_loading_time: int | None = None
    overcrowded_capacity: int | None = None
    catering_level: int | None = None
    comfort: int | None = None  # scalar default; class breakdown in comfort_by_class

    # Economics
    cost: int | None = None
    runningcost: int | None = None
    fixed_cost: int | None = None
    maintenance: int | None = None
    upgrade_price: int | None = None
    increase_maintenance_after_years: int | None = None
    years_before_maintenance_max_reached: int | None = None

    # Coupling / behaviour
    bidirectional: int | None = None
    can_lead_from_rear: int | None = None

    # Effects
    smoke: str | None = None
    sound: str | None = None

    # Aircraft
    minimum_runway_length: int | None = None
    range: int | None = None

    # Indexed lists.  Field name = dat key, except `payload_by_class`
    # which targets the upstream `payload[N]=` convention.
    constraint_prev: list[str] = field(
        default_factory=list,
        metadata={"dat_key": "Constraint[Prev]"},
    )
    constraint_next: list[str] = field(
        default_factory=list,
        metadata={"dat_key": "Constraint[Next]"},
    )
    payload_by_class: list[int] = _list_field(dat_key="payload")
    comfort_by_class: list[int] = _list_field(dat_key="comfort")
    liverytype: list[str] = _list_field()
    upgrade: list[str] = _list_field()
    way_constraint_permissive: list[str] = _list_field()

    # Bake-pipeline metadata.  Not emitted into the dat.
    blend: str | None = _bake_meta()
    upstream_dat: str | None = _bake_meta()


_VEHICLE_FIELDS_SCALAR: tuple[str, ...] = tuple(
    f.name for f in fields(Vehicle)
    if f.default_factory is MISSING and not f.metadata.get("bake_meta")
)
# (field_name, dat_key) pairs for indexed-list emission.
_VEHICLE_FIELDS_LIST: tuple[tuple[str, str], ...] = tuple(
    (f.name, f.metadata.get("dat_key", f.name))
    for f in fields(Vehicle)
    if f.default_factory is not MISSING and not f.metadata.get("bake_meta")
)


@dataclass
class Way:
    """A `obj=way` definition.  Fields cover the hex-engine schema
    (`descriptor/writer/way_writer.cc`) plus a few Simutrans-Extended
    keys the upstream Britain dats carry (`wear_capacity`, `axle_load`).
    Image refs are derived from the baked hex ribi atlas at emit time —
    SPECs hold gameplay data only.

    Order of fields = canonical emit order.  Unset scalars (`None`)
    are skipped on emit, matching upstream's convention of omitting
    keys that take the engine's default.
    """
    # Required
    name: str
    waytype: str

    # Identity / metadata
    copyright: str | None = None
    system_type: int | None = None

    # Lifecycle
    intro_year: int | None = None
    intro_month: int | None = None
    retire_year: int | None = None
    retire_month: int | None = None

    # Performance / load
    topspeed: int | None = None
    max_weight: int | None = None
    axle_load: int | None = None
    wear_capacity: int | None = None

    # Economics
    cost: int | None = None
    maintenance: int | None = None

    # Rendering hints
    draw_as_ding: int | None = None
    clip_below: int | None = None
    has_double_slopes: int | None = None

    # Toolbar / placement, read via `cursorskin_writer_t` in
    # `way_writer.cc`.  `port_way` drops upstream's `./images/...`
    # refs (their PNGs were stripped from history); `emit_way`
    # defaults unset values to existing ribi-atlas cells so
    # `way_builder_t::weg_search` picks the way up as a buildable
    # default (TODO.md → "Bake hex icon + cursor sprites for ways").
    # SPECs that want bespoke artwork set their own ref.
    icon: str | None = None
    cursor: str | None = None

    # Bake-pipeline metadata.  Not emitted into the dat.  `materials`
    # is a per-blend-material RGB recolour dict applied via
    # `mat.diffuse_color` before render — see
    # `docs/bake-way.md` -> "Per-way material recolour".
    blend: str | None = _bake_meta()
    # Upstream repo to fetch `blend` from: "jp" (jamespetts) or "jh"
    # (JamesHood; carries the integrated per-ribi viaduct families
    # that jamespetts doesn't ship -- see CLAUDE.md "Cross-repo
    # provenance").  Mirrors `Building.blend_source`.
    blend_source: str = _bake_meta(default="jp")
    upstream_dat: str | None = _bake_meta()
    materials: dict[str, tuple[int, int, int]] | None = _bake_meta()
    # Install the blend's authored camera instead of the projection
    # default; JH viaduct blends author SW-looking-NE at
    # ortho_scale=12 which doesn't match SQUARE_VIEWPOINT['S'].
    inherit_camera: bool = _bake_meta(default=False)
    # 1-to-1 cell render: skip chord composition entirely and alias
    # one render as every cell of the atlas.  For JH full-cell
    # viaduct blends where geometry already fills the cell;
    # `full_cell_rotations` is a per-ribi world-Z rotation in
    # degrees so an EW-authored blend can cover NS via `{"NS": 90}`.
    full_cell: bool = _bake_meta(default=False)
    full_cell_rotations: dict[str, float] | None = _bake_meta()
    # Comma-separated mesh names to drop on entry; default Sphere is
    # the upstream sun-direction visualizer.  Per-blend overrides go
    # here when the blend ships extra debug meshes that don't belong
    # in the bake (see CLAUDE.md -> "Way-bake architecture" -> Naming
    # pitfall).
    strip: str = _bake_meta(default="Sphere")


_WAY_FIELDS_SCALAR: tuple[str, ...] = tuple(
    f.name for f in fields(Way) if not f.metadata.get("bake_meta")
)


@dataclass
class Bridge:
    """A `obj=bridge` definition.  Fields cover the upstream Britain
    schema (`plate-girder.dat` shape: gameplay scalars + per-direction
    per-variant per-season Back/Front Image / Start / Ramp cells).
    Image refs are derived from the baked hex bridge atlas at emit
    time -- SPECs hold gameplay data + the three piece-blend paths
    only.

    The hex bridge bake renders three JH-sourced blends -- one per
    piece kind (image span, start abutment, ramp) -- through
    `bridge_hex_viewpoint(piece)`, stitches the per-piece atlases
    into one `<basename>.png` (see `_HEX_BRIDGE_*` above), and writes
    image refs against that layout.  Only variant-1 (no `2` suffix)
    and season 0 are emitted on the first pass; variant 2,
    snow / season 1 and depth-clipped Front cells are deferred -- see
    TODO.md -> "Hex bridge cell coverage" for the follow-up list.

    Order of fields = canonical emit order.  Unset scalars (`None`)
    are skipped on emit.
    """
    # Required
    name: str
    waytype: str

    # Identity / metadata
    copyright: str | None = None

    # Lifecycle
    intro_year: int | None = None
    intro_month: int | None = None
    retire_year: int | None = None
    retire_month: int | None = None

    # Performance / load
    topspeed: int | None = None
    max_weight: int | None = None
    max_length: int | None = None

    # Economics
    cost: int | None = None
    maintenance: int | None = None

    # Engine behaviour
    has_own_way_graphics: int | None = None
    pillar_distance: int | None = None
    pillar_asymmetric: int | None = None

    # Toolbar / placement.  Defaulted to existing atlas cells in
    # `emit_bridge` when unset, matching the `Way` convention --
    # `bridge_builder_t::lookup` picks the bridge up as a buildable
    # default rather than failing on a missing icon ref.
    icon: str | None = None
    cursor: str | None = None

    # Bake-pipeline metadata.  Not emitted into the dat.  Three blend
    # paths -- one per piece kind -- because JH ships the plate-
    # girder family as three separate `.blend` files
    # (straight / end / slope); `bake_bridge` renders each through
    # `bridge_hex_viewpoint(piece)` and stitches the per-piece atlases
    # into one PNG.  All three are required; partial families need a
    # `_bridge_piece_blends` change first.
    blend_image: str | None = _bake_meta()
    blend_start: str | None = _bake_meta()
    blend_ramp: str | None = _bake_meta()
    upstream_dat: str | None = _bake_meta()


_BRIDGE_FIELDS_SCALAR: tuple[str, ...] = tuple(
    f.name for f in fields(Bridge) if not f.metadata.get("bake_meta")
)


@dataclass
class Tunnel:
    """A `obj=tunnel` definition.  Fields cover the hex-engine schema
    (`descriptor/writer/tunnel_writer.cc`) plus a few extended scalars
    the engine silently ignores.  Per-facing image refs are derived from
    the baked atlas at emit time; see `tunnel_hex_viewpoint` for the
    Front/Back split and atlas layout.

    Snow season `[1]` refs and the multi-portal `<edge>{l,r,m}` suffix
    variants (4-portal broad tunnels) aren't emitted yet -- see TODO.md
    "Tunnel snow + multi-portal variants".

    Order of fields = canonical emit order.  Unset scalars are skipped.
    """
    # Required
    name: str
    waytype: str

    # Identity
    copyright: str | None = None

    # Lifecycle
    intro_year: int | None = None
    intro_month: int | None = None
    retire_year: int | None = None
    retire_month: int | None = None

    # Performance / load.  `axle_load` is read by `tunnel_writer.cc`;
    # `max_weight` is Extended-only and silently ignored by hex --
    # kept for round-trip fidelity (mirrors Vehicle's convention).
    topspeed: int | None = None
    max_weight: int | None = None
    axle_load: int | None = None

    # Economics
    cost: int | None = None
    maintenance: int | None = None

    # Optional xref to a way object (engine builds it under the tunnel
    # cell on placement); upstream's `severn-tunnel-track` was wired
    # this way.  Empty / None = no embedded way.
    way: str | None = None

    # Toolbar / placement -- defaulted to atlas cells at emit time
    # when unset (mirrors Bridge / Way).
    icon: str | None = None
    cursor: str | None = None

    # Bake-pipeline metadata.  `blend_source` defaults to "jh" since
    # the first ported tunnel (stone-tunnel) lives in JamesHood's
    # blends repo; jamespetts has the canal-tunnel blends and would
    # use `blend_source="jp"`.
    blend: str | None = _bake_meta()
    blend_source: str = _bake_meta(default="jh")
    upstream_dat: str | None = _bake_meta()


_TUNNEL_FIELDS_SCALAR: tuple[str, ...] = tuple(
    f.name for f in fields(Tunnel) if not f.metadata.get("bake_meta")
)


# Hex tunnel facing labels in canonical atlas column order, matching
# `hex_keys::edge_names` in the engine writer.  Order is cw-from-N
# (same as bridge `start` / `ramp`), so col 0 = n, ..., col 5 = nw.
TUNNEL_FACING_LABELS: tuple[str, ...] = ("n", "ne", "se", "s", "sw", "nw")


class Symmetry(IntEnum):
    """Building silhouette symmetry — `Building.symmetry`.

    Numeric value is the order of the rotational group: `NONE = 1`
    (trivial, asymmetric); `CONTINUOUS = 0` is the sentinel for a
    continuously-symmetric silhouette (cylinder, sphere — looks the
    same under any rotation).  IntEnum so the consumer (`pak.bake.
    hex_layouts_default`) can use `int(symmetry)` in the gcd
    reduction; extend with `BILATERAL = 2`, `ROTATIONAL_N = N` when
    a port surfaces that authoring.
    """

    NONE = 1
    CONTINUOUS = 0


@dataclass
class Building:
    """A `obj=building` definition.  Fields cover the hex-engine schema
    (`descriptor/writer/building_writer.cc`) plus the Simutrans-Extended
    demand / employment / class-proportion keys upstream Britain dats
    carry.  Image refs are derived from the baked atlas at emit time;
    SPECs hold gameplay data only.

    Footprint is `(dims_x, dims_y)` tiles.  Layout count
    (the Z in `dims=X,Y,Z`) is not a SPEC field — the bake driver
    derives it from `symmetry` and threads it through
    `emit_building`'s `layouts` kwarg.  Declares what the *asset*
    looks like (its silhouette symmetry) and lets the bake decide
    how many rotations to render under the active projection.

    Order of fields = canonical emit order.  Unset scalars (`None`) and
    empty lists are skipped on emit.  Factory-only keys (InputGood,
    OutputGood, Productivity, …) are not modelled here; a future
    `Factory` dataclass covers `Obj=factory`.
    """
    # Required
    name: str
    type: str  # res/com/ind/cur/mon/tow/hq/dock/harbour/fac/stop/extension/...

    # Identity / metadata
    copyright: str | None = None

    # Footprint — emitted together as `dims=X,Y,Z`; Z (layouts)
    # threads through emit_building from the bake driver.
    dims_x: int = 1
    dims_y: int = 1

    # Symmetry of the asset's silhouette — projection-agnostic; the
    # bake derives the layout count, see `pak.bake.hex_layouts_default`.
    symmetry: Symmetry = _bake_meta(default=Symmetry.NONE)

    # Vertical stack — number of `backimage[…][height][…]` levels the
    # engine paints, each shifted up by `raster_width` px (one full
    # cell).  Single-cell buildings keep `heights=1`; a 2-storey
    # detached house typically needs 2 since its model is too tall to
    # fit one hex cell at the pakset calibration.  See CLAUDE.md ->
    # "Building-bake architecture" for the world-z per height-level.
    heights: int = 1

    # Seasonal variants — number of `backimage[…][season]` slots the
    # engine reads (0 = summer, 1 = winter, …).  Default 1 = summer
    # only; set 2 to opt in to a winter render.  The atlas grows a
    # season-major top half (summer) / bottom half (winter) row layout
    # — see `emit_building` / `iter_building_cells` for the formula and
    # CLAUDE.md -> "Building-bake architecture" for the snow pass.
    seasons: int = 1

    # Type-specific
    level: int | None = None
    chance: int | None = None

    # Lifecycle
    intro_year: int | None = None
    intro_month: int | None = None
    retire_year: int | None = None
    retire_month: int | None = None

    # Siting / placement
    needs_ground: int | None = None
    noinfo: int | None = None
    noconstruction: int | None = None
    allow_underground: int | None = None
    climates: str | None = None
    regions: str | None = None

    # Build (mon/tow/cur)
    build_time: int | None = None

    # Demand / employment (Simutrans-Extended)
    population_and_visitor_demand_capacity: int | None = None
    employment_capacity: int | None = None
    mail_demand: int | None = None
    passengers: int | None = None  # cur/mon/tow/hq alias for level

    # HQ
    hq_level: int | None = None

    # Stops / extensions
    waytype: str | None = None
    capacity: int | None = None
    maintenance: int | None = None
    cost: int | None = None

    # Animation
    animation_time: int | None = None

    # Effects
    smoke: str | None = None

    # Indexed lists
    class_proportion: list[int] = field(default_factory=list)
    class_proportion_jobs: list[int] = field(default_factory=list)
    upgrade: list[str] = field(default_factory=list)

    # Bake-pipeline metadata.  Not emitted into the dat.  `materials`
    # is a per-blend-material `Material` recipe (BI slot stacks, image
    # refs, procedural noise); `lighting` overrides the EEVEE ambient
    # / sun tune per asset.  `blend_winter` / `materials_winter` opt
    # the asset into the winter atlas pass when `seasons >= 2`.
    # `blend_source` selects which upstream blends repo `blend` /
    # `blend_winter` resolve against -- "jp" = jamespetts (default,
    # citybuildings / signals / etc.), "jh" = JamesHood (attractions
    # and other categories jamespetts doesn't carry).
    blend: str | None = _bake_meta()
    upstream_dat: str | None = _bake_meta()
    materials: dict[str, Material] | None = _bake_meta()
    blend_winter: str | None = _bake_meta()
    materials_winter: dict[str, Material] | None = _bake_meta()
    lighting: Lighting | None = _bake_meta()
    blend_source: str = _bake_meta(default="jp")
    # Blend-frame world units per engine tile.  Sole anchor for the
    # asset's render scale (camera ortho, canvas, fit_matrix all
    # derive from this and `dims`).  Default 12 = the contributing-
    # graphics building convention; override for assets that render
    # at a different per-tile rate.
    blend_units_per_tile: float = _bake_meta(default=12.0)
    # World-space offset declaring where the model's centre actually
    # sits, when the artist authored it away from world origin.  The
    # renderer pre-translates by `-offset` before everything else, so
    # the model's effective centre lands at world origin -- the layout
    # rotation then pivots around the model's centre, not around an
    # arbitrary world point.  Default None means the artist honoured
    # the contributing-graphics spec ("centre near origin"); the diff
    # will surface any drift as IoU residual, and the porter can pin
    # the offset here after investigation (e.g. via the
    # `pak.diag_centroid_align` sweep).  Units: world units, same
    # frame as the blend's authored XYZ.
    blend_model_offset_xyz: tuple[float, float, float] | None = _bake_meta()
    # Comma-separated mesh names to drop from the scene on entry.
    # Default `Sphere` is the upstream sun-direction visualizer; per-blend
    # overrides go here when a blend ships extra debug meshes that have no
    # material slot (so `materials=` can't reach them) and aren't picked up
    # by upstream's BI renderer either — e.g. attractions/stonehenge.blend
    # ships three corner registration quads (Plane.002/004/005) with empty
    # `material_slots` that Cycles renders as flat-grey squares.  Same
    # shape as `Way.strip`; both wire through `render.py`'s
    # `Viewpoint.strip_meshes`.
    strip: str = _bake_meta(default="Sphere")


@dataclass
class Tree:
    """A `obj=tree` definition (`descriptor/writer/tree_writer.cc`).

    The engine reads exactly 5 ages and `seasons` seasonal variants
    (`seasons` ∈ {1, 2, 4, 5}); `image[age][season]` keys point at one
    sprite each.  Upstream pak128.Britain conventionally maps age 4
    (oldest / dormant) to the bare `<stem>-winter-3` image across every
    non-winter season -- `emit_trees` mirrors that by exposing an
    optional `age_overrides` map below.

    Order of fields = canonical emit order.  Unset scalars (`None`) are
    skipped on emit; `seasons` and `distribution_weight` always emit
    (the engine reads them as required scalars even though it has
    defaults).
    """
    # Required
    name: str

    # Identity / metadata
    copyright: str | None = None

    # Engine behaviour
    distribution_weight: int = 3
    climates: str | None = None
    # 1 = no seasons, 2 = summer+winter, 4 = summer/autumn/winter/spring,
    # 5 = + winter-snow.  See `tree_writer.cc`.
    seasons: int = 1

    # Bake-pipeline metadata.  Not emitted into the dat.
    blend: str | None = _bake_meta()
    upstream_dat: str | None = _bake_meta()


_TREE_FIELDS_SCALAR: tuple[str, ...] = tuple(
    f.name for f in fields(Tree)
    if f.name != "seasons" and not f.metadata.get("bake_meta")
)
# Engine reads exactly 5 ages (`tree_writer.cc` loops `age in 0..5`);
# not configurable per asset.  Public so bake-side callers can clamp
# their rendered-age count against it without re-declaring the magic
# number.
TREE_AGE_COUNT: int = 5


def layouts_default(dims_x: int, dims_y: int) -> int:
    """Engine default for `layouts` when `dims=` carries only `X,Y`.

    Mirrors `building_writer.cc::write_obj`: `layouts = (size.x == size.y)
    ? 1 : 2`.  Square footprints have no asymmetric rotation, so the
    engine keys all four map rotations to the one layout; rectangular
    footprints need two variants (one per orientation) and the engine
    keys map rotations pairwise."""
    return 1 if dims_x == dims_y else 2


# `[layout][y][x][height][phase][season]` bracket order — fixed by
# `building_writer.cc::write_obj` (the hex engine reads only this
# order).  Phase defaults to 0 for an asset bake without animation;
# season is loop-driven from `Building.seasons` (1 = summer only, 2 =
# +winter).  Height varies per (l,y,x,h) cell.
_BUILDING_IMAGE_PHASE = 0


# dims_x / dims_y emit together as a single `dims=X,Y,Z` line (Z
# is the bake-supplied `layouts` kwarg), not as plain `name=value`
# per field.  `heights` is implicit in the per-(l,y,x,h) backimage
# refs — the engine reads height levels until the next index
# returns no key — so it doesn't get a scalar key either.  All
# three filtered out of the generic emit.
_BUILDING_FIELDS_SCALAR: tuple[str, ...] = tuple(
    f.name for f in fields(Building)
    if f.default_factory is MISSING
    and f.name not in ("dims_x", "dims_y", "heights", "seasons")
    and not f.metadata.get("bake_meta")
)
_BUILDING_FIELDS_LIST: tuple[tuple[str, str], ...] = tuple(
    (f.name, f.metadata.get("dat_key", f.name))
    for f in fields(Building)
    if f.default_factory is not MISSING and not f.metadata.get("bake_meta")
)


def iter_building_cells(b: Building, *, layouts: int):
    """Yield `(season, layout, y, x, height)` quintuples in canonical emit
    order.

    Iteration order: `s, h, l, y, x` — season outermost, height next,
    then layout, then the per-layout `(y, x)` cells.  Matches the
    atlas layout `row = s * heights + h`, `col = l * dims_x*dims_y +
    y * w + x` (each season is a `heights`-row stripe; within a
    stripe, each row is one height; each row's columns walk the
    layout blocks left-to-right).  For 1x1xN-layout single-height
    buildings with seasons=2 the result is the upstream
    `1600-detatched-house-2f.png` shape: row 0 = summer layouts,
    row 1 = winter layouts.

    Per-layout `(y, x)` follows the engine's loops in
    `building_writer.cc`: even layouts iterate `y in [0, size.y),
    x in [0, size.x)`; odd layouts swap to `y in [0, size.x),
    x in [0, size.y)`.  Heights stack via the engine's
    `ypos -= raster_width` per level (see `obj/gebaeude.cc`); the
    engine reads height levels by incrementing until the key returns
    empty, so heights / seasons are implicit in the emitted refs (no
    `heights=N` / `seasons=N` scalars).  Bake scripts use this to
    drive per-cell renders; emit_building uses it to wire image
    refs."""
    for s in range(b.seasons):
        for h in range(b.heights):
            for l in range(layouts):
                if l & 1:
                    yh, xw = b.dims_x, b.dims_y
                else:
                    yh, xw = b.dims_y, b.dims_x
                for y in range(yh):
                    for x in range(xw):
                        yield s, l, y, x, h


def building_footprint_centroid(
    dims_x: int, dims_y: int, layout: int,
) -> tuple[float, float]:
    """Per-layout footprint centroid in (x, y) koord units.  Mirrors the
    engine's even/odd `(y, x)` cell-range swap from `building_writer.cc`
    (even layouts span [dims_y, dims_x], odd layouts swap to
    [dims_x, dims_y]).  Used to anchor render canvases and stitch
    upstream cells so a building authored with its model centred on
    world (0, 0, 0) lands its footprint midpoint at the canvas centre,
    same convention either side of the calibration diff."""
    if layout & 1:
        return ((dims_y - 1) / 2.0, (dims_x - 1) / 2.0)
    return ((dims_x - 1) / 2.0, (dims_y - 1) / 2.0)


def parse(path: Path) -> list[list[tuple[str, str]]]:
    """Parse a `.dat` into a list of objects.

    Each object is a list of `(key, value)` pairs in source order.
    Comments and blank lines are dropped.  A line of dashes ends
    the current object; trailing empty objects are pruned.
    """
    objects: list[list[tuple[str, str]]] = [[]]
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if _TERMINATOR_RE.match(line):
            if objects[-1]:
                objects.append([])
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = _TRAILING_COMMENT_RE.sub("", value)
        objects[-1].append((key.strip(), value.strip()))
    if not objects[-1]:
        objects.pop()
    return objects


def _vehicle_block(vehicle: Vehicle, basename: str) -> list[str]:
    lines = ["obj=vehicle"]
    for name in _VEHICLE_FIELDS_SCALAR:
        v = getattr(vehicle, name)
        if v is not None:
            lines.append(f"{name}={v}")
    for attr, dat_key in _VEHICLE_FIELDS_LIST:
        for i, v in enumerate(getattr(vehicle, attr)):
            lines.append(f"{dat_key}[{i}]={v}")
    for col, facing in enumerate(_HEX_FACINGS):
        lines.append(f"EmptyImage[{facing}]=./{basename}.0.{col}")
    return lines


def emit_vehicles(vehicles: list[Vehicle], *, out_dir: Path, basename: str) -> Path:
    """Write `<out_dir>/<basename>.dat` from one or more Vehicles.

    Each Vehicle becomes an `obj=vehicle` block separated by a row
    of dashes; every block's image refs point at the same shared
    atlas `./<basename>.0.<col>`.  Multi-Vehicle calls (e.g.
    upstream's `dragon-rapide` + `dragon-rapide-mail`, same plane
    in different gameplay roles) pack into one combined dat; when
    variants want distinct sprites, give each its own bake unit
    instead.  Returns the dat path.
    """
    if not vehicles:
        raise ValueError("emit_vehicles requires at least one Vehicle")
    lines: list[str] = []
    for v in vehicles:
        lines.extend(_vehicle_block(v, basename))
        lines.append("----------")
    out_path = out_dir / f"{basename}.dat"
    out_path.write_text("\n".join(lines) + "\n")
    return out_path


def emit_way(way: Way, *, out_dir: Path, basename: str) -> Path:
    """Write `<out_dir>/<basename>.dat` from a Way.

    Emits every set scalar plus `image[<ribi_label>][0]=./<basename>.<row>.<col>`
    for each cell of the hex ribi atlas (popcount-then-ribi order, 8
    cols × 8 rows; see `_HEX_WAY_LABELS`).  The PNG must live at
    `<out_dir>/<basename>.png` and match that layout exactly — drift
    surfaces in-engine as the wrong sprite per ribi.

    Slope sprites (`imageup[<slope_key>][N]`), seasons and front layer
    are not yet baked, so this writer omits them; revisit when the
    slope-cell pass lands.  `cursor` / `icon` default to existing ribi
    cells (TODO.md → "Bake hex icon + cursor sprites for ways") so the
    engine's `way_builder_t::weg_search` picks the way up as a
    buildable default; SPECs override by setting their own.  Returns
    the dat path.
    """
    way = replace(
        way,
        cursor=way.cursor or f"./{basename}.0.0",
        icon=way.icon or f"./{basename}.1.6",
    )
    lines: list[str] = ["obj=way"]
    for name in _WAY_FIELDS_SCALAR:
        v = getattr(way, name)
        if v is not None:
            lines.append(f"{name}={v}")
    for i, label in enumerate(_HEX_WAY_LABELS):
        row, col = divmod(i, _HEX_WAY_ATLAS_COLS)
        lines.append(f"image[{label}][0]=./{basename}.{row}.{col}")
    lines.append("----------")

    out_path = out_dir / f"{basename}.dat"
    out_path.write_text("\n".join(lines) + "\n")
    return out_path


# dat-key prefix per piece kind -- the engine reads e.g.
# `BackImage[<axis>][<season>]` for image, `BackRamp[<dir>][<season>]`
# for ramp.  Capitalisation matches upstream's plate-girder.dat.
_HEX_BRIDGE_PIECE_KEYS: dict[str, str] = {
    "image": "Image",
    "start": "Start",
    "ramp":  "Ramp",
}


def emit_bridge(bridge: Bridge, *, out_dir: Path, basename: str) -> Path:
    """Write `<out_dir>/<basename>.dat` from a Bridge.

    Emits every set scalar plus, per piece in `HEX_BRIDGE_PIECE_ORDER`,
    one `Back<Key>[<label>][0]` and one `Front<Key>[<label>][0]` per
    label in `HEX_BRIDGE_PIECE_LABELS[piece]`.  Front points at the
    same atlas cell as Back -- depth-clipped slicing is deferred, so
    the bridge silhouette is fully opaque over crossing vehicles
    until then (TODO.md -> "Hex bridge cell coverage").

    The PNG must live at `<out_dir>/<basename>.png` and match the
    canonical hex bridge atlas layout (`HEX_BRIDGE_*` above) --
    `pak.bake.bake_bridge` is the producer.  Returns the dat path.
    """
    bridge = replace(
        bridge,
        cursor=bridge.cursor or f"./{basename}.1.0",
        icon=bridge.icon or f"./{basename}.0.0",
    )
    lines: list[str] = ["obj=bridge"]
    for name in _BRIDGE_FIELDS_SCALAR:
        v = getattr(bridge, name)
        if v is not None:
            lines.append(f"{name}={v}")

    for row, piece in enumerate(HEX_BRIDGE_PIECE_ORDER):
        key = _HEX_BRIDGE_PIECE_KEYS[piece]
        for col, label in enumerate(HEX_BRIDGE_PIECE_LABELS[piece]):
            cell = f"./{basename}.{row}.{col}"
            lines.append(f"Back{key}[{label}][0]={cell}")
            lines.append(f"Front{key}[{label}][0]={cell}")
    lines.append("----------")

    out_path = out_dir / f"{basename}.dat"
    out_path.write_text("\n".join(lines) + "\n")
    return out_path


def emit_tunnel(tunnel: Tunnel, *, out_dir: Path, basename: str) -> Path:
    """Write `<out_dir>/<basename>.dat` from a Tunnel.  Emits every set
    scalar plus `frontimage[<edge>][0]=…0.<col>` + `backimage[<edge>]
    [0]=…1.<col>` for each label in `TUNNEL_FACING_LABELS`.  Producer:
    `pak.bake.bake_tunnel`; atlas layout: `tunnel_hex_viewpoint`."""
    tunnel = replace(
        tunnel,
        cursor=tunnel.cursor or f"./{basename}.0.0",
        icon=tunnel.icon or f"./{basename}.0.0",
    )
    lines: list[str] = ["obj=tunnel"]
    for fname in _TUNNEL_FIELDS_SCALAR:
        v = getattr(tunnel, fname)
        if v is not None:
            lines.append(f"{fname}={v}")
    for col, facing in enumerate(TUNNEL_FACING_LABELS):
        lines.append(f"frontimage[{facing}][0]=./{basename}.0.{col}")
        lines.append(f"backimage[{facing}][0]=./{basename}.1.{col}")
    lines.append("----------")

    out_path = out_dir / f"{basename}.dat"
    out_path.write_text("\n".join(lines) + "\n")
    return out_path


def emit_trees(
    trees: list[Tree], *, out_dir: Path, basename: str,
    age_overrides: dict[tuple[int, int], tuple[int, int]] | None = None,
) -> Path:
    """Write `<out_dir>/<basename>.dat` from one or more Trees.

    Each Tree becomes an `obj=tree` block separated by a row of dashes.
    Atlas layout: rows = seasons (top = summer = 0), cols = ages (left
    = youngest = 0).  Image refs follow `image[age][season]=./<basename>
    .<season>.<age>` per the engine's `image[%d][%d]` writer.

    `age_overrides` redirects specific `(age, season)` cells to a
    different `(age, season)` source cell -- e.g. upstream's convention
    of pointing every non-winter age 4 at the bare `winter-3` cell
    (`{(4, 0): (3, 2), (4, 1): (3, 2), (4, 3): (3, 2)}` for the 5-
    season oak).  Unspecified cells render their own per-cell sprite.

    Multi-Tree calls (e.g. upstream's `tree.dat` packing 4 species)
    pack into one combined dat; all blocks share the same atlas.
    Returns the dat path.
    """
    if not trees:
        raise ValueError("emit_trees requires at least one Tree")
    overrides = age_overrides or {}
    lines: list[str] = []
    for t in trees:
        lines.append("obj=tree")
        for name in _TREE_FIELDS_SCALAR:
            v = getattr(t, name)
            if v is not None:
                lines.append(f"{name}={v}")
        lines.append(f"seasons={t.seasons}")
        for a in range(TREE_AGE_COUNT):
            for s in range(t.seasons):
                src_a, src_s = overrides.get((a, s), (a, s))
                lines.append(
                    f"image[{a}][{s}]=./{basename}.{src_s}.{src_a}"
                )
        lines.append("----------")
    out_path = out_dir / f"{basename}.dat"
    out_path.write_text("\n".join(lines) + "\n")
    return out_path


def emit_building(b: Building, *, out_dir: Path, basename: str,
                  layouts: int | None = None) -> Path:
    """Write `<out_dir>/<basename>.dat` from a Building.

    Emits set scalars, then `dims=X,Y,Z` (Z = `layouts`, supplied by
    the bake driver from `pak.bake.hex_layouts_default(b.symmetry)`;
    falls back to `layouts_default(dims_x, dims_y)` for code paths
    that don't go through the bake driver), then indexed lists, then
    `backimage[l][y][x][h][0][s]=./<basename>.<row>.<col>` per cell.

    Atlas shape: `seasons * heights` rows × `layouts * dims_x*dims_y`
    cols.  Row formula: `row = s * heights + h` — each season is a
    `heights`-row stripe (summer on top, winter under it).  Col
    formula: `col = l * dims_x*dims_y + y * w + x` — layouts span
    horizontally, with each layout's per-tile cells occupying a
    `dims_x*dims_y`-wide block; `w` swaps between `dims_x` and
    `dims_y` per the engine's `h = (l&1) ? size.x : size.y` rule (see
    `iter_building_cells`).  For 1x1xN-layout single-height buildings
    with seasons=2 the result is upstream's two-row atlas
    (summer/winter).  The PNG must live at `<out_dir>/<basename>.png`
    and match that layout exactly — drift surfaces in-engine as the
    wrong sprite per tile/level.

    FrontImage and animation phase variants are not yet emitted;
    revisit when a bake script needs them (occlusion-correct
    foreground, animated effects).  Returns the dat path.
    """
    lines: list[str] = ["obj=building"]
    for name in _BUILDING_FIELDS_SCALAR:
        v = getattr(b, name)
        if v is not None:
            lines.append(f"{name}={v}")
    if layouts is None:
        layouts = layouts_default(b.dims_x, b.dims_y)
    lines.append(f"dims={b.dims_x},{b.dims_y},{layouts}")
    for attr, dat_key in _BUILDING_FIELDS_LIST:
        for i, v in enumerate(getattr(b, attr)):
            lines.append(f"{dat_key}[{i}]={v}")

    footprint = b.dims_x * b.dims_y
    for s, l, y, x, h in iter_building_cells(b, layouts=layouts):
        w = b.dims_y if l & 1 else b.dims_x
        row = s * b.heights + h
        col = l * footprint + y * w + x
        lines.append(
            f"backimage[{l}][{y}][{x}][{h}]"
            f"[{_BUILDING_IMAGE_PHASE}]"
            f"[{s}]"
            f"=./{basename}.{row}.{col}"
        )
    lines.append("----------")

    out_path = out_dir / f"{basename}.dat"
    out_path.write_text("\n".join(lines) + "\n")
    return out_path


# Dat-key (lowercased) -> Vehicle list-field name, derived from
# `metadata["dat_key"]` on list fields.  Handles flat keys like
# `comfort[N]` and nested-bracket keys like `Constraint[Prev][N]`
# uniformly — `_harvest_indexed` keys on the prefix string only.
_INDEXED_HARVEST_TO_FIELD: dict[str, str] = {
    dat_key.lower(): attr for attr, dat_key in _VEHICLE_FIELDS_LIST
}

_BUILDING_INDEXED_HARVEST_TO_FIELD: dict[str, str] = {
    dat_key.lower(): attr for attr, dat_key in _BUILDING_FIELDS_LIST
}


def port_vehicle(object_entries: list[tuple[str, str]]) -> Vehicle:
    """Convert one parsed upstream object to a `Vehicle`.

    Seeder for new asset bakes — run once when porting fresh from
    upstream to produce a starter `Vehicle(...)` call (see
    `seed_python`), paste into the bake script, then maintain
    inline.  Not called at bake time; bake scripts hold the
    `Vehicle` directly.

    Harvests every field the dataclass knows about — including
    extended-only — for upstream fidelity.  Indexed `payload[N]`
    additionally populates the scalar `payload` (max, what the
    hex engine reads) when no explicit scalar is provided.
    """
    lookup = {k.lower(): v for k, v in object_entries}
    if lookup.get("obj", "").lower() != "vehicle":
        raise ValueError(f"not obj=vehicle: {lookup.get('obj')!r}")

    scalars = set(_VEHICLE_FIELDS_SCALAR)
    kwargs: dict = {}
    for k, v in object_entries:
        kl = k.lower()
        if kl in scalars and not _INDEX_RE.search(k):
            kwargs[kl] = _coerce(v)

    for base, dest_field in _INDEXED_HARVEST_TO_FIELD.items():
        values = _harvest_indexed(object_entries, base)
        if values:
            kwargs[dest_field] = [_coerce(v) for v in values]

    if "payload" not in kwargs and "payload_by_class" in kwargs:
        nums = [v for v in kwargs["payload_by_class"] if isinstance(v, int)]
        if nums:
            kwargs["payload"] = max(nums)

    return Vehicle(**kwargs)


_BUILDING_PORT_DROP: frozenset[str] = frozenset({
    # Upstream image keys live under `images/<type>/<name>.X.Y` paths
    # whose PNGs were stripped from history.  The hex bake re-emits
    # them from its own atlas under `backimage[l][y][x][...]=./<basename>.<r>.<c>`;
    # carrying the upstream refs would make makeobj error out at build
    # time (mirrors `Way.icon` / `Way.cursor` handling in `port_way`).
    "backimage", "frontimage",
})


def port_building(object_entries: list[tuple[str, str]]) -> Building:
    """Convert one parsed upstream `obj=building` object to a `Building`.

    Seeder for new building bakes — produces a paste-ready
    `Building(...)` source for a `<dir>/<asset>.py` bake script via
    `seed_python`.  Harvests every scalar `Building` field upstream
    sets plus `dims=X,Y` from the engine's footprint triple — the
    third element (upstream's `layouts`) is the square-dimetric
    rotation count and doesn't carry across; the seeded SPEC takes
    `Symmetry.NONE` by default and the porter adjusts to
    `CONTINUOUS` / `BILATERAL` / etc. by inspection.  Scans
    `backimage[…][height][…]` refs to set `heights = max(height) +
    1` so a seeded SPEC carries the upstream's vertical-stack count.
    Image-ref strings (`backimage[…]=…`, `frontimage[…]=…`) are
    dropped — see `_BUILDING_PORT_DROP`.

    Dat keys are matched case-insensitively (`Type=` and `type=` both
    land on `Building.type`); values are preserved verbatim, which
    matches the engine's STRICMP lookup on type names.
    """
    lookup = {k.lower(): v for k, v in object_entries}
    if lookup.get("obj", "").lower() != "building":
        raise ValueError(f"not obj=building: {lookup.get('obj')!r}")

    scalars = set(_BUILDING_FIELDS_SCALAR)
    kwargs: dict = {}
    max_height = 0
    max_season = 0
    for k, v in object_entries:
        kl = k.lower()
        # Image refs: parse out the height and season indices before
        # dropping the value, so we can set `heights` / `seasons` from
        # the upstream stack depth and seasonal-variant count.
        prefix = kl.split("[", 1)[0]
        if prefix in _BUILDING_PORT_DROP:
            # backimage[L][Y][X][H][P][S] — height idx 3, season idx 5
            indices = [s.rstrip("]") for s in kl.split("[")[1:]]
            if len(indices) >= 4:
                try:
                    max_height = max(max_height, int(indices[3]))
                except ValueError:
                    pass
            if len(indices) >= 6:
                try:
                    max_season = max(max_season, int(indices[5]))
                except ValueError:
                    pass
            continue
        if kl == "dims":
            ints = [int(s.strip()) for s in v.split(",")]
            if len(ints) >= 1:
                kwargs["dims_x"] = ints[0]
            if len(ints) >= 2:
                kwargs["dims_y"] = ints[1]
            continue
        if kl in scalars and not _INDEX_RE.search(k):
            kwargs[kl] = _coerce(v)

    for base, dest_field in _BUILDING_INDEXED_HARVEST_TO_FIELD.items():
        values = _harvest_indexed(object_entries, base)
        if values:
            kwargs[dest_field] = [_coerce(v) for v in values]

    if max_height > 0:
        kwargs["heights"] = max_height + 1
    if max_season > 0:
        kwargs["seasons"] = max_season + 1

    return Building(**kwargs)


_WAY_PORT_DROP: frozenset[str] = frozenset({"icon", "cursor"})


def port_way(object_entries: list[tuple[str, str]]) -> Way:
    """Convert one parsed upstream `obj=way` object to a `Way`.

    Seeder for new way bakes — pastes a starter `Way(...)` source into
    a `ways/<asset>.py` bake script via `seed_python`.  Harvests every
    scalar `Way` field the upstream dat sets; image refs (Upstream
    `Image[<square_ribi>]`, `ImageUp[N]`, `Diagonal[<dir>]`, `cursor`,
    `icon`) are dropped — the hex bake re-emits them from its own
    atlas under `image[<hex_ribi>][N]=...` keys.  `icon` / `cursor`
    upstream values point at `./images/<name>.X.Y` cells that live in
    the upstream pak's stripped images/ dir and would make makeobj
    error out (see `Way.icon` field doc); they're dropped here so a
    seeded SPEC bakes cleanly without manual scrubbing.
    """
    lookup = {k.lower(): v for k, v in object_entries}
    if lookup.get("obj", "").lower() != "way":
        raise ValueError(f"not obj=way: {lookup.get('obj')!r}")

    scalars = set(_WAY_FIELDS_SCALAR)
    kwargs: dict = {}
    for k, v in object_entries:
        kl = k.lower()
        if kl in _WAY_PORT_DROP:
            continue
        if kl in scalars and not _INDEX_RE.search(k):
            kwargs[kl] = _coerce(v)

    return Way(**kwargs)


_BRIDGE_PORT_DROP_PREFIXES: tuple[str, ...] = (
    "backimage", "frontimage", "backstart", "frontstart",
    "backramp", "frontramp", "backpillar", "frontpillar",
)


def port_bridge(object_entries: list[tuple[str, str]]) -> Bridge:
    """Convert one parsed upstream `obj=bridge` object to a `Bridge`.

    Seeder for new bridge bakes -- produces a paste-ready
    `Bridge(...)` source via `seed_python`.  Harvests every scalar
    `Bridge` field the upstream dat sets; per-cell image refs
    (`BackImage[...]`, `FrontStart[...]`, etc., and their `2`-suffixed
    variant cousins) are dropped -- the hex bake re-emits them from
    its own atlas.  `icon` / `cursor` are also dropped (upstream's
    values point at `./images/<name>.X.Y` cells stripped from
    history); `emit_bridge` defaults them to existing atlas cells
    so the bridge picks up as a buildable default.

    Variant-2 keys (`BackImage2`, etc.) are dropped on the same
    prefix-match -- only one variant is bake-side modelled yet.
    """
    lookup = {k.lower(): v for k, v in object_entries}
    if lookup.get("obj", "").lower() != "bridge":
        raise ValueError(f"not obj=bridge: {lookup.get('obj')!r}")

    scalars = set(_BRIDGE_FIELDS_SCALAR)
    kwargs: dict = {}
    for k, v in object_entries:
        kl = k.lower()
        prefix = kl.split("[", 1)[0]
        # Drop image refs (`backimage`, `backimage2`, `frontstart`, …)
        # uniformly by prefix-rstrip-digits -- variant-2 cousins differ
        # only by a trailing `2` we want to ignore.
        prefix_no_variant = prefix.rstrip("0123456789")
        if prefix_no_variant in _BRIDGE_PORT_DROP_PREFIXES:
            continue
        if kl in ("icon", "cursor"):
            continue
        if kl in scalars and not _INDEX_RE.search(k):
            kwargs[kl] = _coerce(v)

    return Bridge(**kwargs)


def _harvest_indexed(entries: list[tuple[str, str]], base: str) -> list[str]:
    """Gather `base[N]=…` values sorted by N.  Case-insensitive on key."""
    prefix = f"{base.lower()}["
    indexed: list[tuple[int, str]] = []
    for k, v in entries:
        if not (k.lower().startswith(prefix) and k.endswith("]")):
            continue
        try:
            indexed.append((int(k[len(prefix):-1]), v))
        except ValueError:
            continue
    return [v for _, v in sorted(indexed)]


def seed_python(spec: Any, *, indent: str = "    ") -> str:
    """Render a SPEC dataclass (`Vehicle` or `Way`) as paste-ready
    `<ClassName>(...)` source.

    Only fields that differ from their defaults are emitted — so a
    seeded SPEC pastes cleanly into a bake script without 40 lines
    of `=None` noise — and one field per line for legibility at
    ~30 fields per asset.  Dataclass `__repr__` would include every
    field as a single oneliner; this is the human shape.
    """
    parts: list[str] = []
    for f in fields(spec):
        v = getattr(spec, f.name)
        if f.default is not MISSING:
            default = f.default
        elif f.default_factory is not MISSING:
            default = f.default_factory()
        else:
            default = object()  # required field, never matches
        if v != default:
            parts.append(f"{indent}{f.name}={v!r},")
    return f"{type(spec).__name__}(\n" + "\n".join(parts) + "\n)"


def _coerce(value: str) -> str | int | float:
    """Parse a dat scalar into the narrowest Python type."""
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value
