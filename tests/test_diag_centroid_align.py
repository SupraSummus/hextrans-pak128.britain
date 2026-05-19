"""Tests for `pak.diag_centroid_align`'s joint offset solver.

The forward model rotates a model-local `(mx, my, mz)` by `R_z(step·L)`
before the cardinal dimetric projection -- a small trig expression
that's easy to get a sign wrong on and would silently emit wrong-
sign recommendations without these round-trip checks.

Run from the repo root::

    python3 -m unittest tests.test_diag_centroid_align
"""

from __future__ import annotations

import math
import unittest

import numpy as np

from pak.diag_centroid_align import (
    _R2_PIN_THRESHOLD,
    _SX,
    _SY,
    _SZ,
    _design_rows,
    recommend,
    solve_offset,
)


def _project(layouts: int, offset: tuple[float, float, float]
             ) -> list[tuple[int, int]]:
    """Generate the per-layout screen `(dx, dy)` shifts that
    `solve_offset` would observe under the forward model, rounded to
    int pixels as if read off the IoU sweep."""
    step_rad = math.radians(360.0 / layouts)
    m = np.array(offset, dtype=float)
    shifts: list[tuple[int, int]] = []
    for L in range(layouts):
        rows = _design_rows(step_rad * L)
        dx, dy = rows @ m
        shifts.append((int(round(dx)), int(round(dy))))
    return shifts


class TestDesignMatrix(unittest.TestCase):
    """L=0 design rows must match the cam_z=45° projection matrix."""

    def test_layout_zero_matches_M0(self) -> None:
        rows = _design_rows(0.0)
        # M_0 = [[+Sx, +Sx, 0], [+Sy, -Sy, -Sz]] at the L=0 (cam_z=45°)
        # projection; pinned by the perturbation harness against the
        # real renderer.
        np.testing.assert_allclose(rows[0], [+_SX, +_SX, 0.0])
        np.testing.assert_allclose(rows[1], [+_SY, -_SY, -_SZ])

    def test_pure_z_is_rotation_invariant(self) -> None:
        # +Z component projects to (0, -Sz) regardless of rotation.
        for theta in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
            rows = _design_rows(theta)
            self.assertAlmostEqual(rows[0, 2], 0.0)
            self.assertAlmostEqual(rows[1, 2], -_SZ)


class TestSolveRoundTrip(unittest.TestCase):
    """Synthetic round-trip: pin a known offset, project through the
    forward model, recover via `solve_offset`.  Each row exercises a
    different axis combination across the supported layout counts."""

    CASES = [
        # (layouts, (mx, my, mz))
        (4, (0.0,  0.0,  2.14)),  # pure-Z, the signalbox shape
        (2, (0.0,  0.0, -1.5 )),  # pure-Z on 2 layouts (180°-only)
        (4, (0.5,  0.0,  0.0 )),  # pure-X
        (4, (0.0, -0.6,  0.0 )),  # pure-Y (the column the bug broke)
        (4, (0.3, -0.4,  1.2 )),  # full XYZ
    ]

    def test_round_trip(self) -> None:
        for layouts, offset in self.CASES:
            with self.subTest(layouts=layouts, offset=offset):
                v, _, r2 = solve_offset(_project(layouts, offset))["xyz"]
                np.testing.assert_allclose(v, offset, atol=0.1)
                self.assertGreaterEqual(r2, 0.99)


class TestUnfittableConstantScreenDrift(unittest.TestCase):
    """A drift constant in screen space across rotated layouts cannot
    come from any model-local offset.  This is the stonehenge case --
    the joint XYZ R² should fall below the pin threshold and `recommend`
    should refuse to suggest a pin."""

    def test_constant_screen_drift_unfittable_4_layouts(self) -> None:
        # (-3, +3) px constant across all 4 layouts: nothing rotates, so
        # neither pure-XY nor joint XYZ can explain it.
        shifts = [(-3, 3)] * 4
        fit = solve_offset(shifts)
        xyz_r2 = fit["xyz"][2]
        self.assertLess(xyz_r2, _R2_PIN_THRESHOLD)
        text, suggestion = recommend(fit)
        self.assertIsNone(suggestion)
        self.assertIn("No model-local offset fits", text)


class TestRecommendPicksSimpler(unittest.TestCase):
    """When pure-Z fits within tolerance, prefer it over XYZ (Occam's
    razor); when only XYZ fits, pin XYZ -- the per-layout rotation is
    baked into the design matrix so model-local XY is safe to pin on
    multi-tile."""

    def test_pure_z_preferred_over_xyz(self) -> None:
        fit = solve_offset(_project(4, (0.0, 0.0, 2.14)))
        text, suggestion = recommend(fit)
        np.testing.assert_allclose(suggestion, (0.0, 0.0, 2.14), atol=0.05)
        self.assertIn("Pure-Z", text)

    def test_xy_fit_recommended_without_legacy_warning(self) -> None:
        # Old broken tool emitted a "WARNING: XY rotates with layout"
        # paragraph here -- the joint solver already inverted that
        # rotation, so the warning was misleading.
        fit = solve_offset(_project(4, (0.4, -0.3, 0.0)))
        text, suggestion = recommend(fit)
        self.assertIsNotNone(suggestion)
        self.assertIn("XYZ", text)
        self.assertNotIn("WARNING", text)


if __name__ == "__main__":
    unittest.main()
