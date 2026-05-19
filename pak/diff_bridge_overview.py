"""Render every bridge tile from JH's blends and stitch one overview
grid comparing each rendered facing against the matching upstream
atlas cell.

The graphical companion to `pak.diff_bridge`'s per-case CLI: instead
of one (asset, variant) at a time, this drives the full standard set
for a bridge family (Image, Start v0/v2, Ramp v0/v2) in one command
and emits a single PNG with every (case × facing × ours/upstream/XOR)
laid out for eyeballing.

`pak.diff_bridge --match` still finds rotation mismatches numerically;
this tool's job is to *show* what's matching and what isn't so a
human can spot geometric / material issues (e.g. the JH end abutment
being slightly different from upstream's authored end) that no
permutation search can catch.

CLI:

    python3 -m pak.diff_bridge_overview \\
        --blends-dir ways/plate_girder \\
        --atlas ways/images/plate-girder.png \\
        --out out/diff/plate-girder-overview.png

The blends-dir and atlas paths are taken relative to the JH repo
root and the upstream pak repo root respectively (both fetched
through their lock files).
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from pak import REPO_ROOT

# The five standard plate-girder bridge cases that have a one-blend
# source.  Per-case label is what appears in the overview row header;
# `bake_stem` is the per-blend rendered atlas stem (matches `--name`
# passed to `pak.render`).  Variant 0 = `*`-suffixed dat keys (gentler
# slope); variant 1 = `*2`-suffixed (steeper) -- JH's end/slope blends
# are the steeper variant geometrically and so v2 lands at higher IoU
# than v0 for those tiles.
CASES: tuple[tuple[str, str, str, int], ...] = (
    ("Image v0 (= v2)", "straight", "image", 0),
    ("Start v0",        "end",      "start", 0),
    ("Start v2",        "end",      "start", 1),
    ("Ramp v0",         "slope",    "ramp",  0),
    ("Ramp v2",         "slope",    "ramp",  1),
)

CELL = 128


@dataclass(frozen=True)
class CaseResult:
    label: str
    metrics: dict[str, float]  # facing → IoU
    render_dir: Path
    diff_dir: Path
    bake_stem: str


def _render_blend_if_missing(blend_repo_path: str, render_dir: Path,
                             bake_stem: str) -> None:
    """Skip blender if every per-facing PNG already exists; otherwise
    shell out to `pak.render` once for the four facings."""
    from pak.bake import run_render
    from pak.fetch_jh_blend import fetch as fetch_jh
    from pak.viewpoints import bridge_square_viewpoint
    if all((render_dir / f"{bake_stem}_{f}.png").is_file()
           for f in ("S", "W", "N", "E")):
        return
    blend = fetch_jh(blend_repo_path)
    render_dir.mkdir(parents=True, exist_ok=True)
    run_render(blend=blend, viewpoint=bridge_square_viewpoint(),
               name=bake_stem, out_dir=render_dir)


def _stitch_overview(results: list[CaseResult], out_path: Path) -> None:
    import numpy as np
    from PIL import Image, ImageDraw

    from pak.diff import MAGIC_PINK, checker, silhouette_mask, xor_image

    bg = checker(CELL)

    facings = ("S", "W", "N", "E")
    PAD = 6
    LH = 22
    LABEL_W = 110
    SUB_LH = 14  # per-facing IoU annotation row

    row_h = CELL + PAD + CELL + PAD + CELL + PAD + SUB_LH + PAD
    total_h = LH + len(results) * row_h + PAD
    total_w = PAD + LABEL_W + PAD + len(facings) * (CELL + PAD) + PAD

    panel = Image.new("RGBA", (total_w, total_h), (245, 245, 245, 255))
    draw = ImageDraw.Draw(panel)

    for ci, lbl in enumerate(facings):
        x = PAD + LABEL_W + PAD + ci * (CELL + PAD)
        draw.text((x + CELL // 2 - 4, 4), lbl, fill=(0, 0, 0, 255))

    for ri, r in enumerate(results):
        y0 = LH + ri * row_h
        draw.text((PAD, y0 + 4), r.label, fill=(0, 0, 0, 255))
        for ci, facing in enumerate(facings):
            x = PAD + LABEL_W + PAD + ci * (CELL + PAD)
            ours = Image.open(r.render_dir / f"{r.bake_stem}_{facing}.png").convert("RGBA")
            up = Image.open(r.diff_dir / f"upstream_{facing}.png").convert("RGBA")
            panel.paste(Image.alpha_composite(bg, ours), (x, y0))
            panel.paste(Image.alpha_composite(bg, up), (x, y0 + CELL + PAD))
            a = np.asarray(ours, dtype=np.int16)
            b = np.asarray(up, dtype=np.int16)
            am = silhouette_mask(a, alpha_threshold=0, magic_rgb=MAGIC_PINK)
            bm = silhouette_mask(b, alpha_threshold=0, magic_rgb=MAGIC_PINK)
            xor = Image.fromarray(xor_image(am, bm), "RGBA")
            panel.paste(Image.alpha_composite(bg, xor),
                        (x, y0 + 2 * (CELL + PAD)))
            iou = r.metrics.get(facing, float("nan"))
            draw.text((x + 4, y0 + 3 * (CELL + PAD)),
                      f"IoU {iou:.2f}", fill=(0, 0, 0, 255))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    panel.save(out_path)


def overview(blends_dir: str, atlas_path: str, out_path: Path) -> list[CaseResult]:
    """End-to-end: render every blend in CASES, diff each against the
    matching upstream cells, stitch into one overview PNG.  Cached
    renders are re-used; cached diff outputs (the per-case
    `upstream_<facing>.png` files) get regenerated each run so the
    overview always reflects the current `diff_bridge` cell mapping.

    The family name (`plate-girder`, etc.) is derived from the atlas
    filename so the out-dir layout (`out/diff/<family>-<bake_stem>`)
    follows from a single input rather than a hardcoded prefix.
    """
    from pak.diff_bridge import run
    from pak.fetch_pak import fetch as fetch_pak

    family = Path(atlas_path).stem
    atlas_local = fetch_pak(atlas_path)
    results: list[CaseResult] = []
    for label, bake_stem, asset, variant in CASES:
        render_dir = REPO_ROOT / "out" / "diff" / f"{family}-{bake_stem}"
        diff_dir = REPO_ROOT / "out" / "diff" / f"{family}-{bake_stem}-{asset}-v{variant}"
        blend_repo_path = f"{blends_dir.rstrip('/')}/{bake_stem}.blend"
        _render_blend_if_missing(blend_repo_path, render_dir, bake_stem)
        metrics = run(
            rendered_dir=render_dir,
            render_stem=bake_stem,
            atlas_path=atlas_local,
            asset=asset,
            variant=variant,
            out_dir=diff_dir,
        )
        results.append(CaseResult(
            label=label,
            metrics={m.facing: m.iou for m in metrics},
            render_dir=render_dir,
            diff_dir=diff_dir,
            bake_stem=bake_stem,
        ))
    _stitch_overview(results, out_path)
    return results


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--blends-dir", default="ways/plate_girder",
                    help="dir in the JH blends repo holding "
                         "straight/end/slope.blend (default: ways/plate_girder)")
    ap.add_argument("--atlas", default="ways/images/plate-girder.png",
                    help="upstream atlas path (default: ways/images/plate-girder.png)")
    ap.add_argument("--out", default="out/diff/plate-girder-overview.png")
    args = ap.parse_args(argv)
    results = overview(args.blends_dir, args.atlas,
                       Path(args.out) if Path(args.out).is_absolute()
                       else REPO_ROOT / args.out)
    print(f"wrote {args.out}")
    for r in results:
        line = f"  {r.label:18s}"
        for f in ("S", "W", "N", "E"):
            line += f"  {f}={r.metrics.get(f, float('nan')):.2f}"
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
