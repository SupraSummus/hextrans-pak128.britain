"""One-shot per-material colour solver.

Given a bake script's current MATERIALS, render the asset once through
the square-building viewpoint, render an id-map through the same
viewpoint, then for each material compute the multiplier `mult =
upstream_mean / our_mean` (componentwise, clipped to a sane range)
that would bring ours to upstream's surface mean.  Apply that
multiplier to each material's `color=` field, render again, measure
the blurred-all-pixel dRGB, repeat until no further improvement.

Linearity assumption: under EEVEE with flat ambient + Lambert, rendered
RGB scales roughly linearly with the material's declared `color=`
tint.  Approximately true; multiple damped iterations converge.  Only
`color=`-bearing materials are tuned -- adding a new `color=` to an
image-only material flips its rendering from `image x blend_diffuse`
to `image x gain`, a much larger step than the small gradient
iteration here.  Opt an image-only material into solver tuning by
giving it an explicit `color=`-based starting point in the bake script.

Run:
    python3.12 -m pak.tune_materials citybuildings/res_1600_kg_01.py [--season summer|winter]
"""
from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from pak import REPO_ROOT
from pak.dat import Building
from pak.diff import MAGIC_PINK, silhouette_mask
from pak.fetch_blend import fetch as fetch_blend
from pak.fetch_pak import fetch as fetch_pak
from pak.materials import Material


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _render(blend_path: Path, out_dir: Path, name: str, vp,
            materials: dict | None, *, id_map: bool = False) -> Path:
    """Render the building atlas through `vp` -- the iteration loop
    pre-builds `vp_normal` (with `lighting`) and `vp_idmap` (without)
    so the per-iteration call only needs to swap materials in or
    flip to id-map mode."""
    from pak.bake import run_render
    from pak.compose import compose_atlas
    run_render(blend=blend_path, viewpoint=vp, name=name, out_dir=out_dir,
               materials=None if id_map else materials,
               material_id_map=id_map)
    compose_atlas(vp, render_dir=out_dir, out_dir=out_dir, name=name,
                  cols_per_row=len(vp.facings))
    return out_dir / f"{name}.png"


def _per_material_means(ours, idmap, upstream, mat_to_id,
                        min_pixels: int = 100,
                        blur_sigma: float = 3.0):
    """Returns `{material_name: (ours_mean_rgb, upstream_mean_rgb, n_px)}`
    averaged over each material's id-map region after common-background
    composite + Gaussian blur (the dRGB metric's blur).  Sampling from
    the blurred image (not σ=0 surface) so the per-material target
    matches what the optimiser is trying to minimise -- σ=0 sampling
    produced colours that drove each material's surface mean to
    upstream's surface mean but worsened the σ=3 metric, because the
    metric averages neighborhoods across material boundaries."""
    from scipy.ndimage import gaussian_filter
    our_sil = silhouette_mask(ours, magic_rgb=MAGIC_PINK, alpha_threshold=0)
    up_sil = silhouette_mask(upstream, magic_rgb=MAGIC_PINK, alpha_threshold=0)
    common = our_sil & up_sil
    bg = np.array(MAGIC_PINK, dtype=np.float32)
    ours_c = np.where(our_sil[..., None], ours[..., :3].astype(np.float32), bg)
    up_c = np.where(up_sil[..., None], upstream[..., :3].astype(np.float32), bg)
    if blur_sigma > 0:
        ours_c = np.stack([gaussian_filter(ours_c[..., c], sigma=blur_sigma)
                           for c in range(3)], axis=-1)
        up_c = np.stack([gaussian_filter(up_c[..., c], sigma=blur_sigma)
                         for c in range(3)], axis=-1)
    out = {}
    for name, rgb in mat_to_id.items():
        m = ((idmap[..., 0] == rgb[0]) & (idmap[..., 1] == rgb[1])
             & (idmap[..., 2] == rgb[2]) & common)
        n = int(m.sum())
        if n < min_pixels:
            continue
        out[name] = (ours_c[m].mean(0), up_c[m].mean(0), n)
    return out


