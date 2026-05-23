"""Unified renderer for the upstream Pak128.Britain blends.

One pipeline parameterised by a `Viewpoint` describes both the
square-dimetric upstream view (used as the calibration baseline
against the published pak PNGs) and the hex projection this project
ships.  The same scene-prep, mesh-bake, per-facing-render path
serves both -- viewpoints differ only in camera placement, sun
direction, the per-facing list, and an extrinsic 4x4 baked into
the mesh (identity for square, hex shear for hex).

The .blend is treated as pure model data: any existing Camera,
Sphere or Lamp objects are deleted at load and replaced by ones
the Viewpoint describes.  This makes the bake reproducible
regardless of how the blend was saved.

Mesh strategy: bake `matrix_world` into mesh vertex data once,
then per facing apply `extrinsic @ rot_z(model_rot) @ fit` via
`mesh.transform()`.  See CLAUDE.md -> "silent-failure landmines"
for why we don't carry the projection on a parent Empty
(matrix_basis decomposition drops shear) and why we exit edit mode
up front (the BMesh edit buffer bypasses v.co writes).

Scope: this script runs inside `blender -b -P` and only writes the
per-facing PNGs (`<out_dir>/<name>_<facing.label>.png`).  Atlas
composition -- slicing multi-tile renders, applying per-cell alpha
masks, pasting cells into the final grid -- lives on the parent
side in `pak.compose.compose_atlas`, which has no bpy dependency.
Per-facing PNGs go through Blender's writer; the atlas through
PIL's.  bpy doesn't touch image IO past `bpy.ops.render.render`.

Asset-class dispatch lives in the parent (`pak.bake.run_render` +
factories in `pak.viewpoints`); this script unpickles a `RenderPayload`
and calls `render_facings`.  Adding a new asset class is a parent-side
factory and doesn't touch render.py.

    blender -b <blend_path> -P pak/render.py -- \\
        --out <dir> --name <stem> --payload <pickle_path>
"""

from __future__ import annotations

import argparse
import json
import pickle
import sys
from collections.abc import Callable
from dataclasses import dataclass
from math import radians
from pathlib import Path
from typing import NamedTuple

import numpy as np

HERE = Path(__file__).resolve().parent
# Put the repo root on sys.path so `pak.<module>` imports resolve.
# `hex_synth` uses `from .way import …`, so we need the package form,
# not a flat sys.path on the `pak/` dir.  Mirrors `pak/bake_way.py`.
sys.path.insert(0, str(HERE.parent))

from pak.fetch_blend import fetch as fetch_blend  # noqa: E402

try:
    import bmesh
    import bpy
    import mathutils
except ImportError:
    # bpy / bmesh / mathutils are only available inside the Blender
    # subprocess (see `pak.bake.run_render`).  This module is also
    # imported from plain Python for the dataclass definitions
    # (Facing, Slice, Viewpoint, …) and `RenderPayload`; those
    # consumers never call into the bpy-using functions.
    bpy = bmesh = mathutils = None


class Slice(NamedTuple):
    """One sprite cropped from a Facing's wide canvas — see
    `Facing.slices`.  `offset` is the cell-centre position relative to
    the canvas centre; `alpha_mask` (a W×W float array, or None) clips
    the cell to the tile's pixel-ownership region for multi-tile
    sprites.  Source of the mask depends on projection: square pipes
    through `pak.sq_split` (the An-dz/tilecutter port); hex pipes
    through `pak.hex_split.hex_tile_pixel_mask` (projection Voronoi)."""
    label: str
    offset: tuple[int, int]
    alpha_mask: object | None


@dataclass
class Facing:
    """One sprite direction within a Viewpoint.

    `model_translation` shifts the rotated mesh in world XY before the
    extrinsic shear — used by multi-tile building bakes to bring one
    footprint cell to world origin per facing so the standard hex
    camera renders that single cell's content.  `model_scale` scales
    the mesh uniformly after fit — used by tree bakes to render the
    same model at successive growth stages.

    `slices` opts the facing into image-space slicing: one Blender
    render produces N atlas cells, each a W×W crop centred at
    `(canvas_width/2 + cx_px, canvas_height/2 + cy_px)`.  Used by the
    multi-tile building viewpoint — the whole footprint renders once
    at a wide canvas with the model untranslated, then crops at the
    per-tile screen positions deliver the per-tile sprites.  Default
    `None` keeps the legacy 1-cell-per-facing path; see `Slice`."""
    label: str
    camera_location: tuple[float, float, float]
    camera_rotation_euler: tuple[float, float, float]  # radians
    sun_rotation_euler: tuple[float, float, float]  # radians
    model_rot_z_deg: float = 0.0  # rotation applied to the mesh after fit
    model_translation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    model_scale: float = 1.0
    slices: list[Slice] | None = None
    # Per-facing camera clip overrides; `None` keeps Blender's defaults.
    # Used by `tunnel_hex_viewpoint` to split each portal into Back / Front
    # passes at the tile-centre Y plane.
    clip_start: float | None = None
    clip_end: float | None = None


def _configure_cycles(scn) -> None:
    """Pin Cycles knobs that are otherwise non-deterministic across CI
    runs even on identical hardware: adaptive sampling (per-pixel
    termination on a noise estimate), the denoiser (the blend may save
    it on), and the sample seed (the blend may save a non-zero value).
    Cross-CPU determinism (Intel vs AMD AVX2 transcendentals / embree)
    is still not guaranteed -- see CLAUDE.md -> CI."""
    scn.cycles.use_denoising = False
    scn.cycles.use_adaptive_sampling = False
    scn.cycles.seed = 0


