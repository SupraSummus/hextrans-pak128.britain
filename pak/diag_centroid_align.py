"""Centroid-alignment diagnostic for the multi-tile calibration diff.

Walks the existing `out/diff/<asset>/` artefacts left by
`pak.check` on a multi-tile Building bake unit, reproduces the
per-layout upstream stitched canvas (same lattice + ground anchor
as `diff_buildings.run_multitile`), and sweeps a per-layout (dx,
dy) pixel offset to find the IoU peak.

Reports raw IoU, peak-aligned IoU, and the optimal (dx, dy)
per layout.  Also reports the world-XY translation that would
produce the screen offset under the cardinal dimetric projection,
as a starting suggestion for `Building.blend_model_offset_xyz` --
note the screen→world inverse is ambiguous between XY and Z
translation on the same screen-y axis, so the suggestion assumes
z=0 (most common case for buildings authored with footings on the
ground plane).

Run as::

    python3 -m pak.diag_centroid_align <bake_script.py>

Requires that `pak.check <bake_script>` has already been run so
the per-layout PNGs and the upstream cache are populated.

The diff itself does NOT auto-apply this offset -- if the residual
proves to be consistent positional drift, pin
`blend_model_offset_xyz` on the SPEC and re-run the diff to verify.
"""

from __future__ import annotations

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

# Dimetric world->screen rates at the upstream-normal-cardinal
# projection in our 512x512 canvas at the per-tile=24 standard ortho
# (ortho=48 effective).  Pixels-per-world on the camera plane =
# 512/48 = 10.67; camera at 45° azimuth, 30° elevation gives:
#   world +x → screen (+7.54, +3.78)  = 10.67·(cos 45°, sin 45°·sin 30°)
#   world +y → screen (-7.54, +3.78)
#   world +z → screen (0,    -9.24)   = 10.67·(0,        -cos 30°)
# The XY candidate assumes the drift is ground-plane displacement;
# the Z candidate assumes the model floats above/below z=0.  Picking
# between them: dy consistent across layouts + dx≈0 -> pure-Z drift
# (Z is rotation-invariant); (dx, dy) rotating with the layout -> XY
# drift -- but that one can't be pinned via `blend_model_offset_xyz`
# on multi-tile assets (see CLAUDE.md -> "blend_model_offset_xyz
# applies pre-rotation, model-local").
_WORLD_TO_SCREEN_X_PER_WORLD = 7.54
_WORLD_TO_SCREEN_Y_PER_WORLD = 3.78
_WORLD_TO_SCREEN_Z_PER_WORLD = 9.24


def _screen_to_world_z(dy: int) -> float:
    """SPEC.z candidate.  `_iou_shift`'s screen-y is image-down, world
    +Z is image-up, and the renderer applies `Translation(-offset)`
    -- the signs cancel to a straight division."""
    return -dy / _WORLD_TO_SCREEN_Z_PER_WORLD


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


def _screen_to_world_xy(dx: int, dy: int) -> tuple[float, float]:
    """Inverse-project the per-layout best-shift screen offset to the
    world XY (z=0) translation that should be declared on SPEC as
    `blend_model_offset_xyz` to compensate.

    The best-shift is the offset to apply to upstream so it aligns with
    ours -- equivalently, ours sits at `-best_shift` relative to
    upstream.  To move ours TOWARD upstream we need to ADD `+best_shift`
    to ours' world translation.  The renderer applies
    `Translation(-blend_model_offset_xyz)` to the mesh, so the SPEC
    value equals the world translation we want NEGATED, i.e. the world
    inverse of `+best_shift` directly (no extra negation -- the
    renderer's `-` cancels with the "we want ours to move by
    +best_shift" relation)."""
    a = dx / _WORLD_TO_SCREEN_X_PER_WORLD
    b = dy / _WORLD_TO_SCREEN_Y_PER_WORLD
    return ((a + b) / 2.0, (b - a) / 2.0)


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
    our_canvases = _load_our_renders(out_dir, render_name, layouts)

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
    print(f"  {'L':<3} {'raw IoU':>9} {'aligned':>9} {'dx':>5} {'dy':>5}"
          f"  {'wx (z=0)':>9} {'wy (z=0)':>9} {'wz (xy=0)':>10}")
    dxs, dys = [], []
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
        wx, wy = _screen_to_world_xy(dx, dy)
        wz = _screen_to_world_z(dy)
        dxs.append(dx); dys.append(dy)
        print(f"  {L:<3} {raw:>9.3f} {peak:>9.3f} {dx:>5} {dy:>5}"
              f"  {wx:>+9.2f} {wy:>+9.2f} {wz:>+10.2f}")
    mdx, mdy = sum(dxs) / len(dxs), sum(dys) / len(dys)
    mwx, mwy = _screen_to_world_xy(round(mdx), round(mdy))
    mwz = _screen_to_world_z(mdy)
    print(f"  --  mean offset: screen ({mdx:+.1f},{mdy:+.1f}), "
          f"world (xy, z=0): ({mwx:+.2f},{mwy:+.2f}); "
          f"world (xy=0, z): {mwz:+.2f}")
    print( "      Pick Z when dy is consistent and dx ≈ 0 (rotation-"
          "invariant, safe on multi-tile).  XY only applies on single-"
          "tile assets -- multi-tile XY can't be pinned today.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
