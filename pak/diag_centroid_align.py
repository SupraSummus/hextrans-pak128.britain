"""Centroid-alignment diagnostic for the multi-tile calibration diff.

Walks the existing `out/diff/<asset>/` artefacts left by
`pak.check` on a multi-tile Building bake unit, reproduces the
per-layout upstream stitched canvas (same lattice + ground anchor
as `diff_buildings.run_multitile`), and sweeps a per-layout (dx,
dy) pixel offset to find the IoU peak.

Joins the per-layout 2D measurements into a single model-local
3D offset by least squares.  Each layout L applies `R_z(step·L)`
to `blend_model_offset_xyz` before the cardinal dimetric projection
(`step = 360°/layouts`, the net cam-relative rotation in
`building_square_viewpoint`'s `2·step·l` model + `step·l` camera
convention), so a set of L per-layout (dx, dy) shifts is an
over-determined linear system in `(mx, my, mz)` for layouts ≥ 2.

Three sub-models are fit and ranked by R² (fraction of screen-
shift variance explained):

* **Joint XYZ.**  All three components free -- the true degree of
  freedom `blend_model_offset_xyz` exposes.
* **Pure-Z** (`mx = my = 0`).  Rotation-invariant under the per-
  layout Z rotation.  Preferred over joint XYZ when it suffices,
  by Occam's razor -- a Z-only asset would also fit the joint
  model with R² ≈ 1 and `mx, my` near zero, but the constrained
  fit gives the cleaner pin.
* **Pure-XY** (`mz = 0`).  Reported for diagnosis only.

Recommendation logic: pick pure-Z if it explains ≥ 90 % of the
shift variance.  Else if joint XYZ explains ≥ 90 %, pin XYZ
(safe on multi-tile -- the per-layout rotation is baked into the
design matrix, so the renderer applies the same rotation the
solver inverted).  Else flag the drift as not explainable by any
model-local offset -- either a post-rotation world translation is
needed (see TODO.md → "Multi-tile XY offset gap"), or the
residual isn't a translation at all (mesh stretched, alignment
mode wrong, …).

Run as::

    python3 -m pak.diag_centroid_align <bake_script.py>

Requires that `pak.check <bake_script>` has already been run so
the per-layout PNGs and the upstream cache are populated.

The diff itself does NOT auto-apply the offset -- pin
`blend_model_offset_xyz` on the SPEC from the recommendation and
re-run the diff to verify.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from pak import REPO_ROOT
from pak.bake_units import import_script, specs_of
from pak.dat import Building, building_footprint_centroid
from pak.diff import MAGIC_PINK
from pak.diff_buildings import (
    _atlas_cell,
    _load_our_renders,
    _parse_backimage_entries,
    _silhouette_mask,
    _stitch_upstream_layout,
)
from pak.fetch_pak import fetch as fetch_pak
from pak.upstream import image_stem

# Cardinal-camera projection rates on the 512×512 multi-tile canvas at
# the upstream-normal-cardinal projection (per-tile ortho=24, multi-tile
# canvas=2×).  Pixels-per-world on the camera plane = 512/48 = 10.67;
# the L=0 camera sits at azimuth=45°, elevation=30° (`(45, 135, 225,
# 315)` cardinal sequence in `_UPSTREAM_NORMAL_CARDINAL`).  Re-deriving
# the L=0 projection via `R_z(-45°)·R_x(-60°)` (with image-y down):
#   world +x → screen ( +Sx,  +Sy )
#   world +y → screen ( +Sx,  -Sy )
#   world +z → screen (   0,  -Sz )
# Combined L=0 projection matrix used by `_design_rows`:
#   M_0 = [[ +Sx, +Sx,   0 ],
#          [ +Sy, -Sy, -Sz ]]
# The Y column had its signs flipped in the original commit and was
# caught by `pak/_experiment_ground_truth.py`'s perturbation harness:
# the L=0 camera being at 45° (not 0°) puts world +y on the cam's
# "right" axis (same +Sx contribution as +x) and on the "below-horizon"
# axis (negative image-up contribution = positive screen-y).
_SX = 7.54
_SY = 3.78
_SZ = 9.24

# Fraction-of-variance-explained threshold above which a sub-model is
# considered to explain the per-layout drift.  Tuned for the integer-
# pixel IoU sweep: a "perfect" fit still has up to ±0.5 px rounding per
# axis per layout, so R² rarely reaches 1.0 even when the underlying
# offset is exact.  Empirical reference points on the ported multi-tile
# assets: signalbox at R²=0.95 (joint XYZ pin clears IoU 0.69 → 0.94),
# stonehenge at R²=0.05 (post-rotation world-frame drift -- correctly
# rejected, points at the TODO.md "Multi-tile XY offset gap" customer).
_R2_PIN_THRESHOLD = 0.9


def _iou_shift(our_mask: np.ndarray, up_mask: np.ndarray,
               dx: int, dy: int) -> float:
    shifted = np.roll(np.roll(up_mask, dy, axis=0), dx, axis=1)
    inter = np.logical_and(our_mask, shifted).sum()
    union = np.logical_or(our_mask, shifted).sum()
    return float(inter) / float(union) if union else 0.0


def _sweep_offset(our_mask: np.ndarray, up_mask: np.ndarray,
                  radius: int = 64) -> tuple[int, int, float]:
    best = (0, 0, _iou_shift(our_mask, up_mask, 0, 0))
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            i = _iou_shift(our_mask, up_mask, dx, dy)
            if i > best[2]:
                best = (dx, dy, i)
    return best


def _design_rows(theta_rad: float) -> np.ndarray:
    """The two rows of the (2·layouts × 3) design matrix for one layout.

    Maps a model-local `(mx, my, mz)` through `R_z(theta)` and then the
    L=0 (cam_z=45°) cardinal projection `M_0` to the screen `(dx, dy)`
    shift::

        rotated = (mx·cosθ - my·sinθ, mx·sinθ + my·cosθ, mz)
        dx      = +Sx·rotated_x + Sx·rotated_y
        dy      = +Sy·rotated_x - Sy·rotated_y - Sz·mz
    """
    c, s = math.cos(theta_rad), math.sin(theta_rad)
    return np.array([
        [ _SX * (c + s),  _SX * (c - s),  0.0],
        [ _SY * (c - s), -_SY * (c + s), -_SZ],
    ])


def _fit_offset(
    A_full: np.ndarray, b: np.ndarray, free_cols: tuple[int, ...],
) -> tuple[np.ndarray, np.ndarray, float]:
    """Constrained least-squares: solve `A[:, free_cols] · x = b`,
    return the full 3-vector (zero-padded), per-layout 2D residual, and
    fraction-of-variance-explained.
    """
    A = A_full[:, list(free_cols)]
    x, *_ = np.linalg.lstsq(A, b, rcond=None)
    full = np.zeros(3, dtype=float)
    for i, c in enumerate(free_cols):
        full[c] = x[i]
    pred = A @ x
    res = b - pred
    ss_res = float(np.sum(res * res))
    ss_tot = float(np.sum(b * b))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return full, res.reshape(-1, 2), r2


def solve_offset(shifts: list[tuple[int, int]]) -> dict:
    """Fit a single model-local `(mx, my, mz)` to the per-layout
    `(dx, dy)` screen shifts via least squares.

    `shifts[L]` is the optimal screen shift recovered from layout L's
    silhouette IoU sweep.  Per-layout rotation `step·L` with
    `step = 360°/layouts` matches `building_square_viewpoint`'s
    cam-relative convention.  Returns three named fits (`xyz`, `z`,
    `xy`) each as `(offset_3vec, per_layout_residual_Lx2, r2)`.
    """
    layouts = len(shifts)
    step_rad = math.radians(360.0 / layouts)
    A = np.vstack([_design_rows(step_rad * L) for L in range(layouts)])
    b = np.array([v for shift in shifts for v in shift], dtype=float)
    return {
        "xyz": _fit_offset(A, b, (0, 1, 2)),
        "z":   _fit_offset(A, b, (2,)),
        "xy":  _fit_offset(A, b, (0, 1)),
    }


def recommend(fit: dict) -> tuple[str, tuple[float, float, float] | None]:
    """Return `(text, offset_or_none)` recommendation.  `offset_or_none`
    is the suggested `blend_model_offset_xyz` tuple, or None when no
    model-local offset fits."""
    xyz_v, _, xyz_r2 = fit["xyz"]
    z_v, _, z_r2 = fit["z"]
    if z_r2 >= _R2_PIN_THRESHOLD:
        mz = float(z_v[2])
        return (
            f"Pure-Z explains {z_r2:.0%} of screen-shift variance; pin "
            f"blend_model_offset_xyz=(0.0, 0.0, {mz:+.2f}) "
            f"(rotation-invariant, multi-tile-safe).",
            (0.0, 0.0, mz),
        )
    if xyz_r2 >= _R2_PIN_THRESHOLD:
        mx, my, mz = float(xyz_v[0]), float(xyz_v[1]), float(xyz_v[2])
        return (
            f"Joint XYZ explains {xyz_r2:.0%} of screen-shift variance; "
            f"pin blend_model_offset_xyz=({mx:+.2f}, {my:+.2f}, "
            f"{mz:+.2f}).  (The fit's per-layout rotation is baked into "
            f"the design matrix, so a high-R² model-local XY is safe to "
            f"pin even on multi-tile assets -- the renderer applies the "
            f"same rotation the solver inverted.)",
            (mx, my, mz),
        )
    return (
        f"No model-local offset fits (best XYZ R²={xyz_r2:.0%}).  "
        f"Drift is likely constant in screen space (post-rotation "
        f"world translation -- see TODO.md → 'Multi-tile XY offset "
        f"gap') or not a translation at all (mesh stretched, "
        f"alignment-mode wrong, ...).",
        None,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    script = Path(argv[0]).resolve()
    mod = import_script(script)
    spec = specs_of(mod)[0]
    if not isinstance(spec, Building):
        raise SystemExit(f"{script.name}: SPEC is not a Building")
    if spec.dims_x <= 1 and spec.dims_y <= 1:
        raise SystemExit(f"{script.name}: single-tile, no multi-tile stitch")

    out_dir = REPO_ROOT / "out" / "diff" / script.stem
    if not out_dir.exists():
        raise SystemExit(
            f"{out_dir} not found -- run `python3 -m pak.check {script}` first"
        )
    layouts = spec.layouts or 4

    from PIL import Image

    render_name = Path(spec.blend).stem
    our_canvases = _load_our_renders(out_dir, render_name, layouts,
                                     multi_tile=True)

    up_dat_path = fetch_pak(spec.upstream_dat)
    up_png_path = fetch_pak(
        f"{image_stem(spec.upstream_dat, name=spec.name)}.png"
    )
    up_atlas = np.asarray(Image.open(up_png_path).convert("RGBA"))
    up_index = {
        (e["l"], e["y"], e["x"], e["h"], e["phase"], e["season"]):
            (e["row"], e["col"])
        for e in _parse_backimage_entries(up_dat_path, name=spec.name)
        if e["season"] == 0
    }
    centroid_by_L = {
        L: building_footprint_centroid(spec.dims_x, spec.dims_y, L)
        for L in range(layouts)
    }

    print(f"=== {script.name} centroid-alignment sweep ===")
    print(f"  {'L':<3} {'raw IoU':>9} {'aligned':>9} {'dx':>5} {'dy':>5}")
    shifts: list[tuple[int, int]] = []
    for L in range(layouts):
        cells_by_yx = {
            (k[1], k[2]): _atlas_cell(up_atlas, *up_index[k])
            for k in up_index if k[0] == L
        }
        up_stitched = _stitch_upstream_layout(
            cells_by_yx, centroid_by_L[L], magic_rgb=MAGIC_PINK,
        )
        our_mask = _silhouette_mask(our_canvases[L])
        up_mask = _silhouette_mask(up_stitched)
        raw = _iou_shift(our_mask, up_mask, 0, 0)
        dx, dy, peak = _sweep_offset(our_mask, up_mask)
        shifts.append((dx, dy))
        print(f"  {L:<3} {raw:>9.3f} {peak:>9.3f} {dx:>5} {dy:>5}")

    fit = solve_offset(shifts)
    print()
    print(f"  {'fit':<10} {'mx':>7} {'my':>7} {'mz':>7} {'R²':>6}  "
          f"{'max |res| (px)':>16}")
    for label in ("xyz", "z", "xy"):
        v, res, r2 = fit[label]
        max_res = float(np.max(np.abs(res)))
        print(f"  {label:<10} {v[0]:>+7.2f} {v[1]:>+7.2f} {v[2]:>+7.2f} "
              f"{r2:>6.2f}  {max_res:>16.1f}")
    text, _ = recommend(fit)
    print()
    print(f"  → {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