def _configure_eevee(scn) -> None:
    """EEVEE substitute for BI: taa_render_samples=8 gives proper edge
    alpha-AA (1 writes 0-or-255 only and drops the edge ring); GTAO,
    bloom, SSR, volumetrics off for determinism across CI runners.
    World ambient defaults to 0.30 grey; per-asset overrides flow
    through `Viewpoint.world_ambient` (set at factory time from
    `Lighting.world_ambient`)."""
    scn.eevee.taa_render_samples = 8
    scn.eevee.use_gtao = False
    scn.eevee.use_bloom = False
    scn.eevee.use_ssr = False
    scn.eevee.use_volumetric_lights = False
    scn.eevee.use_soft_shadows = False
    scn.eevee.use_shadow_high_bitdepth = True
    if scn.world is not None:
        scn.world.use_nodes = False
        try:
            scn.world.color = (0.30, 0.30, 0.30)
        except AttributeError:
            pass


def configure_workbench(scn) -> None:
    """Flat-shading substitute: rendered pixel == material's diffuse
    colour directly.  No path tracing, no embree, no SIMD-sensitive
    reductions -- byte-stable across CPUs in practice.  Imported by
    `pak/bake_way.py` (ways have their own harness for composition
    reasons -- see CLAUDE.md -> "Way-bake architecture" -- but share
    the engine-config contract)."""
    shading = scn.display.shading
    shading.light = "FLAT"
    shading.color_type = "MATERIAL"
    shading.show_shadows = False
    shading.show_cavity = False
    shading.show_specular_highlight = False


@dataclass(frozen=True)
class Renderer:
    """Engine choice + everything render.py needs to dispatch on it.
    Collapses the `engine: str` + `_ENGINE_CONFIGURERS[name]` dict
    lookup + `if engine == "BLENDER_EEVEE"` branches into one value.

    `rebind_textures` flags engines whose blends ship pre-2.5 MTex
    slots the renderer rebuilds as Principled BSDF node graphs.  True
    for EEVEE (`_reload_external_textures`, `_bind_textures_via_nodes`
    fire from `render_facings`); false for Cycles and Workbench, where
    blends either use their authored node graphs verbatim or render
    flat-diffuse."""
    name: str  # set as `scn.render.engine`
    configure: Callable[[object], None]  # called on `scn` after engine set
    rebind_textures: bool = False


CYCLES = Renderer(name="CYCLES", configure=_configure_cycles)
EEVEE = Renderer(name="BLENDER_EEVEE", configure=_configure_eevee,
                 rebind_textures=True)
WORKBENCH = Renderer(name="BLENDER_WORKBENCH", configure=configure_workbench)


@dataclass
class Viewpoint:
    """Self-contained recipe for rendering one asset N ways.

    `camera_ortho`, `sun_energy` and `fit_matrix` are callables of
    `BlendAuthored` -- the policy lives in the closure rather than as
    separate "scale by N when authored is None" fields on the
    dataclass.  Common shapes live in `pak.viewpoints` as helpers
    (`_authored_ortho`, `_authored_sun`, `_hex_fit`, `_identity_matrix`,
    `_fixed_hex_scale`).

    `extrinsic` is the OUTERMOST factor applied per facing
    (hex_proj_shear for hex, identity for square); `fit_matrix` is the
    INNERMOST (blend->intra-tile scale), so the per-facing transform
    composes them as `extrinsic @ T @ S @ R @ fit_matrix(authored)`."""
    name: str
    image_width: int
    facings: list[Facing]
    camera_ortho: Callable[[BlendAuthored], float]
    sun_energy: Callable[[BlendAuthored], float]
    fit_matrix: Callable[[BlendAuthored], tuple]  # 4x4 row-major tuple
    extrinsic: tuple | None = None  # 4x4 row-major tuple, or None for identity
    # Vehicles & ways: `CYCLES`.  Buildings: `EEVEE` (BI's
    # use_nodes=False materials render closer to upstream under EEVEE
    # than Cycles).  Both are empirical substitutes for upstream's
    # actual authoring engine (Blender Internal under 2.79, dropped
    # in 2.80) -- see CLAUDE.md -> "Building-bake architecture".
    # `WORKBENCH` available for flat-shading paths (ways).
    engine: Renderer = CYCLES
    # Object names stripped from the scene on entry (in addition to all
    # Camera and Light objects, which always go).  Default `("Sphere",)`
    # drops upstream's sun-direction visualizer mesh.  Tree blends add
    # `"Plane"` -- a large grey ground reference that upstream's
    # rendered PNGs don't show (presumably hidden via a separate
    # render-time script that doesn't ship with the blend).
    strip_meshes: tuple[str, ...] = ("Sphere",)
    # Mesh objects whose any material's name CONTAINS one of these
    # substrings get stripped too.  Used by `bridge_square_viewpoint`
    # to drop the way (Rail / Chair / Wood (sleepers) / Ballast /
    # Tarmac) the JH bridge blends ship as authoring reference —
    # the upstream Image / Start / Ramp cells are way-agnostic
    # (magic-pink-keyed for the engine to paint the way on top), so
    # anything carrying a way material has no business in the bridge
    # silhouette.  Substring matching rather than full names because
    # JH duplicates suffix-vary the same logical material across
    # twins (`Rail.000`/`.001`/`.002`/`.003`, `Ballast`/`Ballast.001`).
    strip_material_substrings: tuple[str, ...] = ()
    # Mesh objects that get replaced with a half-space slab cutter
    # (Holdout-shaded) at render time, fitted to the original verts'
    # best-fit Z=aX+bY+c plane and extruded down in world Z.  Used by
    # the tunnel viewpoints to turn `Plane.003` (the in-tile slope
    # polygon, authored as "Transparent" in upstream JH tunnel blends)
    # into an alpha cutter for the half-space below the slope.
    holdout_meshes: tuple[str, ...] = ()
    # Blender render resolution.  None falls back to a square
    # `image_width × image_width` canvas (the original behaviour).  Used
    # by image-space slicing (multi-tile building hex viewpoint) to
    # render a wide canvas covering the full footprint at the standard
    # per-pixel world rate.  Atlas cells stay at `image_width × image_
    # width`; the larger canvas is sliced into multiple cells per facing
    # (`Facing.slices`).
    canvas_width: int | None = None
    canvas_height: int | None = None
    # EEVEE world ambient override.  When set, `_install_camera_and_sun`
    # forces `scn.world.color` to this triple after the engine
    # configurer runs (which defaults to 0.30 grey for EEVEE).  Used by
    # building viewpoint factories to apply per-asset
    # `Lighting.world_ambient` at construction time, removing the need
    # for a render-time `_apply_lighting` mutation pass.
    world_ambient: tuple[float, float, float] | None = None


