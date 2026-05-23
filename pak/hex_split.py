"""Hex per-tile cutter.

Counterpart to `pak.sq_split`.  Same projection-agnostic driver in
`pak.cell_split`; this module supplies the hex specifics:

  * `hex_polygon_bottom_trim` -- the bottom-corner region outside the
    hex polygon (analogue of square's `_bottom_triangles`).
  * `cell_anchors` over hex axial `(qx, ry, h)` keys -- screen lattice
    via `hex_tile_screen_offset` plus per-`h` `paksize` shift.
  * `_paint_key` -- back-first sort under the hex projection.

The legacy Voronoi-mask primitives (`hex_voronoi_mask`,
`hex_cell_shape_mask`, `hex_tile_pixel_mask`) remain exported for the
2D-remap-building path (`pak.remap_2d_building`), which partitions a
4-hex rhombus via Voronoi rather than going through the cutter.
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


def hex_voronoi_mask(
    my_offset: tuple[int, int],
    other_offsets: list[tuple[int, int]] = (),
    image_width: int = DEFAULT_W,
):
    """Pure projection-Voronoi mask for the hex lattice -- no cell-shape
    clip, no AA slack.  Retained for `pak.remap_2d_building` (the 4-hex
    rhombus partition); the cutter does NOT use it.

    The `hex_proj_shear` extrinsic compresses world y by `1/√3`, so
    world Euclidean distance² between two screen-px offsets `(Δx, Δy)`
    equals `(Δx² + 3·Δy²) / (W/2R)²`.
    """
    half = image_width // 2
    full = image_width
    ys, xs = np.indices((full, full))
    dx_cell = xs - half
    anchor_y = 3 * full // 4
    dy_cell = ys - anchor_y
    my_dist = dx_cell * dx_cell + 3 * dy_cell * dy_cell
    keep = np.ones((full, full), dtype=bool)
    mx, my = my_offset
    for ox, oy in other_offsets:
        rel_x, rel_y = ox - mx, oy - my
        rdx = dx_cell - rel_x
        rdy = dy_cell - rel_y
        other_dist = rdx * rdx + 3 * rdy * rdy
        keep &= (my_dist < other_dist) | (
            (my_dist == other_dist) & (rel_y < 0)
        )
    return keep.astype(np.float32)


def hex_cell_shape_mask(image_width: int = DEFAULT_W):
    """Hex polygon mask with `+1` AA slack.  Retained for
    `pak.remap_2d_building`; the cutter uses `hex_polygon_bottom_trim`
    directly."""
    half = image_width // 2
    quarter = image_width // 4
    full = image_width
    ys, xs = np.indices((full, full))
    dx_cell = xs - half
    anchor_y = 3 * full // 4
    dy_cell = ys - anchor_y
    abs_x = np.abs(dx_cell)
    abs_y = np.abs(dy_cell)
    return ((abs_y <= quarter + 1)
            & (abs_x + abs_y <= half + 1)).astype(np.float32)


def hex_tile_pixel_mask(
    my_offset: tuple[int, int],
    other_offsets: list[tuple[int, int]] = (),
    image_width: int = DEFAULT_W,
):
    """Legacy Voronoi-intersect-shape mask.  Retained for
    `pak.remap_2d_building`; the cutter does NOT use it."""
    return (hex_voronoi_mask(my_offset, other_offsets, image_width)
            * hex_cell_shape_mask(image_width))


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
