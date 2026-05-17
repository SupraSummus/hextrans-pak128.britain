"""Per-material rendering description for the BI-substitute pipeline.

Britain's blends were authored under Blender Internal (2.42 / 2.48
saves); Blender 4.0's loader drops BI's `material.texture_slots`
silently, so a runtime re-render has nothing to bind textures with
beyond the diffuse colour and image data blocks.  `pak.blend_slots`
parses the slot pointers out of the .blend binary directly to
recover what BI saw, but that's a heavyweight one-shot operation
and the slot data sometimes needs hand-tuning (BI authoring quirks
that have to be lived with by overriding per-asset).

The shape that survived for ways -- per-asset `MATERIALS = {...}`
declared inline next to the SPEC, serialised to JSON on the
subprocess command line, applied in the Blender bake driver --
generalises here.  Per-building `MATERIALS` carries one
`Material` per blend material name, declaring whether it's image-
textured (and which image, at what BI texco / size / ofs) or
procedural noise.  Materials missing from the dict render flat-
diffuse, matching Blender 4.0's `use_nodes=False` auto-conversion.

Seeded once by `python3 -m pak.extract_materials <blend>`; review
and paste into the bake script.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any

_TEXCO_VALID = ("GLOB", "ORCO", "UV")


@dataclass
class Material:
    """One blend material's rendering description.

    Either `image` is set (image-textured, sampled at `size` cycles
    per axis under the named BI texco) or `noise=True` (CLOUDS/NOISE
    procedural substitute around the material's diffuse colour) --
    not both; not neither.  An empty Material would just request flat
    diffuse, which is what happens automatically when a name is
    omitted from `MATERIALS`, so the empty form is also rejected to
    avoid two ways to spell the same thing.

    `texco`: BI projection mode the slot was authored for.
        "GLOB" -- world coords (cycles per blend unit = size_axis).
            Sampled at render time via the `blend_world_pos` vertex
            attribute populated by `_bake_world_into_meshes`, so the
            texture stays pinned to the blend frame across per-facing
            model rotation.
        "ORCO" / "UV" -- object-local.  Substituted by
            `TexCoord.Generated` (bbox-normalised); cycles per
            bbox axis = size_axis.
    `size`: per-axis multiplier from the BI MTex slot.
    `ofs`: per-axis offset.  Britain blends almost always 0.
    """
    image: str | None = None
    texco: str = "GLOB"
    size: tuple[float, float, float] = (1.0, 1.0, 1.0)
    ofs: tuple[float, float, float] = (0.0, 0.0, 0.0)
    noise: bool = False

    def __post_init__(self):
        if self.image is None and not self.noise:
            raise ValueError(
                "Material needs either image=... or noise=True; omit "
                "the material name from MATERIALS to render flat-diffuse"
            )
        if self.image is not None and self.noise:
            raise ValueError(
                f"Material(image={self.image!r}) cannot also be noise=True"
            )
        if self.texco not in _TEXCO_VALID:
            raise ValueError(
                f"unknown texco {self.texco!r}; valid: {_TEXCO_VALID}"
            )


_DEFAULTS = {f.name: f.default for f in fields(Material)}


def _non_default_items(m: Material):
    """Yield `(name, value)` for fields whose value differs from the
    dataclass default.  Used by both wire form (`to_jsonable`) and
    paste form (`seed_python`) -- defaults are stable so the dropped
    fields round-trip back through the constructor."""
    for f in fields(Material):
        v = getattr(m, f.name)
        if v != _DEFAULTS[f.name]:
            yield f.name, v


def to_jsonable(materials: dict[str, Material]) -> dict[str, dict[str, Any]]:
    """Serialise `MATERIALS` for subprocess passing.  Default-valued
    fields are dropped to keep the wire form short; tuples come back
    as lists across JSON, which is fine -- `from_jsonable` rebuilds
    the dataclass."""
    return {name: dict(_non_default_items(m)) for name, m in materials.items()}


def from_jsonable(data: dict[str, dict[str, Any]]) -> dict[str, Material]:
    """Rebuild `MATERIALS` after JSON transit.  Tuples in JSON come
    through as lists; tuple-fields get re-tupled so equality with
    in-process Material instances holds."""
    return {
        name: Material(**{
            k: tuple(v) if isinstance(v, list) else v
            for k, v in d.items()
        })
        for name, d in data.items()
    }


def seed_python(materials: dict[str, Material]) -> str:
    """Paste-ready Python source for a `MATERIALS = {...}` dict.

    Emits only non-default Material fields, matching `pak.dat.seed_python`'s
    convention for vehicles -- full dataclass reprs are unreadable, and
    the dict is the authoritative source once pasted."""
    lines = ["MATERIALS = {"]
    for name, m in materials.items():
        parts = [f"{k}={v!r}" for k, v in _non_default_items(m)]
        lines.append(f"    {name!r}: Material({', '.join(parts)}),")
    lines.append("}")
    return "\n".join(lines)


