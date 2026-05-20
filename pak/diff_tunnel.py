"""Calibration diff for tunnel portals against the upstream pak atlas.

Mirrors `diff_bridge.run()` but tailored to upstream's tunnel cell
layout (`ways/<stem>.png`, 4x2 atlas: row 0 = Front[S,N,E,W] per dat
col order, row 1 = Back[W,N], cursor, icon).  We only compare against
Front cells -- our hex bake emits the whole portal as Front with Back
empty, so the apples-to-apples target is upstream Front.

This harness renders through `tunnel_square_viewpoint()` (4 cardinals,
square dimetric -- matches upstream's authoring) rather than the
production `tunnel_hex_viewpoint()`: hex would render 6 facings that
don't have upstream counterparts.  Calibration here pins lighting /
strip-set / camera fidelity against the upstream PNG; the hex bake
then reuses the same blend through the hex projection.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

CELL = 128

# Square-cardinal facing labels for the calibration render -- match
# `tunnel_square_viewpoint()`'s facing order (cam_z 45/135/225/315 =
# S/N/E/W per upstream's tunnel convention).  Production bake uses
# `pak.dat.TUNNEL_FACING_LABELS` (6 hex edges); the two sets are
# independent.
SQUARE_FACING_LABELS: tuple[str, ...] = ("S", "N", "E", "W")

# Upstream `ways/rail-tunnel-stone.png` Front-cell columns by facing.
# Row 0; column order matches the dat's `FrontImage[<F>][0]=...0.<col>`
# lines.  Same shape across the stone-tunnel family (canal-tunnel,
# road-tunnel-stone, etc. share the convention; brick-faced and
# multi-portal tunnels add extra cells that aren't modelled here yet).
UPSTREAM_FRONT_COL = {"S": 0, "N": 1, "E": 2, "W": 3}


@dataclass(frozen=True)
class FacingMetric:
    facing: str
    iou: float
    xor_px: int
    drgb: float


# Calibration floor.  Tunnels are at "whole-portal vs upstream-Front-
# half" so the IoU is fundamentally limited (upstream Front is a
# sub-region of the full silhouette).  Pin the floor below current
# numbers (~0.65) so the check passes on the first commit and drops
# only if our render drifts substantially.  Tighten when alignment
# is closer to upstream's.
FAIL_IOU: float = 0.50


def _upstream_front_cell(atlas, facing: str):
    from pak.diff import key_magic_pink_to_alpha
    col = UPSTREAM_FRONT_COL[facing]
    return key_magic_pink_to_alpha(
        atlas.crop((col * CELL, 0, col * CELL + CELL, CELL))
    )


def _ours_cell(rendered_atlas_path: Path, facing: str):
    """Slice the calibration render atlas (single-row 4-cell, columns
    S/N/E/W per `SQUARE_FACING_LABELS`) at the given facing."""
    from PIL import Image
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
    import numpy as np
    from PIL import Image

    from pak.bake import fetch_blend_by_source, run_render
    from pak.compose import compose_atlas
    from pak.diff import MAGIC_PINK, GridCell, cell_metric, compose_grid
    from pak.fetch_pak import fetch as fetch_pak
    from pak.upstream import image_stem
    from pak.viewpoints import tunnel_square_viewpoint

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

    cells: list[GridCell] = []
    metrics: list[FacingMetric] = []
    for facing in SQUARE_FACING_LABELS:
        ours = np.asarray(_ours_cell(rendered, facing))
        up = np.asarray(_upstream_front_cell(atlas, facing))
        m, om, um = cell_metric(ours, up, alpha_threshold=0,
                                magic_rgb=MAGIC_PINK)
        metrics.append(FacingMetric(facing=facing, iou=m.iou,
                                    xor_px=m.xor_px, drgb=m.drgb))
        cells.append(GridCell(ours, up, om, um, f"Front[{facing}]"))
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
    import argparse

    from pak import REPO_ROOT
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