def _reload_external_textures(bpy) -> None:
    """Britain blends reference textures via relative filepaths like
    `//../../../textures/flemish-bond-improved.png` that don't resolve
    from the blend's location in `.cache/blends/<sha>/`.  For every
    image data block whose file failed to load (size 0), look up its
    basename in the blends repo's `textures/` directory via fetch_blend
    and rewrite the filepath.  No-op for images that loaded fine."""
    for img in bpy.data.images:
        if img.size[0] != 0:
            continue
        if img.type != "IMAGE":
            continue  # skip RENDER_RESULT / COMPOSITING / UV_TEST built-ins
        base = img.filepath.rsplit("/", 1)[-1] if img.filepath else img.name
        if not base:
            continue
        try:
            local = fetch_blend(f"textures/{base}")
        except SystemExit:
            continue
        img.filepath = str(local)
        try:
            img.reload()
        except RuntimeError:
            pass


def _bsdf_node(nt):
    """A flat-shading Principled BSDF (roughness=1, specular=0) — the
    EEVEE substitute for BI's default Lambert."""
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = 1.0
    try:
        bsdf.inputs["Specular IOR Level"].default_value = 0.0
    except KeyError:
        bsdf.inputs["Specular"].default_value = 0.0
    return bsdf


def _resolve_image(bpy, image_name: str):
    """Look up `bpy.data.images[image_name]`; return None if missing
    or if the file failed to load (size 0).  The seeder writes the
    BI slot's Image ID name verbatim, so this is a direct dict-style
    lookup -- no fuzzy matching."""
    img = bpy.data.images.get(image_name)
    if img is None or img.type != "IMAGE" or img.size[0] == 0:
        return None
    return img


