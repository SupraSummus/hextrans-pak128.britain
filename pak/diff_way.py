"""Way square-projection diff harness.

Drives `pak/bake_way.py --projection square --cell-dir <out>`
against a Way SPEC's `blend=` + `materials=`, slices the upstream
PNG (referenced via `upstream_dat`) into per-ribi 128x128 cells at
positions parsed from `image[<ribi>][0]=...row.col,...` keys, and
reports per-ribi silhouette IoU + dRGB plus a `grid.png` showing
ours / upstream / silhouette-XOR.

Upstream way atlases ship as RGBA with magic-pink as the
transparency key; the diff strips that to common transparency
before metric and grid composition.  IoU bar is loose by vehicle
standards: the square projection is a calibration view (V-bend
approximation of upstream's 90 deg corners), and deck-only ports of
elevated ways carry an intentional pillar gap -- contour parity
is not the goal, the harness is a regression check that the deck
silhouette stays where the rail authoring put it.

Run as::

    python3 -m pak.diff_way ways/<asset>.py
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

from pak import REPO_ROOT
from pak.bake import _BAKE_WAY_SCRIPT, _run_blender
from pak.dat import parse
from pak.diff import MAGIC_PINK, GridCell, cell_metric, compose_grid
from pak.fetch_pak import fetch as fetch_pak
from pak.upstream import image_stem
from pak.way_proj import SQUARE_PROJECTION

# Exit-code threshold.  Loose; deck-only ports cluster well below
# the vehicle 0.90 bar because upstream's silhouette includes the
# pier substructure ours doesn't render yet.  Anything that crashes
# falls to 0 and trips the exit code.
FAIL_IOU = 0.05


@dataclass(frozen=True)
class RibiMetric:
    """Per-ribi cell diff result."""
    ribi: str
    iou: float
    xor_px: int
    drgb: float


_KEY_RE = re.compile(r"^image\[([^\]]*)\]\[0\]$", re.I)
_REF_TAIL_RE = re.compile(r"\.(\d+)\.(\d+)$")


def _ribi_cells(upstream_dat: str, *, name: str | None) -> dict[str, tuple[int, int]]:
    """Map ribi-label (uppercase, "-" for the empty cell) -> `(row,
    col)` in the upstream atlas, parsed from `image[<ribi>][0]=
    ...row.col,...` keys on the named object (or first object when
    `name` is None)."""
    objects = parse(fetch_pak(upstream_dat))
    if name is None:
        obj = objects[0]
    else:
        wanted = name.lower()
        obj = None
        for o in objects:
            if any(k.lower() == "name" and v.strip().lower() == wanted for k, v in o):
                obj = o
                break
        if obj is None:
            raise SystemExit(f"no obj named {name!r} in {upstream_dat}")
    cells: dict[str, tuple[int, int]] = {}
    for key, value in obj:
        m = _KEY_RE.match(key)
        if not m:
            continue
        ribi = m.group(1).upper() or "-"
        ref = value.strip().removeprefix("./").split(",", 1)[0]
        rm = _REF_TAIL_RE.search(ref)
        if rm:
            cells[ribi] = (int(rm.group(1)), int(rm.group(2)))
    return cells


def _bake_square(spec, *, render_name: str, cell_dir: Path) -> None:
    """`bake_way.py --projection square --cell-dir <cell_dir>` against
    `spec.blend`; per-cell PNGs land at `<cell_dir>/<render_name>_<ribi>.png`.
    Mirrors the production bake's plumbing so the square diff sees
    what hex ships."""
    args: dict[str, object] = {
        "blend": spec.blend,
        "blend-source": spec.blend_source,
        "name": render_name,
        "out": cell_dir,
        "strip": spec.strip,
        "projection": "square",
        "cell-dir": cell_dir,
    }
    if spec.inherit_camera:
        args["inherit-camera"] = True
    if spec.full_cell:
        args["full-cell"] = True
    if spec.full_cell_rotations:
        args["full-cell-rotations"] = json.dumps(spec.full_cell_rotations)
    if spec.materials:
        args["materials"] = json.dumps(spec.materials)
    _run_blender(script=_BAKE_WAY_SCRIPT, args=args)


def run(spec, *, out_dir: Path) -> list[RibiMetric]:
    """Render `spec.blend` through the square projection, slice
    upstream's atlas into per-ribi cells, and diff each ribi pair.
    Writes per-cell PNGs + `grid.png` into `out_dir` and returns the
    per-ribi metrics list (ordered by `SQUARE_PROJECTION.entries`).
    Ribi labels present in our render but absent from upstream's
    refs (or vice versa) are skipped silently."""
    out_dir.mkdir(parents=True, exist_ok=True)

    render_name = Path(spec.blend).stem
    _bake_square(spec, render_name=render_name, cell_dir=out_dir)

    stem = image_stem(spec.upstream_dat, name=spec.name)
    upstream = np.asarray(Image.open(fetch_pak(f"{stem}.png")).convert("RGBA"))
    cells = _ribi_cells(spec.upstream_dat, name=spec.name)

    metrics: list[RibiMetric] = []
    grid_cells: list[GridCell] = []
    cell_px = 128

    for label, _edges in SQUARE_PROJECTION.entries:
        ours_path = out_dir / f"{render_name}_{label}.png"
        rc = cells.get(label)
        if not ours_path.exists() or rc is None:
            continue
        ours = np.asarray(Image.open(ours_path).convert("RGBA"))
        row, col = rc
        up = upstream[row*cell_px:(row+1)*cell_px,
                      col*cell_px:(col+1)*cell_px].copy()
        m, om, um = cell_metric(ours, up, magic_rgb=MAGIC_PINK)
        metrics.append(RibiMetric(ribi=label, iou=m.iou, xor_px=m.xor_px, drgb=m.drgb))
        grid_cells.append(GridCell(ours, up, om, um, label))

    compose_grid(grid_cells, out_path=out_dir / "grid.png",
                 strip_magic_rgb=MAGIC_PINK,
                 title=f"{spec.name}  (square projection)")
    return metrics


def format_table(metrics: list[RibiMetric]) -> str:
    """Human-readable table of `RibiMetric` rows; mirrors
    `diff_upstream.format_table`'s columns so `--all` summary lines
    are consistent across asset classes."""
    lines = [f"{'ribi':>5}  {'IoU':>6}  {'XOR_px':>7}  {'dRGB(in)':>9}"]
    for m in metrics:
        lines.append(f"{m.ribi:>5}  {m.iou:>6.3f}  {m.xor_px:>7d}  {m.drgb:>9.2f}")
    return "\n".join(lines)


def _parse(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("script", help="bake script path, e.g. ways/<asset>.py")
    ap.add_argument("--out", default=None,
                    help="output dir (default: out/diff/<script-stem>)")
    return ap.parse_args(argv)


def _load_script(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv: list[str]) -> int:
    args = _parse(argv)
    script = Path(args.script).resolve()
    mod = _load_script(script)
    spec = getattr(mod, "SPEC", None)
    if spec is None:
        raise SystemExit(f"{script.name}: no SPEC attribute")
    if spec.blend is None or spec.upstream_dat is None:
        miss = "blend=" if spec.blend is None else "upstream_dat="
        raise SystemExit(f"{script.name}: SPEC missing {miss}")

    out_dir = Path(args.out) if args.out else REPO_ROOT / "out" / "diff" / script.stem
    metrics = run(spec, out_dir=out_dir)

    print(f"wrote {out_dir / 'grid.png'}")
    print(format_table(metrics))
    worst = min((m.iou for m in metrics), default=1.0)
    print(f"worst IoU: {worst:.3f}  (<{FAIL_IOU:.2f} fails)")
    return 0 if worst >= FAIL_IOU else 1


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    sys.exit(main(sys.argv[1:]))
