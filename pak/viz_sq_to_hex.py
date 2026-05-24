"""Visualise `pak.sq_to_hex.sq_to_hex_footprint` outputs in world coords.

Axiom: sq tile edge = hex tile edge = 1 world unit (see sq_to_hex
module docstring).  This view draws the sq rectangle and the regular
hex polygons at their actual world geometry — sq footprint as a
`dims_x × dims_y` rectangle, hex tiles as regular hexagons of edge 1.

Output: `out/sq_to_hex.png`.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from pak.sq_to_hex import (
    CANDIDATE_OFFSETS,
    HEX_EDGE,
    SQRT3,
    hex_world_center,
    sq_to_hex_footprint,
)

# Flat-top regular hex with edge 1, corners on x-axis.
HEX_CORNERS = np.array([
    (HEX_EDGE, 0.0),
    (0.5 * HEX_EDGE, SQRT3 / 2.0 * HEX_EDGE),
    (-0.5 * HEX_EDGE, SQRT3 / 2.0 * HEX_EDGE),
    (-HEX_EDGE, 0.0),
    (-0.5 * HEX_EDGE, -SQRT3 / 2.0 * HEX_EDGE),
    (0.5 * HEX_EDGE, -SQRT3 / 2.0 * HEX_EDGE),
], dtype=float)


def _sq_rect_corners(dims_x: float, dims_y: float,
                     centroid: tuple[float, float],
                     rotation_deg: float) -> np.ndarray:
    """`dims_x × dims_y` rectangle, rotated by `rotation_deg`, placed
    at `centroid`.  Returns 4 corners CCW in world coords."""
    hw, hh = dims_x / 2.0, dims_y / 2.0
    local = np.array([(-hw, -hh), (+hw, -hh), (+hw, +hh), (-hw, +hh)])
    th = math.radians(rotation_deg)
    R = np.array([[math.cos(th), -math.sin(th)],
                  [math.sin(th), math.cos(th)]])
    return (local @ R.T) + np.array(centroid)


def _plot_footprint(ax, dims_x: int, dims_y: int) -> None:
    fp = sq_to_hex_footprint(dims_x, dims_y)
    centroid = CANDIDATE_OFFSETS[fp.anchor_kind]

    # We have normalised cells (min q = min r = 0).  Re-run the
    # rasterisation to get the un-normalised cells so the picture
    # places everything in the hex frame around the chosen anchor.
    from pak.sq_to_hex import _hex_cells_overlapping_rect
    raw = _hex_cells_overlapping_rect(
        dims_x, dims_y, centroid, rotation_deg=fp.rotation_deg)

    qs = [q for q, _r in raw]
    rs = [r for _q, r in raw]
    pad = 1
    q_lo, q_hi = min(qs) - pad, max(qs) + pad
    r_lo, r_hi = min(rs) - pad, max(rs) + pad

    # Background hex grid (light outline).
    for q in range(q_lo, q_hi + 1):
        for r in range(r_lo, r_hi + 1):
            cx, cy = hex_world_center(q, r)
            poly = HEX_CORNERS + np.array([cx, cy])
            ax.add_patch(mpatches.Polygon(
                poly, closed=True, facecolor="none",
                edgecolor="#cccccc", linewidth=0.5, zorder=1))

    # Claimed hex tiles (blue fill + axial label).
    claimed = set(raw)
    for q, r in claimed:
        cx, cy = hex_world_center(q, r)
        poly = HEX_CORNERS + np.array([cx, cy])
        ax.add_patch(mpatches.Polygon(
            poly, closed=True, facecolor="#7fb4ff",
            edgecolor="#003a87", linewidth=1.5, alpha=0.55,
            zorder=2))
        ax.text(cx, cy, f"({q},{r})", ha="center", va="center",
                fontsize=7, color="#001a40", zorder=4)

    # Sq footprint rectangle (yellow, dashed outline).
    rect = _sq_rect_corners(dims_x, dims_y, centroid, fp.rotation_deg)
    ax.add_patch(mpatches.Polygon(
        rect, closed=True, facecolor="#ffe169",
        edgecolor="#b07f00", linewidth=1.5, linestyle="--",
        alpha=0.65, zorder=3))

    # Per-sq-tile gridlines on the rectangle (so the sq cell layout
    # reads at a glance).
    for i in range(dims_x + 1):
        u = -dims_x / 2.0 + i
        verts = np.array([(u, -dims_y / 2.0), (u, dims_y / 2.0)])
        th = math.radians(fp.rotation_deg)
        R = np.array([[math.cos(th), -math.sin(th)],
                      [math.sin(th), math.cos(th)]])
        v = (verts @ R.T) + np.array(centroid)
        ax.plot(v[:, 0], v[:, 1], color="#b07f00", linewidth=0.7,
                linestyle=":", zorder=3.2)
    for j in range(dims_y + 1):
        u = -dims_y / 2.0 + j
        verts = np.array([(-dims_x / 2.0, u), (dims_x / 2.0, u)])
        th = math.radians(fp.rotation_deg)
        R = np.array([[math.cos(th), -math.sin(th)],
                      [math.sin(th), math.cos(th)]])
        v = (verts @ R.T) + np.array(centroid)
        ax.plot(v[:, 0], v[:, 1], color="#b07f00", linewidth=0.7,
                linestyle=":", zorder=3.2)

    # Anchor point marker.
    ax.plot([centroid[0]], [centroid[1]], marker="o", color="red",
            markersize=5, zorder=5)

    # Frame view tightly.
    all_xs, all_ys = [], []
    for q in range(q_lo, q_hi + 1):
        for r in range(r_lo, r_hi + 1):
            cx, cy = hex_world_center(q, r)
            all_xs.append(cx)
            all_ys.append(cy)
    extra = 1.2
    ax.set_xlim(min(all_xs) - extra, max(all_xs) + extra)
    ax.set_ylim(min(all_ys) - extra, max(all_ys) + extra)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    rot_str = f"rot={fp.rotation_deg:.0f}°" if fp.rotation_deg else ""
    ax.set_title(
        f"sq {dims_x}x{dims_y}  ->  {fp.n_cells} hex  bbox={fp.bbox_qr}\n"
        f"anchor: {fp.anchor_kind}  {rot_str}",
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
    fig.suptitle(
        "sq_to_hex_footprint (world coords, edge=1): "
        "sq rectangle (yellow) -> hex cells (blue)",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    out = Path("out/sq_to_hex.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=120)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
