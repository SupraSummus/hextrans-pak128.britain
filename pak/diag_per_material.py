"""Per-material attribution of the upstream-vs-ours pixel diff.

The calibration metric `dRGB(intersection mean)` answers "by how much
do our pixels disagree with upstream's, averaged over the silhouette
intersection".  It does NOT tell you *which material's pixels* are
driving the disagreement.  On `res_1600_kg_01` (winter dRGB 43.9)
the residual could be wholly in one mis-tinted material or evenly
spread; tuning is blind without knowing which.

This driver answers that.  It renders the asset twice through the
same square-building viewpoint:

  1. Normal render, materials applied per `MATERIALS` from the bake
     script.  This is exactly what `pak.diff_buildings` already does.
  2. Material-id-map render (`render.py --material-id-map`): every
     material replaced with a flat unlit emission of a unique RGB id.
     Pixel-aligns with the normal pass; each material's coverage is
     identifiable by its exact id triple.

For each material whose id appears in the map (i.e. whose geometry
covers at least one rendered pixel), we sample:

  - our mean RGB  (from the normal render at the id mask)
  - upstream mean RGB  (from the upstream PNG at the id mask, where
    upstream isn't magic-pink)
  - per-pixel dRGB = |our - upstream|, mean and std over the mask

The summary prints worst-offender materials first — the obvious
targets for the next tuning iteration.  Today scoped to single-tile
buildings (the only kind diff_buildings supports); generalises to
multi-tile once that lands.

Usage:

    python3.12 -m pak.diag_per_material citybuildings/res_1600_kg_01.py
    python3.12 -m pak.diag_per_material <bake-script.py> [--season winter]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from pak import REPO_ROOT
from pak.dat import Building

HERE = Path(__file__).resolve().parent
_TRANSPARENT_RGB = (231, 255, 255)


def _load_bake_script(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _render_id_map(blend_path: Path, out_dir: Path, name: str,
                   layouts: int) -> tuple[Path, dict[str, tuple[int, int, int]]]:
    """Run render.py with --material-id-map.  Returns the rendered atlas
    path and the parsed `{material_name: (r,g,b)}` mapping."""
    script = HERE / "render.py"
    subprocess.run([
        "blender", "-b", str(blend_path), "-P", str(script), "--",
        "--out", str(out_dir), "--name", name,
        "--viewpoint", "square_building",
        "--building-footprint", f"1,1,{layouts},1",
        "--keep-per-facing",
        "--material-id-map",
    ], check=True, stdout=subprocess.DEVNULL)
    sidecar = out_dir / f"{name}.materials.json"
    mat_to_id = {k: tuple(v) for k, v in json.loads(sidecar.read_text()).items()}
    return out_dir / f"{name}.png", mat_to_id


def _render_normal(blend_path: Path, out_dir: Path, name: str, layouts: int,
                   materials: dict | None) -> Path:
    """Run render.py the regular way."""
    script = HERE / "render.py"
    cmd = [
        "blender", "-b", str(blend_path), "-P", str(script), "--",
        "--out", str(out_dir), "--name", name,
        "--viewpoint", "square_building",
        "--building-footprint", f"1,1,{layouts},1",
        "--keep-per-facing",
    ]
    if materials:
        from pak.materials import to_jsonable
        cmd += ["--materials", json.dumps(to_jsonable(materials))]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    return out_dir / f"{name}.png"


def _silhouette_mask(rgba):
    """Mirror `diff_buildings._silhouette_mask`: opaque + non-magic-pink.
    Works on either RGBA (our renders) or RGB-with-pink (upstream)."""
    import numpy as np
    if rgba.shape[-1] == 4:
        a = rgba[..., 3] > 0
    else:
        a = np.ones(rgba.shape[:2], dtype=bool)
    r, g, b = rgba[..., 0], rgba[..., 1], rgba[..., 2]
    pink = ((r == _TRANSPARENT_RGB[0]) & (g == _TRANSPARENT_RGB[1])
            & (b == _TRANSPARENT_RGB[2]))
    return a & ~pink


def _per_material_stats(ours_rgba, upstream_rgba, idmap_rgba,
                        mat_to_id, ours_silhouette):
    """Per-material: where the id-map has each material's RGB triple,
    sample ours and upstream and return mean / dRGB / pixel count.

    The id map is rendered through flat emission and saved through the
    same PNG encode path as the normal atlas; we found exact RGB
    equality survives.  Restricted to the intersection of our silhouette
    and upstream's silhouette so the dRGB matches `diff_buildings`'s
    sense.
    """
    import numpy as np
    up_mask = _silhouette_mask(upstream_rgba)
    common = ours_silhouette & up_mask
    out: list[dict] = []
    for name, rgb in mat_to_id.items():
        id_match = ((idmap_rgba[..., 0] == rgb[0])
                    & (idmap_rgba[..., 1] == rgb[1])
                    & (idmap_rgba[..., 2] == rgb[2]))
        mask = id_match & common
        n = int(mask.sum())
        if n == 0:
            continue
        ours_px = ours_rgba[mask, :3].astype(np.int16)
        up_px = upstream_rgba[mask, :3].astype(np.int16)
        drgb = float(np.abs(ours_px - up_px).mean())
        out.append({
            "name": name,
            "n": n,
            "ours_mean": tuple(int(v) for v in ours_px.mean(0)),
            "ours_std": tuple(int(v) for v in ours_px.std(0)),
            "up_mean": tuple(int(v) for v in up_px.mean(0)),
            "up_std": tuple(int(v) for v in up_px.std(0)),
            "drgb": drgb,
        })
    out.sort(key=lambda r: -r["drgb"] * r["n"])  # worst total disagreement first
    return out, int(common.sum())


def _load_atlases(name_normal: str, name_idmap: str, our_dir: Path,
                  upstream_png: Path, layouts: int):
    """Load all three atlases into 128xN cells, return aligned arrays."""
    import numpy as np
    from PIL import Image
    ours = np.asarray(Image.open(our_dir / f"{name_normal}.png").convert("RGBA"))
    idmap = np.asarray(Image.open(our_dir / f"{name_idmap}.png").convert("RGB"))
    upstream = np.asarray(Image.open(upstream_png).convert("RGB"))
    # Upstream is layouts × {summer, winter} rows of 128.  This caller
    # picked the season already (passes upstream_png with appropriate
    # row cropped).
    return ours, idmap, upstream


def _print_report(stats: list[dict], common_n: int, season: str) -> None:
    print(f"\n--- {season} (per-material attribution, "
          f"{common_n} px in intersection) ---")
    print(f"{'material':<18} {'pixels':>7}  {'ours mean':<16} "
          f"{'upstream mean':<16} {'dRGB':>6} {'contrib':>8}")
    total_contrib = sum(r["drgb"] * r["n"] for r in stats)
    for r in stats:
        contrib = r["drgb"] * r["n"]
        pct = 100.0 * contrib / max(total_contrib, 1)
        ours_str = f"({r['ours_mean'][0]:3d},{r['ours_mean'][1]:3d},{r['ours_mean'][2]:3d})"
        up_str = f"({r['up_mean'][0]:3d},{r['up_mean'][1]:3d},{r['up_mean'][2]:3d})"
        print(f"  {r['name']:<16} {r['n']:>7d}  "
              f"{ours_str:<16} {up_str:<16} "
              f"{r['drgb']:>6.2f} {pct:>6.1f}%")


def _resolve_season(mod, season: str):
    """Pick the (blend, materials, season_row) triple for `season` from a
    bake script's attributes.  Returns None when the asset doesn't
    declare the requested season (e.g. `season="winter"` but spec.seasons
    is 1)."""
    spec = getattr(mod, "SPEC", None)
    if not isinstance(spec, Building):
        return None
    blend = spec.blend
    upstream_dat = spec.upstream_dat
    if blend is None or upstream_dat is None:
        return None
    from pak.upstream import image_stem
    upstream_png = f"{image_stem(upstream_dat, name=spec.name)}.png"
    if season == "winter":
        if not (spec.seasons >= 2 and spec.blend_winter):
            return None
        return spec.blend_winter, spec.materials_winter, 1, upstream_png
    return blend, spec.materials, 0, upstream_png


def _collect_stats(bake_path: Path, season: str) -> tuple[list[dict], int] | None:
    """Render the asset's normal + id-map atlases for `season`, then
    return per-material stats.  None when the asset doesn't declare
    that season (skipped silently — callers print their own diagnostic)."""
    from PIL import Image

    from pak.fetch_blend import fetch as fetch_blend
    from pak.fetch_pak import fetch as fetch_pak

    mod = _load_bake_script(bake_path)
    resolved = _resolve_season(mod, season)
    if resolved is None:
        return None
    blend_ref, materials, season_row, upstream_png = resolved
    blend_path_s = fetch_blend(blend_ref)

    up_path = fetch_pak(upstream_png)
    with Image.open(up_path) as im:
        up_w = im.size[0]
    layouts = min(up_w // 128, 4)

    out_dir = REPO_ROOT / "out" / "diag" / bake_path.stem / season
    out_dir.mkdir(parents=True, exist_ok=True)
    blend_stem = Path(blend_ref).stem
    name_normal = blend_stem
    name_idmap = f"{blend_stem}__idmap"

    _render_normal(blend_path_s, out_dir, name_normal, layouts,
                   materials=materials)
    _, mat_to_id = _render_id_map(blend_path_s, out_dir, name_idmap, layouts)

    ours_atlas, idmap_atlas, up_atlas = _load_atlases(
        name_normal, name_idmap, out_dir, up_path, layouts,
    )
    up_row = up_atlas[season_row * 128:(season_row + 1) * 128]
    ours_sil = _silhouette_mask(ours_atlas)
    return _per_material_stats(
        ours_atlas, up_row, idmap_atlas, mat_to_id, ours_sil,
    )


def run(bake_path: Path, season: str = "summer") -> int:
    result = _collect_stats(bake_path, season)
    if result is None:
        print(f"  {season}: skipped (asset doesn't declare this season)")
        return 0
    stats, common_n = result
    _print_report(stats, common_n, season=season)
    return 0


def _print_catalog_summary(all_stats: dict[str, dict[str, list[dict]]]) -> None:
    """Aggregate worst-offender materials across the catalog.

    For each (asset, season) pair we've run, collect each material's
    `drgb * n` (dRGB-weighted contribution).  Sum across the catalog
    by material name, sort, print top contributors — these are the
    surfaces whose systematic gap is biggest, the next-most-leveraged
    fixes.

    Caveat: this aggregate is *not* the same metric as `pak.check`'s
    `dRGB (intersection mean)`.  We weight by per-material id-map
    coverage which can miss pixels that pak.check's straight silhouette
    intersection includes (edge AA pixels whose id-map RGB doesn't
    match any material exactly).  A ~10-20% difference between the two
    is normal; treat this aggregate as relative-contribution sorting,
    not absolute calibration."""
    from collections import defaultdict
    by_name: dict[str, dict] = defaultdict(
        lambda: {"contrib": 0.0, "n_assets": 0, "n_px": 0,
                 "ours_sum": [0.0, 0.0, 0.0], "up_sum": [0.0, 0.0, 0.0]}
    )
    for _asset, seasons in all_stats.items():
        for _season, stats in seasons.items():
            if stats is None:
                continue
            for r in stats:
                ent = by_name[r["name"]]
                ent["contrib"] += r["drgb"] * r["n"]
                ent["n_assets"] += 1
                ent["n_px"] += r["n"]
                for i in range(3):
                    ent["ours_sum"][i] += r["ours_mean"][i] * r["n"]
                    ent["up_sum"][i] += r["up_mean"][i] * r["n"]
    rows = []
    for name, ent in by_name.items():
        n = max(ent["n_px"], 1)
        rows.append({
            "name": name,
            "contrib": ent["contrib"],
            "n_assets": ent["n_assets"],
            "n_px": ent["n_px"],
            "ours": tuple(int(v / n) for v in ent["ours_sum"]),
            "up": tuple(int(v / n) for v in ent["up_sum"]),
        })
    rows.sort(key=lambda r: -r["contrib"])
    total = sum(r["contrib"] for r in rows)
    print("\n=== catalog summary: dRGB contribution by material name ===")
    print(f"{'material':<20} {'assets':>6} {'pixels':>8} "
          f"{'ours mean':<16} {'upstream mean':<16} {'contrib':>10}")
    for r in rows[:25]:
        pct = 100.0 * r["contrib"] / max(total, 1)
        ours_s = f"({r['ours'][0]:3d},{r['ours'][1]:3d},{r['ours'][2]:3d})"
        up_s = f"({r['up'][0]:3d},{r['up'][1]:3d},{r['up'][2]:3d})"
        print(f"  {r['name']:<18} {r['n_assets']:>6d} {r['n_px']:>8d} "
              f"{ours_s:<16} {up_s:<16} {pct:>9.1f}%")


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("bake_script", nargs="?")
    g.add_argument("--all", action="store_true",
                   help="Run across every Building bake script in the "
                        "repo and print a catalog-wide summary of which "
                        "material names contribute most to total dRGB.")
    ap.add_argument("--season", choices=["summer", "winter", "both"],
                    default="both")
    args = ap.parse_args(argv)
    seasons = ["summer", "winter"] if args.season == "both" else [args.season]

    if args.all:
        from pak.bake_units import discover, import_script, specs_of
        all_stats: dict[str, dict[str, list[dict] | None]] = {}
        for s in discover():
            try:
                mod = import_script(s)
            except Exception:
                continue
            specs = specs_of(mod)
            if not specs or not isinstance(specs[0], Building):
                continue
            asset = s.stem
            print(f"=== {asset} ===")
            all_stats[asset] = {}
            for season in seasons:
                result = _collect_stats(s, season)
                stats = result[0] if result is not None else None
                all_stats[asset][season] = stats
                if stats is not None:
                    total = sum(r["drgb"] * r["n"] for r in stats)
                    n = sum(r["n"] for r in stats) or 1
                    print(f"  {season}: mean per-px dRGB ≈ {total / n:.1f}, "
                          f"top: {', '.join(r['name'] for r in stats[:3])}")
        _print_catalog_summary(all_stats)
        return 0

    path = Path(args.bake_script).resolve()
    for s in seasons:
        run(path, season=s)
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    sys.exit(main(sys.argv[1:]))