def _build_image_material(bpy, m, tex_img, mat_spec) -> None:
    """Wire `m` as `<coord> -> Mapping(scale=size) -> Image ->
    Mul(diffuse) -> Principled BSDF`.

    Coord source by `mat_spec.texco`:
    - "GLOB": Attribute("blend_world_pos") populated by
      `_bake_world_into_meshes`.  Reads the original blend-frame world
      position, untouched by `_apply_facing`'s per-facing v.co rewrites,
      so the texture stays projected from a fixed world frame the way
      BI did when only the camera moved across facings.  Mapping.scale
      is `mat_spec.size` directly: BI sized GLOB textures in world units
      and our attribute coords *are* world units.
    - "ORCO" / "UV": TexCoord.Generated, the bbox-normalised substitute
      (we have no preserved UVs).  Mapping.scale = `mat_spec.size`,
      matching BI's per-axis cycles across the object bbox.

    `mat_spec.color`, when set, replaces the .blend's authored
    `diffuse_color` as the multiplier the image texture gets tinted
    by.  Push a summer-tinted image (e.g. snow blend's Hedge still
    has its summer green diffuse plus a brick image) toward a snow
    tint without losing the image's structural detail."""
    if mat_spec.color is not None:
        fallback_diffuse = (*mat_spec.color, 1.0)
    else:
        fallback_diffuse = tuple(m.diffuse_color)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = _bsdf_node(nt)
    tex_node = nt.nodes.new("ShaderNodeTexImage")
    tex_node.image = tex_img
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.vector_type = "POINT"
    mapping.inputs["Scale"].default_value = tuple(mat_spec.size)
    if any(mat_spec.ofs):
        mapping.inputs["Location"].default_value = tuple(mat_spec.ofs)
    if mat_spec.texco == "GLOB":
        coord = nt.nodes.new("ShaderNodeAttribute")
        coord.attribute_name = "blend_world_pos"
        nt.links.new(coord.outputs["Vector"], mapping.inputs["Vector"])
    else:
        coord = nt.nodes.new("ShaderNodeTexCoord")
        nt.links.new(coord.outputs["Generated"], mapping.inputs["Vector"])
    mul = nt.nodes.new("ShaderNodeMixRGB")
    mul.blend_type = "MULTIPLY"
    mul.inputs["Fac"].default_value = 1.0
    mul.inputs["Color2"].default_value = (*fallback_diffuse[:3], 1.0)
    nt.links.new(mapping.outputs["Vector"], tex_node.inputs["Vector"])
    nt.links.new(tex_node.outputs["Color"], mul.inputs["Color1"])
    nt.links.new(mul.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    m.diffuse_color = fallback_diffuse


def _build_noise_material(bpy, m, mat_spec=None) -> None:
    """CLOUDS substitute: Noise -> ColorRamp around the material's
    diffuse colour.  Used for `Material(noise=True)` entries -- BI's
    pre-2.5 procedural textures don't survive to modern Blender, and
    a noise band around the diffuse colour reads close enough at
    pakset zoom.

    `mat_spec.color`, when set, replaces the .blend's authored
    `diffuse_color` as the band's centre — needed for snow surfaces
    where BI's default CLOUDS slot paints white-over-diffuse but our
    extraction only carries the diffuse."""
    if mat_spec is not None and mat_spec.color is not None:
        fallback_diffuse = (*mat_spec.color, 1.0)[:4]
    else:
        fallback_diffuse = tuple(m.diffuse_color)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = _bsdf_node(nt)
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 50.0
    noise.inputs["Detail"].default_value = 2.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.4
    ramp.color_ramp.elements[0].color = (
        fallback_diffuse[0] * 0.6,
        fallback_diffuse[1] * 0.6,
        fallback_diffuse[2] * 0.6,
        1.0,
    )
    ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[1].color = (
        min(1.0, fallback_diffuse[0] * 1.2),
        min(1.0, fallback_diffuse[1] * 1.2),
        min(1.0, fallback_diffuse[2] * 1.2),
        1.0,
    )
    coord = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(coord.outputs["Generated"], noise.inputs["Vector"])
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    m.diffuse_color = fallback_diffuse


def _bind_textures_via_nodes(bpy, materials) -> None:
    """Build a node-graph substitute for each entry in `materials` (a
    `dict[str, pak.materials.Material]`); leave anything unlisted with
    `use_nodes=False` so Blender's auto-conversion paints the diffuse
    flat.  Names not present in `bpy.data.materials` raise -- a silent
    typo in the bake script's MATERIALS dict would render with the
    blend's stock colour and only diverge from sibling variants by a
    fixed offset.

    Must run after `_bake_world_into_meshes` so the `blend_world_pos`
    attribute the GLOB path samples is in place.

    See CLAUDE.md -> "Building-bake architecture" for the BI->EEVEE
    substitution context."""
    if not materials:
        return
    available = {m.name for m in bpy.data.materials}
    missing = set(materials) - available
    if missing:
        raise RuntimeError(
            f"MATERIALS targets unknown blend materials: {sorted(missing)}; "
            f"have {sorted(available)}"
        )
    for name, mat_spec in materials.items():
        m = bpy.data.materials[name]
        if mat_spec.slots is not None:
            _build_multislot_material(bpy, m, mat_spec)
            continue
        if mat_spec.image is not None:
            tex_img = _resolve_image(bpy, mat_spec.image)
            if tex_img is None:
                # Image data block referenced by the blend's MTex slot but
                # whose file 404'd from upstream (e.g. Britain's
                # `concrete-paving-smalll.jpg` typo'd Pavement path).
                # Fall back to flat diffuse rather than raising -- the
                # asset can still ship; tracked in TODO per-material.
                print(
                    f"  warning: MATERIALS['{name}'].image="
                    f"{mat_spec.image!r} did not load; falling back to "
                    "flat diffuse",
                    flush=True,
                )
                continue
            _build_image_material(bpy, m, tex_img, mat_spec)
        elif mat_spec.noise:
            _build_noise_material(bpy, m, mat_spec)


def _build_slot_output(bpy, nt, slot):
    """Build the per-slot sub-graph for one BI slot.  Returns a
    `(color_socket, intensity_socket)` pair where:

    - `color_socket` is the slot's RGB output (image pixels, or constant
      white for procedurals — BI's default Tex colour band).  Wired into
      the slot-stack MixRGB's Color2.
    - `intensity_socket` is the texture's per-pixel "influence" in [0,1]
      that BI multiplies into the slot's `colfac` before mixing.  For
      IMAGE textures this is the image's alpha (1.0 for opaque); for
      procedurals it's the noise value itself.  Wired (after multiply
      by `slot.fac`) into the MixRGB's Fac input — that's what makes
      a CLOUDS slot a *partial* overlay (lerping toward white where the
      noise is high) rather than a full replace.

    Returns `None, None` when the slot's image refused to load.

    Image slots: `<coord> -> Mapping(scale=size, ofs=ofs) -> ImageTexture
    -> Color/Alpha`.  Coord by texco — GLOB reads the `blend_world_pos`
    vertex attribute populated by `_bake_world_into_meshes` so the
    texture stays pinned to the .blend's world frame across per-facing
    rotations; ORCO / UV use `TexCoord.Generated`.

    Procedural slots: a `TexNoise` (CLOUDS / NOISE / MUSGRAVE all map
    to Blender's smooth fractal noise for our purposes) whose `Fac`
    output is the intensity (BI: noise value drives the influence
    factor; default texture colour at full influence is white).  Scale
    inversely tracks BI's `size` — BI doubles frequency by halving."""
    tex_img = None
    if slot.image is not None:
        tex_img = _resolve_image(bpy, slot.image)
        if tex_img is None:
            return None, None
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.vector_type = "POINT"
    mapping.inputs["Scale"].default_value = tuple(slot.size)
    if any(slot.ofs):
        mapping.inputs["Location"].default_value = tuple(slot.ofs)
    if slot.texco == "GLOB":
        coord = nt.nodes.new("ShaderNodeAttribute")
        coord.attribute_name = "blend_world_pos"
        nt.links.new(coord.outputs["Vector"], mapping.inputs["Vector"])
    else:
        coord = nt.nodes.new("ShaderNodeTexCoord")
        nt.links.new(coord.outputs["Generated"], mapping.inputs["Vector"])
    if slot.image is not None:
        tex_node = nt.nodes.new("ShaderNodeTexImage")
        tex_node.image = tex_img
        nt.links.new(mapping.outputs["Vector"], tex_node.inputs["Vector"])
        # Image texture: color from RGB, intensity from alpha.  For
        # opaque images alpha is 1.0 throughout so the mix factor is
        # just slot.fac — same as the previous single-slot path.
        return tex_node.outputs["Color"], tex_node.outputs["Alpha"]
    # Procedural: noise.Fac is the intensity (0..1) and feeds the slot's
    # influence factor.  Two output paths for the slot's RGB:
    #
    #   color_band -> intensity mapped through the band's stops via a
    #     ValToRGB node.  BI-faithful for Tex's with `TEX_COLORBAND` set
    #     (rare in the Britain pak).
    #
    #   else -> constant `slot.color` (from MTex.r/g/b).  BI's default
    #     when the texture supplies no RGB: Hedge's CLOUDS slot ships
    #     `(0.10, 0.06, 0.04)` and contributes a dark-brown overlay
    #     modulated by noise; MainColour1's ships `(0.60, 0.60, 0.60)`.
    #     Before this path landed the renderer emitted a black->white
    #     ramp here, dropping the per-slot tint and regressing summer
    #     dRGB on res_1600 when switched to slot form.
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 4.0
    noise.inputs["Detail"].default_value = 2.0
    nt.links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    if slot.color_band:
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        cr = ramp.color_ramp
        for i, (pos, r, g, b, a) in enumerate(slot.color_band):
            stop = cr.elements[i] if i < len(cr.elements) else cr.elements.new(pos)
            stop.position = pos
            stop.color = (r, g, b, a)
        nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
        return ramp.outputs["Color"], noise.outputs["Fac"]
    rgb_node = nt.nodes.new("ShaderNodeRGB")
    rgb_node.outputs[0].default_value = (*slot.color, 1.0)
    return rgb_node.outputs["Color"], noise.outputs["Fac"]


def _build_multislot_material(bpy, m, mat_spec):
    """Compose every entry in `mat_spec.slots` over the material's
    diffuse colour using each slot's blend mode + fac.  Mirrors BI's
    Tex stack: each slot's RGB output is mixed into the running base
    in declaration order; slot[N] sees the result of slot[0..N-1] as
    its base.

    A skipped slot (image 404, returns None from `_build_slot_output`)
    contributes nothing — the next slot mixes over the previous
    accumulated base.  `mat_spec.color`, when set, replaces the
    .blend's authored `diffuse_color` as the starting base."""
    if mat_spec.color is not None:
        base = (*mat_spec.color, 1.0)
    else:
        base = tuple(m.diffuse_color)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = _bsdf_node(nt)
    rgb_node = nt.nodes.new("ShaderNodeRGB")
    rgb_node.outputs[0].default_value = (*base[:3], 1.0)
    current = rgb_node.outputs["Color"]
    for slot in mat_spec.slots:
        slot_color, slot_intensity = _build_slot_output(bpy, nt, slot)
        if slot_color is None:
            continue
        mix = nt.nodes.new("ShaderNodeMixRGB")
        mix.blend_type = slot.blend
        nt.links.new(current, mix.inputs["Color1"])
        nt.links.new(slot_color, mix.inputs["Color2"])
        # MixRGB.Fac = slot.fac * texture_intensity.  Multiply via a
        # ShaderNodeMath so a CLOUDS slot's noise-Fac modulates the
        # influence (BI's `factor = colfac * intensity`).  For opaque
        # IMAGE slots this is `slot.fac * 1.0 = slot.fac` — equivalent
        # to wiring `slot.fac` directly, but uniform-path keeps the
        # graph shape consistent.
        fac_mul = nt.nodes.new("ShaderNodeMath")
        fac_mul.operation = "MULTIPLY"
        fac_mul.inputs[0].default_value = slot.fac
        nt.links.new(slot_intensity, fac_mul.inputs[1])
        nt.links.new(fac_mul.outputs["Value"], mix.inputs["Fac"])
        current = mix.outputs["Color"]
    nt.links.new(current, bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])


