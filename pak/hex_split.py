"""Hex per-tile cutter.

Counterpart to `pak.sq_split`.  Same projection-agnostic driver in
`pak.cell_split`; this module supplies the hex specifics:

  * `hex_polygon_bottom_trim` -- the bottom-corner region outside the
    hex polygon (analogue of square's `_bottom_triangles`).
  * `cell_anchors` over hex axial `(qx, ry, h)` keys -- screen lattice
    via `hex_tile_screen_offset` plus per-`h` `paksize` shift.
  * `_paint_key` -- back-first sort under the hex projection.
"""

from __future__ import annotations

import numpy as np

from pak import cell_split
from pak.hex_synth import DEFAULT_W


def hex_tile_screen_offset(qx: int, ry: int) -> tuple[float, float]:
    """Image-space pixel offset for tile `(qx, ry)` under the standard
    hex camera (`ortho_scale=2R`, image width `DEFAULT_W`).

    Derivation: world `(1.5·R·qx, -√3/2·R·qx - √3·R·ry, 0)` projects to
    screen `(W/(2R)·wx, -W/(2R·√3)·wy)` under `hex_proj_shear`.
    Substituting and flipping y for top-down image coords gives:

        cx_px = 0.75 · W · qx
        cy_px = 0.25 · W · qx + 0.5 · W · ry
    """
    return (0.75 * DEFAULT_W * qx,
            0.25 * DEFAULT_W * qx + 0.5 * DEFAULT_W * ry)


def hex_polygon_bottom_trim(image_width: int = DEFAULT_W) -> np.ndarray:
    """Bottom-corner region outside the hex polygon -- the hex analogue
    of `pak.sq_split._bottom_triangles`.  True = trim from ground cells.

    Hex polygon anchored at `(W/2, 3W/4)` with corners at `(±W/2, 0)`
    and `(±W/4, ±W/4)`.  Below the anchor (`dy >= 0`), the polygon
    requires `|dx| + dy <= W/2` (the two lower flanks); outside that =
    bottom-trim.  Half-open intervals (`>` not `>=`) match the square's
    convention so neighbour tiles partition without double-claim."""
    half = image_width // 2
    quarter = image_width // 4
    ys, xs = np.indices((image_width, image_width))
    dx = xs - half
    dy = ys - 3 * image_width // 4
    below_anchor = dy >= 0
    outside_lower_flanks = (dy > quarter) | (np.abs(dx) + dy > half)
    return below_anchor & outside_lower_flanks


def _paint_key(k):
    """Back-first paint order under hex projection.  Tile depth proxy
    is screen y of the tile at h=0 (= `0.25·qx + 0.5·ry`); within tile,
    `h` ascending."""
    qx, ry, h = k
    return (0.25 * qx + 0.5 * ry, h, qx, ry)


def _is_ground(k):
    return k[2] == 0


def _lattice(image_width: int) -> cell_split.Lattice:
    return cell_split.Lattice(
        box=image_width,
        ground_anchor=(image_width // 2, 3 * image_width // 4),
        bottom_trim=hex_polygon_bottom_trim(image_width),
        paint_key=_paint_key,
        is_ground=_is_ground,
    )


def cell_anchors(
    cells_qrh,
    *,
    image_width: int = DEFAULT_W,
) -> dict[tuple[int, int, int], tuple[int, int]]:
    """Map each `(qx, ry, h)` to its ground anchor in a canvas frame
    whose origin sits at `(0, 0)`.  Caller's `stitch` shifts the result
    into positive canvas coords.  Heights stack at `image_width` px per
    `h` step, matching square's `-h * paksize` convention."""
    out: dict[tuple[int, int, int], tuple[int, int]] = {}
    for k in cells_qrh:
        qx, ry, h = k
        dx, dy = hex_tile_screen_offset(qx, ry)
        out[k] = (int(round(dx)), int(round(dy)) - h * image_width)
    return out


def cell_keep_masks(
    cells_qrh,
    *,
    image_width: int = DEFAULT_W,
) -> dict[tuple[int, int, int], np.ndarray]:
    """Per-cell keep-masks for the given hex footprint.  Used by
    `pak.viewpoints` to wire `alpha_mask` per Slice."""
    anchors = cell_anchors(cells_qrh, image_width=image_width)
    return cell_split.cell_keep_masks(anchors, _lattice(image_width))


def stitch(
    cells,
    anchors,
    *,
    into_canvas: np.ndarray | None = None,
    pad: int = 16,
    image_width: int = DEFAULT_W,
):
    return cell_split.stitch(cells, anchors, _lattice(image_width),
                             into_canvas=into_canvas, pad=pad)


def split(
    canvas: np.ndarray,
    anchors,
    *,
    image_width: int = DEFAULT_W,
):
    """Hex wrapper around `pak.cell_split.split`."""
    return cell_split.split(canvas, anchors, _lattice(image_width))


def claim_mask(
    cells,
    anchors,
    canvas_shape,
    *,
    image_width: int = DEFAULT_W,
):
    return cell_split.claim_mask(cells, anchors, canvas_shape,
                                 _lattice(image_width))
