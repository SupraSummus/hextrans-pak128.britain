"""Re-emit every vehicle bake unit's `.dat` from its `SPEC`.

Companion to `make bake-grounds`: where that re-runs the parametric
ground bakers (numpy-fast, byte-identical PNGs in seconds), this
re-emits only the dat side of vehicle bake units — no Blender, no
render — so CI can catch dat drift between the SPEC in the bake
script and the committed `.dat` sibling without a per-asset Cycles
bake.

Bake-unit discovery is shared with `pak.fetch_wavs` via
`pak.bake_units` (see CLAUDE.md -> "Bake units and per-asset
layout").  A bake-unit script without a `SPEC: Vehicle` raises —
the multi-object pattern would need its own re-emit hook; refuse to
silently skip.
"""
from __future__ import annotations

from pathlib import Path

from pak import REPO_ROOT
from pak.bake_units import discover, import_script
from pak.dat import Vehicle, emit_vehicle


def _reemit(script: Path) -> Path:
    spec = getattr(import_script(script), "SPEC", None)
    if not isinstance(spec, Vehicle):
        rel = script.relative_to(REPO_ROOT)
        raise RuntimeError(
            f"{rel} has no `SPEC: Vehicle` — multi-object bake units "
            f"need their own re-emit hook"
        )
    return emit_vehicle(spec, out_dir=script.parent, basename=script.stem)


def main() -> None:
    for script in discover():
        out = _reemit(script)
        print(f"wrote {out.relative_to(REPO_ROOT)}", flush=True)


if __name__ == "__main__":
    main()
