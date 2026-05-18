"""Per-asset bake driver — shrinks bake scripts to their essentials.

A bake script declares one `SPEC` (or `SPECS` list) plus, at
`__main__` time, a single `bake_*_main(SPEC, __file__)` call.
Everything the bake pipeline needs — `blend`, `upstream_stem`,
`materials`, `blend_winter`, `materials_winter`, `lighting`,
`strip` — lives on the SPEC itself as bake-pipeline metadata
(see `pak.dat._bake_meta`).  The dat emitters skip those fields;
this driver reads them off the SPEC and threads them through to
the renderer.

Multi-object bake units call `bake_vehicle` once per output,
passing distinct `basename` per call.  Shared-sprite multi-object
units (SPECS list) all carry the same blend / upstream_stem /
materials values on every Vehicle in the list -- typically via a
local `_BLEND = "..."` variable referenced from each Vehicle's
`blend=`; `bake_vehicle` asserts they match and uses the first.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from pak import REPO_ROOT
from pak.dat import (
    HEX_BRIDGE_ATLAS_COLS,
    HEX_BRIDGE_PIECE_ORDER,
    TREE_AGE_COUNT,
    Bridge,
    Building,
    Tree,
    Vehicle,
    Way,
    emit_bridge,
    emit_building,
    emit_trees,
    emit_vehicles,
    emit_way,
)
from pak.fetch_blend import fetch
from pak.fetch_jh_blend import fetch as fetch_jh
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


def _shared_blend(specs: list, basename: str) -> str:
    """Return the single `blend` path shared across a SPECS list.

    Shared-sprite multi-object scripts (e.g. `dragon-rapide` +
    `-mail`) declare every Vehicle/Tree with the same `blend=` value
    (typically a local `_BLEND = "..."` referenced from each); one
    render produces one atlas referenced by every block.  Diverging
    blends on the same list would silently render the first and
    point both at it — assert match here instead.  Works on any SPEC
    type that carries a `.blend` field.
    """
    blends = {s.blend for s in specs}
    if None in blends:
        raise ValueError(f"{basename}: SPEC missing blend=")
    if len(blends) != 1:
        raise ValueError(f"{basename}: SPECS disagree on blend= ({sorted(blends)})")
    return next(iter(blends))


def bake_vehicle(
    spec: Vehicle | list[Vehicle],
    *,
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

    `Vehicle.blend` is the path inside the upstream blends repo
    (resolved via `fetch_blend.fetch` against the global
    `blends.lock` SHA).  `basename` is the shared filesystem stem
    for atlas and dat — typically the bake script's
    `Path(__file__).stem`.  Returns the dat path.
    """
    specs = [spec] if isinstance(spec, Vehicle) else list(spec)
    blend = _shared_blend(specs, basename)
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


def bake_main(spec: Vehicle | list[Vehicle], file: str) -> Path:
    """Convenience for bake scripts that render one blend per script.

    Derives `out_dir` and `basename` from the calling script's
    `__file__`.  Accepts either a single `Vehicle` (`SPEC`) or a
    list (`SPECS` for shared-sprite variants).
    """
    path = Path(file).resolve()
    return bake_vehicle(spec, basename=path.stem, out_dir=path.parent)


def bake_way(spec: Way, *, basename: str, out_dir: Path) -> Path:
    """Drive `pak/bake_way.py` to render `<out_dir>/<basename>.png`,
    then emit `<out_dir>/<basename>.dat` from `spec`.

    `spec.blend` is the path inside the upstream blends repo (resolved
    by `bake_way.py` via `fetch_blend.fetch`).  `spec.strip` is a
    comma-separated list of mesh names to drop on entry — default
    `Sphere` (the upstream sun-direction visualizer); per-blend
    overrides go here when a blend ships extra debug meshes that
    don't belong in the bake (see `CLAUDE.md` -> "Way-bake
    architecture" -> Naming pitfall).  `spec.materials` (if supplied)
    recolours the blend's named materials in-place — the rail-grade
    catalog renders the same blend with per-variant `materials=`
    dicts on each `ways/<rail>.py` SPEC; this driver serialises the
    dict to JSON on the `--materials` CLI arg, the Blender
    subprocess parses it back (tuples come through as lists; the
    override applier just unpacks three-element sequences).
    Returns the dat path.
    """
    if spec.blend is None:
        raise ValueError(f"{basename}: SPEC missing blend=")
    cmd = [
        "blender", "-b",
        "--python-exit-code", "1",
        "-P", str(_BAKE_WAY_SCRIPT),
        "--",
        "--blend", spec.blend,
        "--name", basename,
        "--out", str(out_dir),
        "--strip", spec.strip,
    ]
    if spec.materials:
        cmd += ["--materials", json.dumps(spec.materials)]
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)

    out_dat = emit_way(spec, out_dir=out_dir, basename=basename)
    try:
        print(f"wrote {out_dat.relative_to(REPO_ROOT)}", flush=True)
    except ValueError:
        print(f"wrote {out_dat}", flush=True)
    return out_dat


