"""Calibration check: render an upstream blend through `blend_render.py`
and pixel-diff each facing against the upstream pakset PNG.

Validates the upstream blend's frame against the calibration contract
documented in CLAUDE.md ("Upstream blend calibration contract"); if
this passes, the same blend feeds `hex_render.py` without per-asset
tweaks.

Run as:

    python3 tools/threed/diff_upstream.py \\
        <blend_path_in_blends_repo> \\
        <upstream_png_stem_in_pak_repo> \\
        [--align vehicles|bases] [--views 8|4] [--out out/diff/<name>]

Outputs `<out>/grid.png` (ours / upstream / amplified abs-diff, 8 cols)
and prints per-facing silhouette IoU and mean abs(RGB-delta).
Calibrated assets land at IoU ≥ 0.93 across all facings; the script
exits non-zero when any facing falls below 0.90, signalling real
drift rather than the colour/AA residual.

Pixel deltas in RGB-but-not-silhouette generally trace to upstream's
livery material swap, not to a geometry problem (see `TODO.md` ->
`sp_*` mask pass).

Dependencies (system Python, not Blender's bundled): `numpy`, `Pillow`.
Blender (`apt-get install blender`) for the render half.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VIEWS_8 = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
VIEWS_4 = ["S", "W", "N", "E"]


def _parse(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("blend", help="path within the blends repo, e.g. trains/Carriages/4wheel-1850.blend")
    ap.add_argument("stem", help="upstream png stem in the pak repo, e.g. trains/carriages/4wheel-1850-first-lnwr")
    ap.add_argument("--align", choices=["vehicles", "bases"], default="vehicles")
    ap.add_argument("--views", type=int, choices=[4, 8], default=8)
    ap.add_argument("--out", default=None, help="output dir (default: out/diff/<stem-basename>)")
    return ap.parse_args(argv)


def _render(blend_path: Path, out_dir: Path, name: str, align: str, views: int) -> None:
    script = HERE / "blend_render.py"
    cmd = [
        "blender", "-b", str(blend_path), "-P", str(script), "--",
        "--out", str(out_dir), "--name", name,
        "--align", align, "--views", str(views),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def _compose(ours_dir: Path, up_paths: dict[str, Path], name: str, views: list[str], out_grid: Path):
    import numpy as np
    from PIL import Image, ImageDraw

    CELL, PAD, LH = 128, 8, 18
    cols, rows = len(views), 3
    W = cols * (CELL + PAD) + PAD
    H = rows * (CELL + PAD) + PAD + LH

    def checker(sz, c1=(210, 210, 210), c2=(180, 180, 180), step=8):
        a = np.zeros((sz, sz, 3), dtype=np.uint8)
        ys, xs = np.indices((sz, sz))
        mask = ((xs // step + ys // step) % 2 == 0)
        a[mask] = c1; a[~mask] = c2
        return Image.fromarray(a, "RGB").convert("RGBA")

    bg = checker(CELL)
    grid = Image.new("RGBA", (W, H), (245, 245, 245, 255))
    draw = ImageDraw.Draw(grid)

    metrics = []
    for i, v in enumerate(views):
        draw.text((PAD + i * (CELL + PAD) + CELL // 2 - 6, 2), v, fill=(0, 0, 0, 255))
        ours = Image.open(ours_dir / f"{name}_{v}.png").convert("RGBA")
        up = Image.open(up_paths[v]).convert("RGBA")
        x = PAD + i * (CELL + PAD)
        grid.paste(Image.alpha_composite(bg, ours), (x, LH + PAD))
        grid.paste(Image.alpha_composite(bg, up), (x, LH + PAD + CELL + PAD))
        a = np.asarray(ours, dtype=np.int16)
        b = np.asarray(up, dtype=np.int16)
        d = np.clip(np.abs(a - b) * 4, 0, 255).astype(np.uint8)
        dmax = d[:, :, :3].max(axis=2)
        d_img = Image.fromarray(np.dstack([dmax] * 3 + [np.full_like(dmax, 255)]), "RGBA")
        grid.paste(d_img, (x, LH + PAD + 2 * (CELL + PAD)))

        am = a[:, :, 3] > 16; bm = b[:, :, 3] > 16
        iou = float((am & bm).sum()) / max(int((am | bm).sum()), 1)
        rgb = float(np.abs(a[:, :, :3] - b[:, :, :3]).mean())
        metrics.append((v, iou, rgb))

    out_grid.parent.mkdir(parents=True, exist_ok=True)
    grid.save(out_grid)
    return metrics


def main(argv: list[str]) -> int:
    args = _parse(argv)
    views = VIEWS_8 if args.views == 8 else VIEWS_4
    stem_name = Path(args.stem).name
    out_dir = Path(args.out) if args.out else ROOT / "out" / "diff" / stem_name
    out_dir.mkdir(parents=True, exist_ok=True)

    from fetch_blend import fetch as fetch_blend
    from fetch_pak import fetch as fetch_pak

    blend_path = fetch_blend(args.blend)
    render_name = Path(args.blend).stem
    _render(blend_path, out_dir, render_name, args.align, args.views)

    up_paths = {v: fetch_pak(f"{args.stem}_{v}.png") for v in views}

    metrics = _compose(out_dir, up_paths, render_name, views, out_dir / "grid.png")

    print(f"wrote {out_dir / 'grid.png'}")
    print(f"{'view':>4}  {'IoU':>6}  {'mean|dRGB|':>10}")
    worst = 1.0
    for v, iou, rgb in metrics:
        print(f"{v:>4}  {iou:>6.3f}  {rgb:>10.2f}")
        worst = min(worst, iou)
    print(f"worst IoU: {worst:.3f}  (calibrated assets land >= 0.93; <0.90 means real drift)")
    return 0 if worst >= 0.90 else 1


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    sys.exit(main(sys.argv[1:]))
