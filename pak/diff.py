"""Shared helpers for the per-asset-class diff harnesses.

`diff_upstream.py`, `diff_buildings.py`, `diff_trees.py`,
`diff_grounds.py` and `diff_fence.py` each render an asset through the
square viewpoint, slice cells out of the upstream pakset PNG, and
report silhouette IoU + RGB-delta + an XOR visualisation.  The
per-class logic (layout permutation, slope→cell mapping, (age,
season) grid, multi-facing OR) stays in each harness; the numerical
and image primitives below are the shared core.

Threshold choice is the caller's: vehicles & trees use `alpha>16`
(historical calibration); buildings & fence use `alpha>0` (so EEVEE's
soft-AA edges aren't dropped — see `diff_buildings._silhouette_mask`
docstring for the calibration story).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

# Upstream pak128.Britain's transparency key colour.  RGB PNGs with this
# pixel value mark "outside the silhouette" — the engine reads it as
# transparent.  Our renders write proper RGBA so this only matters when
# reading upstream PNGs.
MAGIC_PINK: tuple[int, int, int] = (231, 255, 255)


def checker(sz: int,
            c1: tuple[int, int, int] = (210, 210, 210),
            c2: tuple[int, int, int] = (180, 180, 180),
            step: int = 8):
    """RGBA checker-pattern background of size `sz`x`sz`.  Pasted under
    each diff cell so transparent regions visibly differ from
    silhouette-grey ones in the rendered grid."""
    from PIL import Image
    a = np.zeros((sz, sz, 3), dtype=np.uint8)
    ys, xs = np.indices((sz, sz))
    mask = ((xs // step + ys // step) % 2 == 0)
    a[mask] = c1
    a[~mask] = c2
    return Image.fromarray(a, "RGB").convert("RGBA")


def silhouette_mask(arr: np.ndarray, *,
                    alpha_threshold: int = 0,
                    magic_rgb: tuple[int, int, int] | None = None
                    ) -> np.ndarray:
    """Boolean (H, W) mask of opaque-and-not-keyed pixels.

    Accepts RGBA (4-channel) or RGB (3-channel) arrays.  Upstream
    grounds & fence PNGs are RGB-only and rely entirely on `magic_rgb`
    for transparency; everywhere else the input is RGBA.

    `alpha_threshold`: only pixels with alpha > this count as silhouette.
    Caller-tunable because vehicles & trees calibrate at `>16` (drops
    EEVEE/Cycles edge AA) while buildings & fence calibrate at `>0`
    (keeps the AA edge ring).  Ignored on RGB input.

    `magic_rgb`: if set, RGB pixels matching this tuple are excluded
    from the silhouette.  Used when reading upstream PNGs that mark
    transparency via colour rather than alpha; `MAGIC_PINK` is the
    pak128.Britain convention."""
    if arr.shape[-1] == 4:
        sil = arr[..., 3] > alpha_threshold
    else:
        sil = np.ones(arr.shape[:2], dtype=bool)
    if magic_rgb is not None:
        r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
        keyed = ((r == magic_rgb[0])
                 & (g == magic_rgb[1])
                 & (b == magic_rgb[2]))
        sil = sil & ~keyed
    return sil


def iou(mask_a: np.ndarray, mask_b: np.ndarray) -> float:
    """Silhouette intersection-over-union.  Returns 0.0 when union is
    empty (so an empty render reports as a failure rather than a
    perfect match; the mathematical "two empty masks are identical"
    answer would mask exactly the bug we want IoU to surface)."""
    inter = int(np.logical_and(mask_a, mask_b).sum())
    union = int(np.logical_or(mask_a, mask_b).sum())
    return inter / max(union, 1)


def drgb_intersection(rgba_a: np.ndarray, rgba_b: np.ndarray,
                      mask_a: np.ndarray, mask_b: np.ndarray,
                      blur_sigma: float = 0.0) -> float:
    """Mean abs(RGB-delta) over the whole image.  The two renders are
    first composited onto a common background (`MAGIC_PINK`, matching
    upstream's keying) using each side's silhouette mask, then
    optionally Gaussian-blurred by `blur_sigma`, then diffed across
    every pixel (silhouette XOR regions included).

    Common-background composite removes the "ours-zero vs upstream-pink
    transparent region" gap that would otherwise dominate any all-pixel
    metric, and means a naive RGB blur is safe -- both sides have the
    same out-of-silhouette colour so blur kernels don't smear different
    backgrounds into each side's edge pixels asymmetrically.

    The all-pixel coverage (vs the previous intersection-only) means
    silhouette XOR pixels contribute to the metric: where one side has
    surface and the other has background, the per-pixel delta is the
    surface-vs-pink gap.  Treats colour drift and modest geometry drift
    as the same problem -- both shift pixels off-target -- which is the
    right framing for the calibration-target metric we use here."""
    if not (mask_a.any() or mask_b.any()):
        return float("nan")
    bg = np.array(MAGIC_PINK, dtype=np.float32)
    a = np.where(mask_a[..., None],
                 rgba_a[..., :3].astype(np.float32),
                 bg[None, None, :])
    b = np.where(mask_b[..., None],
                 rgba_b[..., :3].astype(np.float32),
                 bg[None, None, :])
    if blur_sigma > 0:
        from scipy.ndimage import gaussian_filter
        a = np.stack([gaussian_filter(a[..., c], sigma=blur_sigma)
                      for c in range(3)], axis=-1)
        b = np.stack([gaussian_filter(b[..., c], sigma=blur_sigma)
                      for c in range(3)], axis=-1)
    return float(np.abs(a - b).mean())


def xor_image(mask_a: np.ndarray, mask_b: np.ndarray) -> np.ndarray:
    """Three-colour silhouette XOR visualisation as an (H, W, 4) RGBA
    array.  Red = only-a, blue = only-b, grey = intersection,
    transparent elsewhere.  Surfaces contour drift at a glance in the
    diff grids."""
    h, w = mask_a.shape
    img = np.zeros((h, w, 4), dtype=np.uint8)
    only_a = mask_a & ~mask_b
    only_b = mask_b & ~mask_a
    inter = mask_a & mask_b
    img[only_a] = (230, 60, 60, 255)
    img[only_b] = (60, 90, 230, 255)
    img[inter] = (180, 180, 180, 255)
    return img


@dataclass(frozen=True)
class CellMetric:
    """Per-cell silhouette IoU + XOR pixel count + mean RGB delta.  The
    three numbers each diff harness reports per facing / layout / (age,
    season) cell; per-class wrappers add their own keying fields around
    these (see `diff_upstream.FacingMetric`, `diff_trees.CellMetric`)."""
    iou: float
    xor_px: int
    drgb: float


def cell_metric(ours_rgba: np.ndarray, up_rgba: np.ndarray, *,
                alpha_threshold: int = 0,
                magic_rgb: tuple[int, int, int] | None = None,
                blur_sigma: float = 0.0,
                ) -> tuple[CellMetric, np.ndarray, np.ndarray]:
    """Silhouette IoU + symmetric-difference pixel count + RGB delta for
    one (ours, upstream) cell pair, plus the two silhouette masks the
    metric was computed against.  Callers reuse the masks for the XOR
    grid (or, in the buildings case, the IoU permutation matrix) without
    recomputing them."""
    our_mask = silhouette_mask(ours_rgba, alpha_threshold=alpha_threshold,
                               magic_rgb=magic_rgb)
    up_mask = silhouette_mask(up_rgba, alpha_threshold=alpha_threshold,
                              magic_rgb=magic_rgb)
    metric = CellMetric(
        iou=iou(our_mask, up_mask),
        xor_px=int((our_mask ^ up_mask).sum()),
        drgb=drgb_intersection(ours_rgba, up_rgba, our_mask, up_mask,
                               blur_sigma=blur_sigma),
    )
    return metric, our_mask, up_mask


@dataclass(frozen=True)
class GridCell:
    """One column of a 3-row diff grid: render-pair plus the masks used
    for the XOR row.  `label` is drawn above the column."""
    ours_rgba: np.ndarray
    up_rgba: np.ndarray
    our_mask: np.ndarray
    up_mask: np.ndarray
    label: str


def compose_grid(cells: list[GridCell], *,
                 out_path: Path,
                 strip_magic_rgb: tuple[int, int, int] | None = None,
                 cell_px: int = 128, pad: int = 8, label_h: int = 18) -> None:
    """Three-row diff grid (ours / upstream / silhouette-XOR) written to
    `out_path`.  One column per `GridCell`; `label` drawn above each.

    `strip_magic_rgb`: if upstream PNGs are RGB-with-key (the building
    case), pixels matching this colour are zeroed-alpha before pasting
    so the checker background reads through rather than rendering as
    solid pink.  Vehicles / trees ship upstream as proper RGBA and pass
    `None`.
    """
    from PIL import Image, ImageDraw

    cols = len(cells)
    rows = 3
    w = cols * (cell_px + pad) + pad
    h = rows * (cell_px + pad) + pad + label_h

    bg = checker(cell_px)
    grid = Image.new("RGBA", (w, h), (245, 245, 245, 255))
    draw = ImageDraw.Draw(grid)

    for i, cell in enumerate(cells):
        x = pad + i * (cell_px + pad)
        draw.text((x + 4, 2), cell.label, fill=(0, 0, 0, 255))
        ours_img = Image.fromarray(cell.ours_rgba, "RGBA")
        up_arr = cell.up_rgba
        if strip_magic_rgb is not None:
            up_arr = up_arr.copy()
            r, g, b = strip_magic_rgb
            keyed = ((up_arr[..., 0] == r)
                     & (up_arr[..., 1] == g)
                     & (up_arr[..., 2] == b))
            up_arr[keyed, 3] = 0
        up_img = Image.fromarray(up_arr, "RGBA")
        grid.paste(Image.alpha_composite(bg, ours_img), (x, label_h + pad))
        grid.paste(Image.alpha_composite(bg, up_img),
                   (x, label_h + pad + cell_px + pad))
        grid.paste(Image.fromarray(xor_image(cell.our_mask, cell.up_mask),
                                   "RGBA"),
                   (x, label_h + pad + 2 * (cell_px + pad)))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    grid.save(out_path)
