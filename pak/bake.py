"""Per-asset bake driver — shrinks bake scripts to their essentials.

A bake script declares one `SPEC` (or `SPECS` list) plus, at
`__main__` time, a single `bake_*_main(SPEC, __file__)` call.
Everything the bake pipeline needs — `blend`, `upstream_dat`,
`materials`, `blend_winter`, `materials_winter`, `lighting`,
`strip` — lives on the SPEC itself as bake-pipeline metadata
(see `pak.dat._bake_meta`).  The dat emitters skip those fields;
this driver reads them off the SPEC and threads them through to
the renderer.

Multi-object bake units call `bake_vehicle` once per output,
passing distinct `basename` per call.  Shared-sprite multi-object
units (SPECS list) all carry the same blend / upstream_dat /
materials values on every Vehicle in the list -- typically via a
local `_BLEND = "..."` variable referenced from each Vehicle's
`blend=`; `bake_vehicle` asserts they match and uses the first.
"""

from __future__ import annotations

import json
import pickle
import subprocess
import tempfile
from pathlib import Path

from pak import REPO_ROOT
from pak.dat import (
    HEX_BRIDGE_ATLAS_COLS,
    HEX_BRIDGE_PIECE_ORDER,
    TREE_AGE_COUNT,
    Bridge,
    Building,
    Symmetry,
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
from pak.fetch_blend import fetch
from pak.fetch_jh_blend import fetch as fetch_jh
from pak.materials import Material

# `pak.compose` and `pak.viewpoints` pull in numpy via hex_synth;
# kept off the module-import path so `pak.reemit_dats` /
# `pak.fetch_wavs` -- both of which import bake-unit scripts that
# `from pak.bake import bake_main` -- still work in dat-only CI
# environments without numpy installed.  Imported lazily inside
# each bake_* function below.

_RENDER_SCRIPT = Path(__file__).resolve().parent / "render.py"
_BAKE_WAY_SCRIPT = Path(__file__).resolve().parent / "bake_way.py"


_HEX_LAYOUT_QUANTUM = 6


def hex_layouts_default(symmetry: Symmetry) -> int:
    """Layout count derived from the asset's symmetry under the hex
    6-fold quantum: `6 // gcd(6, symmetry)`, or 1 for
    `Symmetry.CONTINUOUS`.  Six rotations of an asymmetric building
    cover every on-axis placement under city-placement's
    `simrand(get_all_layouts())` uniform draw; symmetric silhouettes
    collapse redundant rotations.  Same quantum drives
    `building_hex_viewpoint`'s per-layout rotation step.
    """
    if symmetry is Symmetry.CONTINUOUS:
        return 1
    from math import gcd
    return _HEX_LAYOUT_QUANTUM // gcd(_HEX_LAYOUT_QUANTUM, int(symmetry))


def _print_wrote(out_dat: Path) -> None:
    """`wrote <path>` line, repo-relative when possible (tests bake to tmp dirs)."""
    try:
        rel = out_dat.relative_to(REPO_ROOT)
    except ValueError:
        rel = out_dat
    print(f"wrote {rel}", flush=True)


def _run_blender(
    *,
    script: Path,
    blend: Path | None = None,
    args: dict[str, object],
) -> None:
    """Run `blender -b [blend] --python-exit-code 1 -P <script> -- <args>`.

    `args` is `{cli_name: value}` -- `cli_name` becomes `--cli_name`;
    `None` drops the entry, anything else is stringified into
    `--key=<value>`.  The `=` form (rather than space-separated) means
    negative-number values like `model-offset=-0.27,...` aren't
    misparsed as new option flags, and argparse on the Blender side
    accepts both forms identically.
    """
    cmd = ["blender", "-b"]
    if blend is not None:
        cmd.append(str(blend))
    cmd += ["--python-exit-code", "1", "-P", str(script), "--"]
    for key, val in args.items():
        if val is None:
            continue
        cmd.append(f"--{key}={val}")
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def run_render(
    *,
    blend: Path,
    viewpoint,
    name: str,
    out_dir: Path,
    materials: dict | None = None,
    model_offset: tuple[float, float, float] | None = None,
    material_id_map: bool = False,
) -> None:
    """Pickle a `RenderPayload` to a tempfile and drive `pak/render.py`
    against it.  Caller's Viewpoint feeds both this and the parent-side
    `compose_atlas`, so the factory dispatch lives in one place."""
    from pak.render import RenderPayload
    payload = RenderPayload(
        viewpoint=viewpoint, materials=materials,
        model_offset=model_offset, material_id_map=material_id_map,
    )
    with tempfile.NamedTemporaryFile(
        suffix=".pkl", prefix="render-payload-", delete=False,
    ) as fh:
        pickle.dump(payload, fh)
        payload_path = Path(fh.name)
    try:
        _run_blender(
            script=_RENDER_SCRIPT, blend=blend,
            args={"out": out_dir, "name": name, "payload": payload_path},
        )
    finally:
        payload_path.unlink(missing_ok=True)


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
    from pak.compose import compose_atlas
    from pak.viewpoints import HEX_VIEWPOINT
    specs = [spec] if isinstance(spec, Vehicle) else list(spec)
    blend = _shared_blend(specs, basename)
    blend_path = fetch(blend)
    run_render(blend=blend_path, viewpoint=HEX_VIEWPOINT,
               name=basename, out_dir=out_dir)
    compose_atlas(HEX_VIEWPOINT, render_dir=out_dir, out_dir=out_dir,
                  name=basename)

    out_dat = emit_vehicles(specs, out_dir=out_dir, basename=basename)
    _print_wrote(out_dat)
    return out_dat


def bake_main(spec: Vehicle | list[Vehicle], file: str) -> Path:
    """`bake_vehicle` keyed off the calling script's `__file__`."""
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
    args: dict[str, object] = {
        "blend": spec.blend,
        "name": basename,
        "out": out_dir,
        "strip": spec.strip,
    }
    if spec.materials:
        args["materials"] = json.dumps(spec.materials)
    _run_blender(script=_BAKE_WAY_SCRIPT, args=args)

    out_dat = emit_way(spec, out_dir=out_dir, basename=basename)
    _print_wrote(out_dat)
    return out_dat


def bake_way_main(spec: Way, file: str) -> Path:
    """`bake_way` keyed off the calling script's `__file__`."""
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
    from pak.compose import compose_atlas
    from pak.viewpoints import bridge_hex_viewpoint
    blend_path = fetch_jh(blend)
    vp = bridge_hex_viewpoint(piece)
    run_render(blend=blend_path, viewpoint=vp, name=name, out_dir=out_dir)
    compose_atlas(vp, render_dir=out_dir, out_dir=out_dir, name=name)
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
    _print_wrote(out_dat)
    return out_dat


def bake_bridge_main(spec: Bridge, file: str) -> Path:
    """`bake_bridge` keyed off the calling script's `__file__`."""
    path = Path(file).resolve()
    return bake_bridge(spec, basename=path.stem, out_dir=path.parent)


def bake_tunnel(spec: Tunnel, *, basename: str, out_dir: Path) -> Path:
    """Fetch the portal blend, render 4 cardinal facings through
    `tunnel_square_viewpoint()`, compose to a single-row 4-cell atlas,
    emit the dat.

    Per the port decision (TODO.md -> "Tunnel portal Back/Front
    authoring is non-standard"), the whole portal is emitted as
    `FrontImage[F][0]=` for each facing; `BackImage[F][0]` is left
    empty so the engine paints the portal silhouette over the train.

    Returns the dat path.
    """
    from pak.compose import compose_atlas
    from pak.viewpoints import tunnel_square_viewpoint

    if spec.blend is None:
        raise ValueError(f"Tunnel SPEC {spec.name!r} missing blend=")
    blend_path = fetch_blend_by_source(spec.blend, spec.blend_source)
    vp = tunnel_square_viewpoint()
    run_render(blend=blend_path, viewpoint=vp, name=basename, out_dir=out_dir)
    compose_atlas(vp, render_dir=out_dir, out_dir=out_dir, name=basename)

    out_dat = emit_tunnel(spec, out_dir=out_dir, basename=basename)
    _print_wrote(out_dat)
    return out_dat


def bake_tunnel_main(spec: Tunnel, file: str) -> Path:
    """`bake_tunnel` keyed off the calling script's `__file__`."""
    path = Path(file).resolve()
    return bake_tunnel(spec, basename=path.stem, out_dir=path.parent)


_BLEND_FETCHERS = {"jp": fetch, "jh": fetch_jh}


def fetch_blend_by_source(blend: str, source: str) -> Path:
    """Resolve `blend` against the upstream repo named by `source`.
    `"jp"` -> jamespetts (`fetch_blend`), `"jh"` -> JamesHood
    (`fetch_jh_blend`).  Building/attraction blends typically live in
    JamesHood; vehicles / ways / signals / citybuildings in jamespetts."""
    try:
        fetcher = _BLEND_FETCHERS[source]
    except KeyError as e:
        raise ValueError(
            f"unknown blend_source={source!r}; expected one of {sorted(_BLEND_FETCHERS)}"
        ) from e
    return fetcher(blend)


def bake_building_atlas(
    *,
    viewpoint_kind: str,
    blend_path: Path,
    name: str,
    out_dir: Path,
    layouts: int,
    dims_x: int,
    dims_y: int,
    heights: int,
    units_per_tile: float,
    materials: dict[str, Material] | None = None,
    lighting=None,
    model_offset_xyz: tuple[float, float, float] | None = None,
    strip: str | None = None,
    keep_per_facing: bool = False,
) -> Path:
    """Shared building render+compose for both `hex_building`
    (production) and `square_building` (calibration diff)
    viewpoint kinds.  `keep_per_facing=True` keeps the per-slice
    cells on disk for the diff path's `_load_our_cell`."""
    from dataclasses import replace

    from pak.compose import compose_atlas
    from pak.viewpoints import building_hex_viewpoint, building_square_viewpoint
    factory = (building_hex_viewpoint if viewpoint_kind == "hex_building"
               else building_square_viewpoint)
    vp = factory(
        layouts=layouts, dims_x=dims_x, dims_y=dims_y, heights=heights,
        units_per_tile=units_per_tile, lighting=lighting,
    )
    if strip:
        vp = replace(vp, strip_meshes=tuple(
            n for n in strip.split(",") if n
        ))
    run_render(
        blend=blend_path, viewpoint=vp, name=name, out_dir=out_dir,
        materials=materials, model_offset=model_offset_xyz,
    )
    compose_atlas(
        vp, render_dir=out_dir, out_dir=out_dir, name=name,
        cols_per_row=layouts * dims_x * dims_y,
        keep_per_facing=keep_per_facing,
    )
    return out_dir / f"{name}.png"


def _render_building_season(
    *, blend: str, name: str, out_dir: Path, spec: Building, layouts: int,
    materials: dict[str, Material] | None,
    lighting=None,
) -> Path:
    return bake_building_atlas(
        viewpoint_kind="hex_building",
        blend_path=fetch_blend_by_source(blend, spec.blend_source),
        name=name, out_dir=out_dir, layouts=layouts,
        dims_x=spec.dims_x, dims_y=spec.dims_y, heights=spec.heights,
        units_per_tile=spec.blend_units_per_tile,
        materials=materials, lighting=lighting,
        model_offset_xyz=spec.blend_model_offset_xyz, strip=spec.strip,
    )


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
    """Fetch the blend(s), render the N-tile atlas, emit the dat.

    Builds `building_hex_viewpoint()` from the SPEC's `(dims_x, dims_y,
    layouts)` footprint and drives `pak/render.py` via `run_render`;
    the factory expands the footprint into `layouts × heights`
    per-layout facings each carrying `dims_x × dims_y` slices (see
    `viewpoints.building_hex_viewpoint`).
    Single-tile (`dims_x == dims_y == 1`) is the degenerate case.  The
    atlas lands at
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
    mapping) and in its `fit_matrix` factory.
    """
    if spec.blend is None:
        raise ValueError(f"{basename}: SPEC missing blend=")
    layouts = hex_layouts_default(spec.symmetry)

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
            blend=b, name=name, out_dir=out_dir, layouts=layouts,
            spec=spec, materials=m, lighting=spec.lighting,
        ))
    if not single:
        _stitch_seasons(tmp_paths, out_dir / f"{basename}.png")
        for p in tmp_paths:
            p.unlink()

    out_dat = emit_building(spec, out_dir=out_dir, basename=basename,
                            layouts=layouts)
    _print_wrote(out_dat)
    return out_dat


