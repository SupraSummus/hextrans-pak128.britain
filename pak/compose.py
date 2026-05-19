"""Atlas composition for renders produced by `pak.render` (the
Blender-side script).

`pak.render` writes one PNG per `Facing` at
`<render_dir>/<name>_<facing.label>.png`.  This module reads those
PNGs in the parent Python process, slices each Facing per its
`slices` list (applying any per-slice alpha mask), composes the
final atlas grid, and writes `<out_dir>/<name>.png`.

Pure PIL + numpy -- no bpy.  Bridge piece atlases and per-season
building atlases also stitch parent-side in `pak.bake` (one layer
above this -- they concatenate already-composed per-piece /
per-season atlases together rather than composing from per-facing
renders).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def _load_rgba(path: Path):
    """Read a PNG as a top-down (H, W, 4) float32 array in [0, 1]."""
    arr = np.asarray(Image.open(path).convert("RGBA"), dtype=np.uint8)
    return arr.astype(np.float32) / 255.0


def _save_rgba(arr, path: Path) -> None:
    """Write a top-down (H, W, 4) float32 array as a PNG."""
    bytes_ = (np.clip(arr, 0.0, 1.0) * 255.0).astype(np.uint8)
    Image.fromarray(bytes_, "RGBA").save(path)


def _facing_cells(facing, rendered, sprite_w: int, canvas_w: int,
                  canvas_h: int):
    """Yield `(label, cell_rgba)` for one Facing.

    No `slices` -> one cell, the rendered canvas itself (canvas size
    equals sprite size in this path by construction).

    With `slices` -> one cell per Slice.  Each slice crops a `sprite_w
    × sprite_w` window centred at `(canvas_w/2 + cx, canvas_h/2 + cy)`,
    pads with zero alpha where the crop runs off the canvas edge, and
    multiplies the alpha channel by `slice.alpha_mask` when supplied
    (per-tile pixel ownership for multi-tile sprites).
    """
    if facing.slices is None:
        yield facing.label, rendered
        return
    cx0 = canvas_w / 2.0
    cy0 = canvas_h / 2.0
    for sl in facing.slices:
        cx_px, cy_px = sl.offset
        x0 = int(round(cx0 + cx_px - sprite_w / 2))
        y0 = int(round(cy0 + cy_px - sprite_w / 2))
        cell = np.zeros((sprite_w, sprite_w, 4), dtype=np.float32)
        sx0 = max(0, -x0)
        sy0 = max(0, -y0)
        dx0 = max(0, x0)
        dy0 = max(0, y0)
        cw = min(sprite_w - sx0, canvas_w - dx0)
        ch = min(sprite_w - sy0, canvas_h - dy0)
        if cw > 0 and ch > 0:
            cell[sy0:sy0 + ch, sx0:sx0 + cw] = (
                rendered[dy0:dy0 + ch, dx0:dx0 + cw]
            )
        if sl.alpha_mask is not None:
            cell[..., 3] *= sl.alpha_mask
        yield sl.label, cell


def _print_atlas_summary(out_path: Path, cells, cols: int, rows: int) -> None:
    """Echo per-cell bbox to stdout (debug aid mirroring `hextrans-pak128
    /tools/threed/bespoke.py::bake_atlas`'s output)."""
    h, w = cells[0][1].shape[:2]
    label_w = max(len(label) for label, _ in cells)
    print(f"wrote {out_path} ({cols * w}x{rows * h} px, {len(cells)} cells)")
    for i, (label, cell) in enumerate(cells):
        r, c = divmod(i, cols)
        mask = cell[..., 3] > 0
        if mask.any():
            ys, xs = np.where(mask)
            bbox = (f"bbox=({int(xs.min())},{int(ys.min())})-"
                    f"({int(xs.max())},{int(ys.max())}) px={int(mask.sum())}")
        else:
            bbox = "EMPTY"
        print(f"  r{r}c{c}: {label:<{label_w}s} {bbox}")


def compose_atlas(viewpoint, render_dir: Path, out_dir: Path, name: str,
                  *, cols_per_row: int | None = None,
                  keep_per_facing: bool = False) -> Path:
    """Compose `<out_dir>/<name>.png` from the per-facing PNGs the
    Blender subprocess wrote to `<render_dir>/<name>_<facing.label>.png`.

    `viewpoint` carries the facings list (and per-facing `slices` for
    multi-tile bakes), sprite/canvas sizes.  `cols_per_row` controls
    atlas width; `None` lays every cell in a single row.

    `keep_per_facing=True` leaves the per-facing PNGs in `render_dir`
    and additionally writes per-slice PNGs (`<out_dir>/<name>_<slice.
    label>.png`) for sliced facings -- consumed by the calibration
    diffs.  `False` removes the per-facing PNGs after composing.
    """
    out_dir = Path(out_dir)
    render_dir = Path(render_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    sprite_w = viewpoint.image_width
    canvas_w = viewpoint.canvas_width or sprite_w
    canvas_h = viewpoint.canvas_height or sprite_w

    facing_pngs = [
        render_dir / f"{name}_{f.label}.png" for f in viewpoint.facings
    ]

    cells: list[tuple[str, np.ndarray]] = []
    for facing, png in zip(viewpoint.facings, facing_pngs, strict=True):
        rendered = _load_rgba(png)
        for label, cell in _facing_cells(
            facing, rendered, sprite_w, canvas_w, canvas_h,
        ):
            cells.append((label, cell))
            if keep_per_facing and facing.slices is not None:
                _save_rgba(cell, out_dir / f"{name}_{label}.png")

    cols = cols_per_row or len(cells)
    rows = (len(cells) + cols - 1) // cols
    h, w = cells[0][1].shape[:2]
    atlas = np.zeros((rows * h, cols * w, 4), dtype=np.float32)
    for i, (_, cell) in enumerate(cells):
        r, c = divmod(i, cols)
        atlas[r * h:(r + 1) * h, c * w:(c + 1) * w] = cell
    out_path = out_dir / f"{name}.png"
    _save_rgba(atlas, out_path)
    _print_atlas_summary(out_path, cells, cols, rows)

    if not keep_per_facing:
        for png in facing_pngs:
            png.unlink(missing_ok=True)

    return out_path
