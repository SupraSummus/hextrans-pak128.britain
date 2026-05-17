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