def proposed_color(cur_color: tuple[float, float, float],
                   ours: np.ndarray, up: np.ndarray,
                   damping: float = 0.6,
                   gain_clamp: tuple[float, float] = (0.5, 2.0),
                   color_clamp: tuple[float, float] = (0.0, 2.5),
                   ) -> tuple[float, float, float]:
    """Propose a new `color=` tint per channel such that EEVEE renders
    `up` instead of `ours`.  Pure function, no Blender.

    Under the EEVEE-with-Lambert linearity assumption, scaling the
    declared tint by `up / ours` drives the rendered surface toward
    upstream's mean.  `damping` mixes the proposed gain toward 1.0
    (no change) per step so the loop doesn't overshoot; `gain_clamp`
    bounds a single step's multiplier; `color_clamp` keeps the
    proposed colour in EEVEE's safe range (>1 is valid as an HDR
    multiplier on an image, up to ~2-3 before saturation)."""
    cur = np.asarray(cur_color, dtype=np.float32)
    ours_safe = np.maximum(ours.astype(np.float32), 1.0)  # avoid div-by-zero
    raw_gain = up.astype(np.float32) / ours_safe
    gain = 1.0 + damping * (raw_gain - 1.0)
    gain = np.clip(gain, *gain_clamp)
    new = cur * gain
    return tuple(float(np.clip(c, *color_clamp)) for c in new)


def _measure_drgb(blend_path: Path, out_dir: Path, vp,
                  materials: dict, up_arr, season_row: int,
                  iter_label: str, blur_sigma: float = 3.0) -> float:
    """Render with `materials`, compute the same blurred-all-pixel dRGB
    used by `diff_buildings.run`."""
    from pak.diff import drgb_intersection
    from pak.diff_buildings import _best_permutation, _iou_matrix
    layouts = len(vp.facings)
    name = f"iter_{iter_label}"
    _render(blend_path, out_dir, name, vp, materials)
    ours = np.array(Image.open(out_dir / f"{name}.png").convert("RGBA"))
    our_cells = [ours[:, c*128:(c+1)*128] for c in range(layouts)]
    our_masks = [silhouette_mask(r, magic_rgb=MAGIC_PINK, alpha_threshold=0)
                 for r in our_cells]
    up_cells = [up_arr[season_row*128:(season_row+1)*128, c*128:(c+1)*128]
                for c in range(layouts)]
    up_masks = [silhouette_mask(c, magic_rgb=MAGIC_PINK, alpha_threshold=0)
                for c in up_cells]
    perm = _best_permutation(_iou_matrix(our_masks, up_masks))
    deltas = [drgb_intersection(our_cells[L], up_cells[perm[L]],
                                our_masks[L], up_masks[perm[L]],
                                blur_sigma=blur_sigma)
              for L in range(layouts)]
    return sum(deltas) / len(deltas)


def _aggregate_means(blend_path, out_dir, vp_normal, vp_idmap,
                     materials, up_arr, season_row, iter_label: str):
    """Render + id-map render at the current MATERIALS; return per-material
    `(ours_mean_rgb, upstream_mean_rgb)` aggregated across layouts."""
    from pak.diff_buildings import _best_permutation, _iou_matrix
    layouts = len(vp_normal.facings)
    name = f"iter_{iter_label}"
    _render(blend_path, out_dir, name, vp_normal, materials)
    _render(blend_path, out_dir, f"{name}_idmap", vp_idmap, None, id_map=True)
    sidecar = out_dir / f"{name}_idmap.materials.json"
    mat_to_id = {k: tuple(v) for k, v in json.loads(sidecar.read_text()).items()}
    ours = np.array(Image.open(out_dir / f"{name}.png").convert("RGBA"))
    idm = np.array(Image.open(out_dir / f"{name}_idmap.png").convert("RGB"))
    our_cells = [ours[:, c*128:(c+1)*128] for c in range(layouts)]
    idmap_cells = [idm[:, c*128:(c+1)*128] for c in range(layouts)]
    up_cells = [up_arr[season_row*128:(season_row+1)*128, c*128:(c+1)*128]
                for c in range(layouts)]
    our_masks = [silhouette_mask(r, magic_rgb=MAGIC_PINK, alpha_threshold=0)
                 for r in our_cells]
    up_masks = [silhouette_mask(c, magic_rgb=MAGIC_PINK, alpha_threshold=0)
                for c in up_cells]
    perm = _best_permutation(_iou_matrix(our_masks, up_masks))
    accum_ours, accum_up, accum_n = {}, {}, {}
    for L in range(layouts):
        stats = _per_material_means(
            our_cells[L], idmap_cells[L], up_cells[perm[L]], mat_to_id,
        )
        for n, (o, u, c) in stats.items():
            accum_ours[n] = accum_ours.get(n, np.zeros(3, np.float32)) + o * c
            accum_up[n] = accum_up.get(n, np.zeros(3, np.float32)) + u * c
            accum_n[n] = accum_n.get(n, 0) + c
    return ({n: accum_ours[n] / accum_n[n] for n in accum_n},
            {n: accum_up[n] / accum_n[n] for n in accum_n})


