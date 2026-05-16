"""Re-emit every vehicle bake unit's `.dat` from its `SPEC`.

Companion to `make bake-grounds`: where that re-runs the parametric
ground bakers (numpy-fast, byte-identical PNGs in seconds), this
re-emits only the dat side of vehicle bake units — no Blender, no
render — so CI can catch dat drift between the SPEC in the bake
script and the committed `.dat` sibling without a per-asset Cycles
bake.

Bake-unit discovery is shared with `pak.fetch_wavs` via
`pak.bake_units` (see CLAUDE.md -> "Bake units and per-asset
layout").  A script with `SPECS: list[Vehicle]` (shared-sprite
variants — e.g. `air/dragon_rapide.py`) emits a combined multi-
object dat via `emit_vehicles`; otherwise `SPEC: Vehicle | Way |
Building` drives the single-object emitters.  A script with
neither raises rather than silently skipping.
"""
from __future__ import annotations

from pathlib import Path

from pak import REPO_ROOT
from pak.bake_units import discover, import_script, specs_of
from pak.dat import (
    Building, Vehicle, Way, emit_building, emit_vehicles, emit_way,
)


def _reemit(script: Path) -> Path:
    specs = specs_of(import_script(script))
    out_dir, basename = script.parent, script.stem
    if specs and all(isinstance(s, Vehicle) for s in specs):
        return emit_vehicles(specs, out_dir=out_dir, basename=basename)
    if len(specs) == 1 and isinstance(specs[0], Way):
        return emit_way(specs[0], out_dir=out_dir, basename=basename)
    if len(specs) == 1 and isinstance(specs[0], Building):
        return emit_building(specs[0], out_dir=out_dir, basename=basename)
    rel = script.relative_to(REPO_ROOT)
    raise RuntimeError(
        f"{rel} has no usable `SPEC` / `SPECS` for reemit"
    )


def main() -> None:
    for script in discover():
        out = _reemit(script)
        print(f"wrote {out.relative_to(REPO_ROOT)}", flush=True)


if __name__ == "__main__":
    main()
