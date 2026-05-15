"""Fetch every `.wav` referenced by a ported asset's bake unit.

Walks every per-asset bake script (`pak.bake_units.discover`),
reads `SPEC.sound`, and pulls each unique wav from the upstream pak
repo via `fetch_pak` into `<dest>/`.  Sound effects were stripped from
this repo's history (CLAUDE.md -> "Repo size strategy") so the
build's `copy` step stages them on demand.

Reading the bake-unit `.py` keeps the source of truth singular —
the same `SPEC: Vehicle` that drives `emit_vehicle` also names the
wav.  The committed `.dat` is the derived artefact; never read it
here.

Usage: python3 -m pak.fetch_wavs <dest-dir>
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from .bake_units import discover, import_script
from .dat import Vehicle
from .fetch_pak import fetch


def collect() -> set[str]:
    """Every `.wav` named by a ported bake unit's `SPEC.sound`."""
    wavs: set[str] = set()
    for script in discover():
        spec = getattr(import_script(script), "SPEC", None)
        if isinstance(spec, Vehicle) and spec.sound:
            wavs.add(spec.sound)
    return wavs


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    dest = Path(argv[0])
    dest.mkdir(parents=True, exist_ok=True)
    for name in sorted(collect()):
        shutil.copy2(fetch(f"sound/{name}"), dest / name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
