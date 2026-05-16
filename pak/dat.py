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
schema) and calls `emit_vehicle` per output.  `Vehicle.__init__`
catches typos at construction; `emit_vehicle` writes the dat
with image refs pointing at the atlas baked alongside.

`Vehicle` fields cover both hex-engine and Simutrans-Extended
schema.  `emit_vehicle` writes all set fields — the hex engine
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
from pathlib import Path
from typing import Any

from pak.way import HEX_ENTRIES


_INDEX_RE = re.compile(r"\[([^\]]*)\]")
_TERMINATOR_RE = re.compile(r"^-+\s*$")

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


def _list_field(*, dat_key: str | None = None) -> Any:
    """Indexed-list field with an optional dat-key override.

    Use `_list_field()` for fields whose dat key matches the
    Python name (`comfort` -> `comfort[N]`).  Pass `dat_key=` to
    remap (`payload_by_class` -> `payload[N]`).
    """
    meta = {"dat_key": dat_key} if dat_key else {}
    return field(default_factory=list, metadata=meta)


@dataclass
class Vehicle:
    """A `obj=vehicle` definition.  Fields cover both hex-engine
    and Simutrans-Extended schema; `emit_vehicle` writes all set
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


_VEHICLE_FIELDS_SCALAR: tuple[str, ...] = tuple(
    f.name for f in fields(Vehicle) if f.default_factory is MISSING
)
# (field_name, dat_key) pairs for indexed-list emission.
_VEHICLE_FIELDS_LIST: tuple[tuple[str, str], ...] = tuple(
    (f.name, f.metadata.get("dat_key", f.name))
    for f in fields(Vehicle)
    if f.default_factory is not MISSING
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


_WAY_FIELDS_SCALAR: tuple[str, ...] = tuple(f.name for f in fields(Way))


@dataclass
class Building:
    """A `obj=building` definition.  Fields cover the hex-engine schema
    (`descriptor/writer/building_writer.cc`) plus the Simutrans-Extended
    demand / employment / class-proportion keys upstream Britain dats
    carry.  Image refs are derived from the baked atlas at emit time;
    SPECs hold gameplay data only.

    Footprint is `(dims_x, dims_y)` tiles with `layouts` rotation
    variants.  `layouts=None` (the default) means "let the engine pick" —
    1 for a square footprint, 2 for rectangular — and `emit_building`
    fills the implied value in `dims=X,Y,Z` so a round-tripped dat
    carries the same shape regardless of how the source dat wrote it.

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

    # Footprint — emitted together as `dims=X,Y,Z`.
    dims_x: int = 1
    dims_y: int = 1
    layouts: int | None = None  # None → engine default per layouts_default()

    # Vertical stack — number of `backimage[…][height][…]` levels the
    # engine paints, each shifted up by `raster_width` px (one full
    # cell).  Single-cell buildings keep `heights=1`; a 2-storey
    # detached house typically needs 2 since its model is too tall to
    # fit one hex cell at the pakset calibration.  See CLAUDE.md ->
    # "Building-bake architecture" for the world-z per height-level.
    heights: int = 1

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
# order).  Phase and season default to 0 for an asset bake without
# animation and single-season; revisit when a bake script first needs
# either of those.  Height varies per (l,y,x,h) cell.
_BUILDING_IMAGE_PHASE = 0
_BUILDING_IMAGE_SEASON = 0


# dims_x / dims_y / layouts emit together as a single `dims=X,Y,Z`
# line, not as plain `name=value` per field.  `heights` is implicit
# in the per-(l,y,x,h) backimage refs — the engine reads height
# levels until the next index returns no key — so it doesn't get a
# scalar key either.  All four filtered out of the generic emit.
_BUILDING_FIELDS_SCALAR: tuple[str, ...] = tuple(
    f.name for f in fields(Building)
    if f.default_factory is MISSING
    and f.name not in ("dims_x", "dims_y", "layouts", "heights")
)
_BUILDING_FIELDS_LIST: tuple[tuple[str, str], ...] = tuple(
    (f.name, f.metadata.get("dat_key", f.name))
    for f in fields(Building)
    if f.default_factory is not MISSING
)


def iter_building_cells(b: Building):
    """Yield `(layout, y, x, height)` quadruples in canonical emit order.

    For each layout in `[0, layouts)`, iterate `(y, x)` matching the
    engine's loops in `building_writer.cc`: even layouts iterate
    `y in [0, size.y), x in [0, size.x)`; odd layouts swap to
    `y in [0, size.x), x in [0, size.y)`.  Then inner-most, iterate
    `height in [0, heights)` — height stacking, painted by the engine
    at `ypos -= raster_width` per level (see `obj/gebaeude.cc`).
    The engine reads height levels by incrementing until the key
    returns empty, so heights is implicit in the emitted refs (no
    `heights=N` scalar).  Bake scripts use this to drive per-cell
    renders; emit_building uses it to wire image refs."""
    layouts = b.layouts if b.layouts is not None else layouts_default(b.dims_x, b.dims_y)
    for l in range(layouts):
        if l & 1:
            yh, xw = b.dims_x, b.dims_y
        else:
            yh, xw = b.dims_y, b.dims_x
        for y in range(yh):
            for x in range(xw):
                for h in range(b.heights):
                    yield l, y, x, h


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
        objects[-1].append((key.strip(), value.strip()))
    if not objects[-1]:
        objects.pop()
    return objects


