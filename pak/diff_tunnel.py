"""Calibration diff for tunnel portals against the upstream pak atlas.

Mirrors `diff_bridge.run()` but tailored to upstream's tunnel cell
layout (`ways/<stem>.png`, atlas with row 0 = Front[<F>] and row 1 =
Back[<F>] per dat col order, plus cursor/icon).  Our square render
emits the whole portal as a single silhouette per facing; upstream
ships the same portal split across Back (rear interior) and Front
(arch / outer face) cells that the engine draws at the same screen
position around the train sprite.  The apples-to-apples target is
therefore the **stitched** Back+Front silhouette, built by alpha-
compositing Back under Front per facing -- conceptually the same
move as `diff_buildings._stitch_upstream_layout` (parse upstream's
image refs from the dat, slice the atlas, paste back onto a canvas
at engine screen positions), specialised to the tunnel case where
both layers land on the same 128x128 cell.

This harness renders through `tunnel_square_viewpoint()` (4 cardinals,
square dimetric -- matches upstream's authoring) rather than the
production `tunnel_hex_viewpoint()`: hex would render 6 facings that
don't have upstream counterparts.  Calibration here pins lighting /
strip-set / camera fidelity against the upstream PNG; the hex bake
then reuses the same blend through the hex projection.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

from pak import REPO_ROOT
from pak.bake import fetch_blend_by_source, run_render
from pak.compose import compose_atlas
from pak.dat import find_object, iter_image_refs, parse
from pak.diff import MAGIC_PINK, GridCell, cell_metric, compose_grid, key_magic_pink_to_alpha
from pak.fetch_pak import fetch as fetch_pak
from pak.upstream import image_stem
from pak.viewpoints import tunnel_square_viewpoint

CELL = 128

# Square-cardinal facing labels for the calibration render -- match
# `tunnel_square_viewpoint()`'s facing order (mouth-points-<F>
# convention shared with `_HEX_TUNNEL_MODEL_ROT_DEG`).  Production
# bake uses `pak.dat.TUNNEL_FACING_LABELS` (6 hex edges); the two
# sets are independent label-spaces over the same convention.
SQUARE_FACING_LABELS: tuple[str, ...] = ("S", "N", "E", "W")

@dataclass(frozen=True)
class FacingMetric:
    facing: str
    iou: float
    xor_px: int
    drgb: float


# Calibration floor.  Stone-tunnel ranges 0.91-0.96 with the slope
# slab cutter active (`Viewpoint.holdout_meshes`).  Pinned a bit below
# the worst to catch directional drift without flapping on the
# residual XOR.
FAIL_IOU: float = 0.85


def _parse_tunnel_image_entries(dat_path: Path, *, name: str):
    """Parse a tunnel dat's `frontimage[<F>][0]=<basename>.<row>.<col>`
    and `backimage[<F>][0]=<basename>.<row>.<col>` entries for the
    `season=0` slot.  Returns `{<F>: {"front": (row, col),
    "back": (row, col) | None}}` keyed by raw-case facing label
    (matches `SQUARE_FACING_LABELS` lookup).

    Sparse Back is honoured: upstream `tunnels.dat`'s stone variant
    only ships Back for W and N, so other facings stitch against Front
    alone.  Multi-object dats are filtered by `name=` (matches the
    object's `Name=` case-insensitively)."""
    obj = find_object(parse(dat_path), name, source=dat_path)
    by_facing: dict[str, dict[str, tuple[int, int] | None]] = {}
    for ref in iter_image_refs(obj):
        if ref.family not in ("frontimage", "backimage"):
            continue
        if ref.row is None or len(ref.indices) != 2 or ref.indices[1] != "0":
            continue
        facing = ref.indices[0]
        layer = "front" if ref.family == "frontimage" else "back"
        by_facing.setdefault(facing, {"front": None, "back": None})[layer] = (
            ref.row, ref.col
        )
    return by_facing


def _stitch_upstream_cell(atlas, front_rc: tuple[int, int],
                          back_rc: tuple[int, int] | None):
    """Alpha-composite upstream Back under Front at the shared 128² cell.
    Back-less facings (e.g. stone tunnel's E/S) collapse to Front alone."""
    def _crop(rc: tuple[int, int]):
        row, col = rc
        return key_magic_pink_to_alpha(
            atlas.crop((col * CELL, row * CELL,
                        col * CELL + CELL, row * CELL + CELL))
        )

    front = _crop(front_rc)
    if back_rc is None:
        return front
    back = _crop(back_rc)
    return Image.alpha_composite(back, front)


def _ours_cell(rendered_atlas_path: Path, facing: str):
    """Slice the calibration render atlas (single-row 4-cell, columns
    S/N/E/W per `SQUARE_FACING_LABELS`) at the given facing."""
    col = SQUARE_FACING_LABELS.index(facing)
    atlas = Image.open(rendered_atlas_path).convert("RGBA")
    return atlas.crop((col * CELL, 0, col * CELL + CELL, CELL))


def run(blend: str, upstream_dat: str, *, out_dir: Path, name: str,
        blend_source: str = "jh") -> list[FacingMetric]:
    """Render `blend` through `tunnel_square_viewpoint()`, slice the
    rendered atlas + upstream atlas per facing, write `grid.png` and
    return per-facing metrics.

    `upstream_dat` follows the SPEC convention -- the dat's first
    image ref tells us the upstream PNG path via `pak.upstream.
    image_stem`.  `name` is the SPEC's `name=` (used for multi-object
    upstream dats; single-object dats can pass any of the names).
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    blend_path = fetch_blend_by_source(blend, blend_source)
    vp = tunnel_square_viewpoint()
    render_stem = name
    run_render(blend=blend_path, viewpoint=vp,
               name=render_stem, out_dir=out_dir)
    rendered = compose_atlas(vp, render_dir=out_dir, out_dir=out_dir,
                             name=render_stem)

    upstream_png = fetch_pak(f"{image_stem(upstream_dat, name=name)}.png")
    atlas = Image.open(upstream_png).convert("RGBA")
    entries = _parse_tunnel_image_entries(fetch_pak(upstream_dat), name=name)

    cells: list[GridCell] = []
    metrics: list[FacingMetric] = []
    for facing in SQUARE_FACING_LABELS:
        layers = entries.get(facing)
        if layers is None or layers.get("front") is None:
            raise SystemExit(
                f"{upstream_dat}: no FrontImage[{facing}][0] for {name!r}"
            )
        ours = np.asarray(_ours_cell(rendered, facing))
        up = np.asarray(_stitch_upstream_cell(
            atlas, layers["front"], layers.get("back"),
        ))
        m, om, um = cell_metric(ours, up, alpha_threshold=0,
                                magic_rgb=MAGIC_PINK)
        metrics.append(FacingMetric(facing=facing, iou=m.iou,
                                    xor_px=m.xor_px, drgb=m.drgb))
        label = (f"Back+Front[{facing}]" if layers.get("back")
                 else f"Front[{facing}]")
        cells.append(GridCell(ours, up, om, um, label))
    compose_grid(cells, out_path=out_dir / "grid.png",
                 strip_magic_rgb=MAGIC_PINK)
    return metrics


def format_table(metrics: list[FacingMetric]) -> str:
    lines = [f"{'view':>4}  {'IoU':>6}  {'XOR_px':>7}  {'dRGB':>7}"]
    for m in metrics:
        lines.append(
            f"{m.facing:>4}  {m.iou:>6.3f}  {m.xor_px:>7d}  {m.drgb:>7.2f}"
        )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("blend")
    ap.add_argument("upstream_dat")
    ap.add_argument("--name", required=True,
                    help="object Name= in upstream_dat (multi-object dats)")
    ap.add_argument("--blend-source", default="jh", choices=["jp", "jh"])
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    out_dir = (Path(args.out) if args.out
               else REPO_ROOT / "out" / "diff" / args.name)
    metrics = run(args.blend, args.upstream_dat,
                  out_dir=out_dir, name=args.name,
                  blend_source=args.blend_source)
    print(f"wrote {out_dir / 'grid.png'}")
    print(format_table(metrics))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