def bake_way_main(spec: Way, file: str) -> Path:
    """Convenience for single-way bake scripts.

    Derives `out_dir` and `basename` from the calling script's
    `__file__`, so each bake script's bottom collapses to:

        if __name__ == "__main__":
            bake_way_main(SPEC, __file__)
    """
    path = Path(file).resolve()
    return bake_way(spec, basename=path.stem, out_dir=path.parent)


def _bridge_piece_blends(spec: Bridge) -> dict[str, str]:
    """Resolve `(piece, blend_path)` for every piece in
    `HEX_BRIDGE_PIECE_ORDER`.  All three pieces are required today;
    partial coverage (span-only / start-only) isn't supported until
    a real asset needs it."""
    blends = {
        "image": spec.blend_image,
        "start": spec.blend_start,
        "ramp":  spec.blend_ramp,
    }
    missing = [p for p in HEX_BRIDGE_PIECE_ORDER if blends[p] is None]
    if missing:
        raise ValueError(
            f"Bridge SPEC missing piece blends: {missing} "
            f"(need blend_image, blend_start, blend_ramp)"
        )
    return blends


def _render_bridge_piece(
    *, blend: str, name: str, out_dir: Path, piece: str,
) -> Path:
    """Render one piece blend through `bridge_hex_viewpoint(piece)`
    into `<out_dir>/<name>.png` and return the path.  One blender
    subprocess per call."""
    blend_path = fetch_jh(blend)
    cmd = [
        "blender", "-b", str(blend_path),
        "--python-exit-code", "1",
        "-P", str(_RENDER_SCRIPT),
        "--",
        "--out", str(out_dir),
        "--name", name,
        "--viewpoint", "bridge_hex",
        "--bridge-piece", piece,
    ]
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)
    return out_dir / f"{name}.png"


def _stitch_bridge_atlas(
    piece_pngs: dict[str, Path],
    out_path: Path,
) -> None:
    """Stitch per-piece single-row PNGs into the canonical hex bridge
    atlas at `out_path`.  Rows follow `HEX_BRIDGE_PIECE_ORDER` (image
    on top); each row is padded to `HEX_BRIDGE_ATLAS_COLS` cells wide
    so the narrower image row's 3 axis cells land flush-left with the
    trailing cells transparent."""
    from PIL import Image
    sizes = {Image.open(p).size for p in piece_pngs.values()}
    heights = {h for _, h in sizes}
    if len(heights) != 1:
        raise RuntimeError(
            f"bridge piece PNGs have mismatched cell heights: {sorted(sizes)}"
        )
    # All renders are square `DEFAULT_W`-sized cells; one row's height
    # equals one cell's edge length.
    (cell,) = heights
    atlas = Image.new(
        "RGBA",
        (HEX_BRIDGE_ATLAS_COLS * cell, len(HEX_BRIDGE_PIECE_ORDER) * cell),
        (0, 0, 0, 0),
    )
    for row, piece in enumerate(HEX_BRIDGE_PIECE_ORDER):
        atlas.paste(Image.open(piece_pngs[piece]).convert("RGBA"),
                    (0, row * cell))
    atlas.save(out_path)