def emit_vehicle(vehicle: Vehicle, *, out_dir: Path, basename: str) -> Path:
    """Write `<out_dir>/<basename>.dat` from a Vehicle.

    Emits every set field on the Vehicle.  Image refs point at
    `./<basename>.0.<col>` for col in 0..7, matching the single-row
    hex atlas baked alongside (PNG must live at
    `<out_dir>/<basename>.png`).  Returns the dat path.
    """
    lines: list[str] = ["obj=vehicle"]
    for name in _VEHICLE_FIELDS_SCALAR:
        v = getattr(vehicle, name)
        if v is not None:
            lines.append(f"{name}={v}")
    for attr, dat_key in _VEHICLE_FIELDS_LIST:
        for i, v in enumerate(getattr(vehicle, attr)):
            lines.append(f"{dat_key}[{i}]={v}")
    for col, facing in enumerate(_HEX_FACINGS):
        lines.append(f"EmptyImage[{facing}]=./{basename}.0.{col}")
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


def emit_building(b: Building, *, out_dir: Path, basename: str) -> Path:
    """Write `<out_dir>/<basename>.dat` from a Building.

    Emits set scalars, then `dims=X,Y,Z` (with layouts filled in from
    `layouts_default` when the SPEC left it `None`), then indexed
    lists, then `backimage[l][y][x][h][0][0]=./<basename>.<row>.<col>`
    per cell — `row = l*heights + h` (layout-major, height inner),
    `col = y*w + x` within the layout's engine-determined bounds
    (see `iter_building_cells`).  The PNG must live at
    `<out_dir>/<basename>.png` and match that layout exactly — drift
    surfaces in-engine as the wrong sprite per tile/level.

    FrontImage, animation phase and season variants are not yet
    emitted; revisit when a bake script needs any of them (occlusion-
    correct foreground, animated effects, snowed-over winters).
    Returns the dat path.
    """
    lines: list[str] = ["obj=building"]
    for name in _BUILDING_FIELDS_SCALAR:
        v = getattr(b, name)
        if v is not None:
            lines.append(f"{name}={v}")
    layouts = b.layouts if b.layouts is not None else layouts_default(b.dims_x, b.dims_y)
    lines.append(f"dims={b.dims_x},{b.dims_y},{layouts}")
    for attr, dat_key in _BUILDING_FIELDS_LIST:
        for i, v in enumerate(getattr(b, attr)):
            lines.append(f"{dat_key}[{i}]={v}")

    for l, y, x, h in iter_building_cells(b):
        w = b.dims_y if l & 1 else b.dims_x
        col = y * w + x
        row = l * b.heights + h
        lines.append(
            f"backimage[{l}][{y}][{x}][{h}]"
            f"[{_BUILDING_IMAGE_PHASE}]"
            f"[{_BUILDING_IMAGE_SEASON}]"
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
    sets plus the engine's `dims=X,Y[,Z]` triple (split out to
    `dims_x`, `dims_y`, `layouts`).  Scans `backimage[…][height][…]`
    refs to set `heights = max(height) + 1` so a seeded SPEC carries
    the upstream's vertical-stack count.  Image-ref strings (`backimage[…]
    `=…`, `frontimage[…]=…`) are dropped — see `_BUILDING_PORT_DROP`.

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
    for k, v in object_entries:
        kl = k.lower()
        # Image refs: parse out the height index before dropping the
        # value, so we can set `heights` from the upstream stack depth.
        prefix = kl.split("[", 1)[0]
        if prefix in _BUILDING_PORT_DROP:
            # backimage[L][Y][X][H][P][S] — height is index 3
            indices = [s.rstrip("]") for s in kl.split("[")[1:]]
            if len(indices) >= 4:
                try:
                    max_height = max(max_height, int(indices[3]))
                except ValueError:
                    pass
            continue
        if kl == "dims":
            ints = [int(s.strip()) for s in v.split(",")]
            if len(ints) >= 1:
                kwargs["dims_x"] = ints[0]
            if len(ints) >= 2:
                kwargs["dims_y"] = ints[1]
            if len(ints) >= 3:
                kwargs["layouts"] = ints[2]
            continue
        if kl in scalars and not _INDEX_RE.search(k):
            kwargs[kl] = _coerce(v)

    for base, dest_field in _BUILDING_INDEXED_HARVEST_TO_FIELD.items():
        values = _harvest_indexed(object_entries, base)
        if values:
            kwargs[dest_field] = [_coerce(v) for v in values]

    if max_height > 0:
        kwargs["heights"] = max_height + 1

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
