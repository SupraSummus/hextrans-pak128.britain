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
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from pak import REPO_ROOT
from pak.dat import Building
from pak.diff import MAGIC_PINK, silhouette_mask
from pak.fetch_blend import fetch as fetch_blend
from pak.fetch_pak import fetch as fetch_pak
from pak.materials import Material, to_jsonable

HERE = Path(__file__).resolve().parent


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _render(blend_path: Path, out_dir: Path, name: str, layouts: int,
            materials: dict | None, lighting=None,
            id_map: bool = False) -> Path:
    script = HERE / "render.py"
    cmd = [
        "blender", "-b", str(blend_path), "-P", str(script), "--",
        "--out", str(out_dir), "--name", name,
        "--viewpoint", "square_building",
        "--building-footprint", f"1,1,{layouts},1",
        "--keep-per-facing",
    ]
    if id_map:
        cmd += ["--material-id-map"]
    elif materials:
        cmd += ["--materials", json.dumps(to_jsonable(materials))]
    if lighting is not None and not id_map:
        cmd += ["--lighting", json.dumps(lighting.to_jsonable())]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
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


def _measure_drgb(blend_path: Path, out_dir: Path, layouts: int,
                  materials: dict, lighting, up_arr, season_row: int,
                  iter_label: str, blur_sigma: float = 3.0) -> float:
    """Render with `materials` + `lighting`, compute the same blurred-
    all-pixel dRGB used by `diff_buildings.run`."""
    from pak.diff import drgb_intersection
    from pak.diff_buildings import _best_permutation, _iou_matrix
    name = f"iter_{iter_label}"
    _render(blend_path, out_dir, name, layouts, materials, lighting)
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


def _aggregate_means(blend_path, out_dir, layouts, materials, lighting,
                     up_arr, season_row, iter_label: str):
    """Render + id-map render at the current MATERIALS; return per-material
    `(ours_mean_rgb, upstream_mean_rgb)` aggregated across layouts."""
    from pak.diff_buildings import _best_permutation, _iou_matrix
    name = f"iter_{iter_label}"
    _render(blend_path, out_dir, name, layouts, materials, lighting)
    _render(blend_path, out_dir, f"{name}_idmap", layouts, None, None, id_map=True)
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


def run(bake_path: Path, season: str = "summer", max_iters: int = 50) -> None:
    mod = _load_module(bake_path)
    spec = getattr(mod, "SPEC", None)
    if not isinstance(spec, Building):
        raise SystemExit(f"{bake_path}: not a Building")
    if season == "winter":
        if spec.seasons < 2:
            raise SystemExit("asset has no winter season")
        blend = mod.BLEND_WINTER
        materials = dict(getattr(mod, "MATERIALS_WINTER", {}) or {})
        season_row = 1
    else:
        blend = mod.BLEND
        materials = dict(getattr(mod, "MATERIALS", {}) or {})
        season_row = 0
    lighting = getattr(mod, "LIGHTING", None)
    upstream_stem = mod.UPSTREAM_STEM

    blend_path = fetch_blend(blend)
    up_path = fetch_pak(upstream_stem)
    up_arr = np.array(Image.open(up_path).convert("RGB"))
    layouts = min(up_arr.shape[1] // 128, 4)

    out_dir = REPO_ROOT / "out" / "tune" / bake_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    best_drgb = _measure_drgb(blend_path, out_dir, layouts, materials,
                              lighting, up_arr, season_row, "baseline")
    best_materials = dict(materials)
    print(f"  baseline dRGB={best_drgb:.3f}")

    current = dict(materials)
    for i in range(max_iters):
        mean_ours, mean_up = _aggregate_means(
            blend_path, out_dir, layouts, current, lighting, up_arr,
            season_row, f"meas{i}",
        )
        proposed = dict(current)
        for name_, mat in current.items():
            if name_ not in mean_ours or mat.color is None:
                continue
            new_color = proposed_color(mat.color, mean_ours[name_], mean_up[name_])
            proposed[name_] = dataclasses.replace(mat, color=new_color)
        drgb = _measure_drgb(blend_path, out_dir, layouts, proposed, lighting,
                             up_arr, season_row, f"prop{i}")
        improved = drgb < best_drgb
        print(f"  iter {i}: proposed dRGB={drgb:.3f}  "
              f"{'(IMPROVED)' if improved else '(WORSE; stopping)'}")
        if improved:
            best_drgb = drgb
            best_materials = proposed
            current = proposed
        else:
            break

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
