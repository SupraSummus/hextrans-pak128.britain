"""Bake the 4wheel-1850s-first passenger carriage.

First asset under the per-asset template (`CLAUDE.md` -> "Per-asset
directory layout").  Drives `tools/threed/hex_render.py` against the
upstream blend.

Run from anywhere:

    python3 vehicles/trains/4wheel_1850s_first/bake.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
NAME = "4wheel-1850s-first"
BLEND_PATH = "trains/Carriages/4wheel-1850.blend"


def main() -> int:
    sys.path.insert(0, str(HERE.parents[2] / "tools" / "threed"))
    from fetch_blend import fetch  # noqa: E402

    blend = fetch(BLEND_PATH)
    script = HERE.parents[2] / "tools" / "threed" / "hex_render.py"
    cmd = [
        "blender", "-b", str(blend), "-P", str(script),
        "--",
        "--out", str(HERE),
        "--name", NAME,
        "--views", "8",
    ]
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