def _swap_to_id_map(bpy) -> dict[str, tuple[int, int, int]]:
    """Replace every material's node graph with a flat unlit emission of
    a unique RGB id.  Used by `--material-id-map`: the resulting render
    pixel-aligns with the normal render, and each material's pixels are
    identifiable by their exact RGB triple.

    Ids are spaced on a coarse grid (40-unit step in each channel,
    skipping (0,0,0)) so floating-point round-trip through the EEVEE /
    PNG encode survives — exact equality at integer RGB is reliable for
    flat emission, but a margin keeps it robust under future engine
    changes.  Returns the `{material_name: (r,g,b)}` mapping so the
    diagnostic driver can decode masks from the map PNG."""
    palette: list[tuple[int, int, int]] = []
    step = 40
    for r in range(step, 256, step):
        for g in range(step, 256, step):
            for b in range(step, 256, step):
                palette.append((r, g, b))
    mat_to_id: dict[str, tuple[int, int, int]] = {}
    for i, m in enumerate(bpy.data.materials):
        if i >= len(palette):
            raise RuntimeError(
                f"material-id-map: ran out of palette slots at {i} "
                f"({m.name})"
            )
        rgb = palette[i]
        mat_to_id[m.name] = rgb
        m.use_nodes = True
        nt = m.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        emit = nt.nodes.new("ShaderNodeEmission")
        emit.inputs["Color"].default_value = (rgb[0] / 255.0, rgb[1] / 255.0,
                                              rgb[2] / 255.0, 1.0)
        emit.inputs["Strength"].default_value = 1.0
        nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
    return mat_to_id


@dataclass
class BlendAuthored:
    """Parameters captured from the .blend before its scene objects are
    stripped.  The .blend is treated as pure model data — every
    render-time prop is reinstalled from the Viewpoint — but the artist's
    authored choices land here and feed back in.

    `ortho_scale` drives the per-asset `INTRA_TILE_PER_BLEND_UNIT =
    2*HEX_TILE_RADIUS / ortho_scale` (vehicles=24, many buildings=12).
    `sun_energy` carries the upstream-authored 0.028 that BI rendered
    against; modern engines apply `viewpoints._BI_TO_EEVEE_SUN_SCALE`
    to compensate.  Sun color isn't extracted — all Britain blends
    ship `(1,1,1)` (white), the default a freshly-installed SUN lamp
    gets anyway.  World ambient also isn't extracted: authored
    `world.color` was the BI background sky, not the ambient term,
    and modern EEVEE's `world.color` IS the ambient term — so the
    authored value would be the wrong thing to plug in."""
    ortho_scale: float | None = None
    sun_energy: float | None = None


