"""Per-asset bake driver — shrinks bake scripts to their essentials.

A bake script's job is to declare:

  - the asset's `SPEC` (`Vehicle`, holds gameplay data)
  - the upstream blend path

`bake_vehicle` does the rest: fetch the blend, run the hex
renderer to produce the atlas PNG, write the dat next to it.
Bake scripts collapse to ~10 lines of imports + spec + a
one-line `bake_vehicle(...)` call at `__main__` time.

Multi-object bake units call `bake_vehicle` once per output,
passing distinct `basename` (and typically distinct `blend`)
per call.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from pak import REPO_ROOT
from pak.dat import Vehicle, Way, emit_vehicle, emit_way
from pak.fetch_blend import fetch


_RENDER_SCRIPT = Path(__file__).resolve().parent / "render.py"
_BAKE_WAY_SCRIPT = Path(__file__).resolve().parent / "bake_way.py"


def bake_vehicle(
    spec: Vehicle,
    *,
    blend: str,
    basename: str,
    out_dir: Path,
    viewpoint: str = "hex",
) -> Path:
    """Fetch the blend, render `<out_dir>/<basename>.png`, emit
    `<out_dir>/<basename>.dat` from `spec`.

    `blend` is the path inside the upstream blends repo (resolved
    via `fetch_blend.fetch` against the global `blends.lock` SHA).
    `basename` is the shared filesystem stem for both atlas and
    dat — typically the bake script's `Path(__file__).stem`.
    Returns the dat path.
    """
    blend_path = fetch(blend)
    cmd = [
        "blender", "-b", str(blend_path), "-P", str(_RENDER_SCRIPT),
        "--",
        "--out", str(out_dir),
        "--name", basename,
        "--viewpoint", viewpoint,
    ]
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)

    out_dat = emit_vehicle(spec, out_dir=out_dir, basename=basename)
    try:
        print(f"wrote {out_dat.relative_to(REPO_ROOT)}", flush=True)
    except ValueError:
        print(f"wrote {out_dat}", flush=True)
    return out_dat


def bake_main(spec: Vehicle, blend: str, file: str) -> Path:
    """Convenience for single-vehicle bake scripts.

    Derives `out_dir` and `basename` from the calling script's
    `__file__`, so each bake script's bottom collapses to:

        if __name__ == "__main__":
            bake_main(SPEC, BLEND, __file__)

    Multi-object bake units call `bake_vehicle` directly per
    output instead.
    """
    path = Path(file).resolve()
    return bake_vehicle(
        spec, blend=blend, basename=path.stem, out_dir=path.parent,
    )


def bake_way(
    spec: Way,
    *,
    blend: str,
    basename: str,
    out_dir: Path,
    strip: str = "Sphere",
    samples: int = 32,
) -> Path:
    """Drive `pak/bake_way.py` to render `<out_dir>/<basename>.png`,
    then emit `<out_dir>/<basename>.dat` from `spec`.

    `blend` is the path inside the upstream blends repo (resolved by
    `bake_way.py` via `fetch_blend.fetch`).  `strip` is a comma-
    separated list of mesh names to drop on entry — default `Sphere`
    (the upstream sun-direction visualizer); per-blend overrides go
    here when a blend ships extra debug meshes that don't belong in
    the bake (see `CLAUDE.md` -> "Way-bake architecture" -> Naming
    pitfall).  Returns the dat path.
    """
    cmd = [
        "blender", "-b", "-P", str(_BAKE_WAY_SCRIPT),
        "--",
        "--blend", blend,
        "--name", basename,
        "--out", str(out_dir),
        "--strip", strip,
        "--samples", str(samples),
    ]
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)

    out_dat = emit_way(spec, out_dir=out_dir, basename=basename)
    try:
        print(f"wrote {out_dat.relative_to(REPO_ROOT)}", flush=True)
    except ValueError:
        print(f"wrote {out_dat}", flush=True)
    return out_dat


def bake_way_main(
    spec: Way, blend: str, file: str, *, strip: str = "Sphere",
) -> Path:
    """Convenience for single-way bake scripts.

    Derives `out_dir` and `basename` from the calling script's
    `__file__`, so each bake script's bottom collapses to:

        if __name__ == "__main__":
            bake_way_main(SPEC, BLEND, __file__)
    """
    path = Path(file).resolve()
    return bake_way(
        spec, blend=blend, basename=path.stem, out_dir=path.parent,
        strip=strip,
    )