def bake_tree(
    spec: Tree | list[Tree],
    *,
    basename: str,
    out_dir: Path,
    ages: int = 4,
) -> Path:
    """Fetch the blend, render `<out_dir>/<basename>.png` (ages × seasons
    grid driven by the SPEC's `seasons`), emit `<out_dir>/<basename>.dat`.

    `spec` may be a single `Tree` or a list (one combined dat sharing
    one atlas, matching upstream's `tree.dat` shape).  `ages` defaults
    to 4 -- upstream pak128.Britain renders ages 0..3 distinctly and
    points age 4 (the dormant / dying stage) at the bare `winter-3`
    image rather than rendering separately; `clamp_age_overrides`
    mirrors that at dat-emit time by pointing every engine age outside
    `[0, ages)` at the last rendered cell of the same season.  Returns
    the dat path.
    """
    from pak.compose import compose_atlas
    from pak.viewpoints import tree_hex_viewpoint
    specs = [spec] if isinstance(spec, Tree) else list(spec)
    # All specs must agree on seasons for one shared atlas; emit_trees
    # walks per-Tree `seasons` independently, but the rendered atlas is
    # a single grid -- mismatched seasons would need per-Tree atlas
    # slices, which the upstream `tree.dat` doesn't exercise.
    seasons = max(t.seasons for t in specs)
    blend = _shared_blend(specs, basename)
    blend_path = fetch(blend)

    vp = tree_hex_viewpoint(ages=ages, seasons=seasons)
    run_render(blend=blend_path, viewpoint=vp, name=basename, out_dir=out_dir)
    compose_atlas(vp, render_dir=out_dir, out_dir=out_dir, name=basename,
                  cols_per_row=ages)

    out_dat = emit_trees(
        specs, out_dir=out_dir, basename=basename,
        age_overrides=clamp_age_overrides(seasons=seasons, ages=ages),
    )
    _print_wrote(out_dat)
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
    spec: Tree | list[Tree], file: str, *, ages: int = 4,
) -> Path:
    """`bake_tree` keyed off the calling script's `__file__`."""
    path = Path(file).resolve()
    return bake_tree(spec, basename=path.stem, out_dir=path.parent, ages=ages)


def bake_building_main(spec: Building, file: str) -> Path:
    """`bake_building` keyed off the calling script's `__file__`."""
    path = Path(file).resolve()
    return bake_building(spec, basename=path.stem, out_dir=path.parent)
