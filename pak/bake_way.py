"""Bake one hex cell of a way asset from an upstream blend.

See CLAUDE.md → "Way-bake architecture" for the contract: the
upstream blend is the geometric atom; this driver scales it onto a
hex through-tile chord, applies the engine's hex projection shear,
and renders one cell through Cycles.  Composition into the 63 ribi
cells + slope variants — clone the atom per `StraightPath` from
`pak/way_topology.py`, `bmesh.ops.bisect_plane`-clip at cap planes,
transform onto the chord — is the next layer (see TODO.md).

Run via:

    blender -b -P pak/bake_way.py -- \\
        --blend ways/ns-cssr.blend --name cssr --out ways/

`--blend` is resolved against the blends repo via `pak/fetch_blend.py`;
the actual file is fetched on demand and cached.

Blender-only — this module imports `bpy` and `mathutils` at top level
and isn't importable outside `blender -b -P`.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy
import mathutils


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from fetch_blend import fetch as fetch_blend  # noqa: E402
from hex_synth import DEFAULT_W, HEX_TILE_RADIUS, hex_proj_shear  # noqa: E402


def _argv() -> list[str]:
    """Return the script args after `--` (Blender swallows everything before)."""
    if "--" in sys.argv:
        return sys.argv[sys.argv.index("--") + 1:]
    return []


def _parse(args: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--blend", required=True,
                   help="blend path within the blends repo, e.g. ways/ns-cssr.blend")
    p.add_argument("--name", required=True,
                   help="output basename (atlas <name>.png, dat-ref base)")
    p.add_argument("--out", type=Path, required=True,
                   help="output directory (atlas PNG goes here)")
    # Default-strip: `Sphere` is the upstream sun-direction visualizer
    # (`pak/render.py` strips it for vehicle bakes for the same
    # reason).  `Plane` is NOT noise in ns-cssr.blend — it's the
    # 2048-poly ballast pile.  Per-blend strip lists move into a
    # `ways/<asset>.py` wrapper once the asset count grows past 1.
    p.add_argument("--strip", default="Sphere",
                   help="comma-separated mesh object names to strip "
                        "(default: 'Sphere'). All cameras + lights "
                        "are always stripped.")
    return p.parse_args(args)


def _strip_scene(strip_meshes: set[str]) -> None:
    """Strip every camera/light + any mesh whose name is in
    `strip_meshes`.  Cameras + lights always go — we install our own
    from the way-bake recipe."""
    for obj in list(bpy.context.scene.objects):
        if obj.type in ("CAMERA", "LIGHT"):
            bpy.data.objects.remove(obj, do_unlink=True)
            continue
        if obj.type == "MESH" and obj.name in strip_meshes:
            bpy.data.objects.remove(obj, do_unlink=True)


def _atoms() -> list:
    """Return every MESH object remaining in the scene, sorted by name.
    Stable ordering for readability of the per-bake stdout — Cycles
    sampling still randomises pixel output run-to-run."""
    return sorted(
        (obj for obj in bpy.context.scene.objects if obj.type == "MESH"),
        key=lambda o: o.name,
    )


def _bake_world_transforms(atoms) -> None:
    """Bake `obj.matrix_world` into the mesh's vertex data and reset
    the world matrix to identity, so subsequent `mesh.transform()`
    calls compose cleanly without re-decomposing the basis (CLAUDE.md
    "matrix_basis drops shear")."""
    for obj in atoms:
        # Edit-mode landmine: writes to obj.data.vertices are invisible
        # to the renderer if the mesh is in edit mode.  Force OBJECT.
        if obj.data.is_editmode:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="OBJECT")
        obj.data.transform(obj.matrix_world)
        obj.matrix_world = mathutils.Matrix.Identity(4)


def _y_extent(atoms) -> tuple[float, float]:
    """Y range across every vertex of every atom.  The blend authors the
    rail along +Y; this is the chord direction the atom occupies."""
    y_min = min(v.co.y for obj in atoms for v in obj.data.vertices)
    y_max = max(v.co.y for obj in atoms for v in obj.data.vertices)
    return y_min, y_max


def _scale_and_centre_y(atoms, *, target_length: float,
                        y_min: float, y_max: float) -> float:
    """Scale every atom uniformly so the Y extent becomes `target_length`,
    then shift so Y is centred on origin.  Returns the applied scale
    factor.

    Uniform scale (not just Y) because the cross-section sizes — rail
    gauge, sleeper width — share the blend's world scale; squashing Y
    independently would distort the rail's aspect ratio.
    """
    src_len = y_max - y_min
    scale = target_length / src_len
    scale_mat = mathutils.Matrix.Diagonal((scale, scale, scale, 1.0))
    for obj in atoms:
        obj.data.transform(scale_mat)
    y_mid = (y_min + y_max) * 0.5 * scale
    shift = mathutils.Matrix.Translation((0.0, -y_mid, 0.0))
    for obj in atoms:
        obj.data.transform(shift)
    return scale


def _apply_extrinsic(atoms, extrinsic_rows) -> None:
    """Apply a 4x4 row-major extrinsic (the hex projection shear) to
    every atom's mesh data.  `mesh.transform()` accepts arbitrary 4x4
    directly (CLAUDE.md landmine #4)."""
    m = mathutils.Matrix(extrinsic_rows)
    for obj in atoms:
        obj.data.transform(m)


def _install_hex_camera_and_sun() -> None:
    """Add the engine's hex camera + sun.  Matches `pak/viewpoints.py`
    HEX_VIEWPOINT shape: ortho camera looking +Y at the origin,
    ortho_scale = 2R (so world x in [-R, R] maps to image width); sun
    pitched 30° from straight-down."""
    scene = bpy.context.scene

    cam_data = bpy.data.cameras.new("_way_camera")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = 2.0 * HEX_TILE_RADIUS
    cam_obj = bpy.data.objects.new("_way_camera_obj", cam_data)
    scene.collection.objects.link(cam_obj)
    cam_obj.location = (0.0, -10.0, 0.5)
    cam_obj.rotation_euler = (math.radians(90.0), 0.0, 0.0)
    scene.camera = cam_obj

    sun_data = bpy.data.lights.new("_way_sun", type="SUN")
    sun_data.energy = 0.028  # matches viewpoints.py _SUN_ENERGY
    sun_obj = bpy.data.objects.new("_way_sun_obj", sun_data)
    scene.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (math.radians(30.0), 0.0, 0.0)


def _configure_render(*, image_width: int, samples: int = 32) -> None:
    """Force RGBA + transparent film, fixed resolution, Cycles backend.
    Overrides whatever the blend saved (some Britain blends ship with
    RGB + solid world background)."""
    scene = bpy.context.scene
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = True
    scene.render.resolution_x = image_width
    # Match the hex cell shape: W wide × W tall (2u + top_pad = 4u = W
    # at the standard W=128 / u=32 / top_pad=4*lift=4*16=64 settings).
    scene.render.resolution_y = image_width
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples


def _render_to(out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.render.filepath = str(out_path)
    bpy.ops.render.render(write_still=True)


def main() -> None:
    args = _parse(_argv())

    blend_path = fetch_blend(args.blend)
    print(f"loading blend: {blend_path}")
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))

    # 1. Strip authored cameras + lights, plus caller-named meshes.
    _strip_scene({n for n in args.strip.split(",") if n})
    atoms = _atoms()
    print(f"atoms after strip: {[a.name for a in atoms]}")

    # 2. Bake matrix_world into mesh data so subsequent transforms
    # compose cleanly.
    _bake_world_transforms(atoms)

    # 3. Scale uniformly so the rail's +Y extent matches the hex
    # through-tile chord (R * sqrt(3)), and shift to origin.
    #
    # The R * sqrt(3) target is a working assumption, not a measured
    # constant: the blend authors a long strand (~8.7 units) that
    # upstream's render script crops via camera framing, so the blend
    # doesn't carry "one tile" as a named anchor.  Setting the strand
    # length to the through-tile chord gets a tile-filling render at
    # ortho_scale = 2R but adjacent tiles' rails won't be guaranteed
    # to meet flush — a tile-overlap fraction may be needed (see
    # TODO.md → "One rail way under hex" → tile-chord convention).
    y_min, y_max = _y_extent(atoms)
    target_chord = HEX_TILE_RADIUS * math.sqrt(3.0)
    scale = _scale_and_centre_y(
        atoms, target_length=target_chord, y_min=y_min, y_max=y_max,
    )
    print(f"rail Y extent before scale: [{y_min:.3f}, {y_max:.3f}] "
          f"-> after scale {scale:.4f} -> tile chord {target_chord:.3f}")

    # 4. Apply the hex projection shear (so a +Y-looking ortho camera
    # reproduces the engine's hex sx, sy mapping).
    _apply_extrinsic(atoms, hex_proj_shear())

    # 5. Hex camera + sun + render config.
    _install_hex_camera_and_sun()
    _configure_render(image_width=DEFAULT_W)

    # 6. Render the through-tile straight as `<name>_hex_s_n.png` —
    # baseline cell; per-ribi composition is the next layer (TODO.md).
    out_path = args.out / f"{args.name}_hex_s_n.png"
    _render_to(out_path)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