def bake_bridge(spec: Bridge, *, basename: str, out_dir: Path) -> Path:
    """Fetch the piece blends, render the hex bridge atlas, emit the
    dat.

    Per-piece renders (`<basename>__<piece>.png`) go through
    `bridge_hex_viewpoint(piece)` -- 3 facings for the image span,
    6 each for start / ramp endpoints -- then `_stitch_bridge_atlas`
    composes them into `<out_dir>/<basename>.png` matching
    `pak.dat.emit_bridge`'s row formula (image / start / ramp).

    See TODO.md -> "Hex bridge cell coverage" for the depth-clipped
    Back/Front, variant 2 + season 1, and engine-schema follow-ups
    visible in the emitted dat.  Returns the dat path.
    """
    piece_blends = _bridge_piece_blends(spec)
    piece_pngs: dict[str, Path] = {}
    for piece, blend in piece_blends.items():
        piece_name = f"{basename}__{piece}"
        piece_pngs[piece] = _render_bridge_piece(
            blend=blend, name=piece_name, out_dir=out_dir, piece=piece,
        )

    _stitch_bridge_atlas(piece_pngs, out_dir / f"{basename}.png")
    for p in piece_pngs.values():
        p.unlink()

    out_dat = emit_bridge(spec, out_dir=out_dir, basename=basename)
    try:
        print(f"wrote {out_dat.relative_to(REPO_ROOT)}", flush=True)
    except ValueError:
        print(f"wrote {out_dat}", flush=True)
    return out_dat


def bake_bridge_main(spec: Bridge, file: str) -> Path:
    """Convenience for single-bridge bake scripts.

    Derives `out_dir` and `basename` from the calling script's
    `__file__`, so each bake script's bottom collapses to:

        if __name__ == "__main__":
            bake_bridge_main(SPEC, __file__)
    """
    path = Path(file).resolve()
    return bake_bridge(spec, basename=path.stem, out_dir=path.parent)


def _render_building_season(
    *, blend: str, name: str, out_dir: Path, spec: Building,
    materials: dict[str, Material] | None,
    lighting=None,
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
    if lighting is not None:
        cmd += ["--lighting", json.dumps(lighting.to_jsonable())]
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


def bake_building(spec: Building, *, basename: str, out_dir: Path) -> Path:
    """Fetch the blend(s), render the multi-tile atlas, emit the dat.

    Drives `pak/render.py` under `--viewpoint hex_building` with the
    SPEC's `(dims_x, dims_y, layouts)` footprint; the renderer
    expands that into `layouts × dims_x × dims_y` per-cell facings
    (see `viewpoints.building_hex_viewpoint`).  The atlas lands at
    `<out_dir>/<basename>.png` shaped `seasons*heights` rows ×
    `layouts*dims_x*dims_y` cols — see `emit_building` for the
    matching `backimage[l][y][x][h][0][s]=./<basename>.<row>.<col>`
    row/col formula.

    When `spec.seasons >= 2`, requires `spec.blend_winter` (the
    upstream sibling `-snow.blend` per asset) and typically
    `spec.materials_winter` (seed via `python3 -m pak.extract_materials
    <winter-blend>`).  Renders each season into a temporary
    `<basename>__s<i>.png`, then vertically concatenates with summer
    on top.

    Layout rotation, per-cell translation, and the model's centring
    convention are all best-guess on the first pass.  When the first
    real bake surfaces misalignment, fix in
    `viewpoints.building_hex_viewpoint` (rotation sign / koord-tile
    mapping) and in `render.py::_compute_fit` (the `fit_kind="hex"`
    centring may need a multi-tile variant that anchors on the
    building's koord origin rather than the model's XY bbox).
    """
    if spec.blend is None:
        raise ValueError(f"{basename}: SPEC missing blend=")
    spec = _resolve_building_layouts(spec)

    # Single-season bake renders straight into `<basename>.png`;
    # multi-season renders per-season into `<basename>__s<i>.png`
    # tempfiles, then `_stitch_seasons` concatenates summer-on-top.
    season_inputs: list[tuple[str, dict[str, Material] | None]] = [
        (spec.blend, spec.materials),
    ]
    if spec.seasons >= 2:
        if spec.blend_winter is None:
            raise ValueError(
                f"{basename}: spec.seasons={spec.seasons} requires blend_winter"
            )
        season_inputs.append((spec.blend_winter, spec.materials_winter))

    single = len(season_inputs) == 1
    tmp_paths: list[Path] = []
    for s, (b, m) in enumerate(season_inputs):
        name = basename if single else f"{basename}__s{s}"
        tmp_paths.append(_render_building_season(
            blend=b, name=name, out_dir=out_dir,
            spec=spec, materials=m, lighting=spec.lighting,
        ))
    if not single:
        _stitch_seasons(tmp_paths, out_dir / f"{basename}.png")
        for p in tmp_paths:
            p.unlink()

    out_dat = emit_building(spec, out_dir=out_dir, basename=basename)
    try:
        print(f"wrote {out_dat.relative_to(REPO_ROOT)}", flush=True)
    except ValueError:
        print(f"wrote {out_dat}", flush=True)
    return out_dat


def bake_tree(
    spec: Tree | list[Tree],
    *,
    basename: str,
    out_dir: Path,
    ages: int = 4,
    viewpoint: str = "tree_hex",
) -> Path:
    """Fetch the blend, render `<out_dir>/<basename>.png` (ages × seasons
    grid driven by the SPEC's `seasons`), emit `<out_dir>/<basename>.dat`.

    `spec` may be a single `Tree` or a list (one combined dat sharing
    one atlas, matching upstream's `tree.dat` shape).  `ages` defaults
    to 4 -- upstream pak128.Britain renders ages 0..3 distinctly and
    points age 4 (the dormant / dying stage) at the bare `winter-3`
    image rather than rendering separately; `clamp_age_overrides`
    mirrors that at dat-emit time by pointing every engine age outside
    `[0, ages)` at the last rendered cell of the same season.
    `viewpoint` selects `tree_hex` (shipped atlas) or `tree_square`
    (calibration diff).  Returns the dat path.
    """
    specs = [spec] if isinstance(spec, Tree) else list(spec)
    # All specs must agree on seasons for one shared atlas; emit_trees
    # walks per-Tree `seasons` independently, but the rendered atlas is
    # a single grid -- mismatched seasons would need per-Tree atlas
    # slices, which the upstream `tree.dat` doesn't exercise.
    seasons = max(t.seasons for t in specs)
    blend = _shared_blend(specs, basename)
    blend_path = fetch(blend)

    cmd = [
        "blender", "-b", str(blend_path),
        "--python-exit-code", "1",
        "-P", str(_RENDER_SCRIPT),
        "--",
        "--out", str(out_dir),
        "--name", basename,
        "--viewpoint", viewpoint,
        "--tree-grid", f"{ages},{seasons}",
        "--cols-per-row", str(ages),
    ]
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)

    out_dat = emit_trees(
        specs, out_dir=out_dir, basename=basename,
        age_overrides=clamp_age_overrides(seasons=seasons, ages=ages),
    )
    try:
        print(f"wrote {out_dat.relative_to(REPO_ROOT)}", flush=True)
    except ValueError:
        print(f"wrote {out_dat}", flush=True)
    return out_dat