def tune(blend: str, upstream_dat: str, *, name: str,
         materials: dict[str, Material],
         lighting=None, season_row: int = 0,
         max_iters: int = 50, blur_sigma: float = 3.0,
         blend_units_per_tile: float = 12.0,
         out_dir: Path,
         ) -> tuple[float, float, dict[str, Material]]:
    """Run the gradient solver against `building_square_viewpoint`.
    Returns `(baseline_dRGB, best_dRGB, best_materials)` -- the caller
    decides what to do with the result (mutate a SPEC in memory, write
    it back to a script, print it for paste-in).  No file I/O beyond
    the per-iter scratch renders under `out_dir`."""
    from pak.upstream import image_stem
    from pak.viewpoints import building_square_viewpoint
    blend_path = fetch_blend(blend)
    up_arr = np.array(Image.open(fetch_pak(
        f"{image_stem(upstream_dat, name=name)}.png"
    )).convert("RGB"))
    layouts = min(up_arr.shape[1] // 128, 4)
    out_dir.mkdir(parents=True, exist_ok=True)
    vp_normal = building_square_viewpoint(
        layouts=layouts, units_per_tile=blend_units_per_tile,
        dims_x=1, dims_y=1, heights=1, lighting=lighting,
    )
    vp_idmap = building_square_viewpoint(
        layouts=layouts, units_per_tile=blend_units_per_tile,
        dims_x=1, dims_y=1, heights=1,
    )
    baseline = _measure_drgb(blend_path, out_dir, vp_normal, materials,
                             up_arr, season_row, "baseline", blur_sigma)
    print(f"  baseline dRGB={baseline:.3f}")
    best, best_mats, current = baseline, dict(materials), dict(materials)
    for i in range(max_iters):
        try:
            mean_ours, mean_up = _aggregate_means(
                blend_path, out_dir, vp_normal, vp_idmap, current,
                up_arr, season_row, f"meas{i}",
            )
        except Exception as e:
            print(f"  iter {i}: aggregate_means failed: {e}; stopping")
            break
        proposed = dict(current)
        moved = False
        for n_, mat in current.items():
            if n_ not in mean_ours or mat.color is None:
                continue
            nc = proposed_color(mat.color, mean_ours[n_], mean_up[n_])
            if nc != mat.color:
                proposed[n_] = dataclasses.replace(mat, color=nc)
                moved = True
        if not moved:
            print(f"  iter {i}: no movement; stopping")
            break
        drgb = _measure_drgb(blend_path, out_dir, vp_normal, proposed,
                             up_arr, season_row, f"prop{i}", blur_sigma)
        improved = drgb < best - 0.01
        print(f"  iter {i}: proposed dRGB={drgb:.3f} "
              f"{'(IMPROVED)' if improved else '(WORSE; stopping)'}")
        if not improved:
            break
        best, best_mats, current = drgb, proposed, proposed
    return baseline, best, best_mats


def run(bake_path: Path, season: str = "summer", max_iters: int = 50) -> None:
    mod = _load_module(bake_path)
    spec = getattr(mod, "SPEC", None)
    if not isinstance(spec, Building):
        raise SystemExit(f"{bake_path}: not a Building")
    if season == "winter":
        if spec.seasons < 2:
            raise SystemExit("asset has no winter season")
        blend, materials, season_row = (
            spec.blend_winter, dict(spec.materials_winter or {}), 1,
        )
    else:
        blend, materials, season_row = (
            spec.blend, dict(spec.materials or {}), 0,
        )
    _, best_drgb, best_materials = tune(
        blend, spec.upstream_dat, name=spec.name,
        materials=materials, lighting=spec.lighting,
        season_row=season_row, max_iters=max_iters,
        blend_units_per_tile=spec.blend_units_per_tile,
        out_dir=REPO_ROOT / "out" / "tune" / bake_path.stem,
    )
    print(f"\n# Best MATERIALS for {bake_path.stem} ({season}); dRGB={best_drgb:.3f}")
    print("MATERIALS = {")
    for name_, mat in best_materials.items():
        fields = []
        for f in dataclasses.fields(Material):
            v = getattr(mat, f.name)
            if v != f.default:
                if f.name == "color":
                    v = tuple(round(c, 3) for c in v)
                fields.append(f"{f.name}={v!r}")
        print(f"    {name_!r}: Material({', '.join(fields)}),")
    print("}")


def _main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("bake_script", type=Path)
    ap.add_argument("--season", choices=["summer", "winter"], default="summer")
    args = ap.parse_args()
    run(args.bake_script, season=args.season)


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    _main()
