"""Sprite providers — abstract "where the per-asset PNG comes from".

A `Building` SPEC's `sprites=` field carries the provider that fills
`<basename>.png` at the shape `emit_building` expects.  Two providers:

* `BlendRender` — render through `pak/render.py` (Cycles) from a
  `.blend` in jamespetts' or JamesHood's upstream blends repo.
* `UpstreamRemap` — stitch upstream's per-cell square-dimetric atlas
  via `pak.sq_split` and re-slice via `pak.hex_split` onto a 4-hex
  rhombus.  For assets with no upstream `.blend` (classical
  townhalls; see TODO.md → "2D-remap for blendless buildings").

`bake_building` / `bake_factory` call `spec.sprites.produce(...)`.
Pre-`sprites=` scripts feed a synthesised `BlendRender` through the
same dispatch -- see `pak.bake._sprites_for` and TODO.md →
"Sprite-provider migration of consumer tools".
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

import numpy as np
from PIL import Image

from pak.bake import bake_building_atlas, fetch_blend_by_source
from pak.fetch_pak import fetch as fetch_pak
from pak.remap_2d_building import remap_to_cells

if TYPE_CHECKING:
    from pak.dat import Building
    from pak.materials import Lighting, Material


class SpriteProvider(Protocol):
    def produce(self, *, spec: Building, basename: str,
                out_dir: Path, layouts: int) -> None: ...


@dataclass
class BlendRender:
    """Render the per-asset atlas through Cycles from a `.blend`.

    Holds the render-pipeline knobs (blend path, materials, lighting,
    optional winter sibling, model-centre offset, mesh-strip list);
    shape fields (`dims`, `seasons`, `heights`) stay on the `Building`
    SPEC and arrive through the `spec=` kwarg at produce time."""

    blend: str | None = None
    blend_source: str = "jp"
    materials: dict[str, Material] | None = None
    blend_winter: str | None = None
    materials_winter: dict[str, Material] | None = None
    lighting: Lighting | None = None
    blend_units_per_tile: float = 12.0
    blend_model_offset_xyz: tuple[float, float, float] | None = None
    strip: str = "Sphere"

    def produce(self, *, spec, basename, out_dir, layouts):
        if self.blend is None:
            raise ValueError(f"{basename}: BlendRender missing blend=")
        season_inputs: list[tuple[str, dict[str, Material] | None]] = [
            (self.blend, self.materials),
        ]
        if spec.seasons >= 2:
            if self.blend_winter is None:
                raise ValueError(
                    f"{basename}: spec.seasons={spec.seasons} requires "
                    f"BlendRender.blend_winter"
                )
            season_inputs.append((self.blend_winter, self.materials_winter))
        single = len(season_inputs) == 1
        tmp_paths: list[Path] = []
        for s, (b, m) in enumerate(season_inputs):
            name = basename if single else f"{basename}__s{s}"
            tmp_paths.append(bake_building_atlas(
                viewpoint_kind="hex_building",
                blend_path=fetch_blend_by_source(b, self.blend_source),
                name=name, out_dir=out_dir, layouts=layouts,
                dims_x=spec.dims_x, dims_y=spec.dims_y, heights=spec.heights,
                units_per_tile=self.blend_units_per_tile,
                materials=m, lighting=self.lighting,
                model_offset_xyz=self.blend_model_offset_xyz, strip=self.strip,
            ))
        if not single:
            _stitch_seasons(tmp_paths, out_dir / f"{basename}.png")
            for p in tmp_paths:
                p.unlink()


@dataclass
class UpstreamRemap:
    """Remap upstream's square-dimetric atlas onto a hex 4-hex rhombus.

    Reads `spec.upstream_dat`; no blend involved.  Constrained to 2×2
    single-storey CONTINUOUS-symmetry layouts (one rhombus, one
    layout).  The three rhombus orientations live in
    `pak.remap_2d_building.RHOMBUS_ORIENTATIONS`; default `"slash"`
    is the canonical townhall placement."""

    orientation: str = "slash"

    def produce(self, *, spec, basename, out_dir, layouts):
        if spec.upstream_dat is None:
            raise ValueError(f"{basename}: SPEC.upstream_dat is required")
        if (spec.dims_x, spec.dims_y) != (2, 2) or spec.heights != 1:
            raise ValueError(
                f"{basename}: UpstreamRemap wants dims=2,2 heights=1; got "
                f"dims={spec.dims_x},{spec.dims_y} heights={spec.heights}",
            )
        if layouts != 1:
            raise ValueError(
                f"{basename}: UpstreamRemap wants symmetry to reduce to "
                f"layouts=1; got {spec.symmetry!r} → {layouts}",
            )
        upstream_dat = fetch_pak(spec.upstream_dat)
        rows = [
            np.concatenate(
                remap_to_cells(upstream_dat, spec.name,
                               layout=0, season=s,
                               orientation=self.orientation)[0],
                axis=1,
            )
            for s in range(spec.seasons)
        ]
        Image.fromarray(np.vstack(rows)).save(out_dir / f"{basename}.png")


def _stitch_seasons(season_pngs: list[Path], out_path: Path) -> None:
    """Vertically concatenate per-season PNGs into one atlas.

    Top = summer, bottom = winter — matches `emit_building`'s row
    formula `s * heights + h`.  All inputs must share dimensions."""
    images = [Image.open(p).convert("RGBA") for p in season_pngs]
    sizes = {img.size for img in images}
    if len(sizes) > 1:
        raise RuntimeError(f"season PNGs have mismatched sizes: {sorted(sizes)}")
    w, h = images[0].size
    combined = Image.new("RGBA", (w, h * len(images)), (0, 0, 0, 0))
    for i, img in enumerate(images):
        combined.paste(img, (0, i * h))
    combined.save(out_path)
