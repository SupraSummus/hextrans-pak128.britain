"""Run the upstream calibration diff for one or more baked vehicles.

Each bake script (e.g. `trains/_4wheel_1850s_first.py`) declares
`BLEND` and `UPSTREAM_STEM` next to its `SPEC`; this driver imports
the module and hands those to `diff_upstream.run`, so the only
thing a caller needs to remember is the bake-script path.

Usage::

    python3 -m pak.check trains/_4wheel_1850s_first.py
    python3 -m pak.check --all

`--all` walks the repo for bake scripts (anything that imports
`pak.bake`) and runs the diff for each one that declares
`UPSTREAM_STEM`.  Scripts without the constant are skipped with a
notice -- fill them in when the upstream sprite stem is known.
A summary line per asset reports worst-facing IoU and total XOR
pixel count, so contour drift is easy to compare across the fleet.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

from pak import REPO_ROOT, diff_buildings, diff_upstream
from pak.bake_units import specs_of
from pak.dat import Building


_SKIP_DIRS = {"pak", "tests", "out", ".cache", ".git"}


def _load(script: Path):
    spec = importlib.util.spec_from_file_location(script.stem, script)
    mod = importlib.util.module_from_spec(spec)
    # Bake scripts call `bake_main(...)` only under `if __name__ == "__main__"`,
    # so importing is side-effect-free.
    spec.loader.exec_module(mod)
    return mod


def _discover() -> list[Path]:
    """All bake scripts in the repo (anything that imports `pak.bake`)."""
    out: list[Path] = []
    for p in sorted(REPO_ROOT.rglob("*.py")):
        if p.name == "__init__.py":
            continue
        rel = p.relative_to(REPO_ROOT)
        if rel.parts and rel.parts[0] in _SKIP_DIRS:
            continue
        if "from pak.bake import" in p.read_text():
            out.append(p)
    return out


def _run_one(script: Path, views: int) -> tuple[float, int | None, float] | None:
    """Returns `(worst_iou, xor_px_or_None, fail_floor)` -- `xor_px`
    is None for buildings since the harness doesn't compute it yet."""
    mod = _load(script)
    blend = getattr(mod, "BLEND", None)
    stem = getattr(mod, "UPSTREAM_STEM", None)
    specs = specs_of(mod)
    spec = specs[0] if specs else None
    if blend is None or stem is None:
        missing = "BLEND" if blend is None else "UPSTREAM_STEM"
        print(f"{script.name}: no {missing}, skipping (add one to enable diff)")
        return None

    out_dir = REPO_ROOT / "out" / "diff" / script.stem
    if isinstance(spec, Building):
        layouts = spec.layouts or 1
        mat, perm = diff_buildings.run(
            blend, stem, layouts=layouts, out_dir=out_dir,
        )
        worst, best, diag = diff_buildings.summarise(mat, perm)
        print(diff_buildings.format_matrix(mat, perm))
        print(f"mean IoU identity: {diag:.3f}  best perm: {best:.3f}  "
              f"worst-of-best: {worst:.3f}  perm={perm}")
        return worst, None, diff_buildings.FAIL_IOU

    metrics = diff_upstream.run(blend, stem, views=views, out_dir=out_dir)
    print(f"wrote {out_dir / 'grid.png'}")
    print(diff_upstream.format_table(metrics))
    worst = min(m.iou for m in metrics)
    xor_tot = sum(m.xor_px for m in metrics)
    print(f"worst IoU: {worst:.3f}  sum XOR: {xor_tot} px")
    return worst, xor_tot, diff_upstream.FAIL_IOU


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("script", nargs="?", help="bake script path, e.g. trains/_4wheel_1850s_first.py")
    g.add_argument("--all", action="store_true", help="run for every bake script in the repo")
    ap.add_argument("--views", type=int, choices=[4, 8], default=8)
    args = ap.parse_args(argv)

    scripts = _discover() if args.all else [Path(args.script).resolve()]

    summary: list[tuple[str, float, int | None]] = []
    rc = 0
    for s in scripts:
        print(f"=== {s.relative_to(REPO_ROOT)} ===")
        result = _run_one(s, args.views)
        if result is None:
            continue
        worst, xor_tot, fail_floor = result
        summary.append((s.stem, worst, xor_tot))
        if worst < fail_floor:
            rc = 1
        print()

    if len(summary) > 1:
        print("=== summary ===")
        print(f"{'asset':<28}  {'worst IoU':>9}  {'sum XOR_px':>10}")
        for name, worst, xor_tot in summary:
            xor_cell = f"{xor_tot:>10d}" if xor_tot is not None else f"{'—':>10}"
            print(f"{name:<28}  {worst:>9.3f}  {xor_cell}")

    return rc


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    sys.exit(main(sys.argv[1:]))
