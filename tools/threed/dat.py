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
"""

from __future__ import annotations

import re
from dataclasses import MISSING, dataclass, field, fields
from pathlib import Path
from typing import Any


_INDEX_RE = re.compile(r"\[([^\]]*)\]")
_TERMINATOR_RE = re.compile(r"^-+\s*$")

# Single-row 8-facing atlas; column i corresponds to facings[i]
# in render.py / viewpoints.py HEX_VIEWPOINT.  Match exactly or
# the engine renders the wrong sprite per direction.
_HEX_FACINGS: tuple[str, ...] = ("S", "SW", "W", "NW", "N", "NE", "E", "SE")


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
    `./<basename>.col.0` for col in 0..7, matching the single-row
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
        lines.append(f"EmptyImage[{facing}]=./{basename}.{col}.0")
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


def seed_python(vehicle: Vehicle, *, indent: str = "    ") -> str:
    """Render a `Vehicle` as paste-ready `Vehicle(...)` source.

    Only fields that differ from their defaults are emitted — so a
    seeded Vehicle pastes cleanly into a bake script without 40
    lines of `=None` noise — and one field per line for legibility
    at ~30 fields per asset.  Dataclass `__repr__` would include
    every field as a single oneliner; this is the human shape.
    """
    parts: list[str] = []
    for f in fields(vehicle):
        v = getattr(vehicle, f.name)
        if f.default is not MISSING:
            default = f.default
        elif f.default_factory is not MISSING:
            default = f.default_factory()
        else:
            default = object()  # required field, never matches
        if v != default:
            parts.append(f"{indent}{f.name}={v!r},")
    return "Vehicle(\n" + "\n".join(parts) + "\n)"


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
