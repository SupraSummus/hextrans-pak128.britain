"""Per-asset bake driver — shrinks bake scripts to their essentials.

A bake script's job is to declare:

  - the asset's `SPEC` (`Vehicle`, holds gameplay data)
  - the upstream blend path

`bake_vehicle` does the rest: fetch the blend, run the hex
renderer to produce the atlas PNG, write the dat next to it.
Bake scripts collapse to ~10 lines of imports + spec + a
one-line `bake_vehicle(...)` call at `__main__` time.

Multi-object bake units call `bake_vehicle` once per output,
passing distinct `basename` (and typically distinct `blend`)
per call.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from pak import REPO_ROOT
from pak.dat import (
    Building, Vehicle, Way, emit_building, emit_vehicles, emit_way,
)
from pak.fetch_blend import fetch


_RENDER_SCRIPT = Path(__file__).resolve().parent / "render.py"
_BAKE_WAY_SCRIPT = Path(__file__).resolve().parent / "bake_way.py"


def hex_layouts_default(dims_x: int, dims_y: int) -> int:
    """Layout count this hex pak bakes when a Building SPEC leaves
    `layouts=None`.  Pak-side policy, not engine schema — atlas size
    is a render-time choice, distinct from `pak.dat.layouts_default`
    which mirrors the engine's read-side default for `dims=X,Y` (no
    Z).  Single-tile assets get 8 to match `HEX_VIEWPOINT`'s 8-facing
    convention (half cardinal, half 45° corner views).  Rectangular
    tiles fall back to the engine default (2 — one per orientation)
    until a multi-tile asset ports and pins the right hex count;
    see TODO.md → "Building hex layout count is arbitrary at 8".
    """
    if dims_x == 1 and dims_y == 1:
        return 8
    from pak.dat import layouts_default
    return layouts_default(dims_x, dims_y)


def _resolve_building_layouts(spec: Building) -> Building:
    """Return `spec` with `layouts` filled in from `hex_layouts_default`
    when it was left None.  Both `bake_building` and `pak.reemit_dats`
    funnel through this so the atlas size declared in the rendered
    PNG and the `dims=X,Y,Z` line in the emitted dat agree."""
    if spec.layouts is not None:
        return spec
    from dataclasses import replace
    return replace(spec, layouts=hex_layouts_default(spec.dims_x, spec.dims_y))


def bake_vehicle(
    spec: Vehicle | list[Vehicle],
    *,
    blend: str,
    basename: str,
    out_dir: Path,
    viewpoint: str = "hex",
) -> Path:
    """Fetch the blend, render `<out_dir>/<basename>.png`, emit
    `<out_dir>/<basename>.dat` from `spec`.

    `spec` may be a single `Vehicle` or a list — multi-object bake
    units that share one sprite (upstream `dragon-rapide` +
    `dragon-rapide-mail`) pass a list, and every block's image refs
    point at the same atlas.  Bake units whose objects need distinct
    sprites (e.g. loco + tender) call `bake_vehicle` once per output
    with distinct `basename` instead.

    `blend` is the path inside the upstream blends repo (resolved
    via `fetch_blend.fetch` against the global `blends.lock` SHA).
    `basename` is the shared filesystem stem for atlas and dat —
    typically the bake script's `Path(__file__).stem`.  Returns the
    dat path.
    """
    specs = [spec] if isinstance(spec, Vehicle) else list(spec)
    blend_path = fetch(blend)
    cmd = [
        "blender", "-b", str(blend_path),
        "--python-exit-code", "1",
        "-P", str(_RENDER_SCRIPT),
        "--",
        "--out", str(out_dir),
        "--name", basename,
        "--viewpoint", viewpoint,
    ]
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)

    out_dat = emit_vehicles(specs, out_dir=out_dir, basename=basename)
    try:
        print(f"wrote {out_dat.relative_to(REPO_ROOT)}", flush=True)
    except ValueError:
        print(f"wrote {out_dat}", flush=True)
    return out_dat


def bake_main(spec: Vehicle | list[Vehicle], blend: str, file: str) -> Path:
    """Convenience for bake scripts that render one blend per script.

    Derives `out_dir` and `basename` from the calling script's
    `__file__`.  Accepts either a single `Vehicle` (`SPEC`) or a
    list (`SPECS` for shared-sprite variants).
    """
    path = Path(file).resolve()
    return bake_vehicle(
        spec, blend=blend, basename=path.stem, out_dir=path.parent,
    )


def bake_way(
    spec: Way,
    *,
    blend: str,
    basename: str,
    out_dir: Path,
    strip: str = "Sphere",
    materials: dict[str, tuple[int, int, int]] | None = None,
) -> Path:
    """Drive `pak/bake_way.py` to render `<out_dir>/<basename>.png`,
    then emit `<out_dir>/<basename>.dat` from `spec`.

    `blend` is the path inside the upstream blends repo (resolved by
    `bake_way.py` via `fetch_blend.fetch`).  `strip` is a comma-
    separated list of mesh names to drop on entry — default `Sphere`
    (the upstream sun-direction visualizer); per-blend overrides go
    here when a blend ships extra debug meshes that don't belong in
    the bake (see `CLAUDE.md` -> "Way-bake architecture" -> Naming
    pitfall).  `materials` (if supplied) recolours the blend's named
    materials in-place — the rail-grade catalog renders the same
    blend with per-variant `MATERIALS` dicts colocated in each
    `ways/<rail>.py`; this driver serialises the dict to JSON on
    the `--materials` CLI arg, the Blender subprocess parses it
    back (tuples come through as lists; the override applier
    just unpacks three-element sequences).  Returns the dat path.
    """
    cmd = [
        "blender", "-b",
        "--python-exit-code", "1",
        "-P", str(_BAKE_WAY_SCRIPT),
        "--",
        "--blend", blend,
        "--name", basename,
        "--out", str(out_dir),
        "--strip", strip,
    ]
    if materials:
        cmd += ["--materials", json.dumps(materials)]
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)

    out_dat = emit_way(spec, out_dir=out_dir, basename=basename)
    try:
        print(f"wrote {out_dat.relative_to(REPO_ROOT)}", flush=True)
    except ValueError:
        print(f"wrote {out_dat}", flush=True)
    return out_dat


def bake_way_main(
    spec: Way, blend: str, file: str, *,
    strip: str = "Sphere",
    materials: dict[str, tuple[int, int, int]] | None = None,
) -> Path:
    """Convenience for single-way bake scripts.

    Derives `out_dir` and `basename` from the calling script's
    `__file__`, so each bake script's bottom collapses to:

        if __name__ == "__main__":
            bake_way_main(SPEC, BLEND, __file__, materials=MATERIALS)
    """
    path = Path(file).resolve()
    return bake_way(
        spec, blend=blend, basename=path.stem, out_dir=path.parent,
        strip=strip, materials=materials,
    )


def bake_building(
    spec: Building,
    *,
    blend: str,
    basename: str,
    out_dir: Path,
) -> Path:
    """Fetch the blend, render the multi-tile atlas, emit the dat.

    Drives `pak/render.py` under `--viewpoint hex_building` with the
    SPEC's `(dims_x, dims_y, layouts)` footprint; the renderer
    expands that into `layouts × dims_x × dims_y` per-cell facings
    (see `viewpoints.building_hex_viewpoint`).  The atlas lands at
    `<out_dir>/<basename>.png` with `dims_x * dims_y` cells per row,
    one row per layout — matching the `backimage[l][y][x][0][0][0]
    =./<basename>.<l>.<col>` refs `emit_building` writes.

    Layout rotation, per-cell translation, and the model's centring
    convention are all best-guess on the first pass.  When the first
    real bake surfaces misalignment, fix in
    `viewpoints.building_hex_viewpoint` (rotation sign / koord-tile
    mapping) and in `render.py::_compute_fit` (the `fit_kind="hex"`
    centring may need a multi-tile variant that anchors on the
    building's koord origin rather than the model's XY bbox).
    """
    spec = _resolve_building_layouts(spec)
    blend_path = fetch(blend)
    cells_per_row = spec.dims_x * spec.dims_y
    cmd = [
        "blender", "-b", str(blend_path),
        "--python-exit-code", "1",
        "-P", str(_RENDER_SCRIPT),
        "--",
        "--out", str(out_dir),
        "--name", basename,
        "--viewpoint", "hex_building",
        "--building-footprint",
        f"{spec.dims_x},{spec.dims_y},{spec.layouts},{spec.heights}",
        "--cols-per-row", str(cells_per_row),
    ]
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)

    out_dat = emit_building(spec, out_dir=out_dir, basename=basename)
    try:
        print(f"wrote {out_dat.relative_to(REPO_ROOT)}", flush=True)
    except ValueError:
        print(f"wrote {out_dat}", flush=True)
    return out_dat


def bake_building_main(spec: Building, blend: str, file: str) -> Path:
    """Convenience for single-building bake scripts.

    Derives `out_dir` and `basename` from the calling script's
    `__file__`, so each bake script's bottom collapses to:

        if __name__ == "__main__":
            bake_building_main(SPEC, BLEND, __file__)
    """
    path = Path(file).resolve()
    return bake_building(
        spec, blend=blend, basename=path.stem, out_dir=path.parent,
    )