def clamp_age_overrides(
    *, seasons: int, ages: int,
) -> dict[tuple[int, int], tuple[int, int]]:
    """Point every engine age `>= ages` at the last rendered cell of
    the same season.

    The engine reads exactly `TREE_AGE_COUNT` (= 5) ages and fatals on
    a missing `image[age][season]` key; bakes typically render fewer
    (upstream pak128.Britain renders 4 distinct stages and reuses the
    last for age 4, the dormant stage).  Pulled out so `pak.reemit_
    dats`' regenerated dats match what `bake_tree` writes.
    """
    return {
        (a, s): (ages - 1, s)
        for a in range(ages, TREE_AGE_COUNT)
        for s in range(seasons)
    }


def bake_tree_main(
    spec: Tree | list[Tree], file: str, *,
    ages: int = 4,
    viewpoint: str = "tree_hex",
) -> Path:
    """Convenience for single-tree bake scripts.

    Derives `out_dir` and `basename` from the calling script's
    `__file__`, so each bake script's bottom collapses to:

        if __name__ == "__main__":
            bake_tree_main(SPEC, __file__)
    """
    path = Path(file).resolve()
    return bake_tree(
        spec, basename=path.stem, out_dir=path.parent,
        ages=ages, viewpoint=viewpoint,
    )


def bake_building_main(spec: Building, file: str) -> Path:
    """Convenience for single-building bake scripts.

    Derives `out_dir` and `basename` from the calling script's
    `__file__`, so each bake script's bottom collapses to:

        if __name__ == "__main__":
            bake_building_main(SPEC, __file__)
    """
    path = Path(file).resolve()
    return bake_building(spec, basename=path.stem, out_dir=path.parent)
