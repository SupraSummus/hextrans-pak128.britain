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

from tools.threed.dat import Vehicle, emit_vehicle
from tools.threed.fetch_blend import fetch


_REPO = Path(__file__).resolve().parents[2]
_RENDER_SCRIPT = _REPO / "tools" / "threed" / "render.py"


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
        print(f"wrote {out_dat.relative_to(_REPO)}", flush=True)
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
