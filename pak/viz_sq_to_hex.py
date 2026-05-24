"""Visualise `pak.sq_to_hex` placements in world coords.

Writes `out/sq_to_hex.png`: one row per `(dims_x, dims_y)` size, one
column per anchor placement that ties for minimum cell count.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from pak.sq_to_hex import (
    CANDIDATE_OFFSETS,
    HEX_TILE_RADIUS,
    SQ_ROTATION_DEG,
    HexFootprint,
    hex_cells_overlapping_rect,
    hex_world_center,
    sq_to_hex_all_minimal,
)
from pak.way import HEX_CORNERS as _HEX_CORNERS_BY_DIR

HEX_CORNERS = np.array(
    [_HEX_CORNERS_BY_DIR[d] for d in ("E", "NE", "NW", "W", "SW", "SE")],
    dtype=float,
)


def _to_world(local_xy: np.ndarray, centroid: tuple[float, float],
              rotation_deg: float) -> np.ndarray:
    th = math.radians(rotation_deg)
    R = np.array([[math.cos(th), -math.sin(th)],
                  [math.sin(th),  math.cos(th)]])
    return (local_xy @ R.T) + np.array(centroid)


def _plot_placement(ax, dims_x: int, dims_y: int, fp: HexFootprint) -> None:
    centroid = CANDIDATE_OFFSETS[fp.anchor_kind]
    raw = hex_cells_overlapping_rect(dims_x, dims_y, centroid)

    qs = [q for q, _ in raw]
    rs = [r for _, r in raw]
    pad = 1
    for q in range(min(qs) - pad, max(qs) + pad + 1):
        for r in range(min(rs) - pad, max(rs) + pad + 1):
            cx, cy = hex_world_center(q, r)
            ax.add_patch(mpatches.Polygon(
                HEX_CORNERS + (cx, cy), closed=True, facecolor="none",
                edgecolor="#cccccc", linewidth=0.5, zorder=1))

    for q, r in raw:
        cx, cy = hex_world_center(q, r)
        ax.add_patch(mpatches.Polygon(
            HEX_CORNERS + (cx, cy), closed=True, facecolor="#7fb4ff",
            edgecolor="#003a87", linewidth=1.5, alpha=0.55, zorder=2))
        ax.text(cx, cy, f"({q},{r})", ha="center", va="center",
                fontsize=7, color="#001a40", zorder=4)

    hw, hh = dims_x / 2.0, dims_y / 2.0
    rect_local = np.array([(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)])
    rect = _to_world(rect_local, centroid, SQ_ROTATION_DEG)
    ax.add_patch(mpatches.Polygon(
        rect, closed=True, facecolor="#ffe169", edgecolor="#b07f00",
        linewidth=1.5, linestyle="--", alpha=0.65, zorder=3))

    for i in range(dims_x + 1):
        line = _to_world(
            np.array([(-hw + i, -hh), (-hw + i, hh)]),
            centroid, SQ_ROTATION_DEG)
        ax.plot(line[:, 0], line[:, 1], color="#b07f00",
                linewidth=0.7, linestyle=":", zorder=3.2)
    for j in range(dims_y + 1):
        line = _to_world(
            np.array([(-hw, -hh + j), (hw, -hh + j)]),
            centroid, SQ_ROTATION_DEG)
        ax.plot(line[:, 0], line[:, 1], color="#b07f00",
                linewidth=0.7, linestyle=":", zorder=3.2)

    ax.plot([centroid[0]], [centroid[1]], marker="o", color="red",
            markersize=5, zorder=5)

    cs = [hex_world_center(q, r) for q, r in raw]
    pad_world = 1.5 * HEX_TILE_RADIUS
    ax.set_xlim(min(c[0] for c in cs) - pad_world,
                max(c[0] for c in cs) + pad_world)
    ax.set_ylim(min(c[1] for c in cs) - pad_world,
                max(c[1] for c in cs) + pad_world)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"{dims_x}x{dims_y}  {fp.anchor_kind}\n"
                 f"bbox={fp.bbox_qr}", fontsize=8)


def _row_placements(n: int, m: int) -> list[tuple[int, int, HexFootprint]]:
    """All minimal placements for `(n, m)` and (when asymmetric) `(m, n)`,
    deduplicated by normalised cell set."""
    seen: set[tuple[tuple[int, int], ...]] = set()
    out: list[tuple[int, int, HexFootprint]] = []
    pairs = [(n, m)] if n == m else [(n, m), (m, n)]
    for dx, dy in pairs:
        for fp in sq_to_hex_all_minimal(dx, dy):
            if fp.cells in seen:
                continue
            seen.add(fp.cells)
            out.append((dx, dy, fp))
    return out


def main() -> None:
    sizes = [(1, 1), (1, 2), (2, 2), (1, 3), (2, 3), (3, 3),
             (2, 4), (3, 4), (4, 4)]
    rows = [(n, m, _row_placements(n, m)) for n, m in sizes]
    ncols = max(len(fps) for _, _, fps in rows)
    nrows = len(rows)
    fig, axes = plt.subplots(nrows, ncols,
                              figsize=(3.0 * ncols, 3.0 * nrows),
                              squeeze=False)
    for row_idx, (n, m, fps) in enumerate(rows):
        for col_idx in range(ncols):
            ax = axes[row_idx, col_idx]
            if col_idx < len(fps):
                dx, dy, fp = fps[col_idx]
                _plot_placement(ax, dx, dy, fp)
            else:
                ax.axis("off")
        label = f"{n}x{m}" if n == m else f"{n}x{m} / {m}x{n}"
        axes[row_idx, 0].set_ylabel(
            f"{label}\n-> {fps[0][2].n_cells} hex",
            fontsize=10, rotation=0, labelpad=40, ha="right", va="center",
        )
    fig.suptitle(
        "sq_to_hex: all anchor placements tied for minimum cell count",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    out = Path("out/sq_to_hex.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=120)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
