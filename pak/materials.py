"""Per-material rendering description for the BI-substitute pipeline.

Britain's blends were authored under Blender Internal (2.42 / 2.48
saves); Blender 4.0's loader drops BI's `material.texture_slots`
silently, so a runtime re-render has nothing to bind textures with
beyond the diffuse colour and image data blocks.  `pak.blend_slots`
parses the slot pointers out of the .blend binary directly to
recover what BI saw, but that's a heavyweight one-shot operation
and the slot data sometimes needs hand-tuning (BI authoring quirks
that have to be lived with by overriding per-asset).

The shape that survived for ways -- a per-asset `materials={...}`
dict declared inline on the SPEC, serialised to JSON on the
subprocess command line, applied in the Blender bake driver --
generalises here.  Each building's `Building.materials` (and
each way's `Way.materials`) carries one `Material` per blend
material name, declaring whether it's image-textured (and which
image, at what BI texco / size / ofs) or procedural noise.
Materials missing from the dict render flat-diffuse, matching
Blender 4.0's `use_nodes=False` auto-conversion.

Seeded once by `python3 -m pak.extract_materials <blend>`
(emits a `MATERIALS = {...}` block ready to paste into the SPEC's
`materials=` field); review before pasting.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any

_TEXCO_VALID = ("GLOB", "ORCO", "UV")

# BI's MTex.blendtype enum mapped to Blender's MixRGB shader node
# blend_type names.  The full BI enum is wider; this covers what the
# Britain blends actually use (Mix, Multiply, Add — every snow blend
# we inspected sits at Mix).
_BLEND_BI_TO_SHADER = {
    "MIX":        "MIX",
    "MULTIPLY":   "MULTIPLY",
    "ADD":        "ADD",
    "SUBTRACT":   "SUBTRACT",
    "SCREEN":     "SCREEN",
    "DIVIDE":     "DIVIDE",
    "DIFFERENCE": "DIFFERENCE",
}
_PROC_VALID = ("CLOUDS", "NOISE", "MUSGRAVE", "STUCCI", "WOOD")


@dataclass
class Slot:
    """One BI texture slot's rendering description.

    Mirrors `pak.blend_slots.TextureSlot` but in the Material spec form
    that survives JSON round-trip and lives in a SPEC's
    `materials={...}` dict.  Either `image` is set (image-textured) or
    `procedural` is set (one of `_PROC_VALID`); not both.

    `blend` is the BI slot blend mode mapped onto Blender's MixRGB
    `blend_type` (see `_BLEND_BI_TO_SHADER`).  `fac` is the BI slot
    influence factor in [0, 1] — every Britain slot extracted to date
    ships at 1.0 (full influence).

    `color` carries the per-slot RGB BI uses as the procedural slot's
    constant output when neither a colour band nor an stype=COLOR
    texture supplies RGB.  Hedge's CLOUDS slot ships `(0.10, 0.06,
    0.04)` (dark brown dirt-tint over a green diffuse); MainColour1's
    ships `(0.60, 0.60, 0.60)` (mid-gray); etc.  Read from MTex.r/g/b.
    Meaningful only for `procedural=` slots; on `image=` slots it
    carries the magenta-default sentinel and is ignored.

    `color_band`, when set, replaces the constant `color` with an
    intensity-mapped gradient (each entry `(pos, r, g, b, a)`).  Read
    from the Tex's ColorBand when `Tex.flag & TEX_COLORBAND` is set —
    rare in the Britain pak (handful of materials) but the BI-faithful
    path when present.  Currently consumed for procedural slots only;
    extending to IMAGE slots (where BI overrides the image pixel with
    band-of-intensity) is open if a per-asset audit surfaces one."""
    image: str | None = None
    procedural: str | None = None
    texco: str = "GLOB"
    size: tuple[float, float, float] = (1.0, 1.0, 1.0)
    ofs: tuple[float, float, float] = (0.0, 0.0, 0.0)
    blend: str = "MIX"
    fac: float = 1.0
    color: tuple[float, float, float] = (1.0, 1.0, 1.0)
    color_band: list[tuple[float, float, float, float, float]] | None = None

    def __post_init__(self):
        if (self.image is None) == (self.procedural is None):
            raise ValueError(
                "Slot needs exactly one of image= or procedural=; "
                f"got image={self.image!r} procedural={self.procedural!r}"
            )
        if self.texco not in _TEXCO_VALID:
            raise ValueError(
                f"unknown texco {self.texco!r}; valid: {_TEXCO_VALID}"
            )
        if self.procedural is not None and self.procedural not in _PROC_VALID:
            raise ValueError(
                f"unknown procedural {self.procedural!r}; valid: {_PROC_VALID}"
            )
        if self.blend not in _BLEND_BI_TO_SHADER:
            raise ValueError(
                f"unknown blend mode {self.blend!r}; valid: "
                f"{tuple(_BLEND_BI_TO_SHADER)}"
            )


@dataclass
class Material:
    """One blend material's rendering description.

    Three forms, exactly one applies:

    1. `slots=[Slot(...), ...]` — full BI slot stack, composed in order
       (see `Slot`).  The BI-faithful form, seeded by
       `pak.extract_materials`.  Procedural slots emit a constant
       `Slot.color` (the per-slot MTex RGB) or, when the Tex carries
       an active `TEX_COLORBAND`, the band mapped through the noise
       intensity — same data the BI renderer reads at run time.
    2. `image=...` (+ optional `size`, `ofs`, `texco`) — legacy single
       image slot, mixed `image × diffuse` over the BSDF.  Equivalent
       to a one-Slot list at Mix fac=1.0 but with the extra diffuse
       multiply baked in (the heuristic predates multi-slot support
       and stays for back-compat).
    3. `noise=True` — single procedural CLOUDS slot with a noise band
       around the .blend's diffuse (or `color=` override).  Cheap
       substitute for the BI procedural; not the same shader as a
       slots-form CLOUDS slot (which mixes `(intensity, intensity,
       intensity)` over the running base).

    `color`, when set, replaces the .blend's authored `diffuse_color`
    as the multiplier (single-image form) or the noise band's centre
    (single-noise form), or the slot stack's base (slots form).  Use
    case: BI's default CLOUDS slot paints white-over-diffuse at
    fac=1.0; without the Tex datablock parsed our extraction sees
    only the material diffuse, so the snow blend's Brick / Roof come
    out reddish-brown instead of white snow.  Pinning `color=(1,1,1)`
    or similar recovers the upstream look.  Per-asset override; the
    proper fix is Tex datablock colour bands.

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
    # Diffuse-colour override.  When set, the renderer uses this in
    # place of the .blend's authored `material.diffuse_color` as the
    # noise band's centre (for `noise=True`) or the multiplied tint
    # (for image-textured slots).  Use case: BI's default CLOUDS slot
    # paints the surface `white * noise_intensity` (because the
    # texture's default colour is white at fac=1.0) regardless of the
    # material's diffuse — our substitute can't infer that, so the
    # snow blend's Brick/Roof come out reddish-brown/grey instead of
    # white snow.  Pinning `color=(1,1,1)` recovers the upstream look.
    color: tuple[float, float, float] | None = None
    # Full BI slot stack.  When set, takes precedence over `image=` /
    # `noise=` — the renderer composites every slot in order over the
    # material's authored diffuse (or `color=` override) using each
    # slot's blend mode and fac.  This is the BI-faithful path; the
    # single-slot fields above remain for back-compat and for hand-
    # written overrides that only need the first slot.  Seeded by
    # `pak.extract_materials`.
    slots: list[Slot] | None = None

    def __post_init__(self):
        if self.slots is not None:
            if self.image is not None or self.noise:
                raise ValueError(
                    "Material(slots=...) cannot combine with image= or "
                    "noise= — the slot list is the authoritative source"
                )
            return
        if self.image is None and not self.noise:
            raise ValueError(
                "Material needs either image=... or noise=True or slots=[...]; "
                "omit the material name from the SPEC's materials= dict to "
                "render flat-diffuse"
            )
        if self.image is not None and self.noise:
            raise ValueError(
                f"Material(image={self.image!r}) cannot also be noise=True"
            )
        if self.texco not in _TEXCO_VALID:
            raise ValueError(
                f"unknown texco {self.texco!r}; valid: {_TEXCO_VALID}"
            )


@dataclass
class Lighting:
    """Per-asset world + sun lighting overrides.

    The EEVEE building viewpoint defaults (world ambient grey 0.30, sun
    energy scale 2.0 over the .blend's BI-authored 0.028, sun elevation
    30°, sun azimuth offset -90° from camera) were grid-searched
    against the heuristic materials path on one pilot; under the slot-
    form / hybrid path and the alpha-premultiplied blurred dRGB metric
    the optimum shifts per asset.  Set `lighting=Lighting(...)` on the
    SPEC to override.  Buildings without a `lighting=` value fall back
    to the defaults baked into `pak.viewpoints.building_*_viewpoint`
    and `pak.render._configure_eevee`.

    `world_ambient`: replaces `scn.world.color`; modern EEVEE uses
        this as the constant ambient term BI's `world.amb` field
        played in the legacy pipeline.
    `sun_energy_scale`: replaces `viewpoints._BI_TO_EEVEE_SUN_SCALE`;
        multiplied against the .blend's authored sun energy (BI's
        0.028) to compensate for BI vs EEVEE energy unit conventions.
    `sun_elev_deg`, `sun_az_offset_deg`: replace the defaults of
        `viewpoints.sun_rotation_for_camera`."""
    world_ambient: tuple[float, float, float] | None = None
    sun_energy_scale: float | None = None
    sun_elev_deg: float | None = None
    sun_az_offset_deg: float | None = None

    def to_jsonable(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_jsonable(cls, d: dict[str, Any]) -> Lighting:
        kw: dict[str, Any] = {}
        for k, v in d.items():
            kw[k] = tuple(v) if isinstance(v, list) else v
        return cls(**kw)


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


_SLOT_DEFAULTS = {f.name: f.default for f in fields(Slot)}


def _slot_to_jsonable(s: Slot) -> dict[str, Any]:
    return {k: v for k, v in s.__dict__.items()
            if v != _SLOT_DEFAULTS.get(k)}


def _slot_from_jsonable(d: dict[str, Any]) -> Slot:
    kw: dict[str, Any] = {}
    for k, v in d.items():
        if k == "color_band":
            kw[k] = [tuple(stop) for stop in v]
        elif isinstance(v, list):
            kw[k] = tuple(v)
        else:
            kw[k] = v
    return Slot(**kw)


def to_jsonable(materials: dict[str, Material]) -> dict[str, dict[str, Any]]:
    """Serialise `MATERIALS` for subprocess passing.  Default-valued
    fields are dropped to keep the wire form short; tuples come back
    as lists across JSON, which is fine -- `from_jsonable` rebuilds
    the dataclass.  Slots serialise recursively."""
    out: dict[str, dict[str, Any]] = {}
    for name, m in materials.items():
        d = dict(_non_default_items(m))
        if "slots" in d:
            d["slots"] = [_slot_to_jsonable(s) for s in m.slots]
        out[name] = d
    return out


def from_jsonable(data: dict[str, dict[str, Any]]) -> dict[str, Material]:
    """Rebuild `MATERIALS` after JSON transit.  Tuples in JSON come
    through as lists; tuple-fields get re-tupled so equality with
    in-process Material instances holds."""
    out: dict[str, Material] = {}
    for name, d in data.items():
        kw: dict[str, Any] = {}
        for k, v in d.items():
            if k == "slots":
                kw["slots"] = [_slot_from_jsonable(sd) for sd in v]
            elif isinstance(v, list):
                kw[k] = tuple(v)
            else:
                kw[k] = v
        out[name] = Material(**kw)
    return out


def _slot_repr(s: Slot) -> str:
    parts = [f"{k}={v!r}" for k, v in s.__dict__.items()
             if v != _SLOT_DEFAULTS.get(k)]
    return f"Slot({', '.join(parts)})"


def seed_python(materials: dict[str, Material]) -> str:
    """Paste-ready Python source for a `MATERIALS = {...}` dict.

    Emits only non-default Material fields, matching `pak.dat.seed_python`'s
    convention for vehicles -- full dataclass reprs are unreadable, and
    the dict is the authoritative source once pasted."""
    lines = ["MATERIALS = {"]
    for name, m in materials.items():
        if m.slots is not None:
            slot_reprs = ",\n        ".join(_slot_repr(s) for s in m.slots)
            extras = [f"{k}={v!r}" for k, v in _non_default_items(m)
                      if k != "slots"]
            extras_s = ", " + ", ".join(extras) if extras else ""
            lines.append(f"    {name!r}: Material(slots=[")
            lines.append(f"        {slot_reprs},")
            lines.append(f"    ]{extras_s}),")
        else:
            parts = [f"{k}={v!r}" for k, v in _non_default_items(m)]
            lines.append(f"    {name!r}: Material({', '.join(parts)}),")
    lines.append("}")
    return "\n".join(lines)


