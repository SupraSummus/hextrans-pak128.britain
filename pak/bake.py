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
from pak.dat import Building, Vehicle, Way, emit_building, emit_vehicles, emit_way
from pak.fetch_blend import fetch
from pak.materials import Material

_RENDER_SCRIPT = Path(__file__).resolve().parent / "render.py"
_BAKE_WAY_SCRIPT = Path(__file__).resolve().parent / "bake_way.py"


def hex_layouts_default(dims_x: int, dims_y: int) -> int:
    """Layout count this hex pak bakes when a Building SPEC leaves
    `layouts=None`.  Pak-side policy, not engine schema — atlas size
    is a render-time choice, distinct from `pak.dat.layouts_default`
    which mirrors the engine's read-side default for `dims=X,Y` (no
    Z).  Single-tile assets get 6 — hex has 6-fold rotational
    symmetry, so 60° steps map facings onto the six hex edge
    directions exactly.  City-building placement (`simcity.cc` ->
    `simrand(get_all_layouts())`) is uniform over `[0, layouts)`,
    so 6 layouts give every map placement an on-axis silhouette;
    8 would have left half of placements at 45° off-axis where the
    hex grid has nothing to align to.  Map rotation (which
    `gebaeude_t::rotate90` would walk) is fatal under hex and the
    code path is unreachable, so its missing 6-layout case doesn't
    bite.  Rectangular tiles fall back to the engine default (2 —
    one per orientation) until a multi-tile asset ports and pins
    the right hex count.
    """
    if dims_x == 1 and dims_y == 1:
        return 6
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


def _render_building_season(
    *, blend: str, name: str, out_dir: Path, spec: Building,
    materials: dict[str, Material] | None,
) -> Path:
    """Render one season's atlas to `<out_dir>/<name>.png` and return
    the path.  One blender subprocess per call."""
    blend_path = fetch(blend)
    # One atlas row per `(season, height)` stripe; each row holds
    # `layouts * dims_x * dims_y` cells (layouts span columns).  See
    # `pak.dat.emit_building` for the matching row/col formula.
    cells_per_row = spec.layouts * spec.dims_x * spec.dims_y
    cmd = [
        "blender", "-b", str(blend_path),
        "--python-exit-code", "1",
        "-P", str(_RENDER_SCRIPT),
        "--",
        "--out", str(out_dir),
        "--name", name,
        "--viewpoint", "hex_building",
        "--building-footprint",
        f"{spec.dims_x},{spec.dims_y},{spec.layouts},{spec.heights}",
        "--cols-per-row", str(cells_per_row),
    ]
    if materials:
        from pak.materials import to_jsonable
        cmd += ["--materials", json.dumps(to_jsonable(materials))]
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)
    return out_dir / f"{name}.png"


def _stitch_seasons(season_pngs: list[Path], out_path: Path) -> None:
    """Vertically concatenate per-season PNGs into a single atlas.

    Top = summer, bottom = winter — matches `emit_building`'s row
    formula `s * heights + h` (each season is a `heights`-row
    stripe).  All inputs must share dimensions (same viewpoint, same
    footprint)."""
    from PIL import Image
    images = [Image.open(p).convert("RGBA") for p in season_pngs]
    sizes = {img.size for img in images}
    if len(sizes) > 1:
        raise RuntimeError(f"season PNGs have mismatched sizes: {sorted(sizes)}")
    w, h = images[0].size
    combined = Image.new("RGBA", (w, h * len(images)), (0, 0, 0, 0))
    for i, img in enumerate(images):
        combined.paste(img, (0, i * h))
    combined.save(out_path)


def bake_building(
    spec: Building,
    *,
    blend: str,
    basename: str,
    out_dir: Path,
    materials: dict[str, Material] | None = None,
    blend_winter: str | None = None,
    materials_winter: dict[str, Material] | None = None,
) -> Path:
    """Fetch the blend(s), render the multi-tile atlas, emit the dat.

    Drives `pak/render.py` under `--viewpoint hex_building` with the
    SPEC's `(dims_x, dims_y, layouts)` footprint; the renderer
    expands that into `layouts × dims_x × dims_y` per-cell facings
    (see `viewpoints.building_hex_viewpoint`).  The atlas lands at
    `<out_dir>/<basename>.png` shaped `seasons*heights` rows ×
    `layouts*dims_x*dims_y` cols — see `emit_building` for the
    matching `backimage[l][y][x][h][0][s]=./<basename>.<row>.<col>`
    row/col formula.

    When `spec.seasons >= 2`, requires `blend_winter` (the upstream
    sibling `-snow.blend` per asset) and typically `materials_winter`
    (seed via `python3 -m pak.extract_materials <winter-blend>`).
    Renders each season into a temporary `<basename>__s<i>.png`, then
    vertically concatenates with summer on top.

    Layout rotation, per-cell translation, and the model's centring
    convention are all best-guess on the first pass.  When the first
    real bake surfaces misalignment, fix in
    `viewpoints.building_hex_viewpoint` (rotation sign / koord-tile
    mapping) and in `render.py::_compute_fit` (the `fit_kind="hex"`
    centring may need a multi-tile variant that anchors on the
    building's koord origin rather than the model's XY bbox).
    """
    spec = _resolve_building_layouts(spec)

    season_inputs: list[tuple[str, dict[str, Material] | None]] = [(blend, materials)]
    if spec.seasons >= 2:
        if blend_winter is None:
            raise ValueError(
                f"{basename}: spec.seasons={spec.seasons} requires blend_winter"
            )
        season_inputs.append((blend_winter, materials_winter))

    if len(season_inputs) == 1:
        _render_building_season(
            blend=blend, name=basename, out_dir=out_dir,
            spec=spec, materials=materials,
        )
    else:
        tmp_paths: list[Path] = []
        for s, (b, m) in enumerate(season_inputs):
            tmp_name = f"{basename}__s{s}"
            tmp_paths.append(_render_building_season(
                blend=b, name=tmp_name, out_dir=out_dir,
                spec=spec, materials=m,
            ))
        _stitch_seasons(tmp_paths, out_dir / f"{basename}.png")
        for p in tmp_paths:
            p.unlink()

    out_dat = emit_building(spec, out_dir=out_dir, basename=basename)
    try:
        print(f"wrote {out_dat.relative_to(REPO_ROOT)}", flush=True)
    except ValueError:
        print(f"wrote {out_dat}", flush=True)
    return out_dat


def bake_building_main(
    spec: Building, blend: str, file: str, *,
    materials: dict[str, Material] | None = None,
    blend_winter: str | None = None,
    materials_winter: dict[str, Material] | None = None,
) -> Path:
    """Convenience for single-building bake scripts.

    Derives `out_dir` and `basename` from the calling script's
    `__file__`, so each bake script's bottom collapses to:

        if __name__ == "__main__":
            bake_building_main(SPEC, BLEND, __file__, materials=MATERIALS)

    Pass `blend_winter` / `materials_winter` alongside when the SPEC
    declares `seasons=2`.
    """
    path = Path(file).resolve()
    return bake_building(
        spec, blend=blend, basename=path.stem, out_dir=path.parent,
        materials=materials,
        blend_winter=blend_winter, materials_winter=materials_winter,
    )
