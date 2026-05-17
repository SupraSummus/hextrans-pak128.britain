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
from pak.materials import Material, seed_python

_TEXCO_NAME = {TEXCO_GLOB: "GLOB", TEXCO_ORCO: "ORCO", TEXCO_UV: "UV"}


def materials_from_blend(blend_path: Path) -> dict[str, Material]:
    """Slot-data -> per-material `Material` description.  Picks the
    first IMAGE slot if any, else the first CLOUDS/NOISE slot, else
    omits the material (renders flat-diffuse)."""
    raw = extract(blend_path)
    out: dict[str, Material] = {}
    for name, ms in raw.items():
        image_slot = None
        procedural = False
        for s in ms.slots:
            if s.tex_type == "IMAGE" and s.image_name:
                if image_slot is None:
                    image_slot = s
            elif s.tex_type in ("CLOUDS", "NOISE"):
                procedural = True
        if image_slot is not None:
            texco = _TEXCO_NAME.get(image_slot.texco, "GLOB")
            out[name] = Material(
                image=image_slot.image_name,
                texco=texco,
                size=tuple(round(v, 4) for v in image_slot.size),
                ofs=tuple(round(v, 4) for v in image_slot.ofs),
            )
        elif procedural:
            out[name] = Material(noise=True)
    return out


def _main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <blend_path>")
    mats = materials_from_blend(Path(sys.argv[1]))
    print(seed_python(mats))


if __name__ == "__main__":
    _main()
