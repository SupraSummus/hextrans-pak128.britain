#!/usr/bin/env python3
"""Bake the hex pakset's animated open-water deliverable.

Per-(depth, stage) cell carrying the flat hex silhouette filled with
a procedural sparkle pattern.  Style mirrors the legacy: dark navy
base + sparse glint pixels that re-position between frames rather
than fade in place.  All 6 × 32 = 192 cells declared —
`wasser_t::display` queries `sea->get_image(depth, stage)` on every
depth tier, so missing cells flicker the sprite out.  Engine clamps
the depth axis at `water_depth_levels = count - 2`; flat-only on slope.

Atlas is keyed by `(depth, stage)`, not by slope — passes its own
`iter_entries` to `hex_synth.bake_pakset` rather than the
slope-keyed default.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pak import hex_synth

N_DEPTHS = 6
N_STAGES = 32

# Base + glint colours at depth 0.  At GLINT_FRACTION = 0.12, the
# convex combination 0.88 * BASE + 0.12 * GLINT lands within ~1 RGB
# unit of the legacy pak128 depth-0 mean (79, 90, 117).  Both colours
# scale linearly to LEGACY_DEEPEST_FACTOR at depth N_DEPTHS - 1, where
# the legacy mean is (62, 70, 91) — average per-channel ratio 0.78.
# Calibration is pak128, not Britain — see TODO.md.
WATER_BASE_RGB = (75, 86, 112)
GLINT_RGB = (110, 130, 160)
LEGACY_DEEPEST_FACTOR = 0.78

# Top-K glint promotion: K = round(GLINT_FRACTION * n_inside_silhouette)
# is constant per stage, so the per-frame DC is bit-identical across
# stages.  Per-pixel phase staggers a slow-stage ratchet so glints
# persist for GLINT_PERSISTENCE frames before re-hashing.
GLINT_FRACTION = 0.12
GLINT_PERSISTENCE = 8

assert N_STAGES % GLINT_PERSISTENCE == 0
N_SLOW_STAGES = N_STAGES // GLINT_PERSISTENCE


def depth_shade_factor(depth: int) -> float:
    if N_DEPTHS <= 1:
        return 1.0
    return 1.0 - (depth / (N_DEPTHS - 1)) * (1.0 - LEGACY_DEEPEST_FACTOR)


def _shade(rgb, factor):
    return tuple(int(round(c * factor)) for c in rgb)


def _stage_hash(xs: np.ndarray, ys: np.ndarray, stage: int) -> np.ndarray:
    """Per-pixel pseudo-random integer keyed on (x, y, slow_stage)."""
    xs_u = xs.astype(np.uint32)
    ys_u = ys.astype(np.uint32)
    phase = (xs_u * np.uint32(0x12345) + ys_u * np.uint32(0x67891)) \
        % np.uint32(GLINT_PERSISTENCE)
    slow_stage = ((np.uint32(stage) + phase) // np.uint32(GLINT_PERSISTENCE)) \
        % np.uint32(N_SLOW_STAGES)

    h = (xs_u * np.uint32(0x9E3779B1)) ^ \
        (ys_u * np.uint32(0x85EBCA6B)) ^ \
        (slow_stage * np.uint32(0xC2B2AE35))
    h ^= h >> np.uint32(13)
    h = (h * np.uint32(0x27D4EB2D)) & np.uint32(0xFFFFFFFF)
    h ^= h >> np.uint32(15)
    return h


def render_water(stage: int, depth: int,
                 geom: hex_synth.HexGeom | None = None) -> np.ndarray:
    """Render one (depth, stage) cell of flat hex water."""
    if geom is None:
        geom = hex_synth.HexGeom()

    factor = depth_shade_factor(depth)
    base_rgb = _shade(WATER_BASE_RGB, factor)
    glint_rgb = _shade(GLINT_RGB, factor)

    buf = np.zeros((geom.h, geom.w, 4), dtype=np.uint8)
    xs_poly, ys_poly = list(geom.vx), geom.lifted_vy(0)
    hex_synth.fill_polygon(buf, xs_poly, ys_poly, base_rgb)
    hex_synth.seal_horizontal_edges(buf, xs_poly, ys_poly, base_rgb)

    inside = np.argwhere(buf[..., 3] > 0)  # (Npx, 2) array of [y, x]
    k = int(round(GLINT_FRACTION * inside.shape[0]))
    if k > 0:
        h = _stage_hash(inside[:, 1], inside[:, 0], stage)
        glint = inside[np.argsort(h, kind="stable")[-k:]]
        buf[glint[:, 0], glint[:, 1], :3] = glint_rgb

    return buf


def _water_entries(_geom):
    for depth in range(N_DEPTHS):
        for stage in range(N_STAGES):
            yield depth, stage, (stage, depth), f"depth={depth} stage={stage}"


if __name__ == "__main__":
    hex_synth.bake_pakset(
        script_path=Path(__file__).resolve(),
        asset_name="water",
        obj_name="Water",
        render_cell=lambda stage, depth, geom: render_water(stage, depth, geom=geom),
        iter_entries=_water_entries,
        default_cols=16,
    )