def strip_scene(
    bpy,
    strip_meshes: tuple[str, ...] | set[str] = ("Sphere",),
    strip_material_substrings: tuple[str, ...] | set[str] = (),
) -> BlendAuthored:
    """Capture authored Camera/Sun parameters into a BlendAuthored, then
    remove the corresponding scene objects so the Viewpoint can install
    its own.  `strip_meshes` names extra mesh objects to drop on entry
    (default `("Sphere",)` -- upstream's sun-visualisation parent mesh;
    Lamp.001 is parented to it and goes via the LIGHT branch).
    `strip_material_substrings` drops mesh objects whose any material
    slot's name contains one of the given substrings -- the bridge
    path uses this to remove way-material meshes (Rail/Chair/...)
    without enumerating per-blend mesh-name variants.  Also
    consumed by `pak/bake_way.py` -- ways install their own camera +
    sun from a Projection and discard the BlendAuthored return value."""
    authored = BlendAuthored()
    strip_names = set(strip_meshes)
    subs = tuple(strip_material_substrings)
    for obj in list(bpy.context.scene.objects):
        if obj.type == "CAMERA":
            if authored.ortho_scale is None and obj.data.type == "ORTHO":
                authored.ortho_scale = float(obj.data.ortho_scale)
            bpy.data.objects.remove(obj, do_unlink=True)
        elif obj.type == "LIGHT":
            la = obj.data
            if authored.sun_energy is None and la.type == "SUN":
                authored.sun_energy = float(la.energy)
            bpy.data.objects.remove(obj, do_unlink=True)
        elif obj.name in strip_names:
            bpy.data.objects.remove(obj, do_unlink=True)
        elif obj.type == "MESH" and subs and any(
            ms.material and any(s in ms.material.name for s in subs)
            for ms in obj.material_slots
        ):
            bpy.data.objects.remove(obj, do_unlink=True)
    return authored


def _apply_holdout(bpy, names: tuple[str, ...] | set[str]) -> None:
    """Replace each named mesh's geometry with a 200x200 quad fitted to
    the original verts' best-fit `Z = aX + bY + c` plane, extrude it
    straight down in world Z by 100 units, and Holdout-shade the
    result -- a deep slab that alpha-zeroes the half-space below the
    original plane.  Replacing the geometry (rather than reusing it as
    an in-place cutter) handles the JH tunnel topology where Plane.003
    is two disconnected strips with a mouth-sized gap in the middle,
    not an annulus; the gap would otherwise leak.  No-op for names
    absent from the scene."""
    if not names:
        return
    wanted = set(names)
    holdout = bpy.data.materials.new("_holdout")
    holdout.use_nodes = True
    nt = holdout.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    ho_n = nt.nodes.new("ShaderNodeHoldout")
    nt.links.new(ho_n.outputs[0], out.inputs[0])
    for obj in bpy.context.scene.objects:
        if obj.type != "MESH" or obj.name not in wanted:
            continue
        # Bake the object's world transform into the mesh data so the
        # bmesh ops below work in world coords directly.  Safe because
        # the object isn't parented or animated -- it's a static slope
        # polygon.
        obj.data.transform(obj.matrix_world)
        obj.matrix_world = mathutils.Matrix.Identity(4)
        a, b, c = _fit_plane_z(obj.data.vertices)
        bm = bmesh.new()
        size = 100.0
        corners = [(-size, -size), (size, -size), (size, size), (-size, size)]
        top = [bm.verts.new((x, y, a*x + b*y + c)) for x, y in corners]
        bm.faces.new(top)
        result = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
        for elem in result["geom"]:
            if isinstance(elem, bmesh.types.BMVert):
                elem.co.z -= 100.0
        bm.to_mesh(obj.data)
        bm.free()
        obj.data.materials.clear()
        obj.data.materials.append(holdout)


def _fit_plane_z(verts) -> tuple[float, float, float]:
    """Least-squares fit `Z = a*X + b*Y + c` to the given mesh verts'
    world-space coordinates.  Returns `(a, b, c)`.  The fit is exact
    when the input verts are coplanar (which Plane.003 in JH tunnel
    blends is)."""
    pts = np.array([(v.co.x, v.co.y, v.co.z) for v in verts])
    A = np.column_stack([pts[:, 0], pts[:, 1], np.ones(len(pts))])
    coeffs, *_ = np.linalg.lstsq(A, pts[:, 2], rcond=None)
    return float(coeffs[0]), float(coeffs[1]), float(coeffs[2])


