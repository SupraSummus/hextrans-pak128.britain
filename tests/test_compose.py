"""Tests for `pak.compose` -- the parent-side atlas composer that
reads per-facing PNGs written by `pak.render` (the Blender script).

Run from the repo root:

    python3 -m unittest tests.test_compose
"""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from pak.compose import compose_atlas
from pak.render import Facing, Slice, Viewpoint


def _compose_silent(*args, **kwargs):
    """`compose_atlas` always prints a bbox summary -- noise in test
    output.  Swallow stdout for the call."""
    with contextlib.redirect_stdout(io.StringIO()):
        return compose_atlas(*args, **kwargs)


def _viewpoint(facings, image_width=4, canvas_width=None, canvas_height=None):
    """A bare Viewpoint that compose_atlas reads -- only the facing
    list and the sprite/canvas sizes matter; the bpy-facing fields
    (camera_ortho, sun_energy, fit_matrix, ...) compose never touches."""
    return Viewpoint(
        name="test",
        image_width=image_width,
        facings=facings,
        camera_ortho=lambda _: 1.0,
        sun_energy=lambda _: 1.0,
        fit_matrix=lambda _: tuple(tuple(0.0 for _ in range(4)) for _ in range(4)),
        canvas_width=canvas_width,
        canvas_height=canvas_height,
    )


def _facing(label, **kwargs):
    return Facing(
        label=label,
        camera_location=(0.0, 0.0, 0.0),
        camera_rotation_euler=(0.0, 0.0, 0.0),
        sun_rotation_euler=(0.0, 0.0, 0.0),
        **kwargs,
    )


def _solid_png(path: Path, w: int, h: int, rgba: tuple[int, int, int, int]):
    """Write a solid-colour PNG of the given size."""
    arr = np.full((h, w, 4), rgba, dtype=np.uint8)
    Image.fromarray(arr, "RGBA").save(path)


class TestComposeAtlas(unittest.TestCase):
    def test_single_row_per_facing_atlas(self):
        """Two facings, no slicing -- cells line up left-to-right in
        facing-list order."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            _solid_png(tmp / "asset_A.png", 4, 4, (255, 0, 0, 255))
            _solid_png(tmp / "asset_B.png", 4, 4, (0, 255, 0, 255))
            vp = _viewpoint([_facing("A"), _facing("B")])
            out_path = _compose_silent(
                vp, render_dir=tmp, out_dir=tmp, name="asset",
            )
            atlas = np.asarray(Image.open(out_path).convert("RGBA"))
            self.assertEqual(atlas.shape, (4, 8, 4))
            self.assertEqual(tuple(atlas[0, 0]), (255, 0, 0, 255))
            self.assertEqual(tuple(atlas[0, 4]), (0, 255, 0, 255))

    def test_cleanup_removes_per_facing_pngs_by_default(self):
        """keep_per_facing=False (default) deletes the per-facing PNGs
        after composing; bake.py relies on this so per-asset bake
        scripts don't ship stray `<name>_<facing>.png` siblings."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            _solid_png(tmp / "asset_A.png", 4, 4, (255, 0, 0, 255))
            _compose_silent(
                _viewpoint([_facing("A")]),
                render_dir=tmp, out_dir=tmp, name="asset",
            )
            self.assertFalse((tmp / "asset_A.png").exists())
            self.assertTrue((tmp / "asset.png").exists())

    def test_keep_per_facing_preserves_inputs(self):
        """Calibration diffs (diff_upstream, diff_trees, ...) need the
        per-facing PNGs to compare against upstream."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            _solid_png(tmp / "asset_A.png", 4, 4, (255, 0, 0, 255))
            _compose_silent(
                _viewpoint([_facing("A")]),
                render_dir=tmp, out_dir=tmp, name="asset",
                keep_per_facing=True,
            )
            self.assertTrue((tmp / "asset_A.png").exists())

    def test_slice_crops_offset_window_from_wide_canvas(self):
        """Multi-tile bakes render a wide canvas per Facing; each
        Slice crops a sprite_w×sprite_w window centred on
        `(canvas/2 + slice.offset)`.  Verifies the offset math
        directly -- this is the building_*_viewpoint -> compose
        contract."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            # 8-wide canvas with a 4×4 sprite_w: left half red, right
            # half green.  Slice offsets -2 (centre at canvas col 2)
            # and +2 (centre at canvas col 6) should crop a fully-red
            # cell and a fully-green cell respectively.
            canvas = np.zeros((4, 8, 4), dtype=np.uint8)
            canvas[:, :4] = (255, 0, 0, 255)
            canvas[:, 4:] = (0, 255, 0, 255)
            Image.fromarray(canvas, "RGBA").save(tmp / "asset_L0.png")
            slices = [
                Slice(label="L0_left", offset=(-2, 0), alpha_mask=None),
                Slice(label="L0_right", offset=(2, 0), alpha_mask=None),
            ]
            vp = _viewpoint(
                [_facing("L0", slices=slices)],
                image_width=4, canvas_width=8, canvas_height=4,
            )
            out_path = _compose_silent(
                vp, render_dir=tmp, out_dir=tmp, name="asset",
            )
            atlas = np.asarray(Image.open(out_path).convert("RGBA"))
            # Two 4×4 cells side-by-side.
            self.assertEqual(atlas.shape, (4, 8, 4))
            self.assertEqual(tuple(atlas[2, 0]), (255, 0, 0, 255))   # left slice
            self.assertEqual(tuple(atlas[2, 4]), (0, 255, 0, 255))   # right slice

    def test_slice_alpha_mask_clips_cell_alpha(self):
        """`Slice.alpha_mask` (per-pixel float [0,1]) multiplies the
        cell's alpha channel -- the pixel-ownership mechanism for
        multi-tile sprites that prevents overdraw between
        neighbours.  Verifies the cell's alpha drops where the mask
        is zero, RGB stays untouched."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            # 4×4 solid opaque red.
            _solid_png(tmp / "asset_L0.png", 4, 4, (255, 0, 0, 255))
            # Mask: left half opaque, right half transparent.
            mask = np.zeros((4, 4), dtype=np.float32)
            mask[:, :2] = 1.0
            slices = [Slice(label="L0_X0", offset=(0, 0), alpha_mask=mask)]
            vp = _viewpoint([_facing("L0", slices=slices)], image_width=4)
            out_path = _compose_silent(
                vp, render_dir=tmp, out_dir=tmp, name="asset",
            )
            atlas = np.asarray(Image.open(out_path).convert("RGBA"))
            self.assertEqual(atlas[0, 0, 3], 255)  # left: opaque survives
            self.assertEqual(atlas[0, 3, 3], 0)    # right: mask zeroed
            self.assertEqual(atlas[0, 0, 0], 255)  # RGB untouched on left
            self.assertEqual(atlas[0, 3, 0], 255)  # RGB untouched on right

    def test_keep_per_facing_writes_per_slice_pngs(self):
        """For sliced facings, keep_per_facing=True saves each Slice's
        cell to `<out>/<name>_<slice.label>.png` -- diff_buildings
        consumes those per-tile sprites."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            _solid_png(tmp / "asset_L0.png", 4, 4, (255, 0, 0, 255))
            slices = [Slice(label="L0_X0", offset=(0, 0), alpha_mask=None)]
            vp = _viewpoint([_facing("L0", slices=slices)], image_width=4)
            _compose_silent(
                vp, render_dir=tmp, out_dir=tmp, name="asset",
                keep_per_facing=True,
            )
            self.assertTrue((tmp / "asset_L0_X0.png").exists())


if __name__ == "__main__":
    unittest.main()
