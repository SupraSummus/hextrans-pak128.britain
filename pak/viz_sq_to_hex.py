"""Visualise `pak.sq_to_hex.sq_to_hex_footprint` outputs.

Renders a grid of subplots, one per `(dims_x, dims_y)` footprint:
the sq diamond polygon (yellow), the claimed hex cells (blue fill +
outline, labelled with axial `(q, r)`), unclaimed neighbouring hex
cells (grey outline).  Title carries the winning anchor kind and the
cell count.  Output goes to `out/sq_to_hex.png`.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from pak.hex_split import hex_tile_screen_offset
from pak.sq_split import W
from pak.sq_to_hex import CANDIDATE_ANCHORS, sq_diamond_mask, sq_to_hex_footprint

HALF = W // 2
FOURTH = W // 4

# Hex polygon corners relative to the hex's ground anchor, in screen px.
# Anchor is at (W/2, 3W/4) inside the 128² sprite; polygon corners from
# `hex_polygon_bottom_trim`'s docstring.
HEX_CORNERS = np.array([
    (-HALF, 0),
    (-FOURTH, -FOURTH),
    (+FOURTH, -FOURTH),
    (+HALF, 0),
    (+FOURTH, +FOURTH),
    (-FOURTH, +FOURTH),
], dtype=float)


def _sq_diamond_corners(dims_x: int, dims_y: int) -> np.ndarray:
    """Outline of the union of sq cell diamonds (the footprint polygon)
    relative to the sq centroid."""
    # The outer hull is itself a diamond of size (dx+dy)*W/2 by (dx+dy)*W/4.
    w = (dims_x + dims_y) * HALF / 2
    h = (dims_x + dims_y) * FOURTH / 2
    return np.array([(0, -h), (+w, 0), (0, +h), (-w, 0)], dtype=float)


def _plot_footprint(ax, dims_x: int, dims_y: int) -> None:
    fp = sq_to_hex_footprint(dims_x, dims_y)
    mask, centroid = sq_diamond_mask(dims_x, dims_y)
    cx, cy = centroid

    # Re-derive hex anchor placement in the same canvas frame so the
    # picture's geometry matches the algorithm exactly.
    ox, oy = CANDIDATE_ANCHORS[fp.anchor_kind]
    hex_ax = cx + int(round(ox))
    hex_ay = cy + int(round(oy))

    # The cells coming back from `sq_to_hex_footprint` are normalised
    # to min-q=min-r=0.  To put them back at their actual screen
    # position, we need to undo that shift -- re-run the partition for
    # this anchor to find which axial offsets the claimed cells live
    # at in their native frame.
    from pak.sq_to_hex import _hex_cells_covering
    raw_claimed, _owner, anchors = _hex_cells_covering(
        mask, centroid, (ox, oy))

    # Show the sq diamond polygon (yellow fill, dashed outline)
    diam = _sq_diamond_corners(dims_x, dims_y) + np.array([cx, cy])
    ax.add_patch(mpatches.Polygon(diam, closed=True,
                                   facecolor="#ffe169", edgecolor="#b07f00",
                                   linewidth=1.5, linestyle="--", alpha=0.65,
                                   zorder=2))
    # Show individual sq cell anchors (small markers)
    xc = (dims_x - 1) / 2.0
    yc = (dims_y - 1) / 2.0
    for y in range(dims_y):
        for x in range(dims_x):
            sax = cx + HALF * (x - xc) - HALF * (y - yc)
            say = cy + FOURTH * (x - xc) + FOURTH * (y - yc)
            ax.plot([sax], [say], marker="+", color="#7a5500",
                    markersize=6, zorder=3)

    # Background grid of hex tiles around the cluster (faint outlines)
    qs = [q for q, _r in raw_claimed]
    rs = [r for _q, r in raw_claimed]
    pad = 1
    for q in range(min(qs) - pad, max(qs) + pad + 1):
        for r in range(min(rs) - pad, max(rs) + pad + 1):
            ax_x, ay_y = anchors[(q, r, 0)]
            poly = HEX_CORNERS + np.array([ax_x, ay_y])
            ax.add_patch(mpatches.Polygon(poly, closed=True,
                                          facecolor="none",
                                          edgecolor="#cccccc",
                                          linewidth=0.5, zorder=1))

    # Claimed hex cells (filled blue, axial label)
    claimed_set = set(raw_claimed)
    for q, r in raw_claimed:
        ax_x, ay_y = anchors[(q, r, 0)]
        poly = HEX_CORNERS + np.array([ax_x, ay_y])
        ax.add_patch(mpatches.Polygon(poly, closed=True,
                                      facecolor="#7fb4ff", edgecolor="#003a87",
                                      linewidth=1.5, alpha=0.55, zorder=2.5))
        ax.text(ax_x, ay_y, f"({q},{r})",
                ha="center", va="center", fontsize=7, color="#001a40",
                zorder=4)

    # Anchor point marker
    ax.plot([hex_ax], [hex_ay], marker="o", color="red", markersize=5,
            markerfacecolor="red", zorder=5)

    # Frame the view tightly
    all_xs = [anchors[(q, r, 0)][0] for q in range(min(qs), max(qs) + 1)
              for r in range(min(rs), max(rs) + 1)]
    all_ys = [anchors[(q, r, 0)][1] for q in range(min(qs), max(qs) + 1)
              for r in range(min(rs), max(rs) + 1)]
    extra = W
    ax.set_xlim(min(all_xs) - extra, max(all_xs) + extra)
    ax.set_ylim(max(all_ys) + extra, min(all_ys) - extra)  # y inverted
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(
        f"sq {dims_x}x{dims_y}  ->  {fp.n_cells} hex  bbox={fp.bbox_qr}\n"
        f"anchor: {fp.anchor_kind}",
        fontsize=9,
    )


def main() -> None:
    sizes = [(1, 1), (1, 2), (2, 1), (2, 2),
             (1, 3), (3, 1), (2, 3), (3, 2),
             (3, 3), (4, 4), (4, 2), (2, 4)]
    ncols = 4
    nrows = math.ceil(len(sizes) / ncols)
    fig, axes = plt.subplots(nrows, ncols,
                              figsize=(3.4 * ncols, 3.4 * nrows))
    axes = np.atleast_1d(axes).ravel()
    for ax, (n, m) in zip(axes, sizes, strict=False):
        _plot_footprint(ax, n, m)
    for ax in axes[len(sizes):]:
        ax.axis("off")
    fig.suptitle("sq_to_hex_footprint: sq diamond (yellow) -> hex cells (blue)",
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    out = Path("out/sq_to_hex.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=120)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