def _install_camera_and_sun(bpy, viewpoint: Viewpoint,
                            authored: BlendAuthored):
    """Create one camera and one SUN light, configured per the
    Viewpoint's `camera_ortho` / `sun_energy` callables (resolved
    against the BlendAuthored captured by `strip_scene`).  Per-facing
    pose changes (location, rotation) happen in the render loop."""
    cam_data = bpy.data.cameras.new("_render_camera")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = viewpoint.camera_ortho(authored)
    cam = bpy.data.objects.new("_render_camera", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.rotation_mode = "XYZ"

    sun_data = bpy.data.lights.new("_render_sun", type="SUN")
    sun_data.energy = viewpoint.sun_energy(authored)
    sun = bpy.data.objects.new("_render_sun", sun_data)
    bpy.context.scene.collection.objects.link(sun)
    sun.rotation_mode = "XYZ"

    scn = bpy.context.scene
    scn.render.resolution_x = viewpoint.canvas_width or viewpoint.image_width
    scn.render.resolution_y = viewpoint.canvas_height or viewpoint.image_width
    scn.render.resolution_percentage = 100
    scn.render.film_transparent = True
    scn.render.image_settings.color_mode = "RGBA"
    # Match upstream's saved colour-management: Raw view transform,
    # sRGB display, gamma 1.0, no exposure.  Britain blends ship these
    # values; some get clobbered if the blend was re-saved under a
    # newer Blender with Filmic defaulting on.
    scn.view_settings.view_transform = "Raw"
    scn.view_settings.look = "None"
    scn.view_settings.exposure = 0.0
    scn.view_settings.gamma = 1.0
    scn.display_settings.display_device = "sRGB"
    # Pin thread count for all engines: multi-threaded reduction order
    # is otherwise non-deterministic across CI runs even on identical
    # hardware.  Engine-specific determinism knobs go in each
    # `Renderer.configure` callback (`_configure_cycles` etc).
    scn.render.threads_mode = "FIXED"
    scn.render.threads = 1

    scn.render.engine = viewpoint.engine.name
    viewpoint.engine.configure(scn)
    # Per-viewpoint world-ambient override (e.g. `Lighting.world_ambient`
    # baked into a building viewpoint at factory time).  Applied after
    # the engine configurer so it overrides EEVEE's default 0.30 grey.
    if viewpoint.world_ambient is not None and scn.world is not None:
        try:
            scn.world.use_nodes = False
            scn.world.color = viewpoint.world_ambient
        except AttributeError:
            pass

    return cam, sun


def exit_edit_mode(bpy) -> None:
    """Upstream blends occasionally ship with one mesh stuck in edit
    mode (e.g. 4wheel-1850's body Cube.009).  Blender renders the BMesh
    edit buffer rather than `obj.data` until the object leaves edit
    mode -- our mesh.transform() / v.co writes are invisible to the
    renderer otherwise.  See CLAUDE.md -> "Edit-mode meshes".  Imported
    by `pak/bake_way.py`."""
    prev_active = bpy.context.view_layer.objects.active
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH" and obj.data.is_editmode:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.objects.active = prev_active


def _collection_renders(bpy, coll, cache):
    """Walk the collection ancestry: a collection contributes to the
    render only if neither it nor any ancestor sets hide_render.

    Britain blends keep livery variants, alt-detail meshes and
    render-time-only scaffolding (flagpoles, ensigns) in collections
    flagged hide_render; vertex iteration must respect that or fit
    math gets dragged by geometry that never renders."""
    if coll.name in cache:
        return cache[coll.name]
    if coll.hide_render:
        cache[coll.name] = False
        return False
    for parent in bpy.data.collections:
        if coll.name in parent.children.keys():
            if not _collection_renders(bpy, parent, cache):
                cache[coll.name] = False
                return False
    cache[coll.name] = True
    return True


def _bake_world_into_meshes(bpy, mathutils):
    """Bake each renderable mesh's matrix_world into its vertex data
    and clear the object's transform to identity; return a list of
    (obj, original_world_coords) records.  The records' `orig` is the
    canonical world position of each vertex, used to reset the mesh
    between facings (via `_apply_facing`).

    Linked-mesh data is unshared up front so per-instance baked
    transforms don't collide."""
    M = mathutils.Matrix
    scn = bpy.context.scene

    exit_edit_mode(bpy)

    cache: dict = {}
    def renders(obj):
        return (not obj.hide_render
                and all(_collection_renders(bpy, c, cache) for c in obj.users_collection))

    rendered = [o for o in scn.objects if o.type == "MESH" and renders(o)]

    # Several upstream `-snow.blend` siblings (e.g. `citybuildings/
    # 1600-detatched-house-2f-snow.blend`) ship with their geometry
    # collection set to `hide_render=True` — JP toggles visibility
    # manually before rendering interactively, and the saved state
    # carries the off-toggle.  When the per-collection filter rejects
    # every mesh, lift `hide_render` on every collection containing a
    # mesh whose own `hide_render` is False — Blender's renderer
    # itself respects collection.hide_render regardless of our vertex
    # transforms, so we have to flip the flag, not just the filter.
    # Same principle as the film_transparent / RGBA forcing in
    # `_install_camera_and_sun`: don't trust the blend's saved state
    # when it's the engine-substitute-default we know is wrong.
    if not rendered:
        for c in bpy.data.collections:
            if any(o.type == "MESH" and not o.hide_render for o in c.objects):
                c.hide_render = False
        cache.clear()
        rendered = [o for o in scn.objects if o.type == "MESH" and renders(o)]

    # Snapshot every matrix_world before any mutation: mutating a
    # parent's transform mid-loop silently shifts its children's
    # effective world position.
    snapshots = [(o, o.matrix_world.copy()) for o in rendered]

    seen_data = set()
    records = []
    for obj, mw in snapshots:
        if obj.data.users > 1 or id(obj.data) in seen_data:
            obj.data = obj.data.copy()
        seen_data.add(id(obj.data))
        obj.data.transform(mw)
        if obj.parent is not None:
            obj.parent = None
            obj.matrix_parent_inverse = M.Identity(4)
        obj.matrix_basis = M.Identity(4)
        orig = [v.co.copy() for v in obj.data.vertices]
        # Snapshot blend-frame world position as a vertex attribute so
        # the shader can sample BI's TEXCO_GLOB coords directly after
        # `_apply_facing` rewrites v.co per facing.  Per-facing rotation
        # otherwise wobbles Generated-derived texture coords because the
        # mesh AABB grows with rotation; reading from this attribute
        # keeps the texture pinned to the original blend frame, the way
        # BI did when only the camera moved.
        mesh = obj.data
        attr = mesh.attributes.get("blend_world_pos")
        if attr is None:
            attr = mesh.attributes.new(
                name="blend_world_pos", type="FLOAT_VECTOR", domain="POINT",
            )
        attr.data.foreach_set("vector", [c for v in orig for c in v])
        records.append((obj, orig))

    # Force the matrix_world cache to refresh: assignments to
    # matrix_basis are lazy, and the renderer otherwise reads stale
    # non-identity matrices for objects with non-unit scale,
    # double-applying their original transform on top of the baked mesh.
    bpy.context.view_layer.update()
    return records


def _apply_facing(records, M_target) -> None:
    """Rewrite each mesh's vertices to `M_target @ canonical_world_co`.
    Called once per facing; matrix_world stays the identity."""
    for obj, orig in records:
        for v, oc in zip(obj.data.vertices, orig, strict=True):
            v.co = M_target @ oc
        obj.data.update()


def render_facings(bpy, mathutils, viewpoint: Viewpoint, out_dir: Path,
                   name: str,
                   materials: dict | None = None,
                   material_id_map: bool = False,
                   model_offset: tuple[float, float, float] | None = None,
                   ) -> None:
    """Render `viewpoint.facings` of the currently loaded blend; write
    one PNG per Facing at `<out_dir>/<name>_<facing.label>.png`.

    No atlas composition, no slicing -- those live in `pak.compose.
    compose_atlas`, which runs on the parent side from the per-facing
    PNGs this writes.  For multi-tile bakes the per-facing PNG is the
    full wide canvas (Facing.canvas_width × canvas_height); compose
    crops per-cell windows from it using the Facing's `slices` list.

    `materials` is the per-asset `MATERIALS = {...}` dict from the bake
    script (a `dict[str, pak.materials.Material]`).  Applied after the
    world-bake step so the GLOB-coord path can read the
    `blend_world_pos` vertex attribute it populates.

    `material_id_map=True` replaces every material with a flat unlit
    emission of a unique RGB id (sidecar JSON written next to the
    per-facing PNGs at `<out_dir>/<name>.materials.json`) so the
    resulting renders pixel-align with the normal pass but each
    material's coverage is identifiable.  Used by `pak.diag_per_material`
    to attribute the upstream-vs-ours dRGB to specific materials."""
    authored = strip_scene(bpy, viewpoint.strip_meshes,
                           viewpoint.strip_material_substrings)
    _apply_holdout(bpy, viewpoint.holdout_meshes)
    if viewpoint.engine.rebind_textures:
        _reload_external_textures(bpy)
    cam, sun = _install_camera_and_sun(bpy, viewpoint, authored)
    records = _bake_world_into_meshes(bpy, mathutils)
    if material_id_map:
        mat_to_id = _swap_to_id_map(bpy)
        sidecar = Path(out_dir) / f"{name}.materials.json"
        sidecar.parent.mkdir(parents=True, exist_ok=True)
        sidecar.write_text(json.dumps(mat_to_id, indent=2, sort_keys=True))
    elif viewpoint.engine.rebind_textures and materials:
        _bind_textures_via_nodes(bpy, materials)
    fit = mathutils.Matrix(viewpoint.fit_matrix(authored))
    extrinsic = (mathutils.Matrix(viewpoint.extrinsic) if viewpoint.extrinsic
                 else mathutils.Matrix.Identity(4))

    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    scn = bpy.context.scene
    cam_clip_start_default = cam.data.clip_start
    cam_clip_end_default = cam.data.clip_end
    for facing in viewpoint.facings:
        cam.location = facing.camera_location
        cam.rotation_euler = facing.camera_rotation_euler
        cam.data.clip_start = (facing.clip_start if facing.clip_start is not None
                               else cam_clip_start_default)
        cam.data.clip_end = (facing.clip_end if facing.clip_end is not None
                             else cam_clip_end_default)
        sun.rotation_euler = facing.sun_rotation_euler
        M_scale = mathutils.Matrix.Diagonal((
            facing.model_scale, facing.model_scale, facing.model_scale, 1.0,
        ))
        M_target = (extrinsic
                    @ mathutils.Matrix.Translation(facing.model_translation)
                    @ M_scale
                    @ mathutils.Matrix.Rotation(radians(facing.model_rot_z_deg), 4, "Z")
                    @ fit)
        if model_offset is not None:
            # Pre-translate the mesh by -offset in world coords so
            # the model's authored centre lands at world origin --
            # the rotation above then pivots around the model
            # centre, not around an arbitrary world point.
            M_target = M_target @ mathutils.Matrix.Translation(
                (-model_offset[0], -model_offset[1], -model_offset[2])
            )
        _apply_facing(records, M_target)
        scn.render.filepath = str(out_dir / f"{name}_{facing.label}.png")
        bpy.ops.render.render(animation=False, write_still=True)


@dataclass
class RenderPayload:
    """Wire-format for the subprocess: a Viewpoint plus the per-asset
    knobs `render_facings` accepts.  Built and pickled by
    `pak.bake.run_render`."""
    viewpoint: Viewpoint
    materials: dict | None = None
    model_offset: tuple[float, float, float] | None = None
    material_id_map: bool = False


def _parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--payload", required=True,
                    help="Path to a pickle of `RenderPayload` -- the full "
                         "rendering recipe (Viewpoint + materials + offset + "
                         "diagnostic flags) marshalled from the parent "
                         "process.  See `pak.bake.run_render`.")
    return ap.parse_args(argv)


def main(argv):
    args = _parse_args(argv)
    with open(args.payload, "rb") as fh:
        payload: RenderPayload = pickle.load(fh)

    render_facings(bpy, mathutils, payload.viewpoint, args.out, args.name,
                   materials=payload.materials,
                   material_id_map=payload.material_id_map,
                   model_offset=payload.model_offset)
    return 0


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(argv))
