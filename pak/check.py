"""Run the upstream calibration diff for one or more baked vehicles.

Each bake script (e.g. `trains/_4wheel_1850s_first.py`) declares
`blend=` and `upstream_dat=` on its `SPEC`; this driver imports
the module, reads those fields off the SPEC, and hands them to
`diff_upstream.run`.  The only thing a caller needs to remember
is the bake-script path.

Usage::

    python3 -m pak.check trains/_4wheel_1850s_first.py
    python3 -m pak.check --all

`--all` walks the repo for bake scripts (anything that imports
`pak.bake`) and runs the diff for each one whose SPEC declares
`upstream_dat`.  Scripts missing the field are skipped with a
notice -- fill it in when the upstream dat path is known.
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


def _run_one(script: Path, views: int) -> tuple[float, int | None, float, float | None] | None:
    """Returns `(worst_iou, xor_px_or_None, fail_floor, drgb_mean_or_None)`
    -- `xor_px` is None for buildings (the harness doesn't compute it
    yet); `drgb_mean` is None for vehicles (printed in the per-facing
    table instead, no need to duplicate in the summary)."""
    mod = _load(script)
    specs = specs_of(mod)
    spec = specs[0] if specs else None
    blend = getattr(spec, "blend", None) if spec is not None else None
    upstream_dat = getattr(spec, "upstream_dat", None) if spec is not None else None
    if blend is None or upstream_dat is None:
        missing = "blend=" if blend is None else "upstream_dat="
        print(f"{script.name}: no SPEC.{missing}, skipping (add one to enable diff)")
        return None

    out_dir = REPO_ROOT / "out" / "diff" / script.stem
    if isinstance(spec, Building):
        multitile = spec.dims_x > 1 or spec.dims_y > 1 or spec.heights > 1
        if multitile:
            # Calibration-grade multi-tile diff: render through
            # `square_building` at the multi-tile footprint, slice into
            # per-tile cells via the square dimetric tile lattice, and
            # also compare the full-canvas stitched silhouette.  Emits
            # `grid_tiles.png` + `grid_stitched.png` side by side.
            spec_layouts = spec.layouts if spec.layouts is not None else 4
            per_cell, per_layout = diff_buildings.run_multitile(
                blend, upstream_dat,
                dims_x=spec.dims_x, dims_y=spec.dims_y, layouts=spec_layouts,
                out_dir=out_dir,
                materials=spec.materials, lighting=spec.lighting,
                name=spec.name,
                blend_source=spec.blend_source,
                blend_ortho_per_tile=spec.blend_ortho_per_tile,
                model_offset_xyz=spec.blend_model_offset_xyz,
            )
            print(f"wrote {out_dir / 'grid_tiles.png'}")
            print(diff_buildings.format_multitile_table(per_cell))
            print(f"wrote {out_dir / 'grid_stitched.png'}")
            print(diff_buildings.format_multitile_layout_table(per_layout))
            worst = min(r.iou for r in per_layout)
            drgb_mean = sum(r.drgb for r in per_layout) / len(per_layout)
            return worst, None, diff_buildings.FAIL_IOU, drgb_mean
        # Read the layout count off the upstream PNG width rather than
        # SPEC.layouts.  SPEC.layouts is None for most ports (resolved
        # to hex_layouts_default at bake time, which is the hex-port's
        # 8-direction choice, not what's in the upstream 4-wide atlas).
        # The PNG is the source of truth for "what columns the upstream
        # actually published"; `_UPSTREAM_NORMAL_CARDINAL` caps the
        # cardinal cameras at 4, so layouts beyond that go unrendered
        # (e.g. an upstream-8 atlas would still diff against our 4
        # cardinals -- diagonals are deferred until they ship).
        from PIL import Image

        from pak.fetch_pak import fetch as fetch_pak
        from pak.upstream import image_stem
        with Image.open(fetch_pak(f"{image_stem(upstream_dat, name=spec.name)}.png")) as im:
            up_w = im.size[0]
        layouts = min(up_w // 128, 4)
        if spec.seasons >= 2:
            if spec.blend_winter is None:
                raise SystemExit(
                    f"{script.name}: spec.seasons={spec.seasons} but "
                    f"blend_winter= not declared on SPEC"
                )
            seasons = diff_buildings.run_seasonal(
                blend, upstream_dat, layouts=layouts, out_dir=out_dir,
                materials=spec.materials,
                blend_winter=spec.blend_winter,
                materials_winter=spec.materials_winter,
                lighting=spec.lighting,
                name=spec.name,
                blend_source=spec.blend_source,
                blend_ortho_per_tile=spec.blend_ortho_per_tile,
            )
        else:
            mat, perm, drgb = diff_buildings.run(
                blend, upstream_dat, layouts=layouts, out_dir=out_dir,
                materials=spec.materials,
                lighting=spec.lighting,
                name=spec.name,
                blend_source=spec.blend_source,
                blend_ortho_per_tile=spec.blend_ortho_per_tile,
            )
            seasons = [("summer", mat, perm, drgb)]

        worst_overall = 1.0
        drgb_overall = 0.0
        for label, mat, perm, drgb in seasons:
            worst, best, diag = diff_buildings.summarise(mat, perm)
            drgb_mean = sum(drgb) / len(drgb)
            if len(seasons) > 1:
                print(f"--- {label} ---")
            print(diff_buildings.format_matrix(mat, perm))
            print(f"mean IoU identity: {diag:.3f}  best perm: {best:.3f}  "
                  f"worst-of-best: {worst:.3f}  perm={perm}")
            print(f"dRGB (blurred all-pixel): mean={drgb_mean:.2f}  "
                  f"per-layout={[round(v, 2) for v in drgb]}")
            worst_overall = min(worst_overall, worst)
            drgb_overall = max(drgb_overall, drgb_mean)
        return worst_overall, None, diff_buildings.FAIL_IOU, drgb_overall

    metrics = diff_upstream.run(blend, upstream_dat, views=views, out_dir=out_dir,
                                name=spec.name)
    print(f"wrote {out_dir / 'grid.png'}")
    print(diff_upstream.format_table(metrics))
    worst = min(m.iou for m in metrics)
    xor_tot = sum(m.xor_px for m in metrics)
    print(f"worst IoU: {worst:.3f}  sum XOR: {xor_tot} px")
    return worst, xor_tot, diff_upstream.FAIL_IOU, None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("script", nargs="?", help="bake script path, e.g. trains/_4wheel_1850s_first.py")
    g.add_argument("--all", action="store_true", help="run for every bake script in the repo")
    ap.add_argument("--views", type=int, choices=[4, 8], default=8)
    args = ap.parse_args(argv)

    scripts = _discover() if args.all else [Path(args.script).resolve()]

    summary: list[tuple[str, float, int | None, float | None]] = []
    rc = 0
    for s in scripts:
        print(f"=== {s.relative_to(REPO_ROOT)} ===")
        result = _run_one(s, args.views)
        if result is None:
            continue
        worst, xor_tot, fail_floor, drgb_mean = result
        summary.append((s.stem, worst, xor_tot, drgb_mean))
        if worst < fail_floor:
            rc = 1
        print()

    if len(summary) > 1:
        print("=== summary ===")
        print(f"{'asset':<28}  {'worst IoU':>9}  {'sum XOR_px':>10}  {'mean dRGB':>9}")
        for name, worst, xor_tot, drgb_mean in summary:
            xor_cell = f"{xor_tot:>10d}" if xor_tot is not None else f"{'—':>10}"
            drgb_cell = f"{drgb_mean:>9.2f}" if drgb_mean is not None else f"{'—':>9}"
            print(f"{name:<28}  {worst:>9.3f}  {xor_cell}  {drgb_cell}")

    return rc


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    sys.exit(main(sys.argv[1:]))
