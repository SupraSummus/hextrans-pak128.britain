"""Re-emit every vehicle bake unit's `.dat` from its `SPEC`.

Companion to `make bake-grounds`: where that re-runs the parametric
ground bakers (numpy-fast, byte-identical PNGs in seconds), this
re-emits only the dat side of vehicle bake units — no Blender, no
render — so CI can catch dat drift between the SPEC in the bake
script and the committed `.dat` sibling without a per-asset Cycles
bake.

Discovery: any `*.py` under the repo (excluding `tools/`, `tests/`,
`grounds/`, `simutranslator/`) with both a `.dat` and a `.png`
sibling sharing its stem.  Each is imported as a module; if it
exposes `SPEC: Vehicle`, `emit_vehicle` rewrites
`<dir>/<stem>.dat`.  A bake-unit script without a `SPEC` raises —
the multi-object pattern (see CLAUDE.md -> "Bake units and per-asset
layout") would need its own re-emit hook; refuse to silently skip.
"""
from __future__ import annotations

import importlib
from pathlib import Path

from tools.threed.dat import Vehicle, emit_vehicle


_REPO = Path(__file__).resolve().parents[2]
_SKIP_DIRS = {"tools", "tests", "grounds", "simutranslator", ".cache",
              "build", "__pycache__"}


def _discover() -> list[Path]:
    scripts: list[Path] = []
    for path in sorted(_REPO.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        rel = path.relative_to(_REPO)
        if rel.parts[0] in _SKIP_DIRS:
            continue
        stem = path.with_suffix("")
        if stem.with_suffix(".dat").exists() and stem.with_suffix(".png").exists():
            scripts.append(path)
    return scripts


def _reemit(script: Path) -> Path:
    rel = script.relative_to(_REPO).with_suffix("")
    mod_name = ".".join(rel.parts)
    mod = importlib.import_module(mod_name)
    spec = getattr(mod, "SPEC", None)
    if not isinstance(spec, Vehicle):
        raise RuntimeError(
            f"{rel}.py has no `SPEC: Vehicle` — multi-object bake units "
            f"need their own re-emit hook"
        )
    return emit_vehicle(spec, out_dir=script.parent, basename=script.stem)


def main() -> None:
    for script in _discover():
        out = _reemit(script)
        print(f"wrote {out.relative_to(_REPO)}", flush=True)


if __name__ == "__main__":
    main()
