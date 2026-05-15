"""Stage upstream PNGs alongside a committed dat for makeobj.

A handful of committed dats depend on PNG siblings that were stripped
from history (CLAUDE.md → "Repo size strategy") and have no hex
re-bake yet:

* `gui/gui64/*.dat`, `gui/gui128/*.dat` — engine-required cursor /
  symbol / skin objects (Construction, GeneralTools, Logo,
  Passagiere…).  GUI elements don't carry the world's hex-projection
  burden so the upstream 64/128-px bitmaps render verbatim under hex.
* `grounds/fences.dat` — the last engine-required ground descriptor
  without a hex bake.

Without these, `pakset_manager_t::resolve_xrefs` and
`{skinverwaltung_t,ground_desc_t}::successfully_loaded` fatal at
load.  This module parses each dat's image refs, fetches every
referenced PNG from the upstream pak repo via `fetch_pak`, and
copies dat + PNGs into a staging dir laid out for makeobj (image
refs are resolved relative to the dat path, so source geometry
has to be preserved).

Same SHA-pinned `pak.lock` + TOFU pattern as `pak.fetch_wavs`.

Usage: python3 -m pak.stage_upstream_pngs <dest> <dat> [<dat>...]
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from . import REPO_ROOT
from .fetch_pak import fetch


# Captures `<basename>` from `Image[...]=<basename>.<row>.<col>` with
# optional layer brackets, optional leading `>` or `./`, and an
# optional `.<z>` suffix.  Covers gui flat refs
# (`Image[0]=construction-site.0.0`) and grounds layered refs
# (`Image[0][0]=images/fence-3.0.0`) in one pass; basenames may carry
# a relative subpath like `images/` so `[A-Za-z0-9_./-]+` covers
# slashes.
_IMAGE_REF_RE = re.compile(
    r"^\s*[Ii]mage(?:\[[^\]]+\])*\s*=\s*>?\s*\.?/?"
    r"([A-Za-z0-9_./-]+?)(?:\.\d+){2,3}\s*$"
)


def png_refs(dat: Path) -> set[str]:
    """Every PNG basename referenced by `dat`, dat-relative."""
    names: set[str] = set()
    for line in dat.read_text().splitlines():
        m = _IMAGE_REF_RE.match(line)
        if m:
            names.add(m.group(1))
    return names


def stage(dat: Path, dest_root: Path) -> None:
    """Copy `dat` to `<dest_root>/<rel-dir>/`, fetch each PNG ref."""
    rel_dir = dat.parent.relative_to(REPO_ROOT)
    out_dir = dest_root / rel_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(dat, out_dir / dat.name)
    for name in sorted(png_refs(dat)):
        png_rel = f"{rel_dir.as_posix()}/{name}.png"
        dest = dest_root / png_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fetch(png_rel), dest)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    dest = Path(argv[0])
    for dat in argv[1:]:
        stage(Path(dat).resolve(), dest)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
