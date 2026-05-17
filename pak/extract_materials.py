"""One-shot seeder: print paste-ready `MATERIALS = {...}` from a blend.

Reads the BI MTex slot data via `pak.blend_slots` (which parses the
.blend binary directly because Blender 4.0 dropped the
`material.texture_slots` API), collapses each material to its
authoritative first IMAGE slot or fallback procedural slot, and
emits the inline Python source to paste next to `SPEC` in the
bake script.

Run as::

    python3 -m pak.extract_materials \\
        .cache/blends/<sha>/citybuildings/<blend>.blend

After paste, hand-edit -- JP's authoring quirks sometimes need
overriding (e.g. a material whose BI slot points at the wrong
image, or a procedural slot whose noise frequency wants tweaking).
The dict in the bake script is the authoritative source once
pasted; this tool only seeds it.
"""
from __future__ import annotations

import sys
from pathlib import Path

from pak.blend_slots import TEXCO_GLOB, TEXCO_ORCO, TEXCO_UV, extract
from pak.materials import Material, Slot, seed_python

_TEXCO_NAME = {TEXCO_GLOB: "GLOB", TEXCO_ORCO: "ORCO", TEXCO_UV: "UV"}
# BI MTex.blendtype enum -> Blender shader-node MixRGB blend_type.
_BLEND_NAME = {
    0: "MIX", 1: "MULTIPLY", 2: "ADD", 3: "SUBTRACT",
    4: "SCREEN", 5: "DIVIDE", 6: "DIFFERENCE",
}


def materials_from_blend(blend_path: Path) -> dict[str, Material]:
    """Slot-data -> per-material `Material` description carrying the
    full slot stack BI composites at render time.

    Multi-slot is the BI-faithful path — every Britain material we've
    inspected uses 1-5 slots at Mix fac=1.0 each, and dropping all but
    the first (the previous one-shot seeder) collapses what BI builds
    additively into a single-slot multiply, losing the texture
    variation upstream's PNGs show.  See `pak.diag_per_material --all`.

    Materials with no usable slot are omitted (the renderer falls back
    to flat diffuse for unlisted entries).  STUCCI / WOOD / OTHER tex
    types are skipped — Britain blends rarely use them, and our
    procedural substitute set is CLOUDS / NOISE / MUSGRAVE.  Fill in
    later if a real consumer surfaces them."""
    raw = extract(blend_path)
    out: dict[str, Material] = {}
    for name, ms in raw.items():
        slots: list[Slot] = []
        for s in ms.slots:
            blend_name = _BLEND_NAME.get(s.blendtype, "MIX")
            texco = _TEXCO_NAME.get(s.texco, "GLOB")
            if s.tex_type == "IMAGE" and s.image_name:
                slots.append(Slot(
                    image=s.image_name,
                    texco=texco,
                    size=tuple(round(v, 4) for v in s.size),
                    ofs=tuple(round(v, 4) for v in s.ofs),
                    blend=blend_name,
                    fac=round(s.colfac, 3),
                ))
            elif s.tex_type in ("CLOUDS", "NOISE", "MUSGRAVE"):
                slots.append(Slot(
                    procedural=s.tex_type,
                    texco=texco,
                    size=tuple(round(v, 4) for v in s.size),
                    ofs=tuple(round(v, 4) for v in s.ofs),
                    blend=blend_name,
                    fac=round(s.colfac, 3),
                ))
        if slots:
            out[name] = Material(slots=slots)
    return out


def _main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <blend_path>")
    mats = materials_from_blend(Path(sys.argv[1]))
    print(seed_python(mats))


if __name__ == "__main__":
    _main()
