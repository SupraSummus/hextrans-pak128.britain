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
from pak.bake import clamp_age_overrides, hex_layouts_default
from pak.bake_units import discover, import_script, specs_of
from pak.dat import (
    Bridge,
    Building,
    Tree,
    Tunnel,
    Vehicle,
    Way,
    emit_bridge,
    emit_building,
    emit_trees,
    emit_tunnel,
    emit_vehicles,
    emit_way,
)

# Rendered-ages count for the Tree reemit path -- matches
# `pak.bake.bake_tree`'s `ages=4` default.  Both feed the same
# `clamp_age_overrides` so the committed dat round-trips byte-for-byte
# through the reemit lint job.
_REEMIT_TREE_AGES = 4


def emit_for_specs(specs: list, out_dir: Path, basename: str) -> Path:
    """Run the matching emitter for a normalised spec list, returning
    the written dat path.  Building specs route their `dims=X,Y,Z`
    through `hex_layouts_default(spec.symmetry)` so the layout count
    matches what `bake_building` would render -- one source of truth
    applied at every emit site (reemit lint, ported-dat test, future
    cross-pak tooling).  Raises on a mixed or unsupported spec list."""
    if specs and all(isinstance(s, Vehicle) for s in specs):
        return emit_vehicles(specs, out_dir=out_dir, basename=basename)
    if len(specs) == 1 and isinstance(specs[0], Way):
        return emit_way(specs[0], out_dir=out_dir, basename=basename)
    if len(specs) == 1 and isinstance(specs[0], Bridge):
        return emit_bridge(specs[0], out_dir=out_dir, basename=basename)
    if len(specs) == 1 and isinstance(specs[0], Tunnel):
        return emit_tunnel(specs[0], out_dir=out_dir, basename=basename)
    if len(specs) == 1 and isinstance(specs[0], Building):
        spec = specs[0]
        return emit_building(
            spec, out_dir=out_dir, basename=basename,
            layouts=hex_layouts_default(spec.symmetry),
        )
    if specs and all(isinstance(s, Tree) for s in specs):
        seasons = max(t.seasons for t in specs)
        return emit_trees(
            specs, out_dir=out_dir, basename=basename,
            age_overrides=clamp_age_overrides(
                seasons=seasons, ages=_REEMIT_TREE_AGES,
            ),
        )
    raise RuntimeError(
        f"unsupported spec list (got {[type(s).__name__ for s in specs]})"
    )


def _reemit(script: Path) -> Path:
    specs = specs_of(import_script(script))
    try:
        return emit_for_specs(specs, script.parent, script.stem)
    except RuntimeError as exc:
        rel = script.relative_to(REPO_ROOT)
        raise RuntimeError(f"{rel}: {exc}") from exc


def main() -> None:
    for script in discover():
        out = _reemit(script)
        print(f"wrote {out.relative_to(REPO_ROOT)}", flush=True)


if __name__ == "__main__":
    main()
