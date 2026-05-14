"""Run the upstream calibration diff for one or more baked vehicles.

Each bake script (e.g. `trains/_4wheel_1850s_first.py`) declares
`BLEND` and `UPSTREAM_STEM` next to its `SPEC`; this driver imports
the module and hands those to `diff_upstream.run`, so the only
thing a caller needs to remember is the bake-script path.

Usage::

    python3 -m tools.threed.check trains/_4wheel_1850s_first.py
    python3 -m tools.threed.check --all

`--all` walks the repo for bake scripts (anything that imports
`tools.threed.bake`) and runs the diff for each one that declares
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

from tools.threed import diff_upstream


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_SKIP_DIRS = {"tools", "tests", "out", ".cache", ".git"}


def _load(script: Path):
    spec = importlib.util.spec_from_file_location(script.stem, script)
    mod = importlib.util.module_from_spec(spec)
    # Bake scripts call `bake_main(...)` only under `if __name__ == "__main__"`,
    # so importing is side-effect-free.
    spec.loader.exec_module(mod)
    return mod


def _discover() -> list[Path]:
    """All bake scripts in the repo (anything that imports `tools.threed.bake`)."""
    out: list[Path] = []
    for p in sorted(ROOT.rglob("*.py")):
        if p.name == "__init__.py":
            continue
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in _SKIP_DIRS:
            continue
        if "from tools.threed.bake import" in p.read_text():
            out.append(p)
    return out


def _run_one(script: Path, views: int) -> tuple[float, int] | None:
    mod = _load(script)
    blend = getattr(mod, "BLEND", None)
    stem = getattr(mod, "UPSTREAM_STEM", None)
    if blend is None or stem is None:
        missing = "BLEND" if blend is None else "UPSTREAM_STEM"
        print(f"{script.name}: no {missing}, skipping (add one to enable diff)")
        return None

    out_dir = ROOT / "out" / "diff" / script.stem
    metrics = diff_upstream.run(blend, stem, views=views, out_dir=out_dir)

    print(f"wrote {out_dir / 'grid.png'}")
    print(diff_upstream.format_table(metrics))
    worst = min(m.iou for m in metrics)
    xor_tot = sum(m.xor_px for m in metrics)
    print(f"worst IoU: {worst:.3f}  sum XOR: {xor_tot} px")
    return worst, xor_tot


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("script", nargs="?", help="bake script path, e.g. trains/_4wheel_1850s_first.py")
    g.add_argument("--all", action="store_true", help="run for every bake script in the repo")
    ap.add_argument("--views", type=int, choices=[4, 8], default=8)
    args = ap.parse_args(argv)

    scripts = _discover() if args.all else [Path(args.script).resolve()]

    summary: list[tuple[str, float, int]] = []
    rc = 0
    for s in scripts:
        print(f"=== {s.relative_to(ROOT)} ===")
        result = _run_one(s, args.views)
        if result is None:
            continue
        worst, xor_tot = result
        summary.append((s.stem, worst, xor_tot))
        if worst < diff_upstream.FAIL_IOU:
            rc = 1
        print()

    if len(summary) > 1:
        print("=== summary ===")
        print(f"{'asset':<28}  {'worst IoU':>9}  {'sum XOR_px':>10}")
        for name, worst, xor_tot in summary:
            print(f"{name:<28}  {worst:>9.3f}  {xor_tot:>10d}")

    return rc


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    sys.exit(main(sys.argv[1:]))
